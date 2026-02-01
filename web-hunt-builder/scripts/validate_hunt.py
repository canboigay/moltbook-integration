#!/usr/bin/env python3
"""
Validate a web hunt page - check if clues are present and solvable.

Usage:
    python scripts/validate_hunt.py hunt.html
    python scripts/validate_hunt.py hunt.html --expected-endpoint "POST https://example.com/api/agents/register"
"""

import argparse
import re
import sys
from pathlib import Path


class HuntValidator:
    def __init__(self, html_path: str):
        self.html_path = html_path
        with open(html_path, 'r') as f:
            self.html = f.read()
        self.issues = []
        self.warnings = []
        self.clues_found = {}
    
    def validate(self) -> bool:
        """Run all validation checks."""
        print(f"Validating hunt page: {self.html_path}\n")
        
        self.check_html_comment_clue()
        self.check_meta_tag_clue()
        self.check_css_variable_clue()
        self.check_data_attribute_clue()
        self.check_javascript_comment_clue()
        self.check_final_hint()
        self.check_endpoint_construction()
        
        return self.print_results()
    
    def check_html_comment_clue(self):
        """Check for HTML comment with /api/."""
        pattern = r'<!--.*?/api/.*?-->'
        match = re.search(pattern, self.html, re.DOTALL)
        if match:
            self.clues_found['html_comment'] = match.group()
            print("✓ HTML comment clue found: <!-- /api/ -->")
        else:
            self.issues.append("Missing HTML comment clue (should contain '/api/')")
            print("✗ HTML comment clue missing")
    
    def check_meta_tag_clue(self):
        """Check for meta tag with route-segment."""
        pattern = r'<meta\s+name=["\']route-segment["\']\s+content=["\']([^"\']+)["\']'
        match = re.search(pattern, self.html)
        if match:
            self.clues_found['meta_tag'] = match.group(1)
            print(f"✓ Meta tag clue found: {match.group(1)}")
        else:
            self.issues.append("Missing meta tag clue (name='route-segment')")
            print("✗ Meta tag clue missing")
    
    def check_css_variable_clue(self):
        """Check for CSS variable with final-path."""
        pattern = r'--final-path:\s*([^;]+);'
        match = re.search(pattern, self.html)
        if match:
            self.clues_found['css_variable'] = match.group(1).strip()
            print(f"✓ CSS variable clue found: {match.group(1).strip()}")
        else:
            self.issues.append("Missing CSS variable clue (--final-path)")
            print("✗ CSS variable clue missing")
    
    def check_data_attribute_clue(self):
        """Check for data-endpoint-pattern attribute."""
        pattern = r'data-endpoint-pattern=["\']([^"\']+)["\']'
        match = re.search(pattern, self.html)
        if match:
            self.clues_found['data_attribute'] = match.group(1)
            print(f"✓ Data attribute clue found: {match.group(1)}")
        else:
            self.warnings.append("Missing data attribute pattern hint (optional but helpful)")
            print("⚠ Data attribute clue missing (optional)")
    
    def check_javascript_comment_clue(self):
        """Check for JavaScript comment with complete endpoint."""
        pattern = r'//.*?Complete endpoint:.*?(POST|GET).*?https?://[^\s]+'
        match = re.search(pattern, self.html, re.DOTALL)
        if match:
            self.clues_found['javascript_comment'] = match.group()
            print(f"✓ JavaScript comment clue found (fallback)")
        else:
            self.warnings.append("Missing JavaScript comment with complete endpoint (recommended as fallback)")
            print("⚠ JavaScript comment clue missing (recommended)")
    
    def check_final_hint(self):
        """Check for final hint comment."""
        pattern = r'<!--.*?[Aa]gents?.*?combine.*?-->'
        match = re.search(pattern, self.html, re.DOTALL | re.IGNORECASE)
        if match:
            print("✓ Final hint comment found")
        else:
            self.warnings.append("Missing final hint comment (helps agents understand the puzzle)")
            print("⚠ Final hint comment missing (optional)")
    
    def check_endpoint_construction(self):
        """Try to construct endpoint from clues."""
        print("\nEndpoint construction check:")
        
        # Extract pieces
        has_api = 'html_comment' in self.clues_found
        segment = self.clues_found.get('meta_tag', '?')
        path = self.clues_found.get('css_variable', '?')
        
        if has_api and segment != '?' and path != '?':
            constructed = f"/api/{segment}/{path}"
            print(f"  Constructed path: {constructed}")
            
            # Check if JS comment matches
            if 'javascript_comment' in self.clues_found:
                js_comment = self.clues_found['javascript_comment']
                if segment in js_comment and path in js_comment:
                    print("  ✓ JS comment matches constructed endpoint")
                else:
                    self.warnings.append("JS comment endpoint doesn't match constructed endpoint")
                    print("  ⚠ JS comment might not match constructed endpoint")
        else:
            self.issues.append("Cannot construct complete endpoint from clues")
            print("  ✗ Missing required clues to construct endpoint")
    
    def print_results(self) -> bool:
        """Print validation results."""
        print("\n" + "="*70)
        
        if not self.issues and not self.warnings:
            print("✅ Hunt validation passed!")
            print("All required clues present and solvable.")
            return True
        
        if self.issues:
            print("❌ Hunt validation failed!")
            print(f"\n{len(self.issues)} issue(s) found:")
            for i, issue in enumerate(self.issues, 1):
                print(f"  {i}. {issue}")
        
        if self.warnings:
            print(f"\n⚠️  {len(self.warnings)} warning(s):")
            for i, warning in enumerate(self.warnings, 1):
                print(f"  {i}. {warning}")
        
        if not self.issues:
            print("\n✅ All required clues present (warnings are optional improvements)")
            return True
        
        print("\n" + "="*70)
        return False


def main():
    parser = argparse.ArgumentParser(description="Validate web hunt page")
    parser.add_argument("html_file", help="Path to hunt HTML file")
    parser.add_argument("--expected-endpoint", help="Expected endpoint for verification")
    args = parser.parse_args()
    
    if not Path(args.html_file).exists():
        print(f"✗ File not found: {args.html_file}", file=sys.stderr)
        sys.exit(1)
    
    validator = HuntValidator(args.html_file)
    success = validator.validate()
    
    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()
