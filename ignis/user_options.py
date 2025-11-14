import os
import json
from ignis.options_manager import OptionsGroup, OptionsManager
from ignis import DATA_DIR, CACHE_DIR  # type: ignore

USER_OPTIONS_FILE = f"{DATA_DIR}/user_options.json"
OLD_USER_OPTIONS_FILE = f"{CACHE_DIR}/user_options.json"


# FIXME: remove someday
def _migrate_old_options_file() -> None:
    with open(OLD_USER_OPTIONS_FILE) as f:
        data = f.read()

    with open(USER_OPTIONS_FILE, "w") as f:
        f.write(data)


def _migrate_palette_type_to_matugen_scheme(data: dict) -> dict:
    """
    Migrate old palette_type format to new matugen_scheme_type format.
    Old format: tonalspot, fruitSalad (camelCase)
    New format: tonal-spot, fruit-salad (kebab-case)
    """
    if "material" in data and "palette_type" in data["material"]:
        old_palette = data["material"]["palette_type"]

        # Mapping from old camelCase to new kebab-case
        palette_migration_map = {
            "tonalspot": "tonal-spot",
            "fruitSalad": "fruit-salad",
            "monochrome": "monochrome",
            "rainbow": "rainbow",
            "expressive": "expressive",
            "neutral": "neutral",
            "vibrant": "vibrant",
            "fidelity": "fidelity",
            "content": "content",
        }

        # Migrate to new format
        new_scheme = palette_migration_map.get(old_palette, "tonal-spot")
        data["material"]["matugen_scheme_type"] = new_scheme

        # Remove old field
        del data["material"]["palette_type"]

        print(f"Migrated palette_type '{old_palette}' -> matugen_scheme_type '{new_scheme}'")

    return data


class UserOptions(OptionsManager):
    def __init__(self):
        if not os.path.exists(USER_OPTIONS_FILE) and os.path.exists(
            OLD_USER_OPTIONS_FILE
        ):
            _migrate_old_options_file()

        # Migrate old palette_type to new matugen_scheme_type if needed
        if os.path.exists(USER_OPTIONS_FILE):
            try:
                with open(USER_OPTIONS_FILE, "r") as f:
                    data = json.load(f)

                # Check if migration is needed
                if "material" in data and "palette_type" in data["material"]:
                    data = _migrate_palette_type_to_matugen_scheme(data)

                    # Save migrated data
                    with open(USER_OPTIONS_FILE, "w") as f:
                        json.dump(data, f, indent=4)
            except (json.JSONDecodeError, IOError):
                pass  # If file is corrupted, OptionsManager will handle it

        try:
            super().__init__(file=USER_OPTIONS_FILE)
        except FileNotFoundError:
            pass

    def save_to_file(self, file: str) -> None:
        """
        Override to save ALL options including defaults, not just modified ones.

        Bug fix: OptionsManager.get_modified_options() only returns explicitly set values,
        causing default values to be lost on save/load cycles. Using to_dict() ensures
        all options are persisted.
        """
        with open(file, "w") as fp:
            json.dump(self.to_dict(), fp, indent=4)

    class User(OptionsGroup):
        avatar: str = f"/var/lib/AccountsService/icons/{os.getenv('USER')}"

    class Settings(OptionsGroup):
        last_page: int = 0

    class Material(OptionsGroup):
        # Color Scheme Settings
        scheme_name: str = "Rose Pine"  # Active built-in color scheme
        scheme_variant: str = "main"  # Variant: main, moon, dawn
        use_wallpaper_colors: bool = False  # False = built-in palette, True = dynamic from wallpaper

        # Matugen Settings (for wallpaper-based generation)
        # Scheme types: tonal-spot, vibrant, expressive, neutral, monochrome, fidelity, content, fruit-salad, rainbow
        matugen_scheme_type: str = "tonal-spot"

        # Dark Mode
        dark_mode: bool = True

        # Current Colors (loaded from scheme or matugen)
        colors: dict[str, str] = {}

        # Font Configuration
        interface_font: str = "Inter"
        interface_font_size: int = 11
        document_font: str = "Inter"
        document_font_size: int = 11
        monospace_font: str = "JetBrains Mono"
        monospace_font_size: int = 10

        # App Theming Toggles
        theme_gtk: bool = True
        theme_qt: bool = True
        theme_kitty: bool = True
        theme_ghostty: bool = True
        theme_fuzzel: bool = True
        theme_hyprland: bool = True
        theme_niri: bool = True
        theme_swaylock: bool = True

    class WallpaperSlideshow(OptionsGroup):
        folder_path: str = os.path.expanduser("~/Pictures")
        single_image_path: str = ""
        use_folder: bool = False  # Use single wallpaper by default
        interval_value: int = 30
        interval_unit: str = "minutes"  # "minutes", "hours", "days"
        fit_mode: str = "fill"  # "fill", "stretch", "center", "fit", "tile"
        transition_shader: str = "fade"  # "fade", "slide", "zoom", "pixelate", "swirl", "wipe"
        transition_duration: float = 1.0  # seconds
        slideshow_enabled: bool = False  # Disabled by default
        shuffle_enabled: bool = True

    class Bar(OptionsGroup):
        # Position and Layout (Phase 2)
        position: str = "top"  # top/bottom/left/right
        floating: bool = False  # Floating mode with margins
        float_margin: int = 8  # Margin in pixels when floating
        density: str = "comfortable"  # compact/comfortable/spacious
        corner_radius: int = 0  # -1=square, 0=normal, 1-2=inverted

        # Size and Appearance (Legacy)
        height: int = 40  # pixels, range 20-120
        background_enabled: bool = True
        transparency: float = 0.7  # 0.0 to 1.0 (0% to 100% opaque)
        padding_horizontal: int = 16  # horizontal padding in pixels
        padding_vertical: int = 6  # vertical padding in pixels
        margin_top: int = 0  # top margin in pixels
        margin_sides: int = 0  # left/right margin in pixels

    class Dock(OptionsGroup):
        # Dock Configuration (Phase 2)
        enabled: bool = True  # Enable/disable dock
        position: str = "bottom"  # bottom/left/right
        size: float = 1.0  # Icon size multiplier (0.5-2.0)
        auto_hide: bool = True  # Auto-hide functionality

        # Auto-hide Configuration (Phase 2, Task 4)
        show_delay: int = 200  # Delay before showing dock (ms)
        hide_delay: int = 500  # Delay before hiding dock (ms)
        reveal_size: int = 1  # Trigger zone size at edge (pixels)

        pinned_apps: list[str] = [
            "firefox",
            "kitty",
            "org.gnome.Nautilus",
            "code",
        ]  # Desktop file IDs or app names

    user = User()
    settings = Settings()
    material = Material()
    wallpaper_slideshow = WallpaperSlideshow()
    bar = Bar()
    dock = Dock()


user_options = UserOptions()
