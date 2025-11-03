import os
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


class UserOptions(OptionsManager):
    def __init__(self):
        if not os.path.exists(USER_OPTIONS_FILE) and os.path.exists(
            OLD_USER_OPTIONS_FILE
        ):
            _migrate_old_options_file()

        try:
            super().__init__(file=USER_OPTIONS_FILE)
        except FileNotFoundError:
            pass

    class User(OptionsGroup):
        avatar: str = f"/var/lib/AccountsService/icons/{os.getenv('USER')}"

    class Settings(OptionsGroup):
        last_page: int = 0

    class Material(OptionsGroup):
        dark_mode: bool = True
        colors: dict[str, str] = {}

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
        height: int = 40  # pixels, range 20-120
        background_enabled: bool = True
        transparency: float = 0.7  # 0.0 to 1.0 (0% to 100% opaque)
        padding_horizontal: int = 16  # horizontal padding in pixels
        padding_vertical: int = 6  # vertical padding in pixels
        margin_top: int = 0  # top margin in pixels
        margin_sides: int = 0  # left/right margin in pixels

    user = User()
    settings = Settings()
    material = Material()
    wallpaper_slideshow = WallpaperSlideshow()
    bar = Bar()


user_options = UserOptions()
