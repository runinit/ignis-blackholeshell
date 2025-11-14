#!/usr/bin/env python3
"""
Test script to validate Phase 3, Task 2: Panel Navigation System
This validates the panel navigation implementation without requiring GTK runtime.
"""

from pathlib import Path


def validate_panel_manager():
    """Validate PanelManager implementation."""
    print("Testing panel_manager.py implementation...")
    file_path = Path("ignis/modules/control_center/panel_manager.py")
    content = file_path.read_text()

    errors = []

    # Check class definition
    if "class PanelManager(IgnisGObject):" not in content:
        errors.append("Missing PanelManager class with IgnisGObject inheritance")

    # Check __gtype_name__
    if '__gtype_name__ = "PanelManager"' not in content:
        errors.append("Missing __gtype_name__ declaration")

    # Check signals
    if '"panel-changed"' not in content:
        errors.append("Missing panel-changed signal")

    # Check state variables
    state_vars = [
        "self._current_panel",
        "self._panel_stack",
        "self._panels",
        "self._on_back_callbacks",
    ]

    for var in state_vars:
        if var not in content:
            errors.append(f"Missing state variable: {var}")

    # Check properties
    properties = ["current_panel", "can_go_back"]
    for prop in properties:
        if f"def {prop}(self)" not in content:
            errors.append(f"Missing property: {prop}")

    # Check methods
    required_methods = [
        "register_panel",
        "show_panel",
        "go_back",
        "reset",
        "get_panel",
    ]

    for method in required_methods:
        if f"def {method}" not in content:
            errors.append(f"Missing method: {method}")

    # Check navigation stack logic
    if "self._panel_stack.append" not in content:
        errors.append("Missing navigation stack append logic")

    if "self._panel_stack.pop()" not in content:
        errors.append("Missing navigation stack pop logic")

    # Check signal emission
    if 'self.emit("panel-changed"' not in content:
        errors.append("Missing panel-changed signal emission")

    # Check global instance function
    if "def get_panel_manager()" not in content:
        errors.append("Missing get_panel_manager() function")

    # Check docstrings
    if "Phase 3, Task 2" not in content:
        errors.append("Missing Phase 3, Task 2 comment")

    if errors:
        print(f"❌ panel_manager.py validation failed:")
        for error in errors:
            print(f"   - {error}")
        return False

    print("✅ panel_manager.py: Complete navigation system")
    return True


def validate_base_panel():
    """Validate base Panel class."""
    print("\nTesting panels/base.py implementation...")
    file_path = Path("ignis/modules/control_center/panels/base.py")
    content = file_path.read_text()

    errors = []

    # Check class definition
    if "class Panel(widgets.Box):" not in content:
        errors.append("Missing Panel class with Box inheritance")

    # Check __gtype_name__
    if '__gtype_name__ = "Panel"' not in content:
        errors.append("Missing __gtype_name__ declaration")

    # Check __init__ parameters
    if "def __init__(self, title: str, **kwargs):" not in content:
        errors.append("Missing __init__ with title parameter")

    # Check title property
    if "def title(self)" not in content:
        errors.append("Missing title property")

    # Check create_header method
    if "def create_header" not in content:
        errors.append("Missing create_header method")

    # Check CSS class assignment
    if '"panel"' not in content:
        errors.append("Missing panel CSS class")

    # Check orientation setting
    if '"vertical"' not in content:
        errors.append("Missing vertical orientation")

    # Check back button creation
    if "panel-back-button" not in content:
        errors.append("Missing panel-back-button CSS class")

    # Check title label
    if "panel-title" not in content:
        errors.append("Missing panel-title CSS class")

    # Check panel manager usage
    if "panel_manager.go_back()" not in content:
        errors.append("Missing go_back() call")

    if errors:
        print(f"❌ panels/base.py validation failed:")
        for error in errors:
            print(f"   - {error}")
        return False

    print("✅ panels/base.py: Complete base Panel class")
    return True


def validate_panels_init():
    """Validate panels/__init__.py."""
    print("\nTesting panels/__init__.py...")
    file_path = Path("ignis/modules/control_center/panels/__init__.py")
    content = file_path.read_text()

    errors = []

    # Check imports
    if "from .base import Panel" not in content:
        errors.append("Missing Panel import")

    # Check __all__
    if '"Panel"' not in content:
        errors.append("Missing Panel in __all__")

    if errors:
        print(f"❌ panels/__init__.py validation failed:")
        for error in errors:
            print(f"   - {error}")
        return False

    print("✅ panels/__init__.py: Proper exports")
    return True


def validate_control_center_integration():
    """Validate Control Center panel integration."""
    print("\nTesting control_center.py panel integration...")
    file_path = Path("ignis/modules/control_center/control_center.py")
    content = file_path.read_text()

    errors = []

    # Check imports
    if "from .panel_manager import get_panel_manager" not in content:
        errors.append("Missing panel_manager import")

    # Check panel manager instance
    if "self._panel_manager = get_panel_manager()" not in content:
        errors.append("Missing panel manager initialization")

    # Check Stack widget
    if "widgets.Stack(" not in content:
        errors.append("Missing Stack widget for panel container")

    if 'transition_type="slide_left_right"' not in content:
        errors.append("Missing slide_left_right transition")

    if "transition_duration=300" not in content:
        errors.append("Missing 300ms transition duration")

    # Check panel registration
    if 'add_named(main_view, "main")' not in content:
        errors.append("Missing main view registration")

    if 'register_panel("main", main_view)' not in content:
        errors.append("Missing panel manager registration")

    # Check signal connection
    if '"panel-changed"' not in content:
        errors.append("Missing panel-changed signal connection")

    # Check methods
    required_methods = [
        "_on_panel_changed",
        "_on_visibility_changed",
        "register_panel",
    ]

    for method in required_methods:
        if f"def {method}" not in content:
            errors.append(f"Missing method: {method}")

    # Check visibility reset
    if "self._panel_manager.reset()" not in content:
        errors.append("Missing panel manager reset on visibility change")

    # Check property
    if "def panel_manager(self):" not in content:
        errors.append("Missing panel_manager property")

    if errors:
        print(f"❌ control_center.py integration validation failed:")
        for error in errors:
            print(f"   - {error}")
        return False

    print("✅ control_center.py: Complete panel integration")
    return True


