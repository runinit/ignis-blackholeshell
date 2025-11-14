import asyncio
from ignis import widgets
from ignis.services.system_tray import SystemTrayService, SystemTrayItem

system_tray = SystemTrayService.get_default()


class TrayItem(widgets.Button):
    __gtype_name__ = "TrayItem"

    def __init__(self, item: SystemTrayItem):
        # Create menu separately - don't add to widget tree
        self._menu = item.menu.copy() if item.menu else None

        super().__init__(
            child=widgets.Icon(image=item.bind("icon"), pixel_size=24),
            tooltip_text=item.bind("tooltip"),
            on_click=lambda x: asyncio.create_task(item.activate_async()),
            setup=lambda self: item.connect("removed", lambda x: self.unparent()),
            on_right_click=lambda x: self._menu.popup() if self._menu else None,
            css_classes=["tray-item", "unset"],
        )


class Tray(widgets.Box):
    __gtype_name__ = "Tray"

    def __init__(self):
        super().__init__(
            css_classes=["tray"],
            spacing=10,
        )

        # Add existing items first
        for item in system_tray.items:
            self.append(TrayItem(item))

        # Then listen for new items
        system_tray.connect("added", lambda x, item: self.append(TrayItem(item)))
