import os
import json
import hashlib
from pathlib import Path
from typing import Optional
from PIL import Image
from gi.repository import GLib
import ignis


CACHE_DIR = os.path.join(ignis.CACHE_DIR, "wallpaper")
THUMBNAIL_DIR = os.path.join(CACHE_DIR, "thumbnails")
METADATA_FILE = os.path.join(CACHE_DIR, "metadata.json")
HISTORY_FILE = os.path.join(CACHE_DIR, "history.json")
CURRENT_WALLPAPER_LINK = os.path.join(CACHE_DIR, "current")

THUMBNAIL_SIZE = (256, 256)
MAX_HISTORY = 100


class WallpaperCache:
    """Manages caching of wallpaper thumbnails, metadata, and history."""

    def __init__(self):
        self._ensure_cache_dirs()
        self._metadata = self._load_metadata()
        self._history = self._load_history()

    def _ensure_cache_dirs(self) -> None:
        """Create cache directories if they don't exist."""
        os.makedirs(THUMBNAIL_DIR, exist_ok=True)

    def _load_metadata(self) -> dict:
        """Load metadata from disk."""
        if os.path.exists(METADATA_FILE):
            try:
                with open(METADATA_FILE, "r") as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return {}
        return {}

    def _save_metadata(self) -> None:
        """Save metadata to disk."""
        try:
            with open(METADATA_FILE, "w") as f:
                json.dump(self._metadata, f, indent=2)
        except IOError as e:
            print(f"Failed to save metadata: {e}")

    def _load_history(self) -> list[str]:
        """Load wallpaper history from disk."""
        if os.path.exists(HISTORY_FILE):
            try:
                with open(HISTORY_FILE, "r") as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return []
        return []

    def _save_history(self) -> None:
        """Save wallpaper history to disk."""
        try:
            with open(HISTORY_FILE, "w") as f:
                json.dump(self._history, f, indent=2)
        except IOError as e:
            print(f"Failed to save history: {e}")

    def _get_file_hash(self, filepath: str) -> str:
        """Generate a hash for a file path to use as cache key."""
        return hashlib.md5(filepath.encode()).hexdigest()

    def get_thumbnail_path(self, wallpaper_path: str) -> str:
        """Get the cached thumbnail path for a wallpaper."""
        file_hash = self._get_file_hash(wallpaper_path)
        return os.path.join(THUMBNAIL_DIR, f"{file_hash}.jpg")

    def generate_thumbnail(self, wallpaper_path: str) -> Optional[str]:
        """Generate and cache a thumbnail for a wallpaper.

        Returns the path to the thumbnail, or None if generation failed.
        """
        if not os.path.exists(wallpaper_path):
            return None

        thumbnail_path = self.get_thumbnail_path(wallpaper_path)

        # Return cached thumbnail if it exists and is newer than source
        if os.path.exists(thumbnail_path):
            if os.path.getmtime(thumbnail_path) >= os.path.getmtime(wallpaper_path):
                return thumbnail_path

        try:
            # Generate thumbnail
            with Image.open(wallpaper_path) as img:
                # Convert to RGB if needed (handles RGBA, grayscale, etc.)
                if img.mode != "RGB":
                    img = img.convert("RGB")

                # Create thumbnail maintaining aspect ratio
                img.thumbnail(THUMBNAIL_SIZE, Image.Resampling.LANCZOS)

                # Save as JPEG for smaller file size
                img.save(thumbnail_path, "JPEG", quality=85, optimize=True)

            return thumbnail_path
        except Exception as e:
            print(f"Failed to generate thumbnail for {wallpaper_path}: {e}")
            return None

    def get_metadata(self, wallpaper_path: str) -> dict:
        """Get or generate metadata for a wallpaper."""
        file_hash = self._get_file_hash(wallpaper_path)

        # Return cached metadata if file hasn't changed
        if file_hash in self._metadata:
            cached = self._metadata[file_hash]
            if os.path.exists(wallpaper_path):
                if cached.get("mtime") == os.path.getmtime(wallpaper_path):
                    return cached

        # Generate new metadata
        metadata = self._extract_metadata(wallpaper_path)
        if metadata:
            self._metadata[file_hash] = metadata
            self._save_metadata()

        return metadata or {}

    def _extract_metadata(self, wallpaper_path: str) -> Optional[dict]:
        """Extract metadata from a wallpaper file."""
        if not os.path.exists(wallpaper_path):
            return None

        try:
            stat = os.stat(wallpaper_path)
            with Image.open(wallpaper_path) as img:
                return {
                    "path": wallpaper_path,
                    "filename": os.path.basename(wallpaper_path),
                    "width": img.width,
                    "height": img.height,
                    "aspect_ratio": round(img.width / img.height, 2),
                    "format": img.format,
                    "mode": img.mode,
                    "size_bytes": stat.st_size,
                    "mtime": stat.st_mtime,
                }
        except Exception as e:
            print(f"Failed to extract metadata from {wallpaper_path}: {e}")
            return None

    def add_to_history(self, wallpaper_path: str) -> None:
        """Add a wallpaper to the history, maintaining max size."""
        # Remove if already in history
        if wallpaper_path in self._history:
            self._history.remove(wallpaper_path)

        # Add to front
        self._history.insert(0, wallpaper_path)

        # Trim to max size
        if len(self._history) > MAX_HISTORY:
            self._history = self._history[:MAX_HISTORY]

        self._save_history()

    def get_history(self) -> list[str]:
        """Get the wallpaper history list."""
        return self._history.copy()

    def get_previous_wallpaper(self, current_wallpaper: str) -> Optional[str]:
        """Get the previous wallpaper from history."""
        try:
            current_index = self._history.index(current_wallpaper)
            if current_index < len(self._history) - 1:
                return self._history[current_index + 1]
        except (ValueError, IndexError):
            pass

        # If current not in history or is last, return None
        return None

    def set_current_wallpaper(self, wallpaper_path: str) -> None:
        """Update the current wallpaper symlink."""
        if os.path.exists(CURRENT_WALLPAPER_LINK) or os.path.islink(CURRENT_WALLPAPER_LINK):
            os.unlink(CURRENT_WALLPAPER_LINK)

        if os.path.exists(wallpaper_path):
            os.symlink(wallpaper_path, CURRENT_WALLPAPER_LINK)

    def get_current_wallpaper(self) -> Optional[str]:
        """Get the current wallpaper path from symlink."""
        if os.path.islink(CURRENT_WALLPAPER_LINK):
            try:
                return os.readlink(CURRENT_WALLPAPER_LINK)
            except OSError:
                pass
        return None

    def clear_cache(self) -> None:
        """Clear all cached data."""
        # Clear thumbnails
        for file in Path(THUMBNAIL_DIR).glob("*.jpg"):
            try:
                file.unlink()
            except OSError:
                pass

        # Clear metadata and history
        self._metadata = {}
        self._history = []
        self._save_metadata()
        self._save_history()

        # Clear current wallpaper link
        if os.path.exists(CURRENT_WALLPAPER_LINK) or os.path.islink(CURRENT_WALLPAPER_LINK):
            try:
                os.unlink(CURRENT_WALLPAPER_LINK)
            except OSError:
                pass
