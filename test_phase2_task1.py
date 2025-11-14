#!/usr/bin/env python3
"""
Test script to validate Phase 2, Task 1: Bar Adaptive Positioning System
This validates code structure without requiring GTK runtime.
"""

import re
from pathlib import Path

def validate_user_options():
    """Validate user_options.py has bar position options."""
    print("Testing user_options.py...")
    file_path = Path("ignis/user_options.py")
    content = file_path.read_text()

    errors = []
    required_options = [
        "position: str = \"top\"",
        "floating: bool = False",
        "float_margin: int = 8",
        "density: str = \"comfortable\"",
        "corner_radius: int = 0",
    ]

    for option in required_options:
        if option not in content:
            errors.append(f"Missing option: {option}")

    # Check for Dock class
    if "class Dock(OptionsGroup):" not in content:
        errors.append("Missing Dock class")

    dock_options = [
        "enabled: bool = True",
        "position: str = \"bottom\"",
        "size: float = 1.0",
        "auto_hide: bool = True",
        "pinned_apps: list[str]",
    ]

    for option in dock_options:
        if option not in content:
            errors.append(f"Missing dock option: {option}")

    # Check dock instantiation
    if "dock = Dock()" not in content:
        errors.append("Dock not instantiated")

    if errors:
        print(f"❌ user_options.py validation failed:")
        for error in errors:
            print(f"   - {error}")
        return False

    print("✅ user_options.py: All bar and dock options present")
    return True


def validate_bar_py():
    """Validate bar.py has adaptive positioning logic."""
    print("\nTesting bar.py...")
    file_path = Path("ignis/modules/bar/bar.py")
    content = file_path.read_text()

    errors = []

    # Check imports
    if "from user_options import user_options" not in content:
        errors.append("Missing user_options import")

    # Check position logic
    required_code = [
        "position = user_options.bar.position",
        "floating = user_options.bar.floating",
        "density = user_options.bar.density",
        "corner_radius = user_options.bar.corner_radius",
        "def _get_anchor_for_position",
        "def _create_layout",
        "vertical = position in [\"left\", \"right\"]",
    ]

    for code in required_code:
        if code not in content:
            errors.append(f"Missing code: {code}")

    # Check anchor logic for all positions
    positions = ["top", "bottom", "left", "right"]
    for pos in positions:
        if f'pos == "{pos}"' not in content:
            errors.append(f"Missing anchor logic for position: {pos}")

    # Check CSS classes
    if 'css_classes = ["bar"' not in content:
        errors.append("Missing CSS class construction")

    if "f\"position-{position}\"" not in content:
        errors.append("Missing position CSS class")

    # Check margins
    margin_checks = [
        "margin_top=margin if position == \"top\" else 0",
        "margin_bottom=margin if position == \"bottom\" else 0",
        "margin_left=margin if position == \"left\" else 0",
        "margin_right=margin if position == \"right\" else 0",
    ]

    for check in margin_checks:
        if check not in content:
            errors.append(f"Missing margin logic: {check}")

    if errors:
        print(f"❌ bar.py validation failed:")
        for error in errors:
            print(f"   - {error}")
        return False

    print("✅ bar.py: All adaptive positioning logic present")
    return True


def validate_bar_scss():
    """Validate bar.scss has position-specific styling."""
    print("\nTesting bar.scss...")
    file_path = Path("ignis/scss/bar.scss")
    content = file_path.read_text()

    errors = []

    # Check position classes
    required_classes = [
        ".bar {",
        "&.position-top {",
        "&.position-bottom {",
        "&.position-left {",
        "&.position-right {",
        "&.floating {",
        "&.square {",
    ]

    for css_class in required_classes:
        if css_class not in content:
            errors.append(f"Missing CSS class: {css_class}")

    # Check density variants
    density_classes = [
        "&.density-compact {",
        "&.density-comfortable {",
        "&.density-spacious {",
    ]

    for css_class in density_classes:
        if css_class not in content:
            errors.append(f"Missing density class: {css_class}")

    # Check Blackhole design tokens usage
    tokens = [
        "$surface-container",
        "$radius-m",
        "$radius-l",
        "$shadow-elevation-2",
        "$animation-normal",
        "$spacing-xxs",
        "$spacing-xs",
        "$spacing-s",
        "$spacing-m",
        "$spacing-l",
    ]

    for token in tokens:
        if token not in content:
            errors.append(f"Missing design token: {token}")

    # Check backdrop filter for floating
    if "backdrop-filter: blur(10px);" not in content:
        errors.append("Missing backdrop-filter for floating mode")

    if errors:
        print(f"❌ bar.scss validation failed:")
        for error in errors:
            print(f"   - {error}")
        return False

    print("✅ bar.scss: All position-specific styling present")
    return True


def main():
    """Run all validations."""
    print("=" * 60)
    print("Phase 2, Task 1: Bar Adaptive Positioning System")
    print("Validation Test")
    print("=" * 60)

    results = []
    results.append(validate_user_options())
    results.append(validate_bar_py())
    results.append(validate_bar_scss())

    print("\n" + "=" * 60)
    print(f"Results: {sum(results)}/3 tests passed")

    if all(results):
        print("✅ Task 1 validation passed!")
        print("\nImplemented features:")
        print("  ✅ Bar position options (top/bottom/left/right)")
        print("  ✅ Floating mode with configurable margins")
        print("  ✅ Density variants (compact/comfortable/spacious)")
        print("  ✅ Corner radius options (square/normal/inverted)")
        print("  ✅ Adaptive positioning logic in bar.py")
        print("  ✅ Vertical layout support for left/right")
        print("  ✅ Position-specific SCSS styling")
        print("  ✅ Blackhole design tokens integration")
        print("  ✅ Dock options structure (for future tasks)")
        return 0
    else:
        print("❌ Task 1 validation failed")
        return 1


if __name__ == "__main__":
    exit(main())
