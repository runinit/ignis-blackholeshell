from ignis import widgets
from user_options import user_options
from .active_page import active_page
from .pages import (
    AboutEntry,
    AppearanceEntry,
    BarEntry,
    MaterialEntry,
    NotificationsEntry,
    RecorderEntry,
    UserEntry,
)


class Settings(widgets.RegularWindow):
    def __init__(self) -> None:
        self._content = widgets.Box(
            hexpand=True,
            vexpand=True,
            css_classes=["settings-content"],
        )
        self._listbox = widgets.ListBox()

        # Manually handle active_page changes to avoid widget re-parenting issues
        active_page.connect("notify::value", lambda obj, param: self._update_content(obj.value))
        # Set initial content
        self._update_content(active_page.value)

        navigation_sidebar = widgets.Box(
            vertical=True,
            css_classes=["settings-sidebar"],
            child=[
                widgets.Label(
                    label="Settings",
                    halign="start",
                    css_classes=["settings-sidebar-label"],
                ),
                self._listbox,
            ],
        )

        # Create GNOME 48-style HeaderBar with title and window controls
        headerbar = widgets.HeaderBar(
            css_classes=["settings-headerbar"],
            show_title_buttons=True,
            title_widget=widgets.Label(
                label="Settings",
                css_classes=["settings-header-title"],
            ),
        )

        super().__init__(
            default_width=1200,
            default_height=700,
            resizable=True,
            hide_on_close=True,
            visible=False,
            titlebar=headerbar,
            child=widgets.Box(child=[navigation_sidebar, self._content]),
            namespace="ignis_SETTINGS",
        )

        self.connect("notify::visible", self.__on_open)

    def _update_content(self, page) -> None:
        """Update the content area with the new page, ensuring proper widget parenting."""
        # Clear existing children to properly unparent any previous widgets
        self._content.child = []
        # Add the new page
        if page:
            self._content.child = [page]

    def __on_open(self, *args) -> None:
        if self.visible is False:
            return

        if len(self._listbox.rows) != 0:
            return

        rows = [
            NotificationsEntry(),
            RecorderEntry(),
            AppearanceEntry(),
            MaterialEntry(),
            BarEntry(),
            UserEntry(),
            AboutEntry(),
        ]

        self._listbox.rows = rows
        self._listbox.activate_row(rows[user_options.settings.last_page])

        self._listbox.connect("row-activated", self.__update_last_page)

    def __update_last_page(self, x, row) -> None:
        user_options.settings.last_page = self._listbox.rows.index(row)
