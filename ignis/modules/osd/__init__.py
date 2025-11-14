"""
OSD (On-Screen Display) Module - Phase 4.

Provides modern OSD windows for volume, brightness, and other system notifications
with Noctalia-inspired design and smooth animations.
"""

from .osd import OSD
from .osd_window import OSDWindow
from .volume_osd import VolumeOSD
from .brightness_osd import BrightnessOSD

__all__ = ["OSD", "OSDWindow", "VolumeOSD", "BrightnessOSD"]
