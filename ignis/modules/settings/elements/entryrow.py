from ignis import widgets
from .row import SettingsRow
from typing import Callable
from ignis.gobject import Binding


class EntryRow(SettingsRow):
    def __init__(
        self,
        text: str | Binding | None = None,
        on_change: Callable | None = None,
        width: int | None = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        entry_kwargs = {
            "on_change": on_change,
            "text": text,
            "halign": "end",
            "valign": "center",
            "hexpand": True,
        }
        # Only set width_request if width is provided (GTK expects int, not None)
        if width is not None:
            entry_kwargs["width_request"] = width

        self._entry = widgets.Entry(**entry_kwargs)
        self.child.append(self._entry)
