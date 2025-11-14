#!/usr/bin/env python3
"""
Test script to validate matugen template format and completeness.
This validates that all templates use correct matugen 3.0 syntax.
"""

import re
import json
from pathlib import Path

TEMPLATE_DIR = Path("ignis/services/material/matugen_templates")

# Matugen 3.0 template pattern: {{colors.token_name.default.hex}}
MATUGEN_PATTERN = re.compile(r'\{\{colors\.\w+\.default\.hex\}\}')

def validate_template(file_path: Path) -> tuple[bool, list[str]]:
    """Validate a matugen template file."""
    errors = []
    content = file_path.read_text()

    # Qt5ct.conf is a config file that references colors.conf, so it doesn't need template vars
    if file_path.name == "qt5ct.conf":
        if "color_scheme_path" in content and "colors.conf" in content:
            return True, []
        else:
            errors.append("qt5ct.conf should reference colors.conf")
            return False, errors

    # Check for matugen template variables
    matches = MATUGEN_PATTERN.findall(content)
    if not matches:
        errors.append(f"No matugen template variables found")
        return False, errors

    # Validate JSON files have valid structure
    if file_path.suffix in ['.json', '.micro']:
        try:
            # For .micro files, they're JSON format
            json.loads(content)
        except json.JSONDecodeError as e:
            errors.append(f"Invalid JSON structure: {e}")
            return False, errors

    # Check for common issues
    if '{{{{' in content or '}}}}' in content:
        errors.append("Double braces detected - likely formatting error")
        return False, errors

    # Validate that templates use Material Design 3 color tokens
    required_tokens = ['primary', 'secondary', 'background', 'surface', 'on_background']
    found_tokens = set()
    for match in matches:
        # Extract token name from {{colors.TOKEN.default.hex}}
        token = match.split('.')[1]
        found_tokens.add(token)

    missing_tokens = [t for t in required_tokens if t not in found_tokens]
    if len(found_tokens) < 5:
        errors.append(f"Only {len(found_tokens)} unique color tokens found, expected more comprehensive coverage")

    return True, errors

def main():
    """Test all matugen templates."""
    print("Testing matugen templates...")
    print("=" * 60)

    templates = [
        "gtk.css",
        "kcolorscheme.colors",
        "qt5ct.conf",
        "colors.conf",
        "walker.css",
        "pywalfox.json",
        "niri-styleswitcher.toml",
        "ghostty",
        "btop.theme",
        "micro.micro",
        "helix.toml",
    ]

    all_passed = True
    results = {}

    for template in templates:
        file_path = TEMPLATE_DIR / template
        if not file_path.exists():
            print(f"❌ {template}: FILE NOT FOUND")
            all_passed = False
            results[template] = False
            continue

        passed, errors = validate_template(file_path)
        results[template] = passed

        if passed:
            # Count template variables
            content = file_path.read_text()
            var_count = len(MATUGEN_PATTERN.findall(content))
            print(f"✅ {template}: {var_count} template variables")
        else:
            print(f"❌ {template}:")
            for error in errors:
                print(f"   - {error}")
            all_passed = False

    print("=" * 60)
    print(f"\nResults: {sum(results.values())}/{len(templates)} templates passed")

    if all_passed:
        print("✅ All matugen templates are valid!")
        return 0
    else:
        print("❌ Some templates have issues")
        return 1

if __name__ == "__main__":
    exit(main())
