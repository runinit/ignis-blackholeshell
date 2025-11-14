"""
DockItem widget - Individual app icon in the dock.
"""

from ignis import widgets
from ignis.services.applications import Application
from user_options import user_options


class DockItem(widgets.Button):
    """A single application icon in the dock."""

    def __init__(self, app: Application, pinned: bool, running: bool):
        self._app = app
        self._pinned = pinned
        self._running = running

        # Icon size based on user preference
        size = int(48 * user_options.dock.size)

        # CSS classes
        css_classes = ["dock-item"]
        if running:
            css_classes.append("running")
        if pinned and not running:
            css_classes.append("inactive")

        super().__init__(
            css_classes=css_classes,
            on_click=lambda x: self._on_click(),
            tooltip_text=app.name,
            child=widgets.Box(
                orientation="vertical",
                spacing=4,
                child=[
                    widgets.Icon(
                        image=app.icon,
                        pixel_size=size,
                    ),
                    # Active indicator dot
                    widgets.Box(
                        css_classes=["active-indicator"],
                        visible=running,
                    ),
                ],
            ),
        )

    def _on_click(self):
        """Launch or focus app."""
        if self._running:
            # TODO: Focus app window (requires window management service)
            # For now, just launch a new instance
            self._app.launch()
        else:
            self._app.launch()

    def update_running_state(self, is_running: bool):
        """Update the running state of this item."""
        self._running = is_running

        if is_running:
            self.add_css_class("running")
            self.remove_css_class("inactive")
        elif self._pinned:
            self.add_css_class("inactive")
            self.remove_css_class("running")

        # Update indicator visibility
        indicator = self.child.child[1]  # The active-indicator box
        indicator.set_visible(is_running)