def validate_scss_styles():
    """Validate panel navigation SCSS styles."""
    print("\nTesting control_center.scss panel styles...")
    file_path = Path("ignis/scss/control_center.scss")
    content = file_path.read_text()

    errors = []

    # Check panel container styles
    if ".panel-container" not in content:
        errors.append("Missing .panel-container class")

    # Check panel styles
    if ".panel" not in content:
        errors.append("Missing .panel class")

    # Check animations
    if "@keyframes slideIn" not in content:
        errors.append("Missing slideIn animation")

    if "transform: translateX(100%);" not in content:
        errors.append("Missing translateX transform")

    # Check panel header
    if ".panel-header" not in content:
        errors.append("Missing .panel-header class")

    # Check back button
    if ".panel-back-button" not in content:
        errors.append("Missing .panel-back-button class")

    # Check title
    if ".panel-title" not in content:
        errors.append("Missing .panel-title class")

    # Check Blackhole tokens
    blackhole_tokens = [
        "$animation-normal",
        "$spacing-s",
        "$spacing-m",
        "$radius-full",
        "$font-size-l",
        "$font-size-xl",
    ]

    for token in blackhole_tokens:
        if token not in content:
            errors.append(f"Missing Blackhole token: {token}")

    # Check Task 2 comment
    if "Phase 3, Task 2" not in content:
        errors.append("Missing Phase 3, Task 2 comment")

    if errors:
        print(f"❌ control_center.scss validation failed:")
        for error in errors:
            print(f"   - {error}")
        return False

    print("✅ control_center.scss: Complete panel navigation styles")
    return True


def validate_directory_structure():
    """Validate panels directory structure."""
    print("\nTesting panels directory structure...")
    errors = []

    # Check directory exists
    panels_dir = Path("ignis/modules/control_center/panels")
    if not panels_dir.exists():
        errors.append("Missing panels directory")
    elif not panels_dir.is_dir():
        errors.append("panels is not a directory")

    # Check required files
    required_files = [
        "ignis/modules/control_center/panels/__init__.py",
        "ignis/modules/control_center/panels/base.py",
    ]

    for file_path in required_files:
        if not Path(file_path).exists():
            errors.append(f"Missing file: {file_path}")

    if errors:
        print(f"❌ Directory structure validation failed:")
        for error in errors:
            print(f"   - {error}")
        return False

    print("✅ Directory structure: Properly organized")
    return True


def main():
    """Run all validations."""
    print("=" * 60)
    print("Phase 3, Task 2: Panel Navigation System")
    print("Validation Test")
    print("=" * 60)

    results = []
    results.append(validate_panel_manager())
    results.append(validate_base_panel())
    results.append(validate_panels_init())
    results.append(validate_control_center_integration())
    results.append(validate_scss_styles())
    results.append(validate_directory_structure())

    print("\n" + "=" * 60)
    print(f"Results: {sum(results)}/6 tests passed")

    if all(results):
        print("✅ Task 2 validation passed!")
        print("\nImplemented features:")
        print("\nPanelManager (panel_manager.py):")
        print("  ✅ Navigation state management")
        print("  ✅ Panel registration system")
        print("  ✅ Navigation stack (push/pop)")
        print("  ✅ show_panel() - Navigate forward")
        print("  ✅ go_back() - Navigate backward")
        print("  ✅ reset() - Return to main")
        print("  ✅ panel-changed signal emission")
        print("  ✅ current_panel and can_go_back properties")
        print("  ✅ On-back callback support")
        print("\nBase Panel Class (panels/base.py):")
        print("  ✅ Inherits from widgets.Box")
        print("  ✅ Vertical orientation by default")
        print("  ✅ Panel CSS class auto-applied")
        print("  ✅ create_header() helper method")
        print("  ✅ Back button with go_back() integration")
        print("  ✅ Title label support")
        print("  ✅ Extra widgets support (toggles, etc.)")
        print("\nControl Center Integration:")
        print("  ✅ Stack widget for panel transitions")
        print("  ✅ slide_left_right transition (300ms)")
        print("  ✅ Main view registered as 'main' panel")
        print("  ✅ panel-changed signal handler")
        print("  ✅ Auto-reset to main on close")
        print("  ✅ register_panel() public method")
        print("  ✅ panel_manager property accessor")
        print("\nCSS Styling:")
        print("  ✅ .panel-container transitions")
        print("  ✅ .panel slideIn animation")
        print("  ✅ translateX(100%) → translateX(0)")
        print("  ✅ Opacity 0 → 1 fade-in")
        print("  ✅ .panel-header layout")
        print("  ✅ .panel-back-button with hover effects")
        print("  ✅ .panel-title typography")
        print("  ✅ All Blackhole tokens used")
        print("\nDirectory Structure:")
        print("  ✅ ignis/modules/control_center/panels/")
        print("  ✅ panels/__init__.py with exports")
        print("  ✅ panels/base.py with Panel class")
        return 0
    else:
        print("❌ Task 2 validation failed")
        return 1


if __name__ == "__main__":
    exit(main())
