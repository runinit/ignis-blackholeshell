import os
from services.material import MaterialService
from services.wallpaper_slideshow import WallpaperSlideshowService
from ..elements import (
    SwitchRow,
    SettingsPage,
    SettingsGroup,
    FileRow,
    SettingsEntry,
    SpinRow,
    ComboBoxRow,
)
from ignis import widgets
from user_options import user_options
from ignis.options import options

material = MaterialService.get_default()
wallpaper_slideshow_service = WallpaperSlideshowService.get_default()


class AppearanceEntry(SettingsEntry):
    def __init__(self):
        page = SettingsPage(
            name="Appearance",
            groups=[
                # Theme settings
                SettingsGroup(
                    name="Theme",
                    rows=[
                        widgets.ListBoxRow(
                            child=widgets.Picture(
                                image=options.wallpaper.bind("wallpaper_path"),
                                width=1920 // 4,
                                height=1080 // 4,
                                halign="center",
                                style="border-radius: 1rem;",
                                content_fit="cover",
                            ),
                            selectable=False,
                            activatable=False,
                        ),
                        SwitchRow(
                            label="Dark mode",
                            active=user_options.material.bind("dark_mode"),
                            on_change=lambda x, state: user_options.material.set_dark_mode(
                                state
                            ),
                            style="margin-top: 1rem;",
                        ),
                        FileRow(
                            label="Wallpaper path",
                            button_label=os.path.basename(
                                options.wallpaper.wallpaper_path
                            )
                            if options.wallpaper.wallpaper_path
                            else None,
                            dialog=widgets.FileDialog(
                                on_file_set=lambda x, file: self._on_wallpaper_selected(
                                    file.get_path()
                                ),
                                initial_path=options.wallpaper.bind("wallpaper_path"),
                                filters=[
                                    widgets.FileFilter(
                                        mime_types=["image/jpeg", "image/png"],
                                        default=True,
                                        name="Images JPEG/PNG",
                                    )
                                ],
                            ),
                        ),
                    ],
                ),
                # Wallpaper Slideshow settings
                SettingsGroup(
                    name="Wallpaper Slideshow",
                    rows=[
                        SwitchRow(
                            label="Enable Slideshow",
                            sublabel="Automatically cycle through wallpapers",
                            active=user_options.wallpaper_slideshow.bind(
                                "slideshow_enabled"
                            ),
                            on_change=lambda x, state: self._on_slideshow_toggled(
                                state
                            ),
                        ),
                        SwitchRow(
                            label="Use Folder",
                            sublabel="Enable folder slideshow instead of single image",
                            active=user_options.wallpaper_slideshow.bind("use_folder"),
                            on_change=lambda x, state: user_options.wallpaper_slideshow.set_use_folder(
                                state
                            ),
                        ),
                        FileRow(
                            label="Wallpaper Folder",
                            sublabel="Folder containing wallpaper images",
                            button_label=os.path.basename(
                                user_options.wallpaper_slideshow.folder_path
                            )
                            if user_options.wallpaper_slideshow.folder_path
                            else "Select Folder",
                            dialog=widgets.FileDialog(
                                select_folder=True,
                                on_file_set=lambda x, file: self._on_folder_selected(
                                    file.get_path()
                                ),
                                initial_path=user_options.wallpaper_slideshow.bind(
                                    "folder_path"
                                ),
                            ),
                        ),
                        SwitchRow(
                            label="Shuffle",
                            sublabel="Randomize wallpaper order",
                            active=user_options.wallpaper_slideshow.bind(
                                "shuffle_enabled"
                            ),
                            on_change=lambda x, state: user_options.wallpaper_slideshow.set_shuffle_enabled(
                                state
                            ),
                        ),
                        SpinRow(
                            label="Interval",
                            sublabel="Minutes between wallpaper changes",
                            value=user_options.wallpaper_slideshow.bind(
                                "interval_value"
                            ),
                            on_change=lambda x, value: user_options.wallpaper_slideshow.set_interval_value(
                                int(value)
                            ),
                            min=1,
                            max=1440,
                            step=5,
                            width=100,
                        ),
                        ComboBoxRow(
                            label="Transition Effect",
                            sublabel="Visual effect for transitions",
                            items=["fade", "slide", "zoom", "pixelate", "swirl", "wipe"],
                            selected=self._get_shader_index(),
                            on_change=lambda x, index: user_options.wallpaper_slideshow.set_transition_shader(
                                ["fade", "slide", "zoom", "pixelate", "swirl", "wipe"][
                                    index
                                ]
                            ),
                        ),
                    ],
                ),
            ],
        )
        super().__init__(
            label="Appearance",
            icon="preferences-desktop-wallpaper-symbolic",
            page=page,
        )

    def _get_shader_index(self) -> int:
        """Get the index for the current shader."""
        shaders = ["fade", "slide", "zoom", "pixelate", "swirl", "wipe"]
        try:
            return shaders.index(user_options.wallpaper_slideshow.transition_shader)
        except ValueError:
            return 0

    def _on_wallpaper_selected(self, wallpaper_path: str) -> None:
        """Handle wallpaper selection."""
        # First set the wallpaper path
        options.wallpaper.set_wallpaper_path(wallpaper_path)
        # Then generate colors from it
        material.generate_colors(wallpaper_path)

    def _on_folder_selected(self, folder_path: str) -> None:
        """Handle folder selection."""
        user_options.wallpaper_slideshow.set_folder_path(folder_path)

        # Load wallpapers from folder
        if user_options.wallpaper_slideshow.use_folder:
            wallpaper_slideshow_service.set_folder(
                folder_path, user_options.wallpaper_slideshow.shuffle_enabled
            )

    def _on_slideshow_toggled(self, enabled: bool) -> None:
        """Handle slideshow enable/disable."""
        user_options.wallpaper_slideshow.set_slideshow_enabled(enabled)

        if enabled:
            # Calculate interval in minutes
            interval_seconds = user_options.wallpaper_slideshow.interval_value * 60
            wallpaper_slideshow_service.play_slideshow(interval_seconds)
        else:
            wallpaper_slideshow_service.pause_slideshow()
