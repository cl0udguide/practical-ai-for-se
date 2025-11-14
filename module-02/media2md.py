#!/usr/bin/env python3
"""
Simple CLI tool to convert media (audio/video files or YouTube) to Markdown with transcription.
Uses yt-dlp for audio extraction and docling for transcription.
"""

import os
import re
import shutil
import sys
import tempfile
from pathlib import Path
from urllib.parse import urlparse

from docling.datamodel.base_models import InputFormat
from docling.document_converter import AudioFormatOption, DocumentConverter


def is_url(string: str) -> bool:
    """Check if the input string is a URL."""
    try:
        result = urlparse(string)
        return all([result.scheme, result.netloc])
    except Exception:
        return False


def extract_youtube_video_id(url: str) -> str:
    """
    Extract the video ID from a YouTube URL.

    Args:
        url: YouTube URL

    Returns:
        Video ID string, or None if not found
    """
    import re

    # Patterns for various YouTube URL formats
    patterns = [
        r"(?:youtube\.com\/watch\?v=|youtu\.be\/)([^&\n?#]+)",
        r"youtube\.com\/embed\/([^&\n?#]+)",
        r"youtube\.com\/v\/([^&\n?#]+)",
    ]

    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)

    return None


def fetch_youtube_transcript(url: str, title: str = None) -> tuple:
    """
    Fetch transcript directly from YouTube.

    Args:
        url: YouTube URL
        title: Optional title for the video

    Returns:
        Tuple of (transcript_text, video_title)
    """
    try:
        import subprocess

        from youtube_transcript_api import YouTubeTranscriptApi

        video_id = extract_youtube_video_id(url)
        if not video_id:
            raise ValueError("Could not extract video ID from URL")

        print(f"Fetching transcript from YouTube for video: {video_id}")

        # Get the transcript using the YouTubeTranscriptApi instance
        api = YouTubeTranscriptApi()
        transcript_obj = api.fetch(video_id, languages=["en"])

        # Combine all text segments (transcript_obj is iterable of FetchedTranscriptSnippet objects)
        full_text = " ".join(item.text for item in transcript_obj)

        # Get video title if not provided
        if not title:
            # Try to get title from yt-dlp metadata
            try:
                result = subprocess.run(
                    ["yt-dlp", "--get-title", url],
                    capture_output=True,
                    text=True,
                    check=True,
                )
                title = result.stdout.strip()
            except Exception:
                title = f"YouTube Video {video_id}"

        print(f"✓ Transcript fetched successfully from YouTube")
        return full_text, title

    except Exception as e:
        raise RuntimeError(f"Failed to fetch YouTube transcript: {e}")


def download_audio_from_url(url: str, output_dir: str) -> Path:
    """
    Download audio from a YouTube URL using yt-dlp.

    Args:
        url: YouTube or other video URL
        output_dir: Directory to save the audio file

    Returns:
        Path to the downloaded audio file
    """
    import subprocess

    print(f"Downloading audio from: {url}")

    # Use yt-dlp to download audio only
    output_template = str(Path(output_dir) / "%(title)s.%(ext)s")

    try:
        # Download audio in best quality, convert to mp3
        result = subprocess.run(
            [
                "yt-dlp",
                "-x",  # Extract audio
                "--audio-format",
                "mp3",
                "--audio-quality",
                "0",  # Best quality
                "-o",
                output_template,
                "--print",
                "after_move:filepath",  # Print final file path
                url,
            ],
            check=True,
            capture_output=True,
            text=True,
        )

        # Get the output file path from yt-dlp
        output_lines = result.stdout.strip().split("\n")
        audio_file = None

        # Find the filepath line
        for line in output_lines:
            if line and not line.startswith("["):
                audio_file = line.strip()

        if not audio_file or not Path(audio_file).exists():
            # Fallback: try to find the file in the output directory
            audio_files = list(Path(output_dir).glob("*.mp3"))
            if audio_files:
                audio_file = str(audio_files[0])
            else:
                raise FileNotFoundError("Could not find downloaded audio file")

        print(f"✓ Audio downloaded: {Path(audio_file).name}")
        return Path(audio_file)

    except subprocess.CalledProcessError as e:
        print(f"Error downloading audio: {e}")
        print(f"stderr: {e.stderr}")
        raise
    except FileNotFoundError:
        print("Error: yt-dlp is not installed.")
        print("Please install it with: pip install yt-dlp")
        sys.exit(1)


