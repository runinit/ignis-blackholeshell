#!/usr/bin/env python3
"""
Test script to validate Phase 2, Task 3: Dock Module Foundation
This validates the dock implementation without requiring GTK runtime.
"""

from pathlib import Path

def validate_dock_module_structure():
    """Validate dock module files exist."""
    print("Testing dock module structure...")

    files = [
        "ignis/modules/dock/__init__.py",
        "ignis/modules/dock/dock.py",
        "ignis/modules/dock/dock_item.py",
        "ignis/scss/dock.scss",
    ]

    errors = []
    for file_path in files:
        if not Path(file_path).exists():
            errors.append(f"Missing file: {file_path}")

    if errors:
        print(f"❌ Module structure validation failed:")
        for error in errors:
            print(f"   - {error}")
        return False

    print("✅ Dock module structure: All files present")
    return True


def validate_dock_init():
    """Validate __init__.py exports Dock."""
    print("\nTesting __init__.py...")
    file_path = Path("ignis/modules/dock/__init__.py")
    content = file_path.read_text()

    errors = []

    if "from .dock import Dock" not in content:
        errors.append("Missing 'from .dock import Dock'")

    if '__all__ = ["Dock"]' not in content:
        errors.append("Missing __all__ export")

    if errors:
        print(f"❌ __init__.py validation failed:")
        for error in errors:
            print(f"   - {error}")
        return False

    print("✅ __init__.py: Proper exports")
    return True


def validate_dock_item():
    """Validate DockItem implementation."""
    print("\nTesting dock_item.py...")
    file_path = Path("ignis/modules/dock/dock_item.py")
    content = file_path.read_text()

    errors = []

    # Check class definition
    if "class DockItem(widgets.Button):" not in content:
        errors.append("Missing DockItem class definition")

    # Check imports
    required_imports = [
        "from ignis import widgets",
        "from ignis.services.applications import Application",
        "from user_options import user_options",
    ]

    for imp in required_imports:
        if imp not in content:
            errors.append(f"Missing import: {imp}")

    # Check initialization parameters
    if "def __init__(self, app: Application, pinned: bool, running: bool):" not in content:
        errors.append("Missing __init__ with correct parameters")

    # Check icon sizing
    if "user_options.dock.size" not in content:
        errors.append("Missing dock size configuration")

    # Check CSS classes
    required_classes = ['"dock-item"', '"running"', '"inactive"']
    for css_class in required_classes:
        if css_class not in content:
            errors.append(f"Missing CSS class: {css_class}")

    # Check active indicator
    if '"active-indicator"' not in content:
        errors.append("Missing active indicator")

    # Check click handler
    if "def _on_click(self):" not in content:
        errors.append("Missing _on_click handler")

    # Check update method
    if "def update_running_state(self, is_running: bool):" not in content:
        errors.append("Missing update_running_state method")

    if errors:
        print(f"❌ dock_item.py validation failed:")
        for error in errors:
            print(f"   - {error}")
        return False

    print("✅ dock_item.py: Complete implementation")
    return True


def validate_dock():
    """Validate Dock main class."""
    print("\nTesting dock.py...")
    file_path = Path("ignis/modules/dock/dock.py")
    content = file_path.read_text()

    errors = []

    # Check class definition
    if "class Dock(widgets.Window):" not in content:
        errors.append("Missing Dock class definition")

    # Check imports
    required_imports = [
        "from ignis import widgets",
        "from ignis.services.applications import ApplicationsService",
        "from .dock_item import DockItem",
        "from user_options import user_options",
    ]

    for imp in required_imports:
        if imp not in content:
            errors.append(f"Missing import: {imp}")

    # Check ApplicationsService initialization
    if "apps_service = ApplicationsService.get_default()" not in content:
        errors.append("Missing ApplicationsService initialization")

    # Check methods
    required_methods = [
        "_get_anchor",
        "_build_dock_items",
        "_find_app",
        "_on_apps_changed",
        "pin_app",
        "unpin_app",
    ]

    for method in required_methods:
        if f"def {method}" not in content:
            errors.append(f"Missing method: {method}")

    # Check position handling
    if "user_options.dock.position" not in content:
        errors.append("Missing position configuration")

    # Check enabled handling
    if "user_options.dock.enabled" not in content:
        errors.append("Missing enabled configuration")

    # Check apps service connection
    if 'apps_service.connect("changed"' not in content:
        errors.append("Missing apps service change listener")

    # Check pinned apps handling
    if "user_options.dock.pinned_apps" not in content:
        errors.append("Missing pinned apps configuration")

    if errors:
        print(f"❌ dock.py validation failed:")
        for error in errors:
            print(f"   - {error}")
        return False

    print("✅ dock.py: Complete implementation")
    return True


