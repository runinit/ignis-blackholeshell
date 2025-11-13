"""
Color Scheme Manager - handles both built-in palettes and dynamic generation.
"""

import os
import json
from typing import Optional
from gi.repository import GObject
from ignis.base_service import BaseService
from ignis import utils
from .matugen_service import MatugenService


class ColorSchemeService(BaseService):
    """Manage color schemes for Blackhole Shell."""

    __gsignals__ = {
        "scheme-changed": (GObject.SignalFlags.RUN_FIRST, GObject.TYPE_NONE, ()),
    }

    def __init__(self):
        super().__init__()
        self._matugen = MatugenService()
        self._current_scheme_name = "Rose Pine"
        self._use_wallpaper_colors = False
        self._current_colors = {}
        self._built_in_schemes = {}
        self._palettes_dir = os.path.join(
            utils.get_current_dir(), "services", "material", "palettes"
        )

        # Load built-in schemes
        self._load_built_in_schemes()

        # Load initial scheme
        self._load_scheme()

    @GObject.Property
    def scheme_name(self) -> str:
        """Current color scheme name."""
        return self._current_scheme_name

    @GObject.Property
    def use_wallpaper_colors(self) -> bool:
        """Whether to use wallpaper-based color generation."""
        return self._use_wallpaper_colors

    @use_wallpaper_colors.setter
    def use_wallpaper_colors(self, value: bool) -> None:
        """Toggle between built-in and wallpaper-based colors."""
        if self._use_wallpaper_colors != value:
            self._use_wallpaper_colors = value
            self._load_scheme()
            self.notify("use-wallpaper-colors")

    @GObject.Property
    def available_schemes(self) -> list[str]:
        """List of available built-in color schemes."""
        return sorted(list(self._built_in_schemes.keys()))

    @GObject.Property
    def current_colors(self) -> dict[str, str]:
        """Current active color palette."""
        return self._current_colors

    @GObject.Property
    def matugen_scheme_type(self) -> str:
        """Current matugen scheme type for wallpaper generation."""
        return self._matugen.scheme_type

    @matugen_scheme_type.setter
    def matugen_scheme_type(self, value: str) -> None:
        """Set matugen scheme type and regenerate if using wallpaper colors."""
        self._matugen.scheme_type = value
        # Don't auto-regenerate, wait for explicit wallpaper change
        self.notify("matugen-scheme-type")

    def set_scheme(self, scheme_name: str) -> None:
        """
        Set active color scheme (built-in only).

        Args:
            scheme_name: Name of built-in scheme (e.g., "Rose Pine")
        """
        if scheme_name in self._built_in_schemes:
            self._current_scheme_name = scheme_name
            self._use_wallpaper_colors = False
            self._load_scheme()
            self.notify("scheme-name")
            self.notify("use-wallpaper-colors")
        else:
            print(f"Color scheme '{scheme_name}' not found")

    def generate_from_wallpaper(
        self, wallpaper_path: str, dark_mode: bool = True
    ) -> None:
        """
        Generate color scheme from wallpaper using matugen.

        Args:
            wallpaper_path: Path to wallpaper image
            dark_mode: Generate dark or light palette
        """
        self._use_wallpaper_colors = True
        colors = self._matugen.generate_from_image(wallpaper_path, dark_mode)

        if colors:
            self._current_colors = colors
            self.emit("scheme-changed")
            self.notify("current-colors")
            self.notify("use-wallpaper-colors")
        else:
            print("Failed to generate colors from wallpaper, keeping current scheme")

    def _load_built_in_schemes(self) -> None:
        """Load all built-in color scheme JSON files."""
        if not os.path.exists(self._palettes_dir):
            print(f"Palettes directory not found: {self._palettes_dir}")
            return

        for filename in os.listdir(self._palettes_dir):
            if filename.endswith(".json"):
                filepath = os.path.join(self._palettes_dir, filename)
                try:
                    with open(filepath, "r") as f:
                        data = json.load(f)
                        scheme_name = data.get("name", filename[:-5])

                        # Store scheme data
                        self._built_in_schemes[scheme_name] = data

                except (json.JSONDecodeError, IOError) as e:
                    print(f"Failed to load palette {filename}: {e}")

    def _load_scheme(self) -> None:
        """Load current color scheme based on settings."""
        if self._use_wallpaper_colors:
            # Load cached wallpaper colors from matugen
            self._current_colors = self._matugen._load_cache()

            # If no cache, fall back to built-in scheme
            if not self._current_colors:
                print("No cached wallpaper colors, falling back to built-in scheme")
                self._use_wallpaper_colors = False
                self._load_built_in_scheme()
        else:
            self._load_built_in_scheme()

        self.emit("scheme-changed")
        self.notify("current-colors")

    def _load_built_in_scheme(self) -> None:
        """Load the currently selected built-in color scheme."""
        scheme_data = self._built_in_schemes.get(self._current_scheme_name)

        if scheme_data:
            self._current_colors = scheme_data.get("colors", {})
        else:
            # Fallback to first available scheme
            if self._built_in_schemes:
                first_scheme = next(iter(self._built_in_schemes.keys()))
                print(
                    f"Scheme '{self._current_scheme_name}' not found, using '{first_scheme}'"
                )
                self._current_scheme_name = first_scheme
                scheme_data = self._built_in_schemes[first_scheme]
                self._current_colors = scheme_data.get("colors", {})
            else:
                print("No built-in color schemes available")
                self._current_colors = {}

    def get_scheme_info(self, scheme_name: str) -> Optional[dict]:
        """
        Get information about a built-in color scheme.

        Args:
            scheme_name: Name of the scheme

        Returns:
            Scheme metadata (name, variant, description, etc.) or None
        """
        scheme = self._built_in_schemes.get(scheme_name)
        if scheme:
            return {
                "name": scheme.get("name"),
                "variant": scheme.get("variant"),
                "description": scheme.get("description"),
                "dark_mode": scheme.get("dark_mode"),
                "source": scheme.get("source"),
            }
        return None