def extract_audio_from_video(video_path: Path, output_dir: str) -> Path:
    """
    Extract audio from a local video file using ffmpeg.

    Args:
        video_path: Path to the local video file
        output_dir: Directory to save the audio file

    Returns:
        Path to the extracted audio file
    """
    import subprocess

    print(f"Extracting audio from: {video_path.name}")

    output_file = Path(output_dir) / f"{video_path.stem}.mp3"

    # Resolve to absolute path to avoid issues with spaces in filenames
    absolute_video_path = video_path.resolve()

    try:
        # Use ffmpeg to extract audio from local file (more reliable for local files than yt-dlp)
        subprocess.run(
            [
                "ffmpeg",
                "-i",
                str(absolute_video_path),  # Input file
                "-vn",  # No video
                "-acodec",
                "libmp3lame",  # MP3 codec
                "-q:a",
                "0",  # Best quality
                "-y",  # Overwrite output file
                str(output_file),
            ],
            check=True,
            capture_output=True,
            text=True,
        )

        print(f"✓ Audio extracted: {output_file.name}")
        return output_file

    except subprocess.CalledProcessError as e:
        print(f"Error extracting audio: {e}")
        print(f"stderr: {e.stderr}")
        raise
    except FileNotFoundError:
        print("Error: ffmpeg is not installed.")
        print("Please install it with:")
        print("  macOS: brew install ffmpeg")
        print("  Ubuntu/Debian: sudo apt install ffmpeg")
        print("  Windows: Download from https://ffmpeg.org/download.html")
        sys.exit(1)


def convert_audio_to_markdown(
    audio_path: Path,
    output_file: str = None,
    asr_model: str = "whisper_tiny",
    title: str = None,
) -> Path:
    """
    Convert an audio file to Markdown using docling.

    Args:
        audio_path: Path to the audio file
        output_file: Path to the output Markdown file (optional)
        asr_model: ASR model to use for transcription
        title: Title to add as headline (optional)

    Returns:
        Path to the output Markdown file
    """
    # Set output path
    if output_file is None:
        output_path = audio_path.with_suffix(".md")
    else:
        output_path = Path(output_file)

    print(f"Transcribing audio with {asr_model} model...")
    print("(This may take a while depending on the audio length)")

    try:
        # Configure converter for audio files
        from docling.datamodel import asr_model_specs
        from docling.datamodel.pipeline_options import AsrPipelineOptions
        from docling.pipeline.asr_pipeline import AsrPipeline

        # Map model name to model spec
        model_map = {
            "whisper_tiny": asr_model_specs.WHISPER_TINY,
            "whisper_base": asr_model_specs.WHISPER_BASE,
            "whisper_small": asr_model_specs.WHISPER_SMALL,
            "whisper_medium": asr_model_specs.WHISPER_MEDIUM,
            "whisper_large": asr_model_specs.WHISPER_LARGE,
            "whisper_turbo": asr_model_specs.WHISPER_TURBO,
        }

        if asr_model not in model_map:
            print(f"Warning: Unknown model '{asr_model}', using whisper_tiny")
            asr_model = "whisper_tiny"

        asr_options = model_map[asr_model]
        pipeline_options = AsrPipelineOptions(asr_options=asr_options)

        # Create proper AudioFormatOption
        audio_format_option = AudioFormatOption(
            pipeline_cls=AsrPipeline,
            pipeline_options=pipeline_options,
        )

        converter = DocumentConverter(
            allowed_formats=[InputFormat.AUDIO],
            format_options={InputFormat.AUDIO: audio_format_option},
        )

        # Convert the audio file
        result = converter.convert(str(audio_path))

        # Export to Markdown
        markdown_content = result.document.export_to_markdown()

        # Post-process the markdown content
        # Remove timestamp markers [time: X-Y]
        markdown_content = re.sub(r"\[time: [0-9.]+-[0-9.]+\]\s*", "", markdown_content)

        # Consolidate fragmented text into proper paragraphs
        # Remove all newlines and join into a single text first
        lines = [line.strip() for line in markdown_content.split("\n") if line.strip()]
        full_text = " ".join(lines)

        # Split on sentence boundaries
        sentences = re.split(r"([.!?])\s+", full_text)

        # Reconstruct with proper paragraph breaks
        paragraphs = []
        current_para = []
        sentence_count = 0

        for i in range(0, len(sentences) - 1, 2):
            sentence = sentences[i] + (
                sentences[i + 1] if i + 1 < len(sentences) else ""
            )
            current_para.append(sentence.strip())
            sentence_count += 1

            # Create paragraph break every 3-5 sentences or at transition keywords
            if sentence_count >= 4 or any(
                keyword in sentence.lower()
                for keyword in [
                    "let's",
                    "next,",
                    "first,",
                    "finally,",
                    "however,",
                    "moreover,",
                ]
            ):
                if current_para:
                    paragraphs.append(" ".join(current_para))
                    current_para = []
                    sentence_count = 0

        # Add any remaining sentences
        if current_para:
            paragraphs.append(" ".join(current_para))

        # Filter out any empty paragraphs and join with single newline (no empty lines)
        paragraphs = [p.strip() for p in paragraphs if p.strip()]
        markdown_content = "\n".join(paragraphs)

        # Add title as headline if provided (with one empty line after title)
        if title:
            markdown_content = f"# {title}\n\n{markdown_content}"

        # Final cleanup: ensure no extra empty lines
        markdown_content = re.sub(r"\n{3,}", "\n", markdown_content)

        # Write to output file
        output_path.write_text(markdown_content, encoding="utf-8")

        print(f"✓ Successfully transcribed to '{output_path}'")
        return output_path

    except Exception as e:
        print(f"Error during transcription: {e}")
        raise


