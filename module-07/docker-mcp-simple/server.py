#!/usr/bin/env python3
"""Simple Docker MCP Server using Docker CLI directly."""

# Standard library imports
import asyncio  # For async/await support
import subprocess  # To execute Docker CLI commands
import sys  # For system operations and exit
import os  # For process ID access
import atexit  # To clean up lock file on exit
from pathlib import Path  # For file path operations
from concurrent.futures import ThreadPoolExecutor  # To run blocking Docker commands in threads

# MCP (Model Context Protocol) imports
from mcp.server import Server  # type: ignore  # Main MCP server class
from mcp.server.stdio import stdio_server  # type: ignore  # STDIO transport for MCP communication
from mcp.types import Tool, TextContent  # type: ignore  # MCP type definitions

# Prevent duplicate server instances (Windows Cursor bug workaround)
# This lock file prevents multiple instances from running simultaneously,
# which can cause issues with STDIO communication
LOCK_FILE = Path(__file__).parent / ".server.lock"

def acquire_lock():
    """
    Acquire lock or exit if another instance is running.
    
    Checks if a lock file exists and if the process ID in it is still running.
    If another instance is active, this process exits silently to avoid conflicts.
    Otherwise, creates a lock file with the current process ID.
    """
    if LOCK_FILE.exists():
        try:
            # Read the process ID from the lock file
            pid = int(LOCK_FILE.read_text().strip())
            # Check if process is still running (Windows-specific check)
            # Uses tasklist command to verify the process exists
            result = subprocess.run(["tasklist", "/FI", f"PID eq {pid}"], capture_output=True, text=True, stdin=subprocess.DEVNULL)
            if str(pid) in result.stdout:
                sys.exit(0)  # Another instance is running, exit silently
        except:
            # If lock file is corrupted or check fails, continue anyway
            pass
    # Write current process ID to lock file
    LOCK_FILE.write_text(str(os.getpid()))
    # Register cleanup function to remove lock file when process exits
    atexit.register(lambda: LOCK_FILE.unlink(missing_ok=True))

acquire_lock()

# Initialize the MCP server with a unique name
server = Server("docker-mcp-simple")

# Thread pool executor for running blocking Docker commands
# Docker CLI commands are synchronous, so we run them in threads to avoid
# blocking the async event loop. Max 4 workers allows concurrent operations.
executor = ThreadPoolExecutor(max_workers=4)


def _run_docker_sync(args: list[str]) -> str:
    """
    Run docker command synchronously (for thread pool).
    
    This function runs blocking Docker CLI commands. It's designed to be executed
    in a thread pool to avoid blocking the async event loop.
    
    Args:
        args: List of Docker command arguments (e.g., ["ps", "-a"])
    
    Returns:
        Command output as string, or error message if command fails
    """
    try:
        # Execute Docker command with 60 second timeout
        # stdin=subprocess.DEVNULL prevents Docker from trying to read from stdin
        result = subprocess.run(
            ["docker"] + args,
            capture_output=True,  # Capture both stdout and stderr
            text=True,  # Return output as string, not bytes
            timeout=60,  # Prevent hanging commands
            stdin=subprocess.DEVNULL  # Don't allow stdin input
        )
        # Check if command failed (non-zero return code)
        if result.returncode != 0:
            return f"Error: {result.stderr}"
        # Return output or success message if no output
        return result.stdout or "Command completed successfully"
    except subprocess.TimeoutExpired:
        return "Error: Command timed out"
    except Exception as e:
        return f"Error: {str(e)}"


async def run_docker_command(args: list[str]) -> str:
    """
    Run a docker command asynchronously using thread pool.
    
    This is the async wrapper that runs the blocking Docker command in a thread,
    allowing the event loop to continue processing other requests.
    
    Args:
        args: List of Docker command arguments
    
    Returns:
        Command output as string
    """
    loop = asyncio.get_event_loop()
    # Run the blocking function in the thread pool executor
    return await loop.run_in_executor(executor, _run_docker_sync, args)


