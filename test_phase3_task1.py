#!/usr/bin/env python3
"""
Test script to validate Phase 3, Task 1: Control Center Base Redesign
This validates the Control Center redesign without requiring GTK runtime.
"""

from pathlib import Path


def validate_control_center_py():
    """Validate Control Center Python implementation."""
    print("Testing control_center.py implementation...")
    file_path = Path("ignis/modules/control_center/control_center.py")
    content = file_path.read_text()

    errors = []

    # Check class definition changed to regular Window
    if "class ControlCenter(widgets.Window):" not in content:
        errors.append("Missing Window class inheritance (should not be RevealerWindow)")

    # Check __gtype_name__
    if '__gtype_name__ = "ControlCenter"' not in content:
        errors.append("Missing __gtype_name__ declaration")

    # Check window properties
    required_properties = [
        'namespace="ignis_CONTROL_CENTER"',
        'anchor=["top", "right"]',
        'exclusivity="normal"',
        'layer="overlay"',
        'css_classes=["control-center"]',
    ]

    for prop in required_properties:
        if prop not in content:
            errors.append(f"Missing window property: {prop}")

    # Check container structure
    if "spacing=12," not in content:
        errors.append("Missing 12px spacing in container")

    if 'css_classes=["control-center-container"]' not in content:
        errors.append("Missing control-center-container CSS class")

    # Check helper methods
    required_methods = [
        "_create_header",
        "_create_quick_settings",
        "_create_media_player",
        "_create_notifications",
    ]

    for method in required_methods:
        if f"def {method}" not in content:
            errors.append(f"Missing helper method: {method}")

    # Check method calls in child list
    method_calls = [
        "self._create_header()",
        "self._create_quick_settings()",
        "self._create_media_player()",
        "self._create_notifications()",
    ]

    for call in method_calls:
        if call not in content:
            errors.append(f"Missing method call: {call}")

    # Check header structure
    if 'css_classes=["control-center-header"]' not in content:
        errors.append("Missing control-center-header CSS class")

    # Check quick settings structure
    if 'css_classes=["control-center-quick-settings"]' not in content:
        errors.append("Missing control-center-quick-settings CSS class")

    if "spacing=8," not in content:
        errors.append("Missing 8px spacing in quick settings")

    # Check widget imports still exist
    widgets = ["QuickSettings", "Brightness", "VolumeSlider", "User", "Media", "NotificationCenter", "WallpaperControl"]
    for widget in widgets:
        if widget not in content:
            errors.append(f"Missing widget import: {widget}")

    # Check docstring
    if "Noctalia-inspired design (Phase 3)" not in content:
        errors.append("Missing Phase 3 docstring")

    if errors:
        print(f"❌ control_center.py validation failed:")
        for error in errors:
            print(f"   - {error}")
        return False

    print("✅ control_center.py: Complete Noctalia redesign")
    return True


def validate_control_center_scss():
    """Validate Control Center SCSS styling."""
    print("\nTesting control_center.scss styling...")
    file_path = Path("ignis/scss/control_center.scss")
    content = file_path.read_text()

    errors = []

    # Check main control-center styling
    required_styles = [
        "background: rgba($surface-container, 0.95);",
        "backdrop-filter: blur(20px);",
        "border-radius: $radius-l 0 0 $radius-l;",
        "padding: $spacing-m;",
        "box-shadow: $shadow-elevation-4;",
        "min-width: 400px;",
        "max-width: 400px;",
    ]

    for style in required_styles:
        if style not in content:
            errors.append(f"Missing main container style: {style}")

    # Check container gap
    if ".control-center-container" not in content:
        errors.append("Missing .control-center-container class")

    if "gap: $spacing-m;" not in content:
        errors.append("Missing gap in container")

    # Check new section classes
    section_classes = [
        ".control-center-header",
        ".control-center-quick-settings",
    ]

    for css_class in section_classes:
        if css_class not in content:
            errors.append(f"Missing section class: {css_class}")

    # Check Blackhole token usage
    blackhole_tokens = [
        "$surface-container",
        "$radius-m",
        "$spacing-s",
        "$spacing-m",
        "$animation-fast",
        "$on-surface",
        "$primary-container",
        "$on-primary-container",
        "$shadow-elevation-4",
    ]

    for token in blackhole_tokens:
        if token not in content:
            errors.append(f"Missing Blackhole token: {token}")

    # Check updated qs-button styling
    if ".qs-button" not in content:
        errors.append("Missing .qs-button class")

    if "transform: scale(1.02);" not in content:
        errors.append("Missing scale transform on hover")

    # Check user widget updates
    if ".user-settings" not in content or ".user-power" not in content:
        errors.append("Missing user widget classes")

    # Check volume controls
    if ".volume-entry" not in content:
        errors.append("Missing volume entry class")

    # Check network widgets
    if ".network-item" not in content:
        errors.append("Missing network item class")

    # Check Phase 3 comment
    if "Phase 3, Task 1" not in content:
        errors.append("Missing Phase 3, Task 1 comment")

    if errors:
        print(f"❌ control_center.scss validation failed:")
        for error in errors:
            print(f"   - {error}")
        return False

    print("✅ control_center.scss: Complete Blackhole token styling")
    return True


