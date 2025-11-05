from ignis import widgets
from ignis import utils
from ignis.services.audio import AudioService
from ..shared_widgets import MaterialVolumeSlider

# Lazy initialization - don't initialize services at import time
_audio = None


def get_audio():
    """Lazy load AudioService"""
    global _audio
    if _audio is None:
        _audio = AudioService.get_default()
    return _audio


class OSD(widgets.Window):
    def __init__(self):
        audio = get_audio()
        super().__init__(
            layer="overlay",
            anchor=["bottom"],
            namespace="ignis_OSD",
            visible=False,
            css_classes=["rec-unset"],
            child=widgets.Box(
                css_classes=["osd"],
                child=[
                    widgets.Icon(
                        pixel_size=26,
                        style="margin-right: 0.5rem;",
                        image=audio.speaker.bind("icon_name"),
                    ),
                    MaterialVolumeSlider(stream=audio.speaker, sensitive=False),
                ],
            ),
        )

    def set_property(self, property_name, value):
        if property_name == "visible":
            self.__update_visible()

        super().set_property(property_name, value)

    @utils.debounce(3000)
    def __update_visible(self) -> None:
        super().set_property("visible", False)
