"""
Network Panel - WiFi network list and connection (Phase 3, Task 6).

Provides WiFi network scanning, connection management, and signal strength display.
"""

import asyncio
from ignis import widgets
from ignis.services.network import NetworkService, WifiAccessPoint
from .base import Panel
from ..panel_manager import get_panel_manager


network = NetworkService.get_default()


class NetworkRow(widgets.Button):
    """A single WiFi network row with signal strength and connection status."""

    def __init__(self, access_point: WifiAccessPoint):
        self._ap = access_point

        super().__init__(
            css_classes=["network-row"],
            on_click=lambda x: asyncio.create_task(access_point.connect_to_graphical()),
            child=widgets.Box(
                child=[
                    widgets.Icon(
                        image=access_point.bind(
                            "strength",
                            transform=lambda value: access_point.icon_name,
                        ),
                        pixel_size=24,
                    ),
                    widgets.Label(
                        label=access_point.ssid,
                        css_classes=["network-name"],
                        halign="start",
                        hexpand=True,
                    ),
                    widgets.Icon(
                        image="object-select-symbolic",
                        visible=access_point.bind("is_connected"),
                        css_classes=["network-connected"],
                    ),
                    widgets.Icon(
                        image="network-wireless-encrypted-symbolic",
                        visible=access_point.bind(
                            "security",
                            transform=lambda sec: len(sec) > 0,
                        ),
                        css_classes=["network-secure"],
                    ),
                ],
            ),
        )


class NetworkPanel(Panel):
    """WiFi network management panel."""

    __gtype_name__ = "NetworkPanel"

    def __init__(self):
        super().__init__(title="WiFi")

        panel_manager = get_panel_manager()

        # Get first WiFi device (most systems have only one)
        wifi_device = network.wifi.devices[0] if network.wifi.devices else None

        # Trigger initial scan
        if wifi_device:
            asyncio.create_task(wifi_device.scan())

        # WiFi toggle switch for header
        wifi_toggle = widgets.Switch(
            active=network.wifi.bind("enabled"),
            on_change=lambda switch, state: network.wifi.set_enabled(state),
            css_classes=["network-toggle"],
        )

        # Build panel content
        self.child = [
            # Header with back button and toggle
            self.create_header(panel_manager, extra_widgets=[wifi_toggle]),
            # Connected network section
            self._create_connected_section(wifi_device),
            # Available networks section
            self._create_available_section(wifi_device),
        ]

    def _create_connected_section(self, device) -> widgets.Box:
        """Create the currently connected network section."""
        if not device or not device.ap or not device.ap.is_connected:
            return widgets.Box(visible=False)

        return widgets.Box(
            orientation="vertical",
            spacing=8,
            css_classes=["network-connected-section"],
            child=[
                widgets.Label(
                    label="Connected",
                    css_classes=["network-section-title"],
                    halign="start",
                ),
                widgets.Box(
                    css_classes=["network-connected-box"],
                    child=[
                        widgets.Icon(
                            image=device.ap.bind(
                                "strength",
                                transform=lambda value: device.ap.icon_name,
                            ),
                            pixel_size=32,
                        ),
                        widgets.Box(
                            orientation="vertical",
                            hexpand=True,
                            child=[
                                widgets.Label(
                                    label=device.ap.bind("ssid"),
                                    css_classes=["network-connected-name"],
                                    halign="start",
                                ),
                                widgets.Label(
                                    label=device.ap.bind(
                                        "strength",
                                        transform=lambda s: f"Signal: {s}%",
                                    ),
                                    css_classes=["network-connected-info"],
                                    halign="start",
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        )

    def _create_available_section(self, device) -> widgets.Box:
        """Create the available networks list section."""
        if not device:
            return widgets.Box(
                child=[
                    widgets.Label(
                        label="No WiFi adapter found",
                        css_classes=["network-no-device"],
                    )
                ]
            )

        return widgets.Box(
            orientation="vertical",
            spacing=8,
            css_classes=["network-available-section"],
            child=[
                widgets.Label(
                    label="Available Networks",
                    css_classes=["network-section-title"],
                    halign="start",
                ),
                widgets.ScrolledWindow(
                    min_content_height=200,
                    max_content_height=400,
                    child=widgets.Box(
                        orientation="vertical",
                        spacing=4,
                        css_classes=["network-list"],
                        child=device.bind(
                            "access_points",
                            transform=lambda aps: [
                                NetworkRow(ap) for ap in aps if not ap.is_connected
                            ],
                        ),
                    ),
                ),
            ],
        )
