"""
Bluetooth Panel - Bluetooth device management (Phase 3, Task 7).

Provides Bluetooth device pairing, connection management, and device status display.
"""

from ignis import widgets
from ignis.services.bluetooth import BluetoothService, BluetoothDevice
from .base import Panel
from ..panel_manager import get_panel_manager


bluetooth = BluetoothService.get_default()


class DeviceRow(widgets.Button):
    """A single Bluetooth device row with icon, name, and connection status."""

    def __init__(self, device: BluetoothDevice):
        self._device = device

        super().__init__(
            css_classes=["bluetooth-device-row"],
            on_click=lambda x: device.disconnect_from()
            if device.connected
            else device.connect_to(),
            child=widgets.Box(
                child=[
                    widgets.Icon(
                        image=device.bind("icon_name"),
                        pixel_size=24,
                    ),
                    widgets.Box(
                        orientation="vertical",
                        hexpand=True,
                        child=[
                            widgets.Label(
                                label=device.alias,
                                css_classes=["bluetooth-device-name"],
                                halign="start",
                            ),
                            widgets.Label(
                                label=self._get_device_status(device),
                                css_classes=["bluetooth-device-status"],
                                halign="start",
                            ),
                        ],
                    ),
                    widgets.Icon(
                        image="object-select-symbolic",
                        visible=device.bind("connected"),
                        css_classes=["bluetooth-device-connected"],
                    ),
                ],
            ),
        )

    def _get_device_status(self, device: BluetoothDevice) -> str:
        """Get device status string."""
        if device.connected:
            return "Connected"
        elif device.paired:
            return "Paired"
        else:
            return "Available"


class BluetoothPanel(Panel):
    """Bluetooth device management panel."""

    __gtype_name__ = "BluetoothPanel"

    def __init__(self):
        super().__init__(title="Bluetooth")

        panel_manager = get_panel_manager()

        # Bluetooth toggle switch for header
        bt_toggle = widgets.Switch(
            active=bluetooth.bind("powered"),
            on_change=lambda switch, state: bluetooth.set_powered(state),
            css_classes=["bluetooth-toggle"],
        )

        # Enable setup mode when panel is shown
        bluetooth.set_setup_mode(True)

        # Build panel content
        self.child = [
            # Header with back button and toggle
            self.create_header(panel_manager, extra_widgets=[bt_toggle]),
            # Paired devices section
            self._create_devices_section(
                title="Paired Devices",
                filter_func=lambda d: d.paired,
            ),
            # Available devices section
            self._create_devices_section(
                title="Available Devices",
                filter_func=lambda d: not d.paired,
            ),
        ]

        # Register on_back callback to disable setup mode
        panel_manager.register_panel(
            "bluetooth",
            self,
            on_back=lambda: bluetooth.set_setup_mode(False),
        )

    def _create_devices_section(self, title: str, filter_func) -> widgets.Box:
        """Create a devices section (paired or available)."""
        return widgets.Box(
            orientation="vertical",
            spacing=8,
            css_classes=["bluetooth-devices-section"],
            child=[
                widgets.Label(
                    label=title,
                    css_classes=["bluetooth-section-title"],
                    halign="start",
                ),
                widgets.ScrolledWindow(
                    min_content_height=150,
                    max_content_height=300,
                    child=widgets.Box(
                        orientation="vertical",
                        spacing=4,
                        css_classes=["bluetooth-devices-list"],
                        child=bluetooth.bind(
                            "devices",
                            transform=lambda devices: [
                                DeviceRow(device)
                                for device in devices
                                if filter_func(device)
                            ],
                        ),
                    ),
                ),
            ],
        )
