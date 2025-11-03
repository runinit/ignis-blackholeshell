import os
from gi.repository import GLib, GObject
from ignis import widgets
from ignis.base_widget import BaseWidget
from ignis.menu_model import IgnisMenuModel, IgnisMenuItem, IgnisMenuSeparator
from services.wallpaper_slideshow import WallpaperSlideshowService
from user_options import user_options


class WallpaperControl(widgets.Box):
    """Control widget for wallpaper slideshow in the Control Center."""

    def __init__(self):
        self._service = WallpaperSlideshowService.get_default()
        self._options = user_options.wallpaper_slideshow

        # Progress tracking
        self._progress_timer: int | None = None
        self._time_remaining: int = 0
        self._total_interval: int = 0

        # Create widgets
        self._thumbnail = self._create_thumbnail()
        self._filename_label = self._create_filename_label()
        self._progress_bar = self._create_progress_bar()
        self._controls = self._create_controls()

        # Right-click menu
        self._menu = self._create_menu()

        # Container that can be hidden
        self._container = widgets.Box(
            vertical=True,
            child=[
                # Horizontal layout with thumbnail and controls
                widgets.Box(
                    vertical=False,
                    spacing=12,
                    child=[
                        # Thumbnail
                        self._thumbnail,
                        # Controls and info on the right
                        widgets.Box(
                            vertical=True,
                            vexpand=True,
                            hexpand=True,
                            child=[
                                # Playback controls
                                self._controls,
                                # Filename and progress
                                widgets.Box(
                                    vertical=True,
                                    vexpand=True,
                                    valign="end",
                                    child=[
                                        self._filename_label,
                                        self._progress_bar,
                                    ],
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        )

        super().__init__(
            vertical=True,
            css_classes=["wallpaper-control"],
            child=[
                self._container,
                # Context menu
                self._menu,
            ],
        )

        # Connect signals
        self._service.connect("wallpaper-changed", self._on_wallpaper_changed)
        self._service.connect("slideshow-state-changed", self._on_slideshow_state_changed)
        self._service.connect("queue-updated", self._on_queue_updated)

        # Initialize state
        self._update_visibility()
        self._update_thumbnail()
        self._update_controls()
        self._start_progress_timer()

    def _create_thumbnail(self) -> BaseWidget:
        """Create the wallpaper thumbnail preview."""
        return widgets.Picture(
            image="",
            width=120,
            height=68,  # 16:9 aspect ratio
            content_fit="cover",
            css_classes=["wallpaper-control-thumbnail"],
        )

    def _create_filename_label(self) -> BaseWidget:
        """Create the label showing current wallpaper filename."""
        return widgets.Label(
            label="No wallpaper",
            ellipsize="end",
            max_width_chars=25,
            css_classes=["wallpaper-control-filename"],
        )

    def _create_progress_bar(self) -> BaseWidget:
        """Create the progress bar showing time until next wallpaper."""
        return widgets.Scale(
            value=0.0,
            min=0.0,
            max=1.0,
            draw_value=False,
            sensitive=False,  # Make it non-interactive
            css_classes=["wallpaper-control-progress"],
        )

    def _create_controls(self) -> BaseWidget:
        """Create the playback control buttons."""
        return widgets.Box(
            halign="start",
            valign="start",
            spacing=4,
            css_classes=["wallpaper-control-buttons"],
            child=[
                # Previous button
                widgets.Button(
                    child=widgets.Label(label="⏮"),
                    on_click=lambda x: self._service.previous_wallpaper(),
                    css_classes=["wallpaper-control-button"],
                    tooltip_text="Previous wallpaper",
                ),
                # Play/Pause button
                widgets.Button(
                    child=widgets.Label(
                        label=self._get_play_pause_icon(),
                        setup=lambda label: self._service.connect(
                            "slideshow-state-changed",
                            lambda s, playing: label.set_label(self._get_play_pause_icon())
                        ),
                    ),
                    on_click=lambda x: self._toggle_slideshow(),
                    css_classes=["wallpaper-control-button", "play-pause"],
                    tooltip_text="Play/Pause slideshow",
                ),
                # Next button
                widgets.Button(
                    child=widgets.Label(label="⏭"),
                    on_click=lambda x: self._service.next_wallpaper(),
                    css_classes=["wallpaper-control-button"],
                    tooltip_text="Next wallpaper",
                ),
            ],
        )

    def _create_menu(self) -> BaseWidget:
        """Create the right-click context menu."""
        menu = widgets.PopoverMenu()

        menu.model = IgnisMenuModel(
            IgnisMenuItem(
                label="Open Wallpaper Picker",
                on_activate=lambda x: self._open_picker(),
            ),
            IgnisMenuSeparator(),
            IgnisMenuItem(
                label="Shuffle Queue",
                on_activate=lambda x: self._service.shuffle_queue(),
            ),
            IgnisMenuItem(
                label="Reload Folder",
                on_activate=lambda x: self._service.reload_folder(shuffle=self._options.shuffle_enabled),
            ),
        )

        # Enable right-click on the entire widget
        self.on_right_click = lambda x: menu.popup()

        return menu

    def _get_play_pause_icon(self) -> str:
        """Get the appropriate play/pause icon."""
        return "⏸" if self._service.is_playing else "▶"

    def _toggle_slideshow(self) -> None:
        """Toggle slideshow playback."""
        interval_seconds = self._calculate_interval_seconds()
        self._service.toggle_playback(interval_seconds)

    def _calculate_interval_seconds(self) -> int:
        """Calculate interval in seconds from user options."""
        value = self._options.interval_value
        unit = self._options.interval_unit

        if unit == "minutes":
            return value * 60
        elif unit == "hours":
            return value * 3600
        elif unit == "days":
            return value * 86400
        else:
            return 300  # Default 5 minutes

    def _update_visibility(self) -> None:
        """Update visibility of controls based on slideshow state."""
        # Only show if slideshow is enabled
        should_show = self._options.slideshow_enabled and self._options.use_folder
        self._container.set_visible(should_show)

    def _update_thumbnail(self) -> None:
        """Update the wallpaper thumbnail to show next in rotation."""
        # Show next wallpaper in queue, not current
        next_wallpaper = self._service.next_wallpaper_preview
        if next_wallpaper and os.path.exists(next_wallpaper):
            # Get cached thumbnail
            thumbnail = self._service._cache.get_thumbnail_path(next_wallpaper)

            # Generate if doesn't exist
            if not os.path.exists(thumbnail):
                thumbnail = self._service._cache.generate_thumbnail(next_wallpaper)

            if thumbnail:
                self._thumbnail.set_image(thumbnail)

            # Update filename
            self._filename_label.set_label(f"Next: {os.path.basename(next_wallpaper)}")
        else:
            self._thumbnail.set_image("")
            self._filename_label.set_label("No slideshow")

    def _update_controls(self) -> None:
        """Update the control button states."""
        # This is handled by signal bindings in _create_controls
        pass

    def _start_progress_timer(self) -> None:
        """Start the progress bar update timer."""
        if self._progress_timer:
            GLib.source_remove(self._progress_timer)

        self._total_interval = self._calculate_interval_seconds()
        self._time_remaining = self._total_interval

        # Update every second
        self._progress_timer = GLib.timeout_add_seconds(1, self._on_progress_tick)

    def _on_progress_tick(self) -> bool:
        """Handle progress timer tick."""
        if not self._service.is_playing:
            # Reset when paused
            self._progress_bar.set_value(0.0)
            return True

        # Decrease time remaining
        self._time_remaining -= 1

        if self._time_remaining <= 0:
            # Reset for next cycle
            self._time_remaining = self._total_interval

        # Update progress bar
        elapsed = self._total_interval - self._time_remaining
        fraction = elapsed / self._total_interval if self._total_interval > 0 else 0.0
        self._progress_bar.set_value(fraction)

        return True  # Continue timer

    def _on_wallpaper_changed(self, service: WallpaperSlideshowService, path: str) -> None:
        """Handle wallpaper change event."""
        self._update_thumbnail()

        # Reset progress
        self._time_remaining = self._total_interval

    def _on_slideshow_state_changed(self, service: WallpaperSlideshowService, playing: bool) -> None:
        """Handle slideshow state change event."""
        self._update_visibility()

        if playing:
            # Recalculate interval in case settings changed
            self._total_interval = self._calculate_interval_seconds()
            self._time_remaining = self._total_interval
        else:
            # Reset progress when stopped
            self._progress_bar.set_value(0.0)

    def _on_queue_updated(self, service: WallpaperSlideshowService) -> None:
        """Handle queue update event."""
        self._update_visibility()
        self._update_thumbnail()

    def _open_picker(self) -> None:
        """Open the wallpaper picker."""
        from ignis.window_manager import WindowManager

        window_manager = WindowManager.get_default()
        window_manager.open_window("ignis_WALLPAPER_PICKER")
