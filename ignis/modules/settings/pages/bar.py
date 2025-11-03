from ..elements import (
    SwitchRow,
    SettingsPage,
    SettingsGroup,
    SettingsEntry,
    SpinRow,
)
from user_options import user_options


class BarEntry(SettingsEntry):
    def __init__(self):
        page = SettingsPage(
            name="Bar",
            groups=[
                # Appearance settings
                SettingsGroup(
                    name="Appearance",
                    rows=[
                        SwitchRow(
                            label="Show Background",
                            sublabel="Display background color behind bar",
                            active=user_options.bar.bind("background_enabled"),
                            on_change=lambda x, state: user_options.bar.set_background_enabled(
                                state
                            ),
                        ),
                        SpinRow(
                            label="Transparency",
                            sublabel="Background opacity (0% = fully transparent)",
                            value=user_options.bar.bind(
                                "transparency", transform=lambda v: int(v * 100)
                            ),
                            on_change=lambda x, value: user_options.bar.set_transparency(
                                value / 100.0
                            ),
                            min=0,
                            max=100,
                            step=5,
                            width=100,
                        ),
                    ],
                ),
                # Size settings
                SettingsGroup(
                    name="Size",
                    rows=[
                        SpinRow(
                            label="Height",
                            sublabel="Bar height in pixels",
                            value=user_options.bar.bind("height"),
                            on_change=lambda x, value: user_options.bar.set_height(
                                int(value)
                            ),
                            min=20,
                            max=120,
                            step=5,
                            width=100,
                        ),
                    ],
                ),
                # Spacing settings
                SettingsGroup(
                    name="Spacing",
                    rows=[
                        SpinRow(
                            label="Horizontal Padding",
                            sublabel="Internal padding on left and right sides",
                            value=user_options.bar.bind("padding_horizontal"),
                            on_change=lambda x, value: user_options.bar.set_padding_horizontal(
                                int(value)
                            ),
                            min=0,
                            max=50,
                            step=2,
                            width=100,
                        ),
                        SpinRow(
                            label="Vertical Padding",
                            sublabel="Internal padding on top and bottom",
                            value=user_options.bar.bind("padding_vertical"),
                            on_change=lambda x, value: user_options.bar.set_padding_vertical(
                                int(value)
                            ),
                            min=0,
                            max=30,
                            step=1,
                            width=100,
                        ),
                        SpinRow(
                            label="Top Margin",
                            sublabel="Space between bar and top of screen",
                            value=user_options.bar.bind("margin_top"),
                            on_change=lambda x, value: user_options.bar.set_margin_top(
                                int(value)
                            ),
                            min=0,
                            max=50,
                            step=1,
                            width=100,
                        ),
                        SpinRow(
                            label="Side Margins",
                            sublabel="Space between bar and screen edges",
                            value=user_options.bar.bind("margin_sides"),
                            on_change=lambda x, value: user_options.bar.set_margin_sides(
                                int(value)
                            ),
                            min=0,
                            max=100,
                            step=5,
                            width=100,
                        ),
                    ],
                ),
            ],
        )
        super().__init__(
            label="Bar",
            icon="preferences-system-symbolic",
            page=page,
        )
