#!/usr/bin/env python3
"""
Test script to validate Settings UI integration for Color Scheme.
This validates that material.py has the correct structure without requiring GTK.
"""

import re
from pathlib import Path

SETTINGS_FILE = Path("ignis/modules/settings/pages/material.py")

def validate_settings_ui() -> tuple[bool, list[str]]:
    """Validate the settings UI has Color Scheme section."""
    errors = []
    content = SETTINGS_FILE.read_text()

    # Check for ColorSchemeService import
    if "from services.material import" not in content:
        errors.append("Missing services.material import")
        return False, errors

    # Check for ColorSchemeService usage
    if "ColorSchemeService" not in content:
        errors.append("ColorSchemeService not imported or used")

    # Check for SettingsGroup with "Color Scheme"
    if 'name="Color Scheme"' not in content:
        errors.append("Missing Color Scheme SettingsGroup")

    # Check for required UI components
    required_components = [
        "Built-in Color Scheme",
        "Use Wallpaper Colors",
        "Matugen Scheme Type",
    ]

    for component in required_components:
        if component not in content:
            errors.append(f"Missing UI component: {component}")

    # Check for handler methods
    required_methods = [
        "_get_scheme_index",
        "_on_scheme_changed",
        "_on_wallpaper_toggle",
    ]

    for method in required_methods:
        if method not in content:
            errors.append(f"Missing handler method: {method}")

    # Check for matugen scheme type handler (can be inline lambda or method)
    if "set_matugen_scheme_type" not in content:
        errors.append("Missing matugen_scheme_type handler")

    # Check for color_scheme_service instantiation
    if "color_scheme_service = ColorSchemeService.get_default()" not in content:
        errors.append("ColorSchemeService not properly instantiated")

    # Check for available_schemes usage
    if "available_schemes" not in content:
        errors.append("available_schemes property not used")

    return len(errors) == 0, errors

def main():
    """Test Settings UI integration."""
    print("Testing Settings UI Color Scheme integration...")
    print("=" * 60)

    if not SETTINGS_FILE.exists():
        print(f"❌ {SETTINGS_FILE}: FILE NOT FOUND")
        return 1

    passed, errors = validate_settings_ui()

    if passed:
        print("✅ Settings UI Color Scheme section is properly integrated")
        print("\nComponents found:")
        print("  - ColorSchemeService import and instantiation")
        print("  - Color Scheme SettingsGroup")
        print("  - Built-in Color Scheme dropdown")
        print("  - Use Wallpaper Colors toggle")
        print("  - Matugen Scheme Type selector")
        print("  - Handler methods for scheme changes")
        print("=" * 60)
        print("\n✅ Settings UI validation passed!")
        return 0
    else:
        print("❌ Settings UI has issues:")
        for error in errors:
            print(f"   - {error}")
        print("=" * 60)
        print("\n❌ Settings UI validation failed")
        return 1

if __name__ == "__main__":
    exit(main())
