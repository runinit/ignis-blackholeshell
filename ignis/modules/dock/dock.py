"""
Dock window - Main dock implementation.
"""

from gi.repository import GLib
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

        # Store references for auto-hide setup (done after super().__init__)
        self._auto_hide_enabled = user_options.dock.auto_hide

        # Wrap dock_box in EventBox for hover detection (auto-hide)
        dock_child = self._dock_box
        if self._auto_hide_enabled and enabled:
            # Don't pass child in constructor to avoid re-parenting issues
            # EventBox inherits from Box and treats Box children as iterable
            event_box = widgets.EventBox(
                on_hover=lambda x: self._on_dock_enter(),
                on_hover_lost=lambda x: self._on_dock_leave(),
            )
            event_box.append(self._dock_box)
            dock_child = event_box

        super().__init__(
            namespace=f"ignis_DOCK_{monitor}",
            monitor=monitor,
            anchor=anchor,
            exclusivity="normal",
            layer="top",
            kb_mode="none",
            css_classes=css_classes,
            visible=enabled and not user_options.dock.auto_hide,
            child=dock_child,
        )

        # Auto-hide state management
        self._is_hidden = False
        self._show_timer_id = None
        self._hide_timer_id = None
        self._mouse_inside = False
        self.monitor = monitor
        self.position = position

        # TODO: Listen to app changes when WindowManager integration is added
        # ApplicationsService doesn't emit a "changed" signal
        # Will need to connect to WindowManager signals for running app tracking
        # apps_service.connect("changed", lambda *_: self._on_apps_changed())

        # Setup auto-hide if enabled
        if self._auto_hide_enabled and enabled:
            self._setup_auto_hide()

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
        """Build list of dock items (pinned apps only for now)."""
        items = []
        pinned_ids = user_options.dock.pinned_apps

        # Note: ApplicationsService doesn't track running apps
        # TODO: Integrate with WindowManager service for running app tracking

        # Add pinned apps
        for app_id in pinned_ids:
            app = self._find_app(app_id)
            if app:
                # For now, treat all pinned apps as not running
                # TODO: Check actual running state via window manager
                item = DockItem(app, pinned=True, running=False, dock=self)
                items.append(item)
                self._items.append(item)

        return items

    def _find_app(self, app_id: str) -> ApplicationsService | None:
        """Find an application by ID or name."""
        all_apps = apps_service.apps

        # Try exact desktop file match first
        for app in all_apps:
            if app.desktop_file and app.desktop_file == app_id:
                return app

        # Try case-insensitive name match
        for app in all_apps:
            if app.name and app.name.lower() == app_id.lower():
                return app
            if app.desktop_file and app.desktop_file.lower() == app_id.lower():
                return app

        # Try fuzzy search as last resort
        results = apps_service.search(apps_service.apps, app_id)
        return results[0] if results else None

    def _on_apps_changed(self):
        """Handle application changes (open/close)."""
        # Rebuild dock items
        self._items.clear()
        new_items = self._build_dock_items()

        # Update dock box children - remove all existing children first
        # Get current children and remove them
        child = self._dock_box.get_first_child()
        while child:
            next_child = child.get_next_sibling()
            self._dock_box.remove(child)
            child = next_child

        # Add new items
        for item in new_items:
            self._dock_box.append(item)

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

    # Auto-hide functionality (Phase 2, Task 4)

    def _setup_auto_hide(self):
        """Setup auto-hide with peek/trigger window."""
        reveal_size = user_options.dock.reveal_size

        # Create peek/trigger window at dock edge
        self._peek_window = widgets.Window(
            namespace=f"ignis_DOCK_PEEK_{self.monitor}",
            monitor=self.monitor,
            anchor=self._get_peek_anchor(),
            exclusivity="ignore",
            layer="overlay",
            kb_mode="none",
            css_classes=["dock-peek"],
            child=widgets.EventBox(
                on_hover=lambda x: self._on_peek_hover(),
                on_hover_lost=lambda x: self._on_peek_hover_lost(),
            ),
        )

        # Set peek window size based on position
        if self.position == "bottom":
            self._peek_window.set_size_request(-1, reveal_size)
        elif self.position == "left":
            self._peek_window.set_size_request(reveal_size, -1)
        elif self.position == "right":
            self._peek_window.set_size_request(reveal_size, -1)

        # Note: Hover handlers for dock are set via EventBox wrapper in __init__
        # No need for GTK3-style signal connections (enter-notify-event, leave-notify-event)

        # Initially hide dock if auto-hide is enabled
        self._is_hidden = True
        self.set_visible(False)
        self.add_css_class("hidden")

    def _get_peek_anchor(self) -> list[str]:
        """Get anchor for peek/trigger window based on dock position."""
        if self.position == "bottom":
            return ["bottom", "left", "right"]
        elif self.position == "left":
            return ["left", "top", "bottom"]
        elif self.position == "right":
            return ["right", "top", "bottom"]
        return ["bottom", "left", "right"]

    def _on_peek_hover(self):
        """Handle mouse hovering over peek window."""
        self._cancel_hide_timer()
        self._schedule_show()

    def _on_peek_hover_lost(self):
        """Handle mouse leaving peek window."""
        if not self._mouse_inside:
            self._cancel_show_timer()
            self._schedule_hide()

    def _on_dock_enter(self):
        """Handle mouse entering dock."""
        self._mouse_inside = True
        self._cancel_hide_timer()

    def _on_dock_leave(self):
        """Handle mouse leaving dock."""
        self._mouse_inside = False
        self._schedule_hide()

    def _schedule_show(self):
        """Schedule dock to show after delay."""
        self._cancel_show_timer()

        show_delay = user_options.dock.show_delay
        if show_delay > 0:
            self._show_timer_id = GLib.timeout_add(show_delay, self._show_dock)
        else:
            self._show_dock()

    def _schedule_hide(self):
        """Schedule dock to hide after delay."""
        self._cancel_hide_timer()

        hide_delay = user_options.dock.hide_delay
        if hide_delay > 0:
            self._hide_timer_id = GLib.timeout_add(hide_delay, self._hide_dock)
        else:
            self._hide_dock()

    def _cancel_show_timer(self):
        """Cancel scheduled show operation."""
        if self._show_timer_id:
            GLib.source_remove(self._show_timer_id)
            self._show_timer_id = None

    def _cancel_hide_timer(self):
        """Cancel scheduled hide operation."""
        if self._hide_timer_id:
            GLib.source_remove(self._hide_timer_id)
            self._hide_timer_id = None

    def _show_dock(self):
        """Show the dock with animation."""
        if self._is_hidden and self._auto_hide_enabled:
            self._is_hidden = False
            self.remove_css_class("hidden")
            self.add_css_class("showing")
            self.set_visible(True)
            # Remove showing class after animation
            GLib.timeout_add(300, lambda: self.remove_css_class("showing"))

        self._show_timer_id = None
        return False  # Don't repeat timer

    def _hide_dock(self):
        """Hide the dock with animation."""
        if not self._is_hidden and self._auto_hide_enabled and not self._mouse_inside:
            self._is_hidden = True
            self.add_css_class("hiding")
            # Hide after animation completes
            GLib.timeout_add(300, self._complete_hide)

        self._hide_timer_id = None
        return False  # Don't repeat timer

    def _complete_hide(self):
        """Complete the hide operation after animation."""
        if self._is_hidden:
            self.set_visible(False)
            self.remove_css_class("hiding")
            self.add_css_class("hidden")
        return False  # Don't repeat timer
