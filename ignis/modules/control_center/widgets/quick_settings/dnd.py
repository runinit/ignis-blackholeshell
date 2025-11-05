from ...qs_button import QSButton
from ignis.services.notifications import NotificationService
from ignis.options import options

# Lazy initialization - don't initialize services at import time
_notifications = None


def get_notifications():
    """Lazy load NotificationService"""
    global _notifications
    if _notifications is None:
        _notifications = NotificationService.get_default()
    return _notifications


class DNDButton(QSButton):
    __gtype_name__ = "DNDButton"

    def __init__(self):
        super().__init__(
            label=options.notifications.bind(
                "dnd", lambda value: "Silent" if value else "Noisy"
            ),
            icon_name=options.notifications.bind(
                "dnd",
                transform=lambda value: "notification-disabled-symbolic"
                if value
                else "notification-symbolic",
            ),
            on_activate=lambda x: self.__activate(True),
            on_deactivate=lambda x: self.__activate(False),
            active=options.notifications.bind("dnd"),
        )

    def __activate(self, state: bool) -> None:
        options.notifications.dnd = state
