from ignis import widgets
from .widgets import StatusPill, Tray, KeyboardLayout, Battery, Apps, Workspaces
from user_options import user_options


class Bar(widgets.Window):
    __gtype_name__ = "Bar"

    def __init__(self, monitor: int):
        position = user_options.bar.position
        floating = user_options.bar.floating
        density = user_options.bar.density
        corner_radius = user_options.bar.corner_radius

        # Determine anchor based on position and floating mode
        anchor = self._get_anchor_for_position(position, floating)

        # Set exclusivity (floating bars don't reserve space)
        exclusivity = "exclusive" if not floating else "ignore"

        # Set margins for floating mode
        margin = user_options.bar.float_margin if floating else 0

        # Build CSS classes
        css_classes = ["bar", f"position-{position}", f"density-{density}"]

        if floating:
            css_classes.append("floating")

        if corner_radius == -1:
            css_classes.append("square")
        elif corner_radius >= 1:
            css_classes.append("inverted")

        # Determine if we need vertical orientation
        vertical = position in ["left", "right"]

        super().__init__(
            anchor=anchor,
            exclusivity=exclusivity,
            monitor=monitor,
            namespace=f"ignis_BAR_{monitor}",
            layer="top",
            kb_mode="none",
            visible=True,
            margin_top=margin if position == "top" else 0,
            margin_bottom=margin if position == "bottom" else 0,
            margin_left=margin if position == "left" else 0,
            margin_right=margin if position == "right" else 0,
            child=self._create_layout(vertical, monitor),
            css_classes=css_classes,
        )

    def _get_anchor_for_position(self, pos: str, floating: bool) -> list[str]:
        """Get layer shell anchor based on position."""
        if pos == "top":
            return ["top", "left", "right"] if not floating else ["top"]
        elif pos == "bottom":
            return ["bottom", "left", "right"] if not floating else ["bottom"]
        elif pos == "left":
            return ["left", "top", "bottom"] if not floating else ["left"]
        elif pos == "right":
            return ["right", "top", "bottom"] if not floating else ["right"]
        return ["top", "left", "right"]  # fallback

    def _create_layout(self, vertical: bool, monitor: int):
        """Create bar layout based on orientation."""
        if vertical:
            # Vertical layout for left/right positions
            return widgets.Box(
                orientation="vertical",
                css_classes=["bar-widget"],
                child=[
                    widgets.Box(child=[Workspaces()], valign="start"),
                    widgets.Box(child=[Apps()], valign="center", vexpand=True),
                    widgets.Box(
                        orientation="vertical",
                        child=[Tray(), KeyboardLayout(), Battery(), StatusPill(monitor)],
                        valign="end",
                    ),
                ],
            )
        else:
            # Horizontal layout for top/bottom positions (default)
            return widgets.CenterBox(
                css_classes=["bar-widget"],
                start_widget=widgets.Box(child=[Workspaces()]),
                center_widget=widgets.Box(child=[Apps()]),
                end_widget=widgets.Box(
                    child=[Tray(), KeyboardLayout(), Battery(), StatusPill(monitor)]
                ),
            )
