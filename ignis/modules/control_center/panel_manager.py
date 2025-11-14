"""
Panel Manager - Navigation system for Control Center panels (Phase 3, Task 2).

Manages panel navigation, transitions, and the navigation stack for sub-panels
like Calendar, Audio, WiFi, and Bluetooth.
"""

from typing import Optional, Dict, Callable
from ignis.gobject import IgnisGObject
from gi.repository import GObject


class PanelManager(IgnisGObject):
    """Manages panel navigation and transitions."""

    __gtype_name__ = "PanelManager"
    __gsignals__ = {
        "panel-changed": (GObject.SignalFlags.RUN_FIRST, GObject.TYPE_NONE, (str,)),
    }

    def __init__(self):
        super().__init__()
        self._current_panel: Optional[str] = "main"
        self._panel_stack: list[str] = []
        self._panels: Dict[str, any] = {}
        self._on_back_callbacks: Dict[str, Callable] = {}

    @GObject.Property
    def current_panel(self) -> str:
        """Get the name of the currently visible panel."""
        return self._current_panel

    @GObject.Property
    def can_go_back(self) -> bool:
        """Check if there are panels in the navigation stack."""
        return len(self._panel_stack) > 0

    def register_panel(self, name: str, panel, on_back: Optional[Callable] = None):
        """
        Register a panel with the manager.

        Args:
            name: Unique identifier for the panel
            panel: The panel widget instance
            on_back: Optional callback to execute when navigating back from this panel
        """
        self._panels[name] = panel
        if on_back:
            self._on_back_callbacks[name] = on_back

    def show_panel(self, name: str):
        """
        Show a panel and add current panel to navigation stack.

        Args:
            name: Name of the panel to show
        """
        if name not in self._panels:
            print(f"Warning: Panel '{name}' not registered")
            return

        # Add current panel to stack if not already there
        if self._current_panel and self._current_panel != name:
            self._panel_stack.append(self._current_panel)

        # Update current panel
        self._current_panel = name
        self.notify("current-panel")
        self.notify("can-go-back")
        self.emit("panel-changed", name)

    def go_back(self):
        """Navigate back to the previous panel in the stack."""
        if not self.can_go_back:
            return

        # Execute on_back callback for current panel if it exists
        if self._current_panel in self._on_back_callbacks:
            self._on_back_callbacks[self._current_panel]()

        # Pop the previous panel from stack
        previous_panel = self._panel_stack.pop()
        self._current_panel = previous_panel
        self.notify("current-panel")
        self.notify("can-go-back")
        self.emit("panel-changed", previous_panel)

    def reset(self):
        """Reset navigation to main panel and clear stack."""
        self._panel_stack.clear()
        self._current_panel = "main"
        self.notify("current-panel")
        self.notify("can-go-back")
        self.emit("panel-changed", "main")

    def get_panel(self, name: str):
        """
        Get a registered panel by name.

        Args:
            name: Name of the panel to retrieve

        Returns:
            The panel widget or None if not found
        """
        return self._panels.get(name)


# Global instance
_panel_manager_instance = None


def get_panel_manager() -> PanelManager:
    """Get the global PanelManager instance."""
    global _panel_manager_instance
    if _panel_manager_instance is None:
        _panel_manager_instance = PanelManager()
    return _panel_manager_instance
