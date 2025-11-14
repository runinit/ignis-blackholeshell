"""
Volume OSD - On-Screen Display for volume control (Phase 4, Task 2).

Displays volume level with icon, progress bar, and percentage label.
"""

from ignis import widgets
from ignis.services.audio import AudioService
from .osd_window import OSDWindow


class VolumeOSD(OSDWindow):
    """Volume OSD with icon, progress bar, and label."""

    __gtype_name__ = "VolumeOSD"

    def __init__(self, monitor: int = 0):
        """
        Initialize Volume OSD.

        Args:
            monitor: Monitor number to display on
        """
        self._audio = AudioService.get_default()

        super().__init__(monitor, namespace_suffix="VOLUME")

        # Create UI elements
        self._icon = widgets.Icon(
            image=self._get_volume_icon(),
            pixel_size=48,
            css_classes=["osd-icon"],
        )

        self._progress = widgets.LevelBar(
            min_value=0,
            max_value=100,
            value=self._get_volume_value(),
            css_classes=["osd-progress"],
        )

        self._label = widgets.Label(
            label=self._get_volume_label(),
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

        # Connect to audio service signals
        if self._audio.speaker:
            self._audio.speaker.connect("notify::volume", lambda *_: self._on_volume_changed())
            self._audio.speaker.connect("notify::is-muted", lambda *_: self._on_mute_changed())

    def _get_volume_value(self) -> float:
        """Get current volume as percentage (0-100)."""
        if not self._audio.speaker:
            return 0
        return self._audio.speaker.volume * 100

    def _get_volume_icon(self) -> str:
        """Get appropriate volume icon based on current state."""
        if not self._audio.speaker:
            return "audio-volume-muted-symbolic"

        if self._audio.speaker.is_muted:
            return "audio-volume-muted-symbolic"

        volume = self._audio.speaker.volume
        if volume == 0:
            return "audio-volume-muted-symbolic"
        elif volume < 0.33:
            return "audio-volume-low-symbolic"
        elif volume < 0.66:
            return "audio-volume-medium-symbolic"
        else:
            return "audio-volume-high-symbolic"

    def _get_volume_label(self) -> str:
        """Get volume percentage label."""
        if not self._audio.speaker:
            return "0%"

        if self._audio.speaker.is_muted:
            return "Muted"

        return f"{int(self._audio.speaker.volume * 100)}%"

    def _on_volume_changed(self):
        """Handle volume change."""
        if not self._audio.speaker:
            return

        volume = self._get_volume_value()
        self._progress.set_value(volume)
        self._label.set_label(self._get_volume_label())
        self._icon.set_image(self._get_volume_icon())
        self.show_osd()

    def _on_mute_changed(self):
        """Handle mute state change."""
        if not self._audio.speaker:
            return

        self._label.set_label(self._get_volume_label())
        self._icon.set_image(self._get_volume_icon())
        self.show_osd()
