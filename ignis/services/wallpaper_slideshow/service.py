import os
import random
import asyncio
from pathlib import Path
from typing import Optional
from gi.repository import GLib, Gio, GObject
from ignis.base_service import BaseService
from ignis.services.wallpaper import WallpaperService
from ignis.options import options
from ignis import utils
from user_options import user_options
from .cache import WallpaperCache


# Supported image extensions
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".gif", ".tiff", ".tif"}

# Map shader names to swww transition types
SHADER_TO_SWWW = {
    "fade": "fade",
    "slide": "left",
    "zoom": "grow",
    "pixelate": "fade",  # swww doesn't have pixelate, use fade
    "swirl": "wave",
    "wipe": "wipe",
}


class WallpaperSlideshowService(BaseService):
    """Service for managing wallpaper slideshow with folder monitoring."""

    __gsignals__ = {
        "wallpaper-changed": (GObject.SignalFlags.RUN_FIRST, GObject.TYPE_NONE, (str,)),
        "slideshow-state-changed": (GObject.SignalFlags.RUN_FIRST, GObject.TYPE_NONE, (bool,)),
        "queue-updated": (GObject.SignalFlags.RUN_FIRST, GObject.TYPE_NONE, ()),
    }

    def __init__(self):
        super().__init__()

        self._cache = WallpaperCache()
        self._wallpaper_service = WallpaperService.get_default()

        # Slideshow state
        self._folder_path: Optional[str] = None
        self._wallpaper_queue: list[str] = []
        self._current_index: int = 0
        self._is_playing: bool = False
        self._timer_id: Optional[int] = None

        # Folder monitoring
        self._folder_monitor: Optional[Gio.FileMonitor] = None

    # Properties
    @GObject.Property
    def current_wallpaper(self) -> str:
        """Get the current wallpaper path."""
        return self._cache.get_current_wallpaper() or ""

    @GObject.Property
    def is_playing(self) -> bool:
        """Check if slideshow is currently playing."""
        return self._is_playing

    @GObject.Property
    def queue_length(self) -> int:
        """Get the number of wallpapers in the queue."""
        return len(self._wallpaper_queue)

    @GObject.Property
    def current_index(self) -> int:
        """Get the current position in the queue."""
        return self._current_index

    @GObject.Property
    def next_wallpaper_preview(self) -> str:
        """Get the next wallpaper in queue without switching to it."""
        if not self._wallpaper_queue:
            return ""
        next_index = (self._current_index + 1) % len(self._wallpaper_queue)
        return self._wallpaper_queue[next_index]

    # Public methods
    def set_folder(self, folder_path: str, shuffle: bool = True) -> bool:
        """Set the folder to monitor for wallpapers.

        Args:
            folder_path: Path to the folder containing wallpapers
            shuffle: Whether to shuffle the wallpaper queue

        Returns:
            True if folder was set successfully
        """
        if not os.path.isdir(folder_path):
            print(f"Invalid folder path: {folder_path}")
            return False

        self._folder_path = folder_path
        self._load_wallpapers_from_folder(shuffle)
        self._setup_folder_monitor()

        return True

    def set_wallpaper(self, wallpaper_path: str, update_material: bool = True) -> bool:
        """Set a specific wallpaper.

        Args:
            wallpaper_path: Path to the wallpaper image
            update_material: Whether to regenerate Material You colors

        Returns:
            True if wallpaper was set successfully
        """
        if not os.path.exists(wallpaper_path):
            print(f"Wallpaper not found: {wallpaper_path}")
            return False

        # Set wallpaper using swww with transition
        self._set_wallpaper_with_swww(wallpaper_path)

        # Update cache
        self._cache.set_current_wallpaper(wallpaper_path)
        self._cache.add_to_history(wallpaper_path)

        # Generate thumbnail asynchronously
        GLib.idle_add(lambda: self._cache.generate_thumbnail(wallpaper_path))

        # Emit signal
        self.emit("wallpaper-changed", wallpaper_path)
        self.notify("current-wallpaper")

        # Update MaterialService if requested
        if update_material:
            self._update_material_colors(wallpaper_path)

        return True

    def next_wallpaper(self) -> bool:
        """Switch to the next wallpaper in the queue."""
        if not self._wallpaper_queue:
            return False

        self._current_index = (self._current_index + 1) % len(self._wallpaper_queue)
        wallpaper = self._wallpaper_queue[self._current_index]

        return self.set_wallpaper(wallpaper)

    def previous_wallpaper(self) -> bool:
        """Switch to the previous wallpaper (from history)."""
        current = self.current_wallpaper
        if not current:
            return False

        previous = self._cache.get_previous_wallpaper(current)
        if not previous:
            # If no previous in history, go back in queue
            if not self._wallpaper_queue:
                return False
            self._current_index = (self._current_index - 1) % len(self._wallpaper_queue)
            previous = self._wallpaper_queue[self._current_index]

        return self.set_wallpaper(previous)

    def play_slideshow(self, interval_seconds: int) -> None:
        """Start the slideshow timer.

        Args:
            interval_seconds: Interval between wallpaper changes in seconds
        """
        if self._is_playing:
            self.pause_slideshow()

        if not self._wallpaper_queue:
            print("No wallpapers in queue")
            return

        self._is_playing = True
        self._timer_id = GLib.timeout_add_seconds(
            interval_seconds,
            self._on_timer_tick
        )

        self.emit("slideshow-state-changed", True)
        self.notify("is-playing")

    def pause_slideshow(self) -> None:
        """Pause the slideshow timer."""
        if self._timer_id is not None:
            GLib.source_remove(self._timer_id)
            self._timer_id = None

        self._is_playing = False

        self.emit("slideshow-state-changed", False)
        self.notify("is-playing")

    def toggle_playback(self, interval_seconds: int = 300) -> None:
        """Toggle slideshow playback."""
        if self._is_playing:
            self.pause_slideshow()
        else:
            self.play_slideshow(interval_seconds)

    def shuffle_queue(self) -> None:
        """Shuffle the wallpaper queue."""
        if self._wallpaper_queue:
            # Remember current wallpaper
            current = None
            if 0 <= self._current_index < len(self._wallpaper_queue):
                current = self._wallpaper_queue[self._current_index]

            # Shuffle
            random.shuffle(self._wallpaper_queue)

            # Find new index of current wallpaper
            if current and current in self._wallpaper_queue:
                self._current_index = self._wallpaper_queue.index(current)
            else:
                self._current_index = 0

            self.emit("queue-updated")
            self.notify("queue-length")

    def get_queue(self) -> list[str]:
        """Get a copy of the current wallpaper queue."""
        return self._wallpaper_queue.copy()

    def get_history(self) -> list[str]:
        """Get the wallpaper history."""
        return self._cache.get_history()

    def reload_folder(self, shuffle: bool = False) -> None:
        """Reload wallpapers from the current folder."""
        if self._folder_path:
            self._load_wallpapers_from_folder(shuffle)

    # Private methods
    def _set_wallpaper_with_swww(self, wallpaper_path: str) -> None:
        """Set wallpaper using swww with transition effects.

        Args:
            wallpaper_path: Path to the wallpaper image
        """
        # Get transition settings from user options
        transition_shader = user_options.wallpaper_slideshow.transition_shader
        transition_type = SHADER_TO_SWWW.get(transition_shader, "fade")

        # Duration is fixed at 1 second for now (transition_duration removed from UI)
        duration = 1.0

        # Build swww command
        cmd = [
            "swww", "img",
            wallpaper_path,
            "--transition-type", transition_type,
            "--transition-duration", str(duration),
            "--transition-fps", "60",
        ]

        # Add angle for wipe/wave transitions
        if transition_type in ["wipe", "wave"]:
            cmd.extend(["--transition-angle", "45"])

        # Execute swww command asynchronously
        asyncio.create_task(self._exec_swww(cmd, wallpaper_path))

    async def _exec_swww(self, cmd: list[str], wallpaper_path: str) -> None:
        """Execute swww command asynchronously.

        Args:
            cmd: Command to execute
            wallpaper_path: Wallpaper path (for updating options after)
        """
        try:
            await utils.exec_sh_async(" ".join(cmd))
            # Update options after swww sets the wallpaper
            options.wallpaper.set_wallpaper_path(wallpaper_path)
        except Exception as e:
            print(f"Failed to set wallpaper with swww: {e}")
            # Fallback to direct setting
            options.wallpaper.set_wallpaper_path(wallpaper_path)

    def _load_wallpapers_from_folder(self, shuffle: bool = True) -> None:
        """Load all wallpapers from the monitored folder."""
        if not self._folder_path:
            return

        wallpapers = []

        try:
            for file_path in Path(self._folder_path).iterdir():
                if file_path.is_file() and file_path.suffix.lower() in IMAGE_EXTENSIONS:
                    wallpapers.append(str(file_path.absolute()))
        except OSError as e:
            print(f"Error reading folder {self._folder_path}: {e}")
            return

        if not wallpapers:
            print(f"No wallpapers found in {self._folder_path}")
            return

        # Sort for consistent order before shuffling
        wallpapers.sort()

        if shuffle:
            random.shuffle(wallpapers)

        self._wallpaper_queue = wallpapers
        self._current_index = 0

        print(f"Loaded {len(wallpapers)} wallpapers from {self._folder_path}")

        self.emit("queue-updated")
        self.notify("queue-length")
        self.notify("current-index")

    def _setup_folder_monitor(self) -> None:
        """Set up file monitoring for the wallpaper folder."""
        # Remove existing monitor
        if self._folder_monitor:
            self._folder_monitor.cancel()
            self._folder_monitor = None

        if not self._folder_path:
            return

        try:
            folder = Gio.File.new_for_path(self._folder_path)
            self._folder_monitor = folder.monitor_directory(
                Gio.FileMonitorFlags.NONE,
                None
            )
            self._folder_monitor.connect("changed", self._on_folder_changed)

            print(f"Monitoring folder: {self._folder_path}")
        except Exception as e:
            print(f"Failed to monitor folder {self._folder_path}: {e}")

    def _on_folder_changed(
        self,
        monitor: Gio.FileMonitor,
        file: Gio.File,
        other_file: Optional[Gio.File],
        event_type: Gio.FileMonitorEvent
    ) -> None:
        """Handle folder change events."""
        # Only reload on created/deleted events
        if event_type in (
            Gio.FileMonitorEvent.CREATED,
            Gio.FileMonitorEvent.DELETED,
            Gio.FileMonitorEvent.MOVED_IN,
            Gio.FileMonitorEvent.MOVED_OUT,
        ):
            # Debounce reloads
            GLib.idle_add(lambda: self._load_wallpapers_from_folder(shuffle=False))

    def _on_timer_tick(self) -> bool:
        """Handle slideshow timer tick."""
        self.next_wallpaper()
        return True  # Continue timer

    def _update_material_colors(self, wallpaper_path: str) -> None:
        """Trigger Material You color generation for a wallpaper."""
        try:
            from services.material import MaterialService
            material = MaterialService.get_default()

            # This will regenerate colors and reload CSS
            GLib.idle_add(lambda: material.generate_colors(wallpaper_path))
        except ImportError:
            print("MaterialService not available")
        except Exception as e:
            print(f"Failed to update material colors: {e}")
