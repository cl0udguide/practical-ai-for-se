# Practice Lesson: Converting ANY popular document format to markdown

## Setup

First, make sure that the Python virtual environment is activated.

From the root directory with exercises, run this:

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

Then change the directory to module-02:

**All platforms:**
```bash
cd module-02
```

Then double-check if docling was properly installed:

```bash
docling --version
```

To display docling help:

```bash
docling --help
```

---

## Converting PDF Files

### Default image export mode (embedded images):

```bash
docling document.pdf --to md
```

### "Referenced" image export mode (images saved as separate files):

```bash
docling document.pdf --to md --image-export-mode referenced
```

### "Placeholder" image export mode (image placeholders only):

```bash
docling document.pdf --to md --image-export-mode placeholder
```

### Remove image placeholders from markdown

**Windows (PowerShell):**
```powershell
$file = 'output.md'; $content = Get-Content $file | Where-Object { $_ -notmatch '<!-- *image *-->' }; $content | Set-Content $file
```

**macOS:**
```bash
sed -i '' '/<!-- *image *-->/ {N;d;}' output.md
```

**Linux:**
```bash
sed -i '/<!-- *image *-->/ {N;d;}' output.md
```

---

## Converting MS Word (DOCX) Files

```bash
docling document.docx --to md --image-export-mode placeholder
```

---

## Converting MS PowerPoint (PPTX) Files

### Using docling (basic conversion):

```bash
docling presentation.pptx --to md --image-export-mode placeholder
```

### Using pptx2md.py (with speaker notes):

Display help:

```bash
python pptx2md.py --help
```

Convert with speaker notes:

**All platforms:**
```bash
python pptx2md.py presentation.pptx
```

Custom output file:

```bash
python pptx2md.py presentation.pptx output.md
```

Without speaker notes:

```bash
python pptx2md.py presentation.pptx --no-notes
```

---

## Converting MS Excel (XLSX) Files

### Using docling (basic conversion):

```bash
docling spreadsheet.xlsx --to md --image-export-mode placeholder
```

### Using xlsx2md.py (with formula evaluation):

Display help:

```bash
python xlsx2md.py --help
```

Convert with evaluated formulas:

**All platforms:**
```bash
python xlsx2md.py spreadsheet.xlsx
```

Custom output file:

```bash
python xlsx2md.py spreadsheet.xlsx output.md
```

---

## Converting Websites

### Using docling (basic conversion):

```bash
docling https://example.com/ --to md --image-export-mode placeholder
```

### Using www2md.py (with JavaScript rendering and bot protection bypass):

Display help:

```bash
python www2md.py --help
```

Basic conversion:

**All platforms:**
```bash
python www2md.py https://example.com
```

With custom output:

```bash
python www2md.py https://example.com -o output.md
```

Headless mode (no browser window):

```bash
python www2md.py https://example.com --headless
```

Using Firefox browser:

```bash
python www2md.py https://example.com --browser firefox
```

---

## Converting Media Files (Audio/Video)

### Display help:

```bash
python media2md.py --help
```

### YouTube videos (using YouTube Transcript API - fastest):

**All platforms:**
```bash
python media2md.py "https://www.youtube.com/watch?v=VIDEO_ID" --use-youtube-transcript
```

### YouTube videos (using Whisper - higher quality):

```bash
python media2md.py "https://www.youtube.com/watch?v=VIDEO_ID" --model whisper_base
```

### Local audio files:

```bash
python media2md.py audio.mp3
```

### Local video files:

```bash
python media2md.py video.mp4 --model whisper_base
```

### Keep extracted audio file:

```bash
python media2md.py video.mp4 --keep-audio
```

---

## Supported File Formats

- **Documents:** PDF, DOCX
- **Presentations:** PPTX
- **Spreadsheets:** XLSX, XLSM
- **Audio:** MP3, WAV, M4A, FLAC, OGG, AAC, WMA
- **Video:** MP4, AVI, MOV, MKV, WEBM, FLV, WMV, M4V, MPG, MPEG
- **Web:** Any URL (with JavaScript rendering support)
