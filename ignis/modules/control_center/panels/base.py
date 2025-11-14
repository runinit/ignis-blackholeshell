"""
Base Panel Class - Foundation for all Control Center panels (Phase 3, Task 2).

Provides common structure and functionality for sub-panels like Calendar, Audio,
WiFi, and Bluetooth.
"""

from ignis import widgets
from typing import Optional


class Panel(widgets.Box):
    """Base class for all Control Center panels."""

    __gtype_name__ = "Panel"

    def __init__(self, title: str, **kwargs):
        """
        Initialize a panel.

        Args:
            title: The panel title to display in the header
            **kwargs: Additional arguments passed to Box
        """
        self._title = title

        # Ensure vertical orientation
        if "orientation" not in kwargs:
            kwargs["orientation"] = "vertical"

        # Add panel CSS class
        if "css_classes" in kwargs:
            if isinstance(kwargs["css_classes"], list):
                kwargs["css_classes"].append("panel")
            else:
                kwargs["css_classes"] = [kwargs["css_classes"], "panel"]
        else:
            kwargs["css_classes"] = ["panel"]

        super().__init__(**kwargs)

    @property
    def title(self) -> str:
        """Get the panel title."""
        return self._title

    def create_header(
        self,
        panel_manager,
        show_back_button: bool = True,
        extra_widgets: Optional[list] = None,
    ) -> widgets.Box:
        """
        Create a standard panel header with back button and title.

        Args:
            panel_manager: The PanelManager instance for navigation
            show_back_button: Whether to show the back button
            extra_widgets: Additional widgets to add to the header (e.g., toggle switches)

        Returns:
            A Box widget containing the header
        """
        header_children = []

        # Back button
        if show_back_button:
            back_button = widgets.Button(
                label="←",
                css_classes=["panel-back-button"],
                on_click=lambda x: panel_manager.go_back(),
            )
            header_children.append(back_button)

        # Title
        title_label = widgets.Label(
            label=self._title,
            css_classes=["panel-title"],
            hexpand=True,
            halign="start",
        )
        header_children.append(title_label)

        # Extra widgets (e.g., toggle switch)
        if extra_widgets:
            header_children.extend(extra_widgets)

        return widgets.Box(
            css_classes=["panel-header"],
            child=header_children,
        )
