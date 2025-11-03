import os
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

service = WallpaperSlideshowService.get_default()


class WallpaperSlideshowEntry(SettingsEntry):
    def __init__(self):
        page = SettingsPage(
            name="Wallpaper Slideshow",
            groups=[
                # Source Configuration
                SettingsGroup(
                    name="Source",
                    rows=[
                        SwitchRow(
                            label="Use Folder",
                            sublabel="Enable to use folder slideshow instead of single image",
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
                        FileRow(
                            label="Single Wallpaper",
                            sublabel="Single image to use (when folder mode is off)",
                            button_label=os.path.basename(
                                user_options.wallpaper_slideshow.single_image_path
                            )
                            if user_options.wallpaper_slideshow.single_image_path
                            else "Select Image",
                            dialog=widgets.FileDialog(
                                on_file_set=lambda x, file: self._on_single_image_selected(
                                    file.get_path()
                                ),
                                initial_path=user_options.wallpaper_slideshow.bind(
                                    "single_image_path"
                                ),
                                filters=[
                                    widgets.FileFilter(
                                        mime_types=[
                                            "image/jpeg",
                                            "image/png",
                                            "image/webp",
                                        ],
                                        default=True,
                                        name="Images",
                                    )
                                ],
                            ),
                        ),
                    ],
                ),
                # Slideshow Settings
                SettingsGroup(
                    name="Slideshow",
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
                            label="Shuffle",
                            sublabel="Randomize wallpaper order",
                            active=user_options.wallpaper_slideshow.bind(
                                "shuffle_enabled"
                            ),
                            on_change=lambda x, state: user_options.wallpaper_slideshow.set_shuffle_enabled(
                                state
                            ),
                        ),
                    ],
                ),
                # Interval Settings
                SettingsGroup(
                    name="Interval",
                    rows=[
                        SpinRow(
                            label="Interval Value",
                            sublabel="Time between wallpaper changes",
                            value=user_options.wallpaper_slideshow.bind(
                                "interval_value"
                            ),
                            on_change=lambda x, value: user_options.wallpaper_slideshow.set_interval_value(
                                int(value)
                            ),
                            min=1,
                            max=1000,
                            step=1,
                            width=100,
                        ),
                        ComboBoxRow(
                            label="Interval Unit",
                            sublabel="Time unit for interval",
                            items=["minutes", "hours", "days"],
                            selected=self._get_interval_unit_index(),
                            on_change=lambda x, index: user_options.wallpaper_slideshow.set_interval_unit(
                                ["minutes", "hours", "days"][index]
                            ),
                        ),
                    ],
                ),
                # Display Settings
                SettingsGroup(
                    name="Display",
                    rows=[
                        ComboBoxRow(
                            label="Fit Mode",
                            sublabel="How wallpapers are scaled and positioned",
                            items=["fill", "stretch", "center", "fit", "tile"],
                            selected=self._get_fit_mode_index(),
                            on_change=lambda x, index: user_options.wallpaper_slideshow.set_fit_mode(
                                ["fill", "stretch", "center", "fit", "tile"][index]
                            ),
                        ),
                    ],
                ),
                # Transition Settings
                SettingsGroup(
                    name="Transitions",
                    rows=[
                        ComboBoxRow(
                            label="Transition Effect",
                            sublabel="Visual effect for wallpaper transitions",
                            items=["fade", "slide", "zoom", "pixelate", "swirl", "wipe"],
                            selected=self._get_shader_index(),
                            on_change=lambda x, index: user_options.wallpaper_slideshow.set_transition_shader(
                                ["fade", "slide", "zoom", "pixelate", "swirl", "wipe"][
                                    index
                                ]
                            ),
                        ),
                        widgets.ListBoxRow(
                            child=widgets.Box(
                                vertical=False,
                                spacing=12,
                                child=[
                                    widgets.Box(
                                        vertical=True,
                                        child=[
                                            widgets.Label(
                                                label="Transition Duration",
                                                halign="start",
                                                css_classes=["settings-row-label"],
                                            ),
                                            widgets.Label(
                                                label="Animation duration in seconds",
                                                halign="start",
                                                css_classes=["settings-row-subtitle"],
                                            ),
                                        ],
                                    ),
                                    widgets.Box(
                                        hexpand=True,
                                        halign="end",
                                        child=[
                                            widgets.Scale(
                                                min=0.5,
                                                max=5.0,
                                                step=0.1,
                                                value=user_options.wallpaper_slideshow.bind(
                                                    "transition_duration"
                                                ),
                                                on_change=lambda x, value: user_options.wallpaper_slideshow.set_transition_duration(
                                                    value
                                                ),
                                                width_request=200,
                                                draw_value=True,
                                                digits=1,
                                                setup=lambda scale: [
                                                    scale.add_mark(0.5, 1, "0.5s"),  # 1 = Gtk.PositionType.BOTTOM
                                                    scale.add_mark(1.0, 1, "1s"),
                                                    scale.add_mark(2.0, 1, "2s"),
                                                    scale.add_mark(3.0, 1, "3s"),
                                                    scale.add_mark(5.0, 1, "5s"),
                                                ],
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                            selectable=False,
                            activatable=False,
                        ),
                    ],
                ),
            ],
        )
        super().__init__(
            label="Wallpaper Slideshow",
            icon="preferences-desktop-wallpaper-symbolic",
            page=page,
        )

    def _get_interval_unit_index(self) -> int:
        """Get the index for the current interval unit."""
        units = ["minutes", "hours", "days"]
        try:
            return units.index(user_options.wallpaper_slideshow.interval_unit)
        except ValueError:
            return 0

    def _get_fit_mode_index(self) -> int:
        """Get the index for the current fit mode."""
        modes = ["fill", "stretch", "center", "fit", "tile"]
        try:
            return modes.index(user_options.wallpaper_slideshow.fit_mode)
        except ValueError:
            return 0

    def _get_shader_index(self) -> int:
        """Get the index for the current shader."""
        shaders = ["fade", "slide", "zoom", "pixelate", "swirl", "wipe"]
        try:
            return shaders.index(user_options.wallpaper_slideshow.transition_shader)
        except ValueError:
            return 0

    def _on_folder_selected(self, folder_path: str) -> None:
        """Handle folder selection."""
        user_options.wallpaper_slideshow.set_folder_path(folder_path)

        # Load wallpapers from folder
        if user_options.wallpaper_slideshow.use_folder:
            service.set_folder(
                folder_path, user_options.wallpaper_slideshow.shuffle_enabled
            )

    def _on_single_image_selected(self, image_path: str) -> None:
        """Handle single image selection."""
        user_options.wallpaper_slideshow.set_single_image_path(image_path)

        # Set wallpaper if not in folder mode
        if not user_options.wallpaper_slideshow.use_folder:
            service.set_wallpaper(image_path)

    def _on_slideshow_toggled(self, enabled: bool) -> None:
        """Handle slideshow enable/disable."""
        user_options.wallpaper_slideshow.set_slideshow_enabled(enabled)

        if enabled:
            # Calculate interval
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

            service.play_slideshow(interval)
        else:
            service.pause_slideshow()
