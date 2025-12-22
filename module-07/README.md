# MCP Servers Installation Guide

This guide provides step-by-step installation instructions for the two MCP (Model Context Protocol) servers configured in this project: MCP Toolbox for Databases for database management and Docker MCP for container management.

## Table of Contents

- [Prerequisites](#prerequisites)
- [MCP Toolbox for Databases Installation](#1-mcp-toolbox-for-databases)
- [Docker Local Installation](#2-docker-mcp-simple)
- [Configuring MCP Servers](#configuring-mcp-servers)
  - [Cursor IDE Configuration](#cursor-ide-configuration)
  - [Claude Code Configuration](#claude-code-configuration)
- [Verification Steps](#verification-steps)
- [Troubleshooting](#troubleshooting)
- [Natural Language Usage Examples](#natural-language-usage-examples)
- [Additional Resources](#additional-resources)

---

## Prerequisites

Before installing the MCP servers, ensure you have the following installed:

- **Windows 10/11** (current setup)
- **Docker Desktop** or **Docker Engine** (latest version recommended)
- **UV Package Manager** (Python package manager)
- **Python 3.12+** (required for UV)
- **Cursor IDE** or **Claude Code** (for MCP integration)
  - At least one of these IDEs is required to use the MCP servers

---

## 1. MCP Toolbox for Databases

**MCP Toolbox for Databases** is an open source MCP server for databases that provides comprehensive database management and analysis tools for PostgreSQL, with special support for vector databases using the pgvector extension. It supports multiple database types including PostgreSQL, MySQL, MariaDB, SQL Server, and SQLite.

**Official Repository**: [https://github.com/googleapis/genai-toolbox](https://github.com/googleapis/genai-toolbox)  
**Documentation**: [https://googleapis.github.io/genai-toolbox/getting-started/introduction/](https://googleapis.github.io/genai-toolbox/getting-started/introduction/)

### Installation Steps

#### Step 1: Ensure Docker is Running

Before installing MCP Toolbox for Databases, verify that Docker is running:

```bash
# Check Docker version
docker --version

# Verify Docker daemon is running
docker ps
```

If Docker is not running, start Docker Desktop or your Docker service.

#### Step 2: Pull the MCP Toolbox for Databases Image

Pull the latest MCP Toolbox for Databases Docker image:

```bash
# Pull the latest MCP Toolbox for Databases image
docker pull us-central1-docker.pkg.dev/database-toolbox/toolbox/toolbox:latest
```

**Note:** This image is pulled from Google's Artifact Registry. Ensure you have internet connectivity. For alternative installation methods, see the [official documentation](https://googleapis.github.io/genai-toolbox/getting-started/introduction/).

#### Step 3: Set Up PostgreSQL Database

MCP Toolbox for Databases requires a database connection. If you don't already have a PostgreSQL database with pgvector, set one up:

```bash
# Start PostgreSQL with pgvector extension
docker run -d \
  --name postgres-pgvector \
  -e POSTGRES_DB=n8n_rag \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=your_secure_password \
  -p 5432:5432 \
  pgvector/pgvector:pg16
```

**Important:** Replace `your_secure_password` with a strong, secure password.

**For Windows PowerShell, use this format:**
```powershell
docker run -d `
  --name postgres-pgvector `
  -e POSTGRES_DB=n8n_rag `
  -e POSTGRES_USER=postgres `
  -e POSTGRES_PASSWORD=your_secure_password `
  -p 5432:5432 `
  pgvector/pgvector:pg16
```

#### Step 4: Verify Database Connection

Test that your PostgreSQL database is accessible:

```bash
# Test database connection
docker exec -it postgres-pgvector psql -U postgres -d n8n_rag -c "SELECT version();"
```

You should see PostgreSQL version information. If the connection fails, check:
- Container is running: `docker ps`
- Container logs: `docker logs postgres-pgvector`
- Port 5432 is not in use by another service

#### Step 5: Create tools.yaml Configuration File

MCP Toolbox for Databases requires a `tools.yaml` configuration file that defines your database connection. Create this file:

1. **Create a directory for your MCP configuration** (optional, but recommended):
   ```bash
   # Windows PowerShell
   mkdir $env:USERPROFILE\.mcp-toolbox
   
   # Or create it manually in: C:\Users\<YourUsername>\.mcp-toolbox
   ```

2. **Create the `tools.yaml` file** in that directory with the following content:

   **File location:** `C:\Users\<YourUsername>\.mcp-toolbox\tools.yaml`

   ```yaml
   sources:
     postgres:
       kind: postgres
       host: postgres-pgvector
       port: 5432
       database: n8n_rag
       user: postgres
       password: your_secure_password
   ```

   **Important:** 
   - Replace `your_secure_password` with the actual PostgreSQL password you set in Step 3
   - The `host` should be the container name (`postgres-pgvector`) when both containers are on the same Docker network
   - If running PostgreSQL outside Docker, use `host.docker.internal`, `localhost`, or `127.0.0.1`
   - Save this file - you'll need to reference its path in the next step

### Configure MCP Toolbox for Databases in Your IDE

After installing the Docker image and setting up your database, you need to configure MCP Toolbox for Databases in Cursor or Claude Code.

#### Cursor IDE Configuration

1. **Open Cursor Settings**:
   - Press `Ctrl + Shift + J` (or `Cmd + Shift + J` on Mac) to open Settings in Cursor > 2.0
   - Search for "MCP" in the settings search bar
   - Click on **"MCP Servers"** or **"Model Context Protocol"**
   - Click **"Add Server"** or the **"+"** button

   **Alternative: Direct File Edit**
   
   If you prefer to edit the configuration file directly, locate the Cursor MCP settings file:
   
   **Windows Path (common locations):**
   ```
   %APPDATA%\Cursor\User\settings.json
   ```
   or
   ```
   %USERPROFILE%\.cursor\config\mcp.json
   ```
   
   **Note:** The exact path may vary depending on your Cursor version. Check Cursor's documentation or use the Settings UI method above.

2. **Add MCP Toolbox for Databases Configuration**:
   
   In the MCP server configuration, add the following JSON configuration. **Important:** Replace `<YourUsername>` with your actual Windows username and adjust the network name if needed:
   
   ```json
   {
     "mcpServers": {
       "mcp-db": {
         "command": "docker",
         "args": [
           "run",
           "-i",
           "--rm",
           "--network",
           "n8n-simple-private-rag_n8n-network",
           "-e",
           "POSTGRES_HOST=postgres-pgvector",
           "-e",
           "POSTGRES_USER=postgres",
           "-e",
           "POSTGRES_PASSWORD=your_secure_password",
           "-e",
           "POSTGRES_DATABASE=n8n_rag",
           "-e",
           "POSTGRES_PORT=5432",
           "-v",
           "C:/Users/<YourUsername>/.mcp-toolbox:/config",
           "-w",
           "/config",
           "us-central1-docker.pkg.dev/database-toolbox/toolbox/toolbox:latest",
           "--stdio",
           "--prebuilt",
           "postgres"
         ],
         "env": {}
       }
     }
   }
   ```
   
   **Configuration Explanation:**
   - `--network` connects the container to the same Docker network as PostgreSQL (required for container-to-container communication)
   - `-e POSTGRES_*` environment variables are required for the `--prebuilt postgres` configuration
   - `--stdio` enables MCP stdio mode for communication with the IDE
   - `--prebuilt postgres` loads all pre-built PostgreSQL tools automatically
   - `-v` mounts your local `tools.yaml` directory into the container at `/config`
   - `-w /config` sets the working directory so the container can find `tools.yaml`
   
   **Important:** 
   - Replace `<YourUsername>` with your actual Windows username
   - Replace `your_secure_password` with your actual PostgreSQL password
   - Replace `n8n-simple-private-rag_n8n-network` with your actual Docker network name (find it with `docker network ls`)
   - Use forward slashes `/` in the path for Windows compatibility

3. **Save and Restart**:
   - Save the configuration file
   - **Restart Cursor IDE** completely (close and reopen)
   - The MCP server should now be available

#### Claude Code Configuration

1. **Locate Configuration File**:
   
   **Windows Path:**
   ```
   %APPDATA%\Claude\claude_desktop_config.json
   ```
   
   Or navigate to:
   ```
   C:\Users\<YourUsername>\AppData\Roaming\Claude\claude_desktop_config.json
   ```
   
   **Note:** If the file doesn't exist, create it.

2. **Add MCP Toolbox for Databases Configuration**:
   
   Open (or create) the `claude_desktop_config.json` file and add the following configuration. **Important:** Replace `<YourUsername>` with your actual Windows username and adjust the network name if needed:
   
   ```json
   {
     "mcpServers": {
       "mcp-db": {
         "command": "docker",
         "args": [
           "run",
           "-i",
           "--rm",
           "--network",
           "n8n-simple-private-rag_n8n-network",
           "-e",
           "POSTGRES_HOST=postgres-pgvector",
           "-e",
           "POSTGRES_USER=postgres",
           "-e",
           "POSTGRES_PASSWORD=your_secure_password",
           "-e",
           "POSTGRES_DATABASE=n8n_rag",
           "-e",
           "POSTGRES_PORT=5432",
           "-v",
           "C:/Users/<YourUsername>/.mcp-toolbox:/config",
           "-w",
           "/config",
           "us-central1-docker.pkg.dev/database-toolbox/toolbox/toolbox:latest",
           "--stdio",
           "--prebuilt",
           "postgres"
         ],
         "env": {}
       }
     }
   }
   ```
   
   **Configuration Explanation:**
   - `--network` connects the container to the same Docker network as PostgreSQL
   - `-e POSTGRES_*` environment variables are required for the `--prebuilt postgres` configuration
   - `--stdio` enables MCP stdio mode for communication with the IDE
   - `--prebuilt postgres` loads all pre-built PostgreSQL tools automatically
   - `-v` mounts your local `tools.yaml` directory into the container at `/config`
   
   **Important:** 
   - Replace `<YourUsername>` with your actual Windows username
   - Replace `your_secure_password` with your actual PostgreSQL password
   - Replace `n8n-simple-private-rag_n8n-network` with your actual Docker network name
   - Use forward slashes `/` in the path for better compatibility

3. **Save and Restart**:
   - Save the configuration file
   - **Restart Claude Code** completely
   - The MCP server should now be available

#### Configuration Notes

- **Server Name**: The server name `mcp-db` can be customized to your preference
- **Docker Network**: The `--network` flag is essential for container-to-container communication
- **Environment Variables**: The `POSTGRES_*` environment variables are required for `--prebuilt postgres` mode
- **tools.yaml File**: The source connection is also configured in the `tools.yaml` file
- **Database Host**: Use the PostgreSQL container name (`postgres-pgvector`) when both containers are on the same Docker network
- **--stdio Flag**: Required for MCP stdio mode communication with the IDE
- **--prebuilt postgres**: Automatically loads all pre-built PostgreSQL tools (execute_sql, list_tables, list_indexes, etc.)
- **Password**: Make sure the password in both environment variables and `tools.yaml` matches what you set when creating the PostgreSQL container
- **Volume Mount**: The Docker container must have access to the `tools.yaml` file via the volume mount (`-v` flag)

#### Verify Configuration

After restarting your IDE, test the configuration:

```bash
# In Cursor/Claude Code chat, try:
@mcp-db list tables
```

Expected result: A list of all tables in your PostgreSQL database, or an empty list if no tables exist yet.

### Available Tools

MCP Toolbox for Databases provides comprehensive database management capabilities:

- **Database Analysis**: Monitor PostgreSQL performance, health, and statistics
- **Query Optimization**: Generate EXPLAIN plans and analyze query performance
- **Extension Management**: Install and manage PostgreSQL extensions (including pgvector)
- **Performance Monitoring**: Track slow queries, active connections, and resource usage
- **Vector Database Support**: Optimized for AI/ML workloads with pgvector extension
- **Schema Management**: Inspect tables, indexes, and database structure
- **Health Checks**: Identify bloated tables, dead tuples, and configuration issues

### Usage Examples

Once configured in Cursor or Claude Code, use MCP Toolbox for Databases with natural language commands:

```bash
# Basic commands
@mcp-db give me a summary report about my database
@mcp-db list tables
```

#### Natural Language Examples

You can interact with the database using plain English:

```
# Explore database structure
"Show me all tables in my database and their column types"

# Understand vector data
"How many document chunks are stored in the n8n_vectors table and what's the average text length?"

# Analyze content sources
"List all unique document sources from the metadata and count how many chunks each has"

# Find specific content
"Search for all chunks that mention 'VMware' or 'virtualization' in the text"

# Database health check
"Check if there are any bloated tables or dead tuples that need vacuuming"

# Performance monitoring
"Show me the slowest queries that have run against this database"

# Index analysis
"Which indexes exist on my tables and are they being used efficiently?"

# Storage analysis
"What's the total size of my database and how much space does each table use?"

# Connection monitoring
"How many active connections are there to the database right now?"

# Configuration review
"Show me the current PostgreSQL memory and autovacuum settings"

# Optimization suggestions
"Can you suggest any optimizations for my database?"
"Are there any missing indexes that could improve query performance?"

# Backup and export
"Can you make a backup of my database?"
"How can I export data from the n8n_vectors table to CSV?"
"Generate a SQL script to dump my table structure"

# Data management
"Can you help me clean up old or duplicate records?"
"What's the best way to archive data from this table?"
```

---

## 2. Docker MCP Simple

Docker MCP Simple is a lightweight MCP server that provides a natural language interface for managing Docker containers and images directly from Cursor. It uses the Docker CLI directly for fast and reliable performance.

**Location**: `module-07/docker-mcp-simple/`

### Installation Steps

#### Step 1: Install UV Package Manager

UV is a fast Python package installer and resolver. Install it using one of the following methods:

**Option A: PowerShell (Recommended for Windows)**
```powershell
# Run in PowerShell (may require Administrator privileges)
irm https://astral.sh/uv/install.ps1 | iex
```

**Option B: Using pip**
```bash
pip install uv
```

**Verify UV Installation:**
```bash
uv --version
```

#### Step 2: Install Dependencies

Navigate to the docker-mcp-simple directory and sync dependencies:

```bash
cd module-07/docker-mcp-simple
uv sync
```

#### Step 3: Verify Installation

Test that the MCP server works correctly:

```bash
cd module-07/docker-mcp-simple
echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"1.0"}}}' | uv run python server.py
```

You should see a JSON response with server information.

### Available Tools

Docker MCP Simple provides the following tools:

- **list-containers**: List all Docker containers (running and stopped)
- **get-logs**: Get logs from a specific container
- **container-info**: Get detailed information about a container
- **list-images**: List all Docker images
- **docker-stats**: Show container resource usage statistics

### Usage Examples

Once installed and configured in Cursor or Claude Code, you can use Docker MCP with natural language commands:

```bash
# Quick health check - is my Docker MCP working?
@docker-local ping

# What's running on my machine right now?
@docker-local list containers

# Deep dive into a specific container
@docker-local container info postgres-pgvector

# Debugging: why is my n8n workflow failing?
@docker-local get logs n8n

# Resource check before deploying something new
@docker-local docker stats

# Spring cleaning - what images am I hoarding?
@docker-local list images
```

**Pro tip:** Combine with natural language for context:
```
"Show me container info for n8n - I think it crashed"
"Get the last 50 lines of postgres logs, looking for connection errors"
"What containers are eating up my RAM?"
"Is my database container still alive after that power outage?"
"Check if n8n is hogging CPU - my laptop fan is going crazy"
"What version of postgres am I running?"
"Show me what's happening in the toolbox container - it seems stuck"
"List all my containers - I forgot what I have running"
"Which container is using port 5432?"
"Give me a health check on all my Docker services"
```

---

## Configuring MCP Servers

After installing the MCP servers, you need to configure them in your IDE. This section covers configuration for both **Cursor IDE** and **Claude Code**.

### Cursor IDE Configuration

Cursor uses a JSON configuration file to manage MCP servers. Follow these steps to enable both servers:

#### Step 1: Open Cursor Settings

1. Open Cursor IDE
2. Press `Ctrl + Shift + J` (or `Cmd + Shift + J` on Mac) to open Settings in Cursor > 2.0
3. Search for "MCP" in the settings search bar
4. Click on **"MCP Servers"** or **"Model Context Protocol"**
5. Click **"Add Server"** or the **"+"** button

**Alternative: Direct File Edit**

If you prefer to edit the configuration file directly, locate the Cursor MCP settings file:

**Windows Path (common locations):**
```
%APPDATA%\Cursor\User\settings.json
```
or
```
%USERPROFILE%\.cursor\config\mcp.json
```

**Note:** The exact path may vary depending on your Cursor version. Check Cursor's documentation or use the Settings UI method above.

#### Step 2: Edit MCP Configuration

In the MCP server configuration (either through the UI or by editing the file), add the following configuration:

```json
{
  "mcpServers": {
    "docker-local": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "<path-to-project>/module-07/docker-mcp-simple",
        "python",
        "server.py"
      ],
      "env": {}
    },
    "mcp-db": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "--network",
        "n8n-simple-private-rag_n8n-network",
        "-e",
        "POSTGRES_HOST=postgres-pgvector",
        "-e",
        "POSTGRES_USER=postgres",
        "-e",
        "POSTGRES_PASSWORD=your_secure_password",
        "-e",
        "POSTGRES_DATABASE=n8n_rag",
        "-e",
        "POSTGRES_PORT=5432",
        "-v",
        "C:/Users/<YourUsername>/.mcp-toolbox:/config",
        "-w",
        "/config",
        "us-central1-docker.pkg.dev/database-toolbox/toolbox/toolbox:latest",
        "--stdio",
        "--prebuilt",
        "postgres"
      ],
      "env": {}
    }
  }
}
```

**Important Configuration Notes:**

1. **Docker MCP**: 
   - Uses `uvx` command to run the Docker MCP server
   - No additional environment variables required
   - Ensure `uvx` is in your system PATH

2. **MCP Toolbox for Databases**:
   - Uses Docker to run the toolbox container
   - **Requires a `tools.yaml` file** (created in [Step 5 of MCP Toolbox for Databases installation](#step-5-create-toolsyaml-configuration-file))
   - `--network` connects to the same Docker network as PostgreSQL for container-to-container communication
   - `-e POSTGRES_*` environment variables are required for the `--prebuilt postgres` mode
   - `--stdio` enables MCP stdio mode for IDE communication
   - `--prebuilt postgres` loads all pre-built PostgreSQL tools (execute_sql, list_tables, etc.)
   - Replace `<YourUsername>` with your actual Windows username
   - Replace `your_secure_password` with your actual PostgreSQL password
   - Replace `n8n-simple-private-rag_n8n-network` with your Docker network name

#### Step 3: Save and Restart

1. Save the configuration file
2. **Restart Cursor IDE** completely (close and reopen)
3. The MCP servers should now be available

#### Step 4: Verify in Cursor

1. Open Cursor's chat interface
2. Look for MCP server indicators in the chat UI
3. Try using the servers with commands like:
   - `@docker-local list containers`
   - `@mcp-db list tables`

**Alternative: Using Cursor Settings UI**

If Cursor provides a UI for MCP configuration:

1. Go to **Settings** → **Features** → **MCP Servers**
2. Click **"Add MCP Server"** or **"Configure"**
3. Add each server with the configuration above
4. Save and restart Cursor

---

### Claude Code Configuration

Claude Code (Claude Desktop) uses a JSON configuration file to manage MCP servers. Follow these steps:

#### Step 1: Locate Configuration File

**Windows Path:**
```
%APPDATA%\Claude\claude_desktop_config.json
```

Or navigate to:
```
C:\Users\<YourUsername>\AppData\Roaming\Claude\claude_desktop_config.json
```

**Note:** If the file doesn't exist, create it.

#### Step 2: Edit Configuration File

Open (or create) the `claude_desktop_config.json` file and add the following configuration:

```json
{
  "mcpServers": {
    "docker-local": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "<path-to-project>/module-07/docker-mcp-simple",
        "python",
        "server.py"
      ],
      "env": {}
    },
    "mcp-db": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "--network",
        "n8n-simple-private-rag_n8n-network",
        "-e",
        "POSTGRES_HOST=postgres-pgvector",
        "-e",
        "POSTGRES_USER=postgres",
        "-e",
        "POSTGRES_PASSWORD=your_secure_password",
        "-e",
        "POSTGRES_DATABASE=n8n_rag",
        "-e",
        "POSTGRES_PORT=5432",
        "-v",
        "C:/Users/<YourUsername>/.mcp-toolbox:/config",
        "-w",
        "/config",
        "us-central1-docker.pkg.dev/database-toolbox/toolbox/toolbox:latest",
        "--stdio",
        "--prebuilt",
        "postgres"
      ],
      "env": {}
    }
  }
}
```

**Important:** 
- Replace `<YourUsername>` with your actual Windows username
- Replace `your_secure_password` with your actual PostgreSQL password
- Replace `n8n-simple-private-rag_n8n-network` with your Docker network name (find with `docker network ls`)
- The `--prebuilt postgres` flag automatically provides all PostgreSQL tools
- You still need the `tools.yaml` file for the source configuration

#### Step 3: Save and Restart

1. Save the configuration file
2. **Restart Claude Code** completely
3. The MCP servers should now be available

#### Step 4: Verify in Claude Code

1. Open Claude Code
2. Check the MCP servers status (usually visible in the interface)
3. Try using the servers in a conversation:
   - Ask: "List all Docker containers using docker-local"
   - Ask: "Show me all tables in my database using mcp-db"

---

### Configuration Troubleshooting

#### Common Issues

**Problem: Configuration file not found**
- **Solution**: Create the file in the correct location
- **Verify**: Check the path exists and you have write permissions

**Problem: MCP servers not appearing after restart**
- **Solution**: 
  - Verify JSON syntax is valid (use a JSON validator)
  - Check file encoding is UTF-8
  - Ensure all paths and commands are correct
  - Check application logs for errors

**Problem: Docker MCP not working**
- **Solution**: 
  - Verify `uvx` is in your PATH: `where uvx` (Windows)
  - Test manually: `uv run python server.py --help`
  - Check if UV is properly installed

**Problem: MCP Toolbox for Databases connection failed**
- **Solution**:
  - Verify PostgreSQL container is running: `docker ps`
  - Check database credentials match your configuration
  - Ensure `host.docker.internal` resolves correctly (Windows)
  - Test connection manually: `docker exec -it postgres-pgvector psql -U postgres -d n8n_rag`

**Problem: "host.docker.internal" not resolving**
- **Solution (Windows)**:
  - Use `localhost` or `127.0.0.1` instead of `host.docker.internal`
  - Or use your machine's IP address
  - Ensure Docker Desktop networking is configured correctly

#### Windows-Specific Notes

- **Path Separators**: Use forward slashes `/` or escaped backslashes `\\` in JSON paths
- **Environment Variables**: Use `%VARIABLE%` syntax in Windows
- **Docker Desktop**: Ensure Docker Desktop is running before starting Claude Code or Cursor
- **Permissions**: You may need to run the IDE as Administrator if there are permission issues

#### Testing Configuration

After configuration, test each server:

**Test Docker MCP:**
```bash
# In terminal, verify uvx works
uv run python server.py --help

# In Cursor/Claude Code chat
@docker-local list containers
```

**Test MCP Toolbox for Databases:**
```bash
# In terminal, verify Docker can run the image
docker run --rm us-central1-docker.pkg.dev/database-toolbox/toolbox/toolbox:latest --help

# In Cursor/Claude Code chat
@mcp-db list tables
```

---

## Verification Steps

After installing both MCP servers, follow these steps to verify everything is working correctly.

### 1. Restart Your IDE

Close and restart your IDE (Cursor or Claude Code) to ensure MCP servers are properly loaded and connected.

### 2. Verify MCP Servers

**For Cursor:**
1. Open Cursor's MCP settings (usually in Settings → MCP Servers)
2. Verify both servers appear in the list:
   - **Docker MCP**: Should show as connected
   - **MCP Toolbox for Databases**: Should show as connected

**For Claude Code:**
1. Check the MCP servers status in Claude Code's interface
2. Verify both servers are listed and show as active:
   - **Docker MCP**: Should be available
   - **MCP Toolbox for Databases**: Should be available

### 3. Test Basic Functionality

#### Test Docker MCP:
```bash
# In Cursor/Claude Code chat, try:
@docker-local list containers
```

Expected result: A list of all Docker containers (running and stopped).

#### Test MCP Toolbox for Databases:
```bash
# In Cursor/Claude Code chat, try:
@mcp-db list tables
```

Expected result: A list of all tables in your PostgreSQL database.

### 4. Verify Database Connection

Test that MCP Toolbox for Databases can connect to your PostgreSQL database:

```bash
# In Cursor/Claude Code chat, try:
@mcp-db execute sql "SELECT COUNT(*) FROM n8n_vectors;"
```

**Note:** If the `n8n_vectors` table doesn't exist yet, you can test with:
```bash
@mcp-db execute sql "SELECT current_database(), version();"
```

---

## Troubleshooting

### Common Issues and Solutions

#### Docker MCP Issues

**Problem: UV not found**
- **Solution**: Install UV package manager (see [Step 1](#step-1-install-uv-package-manager))
- **Verify**: Run `uv --version` in terminal

**Problem: Permission denied**
- **Solution**: Run PowerShell as Administrator
- **Alternative**: Check if UV is in your PATH environment variable

**Problem: Package not found**
- **Solution**: Check internet connection
- **Verify**: Try `uv run python server.py --help` manually
- **Alternative**: Update UV: `pip install --upgrade uv`

**Problem: Docker MCP not appearing in IDE**
- **Solution**: Restart your IDE (Cursor or Claude Code)
- **Check**: Verify MCP configuration in settings/configuration file
- **Verify**: Check IDE's MCP server logs

#### MCP Toolbox for Databases Issues

**Problem: Database connection failed**
- **Solution**: Verify PostgreSQL container is running: `docker ps`
- **Check**: Verify database credentials in MCP configuration
- **Test**: Manually connect: `docker exec -it postgres-pgvector psql -U postgres -d n8n_rag`

**Problem: Permission denied**
- **Solution**: Check database user permissions
- **Verify**: Ensure the user has access to the database
- **Test**: Try connecting with: `docker exec -it postgres-pgvector psql -U postgres -d n8n_rag`

**Problem: Port conflicts**
- **Solution**: Ensure port 5432 is not used by another service
- **Check**: `netstat -ano | findstr :5432` (Windows)
- **Alternative**: Use a different port and update MCP configuration

**Problem: Image pull failed**
- **Solution**: Check internet connectivity
- **Verify**: Ensure you can access Google's Artifact Registry
- **Retry**: `docker pull us-central1-docker.pkg.dev/database-toolbox/toolbox/toolbox:latest`

**Problem: MCP Toolbox for Databases not connecting**
- **Solution**: Verify Docker image is pulled: `docker images | grep toolbox`
- **Check**: Review MCP configuration for correct image path
- **Verify**: Check your IDE's MCP server logs for connection errors
- **Documentation**: See the [official troubleshooting guide](https://googleapis.github.io/genai-toolbox/getting-started/introduction/)

### Logs and Debugging

#### Docker MCP Logs:
```bash
# Check UV logs (if available)
uv run python server.py --verbose

# Check Cursor MCP logs
# Look in Cursor's settings/logs directory for MCP server logs
```

#### MCP Toolbox for Databases Logs:
```bash
# Check PostgreSQL container logs
docker logs postgres-pgvector

# Check container status
docker ps -a | grep postgres-pgvector

# Test database connectivity
docker exec -it postgres-pgvector psql -U postgres -d n8n_rag -c "SELECT 1;"
```

#### General Debugging Tips:
1. **Check IDE Logs**: Review your IDE's (Cursor or Claude Code) MCP server logs for detailed error messages
2. **Verify Docker**: Ensure Docker Desktop is running and accessible
3. **Test Manually**: Try Docker commands manually to isolate issues
4. **Check Configuration**: Verify MCP server configuration in settings or configuration file
5. **Restart Services**: Restart Docker and your IDE if issues persist

---

## Natural Language Usage Examples

The MCP servers support natural language commands, making it easy to interact with Docker and databases using conversational queries.

## 🐳 Docker Local Usage Examples

Docker Local (`@docker-local`) provides read-only Docker management. Use these natural language commands:

### Container Listing
```
@docker-local list containers
@docker-local show all containers
@docker-local what containers are running?
```

### Container Details
```
@docker-local container info n8n
@docker-local tell me about postgres-pgvector
@docker-local show details for container n8n
```

### Container Logs
```
@docker-local get logs n8n
@docker-local show last 50 lines of logs for postgres-pgvector
@docker-local what's in the n8n container logs?
```

### Image Management
```
@docker-local list images
@docker-local show all docker images
@docker-local what images do I have?
```

### Resource Monitoring
```
@docker-local docker stats
@docker-local show container resource usage
@docker-local which container uses the most memory?
```

### Health Check
```
@docker-local ping
```

---

## 🗄️ MCP Toolbox for Databases Usage Examples

### Database Overview
```
"Show me all tables in my database"
"List all tables with their sizes"
"What tables do I have in the n8n_rag database?"
"Display the schema of all tables"
"Show me the structure of the n8n_vectors table"
```

### Performance Monitoring
```
"Show me the slowest running queries"
"List all active database connections"
"What queries are currently running?"
"Show me the top 10 longest running queries"
"Display queries running for more than 1 minute"
"Show me queries that are blocking other queries"
```

### Database Health and Maintenance
```
"Check for bloated tables in my database"
"Show me tables with dead tuples"
"List invalid indexes that need attention"
"Check autovacuum configuration"
"Show memory configuration settings"
"Display database size and growth statistics"
```

### Query Analysis and Optimization
```
"Generate an execution plan for: SELECT * FROM n8n_vectors LIMIT 10"
"Explain this query: SELECT COUNT(*) FROM n8n_vectors WHERE content LIKE '%VMware%'"
"Show me the query plan for: SELECT * FROM n8n_vectors ORDER BY id DESC"
"Analyze the performance of: SELECT embedding FROM n8n_vectors WHERE id = 'some-uuid'"
"Help me optimize this slow query"
```

### Extension Management
```
"Show me all installed PostgreSQL extensions"
"List available extensions I can install"
"What extensions are currently enabled?"
"Display extension versions and descriptions"
"Check if pgvector extension is installed"
```

### Vector Database Operations
```
"How many vector chunks do I have?"
"Show me the 5 smallest content chunks"
"List the largest embedding vectors"
"What's the average size of my content chunks?"
"Show me chunks containing 'VMware' in the content"
"Find similar vectors to a given embedding"
```

### Custom SQL Queries
```
"Execute this SQL: SELECT COUNT(*) FROM n8n_vectors"
"Run this query: SELECT content, LENGTH(content) FROM n8n_vectors ORDER BY LENGTH(content) DESC LIMIT 5"
"Show me all unique metadata sources"
"Find chunks with the most common content patterns"
"Display the top 10 most frequent content patterns"
```

### Database Statistics
```
"Show me database size and table statistics"
"What's the total size of my database?"
"Display table row counts and sizes"
"Show me the most active tables"
"Give me a summary of database performance metrics"
```

---

## 🎯 Real-World Usage Scenarios

### Scenario 1: Morning Health Check
```
@docker-local list containers
@docker-local docker stats
@mcp-db database_overview
"Are all my services healthy? Check containers and database connections"
```

### Scenario 2: Debugging a Slow RAG Pipeline
```
@mcp-db list_query_stats
@mcp-db long_running_transactions
@docker-local get logs n8n
"Why is my vector search taking so long? Show me slow queries and n8n logs"
```

### Scenario 3: Database Performance Investigation
```
@mcp-db list_table_stats
@mcp-db list_top_bloated_tables
@mcp-db list_indexes only_unused=true
"Which tables need vacuuming? Are there unused indexes I should drop?"
```

### Scenario 4: Resource Monitoring Before Deployment
```
@docker-local docker stats
@mcp-db list_active_queries
@mcp-db list_database_stats
"Do I have enough resources to deploy another container? Check current usage"
```

---

## 🔧 Troubleshooting with Natural Language

### Docker Issues (using @docker-local)
```
"My n8n container seems stuck - show me the logs"
"Why is my postgres container using so much memory?"
"Show me container resource usage - something is slow"
"What's the status of all my containers?"
"Check if postgres-pgvector is still running"
"Get the last 100 lines of logs from n8n"
```

### Database Issues
```
"My database queries are slow, help me optimize them"
"Show me what's causing database locks"
"Why is my database connection failing?"
"Help me identify performance bottlenecks"
"Check if my database needs maintenance"
"Show me database errors and warnings"
```

### General Troubleshooting
```
"Help me diagnose why my MCP server isn't working"
"Show me how to check if Docker is running properly"
"What's the status of my database container?"
"Help me verify my database connection settings"
```

---

## 💡 Pro Tips for Natural Language Usage

### Be Specific
- ✅ "Show me the logs for the postgres-pgvector container"
- ❌ "Show me logs"

### Use Context
- ✅ "Create a new nginx container named web-server on port 8080"
- ❌ "Create container"

### Ask for Help
- ✅ "How do I optimize slow database queries?"
- ✅ "What's the best way to monitor container performance?"
- ✅ "Show me examples of vector database queries"

### Combine Operations
- ✅ "Create a PostgreSQL container and set up monitoring for it"
- ✅ "Show me container status and database performance metrics together"
- ✅ "Deploy a new container and verify it's running properly"

### Use Descriptive Queries
- ✅ "Show me all containers that are using more than 1GB of memory"
- ✅ "List tables in my database that haven't been updated in 30 days"
- ✅ "Find containers that are failing to start"

---

## Additional Resources

### Official Documentation
- **Docker Local**: Custom MCP server in `module-07/docker-mcp-simple/`
- **MCP Toolbox for Databases**: 
  - [GitHub Repository](https://github.com/googleapis/genai-toolbox)
  - [Official Documentation](https://googleapis.github.io/genai-toolbox/getting-started/introduction/)
  - [Docker Image](https://hub.docker.com/r/us-central1-docker.pkg.dev/database-toolbox/toolbox/toolbox)
- **MCP Documentation**: [Model Context Protocol](https://modelcontextprotocol.io/)

### Related Tools
- **Docker Documentation**: [https://docs.docker.com/](https://docs.docker.com/)
- **PostgreSQL Documentation**: [https://www.postgresql.org/docs/](https://www.postgresql.org/docs/)
- **pgvector Extension**: [https://github.com/pgvector/pgvector](https://github.com/pgvector/pgvector)
- **UV Package Manager**: [https://github.com/astral-sh/uv](https://github.com/astral-sh/uv)

---

## Support

If you encounter issues during installation or usage:

1. **Check the Troubleshooting Section**: Review the [Troubleshooting](#troubleshooting) section above for common issues
2. **Verify Prerequisites**: Ensure all prerequisites are installed and up to date
3. **Check Docker Status**: Verify Docker containers are running properly
4. **Review Logs**: Check your IDE's (Cursor or Claude Code) MCP server logs for detailed error messages
5. **Consult Documentation**: Review the official documentation for each MCP server
6. **GitHub Issues**: Check GitHub repositories for known issues and solutions

