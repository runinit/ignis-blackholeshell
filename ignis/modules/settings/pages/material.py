from services.material import MaterialService, ColorSchemeService
from ..elements import (
    SwitchRow,
    SettingsPage,
    SettingsGroup,
    SettingsEntry,
    SpinRow,
    ComboBoxRow,
    EntryRow,
)
from user_options import user_options

material = MaterialService.get_default()
color_scheme_service = ColorSchemeService.get_default()


class MaterialEntry(SettingsEntry):
    def __init__(self):
        # Palette type mapping: value -> display label (using matugen 3.0 format)
        self._palette_map = {
            "tonal-spot": "Tonal Spot (Balanced)",
            "monochrome": "Monochrome (Grayscale)",
            "rainbow": "Rainbow (Colorful)",
            "fruit-salad": "Fruit Salad (Vibrant)",
            "expressive": "Expressive (Bold)",
            "neutral": "Neutral (Subdued)",
            "vibrant": "Vibrant (Bright)",
            "fidelity": "Fidelity (True to source)",
            "content": "Content (Adaptive)",
        }

        # Reverse mapping for index -> value
        self._palette_values = list(self._palette_map.keys())
        # Display labels for ComboBoxRow
        palette_labels = list(self._palette_map.values())

        page = SettingsPage(
            name="Material You",
            groups=[
                # Color Scheme Selection (NEW)
                SettingsGroup(
                    name="Color Scheme",
                    rows=[
                        ComboBoxRow(
                            label="Built-in Color Scheme",
                            sublabel="Select a pre-defined color palette",
                            items=color_scheme_service.available_schemes,
                            selected=self._get_scheme_index(),
                            on_change=lambda x, index: self._on_scheme_changed(index),
                        ),
                        SwitchRow(
                            label="Use Wallpaper Colors",
                            sublabel="Generate colors dynamically from wallpaper",
                            active=user_options.material.bind("use_wallpaper_colors"),
                            on_change=lambda x, active: self._on_wallpaper_toggle(active),
                        ),
                    ],
                ),
                # Matugen Configuration (for wallpaper-based generation)
                SettingsGroup(
                    name="Wallpaper Color Generation",
                    rows=[
                        ComboBoxRow(
                            label="Matugen Scheme Type",
                            sublabel="Algorithm for generating color palettes from wallpaper",
                            items=palette_labels,
                            selected=self._get_palette_index(),
                            on_change=lambda x, index: user_options.material.set_matugen_scheme_type(
                                self._palette_values[index]
                            ),
                        ),
                    ],
                ),
                # Font Configuration
                SettingsGroup(
                    name="Fonts",
                    rows=[
                        EntryRow(
                            label="Interface Font",
                            sublabel="Font used for menus, buttons, and UI elements",
                            text=user_options.material.bind("interface_font"),
                            on_change=lambda x, text: user_options.material.set_interface_font(
                                text
                            ),
                        ),
                        SpinRow(
                            label="Interface Font Size",
                            min=8,
                            max=16,
                            step=1,
                            value=user_options.material.bind("interface_font_size"),
                            on_change=lambda x, value: user_options.material.set_interface_font_size(
                                int(value)
                            ),
                        ),
                        EntryRow(
                            label="Document Font",
                            sublabel="Font used for reading content and documents",
                            text=user_options.material.bind("document_font"),
                            on_change=lambda x, text: user_options.material.set_document_font(
                                text
                            ),
                        ),
                        SpinRow(
                            label="Document Font Size",
                            min=8,
                            max=16,
                            step=1,
                            value=user_options.material.bind("document_font_size"),
                            on_change=lambda x, value: user_options.material.set_document_font_size(
                                int(value)
                            ),
                        ),
                        EntryRow(
                            label="Monospace Font",
                            sublabel="Font used for code and terminal applications",
                            text=user_options.material.bind("monospace_font"),
                            on_change=lambda x, text: user_options.material.set_monospace_font(
                                text
                            ),
                        ),
                        SpinRow(
                            label="Monospace Font Size",
                            min=8,
                            max=16,
                            step=1,
                            value=user_options.material.bind("monospace_font_size"),
                            on_change=lambda x, value: user_options.material.set_monospace_font_size(
                                int(value)
                            ),
                        ),
                    ],
                ),
                # Application Theming Toggles
                SettingsGroup(
                    name="Application Theming",
                    rows=[
                        SwitchRow(
                            label="GTK Applications",
                            sublabel="Theme GTK 3/4 applications (GNOME apps, etc.)",
                            active=user_options.material.bind("theme_gtk"),
                            on_change=lambda x, state: user_options.material.set_theme_gtk(
                                state
                            ),
                        ),
                        SwitchRow(
                            label="Qt Applications",
                            sublabel="Theme Qt 5/6 applications (KDE apps, etc.)",
                            active=user_options.material.bind("theme_qt"),
                            on_change=lambda x, state: user_options.material.set_theme_qt(
                                state
                            ),
                        ),
                        SwitchRow(
                            label="Kitty Terminal",
                            sublabel="Apply colors to Kitty terminal emulator",
                            active=user_options.material.bind("theme_kitty"),
                            on_change=lambda x, state: user_options.material.set_theme_kitty(
                                state
                            ),
                        ),
                        SwitchRow(
                            label="Ghostty Terminal",
                            sublabel="Apply colors to Ghostty terminal emulator",
                            active=user_options.material.bind("theme_ghostty"),
                            on_change=lambda x, state: user_options.material.set_theme_ghostty(
                                state
                            ),
                        ),
                        SwitchRow(
                            label="Fuzzel Launcher",
                            sublabel="Theme Fuzzel application launcher",
                            active=user_options.material.bind("theme_fuzzel"),
                            on_change=lambda x, state: user_options.material.set_theme_fuzzel(
                                state
                            ),
                        ),
                        SwitchRow(
                            label="Hyprland Compositor",
                            sublabel="Apply colors to Hyprland window manager",
                            active=user_options.material.bind("theme_hyprland"),
                            on_change=lambda x, state: user_options.material.set_theme_hyprland(
                                state
                            ),
                        ),
                        SwitchRow(
                            label="Niri Switcher",
                            sublabel="Theme Niri window switcher",
                            active=user_options.material.bind("theme_niri"),
                            on_change=lambda x, state: user_options.material.set_theme_niri(
                                state
                            ),
                        ),
                        SwitchRow(
                            label="Swaylock",
                            sublabel="Apply colors to Swaylock screen locker",
                            active=user_options.material.bind("theme_swaylock"),
                            on_change=lambda x, state: user_options.material.set_theme_swaylock(
                                state
                            ),
                        ),
                    ],
                ),
            ],
        )

        super().__init__(
            page=page,
            label="Material You",
            icon="applications-graphics-symbolic",
        )

    def _get_scheme_index(self) -> int:
        """Get the index of the current color scheme."""
        current_scheme = user_options.material.scheme_name
        schemes = color_scheme_service.available_schemes
        try:
            return schemes.index(current_scheme)
        except ValueError:
            return 0  # Default to first scheme

    def _get_palette_index(self) -> int:
        """Get the index of the current matugen palette type."""
        current = user_options.material.matugen_scheme_type
        try:
            return self._palette_values.index(current)
        except ValueError:
            return 0  # Default to tonal-spot

    def _on_scheme_changed(self, index: int) -> None:
        """Handle color scheme selection."""
        schemes = color_scheme_service.available_schemes
        if 0 <= index < len(schemes):
            scheme_name = schemes[index]
            user_options.material.set_scheme_name(scheme_name)
            color_scheme_service.set_scheme(scheme_name)
            user_options.save_to_file(user_options._file)

    def _on_wallpaper_toggle(self, active: bool) -> None:
        """Handle wallpaper colors toggle."""
        user_options.material.set_use_wallpaper_colors(active)
        color_scheme_service.use_wallpaper_colors = active
        user_options.save_to_file(user_options._file)
