# Module 01: Fundamentals

Local audio transcription tool using OpenAI's Whisper speech recognition model. Process audio files privately on your machine without cloud services or API keys.

## 🎯 Overview

`whisper_local.py` is a command-line tool that automatically transcribes audio files to text using the Whisper ASR (Automatic Speech Recognition) model. All processing happens locally on your machine, ensuring privacy and requiring no internet connection after the initial model download.

## ✨ Features

- 🎤 **Local transcription** - All processing happens on your machine, no cloud required
- 🔒 **Privacy-focused** - No data sent to external services
- 📝 **Multiple output formats** - Plain text or timestamped transcripts
- 🎯 **Simple CLI interface** - Easy to use from the command line
- 🔧 **Flexible output** - Auto-generates output files or specify custom paths
- ⚡ **Multiple audio formats** - Supports mp3, mp4, wav, m4a, webm, and more
- 🌍 **Multi-language** - Automatic language detection

## 📋 Prerequisites

Before using this tool, ensure you have:

- **Python 3.8+** installed
- **ffmpeg** installed (required for audio processing)
- **Virtual environment** activated (see main [README](../README.md))

**New to this project?** See the main [README.md](../README.md) for complete setup instructions including Python, ffmpeg, and virtual environment setup.

## 🚀 Quick Start

1. **Activate your virtual environment:**

   **Windows (PowerShell):**
   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

   **macOS/Linux:**
   ```bash
   source .venv/bin/activate
   ```

2. **Navigate to module-01:**
   ```bash
   cd module-01
   ```

3. **Transcribe the included sample:**
   ```bash
   python whisper_local.py welcome.mp3
   ```

4. **View the result:**
   
   **Windows:**
   ```powershell
   type welcome.txt
   ```

   **macOS/Linux:**
   ```bash
   cat welcome.txt
   ```

**Note:** First run will download the Whisper base model (~140MB).

## 🔧 Installation

### System Dependencies

**ffmpeg** (required for audio processing):

**Windows (using Chocolatey):**
```powershell
choco install ffmpeg
```

Or download manually from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH.

**macOS:**
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

### Python Dependencies

With your virtual environment activated:

```bash
# Install from project root
pip install -r requirements.txt

# Or install individually
pip install openai-whisper
```

**Note:** First run will automatically download the Whisper base model (~140MB).

## 📖 Usage

### Basic Usage

Transcribe an audio file to plain text:

```bash
python whisper_local.py audio.mp3
```

This creates `audio.txt` in the same directory as the input file.

### With Timestamps

Include timestamps in the transcript:

```bash
python whisper_local.py audio.mp3 --timestamps
```

**Output format:**
```
[00:00:00] First segment of speech
[00:00:05] Second segment of speech
[00:00:12] Third segment of speech
```

### Custom Output Path

Specify a custom output file location:

```bash
python whisper_local.py audio.mp3 --output my_transcript.txt
```

### Combined Options

Use multiple flags together:

```bash
python whisper_local.py recording.wav --timestamps --output transcript.txt
```

### Get Help

View all available options:

```bash
python whisper_local.py --help
```

## 📝 Command-Line Arguments

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `audio_file` | positional | Yes | Path to the audio file to transcribe |
| `--timestamps` | flag | No | Include timestamps in output (format: [HH:MM:SS]) |
| `--output`, `-o` | string | No | Custom output file path (default: same directory with .txt extension) |
| `--help`, `-h` | flag | No | Show help message and exit |

## 🎵 Supported Audio Formats

The script supports all audio formats that ffmpeg can process, including:

| Format | Extensions |
|--------|------------|
| MP3 | `.mp3` |
| MP4 Audio | `.mp4`, `.m4a` |
| WAV | `.wav` |
| WebM | `.webm` |
| MPEG | `.mpeg`, `.mpga` |
| FLAC | `.flac` |
| OGG | `.ogg` |

And many more...

## 💡 Examples

### Transcribe the included sample

```bash
python whisper_local.py welcome.mp3
# Creates: welcome.txt
```

### Transcribe a podcast episode

```bash
python whisper_local.py podcast-episode-42.mp3
# Creates: podcast-episode-42.txt
```

### Transcribe a meeting recording with timestamps

```bash
python whisper_local.py meeting-2024-11-10.wav --timestamps
# Creates: meeting-2024-11-10.txt with timestamps
```

