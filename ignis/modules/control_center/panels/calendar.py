"""
Calendar Panel - Dedicated calendar view with events (Phase 3, Task 4).

Provides a full calendar widget with date selection and upcoming events list.
"""

from ignis import widgets
from .base import Panel
from ..panel_manager import get_panel_manager


class CalendarPanel(Panel):
    """Calendar panel with date picker and events."""

    __gtype_name__ = "CalendarPanel"

    def __init__(self):
        super().__init__(title="Calendar")

        panel_manager = get_panel_manager()

        # Build panel content
        self.child = [
            # Header with back button
            self.create_header(panel_manager),
            # Calendar widget
            widgets.Calendar(
                css_classes=["calendar-widget"],
            ),
            # Upcoming events section
            self._create_events_section(),
        ]

    def _create_events_section(self) -> widgets.Box:
        """Create the upcoming events list section."""
        return widgets.Box(
            orientation="vertical",
            spacing=8,
            css_classes=["calendar-events-section"],
            child=[
                widgets.Label(
                    label="Upcoming Events",
                    css_classes=["calendar-events-title"],
                    halign="start",
                ),
                widgets.ScrolledWindow(
                    min_content_height=200,
                    max_content_height=300,
                    child=widgets.Box(
                        orientation="vertical",
                        spacing=4,
                        css_classes=["calendar-events-list"],
                        child=self._get_example_events(),
                    ),
                ),
            ],
        )

    def _get_example_events(self) -> list:
        """
        Get example events for display.

        In a real implementation, this would fetch events from a calendar service
        (e.g., Evolution Data Server, CalDAV, etc.).
        """
        # Example placeholder events
        example_events = [
            {"title": "Team Meeting", "time": "10:00 AM", "date": "Today"},
            {"title": "Lunch with Alex", "time": "12:30 PM", "date": "Today"},
            {"title": "Project Review", "time": "3:00 PM", "date": "Tomorrow"},
            {"title": "Dentist Appointment", "time": "9:00 AM", "date": "Friday"},
        ]

        return [self._create_event_item(event) for event in example_events]

    def _create_event_item(self, event: dict) -> widgets.Box:
        """Create a single event list item."""
        return widgets.Box(
            css_classes=["calendar-event-item"],
            child=[
                widgets.Box(
                    orientation="vertical",
                    child=[
                        widgets.Label(
                            label=event["title"],
                            css_classes=["calendar-event-title"],
                            halign="start",
                        ),
                        widgets.Label(
                            label=f"{event['time']} • {event['date']}",
                            css_classes=["calendar-event-time"],
                            halign="start",
                        ),
                    ],
                ),
            ],
        )
