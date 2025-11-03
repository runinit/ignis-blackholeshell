from ignis import widgets
from .row import SettingsRow
from typing import Callable
from ignis.gobject import Binding


class ComboBoxRow(SettingsRow):
    """A settings row with a combo box dropdown."""

    def __init__(
        self,
        items: list[str],
        selected: int | Binding = 0,
        on_change: Callable | None = None,
        **kwargs,
    ):
        super().__init__(**kwargs)

        # Wrapper to convert on_selected signature (passes string) to on_change style (expects index)
        def on_selected_wrapper(dropdown, selected_string):
            if on_change:
                try:
                    # Convert selected string to index
                    selected_index = items.index(selected_string)
                    on_change(dropdown, selected_index)
                except ValueError:
                    pass  # String not in list, ignore

        self._combo_box = widgets.DropDown(
            items=items,
            selected=selected,
            on_selected=on_selected_wrapper if on_change else None,
            halign="end",
            valign="center",
            hexpand=True,
        )

        self.child.append(self._combo_box)
