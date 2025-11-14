"""
OSD Module - Initialize Volume and Brightness OSDs (Phase 4).

Replaces the old single OSD window with modern, separate Volume and Brightness OSDs.
"""

from ignis import utils
from .volume_osd import VolumeOSD
from .brightness_osd import BrightnessOSD


class OSD:
    """OSD initializer that creates Volume and Brightness OSDs for all monitors."""

    def __init__(self):
        """Initialize Volume and Brightness OSDs for all monitors."""
        # Create Volume OSD for each monitor
        for monitor in range(utils.get_n_monitors()):
            VolumeOSD(monitor)

        # Create Brightness OSD for each monitor
        for monitor in range(utils.get_n_monitors()):
            BrightnessOSD(monitor)
