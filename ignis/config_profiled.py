import os
import sys
import time
from contextlib import contextmanager

# Profiling utilities
startup_times = {}

@contextmanager
def profile_section(name: str):
    """Profile a section of code and record timing"""
    start = time.perf_counter()
    print(f"⏱️  Starting: {name}")
    try:
        yield
    finally:
        elapsed = time.perf_counter() - start
        startup_times[name] = elapsed
        print(f"✅ {name}: {elapsed:.3f}s")

def print_profile_summary():
    """Print summary of all profiled sections"""
    print("\n" + "="*60)
    print("STARTUP PERFORMANCE SUMMARY")
    print("="*60)
    total = sum(startup_times.values())
    for name, elapsed in sorted(startup_times.items(), key=lambda x: -x[1]):
        percent = (elapsed / total * 100) if total > 0 else 0
        print(f"{name:40s} {elapsed:8.3f}s ({percent:5.1f}%)")
    print("="*60)
    print(f"{'TOTAL':40s} {total:8.3f}s (100.0%)")
    print("="*60)

# Start profiling
overall_start = time.perf_counter()

with profile_section("Add venv to path"):
    venv_path = os.path.join(os.path.dirname(__file__), ".venv", "lib", "python3.13", "site-packages")
    if os.path.exists(venv_path):
        sys.path.insert(0, venv_path)

with profile_section("Import ignis core"):
    from ignis import utils
    from ignis.services.wallpaper import WallpaperService
    from ignis.css_manager import CssManager, CssInfoPath
    from ignis.icon_manager import IconManager

with profile_section("Import custom services"):
    from services.wallpaper_slideshow import WallpaperSlideshowService
    from user_options import user_options

with profile_section("Import modules"):
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

with profile_section("Initialize managers"):
    icon_manager = IconManager.get_default()
    css_manager = CssManager.get_default()
    WallpaperService.get_default()

with profile_section("Initialize swww daemon"):
    try:
        utils.exec_sh("pgrep -x swww-daemon > /dev/null || swww-daemon &")
    except:
        pass

with profile_section("Initialize wallpaper slideshow service"):
    wallpaper_slideshow = WallpaperSlideshowService.get_default()

with profile_section("Setup wallpaper slideshow"):
    if user_options.wallpaper_slideshow.use_folder:
        if user_options.wallpaper_slideshow.folder_path:
            wallpaper_slideshow.set_folder(
                user_options.wallpaper_slideshow.folder_path,
                shuffle=user_options.wallpaper_slideshow.shuffle_enabled
            )

            if user_options.wallpaper_slideshow.slideshow_enabled:
                value = user_options.wallpaper_slideshow.interval_value
                unit = user_options.wallpaper_slideshow.interval_unit

                if unit == "minutes":
                    interval = value * 60
                elif unit == "hours":
                    interval = value * 3600
                elif unit == "days":
                    interval = value * 86400
                else:
                    interval = 300

                wallpaper_slideshow.play_slideshow(interval)
    elif user_options.wallpaper_slideshow.single_image_path:
        wallpaper_slideshow.set_wallpaper(user_options.wallpaper_slideshow.single_image_path)

with profile_section("Setup CSS reload triggers"):
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

with profile_section("Apply CSS"):
    css_manager.apply_css(
        CssInfoPath(
            name="main",
            path=os.path.join(utils.get_current_dir(), "style.scss"),
            compiler_function=patch_style_scss,
        )
    )

with profile_section("Add icons"):
    icon_manager.add_icons(os.path.join(utils.get_current_dir(), "icons"))

with profile_section("Create ControlCenter"):
    ControlCenter()

with profile_section("Create Bars"):
    for monitor in range(utils.get_n_monitors()):
        Bar(monitor)

with profile_section("Create NotificationPopups"):
    for monitor in range(utils.get_n_monitors()):
        NotificationPopup(monitor)

with profile_section("Create Launcher"):
    Launcher()

with profile_section("Create Powermenu"):
    Powermenu()

with profile_section("Create OSD"):
    OSD()

with profile_section("Create Settings"):
    Settings()

with profile_section("Create WallpaperPicker"):
    WallpaperPicker()

# Print summary
total_time = time.perf_counter() - overall_start
startup_times["OVERALL"] = total_time
print_profile_summary()
