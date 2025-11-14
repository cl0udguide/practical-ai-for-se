#!/usr/bin/env python3
"""
Simple web page to Markdown converter using Playwright + docling.
Free, open-source solution that handles JavaScript rendering and outputs clean Markdown.
No API keys required!
"""

import argparse
import sys
import tempfile
from pathlib import Path


def print_usage():
    """Print usage information."""
    print("""
Usage: python www2md.py <url> [options]

Arguments:
  url                    URL to download and convert to Markdown

Options:
  -o, --output OUTPUT    (Optional) Path to the output Markdown file
                         If not specified, auto-generates filename from URL

  --wait-time WAIT_TIME  (Optional) Wait time in milliseconds for page to load
                         Default: 5000ms

  --headless             (Optional) Run browser in headless mode (hidden)
                         By default, browser window is visible (for reCAPTCHA)

  --browser ENGINE       (Optional) Browser engine to use
                         Choices: chromium, firefox, webkit
                         Default: chromium

Features:
  - Handles JavaScript-rendered pages automatically
  - Automatically detects and waits for reCAPTCHA completion
  - Browser window visible by default (complete reCAPTCHA manually)
  - Converts full page HTML to clean Markdown using docling

Examples:
  python www2md.py "https://example.com"
  python www2md.py "https://example.com" -o output.md
  python www2md.py "https://example.com" --headless -o output.md
  python www2md.py "https://example.com" --browser firefox -o output.md
  python www2md.py "https://example.com" --wait-time 10000 -o output.md

For reCAPTCHA-protected sites:
  python www2md.py "https://protected-site.com" -o output.md
  (Browser window will open - complete reCAPTCHA manually when prompted)

Requirements:
  - playwright library (install with: pip install playwright)
  - docling library (install with: pip install docling)
  - Browser engine (run: playwright install chromium)
""")