def process_youtube_transcript_to_markdown(
    transcript_text: str, title: str, output_file: str = None
) -> Path:
    """
    Process YouTube transcript text into formatted Markdown.

    Args:
        transcript_text: Raw transcript text from YouTube
        title: Video title
        output_file: Optional output file path

    Returns:
        Path to the output Markdown file
    """
    # Set output path
    if output_file is None:
        output_path = Path.cwd() / f"{title}.md"
    else:
        output_path = Path(output_file)

    print(f"Processing transcript...")

    # Clean up the text
    lines = [line.strip() for line in transcript_text.split("\n") if line.strip()]
    full_text = " ".join(lines)

    # Remove multiple spaces (YouTube transcripts often have extra spaces)
    full_text = re.sub(r"\s+", " ", full_text)

    # Split on sentence boundaries
    sentences = re.split(r"([.!?])\s+", full_text)

    # Reconstruct with proper paragraph breaks
    paragraphs = []
    current_para = []
    sentence_count = 0

    for i in range(0, len(sentences) - 1, 2):
        sentence = sentences[i] + (sentences[i + 1] if i + 1 < len(sentences) else "")
        current_para.append(sentence.strip())
        sentence_count += 1

        # Create paragraph break every 3-5 sentences or at transition keywords
        if sentence_count >= 4 or any(
            keyword in sentence.lower()
            for keyword in [
                "let's",
                "next,",
                "first,",
                "finally,",
                "however,",
                "moreover,",
            ]
        ):
            if current_para:
                paragraphs.append(" ".join(current_para))
                current_para = []
                sentence_count = 0

    # Add any remaining sentences
    if current_para:
        paragraphs.append(" ".join(current_para))

    # Filter out any empty paragraphs and join with single newline
    paragraphs = [p.strip() for p in paragraphs if p.strip()]
    markdown_content = "\n".join(paragraphs)

    # Add title
    markdown_content = f"# {title}\n\n{markdown_content}"

    # Final cleanup
    markdown_content = re.sub(r"\n{3,}", "\n", markdown_content)

    # Write to output file
    output_path.write_text(markdown_content, encoding="utf-8")

    print(f"✓ Successfully processed to '{output_path}'")
    return output_path


def convert_video_to_markdown(
    input_source: str,
    output_file: str = None,
    asr_model: str = "whisper_tiny",
    keep_audio: bool = False,
    use_youtube_transcript: bool = False,
):
    """
    Convert a video (YouTube URL or local file) to Markdown with transcription.

    Args:
        input_source: YouTube URL or path to local video file
        output_file: Path to the output Markdown file (optional)
        asr_model: ASR model to use (whisper_tiny, whisper_base, etc.)
        keep_audio: Whether to keep the extracted audio file
        use_youtube_transcript: Use YouTube's transcript API (faster, YouTube only)
    """
    temp_dir = None
    audio_file = None
    is_temp_audio = False
    original_input_name = None

    try:
        # Check if we should use YouTube transcript API
        if is_url(input_source) and use_youtube_transcript:
            # Try to fetch transcript from YouTube
            try:
                transcript_text, video_title = fetch_youtube_transcript(input_source)
                output_path = process_youtube_transcript_to_markdown(
                    transcript_text, video_title, output_file
                )

                print(f"\n✓ Conversion complete!")
                print(f"  Output: {output_path}")
                print(f"  Method: YouTube Transcript API (fast)")
                return
            except Exception as e:
                print(f"⚠ YouTube transcript not available: {e}")
                print(f"  Falling back to audio transcription...")

        if is_url(input_source):
            # Create a temporary directory for downloads
            temp_dir = tempfile.mkdtemp(prefix="media2md_")
            audio_file = download_audio_from_url(input_source, temp_dir)
            is_temp_audio = not keep_audio
            # Save the filename for default output naming
            original_input_name = audio_file.stem
        else:
            # Local file
            input_path = Path(input_source)

            if not input_path.exists():
                print(f"Error: File '{input_source}' not found.")
                sys.exit(1)

            # Save the original filename for default output naming
            original_input_name = input_path.stem

            # Check if it's already an audio file
            audio_extensions = [".mp3", ".wav", ".m4a", ".flac", ".ogg", ".aac", ".wma"]
            if input_path.suffix.lower() in audio_extensions:
                print(f"Input is already an audio file: {input_path.name}")
                audio_file = input_path
                is_temp_audio = False
            else:
                # Extract audio from video
                temp_dir = tempfile.mkdtemp(prefix="media2md_")
                audio_file = extract_audio_from_video(input_path, temp_dir)
                is_temp_audio = not keep_audio

        # If no output file specified, use current directory with original input name
        if output_file is None:
            output_file = str(Path.cwd() / f"{original_input_name}.md")

        # Convert audio to markdown with title
        output_path = convert_audio_to_markdown(
            audio_file, output_file, asr_model, title=original_input_name
        )

        # Handle audio file cleanup/saving
        if is_temp_audio and audio_file:
            print(f"Cleaning up temporary audio file...")
            audio_file.unlink()
        elif not is_temp_audio and audio_file and audio_file != Path(input_source):
            # If keeping audio from URL/video, move it to current directory
            if is_url(input_source) or (audio_file.parent != Path(input_source).parent):
                saved_audio_path = Path.cwd() / audio_file.name
                shutil.move(str(audio_file), str(saved_audio_path))
                print(f"Audio file saved: {saved_audio_path}")
            else:
                print(f"Audio file saved: {audio_file}")

        print(f"\n✓ Conversion complete!")
        print(f"  Output: {output_path}")

    except Exception as e:
        print(f"\n✗ Conversion failed: {e}")
        sys.exit(1)
    finally:
        # Clean up temporary directory
        if temp_dir and Path(temp_dir).exists():
            try:
                shutil.rmtree(temp_dir)
            except Exception:
                pass