### Transcribe and save to a specific location

```bash
python whisper_local.py interview.m4a --output ~/Documents/interview-transcript.txt
```

### Transcribe multiple files (using a shell loop)

**Bash (macOS/Linux):**
```bash
for file in *.mp3; do
    python whisper_local.py "$file"
done
```

**PowerShell (Windows):**
```powershell
Get-ChildItem *.mp3 | ForEach-Object {
    python whisper_local.py $_.Name
}
```

## 🤖 Whisper Model

This script uses the **base** Whisper model, which provides an optimal balance between:
- **Speed**: Fast transcription on most hardware
- **Accuracy**: Good transcription quality for most use cases
- **Size**: Moderate download size (~140MB)

### Model Details

| Property | Value |
|----------|-------|
| **Language support** | Multi-language (automatic detection) |
| **Model size** | base (~140MB) |
| **Performance** | Suitable for CPU or GPU processing |
| **First download** | ~140MB, one-time operation |

### Available Models

While this script uses the base model, Whisper offers several models:

| Model | Size | Speed | Accuracy | Use Case |
|-------|------|-------|----------|----------|
| tiny | ~40MB | Very fast | Lower | Quick drafts |
| base | ~140MB | Fast | Good | General use ✅ |
| small | ~460MB | Moderate | Better | Higher accuracy |
| medium | ~1.5GB | Slow | High | Professional use |
| large | ~3GB | Very slow | Highest | Maximum accuracy |

**Note:** To use a different model, you would need to modify the script's `load_model()` call.

## ⚡ Performance Considerations

### Processing Time
- **Typical**: 1-5 minutes for a 10-minute audio file on modern CPUs
- **GPU acceleration**: Significantly faster if CUDA-enabled GPU is available
- **First run**: Allow extra time for model download (~140MB)

### Resource Usage
- **Memory**: Moderate (typically 1-2GB during processing)
- **CPU**: Uses available cores efficiently
- **Disk**: ~140MB for model storage

### Optimization Tips
- Use SSD for faster model loading
- Close unnecessary applications to free up memory
- Consider GPU acceleration for large batches

## 🐛 Troubleshooting

### Error: "openai-whisper is not installed"

**Solution:** Install the package:
```bash
pip install openai-whisper
```

### Error: ffmpeg related errors

**Solution:** Verify ffmpeg is installed:
```bash
# Test installation
ffmpeg -version

# If not installed:
# Windows: choco install ffmpeg
# macOS: brew install ffmpeg
# Linux: sudo apt install ffmpeg
```

### Error: "Audio file not found"

**Solution:** Verify the file path is correct:
```bash
# Use absolute path if needed
python whisper_local.py /full/path/to/audio.mp3

# Or navigate to the directory first
cd /path/to/audio/files
python whisper_local.py audio.mp3
```

### Slow transcription

**Solutions:**
- The base model is already optimized for speed
- Close other applications to free up resources
- Use a machine with more CPU cores
- Enable GPU acceleration (requires CUDA-compatible GPU)
- Process shorter audio segments

### Virtual environment not activated

**Solution:** Activate your virtual environment first:

**Windows (PowerShell):**
```powershell
.\.venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**
```cmd
.venv\Scripts\activate.bat
```

**macOS/Linux:**
```bash
source .venv/bin/activate
```

You should see `(.venv)` at the start of your prompt.

## 🔍 Technical Details

| Property | Value |
|----------|-------|
| **Python version** | Python 3.8+ |
| **Model** | OpenAI Whisper base model |
| **Output encoding** | UTF-8 |
| **Timestamp format** | [HH:MM:SS] |
| **Language detection** | Automatic |
| **Privacy** | 100% local processing |

## 🗂️ Project Structure

```
module-01/
├── whisper_local.py    # Main transcription script
├── welcome.mp3         # Sample audio file for testing
└── README.md          # This file
```

## 📚 Additional Resources

- [OpenAI Whisper Repository](https://github.com/openai/whisper)
- [Whisper Paper](https://arxiv.org/abs/2212.04356)
- [FFmpeg Documentation](https://ffmpeg.org/documentation.html)
- [Main Project README](../README.md) - Complete setup guide

## 📄 License

This script uses OpenAI's Whisper model, which is released under the MIT License.

---

**Need help?** See the main [README](../README.md) or check the [Troubleshooting](#-troubleshooting) section above.
