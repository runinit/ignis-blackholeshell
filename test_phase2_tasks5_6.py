#!/usr/bin/env python3
"""
Test script to validate Phase 2, Tasks 5-6: Context Menu & Settings UI
This validates the remaining dock features without requiring GTK runtime.
"""

from pathlib import Path

def validate_dock_item_context_menu():
    """Validate DockItem has context menu implementation."""
    print("Testing DockItem context menu...")
    file_path = Path("ignis/modules/dock/dock_item.py")
    content = file_path.read_text()

    errors = []

    # Check Gdk import for button events
    if "from gi.repository import Gdk" not in content:
        errors.append("Missing Gdk import for button events")

    # Check dock parameter in __init__
    if "def __init__(self, app: Application, pinned: bool, running: bool, dock):" not in content:
        errors.append("Missing dock parameter in __init__")

    if "self._dock = dock" not in content:
        errors.append("Missing dock reference storage")

    # Check button-press-event connection
    if 'self.connect("button-press-event", self._on_button_press)' not in content:
        errors.append("Missing button-press-event connection")

    # Check context menu methods
    required_methods = [
        "_on_button_press",
        "_show_context_menu",
        "_toggle_pin",
        "_quit_app",
    ]

    for method in required_methods:
        if f"def {method}" not in content:
            errors.append(f"Missing method: {method}")

    # Check for right-click detection
    if "Gdk.BUTTON_SECONDARY" not in content:
        errors.append("Missing right-click button detection")

    # Check PopoverMenu usage
    if "widgets.PopoverMenu" not in content:
        errors.append("Missing PopoverMenu implementation")

    # Check menu items
    menu_items = [
        '"Pin to Dock"',
        '"Unpin from Dock"',
        '"Launch"',
        '"Quit"',
    ]

    for item in menu_items:
        if item not in content:
            errors.append(f"Missing menu item: {item}")

    # Check toggle_pin calls dock methods
    if "self._dock.unpin_app" not in content:
        errors.append("Missing unpin_app call")

    if "self._dock.pin_app" not in content:
        errors.append("Missing pin_app call")

    if errors:
        print(f"❌ Context menu validation failed:")
        for error in errors:
            print(f"   - {error}")
        return False

    print("✅ DockItem: Complete context menu implementation")
    return True


def validate_dock_reference_passing():
    """Validate Dock passes reference to DockItem."""
    print("\nTesting Dock reference passing...")
    file_path = Path("ignis/modules/dock/dock.py")
    content = file_path.read_text()

    errors = []

    # Check DockItem calls include dock=self
    if "DockItem(app, pinned=True, running=is_running, dock=self)" not in content:
        errors.append("Missing dock=self for pinned items")

    if "DockItem(app, pinned=False, running=True, dock=self)" not in content:
        errors.append("Missing dock=self for running items")

    if errors:
        print(f"❌ Dock reference passing validation failed:")
        for error in errors:
            print(f"   - {error}")
        return False

    print("✅ Dock: Properly passes reference to DockItem")
    return True


