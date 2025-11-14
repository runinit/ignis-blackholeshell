"""
Control Center Panels - Sub-panels for detailed settings (Phase 3).

This module contains individual panels for Calendar, Audio, Network (WiFi),
and Bluetooth settings accessible from the Control Center.
"""

from .base import Panel
from .calendar import CalendarPanel
from .audio import AudioPanel
from .network import NetworkPanel
from .bluetooth import BluetoothPanel

__all__ = ["Panel", "CalendarPanel", "AudioPanel", "NetworkPanel", "BluetoothPanel"]
