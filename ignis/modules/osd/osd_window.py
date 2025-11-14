"""
OSD Window - Base class for On-Screen Display windows (Phase 4, Task 1).

Provides reusable OSD window with auto-hide, fade animations, and timeout management.
"""

from gi.repository import GLib
from ignis import widgets


class OSDWindow(widgets.Window):
    """Base OSD window with auto-hide and animations."""

    __gtype_name__ = "OSDWindow"

    def __init__(self, monitor: int = 0, namespace_suffix: str = ""):
        """
        Initialize OSD window.

        Args:
            monitor: Monitor number to display on
            namespace_suffix: Suffix for window namespace (e.g., "VOLUME", "BRIGHTNESS")
        """
        self._timeout_id = None
        self._hide_delay = 2000  # 2 seconds default
        self._hide_animation_id = None

        namespace = f"ignis_OSD_{namespace_suffix}_{monitor}" if namespace_suffix else f"ignis_OSD_{monitor}"

        super().__init__(
            namespace=namespace,
            monitor=monitor,
            anchor=["top"],
            exclusivity="ignore",
            layer="overlay",
            kb_mode="none",
            css_classes=["osd-window"],
            visible=False,
        )

    def show_osd(self, duration: int = None):
        """
        Show OSD with auto-hide after duration.

        Args:
            duration: Milliseconds to show before hiding (default: 2000)
        """
        self._cancel_timeout()
        self._cancel_hide_animation()

        # Show window
        self.set_visible(True)
        self.remove_css_class("hiding")
        self.add_css_class("showing")

        # Remove showing class after animation
        GLib.timeout_add(300, lambda: self.remove_css_class("showing"))

        # Schedule hide
        hide_after = duration if duration is not None else self._hide_delay
        self._timeout_id = GLib.timeout_add(hide_after, self._start_hide)

    def _start_hide(self):
        """Start hide animation."""
        self.remove_css_class("showing")
        self.add_css_class("hiding")
        self._hide_animation_id = GLib.timeout_add(300, self._complete_hide)
        self._timeout_id = None
        return False

    def _complete_hide(self):
        """Complete hide after animation."""
        self.set_visible(False)
        self.remove_css_class("hiding")
        self._hide_animation_id = None
        return False

    def _cancel_timeout(self):
        """Cancel pending hide timeout."""
        if self._timeout_id:
            GLib.source_remove(self._timeout_id)
            self._timeout_id = None

    def _cancel_hide_animation(self):
        """Cancel pending hide animation."""
        if self._hide_animation_id:
            GLib.source_remove(self._hide_animation_id)
            self._hide_animation_id = None