@server.list_tools()
async def list_tools() -> list[Tool]:
    """
    List available Docker tools.
    
    This function is called by the MCP client to discover what tools are available.
    Each Tool defines its name, description, and input schema (parameters).
    """
    return [
        # Tool to list Docker containers
        Tool(
            name="list-containers",
            description="List all Docker containers",
            inputSchema={
                "type": "object",
                "properties": {
                    "all": {
                        "type": "boolean",
                        "description": "Show all containers (including stopped)",
                        "default": True
                    }
                }
            }
        ),
        # Tool to retrieve container logs
        Tool(
            name="get-logs",
            description="Get logs from a Docker container",
            inputSchema={
                "type": "object",
                "properties": {
                    "container": {
                        "type": "string",
                        "description": "Container name or ID"
                    },
                    "tail": {
                        "type": "integer",
                        "description": "Number of lines to show",
                        "default": 100
                    }
                },
                "required": ["container"]  # Container is required parameter
            }
        ),
        # Tool to inspect container details
        Tool(
            name="container-info",
            description="Get detailed information about a container",
            inputSchema={
                "type": "object",
                "properties": {
                    "container": {
                        "type": "string",
                        "description": "Container name or ID"
                    }
                },
                "required": ["container"]
            }
        ),
        # Tool to list Docker images
        Tool(
            name="list-images",
            description="List Docker images",
            inputSchema={
                "type": "object",
                "properties": {}  # No parameters needed
            }
        ),
        # Tool to show container resource usage
        Tool(
            name="docker-stats",
            description="Show container resource usage statistics",
            inputSchema={
                "type": "object",
                "properties": {}  # No parameters needed
            }
        ),
        # Tool to test server connectivity
        Tool(
            name="ping",
            description="Test if server is responding",
            inputSchema={
                "type": "object",
                "properties": {}  # No parameters needed
            }
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """
    Handle tool calls from MCP clients.
    
    This function is invoked when a client requests to execute a tool.
    It routes the request to the appropriate Docker command handler.
    
    Args:
        name: Name of the tool to execute
        arguments: Dictionary of tool parameters
    
    Returns:
        List of TextContent objects containing the tool output
    """
    
    if name == "list-containers":
        # Get the 'all' parameter (defaults to True to show stopped containers)
        show_all = arguments.get("all", True)
        # Build Docker ps command with custom format for readable table output
        # Format includes: ID, Names, Image, Status, and Ports
        args = ["ps", "--format", "table {{.ID}}\t{{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}"]
        if show_all:
            # Insert -a flag to show all containers (including stopped)
            args.insert(1, "-a")
        output = await run_docker_command(args)
        
    elif name == "get-logs":
        # Extract container name/ID and tail parameter
        container = arguments.get("container")
        tail = arguments.get("tail", 100)  # Default to last 100 lines
        # Run docker logs with tail option
        output = await run_docker_command(["logs", "--tail", str(tail), container])
        
    elif name == "container-info":
        # Extract container name/ID
        container = arguments.get("container")
        # Use docker inspect with Go template to format output nicely
        # Template extracts: Name, Image, Status, Created time, and Port mappings
        output = await run_docker_command(["inspect", "--format", 
            "Name: {{.Name}}\nImage: {{.Config.Image}}\nStatus: {{.State.Status}}\nCreated: {{.Created}}\nPorts: {{range $p, $conf := .NetworkSettings.Ports}}{{$p}}->{{(index $conf 0).HostPort}} {{end}}", 
            container])
        
    elif name == "list-images":
        # List Docker images with formatted table output
        # Shows: Repository, Tag, Size, and time since creation
        output = await run_docker_command(["images", "--format", "table {{.Repository}}\t{{.Tag}}\t{{.Size}}\t{{.CreatedSince}}"])
        
    elif name == "docker-stats":
        # Show container statistics (CPU, memory, network I/O)
        # --no-stream: Show stats once instead of continuously updating
        output = await run_docker_command(["stats", "--no-stream", "--format", "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}"])
    
    elif name == "ping":
        # Simple health check - no Docker command needed
        output = "pong - server is alive!"
        
    else:
        # Unknown tool requested
        output = f"Unknown tool: {name}"
    
    # Return output wrapped in MCP TextContent format
    return [TextContent(type="text", text=output)]


async def main():
    """
    Run the MCP server.
    
    Sets up STDIO communication channels (stdin/stdout) and starts the server.
    The server will listen for MCP protocol messages on stdin and respond on stdout.
    This allows the server to communicate with MCP clients via standard input/output.
    """
    # Create STDIO transport - reads from stdin, writes to stdout
    # This is the standard way MCP servers communicate with clients
    async with stdio_server() as (read_stream, write_stream):
        # Run the server with the read/write streams and initialization options
        await server.run(
            read_stream,  # Input stream for receiving MCP requests
            write_stream,  # Output stream for sending MCP responses
            server.create_initialization_options()  # Server capabilities and metadata
        )


if __name__ == "__main__":
    # Entry point: start the async event loop and run the server
    asyncio.run(main())

