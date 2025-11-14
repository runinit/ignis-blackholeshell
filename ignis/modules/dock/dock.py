"""
Dock window - Main dock implementation.
"""

from ignis import widgets
from ignis.services.applications import ApplicationsService
from .dock_item import DockItem
from user_options import user_options


apps_service = ApplicationsService.get_default()


class Dock(widgets.Window):
    """Application dock with pinned and running apps."""

    __gtype_name__ = "Dock"

    def __init__(self, monitor: int):
        position = user_options.dock.position
        enabled = user_options.dock.enabled

        # Determine anchor based on position
        anchor = self._get_anchor(position)

        # Determine orientation
        vertical = position in ["left", "right"]

        # Build CSS classes
        css_classes = ["dock", f"position-{position}"]

        # Create dock items
        self._items = []
        self._dock_box = widgets.Box(
            orientation="vertical" if vertical else "horizontal",
            css_classes=["dock-container"],
            spacing=4,
            child=self._build_dock_items(),
        )

        super().__init__(
            namespace=f"ignis_DOCK_{monitor}",
            monitor=monitor,
            anchor=anchor,
            exclusivity="normal",
            layer="top",
            kb_mode="none",
            css_classes=css_classes,
            visible=enabled,
            child=self._dock_box,
        )

        # Listen to app changes
        apps_service.connect("changed", lambda *_: self._on_apps_changed())

    def _get_anchor(self, pos: str) -> list[str]:
        """Get layer shell anchor based on position."""
        if pos == "bottom":
            return ["bottom", "left", "right"]
        elif pos == "left":
            return ["left", "top", "bottom"]
        elif pos == "right":
            return ["right", "top", "bottom"]
        return ["bottom", "left", "right"]  # fallback

    def _build_dock_items(self) -> list:
        """Build list of dock items (pinned + running)."""
        items = []
        pinned_ids = user_options.dock.pinned_apps
        running_apps = apps_service.query("")  # All running apps

        # Get running app IDs/names for comparison
        running_app_ids = set()
        for app in running_apps:
            # Try desktop file first, then app name
            if app.desktop_file:
                running_app_ids.add(app.desktop_file)
            if app.name:
                running_app_ids.add(app.name.lower())

        # Add pinned apps
        for app_id in pinned_ids:
            app = self._find_app(app_id)
            if app:
                # Check if this pinned app is running
                is_running = (
                    app.desktop_file in running_app_ids
                    or (app.name and app.name.lower() in running_app_ids)
                )
                item = DockItem(app, pinned=True, running=is_running, dock=self)
                items.append(item)
                self._items.append(item)

        # Add non-pinned running apps
        for app in running_apps:
            app_id = app.desktop_file if app.desktop_file else app.name
            if app_id not in pinned_ids:
                item = DockItem(app, pinned=False, running=True, dock=self)
                items.append(item)
                self._items.append(item)

        return items

    def _find_app(self, app_id: str) -> ApplicationsService | None:
        """Find an application by ID or name."""
        # Try exact match first
        app = apps_service.get_app(app_id)
        if app:
            return app

        # Try case-insensitive name search
        all_apps = apps_service.query("")
        for app in all_apps:
            if app.name and app.name.lower() == app_id.lower():
                return app
            if app.desktop_file and app.desktop_file.lower() == app_id.lower():
                return app

        # Try fuzzy search as last resort
        results = apps_service.query(app_id, 1)
        return results[0] if results else None

    def _on_apps_changed(self):
        """Handle application changes (open/close)."""
        # Rebuild dock items
        self._items.clear()
        new_items = self._build_dock_items()

        # Update dock box children
        self._dock_box.set_child(new_items)

    def pin_app(self, app_id: str):
        """Pin an app to the dock."""
        pinned = list(user_options.dock.pinned_apps)
        if app_id not in pinned:
            pinned.append(app_id)
            user_options.dock.set_pinned_apps(pinned)
            user_options.save_to_file(user_options._file)
            self._on_apps_changed()

    def unpin_app(self, app_id: str):
        """Unpin an app from the dock."""
        pinned = list(user_options.dock.pinned_apps)
        if app_id in pinned:
            pinned.remove(app_id)
            user_options.dock.set_pinned_apps(pinned)
            user_options.save_to_file(user_options._file)
            self._on_apps_changed()