def print_usage():
    """Print usage information."""
    print("""
Usage: python media2md.py <input> [output.md] [options]

Arguments:
  input         YouTube URL or path to a local video/audio file
  output.md     (Optional) Path to the output Markdown file
                If not specified, saves to current directory with input name + .md

Supported File Formats:
  Audio Files:  .mp3, .wav, .m4a, .flac, .ogg, .aac, .wma
  Video Files:  .mp4, .avi, .mov, .mkv, .webm, .flv, .wmv, .m4v, .mpg, .mpeg
  
  Note: Any format supported by yt-dlp can be processed

Options:
  --model MODEL       ASR model to use for transcription
                      Options: whisper_tiny (default, fastest), whisper_base,
                               whisper_small, whisper_medium, whisper_large,
                               whisper_turbo (most accurate but slower)
  --keep-audio        Keep the extracted audio file (for video files)
  --use-youtube-transcript
                      Use YouTube's transcript API (faster, YouTube only)
                      Falls back to audio transcription if not available
  --help, -h          Show this help message

Examples:
  # Transcribe a YouTube video (fastest - uses YouTube's transcript)
  python media2md.py "https://www.youtube.com/watch?v=VIDEO_ID" --use-youtube-transcript
  
  # Transcribe a YouTube video with Whisper (more accurate for some videos)
  python media2md.py "https://www.youtube.com/watch?v=VIDEO_ID"
  
  # Transcribe a local video file
  python media2md.py presentation.mp4
  
  # Use a more accurate (but slower) model
  python media2md.py video.mp4 --model whisper_base
  
  # Specify output file and keep audio
  python media2md.py video.mp4 transcript.md --keep-audio
  
  # Transcribe an audio file directly
  python media2md.py audio.mp3

Note:
  - Requires yt-dlp to be installed: pip install yt-dlp
  - First run will download the Whisper model (can take a few minutes)
  - Larger models are more accurate but slower and use more memory
""")


def main():
    """Main entry point for the CLI."""
    args = sys.argv[1:]

    # Check for help flag
    if not args or "--help" in args or "-h" in args:
        print_usage()
        sys.exit(0)

    # Parse arguments
    input_source = None
    output_file = None
    asr_model = "whisper_tiny"
    keep_audio = False
    use_youtube_transcript = False

    i = 0
    while i < len(args):
        arg = args[i]

        if arg == "--model":
            if i + 1 < len(args):
                asr_model = args[i + 1]
                i += 2
            else:
                print("Error: --model requires a value")
                sys.exit(1)
        elif arg == "--keep-audio":
            keep_audio = True
            i += 1
        elif arg == "--use-youtube-transcript":
            use_youtube_transcript = True
            i += 1
        elif input_source is None:
            input_source = arg
            i += 1
        elif output_file is None and not arg.startswith("--"):
            output_file = arg
            i += 1
        else:
            print(f"Error: Unknown argument '{arg}'")
            print_usage()
            sys.exit(1)

    if input_source is None:
        print("Error: No input source specified.")
        print_usage()
        sys.exit(1)

    # Convert the video
    convert_video_to_markdown(
        input_source, output_file, asr_model, keep_audio, use_youtube_transcript
    )


if __name__ == "__main__":
    main()
