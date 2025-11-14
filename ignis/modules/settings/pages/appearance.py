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
                # Bar Configuration (Phase 2)
                SettingsGroup(
                    name="Bar Configuration",
                    rows=[
                        ComboBoxRow(
                            label="Position",
                            sublabel="Screen edge for bar placement",
                            items=["Top", "Bottom", "Left", "Right"],
                            selected=self._get_bar_position_index(),
                            on_change=lambda x, index: self._on_bar_position_changed(index),
                        ),
                        SwitchRow(
                            label="Floating Mode",
                            sublabel="Add margins around the bar",
                            active=user_options.bar.bind("floating"),
                            on_change=lambda x, state: user_options.bar.set_floating(state),
                        ),
                        SpinRow(
                            label="Float Margin",
                            sublabel="Margin in pixels when floating",
                            value=user_options.bar.bind("float_margin"),
                            on_change=lambda x, value: user_options.bar.set_float_margin(
                                int(value)
                            ),
                            min=0,
                            max=32,
                            step=1,
                            width=80,
                        ),
                        ComboBoxRow(
                            label="Density",
                            sublabel="Bar height and padding",
                            items=["Compact", "Comfortable", "Spacious"],
                            selected=self._get_bar_density_index(),
                            on_change=lambda x, index: self._on_bar_density_changed(index),
                        ),
                        ComboBoxRow(
                            label="Corner Radius",
                            sublabel="Bar corner style",
                            items=["Square", "Normal", "Inverted"],
                            selected=self._get_bar_corner_radius_index(),
                            on_change=lambda x, index: self._on_bar_corner_radius_changed(
                                index
                            ),
                        ),
                    ],
                ),
                # Dock Configuration (Phase 2)
                SettingsGroup(
                    name="Dock Configuration",
                    rows=[
                        SwitchRow(
                            label="Enable Dock",
                            sublabel="Show application dock",
                            active=user_options.dock.bind("enabled"),
                            on_change=lambda x, state: user_options.dock.set_enabled(state),
                        ),
                        ComboBoxRow(
                            label="Position",
                            sublabel="Screen edge for dock placement",
                            items=["Bottom", "Left", "Right"],
                            selected=self._get_dock_position_index(),
                            on_change=lambda x, index: self._on_dock_position_changed(index),
                        ),
                        SpinRow(
                            label="Icon Size",
                            sublabel="Dock icon size multiplier",
                            value=user_options.dock.bind("size"),
                            on_change=lambda x, value: user_options.dock.set_size(float(value)),
                            min=0.5,
                            max=2.0,
                            step=0.1,
                            width=80,
                        ),
                        SwitchRow(
                            label="Auto-Hide",
                            sublabel="Automatically hide dock when not in use",
                            active=user_options.dock.bind("auto_hide"),
                            on_change=lambda x, state: user_options.dock.set_auto_hide(state),
                        ),
                        SpinRow(
                            label="Show Delay",
                            sublabel="Milliseconds before showing dock",
                            value=user_options.dock.bind("show_delay"),
                            on_change=lambda x, value: user_options.dock.set_show_delay(
                                int(value)
                            ),
                            min=0,
                            max=2000,
                            step=50,
                            width=100,
                        ),
                        SpinRow(
                            label="Hide Delay",
                            sublabel="Milliseconds before hiding dock",
                            value=user_options.dock.bind("hide_delay"),
                            on_change=lambda x, value: user_options.dock.set_hide_delay(
                                int(value)
                            ),
                            min=0,
                            max=2000,
                            step=50,
                            width=100,
                        ),
                        SpinRow(
                            label="Reveal Size",
                            sublabel="Trigger zone size at screen edge (pixels)",
                            value=user_options.dock.bind("reveal_size"),
                            on_change=lambda x, value: user_options.dock.set_reveal_size(
                                int(value)
                            ),
                            min=1,
                            max=10,
                            step=1,
                            width=80,
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

    def _get_bar_position_index(self) -> int:
        """Get the index for the current bar position."""
        positions = ["top", "bottom", "left", "right"]
        try:
            return positions.index(user_options.bar.position)
        except ValueError:
            return 0

    def _get_bar_density_index(self) -> int:
        """Get the index for the current bar density."""
        densities = ["compact", "comfortable", "spacious"]
        try:
            return densities.index(user_options.bar.density)
        except ValueError:
            return 1  # Default to comfortable

    def _get_bar_corner_radius_index(self) -> int:
        """Get the index for the current bar corner radius."""
        # Map corner_radius value to index: -1=square(0), 0=normal(1), 1+=inverted(2)
        radius = user_options.bar.corner_radius
        if radius == -1:
            return 0  # Square
        elif radius == 0:
            return 1  # Normal
        else:
            return 2  # Inverted

    def _on_bar_position_changed(self, index: int) -> None:
        """Handle bar position change."""
        positions = ["top", "bottom", "left", "right"]
        if 0 <= index < len(positions):
            user_options.bar.set_position(positions[index])
            user_options.save_to_file(user_options._file)

    def _on_bar_density_changed(self, index: int) -> None:
        """Handle bar density change."""
        densities = ["compact", "comfortable", "spacious"]
        if 0 <= index < len(densities):
            user_options.bar.set_density(densities[index])
            user_options.save_to_file(user_options._file)

    def _on_bar_corner_radius_changed(self, index: int) -> None:
        """Handle bar corner radius change."""
        # Map index to corner_radius value: square(0)=-1, normal(1)=0, inverted(2)=1
        radius_map = {0: -1, 1: 0, 2: 1}
        user_options.bar.set_corner_radius(radius_map.get(index, 0))
        user_options.save_to_file(user_options._file)

    def _get_dock_position_index(self) -> int:
        """Get the index for the current dock position."""
        positions = ["bottom", "left", "right"]
        try:
            return positions.index(user_options.dock.position)
        except ValueError:
            return 0

    def _on_dock_position_changed(self, index: int) -> None:
        """Handle dock position change."""
        positions = ["bottom", "left", "right"]
        if 0 <= index < len(positions):
            user_options.dock.set_position(positions[index])
            user_options.save_to_file(user_options._file)

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
