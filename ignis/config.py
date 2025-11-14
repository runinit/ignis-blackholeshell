import os
import sys

# Add venv to path for dependencies like materialyoucolor
venv_path = os.path.join(os.path.dirname(__file__), ".venv", "lib", "python3.13", "site-packages")
if os.path.exists(venv_path):
    sys.path.insert(0, venv_path)

# Enable widget parent debugging
import debug_widget_parent

from ignis import utils

def debug_log(msg):
    """Helper to log debug messages."""
    print(f"[CONFIG] {msg}", file=sys.stderr)
from ignis.services.wallpaper import WallpaperService
from services.wallpaper_slideshow import WallpaperSlideshowService
from modules import (
    Bar,
    ControlCenter,
    Launcher,
    NotificationPopup,
    OSD,
    Powermenu,
    Settings,
    WallpaperPicker,
)
from modules.dock import Dock
from ignis.css_manager import CssManager, CssInfoPath
from ignis.icon_manager import IconManager
from user_options import user_options

icon_manager = IconManager.get_default()
css_manager = CssManager.get_default()
WallpaperService.get_default()

# Initialize swww daemon for wallpaper transitions
# Check if already running before starting
try:
    utils.exec_sh("pgrep -x swww-daemon > /dev/null || swww-daemon &")
except:
    pass  # Ignore errors, daemon might already be running

# Initialize wallpaper slideshow service
wallpaper_slideshow = WallpaperSlideshowService.get_default()

# Setup wallpaper slideshow from user options
if user_options.wallpaper_slideshow.use_folder:
    if user_options.wallpaper_slideshow.folder_path:
        wallpaper_slideshow.set_folder(
            user_options.wallpaper_slideshow.folder_path,
            shuffle=user_options.wallpaper_slideshow.shuffle_enabled
        )

        # Start slideshow if enabled
        if user_options.wallpaper_slideshow.slideshow_enabled:
            # Calculate interval in seconds
            value = user_options.wallpaper_slideshow.interval_value
            unit = user_options.wallpaper_slideshow.interval_unit

            if unit == "minutes":
                interval = value * 60
            elif unit == "hours":
                interval = value * 3600
            elif unit == "days":
                interval = value * 86400
            else:
                interval = 300  # Default 5 minutes

            wallpaper_slideshow.play_slideshow(interval)
elif user_options.wallpaper_slideshow.single_image_path:
    # Set single wallpaper
    wallpaper_slideshow.set_wallpaper(user_options.wallpaper_slideshow.single_image_path)

# Setup CSS reload triggers for bar options
user_options.bar.connect_option("height", lambda: css_manager.reload_all_css())
user_options.bar.connect_option("transparency", lambda: css_manager.reload_all_css())
user_options.bar.connect_option("background_enabled", lambda: css_manager.reload_all_css())
user_options.bar.connect_option("padding_horizontal", lambda: css_manager.reload_all_css())
user_options.bar.connect_option("padding_vertical", lambda: css_manager.reload_all_css())
user_options.bar.connect_option("margin_top", lambda: css_manager.reload_all_css())
user_options.bar.connect_option("margin_sides", lambda: css_manager.reload_all_css())


def format_scss_var(name: str, val: str) -> str:
    return f"${name}: {val};\n"


def patch_style_scss(path: str) -> str:
    with open(path) as file:
        contents = file.read()

    scss_colors = ""

    for key, value in user_options.material.colors.items():
        scss_colors += format_scss_var(key, value)

    # Bar variables
    bar_vars = (
        format_scss_var("bar_height", f"{user_options.bar.height}px")
        + format_scss_var("bar_transparency", str(user_options.bar.transparency))
        + format_scss_var("bar_background_enabled", str(user_options.bar.background_enabled).lower())
        + format_scss_var("bar_padding_h", f"{user_options.bar.padding_horizontal}px")
        + format_scss_var("bar_padding_v", f"{user_options.bar.padding_vertical}px")
        + format_scss_var("bar_margin_top", f"{user_options.bar.margin_top}px")
        + format_scss_var("bar_margin_sides", f"{user_options.bar.margin_sides}px")
    )

    string = (
        format_scss_var("darkmode", str(user_options.material.dark_mode).lower())
        + bar_vars
        + scss_colors
        + contents
    )

    return utils.sass_compile(
        string=string, extra_args=["--load-path", utils.get_current_dir()]
    )


css_manager.apply_css(
    CssInfoPath(
        name="main",
        path=os.path.join(utils.get_current_dir(), "style.scss"),
        compiler_function=patch_style_scss,
    )
)

icon_manager.add_icons(os.path.join(utils.get_current_dir(), "icons"))

debug_log("Creating ControlCenter...")
ControlCenter()
debug_log("ControlCenter created")

num_monitors = utils.get_n_monitors()
debug_log(f"Number of monitors: {num_monitors}")

for monitor in range(num_monitors):
    debug_log(f"Creating Bar for monitor {monitor}...")
    Bar(monitor)
    debug_log(f"Bar {monitor} created")

# Initialize dock (Phase 2)
if user_options.dock.enabled:
    debug_log(f"Dock enabled: {user_options.dock.enabled}, auto_hide: {user_options.dock.auto_hide}")
    for monitor in range(num_monitors):
        debug_log(f"Creating Dock for monitor {monitor}...")
        try:
            Dock(monitor)
            debug_log(f"Dock {monitor} created")
        except Exception as e:
            debug_log(f"ERROR creating Dock {monitor}: {e}")
            import traceback
            traceback.print_exc()
else:
    debug_log("Dock disabled in user options")

for monitor in range(num_monitors):
    debug_log(f"Creating NotificationPopup for monitor {monitor}...")
    NotificationPopup(monitor)

debug_log("Creating Launcher...")
Launcher()
debug_log("Creating Powermenu...")
Powermenu()
debug_log("Creating OSD...")
OSD()

debug_log("Creating Settings...")
Settings()
debug_log("Creating WallpaperPicker...")
WallpaperPicker()

debug_log("All modules initialized successfully!")

# Check window visibility
from ignis.window_manager import WindowManager
wm = WindowManager.get_default()
debug_log(f"Checking window visibility...")
for window_name in ["ignis_BAR_0", "ignis_CONTROL_CENTER", "ignis_DOCK_0", "ignis_LAUNCHER"]:
    window = wm.get_window(window_name)
    if window:
        debug_log(f"  {window_name}: visible={window.visible}, monitor={getattr(window, 'monitor', 'N/A')}")
    else:
        debug_log(f"  {window_name}: NOT FOUND")

debug_log("Initialization complete. Windows should be visible now.")
