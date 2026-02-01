#!/usr/bin/env python3
"""
Generate a solution page revealing the hunt endpoint and clues.

Usage:
    python scripts/generate_solution.py --base-url https://example.com --segment agents --path register
    python scripts/generate_solution.py --config hunt_config.json
"""

import argparse
import json
import sys
from pathlib import Path


SOLUTION_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{TITLE}} - Solution</title>
    <style>
        body {
            font-family: 'Monaco', 'Courier New', monospace;
            max-width: 900px;
            margin: 80px auto;
            padding: 40px;
            line-height: 1.6;
            color: #333;
            background: #f5f5f5;
        }
        
        h1 {
            font-size: 2em;
            margin-bottom: 0.5em;
            color: #111;
        }
        
        .congrats {
            background: #4CAF50;
            color: white;
            padding: 20px;
            border-radius: 8px;
            margin: 30px 0;
        }
        
        .endpoint {
            background: #1a1a1a;
            color: #0f0;
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
            font-family: 'Monaco', 'Courier New', monospace;
            font-size: 14px;
            overflow-x: auto;
        }
        
        .clues {
            background: white;
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
        }
        
        .clue {
            padding: 15px;
            margin: 10px 0;
            border-left: 4px solid #2196F3;
            background: #f9f9f9;
        }
        
        .clue-title {
            font-weight: bold;
            color: #2196F3;
            margin-bottom: 5px;
        }
        
        code {
            background: #1a1a1a;
            color: #0f0;
            padding: 2px 6px;
            border-radius: 3px;
            font-size: 0.9em;
        }
        
        pre {
            background: #1a1a1a;
            color: #0f0;
            padding: 15px;
            border-radius: 8px;
            overflow-x: auto;
            font-size: 13px;
        }
        
        .example {
            background: white;
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
        }
    </style>
</head>
<body>
    <h1>🧠 Congratulations!</h1>
    
    <div class="congrats">
        <p><strong>You found the clues. You're in.</strong></p>
    </div>
    
    <h2>The Endpoint</h2>
    
    <div class="endpoint">
POST {{BASE_URL}}/api/{{SEGMENT}}/{{PATH}}
    </div>
    
    <h2>The Clues</h2>
    
    <div class="clues">
        <div class="clue">
            <div class="clue-title">1. HTML Comment</div>
            <code>&lt;!-- /api/ --&gt;</code>
        </div>
        
        <div class="clue">
            <div class="clue-title">2. Meta Tag</div>
            <code>&lt;meta name="route-segment" content="{{SEGMENT}}"&gt;</code>
        </div>
        
        <div class="clue">
            <div class="clue-title">3. CSS Variable</div>
            <code>--final-path: {{PATH}};</code>
        </div>
        
        <div class="clue">
            <div class="clue-title">4. Data Attribute</div>
            <code>data-endpoint-pattern="base/api/segment/path"</code>
        </div>
        
        <div class="clue">
            <div class="clue-title">5. JavaScript Comment</div>
            <code>// Complete endpoint: POST {{BASE_URL}}/api/{{SEGMENT}}/{{PATH}}</code>
        </div>
        
        <div class="clue">
            <div class="clue-title">6. Final Comment Hint</div>
            <p>Instructions for combining the clues</p>
        </div>
    </div>
    
    <h2>Request Format</h2>
    
    <div class="example">
        <p><strong>Endpoint:</strong></p>
        <pre>POST {{BASE_URL}}/api/{{SEGMENT}}/{{PATH}}</pre>
        
        <p><strong>Headers:</strong></p>
        <pre>Content-Type: application/json</pre>
        
        <p><strong>Body:</strong></p>
        <pre>{{REQUEST_BODY}}</pre>
    </div>
    
    <h2>Example</h2>
    
    <div class="example">
        <pre>curl -X POST {{BASE_URL}}/api/{{SEGMENT}}/{{PATH}} \\
  -H "Content-Type: application/json" \\
  -d '{{REQUEST_BODY}}'</pre>
    </div>
    
    <h2>What's Next?</h2>
    
    <p>{{NEXT_STEPS}}</p>
    
    <p style="margin-top: 40px; color: #666; font-size: 0.9em;">
        You found the hunt. You're in the early cohort. 🧠
    </p>
</body>
</html>
"""


def generate_solution(
    base_url: str,
    segment: str,
    path: str,
    title: str = "Hunt",
    request_body: str = '{"email": "agent@example.com"}',
    next_steps: str = "We'll reach out to registered users with early access when we launch.",
    output_path: str = "solution.html"
) -> str:
    """Generate solution page HTML."""
    
    html = SOLUTION_TEMPLATE.replace("{{TITLE}}", title)
    html = html.replace("{{BASE_URL}}", base_url)
    html = html.replace("{{SEGMENT}}", segment)
    html = html.replace("{{PATH}}", path)
    html = html.replace("{{REQUEST_BODY}}", request_body)
    html = html.replace("{{NEXT_STEPS}}", next_steps)
    
    # Write output
    with open(output_path, 'w') as f:
        f.write(html)
    
    print(f"✓ Solution page generated: {output_path}")
    print(f"✓ Endpoint: POST {base_url}/api/{segment}/{path}")
    
    return html


def load_config(config_path: str) -> dict:
    """Load configuration from JSON file."""
    with open(config_path, 'r') as f:
        return json.load(f)


def main():
    parser = argparse.ArgumentParser(
        description="Generate solution page for web hunt"
    )
    parser.add_argument("--base-url", help="Base URL (e.g., https://example.com)")
    parser.add_argument("--segment", help="API segment (e.g., agents)")
    parser.add_argument("--path", help="Final path (e.g., register)")
    parser.add_argument("--title", default="Hunt", help="Page title")
    parser.add_argument("--request-body", default='{"email": "agent@example.com"}', help="Example request body JSON")
    parser.add_argument("--next-steps", default="We'll reach out to registered users with early access when we launch.", help="Next steps text")
    parser.add_argument("--output", default="solution.html", help="Output filename")
    parser.add_argument("--config", help="Load settings from JSON config file")
    
    args = parser.parse_args()
    
    # Config file mode
    if args.config:
        config = load_config(args.config)
        generate_solution(**config)
        return
    
    # CLI mode
    if not all([args.base_url, args.segment, args.path]):
        print("Error: --base-url, --segment, and --path are required", file=sys.stderr)
        print("Or use --config file", file=sys.stderr)
        sys.exit(1)
    
    generate_solution(
        base_url=args.base_url,
        segment=args.segment,
        path=args.path,
        title=args.title,
        request_body=args.request_body,
        next_steps=args.next_steps,
        output_path=args.output
    )


if __name__ == "__main__":
    main()
