"""
Brightness OSD - On-Screen Display for brightness control (Phase 4, Task 3).

Displays brightness level with icon, progress bar, and percentage label.
"""

from ignis import widgets
from ignis.services.backlight import BacklightService
from .osd_window import OSDWindow


class BrightnessOSD(OSDWindow):
    """Brightness OSD with icon, progress bar, and label."""

    __gtype_name__ = "BrightnessOSD"

    def __init__(self, monitor: int = 0):
        """
        Initialize Brightness OSD.

        Args:
            monitor: Monitor number to display on
        """
        self._backlight = BacklightService.get_default()

        super().__init__(monitor, namespace_suffix="BRIGHTNESS")

        # Only create UI if backlight is available
        if not self._backlight.available:
            return

        # Create UI elements
        self._icon = widgets.Icon(
            image=self._get_brightness_icon(),
            pixel_size=48,
            css_classes=["osd-icon"],
        )

        self._progress = widgets.Scale(
            min=0,
            max=100,
            value=self._get_brightness_value(),
            css_classes=["osd-progress"],
            sensitive=False,  # Make read-only for display
        )

        self._label = widgets.Label(
            label=self._get_brightness_label(),
            css_classes=["osd-label"],
        )

        # Set child
        self.child = widgets.Box(
            orientation="vertical",
            spacing=12,
            css_classes=["osd-container"],
            child=[
                self._icon,
                self._progress,
                self._label,
            ],
        )

        # Connect to backlight service signal
        self._backlight.connect("notify::brightness", lambda *_: self._on_brightness_changed())

    def _get_brightness_value(self) -> float:
        """Get current brightness as percentage (0-100)."""
        if not self._backlight.available or self._backlight.max_brightness == 0:
            return 0

        return (self._backlight.brightness / self._backlight.max_brightness) * 100

    def _get_brightness_icon(self) -> str:
        """Get appropriate brightness icon based on current level."""
        if not self._backlight.available:
            return "display-brightness-symbolic"

        brightness_percent = self._get_brightness_value()

        if brightness_percent == 0:
            return "display-brightness-off-symbolic"
        elif brightness_percent < 33:
            return "display-brightness-low-symbolic"
        elif brightness_percent < 66:
            return "display-brightness-medium-symbolic"
        else:
            return "display-brightness-high-symbolic"

    def _get_brightness_label(self) -> str:
        """Get brightness percentage label."""
        if not self._backlight.available:
            return "0%"

        return f"{int(self._get_brightness_value())}%"

    def _on_brightness_changed(self):
        """Handle brightness change."""
        if not self._backlight.available:
            return

        brightness = self._get_brightness_value()
        self._progress.set_value(brightness)
        self._label.set_label(self._get_brightness_label())
        self._icon.set_image(self._get_brightness_icon())
        self.show_osd()
