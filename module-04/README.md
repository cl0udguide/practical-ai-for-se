# Creating a Local "ChatGPT Clone"

This guide will walk you through setting up Ollama (a local LLM/inference server) and OpenWebUI (a web interface) to create your own ChatGPT-like experience running entirely on your local machine.

## Table of Contents

- [Installing Ollama](#installing-ollama)
- [Monitoring GPU Usage](#monitoring-gpu-usage)
- [Testing and Using Ollama](#testing-and-using-ollama)
- [Ollama Interactive Commands](#ollama-interactive-commands)
- [Working with Models](#working-with-models)
- [Running Ollama as a Server](#running-ollama-as-a-server)
- [Deploying OpenWebUI using Docker](#deploying-openwebui-using-docker)

---

## Installing Ollama

Ollama is a tool that allows you to run large language models locally on your machine. Choose the installation method based on your operating system.

### Windows Installation

**Recommended: Native Windows Installer**

1. Visit the [Ollama download page](https://ollama.com/download)
2. Download the Windows installer (`OllamaSetup.exe`)
3. Run the installer and follow the setup wizard
4. The installer will automatically add Ollama to your system PATH

**Pros:**
- Simple installation process
- Automatic PATH configuration
- Native Windows service integration
- Easy updates through the installer
- Easy to enable GPU acceleration
- Achieves best, native performance of GPU - especially important when running Ollama on Windows laptops

**Cons:**
- Requires administrator privileges
- Less control over installation location

**Alternative: WSL2 (Windows Subsystem for Linux)**

If you prefer using WSL2, follow the Linux installation instructions below within your WSL2 environment.

**Pros:**
- More similar to Linux/production environments
- Better for development workflows

**Cons:**
- GPU passthrough can be more complex
- Additional overhead from WSL2
- Requires WSL2 setup

### macOS Installation

**Option 1: Official Installer (Recommended)**

1. Visit the [Ollama download page](https://ollama.com/download)
2. Download the macOS installer (`.dmg` file)
3. Open the `.dmg` file and drag Ollama to your Applications folder
4. Launch Ollama from Applications

**Option 2: Homebrew**

```bash
brew install ollama
```

**Starting Ollama:**
```bash
ollama serve
```

### Linux Installation

**Option 1: Automated Install Script (Recommended)**

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

This script will:
- Download the appropriate binary for your system
- Install it to `/usr/local/bin/ollama`
- Set up systemd service (on systemd-based distributions)

**Option 2: Manual Installation**

1. Download the binary:
```bash
curl -L https://ollama.com/download/ollama-linux-amd64 -o ollama
```

2. Make it executable:
```bash
chmod +x ollama
```

3. Move it to your PATH:
```bash
sudo mv ollama /usr/local/bin/
```

**Starting Ollama as a Service (systemd):**
```bash
sudo systemctl start ollama
sudo systemctl enable ollama  # To start on boot
```

**Starting Ollama Manually:**
```bash
ollama serve
```

### Verifying Installation

After installation, verify Ollama is installed correctly:

**Windows (PowerShell):**
```powershell
ollama --version
```

**macOS/Linux:**
```bash
ollama --version
```

---

## Monitoring GPU Usage

If you have an NVIDIA GPU, you'll want to monitor its usage while running models. Make sure you have the NVIDIA CUDA Toolkit and drivers installed.

### Windows

**Single snapshot:**
```powershell
nvidia-smi
```

**Continuous monitoring (updates every 5 seconds):**
```powershell
nvidia-smi -l 5
```

**Note:** `nvidia-smi` is typically located in `C:\Program Files\NVIDIA Corporation\NVSMI\` on Windows. If it's not in your PATH, you can either:
- Navigate to that directory first
- Add it to your PATH environment variable

### macOS

macOS doesn't support NVIDIA GPUs in recent versions. For Apple Silicon Macs (M1/M2/M3), Ollama automatically uses the Metal framework for GPU acceleration. No additional monitoring is needed, but you can check system resources using:

```bash
# Monitor overall system resources
top

# Or use Activity Monitor (GUI application)
```

### Linux

**Single snapshot:**
```bash
nvidia-smi
```

**Continuous monitoring (updates every 5 seconds):**
```bash
watch -n 5 nvidia-smi
```

Or:
```bash
nvidia-smi -l 5
```

---

## Testing and Using Ollama

Once Ollama is installed, you can start using it from the command line.

### Running Your First Model

**All Operating Systems:**

```bash
ollama run gemma3
```

This command will:
1. Download the model if not already present
2. Load it into memory
3. Start an interactive chat session

You can then type messages and interact with the model:
```
>>> Hi
```

When you're done, exit the interactive session:
```
/bye
```


### Running Multi-Modal Models (e.g., Vision Models)

Some models support multi-modality, allowing them to process both text and images. Test with a multi-modal model:

**Windows (PowerShell):**
```powershell
ollama run gemma3 "What's in this image? C:\Users\YourName\Pictures\photo.jpg"
```

**macOS/Linux:**
```bash
ollama run gemma3 "What's in this image? /path/to/your/image.jpg"
```

---

## Ollama Interactive Commands

When you're in an interactive Ollama session (after running `ollama run <model>`), you can use these commands:

| Command | Description |
|---------|-------------|
| `/?` | Lists all available commands |
| `/show info` | Shows detailed model information |
| `/show parameters` | Shows model parameters and settings |
| `/show system` | Shows the system prompt |
| `/clear` | Clears the conversation context |
| `/bye` | Exits the interactive session |
| `/set parameter <value>` | Sets model parameters (e.g., temperature) |

**Example session:**
```
>>> Hi there!
Hello! How can I help you today?

>>> /show info
Model details...

>>> /clear
Cleared session context

>>> /bye
```

---

## Working with Models

### Finding Models

Browse available models at: [https://ollama.com/library](https://ollama.com/library)

### Downloading Models

**Download without running:**
```bash
ollama pull granite4:micro-h
```

**Additional examples:**
```bash
ollama pull gemma2:2b    # Smaller model (~1.6 GB)
ollama pull gemma2:9b    # Medium model (~5.4 GB)
ollama pull llama3.2     # Larger model
```

**Note:** Model sizes can range from a few hundred MB to over 10 GB. Check the [Ollama library](https://ollama.com/library) for specific model sizes before downloading, especially on limited bandwidth or storage.

### Listing Installed Models

```bash
ollama list
```

Or:
```bash
ollama ls
```

This shows all locally available models, their sizes, and when they were last modified. The size information helps you understand how much disk space each model requires.

### Removing Models

```bash
ollama rm <model-name>
```

Example:
```bash
ollama rm gemma3
```

---

## Running Ollama as a Server

By default, Ollama runs as a service on `localhost:11434`. However, you can configure it to listen on all network interfaces to make it accessible from other machines or containers.

### Starting the Server

**Windows (PowerShell):**
```powershell
# Listen on all interfaces
$env:OLLAMA_HOST = "0.0.0.0:11434"; ollama serve
```

**macOS/Linux (bash/zsh):**
```bash
# Listen on all interfaces
OLLAMA_HOST="0.0.0.0:11434" ollama serve
```

**Persistent Configuration:**

**Windows:**
Set system environment variable permanently:
```powershell
[System.Environment]::SetEnvironmentVariable('OLLAMA_HOST', '0.0.0.0:11434', 'User')
```

**macOS/Linux:**
Add to your shell profile (`~/.bashrc`, `~/.zshrc`, etc.):
```bash
export OLLAMA_HOST="0.0.0.0:11434"
```

### Checking Running Models

To see which models are currently loaded and running in Ollama:

```bash
ollama ps
```

This command displays:
- Currently loaded models
- Model size in memory
- How long the model has been running
- Which processor (CPU/GPU) is being used

This is useful for monitoring resource usage and seeing which models are active.

### Additional Performance Monitoring by OS

Beyond `ollama ps`, you can monitor detailed system resource usage on each platform:

#### Windows

**Task Manager (GUI):**
1. Press `Ctrl + Shift + Esc` to open Task Manager
2. Go to the **Performance** tab
3. Check **GPU** for GPU usage (if available)
4. Check **Memory** for memory usage

#### macOS

**Activity Monitor (GUI):**
1. Press `Cmd + Space` and search for "Activity Monitor"
2. Check the **GPU** tab (if available)
3. Check the **Memory** tab for RAM usage
4. Check the **CPU** tab for processor usage

**Terminal Commands:**
```bash
# Monitor overall system resources
top

# Better alternative with colors and real-time updates
htop  # Install with: brew install htop

# Check GPU usage (Apple Silicon)
sudo powermetrics --samplers gpu_power -i 1000 -n 1
```

**Note:** For Apple Silicon Macs (M1/M2/M3), GPU monitoring is integrated. Use Activity Monitor's GPU History to see Metal (GPU) usage.

#### Linux

**System Monitor (GUI):**
Most Linux distributions include a system monitor application (gnome-system-monitor, ksysguard, etc.)

**Terminal Commands:**
```bash
# Monitor overall resources
top

# Better alternative
htop  # Install with: sudo apt install htop

# Monitor GPU (NVIDIA)
nvidia-smi

# Continuous GPU monitoring
watch -n 1 nvidia-smi  # Updates every second

# Monitor GPU with more details
nvtop  # Install with: sudo apt install nvtop
```

**Check memory usage:**
```bash
free -h
```
These monitoring tools help you ensure your system has enough resources to run models efficiently and identify potential bottlenecks.


### Testing the API

Once the server is running, you can test it with API calls. Ollama supports **OpenAI-compatible API** endpoints, which makes it easy to integrate with existing tools and libraries.

#### OpenAI-Compatible API (Recommended)

The OpenAI-compatible format is useful for integration with tools that expect OpenAI's API format.

**Windows (PowerShell):**
```powershell
curl http://localhost:11434/v1/chat/completions -Method Post -Body '{"model": "gemma3", "messages": [{"role": "user", "content": "Explain the differences between Ansible and Terraform"}]}' -ContentType "application/json"
```

**macOS/Linux:**
```bash
curl http://localhost:11434/v1/chat/completions -d '{
  "model": "gemma3",
  "messages": [
    {
      "role": "user",
      "content": "Explain the differences between Ansible and Terraform"
    }
  ]
}'
```

**Response Format:**

The OpenAI-compatible API returns a structured JSON response similar to OpenAI's format:

```json
{
  "id": "chatcmpl-123",
  "object": "chat.completion",
  "created": 1677652288,
  "model": "gemma3",
  "choices": [{
    "index": 0,
    "message": {
      "role": "assistant",
      "content": "Ansible and Terraform are both Infrastructure as Code (IaC) tools, but they serve different purposes:\n\nAnsible is primarily a configuration management tool that focuses on..."
    },
    "finish_reason": "stop"
  }],
  "usage": {
    "prompt_tokens": 10,
    "completion_tokens": 140,
    "total_tokens": 150
  }
}
```

**Extracting Just the Response Text:**

**Windows (PowerShell):**
```powershell
$result = curl http://localhost:11434/v1/chat/completions -Method Post -Body '{"model": "gemma3", "messages": [{"role": "user", "content": "Explain the differences between Ansible and Terraform"}]}' -ContentType "application/json" | ConvertFrom-Json
$result.choices[0].message.content
```

**macOS/Linux (using jq):**
```bash
curl http://localhost:11434/v1/chat/completions -d '{
  "model": "gemma3",
  "messages": [{"role": "user", "content": "Explain the differences between Ansible and Terraform"}]
}' | jq -r '.choices[0].message.content'
```

#### Native Ollama API (Alternative)

Ollama also has its own native API format for streaming responses:

**Windows (PowerShell):**
```powershell
curl http://localhost:11434/api/generate -Method Post -Body '{"model": "gemma3", "prompt": "Explain the differences between Ansible and Terraform", "stream": false}' -ContentType "application/json"
```

**macOS/Linux:**
```bash
curl http://localhost:11434/api/generate -d '{
  "model": "gemma3",
  "prompt": "Explain the differences between Ansible and Terraform",
  "stream": false
}'
```

**Note:** Setting `"stream": false` returns the complete response at once instead of streaming tokens.

These commands extract just the text content from each streaming JSON response and display it as a continuous readable text.

### Server Help

To see all server options:
```bash
ollama serve --help
```

---

## Deploying OpenWebUI using Docker

OpenWebUI provides a ChatGPT-like web interface for Ollama. We'll use Docker Compose to deploy it.

### Installation Methods Overview

There are multiple ways to install OpenWebUI. I recommend Docker for most use cases, but here's a comparison:

#### Docker Deployment (Recommended)

**Pros:**
- **Isolated environment** - No conflicts with system Python or other packages
- **Easy setup** - Single command to start, no dependency management
- **Consistent behavior** - Works the same across Windows, macOS, and Linux
- **Easy updates** - Simple `docker compose pull` to get latest version
- **Easy cleanup** - Complete removal with `docker compose down -v`
- **Persistent data** - Docker volumes ensure your data is preserved
- **Production-ready** - Same approach used in production environments
- **No Python version issues** - Container includes all dependencies

**Cons:**
- Requires Docker Desktop installed (~500 MB download)
- Uses more disk space than native installation
- Slight overhead from containerization (usually negligible)

#### pip Installation

Install OpenWebUI directly using Python's package manager:

```bash
pip install open-webui
```

**Pros:**
- Native performance (no containerization overhead)
- Smaller disk footprint
- Direct access to Python environment
- Good for development and customization

**Cons:**
- **Python version dependency** - Requires specific Python version (3.11+)
- **Dependency conflicts** - Can conflict with other Python packages
- **Manual dependency management** - Need to handle system libraries
- **Platform-specific issues** - Different setup steps for Windows/Mac/Linux
- **Updates more complex** - Need to manage package versions manually
- **Cleanup harder** - Removing all dependencies can be tricky

#### uv Installation (Modern Python Package Manager)

[uv](https://github.com/astral-sh/uv) is a modern, fast Python package installer:

```bash
uv pip install open-webui
```

**Pros:**
- **Much faster** than pip - 10-100x faster package installation
- Better dependency resolution than pip
- More reliable than pip for complex dependencies
- Built-in virtual environment management

**Cons:**
- Still requires Python environment setup
- Relatively new tool - less community documentation
- Same platform-specific issues as pip
- Dependency conflicts still possible
- Not as isolated as Docker

### Why I Recommend Docker

For this course, we use Docker because:

1. **Consistency** - Everyone gets the same experience regardless of their OS or Python setup
2. **Simplicity** - No need to troubleshoot Python versions, dependencies, or PATH issues
3. **Isolation** - Doesn't interfere with other Python projects or system packages. This is especially important for better security when exposing services to the internet, as containers provide an additional security boundary
4. **Portability** - Easy to share configurations and reproduce setups
5. **Best practices** - Teaches containerization, a crucial skill for modern development
6. **Homelab deployment** - If you want to deploy OpenWebUI in your homelab and expose it to the internet, Docker is the recommended approach for security and ease of management
7. **Course requirement** - We need Docker later in the course anyway to deploy n8n (workflow automation tool), so learning Docker now serves multiple purposes

### Prerequisites

1. **Docker** installed and running

   **Note:** Docker CLI is sufficient for this training, but for simplicity on Windows, I recommend **Docker Desktop**, which is available for free for personal use and provides an easy-to-use GUI.

   - **Windows:** [Download Docker Desktop for Windows](https://www.docker.com/products/docker-desktop) (Recommended)
   - **macOS:** [Download Docker Desktop for Mac](https://www.docker.com/products/docker-desktop)
   - **Linux:** Install Docker Engine and Docker Compose:
     ```bash
     # Install Docker
     curl -fsSL https://get.docker.com -o get-docker.sh
     sudo sh get-docker.sh
     
     # Install Docker Compose
     sudo apt-get update
     sudo apt-get install docker-compose-plugin
     ```

2. **Ollama running as a server** (see [Running Ollama as a Server](#running-ollama-as-a-server))

### Step 1: Start Ollama Server

Before starting OpenWebUI, make sure Ollama is running and listening on all interfaces:

**Windows (PowerShell):**
```powershell
$env:OLLAMA_HOST = "0.0.0.0:11434"; ollama serve
```

**macOS/Linux:**
```bash
OLLAMA_HOST="0.0.0.0:11434" ollama serve
```

Leave this terminal window open and running.

### Step 2: Start OpenWebUI with Docker Compose

Open a **new terminal window** and navigate to the Docker directory:

**Windows (PowerShell):**
```powershell
cd module-04\docker
docker compose up -d
```

**macOS/Linux:**
```bash
cd module-04/docker
docker compose up -d
```

The `-d` flag runs the container in detached mode (in the background).

### Step 3: Access OpenWebUI

Open your web browser and navigate to:
```
http://localhost:3000
```

You should see the OpenWebUI interface. Since authentication is disabled (`WEBUI_AUTH=false` in the docker-compose.yml), you can start chatting immediately.

### Understanding the Configuration

The `docker-compose.yml` file configures:

- **Port mapping**: `3000:8080` - Maps container port 8080 to host port 3000
- **Ollama connection**: `OLLAMA_BASE_URL=http://host.docker.internal:11434` - Connects to Ollama on the host
- **Authentication**: `WEBUI_AUTH=false` - Disables login (useful for local development)
- **Persistent storage**: Saves conversations and settings in a Docker volume
- **Auto-restart**: `unless-stopped` - Automatically restarts the container if it crashes

### Managing OpenWebUI

**View logs:**
```bash
docker compose logs -f
```

**Stop OpenWebUI:**
```bash
docker compose down
```

**Stop and remove all data:**
```bash
docker compose down -v
```

**Restart OpenWebUI:**
```bash
docker compose restart
```

**Update to latest version:**
```bash
docker compose pull
docker compose up -d
```

### Troubleshooting

**Issue: OpenWebUI can't connect to Ollama**

1. Verify Ollama is running:
   
   **Windows (PowerShell):**
   ```powershell
   curl http://localhost:11434/api/tags -Method Get
   ```
   
   **macOS/Linux:**
   ```bash
   curl http://localhost:11434/api/tags
   ```

2. Check if Ollama is listening on all interfaces:
   - Make sure you started Ollama with `OLLAMA_HOST="0.0.0.0:11434"`

3. Check Docker container logs:
   ```bash
   docker compose logs open-webui
   ```

**Issue: Port 3000 already in use**

Edit `docker-compose.yml` and change the port mapping:
```yaml
ports:
  - "3001:8080"  # Use port 3001 instead
```

Then restart:
```bash
docker compose down
docker compose up -d
```

---

## Additional Resources

- [Ollama Official Documentation](https://github.com/ollama/ollama)
- [Ollama Model Library](https://ollama.com/library)
- [OpenWebUI Documentation](https://github.com/open-webui/open-webui)
- [Ollama API Documentation](https://github.com/ollama/ollama/blob/main/docs/api.md)

## Tips and Best Practices

1. **Start with smaller models** if you have limited RAM/VRAM (e.g., `gemma2:2b` or `llama3.2:1b`)
2. **Monitor resource usage** when running models to avoid system slowdowns
3. **Use the `/clear` command** in interactive sessions to free up memory
4. **Keep Ollama updated** for the latest model support and performance improvements
5. **Use Docker volumes** to persist OpenWebUI data across container restarts
6. **Pull models before running** to avoid waiting during your first interactive session
