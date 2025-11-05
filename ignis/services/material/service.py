#!/usr/bin/python
import os
import asyncio
import json
import subprocess
import shutil
from gi.repository import GLib  # type: ignore
from jinja2 import Template

from ignis import utils
from ignis.css_manager import CssManager
from ignis.base_service import BaseService
from ignis.options import options
from user_options import user_options

from .constants import MATERIAL_CACHE_DIR, TEMPLATES, SAMPLE_WALL

css_manager = CssManager.get_default()

# Default colors file (pre-generated with matugen, committed to repo)
DEFAULT_COLORS_FILE = os.path.join(os.path.dirname(__file__), "default_colors.json")
# Runtime cache file (user-specific wallpaper colors)
RUNTIME_CACHE_FILE = os.path.join(MATERIAL_CACHE_DIR, "wallpaper_colors.json")


class MaterialService(BaseService):
    """Material You color generation service using matugen 3.0"""

    def __init__(self):
        super().__init__()

        # Try to load colors from cache (fast path)
        if user_options.material.colors == {}:
            self.__load_colors_from_cache()

        # Set default wallpaper if none set
        if not options.wallpaper.wallpaper_path:
            options.wallpaper.set_wallpaper_path(SAMPLE_WALL)

        # Connect to dark mode changes
        user_options.material.connect_option(
            "dark_mode", lambda: self.__on_dark_mode_changed()
        )

        # Apply GTK theme and fonts on startup
        asyncio.create_task(self.__reload_gtk_theme())

    def __load_colors_from_cache(self) -> None:
        """Load colors from cache - tries runtime cache first, then defaults"""
        # First try runtime cache (user's wallpaper)
        if os.path.exists(RUNTIME_CACHE_FILE):
            try:
                with open(RUNTIME_CACHE_FILE) as f:
                    cache_data = json.load(f)
                    mode_key = "dark_mode" if user_options.material.dark_mode else "light_mode"
                    user_options.material.colors = cache_data.get(mode_key, {})
                    if user_options.material.colors:
                        return  # Successfully loaded from runtime cache
            except Exception:
                pass  # Fall through to defaults

        # Fall back to default colors (sample wallpaper)
        try:
            with open(DEFAULT_COLORS_FILE) as f:
                cache_data = json.load(f)
                mode_key = "dark_mode" if user_options.material.dark_mode else "light_mode"
                user_options.material.colors = cache_data.get(mode_key, {})
        except Exception:
            # Last resort: generate colors for sample wallpaper
            self.generate_colors(SAMPLE_WALL)

    def __on_dark_mode_changed(self) -> None:
        """Handle dark mode toggle - reload from cache if possible"""
        self.__load_colors_from_cache()
        # Reload CSS with new colors
        css_manager.reload_all_css()

    def get_colors_from_img(self, path: str, dark_mode: bool) -> dict[str, str]:
        """Generate Material You colors from image using matugen - EXPENSIVE, use sparingly!"""
        try:
            # Run matugen to generate colors with user-selected palette type
            mode = "dark" if dark_mode else "light"
            palette = user_options.material.palette_type
            result = subprocess.run(
                ["matugen", "image", path, "--json", "hex", "--mode", mode, "--type", palette, "--dry-run"],
                capture_output=True,
                text=True,
                check=True,
            )

            # Parse JSON output
            data = json.loads(result.stdout)

            # Extract and flatten colors for template use
            return self._flatten_matugen_colors(data, dark_mode)

        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"matugen failed: {e.stderr}")
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Failed to parse matugen output: {e}")

    def _snake_to_camel(self, snake_str: str) -> str:
        """Convert snake_case to camelCase"""
        components = snake_str.split('_')
        return components[0] + ''.join(x.title() for x in components[1:])

    def _flatten_matugen_colors(self, data: dict, dark_mode: bool) -> dict[str, str]:
        """Flatten matugen JSON output to match template format - outputs camelCase keys for SCSS"""
        colors = data.get("colors", {})
        palettes = data.get("palettes", {})

        # Get the mode key for nested colors
        mode = "dark" if dark_mode else "light"

        # Flatten nested color structure with camelCase keys
        flattened = {}

        # Extract main colors and convert to camelCase
        for color_name, color_data in colors.items():
            camel_key = self._snake_to_camel(color_name)
            if isinstance(color_data, dict):
                flattened[camel_key] = color_data.get(mode, color_data.get("default", "#000000"))
            else:
                flattened[camel_key] = color_data

        # Add palette key colors (using tone 40 for light, 80 for dark)
        tone = 80 if dark_mode else 40
        for palette_name, palette_data in palettes.items():
            key_color = palette_data.get(str(tone), "#000000")
            # Keep paletteKeyColor suffix as-is, convert the prefix to camelCase
            camel_prefix = self._snake_to_camel(palette_name)
            flattened[f"{camel_prefix}PaletteKeyColor"] = key_color

        # Add dark mode flag for SCSS
        flattened["darkmode"] = str(dark_mode).lower()

        return flattened

    def generate_colors(self, path: str) -> None:
        """Generate colors from wallpaper and save to runtime cache"""
        # Generate both light and dark mode colors
        light_colors = self.get_colors_from_img(path, dark_mode=False)
        dark_colors = self.get_colors_from_img(path, dark_mode=True)

        # Use appropriate colors for current mode
        colors = dark_colors if user_options.material.dark_mode else light_colors
        user_options.material.colors = colors

        # Save to runtime cache for future startups
        self.__save_to_cache(path, light_colors, dark_colors)

        # Render templates
        self.__render_templates(light_colors, dark_colors)
        asyncio.create_task(self.__setup(path))

    def __save_to_cache(self, wallpaper_path: str, light_colors: dict, dark_colors: dict) -> None:
        """Save generated colors to runtime cache"""
        try:
            cache_data = {
                "version": "2.0",  # Changed version to indicate matugen format
                "generator": "matugen-3.0",
                "wallpaper_path": wallpaper_path,
                "light_mode": light_colors,
                "dark_mode": dark_colors,
            }
            with open(RUNTIME_CACHE_FILE, "w") as f:
                json.dump(cache_data, f, indent=2)
        except Exception:
            pass  # Non-critical if cache fails to save

    def __render_templates(self, colors: dict, dark_colors: dict) -> None:
        for template in os.listdir(TEMPLATES):
            self.render_template(
                colors=colors,
                dark_mode=user_options.material.dark_mode,
                input_file=f"{TEMPLATES}/{template}",
                output_file=f"{MATERIAL_CACHE_DIR}/{template}",
            )

        for template in os.listdir(TEMPLATES):
            self.render_template(
                colors=dark_colors,
                dark_mode=True,
                input_file=f"{TEMPLATES}/{template}",
                output_file=f"{MATERIAL_CACHE_DIR}/dark_{template}",
            )

    def render_template(
        self,
        colors: dict,
        input_file: str,
        output_file: str,
        dark_mode: bool | None = None,
    ) -> None:
        if dark_mode is None:
            colors["dark_mode"] = str(user_options.material.dark_mode).lower()
        else:
            colors["dark_mode"] = str(dark_mode).lower()

        with open(input_file) as file:
            template_rendered = Template(file.read()).render(colors)

        with open(output_file, "w") as file:
            file.write(template_rendered)

    async def __reload_gtk_theme(self) -> None:
        # GTK theme commands
        THEME_CMD = "gsettings set org.gnome.desktop.interface gtk-theme {}"
        COLOR_SCHEME_CMD = "gsettings set org.gnome.desktop.interface color-scheme {}"
        ICON_THEME_CMD = "gsettings set org.gnome.desktop.interface icon-theme {}"

        # Font configuration commands
        FONT_CMD = "gsettings set org.gnome.desktop.interface font-name {}"
        DOCUMENT_FONT_CMD = "gsettings set org.gnome.desktop.interface document-font-name {}"
        MONOSPACE_FONT_CMD = "gsettings set org.gnome.desktop.interface monospace-font-name {}"

        # Font antialiasing and hinting
        FONT_ANTIALIASING_CMD = "gsettings set org.gnome.desktop.interface font-antialiasing {}"
        FONT_HINTING_CMD = "gsettings set org.gnome.desktop.interface font-hinting {}"

        # Set color scheme based on dark_mode
        color_scheme = "prefer-dark" if user_options.material.dark_mode else "prefer-light"

        # Apply GTK theme
        await utils.exec_sh_async(THEME_CMD.format("Adwaita"))
        await utils.exec_sh_async(THEME_CMD.format("Material"))
        await utils.exec_sh_async(COLOR_SCHEME_CMD.format(color_scheme))

        # Apply icon theme (Adwaita is default, but you can change this)
        await utils.exec_sh_async(ICON_THEME_CMD.format("Adwaita"))

        # Apply fonts from user settings
        interface_font = f"'{user_options.material.interface_font} {user_options.material.interface_font_size}'"
        document_font = f"'{user_options.material.document_font} {user_options.material.document_font_size}'"
        monospace_font = f"'{user_options.material.monospace_font} {user_options.material.monospace_font_size}'"

        await utils.exec_sh_async(FONT_CMD.format(interface_font))
        await utils.exec_sh_async(DOCUMENT_FONT_CMD.format(document_font))
        await utils.exec_sh_async(MONOSPACE_FONT_CMD.format(monospace_font))

        # Font rendering (rgba for subpixel antialiasing, slight hinting)
        await utils.exec_sh_async(FONT_ANTIALIASING_CMD.format("'rgba'"))
        await utils.exec_sh_async(FONT_HINTING_CMD.format("'slight'"))

        # Copy theme files to application config directories
        home = os.path.expanduser("~")

        # GTK 3.0 & 4.0
        if user_options.material.theme_gtk:
            gtk4_dir = os.path.join(home, ".config", "gtk-4.0")
            os.makedirs(gtk4_dir, exist_ok=True)
            shutil.copy(
                os.path.join(MATERIAL_CACHE_DIR, "gtk.css"),
                os.path.join(gtk4_dir, "gtk.css")
            )

            gtk3_dir = os.path.join(home, ".config", "gtk-3.0")
            os.makedirs(gtk3_dir, exist_ok=True)
            shutil.copy(
                os.path.join(MATERIAL_CACHE_DIR, "gtk.css"),
                os.path.join(gtk3_dir, "gtk.css")
            )

        # Qt5/Qt6
        if user_options.material.theme_qt:
            qt_config = os.path.join(MATERIAL_CACHE_DIR, "qt5ct.conf")
            if os.path.exists(qt_config):
                qt5ct_dir = os.path.join(home, ".config", "qt5ct")
                os.makedirs(qt5ct_dir, exist_ok=True)
                shutil.copy(qt_config, os.path.join(qt5ct_dir, "qt5ct.conf"))

                qt6ct_dir = os.path.join(home, ".config", "qt6ct")
                os.makedirs(qt6ct_dir, exist_ok=True)
                shutil.copy(qt_config, os.path.join(qt6ct_dir, "qt6ct.conf"))

        # Ghostty
        if user_options.material.theme_ghostty:
            ghostty_theme = os.path.join(MATERIAL_CACHE_DIR, "ghostty")
            if os.path.exists(ghostty_theme):
                ghostty_dir = os.path.join(home, ".config", "ghostty")
                os.makedirs(ghostty_dir, exist_ok=True)
                shutil.copy(ghostty_theme, os.path.join(ghostty_dir, "theme"))

        # Fuzzel
        if user_options.material.theme_fuzzel:
            fuzzel_config = os.path.join(MATERIAL_CACHE_DIR, "fuzzel.ini")
            if os.path.exists(fuzzel_config):
                fuzzel_dir = os.path.join(home, ".config", "fuzzel")
                os.makedirs(fuzzel_dir, exist_ok=True)
                shutil.copy(fuzzel_config, os.path.join(fuzzel_dir, "fuzzel.ini"))

        # Niri switcher
        if user_options.material.theme_niri:
            niri_config = os.path.join(MATERIAL_CACHE_DIR, "niri-styleswitcher.toml")
            if os.path.exists(niri_config):
                niri_dir = os.path.join(home, ".config", "niri")
                os.makedirs(niri_dir, exist_ok=True)
                shutil.copy(niri_config, os.path.join(niri_dir, "styleswitcher.toml"))

        # Hyprland colors (already handled in templates)
        # Kitty colors (signals sent via pkill in __setup)
        # Swaylock (already in templates)

    async def __setup(self, image_path: str) -> None:
        try:
            await utils.exec_sh_async("pkill -SIGUSR1 kitty")
        except GLib.Error:
            ...
        options.wallpaper.set_wallpaper_path(image_path)
        css_manager.reload_all_css()
        await self.__reload_gtk_theme()
