#!/usr/bin/env python3
"""
Simple CLI tool to convert PowerPoint presentations to Markdown with speaker notes.
"""

import sys
from pathlib import Path

from docling.datamodel.base_models import InputFormat
from docling.document_converter import DocumentConverter


def convert_pptx_to_markdown(
    input_file: str, output_file: str = None, extract_notes: bool = True
):
    """
    Convert a PPTX file to Markdown format with optional notes extraction.

    Args:
        input_file: Path to the input PPTX file
        output_file: Path to the output Markdown file (optional)
        extract_notes: Whether to extract speaker notes (default: True)
    """
    input_path = Path(input_file)

    # Validate input file
    if not input_path.exists():
        print(f"Error: File '{input_file}' not found.")
        sys.exit(1)

    if input_path.suffix.lower() != ".pptx":
        print(f"Error: File must be a .pptx file, got '{input_path.suffix}'")
        sys.exit(1)

    # Set output path
    if output_file is None:
        output_path = input_path.with_suffix(".md")
    else:
        output_path = Path(output_file)

    print(f"Converting '{input_file}' to Markdown...")
    if extract_notes:
        print("  - Extracting speaker notes: enabled")

    try:
        # Configure converter
        # Note: PowerPoint notes are extracted by default in docling
        converter = DocumentConverter(allowed_formats=[InputFormat.PPTX])

        # Convert the document
        result = converter.convert(str(input_path))

        # Export to Markdown
        # Include FURNITURE layer which contains speaker notes in PowerPoint
        from docling_core.types.doc.document import ContentLayer

        if extract_notes:
            # Include both BODY (main content) and FURNITURE (notes) layers
            markdown_content = result.document.export_to_markdown(
                included_content_layers={ContentLayer.BODY, ContentLayer.FURNITURE}
            )
        else:
            # Only include BODY layer (main content)
            markdown_content = result.document.export_to_markdown(
                included_content_layers={ContentLayer.BODY}
            )

        # Write to output file
        output_path.write_text(markdown_content, encoding="utf-8")

        print(f"✓ Successfully converted to '{output_path}'")
        print(f"  - Pages converted: {len(result.document.pages)}")

    except Exception as e:
        print(f"Error during conversion: {e}")
        sys.exit(1)


def print_usage():
    """Print usage information."""
    print("""
Usage: python pptx2md.py <input.pptx> [output.md] [--no-notes]

Arguments:
  input.pptx    Path to the PowerPoint file to convert
  output.md     (Optional) Path to the output Markdown file
                If not specified, uses the same name as input with .md extension
  --no-notes    (Optional) Disable extraction of speaker notes

Examples:
  python pptx2md.py presentation.pptx
  python pptx2md.py presentation.pptx output.md
  python pptx2md.py presentation.pptx --no-notes
  python pptx2md.py presentation.pptx output.md --no-notes
""")


def main():
    """Main entry point for the CLI."""
    args = sys.argv[1:]

    # Check for help flag
    if not args or "--help" in args or "-h" in args:
        print_usage()
        sys.exit(0)

    # Parse arguments
    input_file = None
    output_file = None
    extract_notes = True

    for arg in args:
        if arg == "--no-notes":
            extract_notes = False
        elif input_file is None:
            input_file = arg
        elif output_file is None and not arg.startswith("--"):
            output_file = arg

    if input_file is None:
        print("Error: No input file specified.")
        print_usage()
        sys.exit(1)

    # Convert the file
    convert_pptx_to_markdown(input_file, output_file, extract_notes)


if __name__ == "__main__":
    main()
