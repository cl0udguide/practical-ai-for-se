#!/usr/bin/env python3
"""
Whisper Local Transcription Script

A CLI tool for transcribing audio files locally using OpenAI's Whisper model.
Automatically generates text transcripts in the same directory as the input file.
"""

import argparse
import os
import sys
from pathlib import Path

try:
    import whisper  # type: ignore
except ImportError:
    # Allow --help or no args to work even without whisper installed
    if "--help" in sys.argv or "-h" in sys.argv or len(sys.argv) == 1:
        whisper = None
    else:
        print("Error: openai-whisper is not installed.", file=sys.stderr)
        print(
            "Please install it using: pip install openai-whisper",
            file=sys.stderr,
        )
        sys.exit(1)


def format_timestamp(seconds):
    """Convert seconds to HH:MM:SS format."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    return f"[{hours:02d}:{minutes:02d}:{secs:02d}]"


def transcribe_audio(audio_path, output_path, include_timestamps=False):
    """
    Transcribe an audio file using Whisper.

    Args:
        audio_path: Path to the input audio file
        output_path: Path to the output transcript file
        include_timestamps: Whether to include timestamps in the output
    """
    # Check if input file exists
    if not os.path.isfile(audio_path):
        print(f"Error: Audio file not found: {audio_path}", file=sys.stderr)
        sys.exit(1)

    if whisper is None:
        print("Error: openai-whisper is not installed.", file=sys.stderr)
        print(
            "Please install it using: pip install openai-whisper",
            file=sys.stderr,
        )
        sys.exit(1)

    print("Loading Whisper model (base)...")
    try:
        model = whisper.load_model("base")
    except (RuntimeError, OSError, ValueError) as e:
        print(f"Error loading Whisper model: {e}", file=sys.stderr)
        print(
            "\nNote: If this is your first time using Whisper, the model will be downloaded.",
            file=sys.stderr,
        )
        print(
            "This may take a few minutes depending on your internet connection.",
            file=sys.stderr,
        )
        sys.exit(1)

    print(f"Transcribing audio file: {audio_path}")
    print("This may take a few minutes depending on the file length...")

    try:
        result = model.transcribe(audio_path)
    except (RuntimeError, OSError, ValueError) as e:
        print(f"Error during transcription: {e}", file=sys.stderr)
        print("\nNote: Make sure ffmpeg is installed on your system.", file=sys.stderr)
        print("  macOS:         brew install ffmpeg", file=sys.stderr)
        print("  Ubuntu/Debian: sudo apt install ffmpeg", file=sys.stderr)
        print(
            "  Windows:       Download from https://ffmpeg.org/download.html",
            file=sys.stderr,
        )
        sys.exit(1)

    # Prepare output content
    if include_timestamps:
        # Format with timestamps for each segment
        output_lines = []
        for segment in result["segments"]:
            timestamp = format_timestamp(segment["start"])
            text = segment["text"].strip()
            output_lines.append(f"{timestamp} {text}")
        output_content = "\n".join(output_lines)
    else:
        # Plain text output
        output_content = result["text"].strip()

    # Write to output file
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(output_content)
            f.write("\n")  # Add trailing newline
        print("\n✓ Transcription complete!")
        print(f"  Output saved to: {output_path}")
    except OSError as e:
        print(f"Error writing output file: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="Transcribe audio files locally using OpenAI Whisper.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s audio.mp3
  %(prog)s audio.mp3 --timestamps
  %(prog)s audio.mp3 --output my_transcript.txt
  %(prog)s /path/to/audio.wav --timestamps --output /path/to/output.txt

Supported audio formats:
  mp3, mp4, mpeg, mpga, m4a, wav, webm, and more (via ffmpeg)

Requirements:
  - Python package: openai-whisper (install via: pip install openai-whisper)
  - System dependency: ffmpeg (must be installed separately)
        """,
    )

    parser.add_argument(
        "audio_file", type=str, help="Path to the audio file to transcribe"
    )

    parser.add_argument(
        "--timestamps",
        action="store_true",
        help="Include timestamps in the output (format: [HH:MM:SS] text)",
    )

    parser.add_argument(
        "--output",
        "-o",
        type=str,
        default=None,
        help="Output file path (default: same directory as input with .txt extension)",
    )

    # If no arguments provided, show help instead of error
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(0)

    args = parser.parse_args()

    # Determine output path
    if args.output:
        output_path = args.output
    else:
        # Generate output filename from input filename
        input_path = Path(args.audio_file)
        output_path = input_path.with_suffix(".txt")

    # Perform transcription
    transcribe_audio(args.audio_file, output_path, args.timestamps)


if __name__ == "__main__":
    main()