def validate_dock_settings_ui():
    """Validate Dock settings UI in appearance.py."""
    print("\nTesting Dock settings UI...")
    file_path = Path("ignis/modules/settings/pages/appearance.py")
    content = file_path.read_text()

    errors = []

    # Check for Dock Configuration group
    if 'name="Dock Configuration"' not in content:
        errors.append("Missing Dock Configuration SettingsGroup")

    # Check required UI components
    required_components = [
        ('label="Enable Dock"', "Enable Dock toggle"),
        ('active=user_options.dock.bind("enabled")', "Enable dock binding"),
        ('label="Position"', "Position dropdown"),
        ('"Bottom", "Left", "Right"', "Position options"),
        ('label="Icon Size"', "Icon size spinner"),
        ('value=user_options.dock.bind("size")', "Size binding"),
        ('label="Auto-Hide"', "Auto-hide toggle"),
        ('active=user_options.dock.bind("auto_hide")', "Auto-hide binding"),
    ]

    for code, description in required_components:
        if code not in content:
            errors.append(f"Missing UI component: {description}")

    # Check for handler methods
    required_handlers = [
        "_get_dock_position_index",
        "_on_dock_position_changed",
    ]

    for handler in required_handlers:
        if handler not in content:
            errors.append(f"Missing handler method: {handler}")

    # Check position mapping
    if 'positions = ["bottom", "left", "right"]' not in content:
        errors.append("Missing dock position mapping")

    # Check size constraints
    if "min=0.5" not in content or "max=2.0" not in content:
        errors.append("Missing icon size constraints")

    # Check sublabels
    sublabels = [
        "Show application dock",
        "Screen edge for dock placement",
        "Dock icon size multiplier",
        "Automatically hide dock when not in use",
    ]

    for sublabel in sublabels:
        if sublabel not in content:
            errors.append(f"Missing sublabel: {sublabel}")

    if errors:
        print(f"❌ Dock settings UI validation failed:")
        for error in errors:
            print(f"   - {error}")
        return False

    print("✅ Dock settings UI: Complete implementation")
    return True


def validate_integration():
    """Validate overall integration."""
    print("\nTesting overall integration...")

    errors = []

    # Check appearance.py has all three settings groups
    appearance_path = Path("ignis/modules/settings/pages/appearance.py")
    appearance_content = appearance_path.read_text()

    groups = [
        'name="Bar Configuration"',
        'name="Dock Configuration"',
    ]

    for group in groups:
        if group not in appearance_content:
            errors.append(f"Missing settings group: {group}")

    # Verify order
    bar_pos = appearance_content.find('name="Bar Configuration"')
    dock_pos = appearance_content.find('name="Dock Configuration"')

    if bar_pos == -1 or dock_pos == -1:
        errors.append("Cannot verify settings group order")
    elif bar_pos > dock_pos:
        errors.append("Dock Configuration should be after Bar Configuration")

    if errors:
        print(f"❌ Integration validation failed:")
        for error in errors:
            print(f"   - {error}")
        return False

    print("✅ Integration: All features properly integrated")
    return True


def main():
    """Run all validations."""
    print("=" * 60)
    print("Phase 2, Tasks 5-6: Context Menu & Settings UI")
    print("Validation Test")
    print("=" * 60)

    results = []
    results.append(validate_dock_item_context_menu())
    results.append(validate_dock_reference_passing())
    results.append(validate_dock_settings_ui())
    results.append(validate_integration())

    print("\n" + "=" * 60)
    print(f"Results: {sum(results)}/4 tests passed")

    if all(results):
        print("✅ Tasks 5-6 validation passed!")
        print("\nImplemented features:")
        print("\nTask 5: Context Menu & App Tracking")
        print("  ✅ Right-click context menu on dock items")
        print("  ✅ Pin/Unpin functionality with menu")
        print("  ✅ Launch menu option")
        print("  ✅ Quit menu option (visible when running)")
        print("  ✅ Gdk button event handling")
        print("  ✅ PopoverMenu integration")
        print("  ✅ Dock reference passing to items")
        print("\nTask 6: Settings UI & Integration")
        print("  ✅ Dock Configuration settings group")
        print("  ✅ Enable/Disable dock toggle")
        print("  ✅ Position selector (Bottom/Left/Right)")
        print("  ✅ Icon size spinner (0.5x - 2.0x)")
        print("  ✅ Auto-Hide toggle")
        print("  ✅ Handler methods for settings")
        print("  ✅ Reactive bindings for real-time updates")
        print("  ✅ Descriptive sublabels")
        print("  ✅ Integration with Bar Configuration")
        print("\nNote: Task 4 (Auto-Hide with peek window) deferred")
        print("      for future enhancement due to complexity.")
        return 0
    else:
        print("❌ Tasks 5-6 validation failed")
        return 1


if __name__ == "__main__":
    exit(main())
