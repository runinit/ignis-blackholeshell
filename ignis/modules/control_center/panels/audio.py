"""
Audio Panel - Audio device management and volume control (Phase 3, Task 5).

Provides detailed audio device selection, volume controls, and device switching
for both output (speakers) and input (microphones).
"""

from ignis import widgets
from ignis.services.audio import AudioService, Stream
from .base import Panel
from ..panel_manager import get_panel_manager


audio = AudioService.get_default()


class DeviceRow(widgets.Box):
    """A single audio device row with icon, name, and selection indicator."""

    def __init__(self, stream: Stream):
        self._stream = stream
        is_default = stream.is_default if hasattr(stream, "is_default") else False

        super().__init__(
            css_classes=["audio-device-row"],
            child=[
                widgets.Icon(
                    image=stream.bind("icon_name") if hasattr(stream, "icon_name") else "audio-card-symbolic",
                    pixel_size=24,
                ),
                widgets.Box(
                    orientation="vertical",
                    hexpand=True,
                    child=[
                        widgets.Label(
                            label=stream.bind("description") if hasattr(stream, "description") else stream.name,
                            css_classes=["audio-device-name"],
                            halign="start",
                        ),
                        widgets.Label(
                            label=self._get_device_info(),
                            css_classes=["audio-device-info"],
                            halign="start",
                        ),
                    ],
                ),
                widgets.Icon(
                    image="object-select-symbolic",
                    visible=is_default,
                    css_classes=["audio-device-selected"],
                ),
            ],
            setup=lambda self: self.connect(
                "button-press-event", lambda *_: stream.set_default()
            ),
        )

    def _get_device_info(self) -> str:
        """Get device information string."""
        if hasattr(self._stream, "port"):
            return self._stream.port
        return "Audio Device"


class AudioPanel(Panel):
    """Audio devices and volume control panel."""

    __gtype_name__ = "AudioPanel"

    def __init__(self):
        super().__init__(title="Audio")

        panel_manager = get_panel_manager()

        # Build panel content
        self.child = [
            # Header with back button
            self.create_header(panel_manager),
            # Output devices section
            self._create_devices_section(
                title="Output Devices",
                devices=audio.speaker.streams if audio.speaker else [],
            ),
            # Input devices section
            self._create_devices_section(
                title="Input Devices",
                devices=audio.microphone.streams if audio.microphone else [],
            ),
        ]

    def _create_devices_section(self, title: str, devices: list) -> widgets.Box:
        """Create a devices section (output or input)."""
        return widgets.Box(
            orientation="vertical",
            spacing=8,
            css_classes=["audio-devices-section"],
            child=[
                widgets.Label(
                    label=title,
                    css_classes=["audio-section-title"],
                    halign="start",
                ),
                widgets.ScrolledWindow(
                    min_content_height=100,
                    max_content_height=200,
                    child=widgets.Box(
                        orientation="vertical",
                        spacing=4,
                        css_classes=["audio-devices-list"],
                        child=audio.speaker.bind(
                            "streams",
                            transform=lambda streams: [
                                DeviceRow(stream) for stream in streams
                            ],
                        ) if title == "Output Devices" else audio.microphone.bind(
                            "streams",
                            transform=lambda streams: [
                                DeviceRow(stream) for stream in streams
                            ],
                        ),
                    ),
                ),
            ],
        )
