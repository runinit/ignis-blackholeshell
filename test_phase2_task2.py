#!/usr/bin/env python3
"""
Test script to validate Phase 2, Task 2: Bar Settings UI
This validates the settings UI implementation without requiring GTK runtime.
"""

from pathlib import Path

def validate_appearance_settings():
    """Validate appearance.py has bar configuration UI."""
    print("Testing appearance.py Bar Configuration UI...")
    file_path = Path("ignis/modules/settings/pages/appearance.py")
    content = file_path.read_text()

    errors = []

    # Check for Bar Configuration SettingsGroup
    if 'name="Bar Configuration"' not in content:
        errors.append("Missing Bar Configuration SettingsGroup")

    # Check for required UI components
    required_components = [
        # Position selector
        ('label="Position"', "Position ComboBoxRow"),
        ('"Top", "Bottom", "Left", "Right"', "Position options"),

        # Floating mode toggle
        ('label="Floating Mode"', "Floating Mode SwitchRow"),
        ('active=user_options.bar.bind("floating")', "Floating binding"),

        # Float margin spinner
        ('label="Float Margin"', "Float Margin SpinRow"),
        ('value=user_options.bar.bind("float_margin")', "Float margin binding"),

        # Density selector
        ('label="Density"', "Density ComboBoxRow"),
        ('"Compact", "Comfortable", "Spacious"', "Density options"),

        # Corner radius selector
        ('label="Corner Radius"', "Corner Radius ComboBoxRow"),
        ('"Square", "Normal", "Inverted"', "Corner radius options"),
    ]

    for code, description in required_components:
        if code not in content:
            errors.append(f"Missing UI component: {description}")

    # Check for handler methods
    required_handlers = [
        "_get_bar_position_index",
        "_get_bar_density_index",
        "_get_bar_corner_radius_index",
        "_on_bar_position_changed",
        "_on_bar_density_changed",
        "_on_bar_corner_radius_changed",
    ]

    for handler in required_handlers:
        if handler not in content:
            errors.append(f"Missing handler method: {handler}")

    # Check for position mapping
    if 'positions = ["top", "bottom", "left", "right"]' not in content:
        errors.append("Missing position mapping array")

    # Check for density mapping
    if 'densities = ["compact", "comfortable", "spacious"]' not in content:
        errors.append("Missing density mapping array")

    # Check for corner radius mapping
    if "radius_map = {0: -1, 1: 0, 2: 1}" not in content:
        errors.append("Missing corner radius mapping")

    # Check for user_options.save_to_file calls
    save_calls = content.count("user_options.save_to_file(user_options._file)")
    if save_calls < 3:
        errors.append(f"Expected at least 3 save_to_file calls, found {save_calls}")

    # Check for sublabels (good UX practice)
    sublabels = [
        "Screen edge for bar placement",
        "Add margins around the bar",
        "Margin in pixels when floating",
        "Bar height and padding",
        "Bar corner style",
    ]

    for sublabel in sublabels:
        if sublabel not in content:
            errors.append(f"Missing sublabel: {sublabel}")

    if errors:
        print(f"❌ appearance.py validation failed:")
        for error in errors:
            print(f"   - {error}")
        return False

    print("✅ appearance.py: All bar settings UI components present")
    return True


def validate_ui_structure():
    """Validate overall UI structure and best practices."""
    print("\nTesting UI structure and best practices...")
    file_path = Path("ignis/modules/settings/pages/appearance.py")
    content = file_path.read_text()

    errors = []
    warnings = []

    # Check imports
    required_imports = [
        "ComboBoxRow",
        "SpinRow",
        "SwitchRow",
        "user_options",
    ]

    for imp in required_imports:
        if imp not in content:
            errors.append(f"Missing import: {imp}")

    # Check for proper binding usage
    if "user_options.bar.bind(" not in content:
        errors.append("Missing reactive bindings for bar options")

    # Check for SpinRow constraints
    if "min=0" not in content or "max=32" not in content:
        warnings.append("Float margin SpinRow may be missing constraints")

    # Check for proper error handling in getter methods
    if "except ValueError:" not in content:
        warnings.append("Getter methods may lack error handling")

    # Check for Phase 2 comment
    if "# Bar Configuration (Phase 2)" not in content:
        warnings.append("Missing phase comment for Bar Configuration section")

    if errors:
        print(f"❌ UI structure validation failed:")
        for error in errors:
            print(f"   - {error}")
        return False

    if warnings:
        print(f"⚠️  UI structure warnings:")
        for warning in warnings:
            print(f"   - {warning}")

    print("✅ UI structure: All checks passed")
    return True


def validate_integration():
    """Validate integration with existing code."""
    print("\nTesting integration with existing code...")

    errors = []

    # Check that appearance.py still has other settings groups
    file_path = Path("ignis/modules/settings/pages/appearance.py")
    content = file_path.read_text()

    existing_groups = [
        'name="Theme"',
        'name="Wallpaper Slideshow"',
        'name="Bar Configuration"',
    ]

    for group in existing_groups:
        if group not in content:
            errors.append(f"Missing settings group: {group}")

    # Verify the Bar Configuration is properly positioned
    theme_pos = content.find('name="Theme"')
    slideshow_pos = content.find('name="Wallpaper Slideshow"')
    bar_pos = content.find('name="Bar Configuration"')

    if theme_pos == -1 or slideshow_pos == -1 or bar_pos == -1:
        errors.append("Cannot verify settings group order")
    elif not (theme_pos < slideshow_pos < bar_pos):
        errors.append("Bar Configuration group not in correct position (should be after Wallpaper Slideshow)")

    if errors:
        print(f"❌ Integration validation failed:")
        for error in errors:
            print(f"   - {error}")
        return False

    print("✅ Integration: Bar Configuration properly integrated")
    return True


def main():
    """Run all validations."""
    print("=" * 60)
    print("Phase 2, Task 2: Bar Settings UI")
    print("Validation Test")
    print("=" * 60)

    results = []
    results.append(validate_appearance_settings())
    results.append(validate_ui_structure())
    results.append(validate_integration())

    print("\n" + "=" * 60)
    print(f"Results: {sum(results)}/3 tests passed")

    if all(results):
        print("✅ Task 2 validation passed!")
        print("\nImplemented features:")
        print("  ✅ Bar Configuration settings group")
        print("  ✅ Position selector (Top/Bottom/Left/Right)")
        print("  ✅ Floating Mode toggle with binding")
        print("  ✅ Float Margin spinner (0-32px)")
        print("  ✅ Density selector (Compact/Comfortable/Spacious)")
        print("  ✅ Corner Radius selector (Square/Normal/Inverted)")
        print("  ✅ 6 handler methods for settings changes")
        print("  ✅ Proper index mapping for dropdowns")
        print("  ✅ user_options.save_to_file() persistence")
        print("  ✅ Descriptive sublabels for all controls")
        print("  ✅ Integration with existing settings groups")
        return 0
    else:
        print("❌ Task 2 validation failed")
        return 1


if __name__ == "__main__":
    exit(main())
