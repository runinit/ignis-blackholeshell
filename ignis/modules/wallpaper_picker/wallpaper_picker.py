import os
from gi.repository import GLib
from ignis import widgets
from ignis.window_manager import WindowManager
from services.wallpaper_slideshow import WallpaperSlideshowService
from user_options import user_options


window_manager = WindowManager.get_default()


class WallpaperPickerItem(widgets.Button):
    """A single wallpaper thumbnail item in the picker grid."""

    def __init__(self, wallpaper_path: str, service: WallpaperSlideshowService):
        self._wallpaper_path = wallpaper_path
        self._service = service

        # Get thumbnail
        thumbnail_path = service._cache.get_thumbnail_path(wallpaper_path)

        # Generate if doesn't exist
        if not os.path.exists(thumbnail_path):
            GLib.idle_add(lambda: service._cache.generate_thumbnail(wallpaper_path))
            thumbnail_path = wallpaper_path  # Use original until thumbnail is ready

        super().__init__(
            css_classes=["wallpaper-picker-item"],
            child=widgets.Picture(
                image=thumbnail_path,
                width=200,
                height=112,  # 16:9 aspect ratio
                content_fit="cover",
                css_classes=["wallpaper-picker-thumbnail"],
            ),
            on_click=lambda x: self._on_click(),
            tooltip_text=os.path.basename(wallpaper_path),
        )

    def _on_click(self) -> None:
        """Handle wallpaper selection."""
        self._service.set_wallpaper(self._wallpaper_path)
        window_manager.close_window("ignis_WALLPAPER_PICKER")


class WallpaperPicker(widgets.Window):
    """Wallpaper picker overlay window."""

    def __init__(self):
        self._service = WallpaperSlideshowService.get_default()
        self._grid = widgets.Grid(
            column_spacing=12,
            row_spacing=12,
            css_classes=["wallpaper-picker-grid"],
        )

        # Scrollable container
        scrolled = widgets.Scroll(
            vexpand=True,
            hexpand=True,
            child=widgets.Box(
                vertical=True,
                css_classes=["wallpaper-picker-container"],
                child=[self._grid],
            ),
        )

        # Header with folder info
        header = widgets.Box(
            vertical=False,
            css_classes=["wallpaper-picker-header"],
            child=[
                widgets.Label(
                    label="Wallpaper Picker",
                    halign="start",
                    hexpand=True,
                    css_classes=["wallpaper-picker-title"],
                ),
                widgets.Button(
                    child=widgets.Label(label="✕"),
                    css_classes=["wallpaper-picker-close"],
                    on_click=lambda x: window_manager.close_window(
                        "ignis_WALLPAPER_PICKER"
                    ),
                    tooltip_text="Close",
                ),
            ],
        )

        super().__init__(
            visible=False,
            popup=True,
            kb_mode="on_demand",
            layer="top",
            css_classes=["wallpaper-picker-window"],
            anchor=["top", "right", "bottom", "left"],
            namespace="ignis_WALLPAPER_PICKER",
            child=widgets.Box(
                child=[
                    # Backdrop button
                    widgets.Button(
                        vexpand=True,
                        hexpand=True,
                        css_classes=["unset"],
                        on_click=lambda x: window_manager.close_window(
                            "ignis_WALLPAPER_PICKER"
                        ),
                    ),
                    # Picker content
                    widgets.Box(
                        vertical=True,
                        css_classes=["wallpaper-picker-content"],
                        child=[header, scrolled],
                    ),
                ],
            ),
            setup=lambda self: self.connect("notify::visible", self._on_visibility_changed),
        )

    def _on_visibility_changed(self, *args) -> None:
        """Load wallpapers when window becomes visible."""
        if self.visible:
            self._load_wallpapers()

    def _load_wallpapers(self) -> None:
        """Load wallpapers from the queue into the grid."""
        # Get wallpapers from service queue
        wallpapers = self._service.get_queue()

        if not wallpapers:
            # Show placeholder
            placeholder = widgets.Label(
                label="No wallpapers found.\nConfigure a folder in Settings.",
                halign="center",
                valign="center",
                css_classes=["wallpaper-picker-placeholder"],
            )
            self._grid.attach(placeholder, 0, 0, 3, 1)  # Span 3 columns
            return

        # Add wallpaper items in a grid (4 columns)
        columns = 4
        for i, wallpaper_path in enumerate(wallpapers):
            item = WallpaperPickerItem(wallpaper_path, self._service)
            row = i // columns
            col = i % columns
            self._grid.attach(item, col, row, 1, 1)
