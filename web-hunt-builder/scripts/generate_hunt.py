#!/usr/bin/env python3
"""
Generate a web hunt page with hidden API endpoint clues.

Usage:
    python scripts/generate_hunt.py --base-url https://example.com --segment agents --path register
    python scripts/generate_hunt.py --config hunt_config.json
    python scripts/generate_hunt.py --interactive
"""

import argparse
import json
import sys
import re
from pathlib import Path


def load_template(template_path: str = None) -> str:
    """Load the HTML template."""
    if not template_path:
        # Default to bundled template
        skill_dir = Path(__file__).parent.parent
        template_path = skill_dir / "assets" / "hunt-template.html"
    
    with open(template_path, 'r') as f:
        return f.read()


def generate_hunt(
    base_url: str,
    segment: str,
    path: str,
    title: str = "Coming Soon",
    heading: str = "Something is being built",
    subtitle: str = "For those who look deeper",
    description: str = "We're working on something new. Stay tuned.",
    cta_heading: str = "Get Early Access",
    cta_text: str = "Join the waitlist for early access.",
    cta_button: str = "Notify Me",
    difficulty: str = "medium",
    template_path: str = None,
    output_path: str = "hunt.html"
) -> str:
    """Generate hunt page HTML."""
    
    template = load_template(template_path)
    
    # Adjust based on difficulty
    if difficulty == "easy":
        # Add hint in page title
        title = f"{title} <!-- Hint: Check the source code -->"
        # Make JS comment more obvious
        template = template.replace(
            "// Complete endpoint:",
            "// AGENTS: Complete endpoint is:"
        )
    elif difficulty == "hard":
        # Remove JS comment fallback
        template = re.sub(
            r'// Complete endpoint:.*?\n',
            '// Endpoint hidden in source\n',
            template,
            flags=re.DOTALL
        )
        # Encode CSS variable in base64
        import base64
        path_encoded = base64.b64encode(path.encode()).decode()
        template = template.replace(
            "{{PATH}}",
            f"<!-- base64: {path_encoded} -->"
        )
    
    # Replace placeholders
    html = template.replace("{{TITLE}}", title)
    html = html.replace("{{BASE_URL}}", base_url)
    html = html.replace("{{SEGMENT}}", segment)
    if difficulty != "hard":  # Only replace if not encoded
        html = html.replace("{{PATH}}", path)
    html = html.replace("{{HEADING}}", heading)
    html = html.replace("{{SUBTITLE}}", subtitle)
    html = html.replace("{{DESCRIPTION}}", description)
    html = html.replace("{{CTA_HEADING}}", cta_heading)
    html = html.replace("{{CTA_TEXT}}", cta_text)
    html = html.replace("{{CTA_BUTTON}}", cta_button)
    
    # Write output
    with open(output_path, 'w') as f:
        f.write(html)
    
    print(f"✓ Hunt page generated: {output_path}")
    print(f"✓ Hidden endpoint: POST {base_url}/api/{segment}/{path}")
    print(f"✓ Difficulty: {difficulty}")
    print(f"\nClue locations:")
    print(f"  1. HTML comment: /api/")
    print(f"  2. Meta tag: {segment}")
    if difficulty == "hard":
        print(f"  3. CSS variable: {path} (base64 encoded)")
    else:
        print(f"  3. CSS variable: {path}")
    print(f"  4. Data attribute: pattern structure")
    if difficulty == "easy":
        print(f"  5. JavaScript comment: complete endpoint (OBVIOUS)")
    elif difficulty == "medium":
        print(f"  5. JavaScript comment: complete endpoint")
    else:
        print(f"  5. JavaScript comment: obfuscated")
    print(f"  6. Final comment: hint about combining clues")
    
    return html


def interactive_mode():
    """Interactive hunt page builder."""
    print("=== Web Hunt Builder (Interactive Mode) ===\n")
    
    # Required fields
    base_url = input("Base URL (e.g., https://example.com): ").strip()
    segment = input("API segment (e.g., agents): ").strip()
    path = input("Final path (e.g., register): ").strip()
    
    # Optional fields
    print("\nOptional fields (press Enter to use defaults):")
    title = input("Page title [Coming Soon]: ").strip() or "Coming Soon"
    heading = input("Main heading [Something is being built]: ").strip() or "Something is being built"
    subtitle = input("Subtitle [For those who look deeper]: ").strip() or "For those who look deeper"
    
    output_path = input("Output filename [hunt.html]: ").strip() or "hunt.html"
    
    # Generate
    print("\n" + "="*50)
    generate_hunt(
        base_url=base_url,
        segment=segment,
        path=path,
        title=title,
        heading=heading,
        subtitle=subtitle,
        output_path=output_path
    )


def load_config(config_path: str) -> dict:
    """Load configuration from JSON file."""
    with open(config_path, 'r') as f:
        return json.load(f)


def main():
    parser = argparse.ArgumentParser(
        description="Generate web hunt pages with hidden API endpoint clues"
    )
    parser.add_argument("--base-url", help="Base URL (e.g., https://example.com)")
    parser.add_argument("--segment", help="API segment (e.g., agents)")
    parser.add_argument("--path", help="Final path (e.g., register)")
    parser.add_argument("--title", default="Coming Soon", help="Page title")
    parser.add_argument("--heading", default="Something is being built", help="Main heading")
    parser.add_argument("--subtitle", default="For those who look deeper", help="Subtitle")
    parser.add_argument("--description", default="We're working on something new. Stay tuned.", help="Description")
    parser.add_argument("--cta-heading", default="Get Early Access", help="CTA heading")
    parser.add_argument("--cta-text", default="Join the waitlist for early access.", help="CTA text")
    parser.add_argument("--cta-button", default="Notify Me", help="CTA button text")
    parser.add_argument("--difficulty", default="medium", choices=["easy", "medium", "hard"],
                       help="Hunt difficulty (default: medium)")
    parser.add_argument("--template", help="Custom template file (optional)")
    parser.add_argument("--output", default="hunt.html", help="Output filename")
    parser.add_argument("--config", help="Load settings from JSON config file")
    parser.add_argument("--interactive", "-i", action="store_true", help="Interactive mode")
    
    args = parser.parse_args()
    
    # Interactive mode
    if args.interactive:
        interactive_mode()
        return
    
    # Config file mode
    if args.config:
        config = load_config(args.config)
        generate_hunt(**config)
        return
    
    # CLI mode (requires base-url, segment, path)
    if not all([args.base_url, args.segment, args.path]):
        print("Error: --base-url, --segment, and --path are required", file=sys.stderr)
        print("Or use --interactive mode or --config file", file=sys.stderr)
        sys.exit(1)
    
    generate_hunt(
        base_url=args.base_url,
        segment=args.segment,
        path=args.path,
        title=args.title,
        heading=args.heading,
        subtitle=args.subtitle,
        description=args.description,
        cta_heading=args.cta_heading,
        cta_text=args.cta_text,
        cta_button=args.cta_button,
        difficulty=args.difficulty,
        template_path=args.template,
        output_path=args.output
    )


if __name__ == "__main__":
    main()
