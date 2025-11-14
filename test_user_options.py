#!/usr/bin/env python3
"""
Test script for user_options.py updates.
Verifies new color scheme options and migration logic.
"""

import sys
import os
import json


def _migrate_palette_type_to_matugen_scheme(data: dict) -> dict:
    """
    Copy of migration function for testing without importing ignis.
    """
    if "material" in data and "palette_type" in data["material"]:
        old_palette = data["material"]["palette_type"]

        palette_migration_map = {
            "tonalspot": "tonal-spot",
            "fruitSalad": "fruit-salad",
            "monochrome": "monochrome",
            "rainbow": "rainbow",
            "expressive": "expressive",
            "neutral": "neutral",
            "vibrant": "vibrant",
            "fidelity": "fidelity",
            "content": "content",
        }

        new_scheme = palette_migration_map.get(old_palette, "tonal-spot")
        data["material"]["matugen_scheme_type"] = new_scheme
        del data["material"]["palette_type"]

    return data


def test_new_options_defaults():
    """Test that new options are defined with correct defaults."""
    print("Testing new color scheme options defaults...")
    print()

    # Read user_options.py and verify default values
    user_options_path = os.path.join(os.path.dirname(__file__), "ignis", "user_options.py")

    with open(user_options_path, "r") as f:
        content = f.read()

    # Check that new options are defined
    required_options = [
        'scheme_name: str = "Rose Pine"',
        'scheme_variant: str = "main"',
        'use_wallpaper_colors: bool = False',
        'matugen_scheme_type: str = "tonal-spot"',
        'dark_mode: bool = True',
        'colors: dict[str, str] = {}',
    ]

    for option in required_options:
        if option not in content:
            raise AssertionError(f"Option not found in user_options.py: {option}")
        print(f"  ✅ Found: {option}")

    print()
    print("✅ All new options are defined with correct defaults!")
    print()


def test_palette_type_migration():
    """Test migration from old palette_type to new matugen_scheme_type."""
    print("Testing palette_type migration...")
    print()

    test_cases = [
        ("tonalspot", "tonal-spot"),
        ("fruitSalad", "fruit-salad"),
        ("monochrome", "monochrome"),
        ("vibrant", "vibrant"),
        ("expressive", "expressive"),
        ("neutral", "neutral"),
        ("fidelity", "fidelity"),
        ("content", "content"),
        ("rainbow", "rainbow"),
    ]

    for old_value, expected_new_value in test_cases:
        # Create test data with old format
        data = {
            "material": {
                "palette_type": old_value,
                "dark_mode": True,
            }
        }

        # Migrate
        migrated = _migrate_palette_type_to_matugen_scheme(data)

        # Verify
        assert "palette_type" not in migrated["material"], "Old field should be removed"
        assert "matugen_scheme_type" in migrated["material"], "New field should exist"
        actual = migrated["material"]["matugen_scheme_type"]
        assert actual == expected_new_value, f"Expected '{expected_new_value}', got '{actual}'"

        print(f"  ✅ '{old_value}' -> '{expected_new_value}'")

    print()
    print("✅ All migration cases passed!")
    print()


def test_no_migration_when_not_needed():
    """Test that migration doesn't run when palette_type doesn't exist."""
    print("Testing no-op migration...")
    print()

    # Data without palette_type (new format)
    data = {
        "material": {
            "matugen_scheme_type": "tonal-spot",
            "scheme_name": "Rose Pine",
        }
    }

    original = json.dumps(data, sort_keys=True)
    migrated = _migrate_palette_type_to_matugen_scheme(data)
    after = json.dumps(migrated, sort_keys=True)

    assert original == after, "Data should not change when migration is not needed"
    print("✅ No-op migration works correctly!")
    print()


def test_options_structure():
    """Test that Material class has all required fields."""
    print("Testing Material class structure...")
    print()

    user_options_path = os.path.join(os.path.dirname(__file__), "ignis", "user_options.py")

    with open(user_options_path, "r") as f:
        content = f.read()

    required_fields = [
        "scheme_name:",
        "scheme_variant:",
        "use_wallpaper_colors:",
        "matugen_scheme_type:",
        "dark_mode:",
        "colors:",
        "interface_font:",
        "interface_font_size:",
        "document_font:",
        "document_font_size:",
        "monospace_font:",
        "monospace_font_size:",
        "theme_gtk:",
        "theme_qt:",
        "theme_kitty:",
        "theme_ghostty:",
        "theme_fuzzel:",
        "theme_hyprland:",
        "theme_niri:",
        "theme_swaylock:",
    ]

    # Check that all fields exist in the file
    for field in required_fields:
        if field not in content:
            raise AssertionError(f"Required field not found in Material class: {field}")

    print(f"✅ Material class has all {len(required_fields)} required fields!")
    print()


def main():
    """Run all tests."""
    print("=" * 60)
    print("User Options Test Suite")
    print("=" * 60)
    print()

    try:
        test_new_options_defaults()
        test_palette_type_migration()
        test_no_migration_when_not_needed()
        test_options_structure()

        print("=" * 60)
        print("✅ ALL TESTS PASSED!")
        print("=" * 60)

    except AssertionError as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
