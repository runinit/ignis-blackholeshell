from ignis import widgets
from ignis.window_manager import WindowManager
from .widgets import (
    QuickSettings,
    Brightness,
    VolumeSlider,
    User,
    Media,
    NotificationCenter,
    WallpaperControl,
)
from .menu import opened_menu
from .panel_manager import get_panel_manager

window_manager = WindowManager.get_default()


class ControlCenter(widgets.Window):
    """Control Center with Noctalia-inspired design (Phase 3)."""

    __gtype_name__ = "ControlCenter"

    def __init__(self):
        # Get panel manager instance
        self._panel_manager = get_panel_manager()

        # Create panel container (Stack for transitions)
        self._panel_container = widgets.Stack(
            transition_type="slide_left_right",
            transition_duration=300,
            css_classes=["panel-container"],
        )

        # Create main view
        main_view = widgets.Box(
            orientation="vertical",
            spacing=12,
            css_classes=["control-center-container"],
            child=[
                self._create_header(),
                self._create_quick_settings(),
                self._create_media_player(),
                self._create_notifications(),
            ],
        )

        # Register main view as a panel
        self._panel_container.add_named(main_view, "main")
        self._panel_manager.register_panel("main", main_view)

        # Set initial visible panel
        self._panel_container.set_visible_child_name("main")

        # Connect panel manager signals
        self._panel_manager.connect(
            "panel-changed", lambda manager, panel_name: self._on_panel_changed(panel_name)
        )

        super().__init__(
            namespace="ignis_CONTROL_CENTER",
            anchor=["top", "right"],
            exclusivity="normal",
            layer="overlay",
            css_classes=["control-center"],
            visible=False,
            kb_mode="on_demand",
            child=self._panel_container,
            setup=lambda self: self.connect(
                "notify::visible", lambda x, y: self._on_visibility_changed()
            ),
        )

    def _on_panel_changed(self, panel_name: str):
        """Handle panel change events from panel manager."""
        self._panel_container.set_visible_child_name(panel_name)

    def _on_visibility_changed(self):
        """Handle visibility changes (reset to main when closing)."""
        if not self.visible:
            # Reset to main panel when closing
            self._panel_manager.reset()
            opened_menu.set_value("")

    def _create_header(self) -> widgets.Box:
        """Create the header section with user info."""
        return widgets.Box(
            css_classes=["control-center-header"],
            child=[User()],
        )

    def _create_quick_settings(self) -> widgets.Box:
        """Create quick settings section."""
        return widgets.Box(
            orientation="vertical",
            spacing=8,
            css_classes=["control-center-quick-settings"],
            child=[
                QuickSettings(),
                VolumeSlider("speaker"),
                VolumeSlider("microphone"),
                Brightness(),
                WallpaperControl(),
            ],
        )

    def _create_media_player(self) -> widgets.Widget:
        """Create media player section."""
        return Media()

    def _create_notifications(self) -> widgets.Widget:
        """Create notifications section."""
        return NotificationCenter()

    def register_panel(self, name: str, panel):
        """
        Register a new panel with the Control Center.

        Args:
            name: Unique identifier for the panel
            panel: The panel widget instance
        """
        self._panel_container.add_named(panel, name)
        self._panel_manager.register_panel(name, panel)

    @property
    def panel_manager(self):
        """Get the panel manager instance."""
        return self._panel_manager