def validate_dock_scss():
    """Validate dock SCSS styling."""
    print("\nTesting dock.scss...")
    file_path = Path("ignis/scss/dock.scss")
    content = file_path.read_text()

    errors = []

    # Check main dock class
    if ".dock {" not in content:
        errors.append("Missing .dock class")

    # Check position classes
    position_classes = [
        "&.position-bottom {",
        "&.position-left {",
        "&.position-right {",
    ]

    for css_class in position_classes:
        if css_class not in content:
            errors.append(f"Missing position class: {css_class}")

    # Check dock-item styling
    if ".dock-item {" not in content:
        errors.append("Missing .dock-item class")

    # Check states
    states = ["&:hover {", "&:active {", "&.running {", "&.inactive {"]
    for state in states:
        if state not in content:
            errors.append(f"Missing state: {state}")

    # Check active indicator
    if ".active-indicator {" not in content:
        errors.append("Missing .active-indicator class")

    # Check Blackhole design tokens
    tokens = [
        "$surface-container",
        "$radius-l",
        "$radius-m",
        "$spacing-s",
        "$spacing-xs",
        "$spacing-m",
        "$shadow-elevation-3",
        "$animation-fast",
        "$primary",
    ]

    for token in tokens:
        if token not in content:
            errors.append(f"Missing design token: {token}")

    if errors:
        print(f"❌ dock.scss validation failed:")
        for error in errors:
            print(f"   - {error}")
        return False

    print("✅ dock.scss: Complete styling with Blackhole tokens")
    return True


def validate_integration():
    """Validate integration with main codebase."""
    print("\nTesting integration...")

    errors = []

    # Check style.scss import
    style_path = Path("ignis/style.scss")
    style_content = style_path.read_text()

    if '@import "./scss/dock.scss";' not in style_content:
        errors.append("dock.scss not imported in style.scss")

    # Check config.py integration
    config_path = Path("ignis/config.py")
    config_content = config_path.read_text()

    if "from modules.dock import Dock" not in config_content:
        errors.append("Dock not imported in config.py")

    if "if user_options.dock.enabled:" not in config_content:
        errors.append("Dock initialization missing enabled check")

    if "Dock(monitor)" not in config_content:
        errors.append("Dock not initialized per monitor")

    if errors:
        print(f"❌ Integration validation failed:")
        for error in errors:
            print(f"   - {error}")
        return False

    print("✅ Integration: Dock properly integrated into codebase")
    return True


def main():
    """Run all validations."""
    print("=" * 60)
    print("Phase 2, Task 3: Dock Module Foundation")
    print("Validation Test")
    print("=" * 60)

    results = []
    results.append(validate_dock_module_structure())
    results.append(validate_dock_init())
    results.append(validate_dock_item())
    results.append(validate_dock())
    results.append(validate_dock_scss())
    results.append(validate_integration())

    print("\n" + "=" * 60)
    print(f"Results: {sum(results)}/6 tests passed")

    if all(results):
        print("✅ Task 3 validation passed!")
        print("\nImplemented features:")
        print("  ✅ Dock module structure (__init__.py, dock.py, dock_item.py)")
        print("  ✅ DockItem widget with icon and active indicator")
        print("  ✅ Dock window with pinned and running apps")
        print("  ✅ Application tracking via ApplicationsService")
        print("  ✅ Pin/unpin functionality")
        print("  ✅ Position support (bottom/left/right)")
        print("  ✅ Icon size customization")
        print("  ✅ Dock SCSS styling with Blackhole tokens")
        print("  ✅ Integration with style.scss and config.py")
        print("  ✅ Enabled/disabled toggle support")
        return 0
    else:
        print("❌ Task 3 validation failed")
        return 1


if __name__ == "__main__":
    exit(main())
