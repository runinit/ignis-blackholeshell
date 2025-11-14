"""
DockItem widget - Individual app icon in the dock.
"""

from ignis import widgets
from ignis.services.applications import Application
from ignis.menu_model import IgnisMenuModel, IgnisMenuItem, IgnisMenuSeparator
from user_options import user_options


class DockItem(widgets.Button):
    """A single application icon in the dock."""

    def __init__(self, app: Application, pinned: bool, running: bool, dock):
        self._app = app
        self._pinned = pinned
        self._running = running
        self._dock = dock  # Reference to parent dock for pin/unpin

        # Icon size based on user preference
        size = int(48 * user_options.dock.size)

        # CSS classes
        css_classes = ["dock-item"]
        if running:
            css_classes.append("running")
        if pinned and not running:
            css_classes.append("inactive")

        # Create context menu
        self._menu = widgets.PopoverMenu()
        self._update_menu()

        super().__init__(
            css_classes=css_classes,
            on_click=lambda x: self._on_click(),
            on_right_click=lambda x: self._menu.popup(),
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

    def _update_menu(self):
        """Update the context menu items."""
        menu_items = [
            IgnisMenuItem(
                label="Unpin from Dock" if self._pinned else "Pin to Dock",
                on_activate=lambda x: self._toggle_pin(),
            ),
            IgnisMenuSeparator(),
            IgnisMenuItem(
                label="Launch",
                on_activate=lambda x: self._app.launch(),
            ),
        ]

        # Add quit option if app is running
        if self._running:
            menu_items.extend([
                IgnisMenuSeparator(),
                IgnisMenuItem(
                    label="Quit",
                    on_activate=lambda x: self._quit_app(),
                ),
            ])

        self._menu.model = IgnisMenuModel(*menu_items)

    def _toggle_pin(self):
        """Toggle pin state of this app."""
        app_id = self._app.desktop_file if self._app.desktop_file else self._app.name
        if self._pinned:
            self._dock.unpin_app(app_id)
            self._pinned = False
        else:
            self._dock.pin_app(app_id)
            self._pinned = True

        # Update menu to reflect new pin state
        self._update_menu()

    def _quit_app(self):
        """Quit the running application."""
        # TODO: Implement app quit (requires window management)
        # For now, this is a placeholder
        pass

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

        # Update menu to show/hide quit option
        self._update_menu()
