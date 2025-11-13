#!/usr/bin/env python3
"""
Test script for color scheme loading.
Verifies that Rose Pine palettes are valid JSON.
"""

import sys
import os
import json

# Test palette files directly without loading the full service
palettes_dir = os.path.join(os.path.dirname(__file__), "ignis", "services", "material", "palettes")

def test_palette_files():
    """Test palette JSON files."""
    print("Testing Rose Pine palette files...")
    print()

    # Required Material Design 3 color keys
    required_keys = [
        "primary",
        "on_primary",
        "secondary",
        "on_secondary",
        "tertiary",
        "on_tertiary",
        "error",
        "on_error",
        "background",
        "on_background",
        "surface",
        "on_surface",
        "surface_variant",
        "on_surface_variant",
        "outline",
    ]

    palette_files = [
        "rose_pine_main.json",
        "rose_pine_moon.json",
        "rose_pine_dawn.json",
    ]

    for filename in palette_files:
        filepath = os.path.join(palettes_dir, filename)
        print(f"Testing {filename}...")

        # Test 1: File exists
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Palette file not found: {filepath}")
        print(f"  ✅ File exists")

        # Test 2: Valid JSON
        try:
            with open(filepath, "r") as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in {filename}: {e}")
        print(f"  ✅ Valid JSON")

        # Test 3: Has required metadata
        for key in ["name", "variant", "dark_mode", "colors"]:
            if key not in data:
                raise ValueError(f"Missing required key '{key}' in {filename}")
        print(f"  ✅ Has required metadata")

        # Test 4: Colors section exists and has required keys
        colors = data["colors"]
        missing_keys = [key for key in required_keys if key not in colors]
        if missing_keys:
            raise ValueError(f"Missing color keys in {filename}: {missing_keys}")
        print(f"  ✅ Has all {len(required_keys)} required M3 color keys")

        # Test 5: All color values are valid hex codes
        for color_name, color_value in colors.items():
            if not color_value.startswith("#") or len(color_value) != 7:
                raise ValueError(
                    f"Invalid color value for '{color_name}' in {filename}: {color_value}"
                )
        print(f"  ✅ All {len(colors)} colors are valid hex codes")

        # Print sample colors
        print(f"\n  Sample colors:")
        print(f"    primary: {colors['primary']}")
        print(f"    background: {colors['background']}")
        print(f"    surface: {colors['surface']}")
        print()

    print("✅ All palette files are valid!")
    print()
    print("Summary:")
    print(f"  - {len(palette_files)} palette files tested")
    print(f"  - {len(required_keys)} M3 color keys verified per palette")
    print(f"  - All palettes use valid hex color format")


if __name__ == "__main__":
    try:
        test_palette_files()
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
