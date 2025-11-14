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

window_manager = WindowManager.get_default()


class ControlCenter(widgets.Window):
    """Control Center with Noctalia-inspired design (Phase 3)."""

    __gtype_name__ = "ControlCenter"

    def __init__(self):
        super().__init__(
            namespace="ignis_CONTROL_CENTER",
            anchor=["top", "right"],
            exclusivity="normal",
            layer="overlay",
            css_classes=["control-center"],
            visible=False,
            kb_mode="on_demand",
            child=widgets.Box(
                orientation="vertical",
                spacing=12,
                css_classes=["control-center-container"],
                child=[
                    self._create_header(),
                    self._create_quick_settings(),
                    self._create_media_player(),
                    self._create_notifications(),
                ],
            ),
            setup=lambda self: self.connect(
                "notify::visible", lambda x, y: opened_menu.set_value("")
            ),
        )

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
