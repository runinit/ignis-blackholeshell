from ignis.variable import Variable
from .elements import SettingsPage
from ignis import widgets

# Create a more visible fallback page for debugging
fallback_page = SettingsPage(
    name="Settings",
    groups=[
        widgets.Label(
            label="Select a category from the sidebar",
            css_classes=["settings-page-name"]
        )
    ]
)
active_page = Variable(value=fallback_page)
