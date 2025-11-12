# Practical AI for Systems Engineers

A comprehensive toolkit for leveraging AI in systems engineering workflows, featuring document conversion, audio/video transcription, AI agents, and RAG (Retrieval-Augmented Generation) implementations.

## 🎯 Overview

This repository provides production-ready CLI tools and examples for:
- **Document Conversion** - PowerPoint, Excel, PDF, Word to Markdown
- **Media Transcription** - YouTube videos and local audio/video files
- **AI Agents** - Financial data analysis, news aggregation, YouTube content analysis
- **RAG Systems** - Vector databases with pgvector and hybrid search
- **Web Scraping** - JavaScript-rendered pages with bot protection bypass

## ⚡ Quick Start Guide

Complete setup guide from scratch to your first transcription in under 10 minutes!

Choose your platform: [Windows](#windows-setup) | [macOS](#macos-setup) | [Linux](#linux-setup)

---

### Windows Setup

### Step 1: Install Python 3.11+

1. **Download Python:**
   - Visit [python.org/downloads](https://www.python.org/downloads/)
   - Download the latest Python 3.11 or 3.12 installer for Windows
   - Look for "Download Python 3.x.x" button

2. **Run the installer:**
   - ✅ **IMPORTANT:** Check "Add Python to PATH" at the bottom
   - Click "Install Now"
   - Wait for installation to complete
   - Click "Close"

3. **Verify installation:**
   Open PowerShell or Command Prompt and run:
   ```powershell
   python --version
   ```
   Should show: `Python 3.11.x` or higher

### Step 2: Install Visual Studio Code

1. **Download VS Code:**
   - Visit [code.visualstudio.com](https://code.visualstudio.com/)
   - Download for Windows
   - Run the installer (accept all defaults)

2. **Install Python Extension:**
   - Open VS Code
   - Click Extensions icon (or press `Ctrl+Shift+X`)
   - Search for "Python"
   - Install the extension by Microsoft

### Step 3: Install Git (Optional)

**Option A: Skip Git (Download ZIP instead)**
- You can download the repository as a ZIP file in Step 5
- Skip to Step 4 if you prefer not to install Git

**Option B: Install Git (Recommended for developers)**

1. **Download Git:**
   - Visit [git-scm.com/downloads](https://git-scm.com/downloads)
   - Download Git for Windows
   - Run installer (accept defaults)

2. **Verify installation:**
   ```powershell
   git --version
   ```

### Step 4: Install ffmpeg

**Option A: Using Chocolatey (Recommended)**

1. **Install Chocolatey** (if not already installed):
   - Right-click PowerShell and "Run as Administrator"
   - Run:
   ```powershell
   Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
   ```

2. **Install ffmpeg:**
   ```powershell
   choco install ffmpeg
   ```

**Option B: Manual Installation**

1. Download ffmpeg from [ffmpeg.org/download.html](https://ffmpeg.org/download.html)
2. Extract to `C:\ffmpeg` or a preferred directory
3. Add to PATH:
   - Search Windows for "Environment Variables"
   - Click "Environment Variables"
   - Under "System Variables", find "Path" and click "Edit"
   - Click "New" and add: `C:\ffmpeg\bin` (or `YourDirectory\bin` if extracted elsewhere)
   - Click OK on all windows
   - Restart your terminal

3. **Verify installation:**
   ```powershell
   ffmpeg -version
   ```

### Step 5: Get the Repository

**Option A: Download as ZIP (No Git Required)**

1. **Download the repository:**
   - Visit the repository URL in your browser
   - Click the green "Code" button
   - Select "Download ZIP"
   - Save to `C:\Users\YourUsername\Documents`

2. **Extract the ZIP:**
   - Right-click the downloaded ZIP file
   - Select "Extract All..."
   - Choose destination folder
   - Click "Extract"
   - **Note:** If the extracted folder has a different name (e.g., `practical-ai-for-se-main`), rename it to `practical-ai-for-se`

3. **Open in VS Code:**
   ```powershell
   cd C:\Users\YourUsername\Documents\practical-ai-for-se
   code .
   ```

**Option B: Clone with Git (If Git Installed)**

1. **Open VS Code:**
   - Press `Ctrl+Shift+P` to open Command Palette
   - Type "Git: Clone"
   - Paste repository URL

   **Or use terminal:**
   ```powershell
   # Navigate to where you want the project
   cd C:\Users\YourUsername\Documents

   # Clone the repository
   git clone <repository-url>

   # Enter the project folder
   cd practical-ai-for-se
   ```

2. **Open in VS Code:**
   ```powershell
   code .
   ```

### Step 6: Create Virtual Environment

Open VS Code's integrated terminal (`Ctrl+``) or PowerShell in the project directory:

1. **Create virtual environment:**
   ```powershell
   python -m venv .venv
   ```

2. **Activate virtual environment:**
   
   **PowerShell:**
   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```
   
   If you get an error, first run:
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```
   Then try activating again.
   
   **Command Prompt:**
   ```cmd
   .venv\Scripts\activate.bat
   ```

3. **Confirm activation:**
   Your prompt should now show `(.venv)` at the beginning:
   ```powershell
   (.venv) PS C:\Users\YourUsername\Documents\practical-ai-for-se>
   ```

### Step 7: Install Requirements

With virtual environment activated:

1. **First, upgrade pip, setuptools, and wheel:**
   ```powershell
   python -m pip install --upgrade pip setuptools wheel
   ```

2. **Install all requirements:**
   ```powershell
   pip install -r requirements.txt
   ```

   This will take a few minutes. Wait for all packages to install.

3. **Verify installation:**
   ```powershell
   pip list
   ```

**⚠️ If you see compilation errors mentioning scikit-image, meson, or missing C compiler:**

This means pip is trying to build packages from source code. Fix it with one of these solutions:

**Solution A - Force Binary Wheels (Try First):**
```powershell
# Install scikit-image separately with binary wheel
pip install --only-binary :all: scikit-image

# Then continue with requirements
pip install -r requirements.txt
```

**Solution B - Install C++ Build Tools:**

If Solution A doesn't work:

1. Download **Build Tools for Visual Studio 2022**:
   - Visit: https://visualstudio.microsoft.com/downloads/
   - Scroll to "Tools for Visual Studio"
   - Download "Build Tools for Visual Studio 2022"

2. Run the installer:
   - Select "Desktop development with C++"
   - Install (requires ~6GB disk space)
   - Restart your computer

3. Try installing requirements again:
   ```powershell
   pip install -r requirements.txt
   ```

### Step 8: Test with Your First Transcription

Let's transcribe the included sample audio file using the local Whisper transcription tool!

1. **Navigate to module-01:**
   ```powershell
   cd module-01
   ```

2. **Check the audio file:**
   
   The repository includes `welcome.mp3` for testing.
   
   You can also use any of your own `.mp3`, `.wav`, or `.m4a` files.

3. **Run transcription:**
   ```powershell
   python whisper_local.py welcome.mp3
   ```

4. **Wait for processing:**
   - First time will download Whisper model (~140MB)
   - Transcription will take a moment depending on audio length
   - Output will be saved as `welcome.txt`

5. **View the result:**
   ```powershell
   # View in terminal
   type welcome.txt

   # Or open in VS Code
   code welcome.txt
   ```

6. **Try with timestamps:**
   ```powershell
   python whisper_local.py welcome.mp3 --timestamps
   ```

### 🎉 Success!

You've successfully:
- ✅ Installed Python, VS Code, Git, and ffmpeg
- ✅ Cloned the repository
- ✅ Created and activated a virtual environment
- ✅ Installed all dependencies
- ✅ Transcribed your first audio file using AI!

**Next Steps:**
- Explore other tools in `module-02` (PowerPoint, Excel, YouTube conversion)
- Try AI agents in `module-08`
- Read the detailed documentation below

**Need Help?** See the [Troubleshooting](#-troubleshooting) section below.

---

### macOS Setup

### Step 1: Install Homebrew (Package Manager)

1. **Install Homebrew:**
   Open Terminal (press `Cmd+Space`, type "Terminal", press Enter) and run:
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

2. **Verify installation:**
   ```bash
   brew --version
   ```

### Step 2: Install Python 3.11+

1. **Install Python via Homebrew:**
   ```bash
   brew install python@3.11
   ```

2. **Verify installation:**
   ```bash
   python3 --version
   ```
   Should show: `Python 3.11.x` or higher

### Step 3: Install Visual Studio Code

1. **Install VS Code via Homebrew:**
   ```bash
   brew install --cask visual-studio-code
   ```
   
   **Or download manually:**
   - Visit [code.visualstudio.com](https://code.visualstudio.com/)
   - Download for macOS
   - Open the `.dmg` file and drag VS Code to Applications

2. **Install Python Extension:**
   - Open VS Code
   - Press `Cmd+Shift+X` to open Extensions
   - Search for "Python"
   - Install the extension by Microsoft

### Step 4: Install Git (Optional)

**Option A: Skip Git (Download ZIP instead)**
- You can download the repository as a ZIP file in Step 6
- Skip to Step 5 if you prefer not to install Git

**Option B: Install Git (Recommended for developers)**

1. **Install Git:**
   ```bash
   brew install git
   ```
   
   Or use the built-in Git (comes with macOS Command Line Tools):
   ```bash
   git --version
   # If not installed, macOS will prompt to install Command Line Tools
   ```

2. **Verify installation:**
   ```bash
   git --version
   ```

### Step 5: Install ffmpeg

```bash
brew install ffmpeg
```

**Verify installation:**
```bash
ffmpeg -version
```

### Step 6: Get the Repository

**Option A: Download as ZIP (No Git Required)**

1. **Download the repository:**
   - Visit the repository URL in your browser
   - Click the green "Code" button
   - Select "Download ZIP"
   - Save to your Downloads folder

2. **Extract and navigate:**
   ```bash
   cd ~/Downloads
   # Extract the ZIP (filename may vary)
   unzip practical-ai-for-se*.zip
   
   # Navigate to extracted folder (rename if needed)
   # If folder is named practical-ai-for-se-main or similar, rename it:
   mv practical-ai-for-se-* practical-ai-for-se
   cd practical-ai-for-se
   ```

3. **Open in VS Code:**
   ```bash
   code .
   ```

**Option B: Clone with Git (If Git Installed)**

1. **Navigate to your desired location:**
   ```bash
   cd ~/Documents
   ```

2. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd practical-ai-for-se
   ```

3. **Open in VS Code:**
   ```bash
   code .
   ```

### Step 7: Create Virtual Environment

Open VS Code's integrated terminal (`` Ctrl+` ``) or continue in Terminal:

1. **Create virtual environment:**
   ```bash
   python3 -m venv .venv
   ```

2. **Activate virtual environment:**
   ```bash
   source .venv/bin/activate
   ```

3. **Confirm activation:**
   Your prompt should now show `(.venv)`:
   ```bash
   (.venv) user@macbook practical-ai-for-se %
   ```

### Step 8: Install Requirements

With virtual environment activated:

1. **First, upgrade pip, setuptools, and wheel:**
   ```bash
   python -m pip install --upgrade pip setuptools wheel
   ```

2. **Install all requirements:**
   ```bash
   pip install -r requirements.txt
   ```

   This will take a few minutes. Wait for all packages to install.

3. **Verify installation:**
   ```bash
   pip list
   ```

### Step 9: Test with Your First Transcription

1. **Navigate to module-01:**
   ```bash
   cd module-01
   ```

2. **Check the audio file:**
   
   The repository includes `welcome.mp3` for testing.
   
   You can also use any of your own `.mp3`, `.wav`, or `.m4a` files.

3. **Run transcription:**
   ```bash
   python whisper_local.py welcome.mp3
   ```

4. **Wait for processing:**
   - First time will download Whisper model (~140MB)
   - Transcription will take a moment depending on audio length
   - Output will be saved as `welcome.txt`

5. **View the result:**
   ```bash
   # View in terminal
   cat welcome.txt
   
   # Or open in VS Code
   code welcome.txt
   ```

6. **Try with timestamps:**
   ```bash
   python whisper_local.py welcome.mp3 --timestamps
   ```

### 🎉 Success!

You've successfully completed the macOS setup!

---

### Linux Setup

### Step 1: Update System Packages

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt upgrade -y
```

**Fedora:**
```bash
sudo dnf update -y
```

**Arch Linux:**
```bash
sudo pacman -Syu
```

### Step 2: Install Python 3.11+

**Ubuntu/Debian:**
```bash
sudo apt install python3 python3-pip python3-venv -y
```

**Fedora:**
```bash
sudo dnf install python3 python3-pip -y
```

**Arch Linux:**
```bash
sudo pacman -S python python-pip
```

**Verify installation:**
```bash
python3 --version
```
Should show: `Python 3.8+` (ideally 3.11+)

### Step 3: Install Visual Studio Code

**Ubuntu/Debian:**
```bash
# Download and install via snap
sudo snap install --classic code

# Or via official Microsoft repository
wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > packages.microsoft.gpg
sudo install -D -o root -g root -m 644 packages.microsoft.gpg /etc/apt/keyrings/packages.microsoft.gpg
sudo sh -c 'echo "deb [arch=amd64,arm64,armhf signed-by=/etc/apt/keyrings/packages.microsoft.gpg] https://packages.microsoft.com/repos/code stable main" > /etc/apt/sources.list.d/vscode.list'
sudo apt update
sudo apt install code -y
```

**Fedora:**
```bash
sudo rpm --import https://packages.microsoft.com/keys/microsoft.asc
sudo sh -c 'echo -e "[code]\nname=Visual Studio Code\nbaseurl=https://packages.microsoft.com/yumrepos/vscode\nenabled=1\ngpgcheck=1\ngpgkey=https://packages.microsoft.com/keys/microsoft.asc" > /etc/yum.repos.d/vscode.repo'
sudo dnf check-update
sudo dnf install code -y
```

**Arch Linux:**
```bash
yay -S visual-studio-code-bin
```

**Install Python Extension:**
- Open VS Code
- Press `Ctrl+Shift+X` to open Extensions
- Search for "Python"
- Install the extension by Microsoft

### Step 4: Install Git (Optional)

**Option A: Skip Git (Download ZIP instead)**
- You can download the repository as a ZIP file in Step 6
- Skip to Step 5 if you prefer not to install Git

**Option B: Install Git (Recommended for developers)**

**Ubuntu/Debian:**
```bash
sudo apt install git -y
```

**Fedora:**
```bash
sudo dnf install git -y
```

**Arch Linux:**
```bash
sudo pacman -S git
```

**Verify installation:**
```bash
git --version
```

### Step 5: Install ffmpeg

**Ubuntu/Debian:**
```bash
sudo apt install ffmpeg -y
```

**Fedora:**
```bash
sudo dnf install ffmpeg -y
```

**Arch Linux:**
```bash
sudo pacman -S ffmpeg
```

**Verify installation:**
```bash
ffmpeg -version
```

### Step 6: Get the Repository

**Option A: Download as ZIP (No Git Required)**

1. **Download the repository:**
   - Visit the repository URL in your browser
   - Click the green "Code" button
   - Select "Download ZIP"
   - Save to your Downloads folder

2. **Extract and navigate:**
   ```bash
   cd ~/Downloads
   # Extract the ZIP (filename may vary)
   unzip practical-ai-for-se*.zip
   
   # Navigate to extracted folder (rename if needed)
   # If folder is named practical-ai-for-se-main or similar, rename it:
   mv practical-ai-for-se-* practical-ai-for-se
   cd practical-ai-for-se
   ```

3. **Open in VS Code:**
   ```bash
   code .
   ```

**Option B: Clone with Git (If Git Installed)**

1. **Navigate to your desired location:**
   ```bash
   cd ~/Documents
   ```

2. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd practical-ai-for-se
   ```

3. **Open in VS Code:**
   ```bash
   code .
   ```

### Step 7: Create Virtual Environment

Open VS Code's integrated terminal (`` Ctrl+` ``) or continue in terminal:

1. **Create virtual environment:**
   ```bash
   python3 -m venv .venv
   ```

2. **Activate virtual environment:**
   ```bash
   source .venv/bin/activate
   ```

3. **Confirm activation:**
   Your prompt should now show `(.venv)`:
   ```bash
   (.venv) user@linux:~/Documents/practical-ai-for-se$
   ```

### Step 8: Install Requirements

With virtual environment activated:

1. **First, upgrade pip, setuptools, and wheel:**
   ```bash
   python -m pip install --upgrade pip setuptools wheel
   ```

2. **Install all requirements:**
   ```bash
   pip install -r requirements.txt
   ```

   This will take a few minutes. Wait for all packages to install.

3. **Verify installation:**
   ```bash
   pip list
   ```

### Step 9: Test with Your First Transcription

1. **Navigate to module-01:**
   ```bash
   cd module-01
   ```

2. **Check the audio file:**
   
   The repository includes `welcome.mp3` for testing.
   
   You can also use any of your own `.mp3`, `.wav`, or `.m4a` files.

3. **Run transcription:**
   ```bash
   python whisper_local.py welcome.mp3
   ```

4. **Wait for processing:**
   - First time will download Whisper model (~140MB)
   - Transcription will take a moment depending on audio length
   - Output will be saved as `welcome.txt`

5. **View the result:**
   ```bash
   # View in terminal
   cat welcome.txt
   
   # Or open in VS Code
   code welcome.txt
   ```

6. **Try with timestamps:**
   ```bash
   python whisper_local.py welcome.mp3 --timestamps
   ```

### 🎉 Success!

You've successfully completed the Linux setup!

---

**All Platforms - Next Steps:**
- Explore other tools in `module-02` (PowerPoint, Excel, YouTube conversion)
- Try AI agents in `module-08`
- Read the detailed documentation below

**Need Help?** See the [Troubleshooting](#-troubleshooting) section below.

---

## 📋 Prerequisites

- **Python 3.8+** (verify: `python --version`)
- **ffmpeg** (required for audio/video processing)
- **Git** (optional - for cloning the repository, or download as ZIP)

## 🚀 Quick Start

### 1. Install System Dependencies

#### ffmpeg Installation

**Windows (using Chocolatey):**
```powershell
choco install ffmpeg
```

Or download manually from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH.

**macOS (using Homebrew):**
```bash
brew install ffmpeg
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install ffmpeg
```

**Verify installation:**
```bash
ffmpeg -version
```

### 2. Clone Repository

```bash
git clone <repository-url>
cd practical-ai-for-se
```

### 3. Create Python Virtual Environment

#### Windows (PowerShell):
```powershell
# Create virtual environment
python -m venv .venv

# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# If you get execution policy error, run:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### Windows (Command Prompt):
```cmd
# Create virtual environment
python -m venv .venv

# Activate virtual environment
.venv\Scripts\activate.bat
```

#### macOS/Linux:
```bash
# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate
```

**Note:** Your terminal prompt should now show `(.venv)` indicating the virtual environment is active.

### 4. Install Python Dependencies

With virtual environment activated:

```bash
pip install -r requirements.txt
```

**First-time setup notes:**
- Whisper models will download automatically on first use (40MB-3GB)
- For Playwright: `playwright install chromium` (for web scraping tools)

### 5. Verify Installation

```bash
# Check docling
docling --version

# Check Python packages
pip list
```

## 📁 Project Structure

```
practical-ai-for-se/
├── module-01/              # Audio transcription with Whisper
│   └── whisper_local.py   # Local audio transcription CLI
│
├── module-02/              # Document conversion tools
│   ├── pptx2md.py         # PowerPoint → Markdown (with speaker notes)
│   ├── xlsx2md.py         # Excel → Markdown (with formula evaluation)
│   ├── media2md.py        # Video/Audio → Markdown transcription
│   └── www2md.py          # Web pages → Markdown (JS rendering support)
│
├── module-03/              # AI workflow demonstrations
│   ├── deep-research-demo/
│   ├── notebooklm-demo/
│   ├── presentation-demo/
│   └── rfp-analysis-demo/
│
├── module-08/              # AI agents and RAG examples
│   ├── 01_basic_agent.py          # Basic agent with YFinance
│   ├── 02_hacker_news_agent.py    # Security news aggregation
│   ├── 03_youtube_agent.py        # YouTube content analyzer
│   └── 04_simple_rag.py           # RAG with pgvector
│
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## 🛠️ Tools & Usage

### Document Conversion Tools (Module 02)

#### PowerPoint to Markdown

Convert presentations with speaker notes extraction:

```bash
cd module-02

# Basic conversion (includes speaker notes)
python pptx2md.py presentation.pptx

# Without speaker notes
python pptx2md.py presentation.pptx --no-notes

# Custom output
python pptx2md.py presentation.pptx output.md

# Show help
python pptx2md.py --help
```

**Features:**
- ✅ Extracts slide content and speaker notes
- ✅ Image export support (embedded/referenced/placeholder)
- ✅ Clean Markdown formatting

#### Excel to Markdown

Convert spreadsheets with automatic formula evaluation:

```bash
cd module-02

# Convert with formula evaluation
python xlsx2md.py spreadsheet.xlsx

# Custom output
python xlsx2md.py spreadsheet.xlsx output.md

# Show help
python xlsx2md.py --help
```

**Features:**
- ✅ Evaluates Excel formulas before conversion
- ✅ Converts all sheets in workbook
- ✅ Preserves table structure
- ✅ Supports .xlsx and .xlsm formats

**Note:** Excel file must have cached formula values (open and save once in Excel).

#### Media to Markdown

Transcribe YouTube videos or local media files:

```bash
cd module-02

# YouTube (fast - uses transcript API)
python media2md.py "https://www.youtube.com/watch?v=VIDEO_ID" --use-youtube-transcript

# YouTube (high quality - uses Whisper)
python media2md.py "https://www.youtube.com/watch?v=VIDEO_ID" --model whisper_base

# Local video file
python media2md.py video.mp4 --model whisper_base

# Local audio file
python media2md.py podcast.mp3

# Keep extracted audio
python media2md.py video.mp4 --keep-audio

# Show help
python media2md.py --help
```

**Supported Formats:**
- **Audio:** mp3, wav, m4a, flac, ogg, aac, wma
- **Video:** mp4, avi, mov, mkv, webm, flv, wmv, m4v, mpg, mpeg

**Whisper Models:**
- `whisper_tiny` - Fastest, lowest accuracy (default)
- `whisper_base` - Good balance
- `whisper_small` - Better accuracy
- `whisper_medium` - High accuracy, slower
- `whisper_large` - Very high accuracy
- `whisper_turbo` - Best accuracy, slowest

**Performance Comparison:**

| Method | Speed | Works With | Quality | Resources |
|--------|-------|------------|---------|-----------|
| YouTube Transcript API | ⚡ Seconds | YouTube only | Good | Minimal |
| Whisper | 🐢 Minutes | Everything | Excellent | CPU/GPU intensive |

#### Web Page to Markdown

Convert web pages with JavaScript rendering support:

```bash
cd module-02

# Basic conversion
python www2md.py "https://example.com"

# Custom output
python www2md.py "https://example.com" -o output.md

# Headless mode (no browser window)
python www2md.py "https://example.com" --headless

# Firefox browser
python www2md.py "https://example.com" --browser firefox

# Show help
python www2md.py --help
```

**Features:**
- ✅ JavaScript rendering support
- ✅ reCAPTCHA detection and handling
- ✅ Multiple browser engines (Chromium/Firefox/WebKit)
- ✅ Cloudflare bypass capabilities

### Audio Transcription (Module 01)

Local audio transcription without cloud services:

```bash
cd module-01

# Basic transcription
python whisper_local.py audio.mp3

# With timestamps
python whisper_local.py audio.mp3 --timestamps

# Custom output
python whisper_local.py audio.mp3 --output transcript.txt

# Show help
python whisper_local.py --help
```

### AI Agents (Module 08)

#### Basic Financial Agent

```bash
cd module-08

# Run basic agent (requires Ollama running locally)
python 01_basic_agent.py
```

Queries stock prices using YFinance integration.

#### Hacker News Security Agent

```bash
cd module-08

# Run security research agent
python 02_hacker_news_agent.py
```

Aggregates and summarizes security vulnerabilities from Hacker News.

#### YouTube Content Analyzer

```bash
cd module-08

# Configure OpenAI API key first
# Create .env file with: OPENAI_API_KEY=your_key_here

# Run YouTube analyzer
python 03_youtube_agent.py
```

Analyzes YouTube videos with timestamps and content breakdown.

#### RAG System with pgvector

```bash
cd module-08

# Setup PostgreSQL with pgvector first (see module-08/docker/docker-compose.yml)
# Update database connection string in 04_simple_rag.py

# Run RAG example
python 04_simple_rag.py
```

Demonstrates hybrid search (semantic + full-text) with markdown-aware chunking.

## 🔧 Common Tasks

### Activating Virtual Environment

**Windows PowerShell:**
```powershell
.\.venv\Scripts\Activate.ps1
```

**Windows Command Prompt:**
```cmd
.venv\Scripts\activate.bat
```

**macOS/Linux:**
```bash
source .venv/bin/activate
```

### Deactivating Virtual Environment

```bash
deactivate
```

### Updating Dependencies

```bash
pip install -r requirements.txt --upgrade
```

### Checking Installed Packages

```bash
pip list
```

## 🐛 Troubleshooting

### Windows PowerShell Execution Policy Error

If you get an error activating the virtual environment:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### ffmpeg Not Found

**Verify installation:**
```bash
ffmpeg -version
```

**If not installed:**
- Windows: `choco install ffmpeg` or download from [ffmpeg.org](https://ffmpeg.org/download.html)
- macOS: `brew install ffmpeg`
- Linux: `sudo apt install ffmpeg`

**Windows PATH issues:**
After manual installation, add ffmpeg to your system PATH:
1. Search for "Environment Variables" in Windows
2. Edit "Path" variable
3. Add ffmpeg bin directory (e.g., `C:\ffmpeg\bin`)
4. Restart terminal

### Virtual Environment Not Activating

**Windows:** Try Command Prompt instead of PowerShell
**macOS/Linux:** Make sure you use `source` command

### Missing Dependencies

Reinstall all dependencies:
```bash
pip install -r requirements.txt --force-reinstall
```

### Compilation Errors (scikit-image, meson, missing compiler)

**Error messages like:**
- "Unknown compiler(s): [['icl'], ['cl'], ['cc'], ['gcc']]"
- "ERROR: Failed to build scikit-image"
- "error: Microsoft Visual C++ 14.0 or greater is required"
- "meson.build:1:0: ERROR: Unknown compiler(s)"

**This happens because:**
- Some packages need to be compiled from C/C++ source code
- Your system lacks the required C/C++ compiler

**Solutions (in order of preference):**

1. **Upgrade pip first (most common fix):**
   ```bash
   python -m pip install --upgrade pip setuptools wheel
   pip install -r requirements.txt
   ```

2. **Force binary wheels:**
   ```bash
   pip install --only-binary :all: scikit-image
   pip install -r requirements.txt
   ```

3. **Install build tools for your platform:**

   **Windows:**
   - Download from: https://visualstudio.microsoft.com/downloads/
   - Install "Build Tools for Visual Studio 2022"
   - Select "Desktop development with C++"
   - Restart computer and retry

   **macOS:**
   ```bash
   xcode-select --install
   ```

   **Linux (Ubuntu/Debian):**
   ```bash
   sudo apt update
   sudo apt install build-essential python3-dev
   ```

   **Linux (Fedora):**
   ```bash
   sudo dnf groupinstall "Development Tools"
   sudo dnf install python3-devel
   ```

**Prevention:**
- Always use Python 3.11 or 3.12 for best binary wheel support
- Keep pip updated: `python -m pip install --upgrade pip`

### YouTube Transcript Not Available

The script automatically falls back to Whisper transcription. Or manually use Whisper:
```bash
python media2md.py "VIDEO_URL" --model whisper_base
```

### Whisper Model Download

First-time use downloads models automatically (40MB-3GB). Requires stable internet connection.

### Playwright Browser Not Installed

For web scraping tools:
```bash
playwright install chromium
```

### Python Version Issues

Verify you're using Python 3.8+:
```bash
python --version
```

If you have multiple Python versions, use:
- Windows: `py -3.8` or `py -3.9`, etc.
- macOS/Linux: `python3.8` or `python3.9`, etc.

## 📦 Dependencies

See [`requirements.txt`](requirements.txt) for complete list. Main dependencies:

**Document Processing:**
- docling - Document conversion
- openpyxl - Excel manipulation
- playwright - Web scraping

**Media Processing:**
- yt-dlp - YouTube download
- youtube-transcript-api - Fast YouTube transcripts
- openai-whisper - Audio transcription

**AI & LLM:**
- agno - Agent framework
- ollama - Local LLM
- openai - OpenAI API

**Vector Database:**
- sqlalchemy - Database ORM
- psycopg[binary] - PostgreSQL adapter
- pgvector - Vector similarity search

## 📚 Additional Resources

- [Docling Documentation](https://github.com/DS4SD/docling)
- [yt-dlp Documentation](https://github.com/yt-dlp/yt-dlp)
- [OpenAI Whisper](https://github.com/openai/whisper)
- [YouTube Transcript API](https://github.com/jdepoix/youtube-transcript-api)
- [Playwright Documentation](https://playwright.dev/python/)
- [pgvector Documentation](https://github.com/pgvector/pgvector)

## 🤝 Contributing

Contributions welcome! Please feel free to submit issues or pull requests.

## 📄 License

This project is provided as-is for educational and practical purposes.

---

**Need Help?** Check the troubleshooting section or open an issue on the repository.