def main():
    args = sys.argv[1:]
    
    # Check for help flag
    if not args or "--help" in args or "-h" in args:
        print_usage()
        sys.exit(0)
    
    parser = argparse.ArgumentParser(
        description="Download web page with JavaScript rendering and convert to Markdown (free, no API key)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python www2md.py "https://example.com"
  python www2md.py "https://example.com" -o output.md
  python www2md.py "https://example.com" --headless -o output.md

For reCAPTCHA-protected sites, the browser window opens by default.
Complete the reCAPTCHA manually when prompted.
"""
    )
    parser.add_argument("url", help="URL to download and convert")
    parser.add_argument(
        "-o", "--output", help="Output markdown file (default: auto-generated)"
    )
    parser.add_argument(
        "--wait-time",
        type=int,
        default=5000,
        help="Wait time in milliseconds for page to load (default: 5000)",
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run browser in headless mode (hidden, use this to hide browser window)",
    )
    parser.add_argument(
        "--browser",
        choices=["chromium", "firefox", "webkit"],
        default="chromium",
        help="Browser engine to use (default: chromium)",
    )
    
    args = parser.parse_args()
    
    # Check dependencies
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("Error: playwright is not installed. Install it with:", file=sys.stderr)
        print("  pip install playwright", file=sys.stderr)
        print("  playwright install chromium", file=sys.stderr)
        sys.exit(1)
    
    try:
        from docling.document_converter import DocumentConverter
    except ImportError:
        print("Error: docling is not installed. Install it with:", file=sys.stderr)
        print("  pip install docling", file=sys.stderr)
        sys.exit(1)
    
    url = args.url
    
    print(f"Downloading: {url}")
    
    try:
        with sync_playwright() as p:
            # Launch browser
            browser_engine = getattr(p, args.browser)
            browser = browser_engine.launch(headless=args.headless)
            
            # Create context with realistic settings
            # Using Firefox user agent - commonly recommended by modern web apps like Nytro.ai
            # Firefox is often better accepted than Chrome-based browsers for automation
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:133.0) Gecko/20100101 Firefox/133.0",
                viewport={"width": 1920, "height": 1080},
            )
            
            page = context.new_page()
            
            # Navigate to page
            print(f"Loading page...")
            page.goto(url, wait_until="networkidle", timeout=60000)
            
            # Check if we got blocked by reCAPTCHA
            page_text = page.inner_text("body")
            is_blocked = "Checking your browser" in page_text or "reCAPTCHA" in page_text or "captcha" in page_text.lower()
            
            if is_blocked:
                if not args.headless:
                    # In visible mode, wait for user to complete reCAPTCHA
                    print("\n" + "="*60)
                    print("RECAPTCHA DETECTED - Please complete it in the browser window")
                    print("="*60)
                    print(f"Waiting up to 5 minutes for reCAPTCHA completion...")
                    print("The script will automatically detect when you're done!")
                    print("="*60 + "\n")
                    
                    # Wait for reCAPTCHA to be completed
                    # Check every 2 seconds for up to 5 minutes (300 seconds)
                    max_wait_seconds = 300
                    check_interval = 2000  # 2 seconds in milliseconds
                    waited_seconds = 0
                    
                    while waited_seconds < max_wait_seconds:
                        page.wait_for_timeout(check_interval)
                        waited_seconds += (check_interval / 1000)
                        
                        # Check if reCAPTCHA is still present
                        current_text = page.inner_text("body")
                        current_url = page.url
                        
                        # Check if we're past the reCAPTCHA page
                        if "Checking your browser" not in current_text:
                            # Check if content has loaded (not just reCAPTCHA page)
                            if len(current_text) > 200:  # Meaningful content loaded
                                print(f"\n[OK] ReCAPTCHA completed! Content loaded after {int(waited_seconds)}s")
                                
                                # Wait a bit more for full page load
                                print("Waiting for page to fully render...")
                                page.wait_for_timeout(3000)
                                
                                # Check URL - if it redirected, we might need to navigate to original
                                if current_url != url and "infohub" in current_url:
                                    print("Navigating to final page...")
                                    page.goto(current_url, wait_until="networkidle", timeout=30000)
                                    page.wait_for_timeout(2000)
                                
                                break
                        
                        # Show progress every 10 seconds
                        if int(waited_seconds) % 10 == 0 and waited_seconds > 0:
                            print(f"Still waiting... ({int(waited_seconds)}s / {max_wait_seconds}s)")
                    
                    if waited_seconds >= max_wait_seconds:
                        print(f"\nWARNING: Timeout reached ({max_wait_seconds}s). Using whatever content is available.", file=sys.stderr)
                else:
                    # In headless mode, just warn
                    print("\nWARNING: Page appears to be blocked by reCAPTCHA!", file=sys.stderr)
                    print("Browser is running in headless mode. Remove --headless flag to see the browser window and complete reCAPTCHA manually.", file=sys.stderr)
                    print(f"  python www2md.py \"{url}\" -o output.md", file=sys.stderr)
            else:
                # No reCAPTCHA detected, just wait normally
                print(f"Waiting {args.wait_time}ms for JavaScript to render...")
                page.wait_for_timeout(args.wait_time)
            
            # Get rendered HTML
            print("Extracting rendered HTML...")
            html_content = page.content()
            
            browser.close()
        
        # Save HTML to temporary file
        print("Saving HTML to temporary file...")
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as tmp_file:
            tmp_file.write(html_content)
            tmp_html_path = tmp_file.name
        
        try:
            # Convert HTML to Markdown using docling
            print("Converting HTML to Markdown using docling...")
            converter = DocumentConverter()
            
            result = converter.convert(tmp_html_path)
            
            if not result or not result.document:
                print("Error: Could not convert HTML to Markdown.", file=sys.stderr)
                sys.exit(1)
            
            # Get markdown from docling result
            markdown = result.document.export_to_markdown()
            
            if not markdown:
                print("Error: Could not extract markdown from converted document.", file=sys.stderr)
                sys.exit(1)
        
        finally:
            # Clean up temporary HTML file
            try:
                Path(tmp_html_path).unlink()
            except Exception:
                pass
        
        # Determine output path
        if args.output:
            output_path = Path(args.output)
        else:
            from urllib.parse import urlparse
            parsed = urlparse(url)
            base_name = parsed.path.strip('/').split('/')[-1] or 'index'
            base_name = base_name.replace('/', '_').replace(':', '_')[:50]
            if not base_name:
                base_name = 'page'
            output_path = Path(f"{base_name}.md")
        
        # Save markdown
        output_path.write_text(markdown, encoding='utf-8')
        
        print(f"Successfully saved to: {output_path}")
        print(f"  Output size: {output_path.stat().st_size / 1024:.1f} KB")
        print(f"  Lines: {len(markdown.splitlines())}")
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