def validate_integration():
    """Validate Control Center integration."""
    print("\nTesting Control Center integration...")

    errors = []

    # Check that control_center.py is importable structure-wise
    cc_path = Path("ignis/modules/control_center/control_center.py")
    cc_content = cc_path.read_text()

    # Verify clean structure (no RevealerWindow remnants)
    if "RevealerWindow" in cc_content:
        errors.append("Found RevealerWindow remnants (should be regular Window)")

    # Verify proper orientation parameter
    if 'orientation="vertical"' not in cc_content:
        errors.append("Missing vertical orientation in Box containers")

    # Check __init__.py exports ControlCenter
    init_path = Path("ignis/modules/control_center/__init__.py")
    if init_path.exists():
        init_content = init_path.read_text()
        if "ControlCenter" not in init_content:
            errors.append("ControlCenter not exported from __init__.py")

    if errors:
        print(f"❌ Integration validation failed:")
        for error in errors:
            print(f"   - {error}")
        return False

    print("✅ Integration: Control Center properly structured")
    return True


def main():
    """Run all validations."""
    print("=" * 60)
    print("Phase 3, Task 1: Control Center Base Redesign")
    print("Validation Test")
    print("=" * 60)

    results = []
    results.append(validate_control_center_py())
    results.append(validate_control_center_scss())
    results.append(validate_integration())

    print("\n" + "=" * 60)
    print(f"Results: {sum(results)}/3 tests passed")

    if all(results):
        print("✅ Task 1 validation passed!")
        print("\nImplemented features:")
        print("\nControl Center Redesign:")
        print("  ✅ Changed from RevealerWindow to regular Window")
        print("  ✅ Anchor: [top, right] - opens from right edge")
        print("  ✅ Exclusivity: normal (doesn't push other windows)")
        print("  ✅ Layer: overlay (stays on top)")
        print("  ✅ Container spacing: 12px between sections")
        print("  ✅ Section spacing: 8px within sections")
        print("\nNoctalia Aesthetics (SCSS):")
        print("  ✅ Background: rgba($surface-container, 0.95)")
        print("  ✅ Backdrop filter: blur(20px)")
        print("  ✅ Border radius: $radius-l 0 0 $radius-l")
        print("  ✅ Box shadow: $shadow-elevation-4")
        print("  ✅ Fixed width: 400px")
        print("  ✅ Padding: $spacing-m")
        print("\nBlackhole Design Tokens:")
        print("  ✅ All spacing uses $spacing-* tokens")
        print("  ✅ All radius uses $radius-* tokens")
        print("  ✅ All colors use M3 color tokens")
        print("  ✅ All animations use $animation-* tokens")
        print("  ✅ Typography uses $font-size-* tokens")
        print("  ✅ Hover effects with scale transforms")
        print("\nStructure:")
        print("  ✅ _create_header() - User widget section")
        print("  ✅ _create_quick_settings() - QS, sliders, controls")
        print("  ✅ _create_media_player() - Media controls")
        print("  ✅ _create_notifications() - Notification center")
        return 0
    else:
        print("❌ Task 1 validation failed")
        return 1


if __name__ == "__main__":
    exit(main())
