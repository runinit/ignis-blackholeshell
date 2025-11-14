from ignis import widgets
from ignis.services.notifications import Notification, NotificationService
from ignis import utils
from gi.repository import GLib  # type: ignore
from ...shared_widgets import NotificationWidget

# Lazy initialization - don't initialize services at import time
_notifications = None


def get_notifications():
    """Lazy load NotificationService"""
    global _notifications
    if _notifications is None:
        _notifications = NotificationService.get_default()
    return _notifications


class Popup(widgets.Revealer):
    def __init__(self, notification: Notification, **kwargs):
        widget = NotificationWidget(notification)
        super().__init__(child=widget, transition_type="slide_down", **kwargs)

        notification.connect("closed", lambda x: self.destroy())

    def destroy(self):
        self.reveal_child = False
        utils.Timeout(self.transition_duration, self.unparent)


class NotificationList(widgets.Box):
    __gtype_name__ = "NotificationList"

    def __init__(self):
        notifications = get_notifications()
        loading_notifications_label = widgets.Label(
            label="Loading notifications...",
            valign="center",
            vexpand=True,
            css_classes=["notification-center-info-label"],
        )

        super().__init__(
            vertical=True,
            child=[loading_notifications_label],
            vexpand=True,
            css_classes=["rec-unset"],
            setup=lambda self: notifications.connect(
                "notified",
                lambda x, notification: self.__on_notified(notification),
            ),
        )

        utils.ThreadTask(
            self.__load_notifications,
            lambda result: self.__set_notifications(result),
        ).run()

    def __set_notifications(self, widgets_list):
        """Set notification widgets from list - runs in main thread."""
        # Remove all existing children
        child = self.get_first_child()
        while child:
            next_child = child.get_next_sibling()
            self.remove(child)
            child = next_child

        # Add notification widgets
        for widget in widgets_list:
            self.append(widget)

    def __on_notified(self, notification: Notification) -> None:
        notify = Popup(notification)
        self.prepend(notify)
        notify.reveal_child = True

    def __load_notifications(self) -> list[widgets.Label | Popup]:
        """Load notifications in background thread (widget creation is safe)."""
        notifications = get_notifications()
        contents: list[widgets.Label | Popup] = []

        # Create notification widgets (safe to create in background, just not modify tree)
        for notification in notifications.notifications:
            contents.append(Popup(notification, reveal_child=True))

        # Add "No notifications" label
        contents.append(
            widgets.Label(
                label="No notifications",
                valign="center",
                vexpand=True,
                visible=notifications.bind(
                    "notifications", lambda value: len(value) == 0
                ),
                css_classes=["notification-center-info-label"],
            )
        )
        return contents


class NotificationCenter(widgets.Box):
    __gtype_name__ = "NotificationCenter"

    def __init__(self):
        notifications = get_notifications()
        super().__init__(
            vertical=True,
            vexpand=True,
            css_classes=["notification-center"],
            child=[
                widgets.Box(
                    css_classes=["notification-center-header", "rec-unset"],
                    child=[
                        widgets.Label(
                            label=notifications.bind(
                                "notifications", lambda value: str(len(value))
                            ),
                            css_classes=["notification-count"],
                        ),
                        widgets.Label(
                            label="notifications",
                            css_classes=["notification-header-label"],
                        ),
                        widgets.Button(
                            child=widgets.Label(label="Clear all"),
                            halign="end",
                            hexpand=True,
                            on_click=lambda x: notifications.clear_all(),
                            css_classes=["notification-clear-all"],
                        ),
                    ],
                ),
                widgets.Scroll(
                    child=NotificationList(),
                    vexpand=True,
                ),
            ],
        )
