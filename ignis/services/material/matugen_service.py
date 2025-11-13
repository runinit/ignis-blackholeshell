"""
Matugen-based color generation service.
Replaces materialyoucolor for wallpaper-based palette generation.
"""

import subprocess
import json
import os
from typing import Optional
from gi.repository import GObject
from ignis.base_service import BaseService
from ignis import CACHE_DIR


class MatugenService(BaseService):
    """Generate Material Design 3 color palettes using matugen."""

    def __init__(self):
        super().__init__()
        self._cache_file = os.path.join(CACHE_DIR, "matugen_colors.json")
        self._template_file = os.path.join(CACHE_DIR, "matugen_output.json")
        self._scheme_type = "tonal-spot"  # Default scheme

    @GObject.Property
    def scheme_type(self) -> str:
        """Current matugen scheme type."""
        return self._scheme_type

    @scheme_type.setter
    def scheme_type(self, value: str) -> None:
        """Set matugen scheme type (tonal-spot, vibrant, etc.)."""
        valid_schemes = [
            "tonal-spot",
            "vibrant",
            "expressive",
            "neutral",
            "monochrome",
            "fidelity",
            "content",
            "fruit-salad",
            "rainbow",
        ]
        if value in valid_schemes:
            self._scheme_type = value
            self.notify("scheme-type")

    def generate_from_image(
        self, image_path: str, dark_mode: bool = True
    ) -> dict[str, str]:
        """
        Generate color palette from image using matugen.

        Args:
            image_path: Path to wallpaper image
            dark_mode: Generate dark or light palette

        Returns:
            Dictionary of Material Design 3 color tokens
        """
        # Check if matugen is available
        if not self._check_matugen_available():
            print("Matugen not found, loading from cache")
            return self._load_cache()

        try:
            # Run matugen with JSON output
            result = subprocess.run(
                [
                    "matugen",
                    "image",
                    image_path,
                    "--json",
                    "hex",
                    "--type",
                    self._scheme_type,
                    "--mode",
                    "dark" if dark_mode else "light",
                ],
                capture_output=True,
                text=True,
                check=True,
                timeout=10,  # 10 second timeout
            )

            # Parse matugen JSON output
            matugen_data = json.loads(result.stdout)

            # Save full output for template system
            self._save_template_data(matugen_data)

            # Extract and flatten colors
            colors = self._extract_colors(matugen_data, dark_mode)

            # Cache the result
            self._save_cache(colors)

            return colors

        except subprocess.CalledProcessError as e:
            print(f"Matugen generation failed: {e.stderr}")
            return self._load_cache()
        except subprocess.TimeoutExpired:
            print("Matugen generation timed out")
            return self._load_cache()
        except json.JSONDecodeError as e:
            print(f"Failed to parse matugen output: {e}")
            return self._load_cache()
        except FileNotFoundError:
            print("Matugen executable not found")
            return self._load_cache()

    def generate_from_color(
        self, color: str, dark_mode: bool = True
    ) -> dict[str, str]:
        """
        Generate color palette from a single color using matugen.

        Args:
            color: Hex color string (e.g., "#c4a7e7")
            dark_mode: Generate dark or light palette

        Returns:
            Dictionary of Material Design 3 color tokens
        """
        if not self._check_matugen_available():
            print("Matugen not found, loading from cache")
            return self._load_cache()

        try:
            # Run matugen with color input
            result = subprocess.run(
                [
                    "matugen",
                    "color",
                    color,
                    "--json",
                    "hex",
                    "--type",
                    self._scheme_type,
                    "--mode",
                    "dark" if dark_mode else "light",
                ],
                capture_output=True,
                text=True,
                check=True,
                timeout=10,
            )

            matugen_data = json.loads(result.stdout)
            self._save_template_data(matugen_data)
            colors = self._extract_colors(matugen_data, dark_mode)
            self._save_cache(colors)

            return colors

        except (subprocess.CalledProcessError, json.JSONDecodeError, FileNotFoundError, subprocess.TimeoutExpired) as e:
            print(f"Matugen color generation failed: {e}")
            return self._load_cache()

    def _extract_colors(self, matugen_data: dict, dark_mode: bool) -> dict[str, str]:
        """
        Extract and flatten matugen color structure.

        Matugen format: {"colors": {"dark": {"primary": {"hex": "#..."}}}}
        Our format: flat dictionary with underscored keys
        """
        mode = "dark" if dark_mode else "light"

        # Try to get colors from the correct mode
        colors_obj = matugen_data.get("colors", {}).get(mode, {})

        if not colors_obj:
            print(f"No colors found for mode '{mode}' in matugen output")
            return {}

        # Flatten nested structure
        flat_colors = {}
        for key, value in colors_obj.items():
            if isinstance(value, dict) and "hex" in value:
                # Convert camelCase to snake_case for consistency
                snake_key = self._camel_to_snake(key)
                flat_colors[snake_key] = value["hex"]

        return flat_colors

    def _camel_to_snake(self, name: str) -> str:
        """Convert camelCase to snake_case."""
        import re

        # Insert underscore before uppercase letters
        s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
        # Insert underscore before sequences of uppercase followed by lowercase
        return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()

    def _save_cache(self, colors: dict[str, str]) -> None:
        """Save generated colors to cache file."""
        os.makedirs(os.path.dirname(self._cache_file), exist_ok=True)
        with open(self._cache_file, "w") as f:
            json.dump(colors, f, indent=2)

    def _load_cache(self) -> dict[str, str]:
        """Load colors from cache file."""
        if os.path.exists(self._cache_file):
            try:
                with open(self._cache_file, "r") as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Failed to load cache: {e}")
        return {}

    def _save_template_data(self, matugen_data: dict) -> None:
        """
        Save full matugen output for template system.
        This file can be used by external apps via matugen templates.
        """
        os.makedirs(os.path.dirname(self._template_file), exist_ok=True)
        with open(self._template_file, "w") as f:
            json.dump(matugen_data, f, indent=2)

    def _check_matugen_available(self) -> bool:
        """Check if matugen is installed and available."""
        try:
            result = subprocess.run(
                ["matugen", "--version"],
                capture_output=True,
                text=True,
                timeout=2,
            )
            return result.returncode == 0
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return False
