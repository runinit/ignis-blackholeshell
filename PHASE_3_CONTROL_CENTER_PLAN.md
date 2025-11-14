# Phase 3: Control Center & Panel System

**Status:** ✅ Complete
**Started:** 2025-11-14
**Completed:** 2025-11-14
**Phase Duration:** Week 3 of Noctalia Design Migration
**Dependencies:** Phase 2 (✅ Complete)

## Overview

Phase 3 focuses on redesigning the Control Center with Noctalia-inspired aesthetics and implementing a modern panel navigation system. This includes updating existing quick settings and creating new dedicated panels for Calendar, Audio, WiFi, Bluetooth, and other system functions.

## Phase 3 Objectives

### Primary Goals
- ✅ Redesign Control Center with Blackhole design tokens (Task 1 - Complete)
- ✅ Implement panel navigation system (Task 2 - Complete)
- ✅ Quick settings maintained (Task 3 - Complete)
- ✅ Create Calendar panel (Task 4 - Complete)
- ✅ Create Audio panel with volume controls (Task 5 - Complete)
- ✅ Create Network panel (WiFi) (Task 6 - Complete)
- ✅ Create Bluetooth panel (Task 7 - Complete)

### Secondary Goals
- ✅ Smooth panel transitions
- ✅ Contextual navigation (back button)
- ⏳ Media player controls enhancement (Future)
- ⏳ Notification center integration (Future)
- ⏳ Performance optimization (Future)

## Task Breakdown

### Task 1: Control Center Base Redesign

**Goal:** Update Control Center container with Noctalia aesthetics

**Files to Modify:**
- `ignis/modules/control_center/control_center.py`
- `ignis/scss/control_center.scss`

**Implementation Details:**

1. **Update Control Center Container:**
```python
class ControlCenter(widgets.Window):
    def __init__(self):
        super().__init__(
            namespace="ignis_CONTROL_CENTER",
            anchor=["top", "right"],
            exclusivity="normal",
            layer="overlay",
            css_classes=["control-center"],
            visible=False,
            child=widgets.Box(
                orientation="vertical",
                spacing=12,
                css_classes=["control-center-container"],
                child=[
                    self._create_header(),
                    self._create_quick_settings(),
                    self._create_media_player(),
                    self._create_notifications(),
                ],
            ),
        )
```

2. **SCSS Redesign:**
```scss
.control-center {
    background: rgba($surface-container, 0.95);
    backdrop-filter: blur(20px);
    border-radius: $radius-l 0 0 $radius-l;
    padding: $spacing-m;
    box-shadow: $shadow-elevation-4;
    min-width: 400px;
    max-width: 400px;
}

.control-center-container {
    gap: $spacing-m;
}
```

**Testing:**
- [x] Control Center opens on right edge
- [x] Blackhole tokens applied correctly
- [x] Backdrop blur effect works
- [x] Proper shadow elevation

**Estimated Time:** 3-4 hours

---

### Task 2: Panel Navigation System

**Goal:** Create panel navigation framework for sub-panels

**Files to Create:**
- `ignis/modules/control_center/panel_manager.py`
- `ignis/modules/control_center/panels/__init__.py`

**Implementation Details:**

1. **Panel Manager:**
```python
class PanelManager:
    """Manages panel navigation and transitions."""

    def __init__(self):
        self._current_panel = None
        self._panel_stack = []
        self._panels = {}

    def register_panel(self, name: str, panel):
        """Register a panel."""
        self._panels[name] = panel

    def show_panel(self, name: str):
        """Show a panel and add to navigation stack."""
        if self._current_panel:
            self._panel_stack.append(self._current_panel)
        self._current_panel = name
        # Emit signal for UI update

    def go_back(self):
        """Navigate back to previous panel."""
        if self._panel_stack:
            self._current_panel = self._panel_stack.pop()
```

2. **Panel Base Class:**
```python
class Panel(widgets.Box):
    """Base class for all panels."""

    def __init__(self, title: str, **kwargs):
        self._title = title
        super().__init__(
            orientation="vertical",
            css_classes=["panel"],
            **kwargs
        )
```

**Testing:**
- [x] Panel registration works
- [x] Navigation stack functions
- [x] Back button navigation
- [x] Panel transitions smooth

**Estimated Time:** 4-5 hours

---

### Task 3: Quick Settings Grid Update

**Goal:** Modernize quick settings layout with Noctalia design

**Files to Modify:**
- `ignis/modules/control_center/quick_settings.py`
- `ignis/scss/control_center.scss`

**Implementation Details:**

1. **Grid Layout:**
```python
class QuickSettings(widgets.Box):
    def __init__(self):
        super().__init__(
            orientation="vertical",
            spacing=8,
            css_classes=["quick-settings"],
            child=[
                # Row 1: WiFi, Bluetooth, Airplane Mode
                widgets.Box(
                    spacing=8,
                    child=[
                        QSButton("wifi", on_click=self._open_wifi_panel),
                        QSButton("bluetooth", on_click=self._open_bluetooth_panel),
                        QSButton("airplane"),
                    ],
                ),
                # Row 2: Dark Mode, DND, Screen Lock
                widgets.Box(
                    spacing=8,
                    child=[
                        QSButton("dark-mode"),
                        QSButton("dnd"),
                        QSButton("lock"),
                    ],
                ),
            ],
        )
```

2. **QS Button Styling:**
```scss
.qs-button {
    background: $surface-container-high;
    border-radius: $radius-m;
    padding: $spacing-m;
    min-width: 100px;
    min-height: 80px;
    transition: all $animation-fast ease;

    &:hover {
        background: $surface-container-highest;
        transform: scale(1.02);
    }

    &.active {
        background: $primary-container;
        color: $on-primary-container;
    }
}
```

**Testing:**
- [x] Grid layout displays correctly
- [x] Buttons toggle properly
- [x] Active states work
- [x] Panel navigation triggers

**Estimated Time:** 3-4 hours

---

### Task 4: Calendar Panel

**Goal:** Create dedicated calendar panel

**Files to Create:**
- `ignis/modules/control_center/panels/calendar.py`

**Implementation Details:**

```python
class CalendarPanel(Panel):
    def __init__(self):
        super().__init__(title="Calendar")

        self.child = [
            # Header with back button
            widgets.Box(
                child=[
                    widgets.Button(
                        label="←",
                        on_click=lambda: panel_manager.go_back(),
                    ),
                    widgets.Label(label="Calendar"),
                ],
            ),
            # Calendar widget
            widgets.Calendar(
                css_classes=["calendar-widget"],
            ),
            # Upcoming events
            self._create_events_list(),
        ]
```

**Testing:**
- [x] Calendar displays correctly
- [x] Month navigation works
- [x] Date selection
- [x] Events list updates

**Estimated Time:** 4-5 hours

---

### Task 5: Audio Panel

**Goal:** Create audio control panel with device switching

**Files to Create:**
- `ignis/modules/control_center/panels/audio.py`

**Implementation Details:**

```python
class AudioPanel(Panel):
    def __init__(self):
        super().__init__(title="Audio")

        audio = AudioService.get_default()

        self.child = [
            # Header
            self._create_header(),
            # Output devices
            widgets.Label(label="Output Devices"),
            widgets.Box(
                orientation="vertical",
                child=[
                    DeviceRow(device) for device in audio.speakers
                ],
            ),
            # Input devices
            widgets.Label(label="Input Devices"),
            widgets.Box(
                orientation="vertical",
                child=[
                    DeviceRow(device) for device in audio.microphones
                ],
            ),
        ]
```

**Testing:**
- [x] Lists all audio devices
- [x] Device switching works
- [x] Volume controls functional
- [x] Mute toggles work

**Estimated Time:** 5-6 hours

---

### Task 6: Network (WiFi) Panel

**Goal:** Create WiFi network list and connection panel

**Files to Create:**
- `ignis/modules/control_center/panels/network.py`

**Implementation Details:**

```python
class NetworkPanel(Panel):
    def __init__(self):
        super().__init__(title="WiFi")

        network = NetworkService.get_default()

        self.child = [
            # Header with toggle
            self._create_header_with_toggle(),
            # Connected network
            self._create_connected_section(),
            # Available networks
            widgets.ScrolledWindow(
                child=widgets.Box(
                    orientation="vertical",
                    child=[
                        NetworkRow(ap) for ap in network.wifi.access_points
                    ],
                ),
            ),
        ]
```

**Testing:**
- [x] Lists available networks
- [x] Shows signal strength
- [x] Connection works
- [x] Password dialog

**Estimated Time:** 5-6 hours

---

### Task 7: Bluetooth Panel

**Goal:** Create Bluetooth device management panel

**Files to Create:**
- `ignis/modules/control_center/panels/bluetooth.py`

**Implementation Details:**

```python
class BluetoothPanel(Panel):
    def __init__(self):
        super().__init__(title="Bluetooth")

        bluetooth = BluetoothService.get_default()

        self.child = [
            # Header with toggle
            self._create_header_with_toggle(),
            # Paired devices
            widgets.Label(label="Paired Devices"),
            widgets.Box(
                orientation="vertical",
                child=[
                    DeviceRow(device) for device in bluetooth.devices
                    if device.paired
                ],
            ),
            # Available devices
            widgets.Label(label="Available Devices"),
            widgets.Box(
                orientation="vertical",
                child=[
                    DeviceRow(device) for device in bluetooth.devices
                    if not device.paired
                ],
            ),
        ]
```

**Testing:**
- [x] Lists paired devices
- [x] Shows available devices
- [x] Pairing works
- [x] Connect/disconnect functions

**Estimated Time:** 5-6 hours

---

### Task 8: Integration & Polish

**Goal:** Integrate all panels and add polish

**Files to Modify:**
- `ignis/modules/control_center/control_center.py`
- `ignis/scss/control_center.scss`

**Implementation Details:**

1. **Panel Container:**
```python
self._panel_container = widgets.Stack(
    transition_type="slide_left_right",
    css_classes=["panel-container"],
)

# Register all panels
self._panel_container.add_named(QuickSettings(), "main")
self._panel_container.add_named(CalendarPanel(), "calendar")
self._panel_container.add_named(AudioPanel(), "audio")
self._panel_container.add_named(NetworkPanel(), "network")
self._panel_container.add_named(BluetoothPanel(), "bluetooth")
```

2. **Animations:**
```scss
.panel-container {
    transition: all $animation-normal ease;
}

.panel {
    animation: slideIn $animation-normal ease;
}

@keyframes slideIn {
    from {
        transform: translateX(100%);
        opacity: 0;
    }
    to {
        transform: translateX(0);
        opacity: 1;
    }
}
```

**Testing:**
- [x] All panels accessible
- [x] Transitions smooth
- [x] Back navigation works
- [x] No memory leaks

**Estimated Time:** 4-5 hours

---

## Directory Structure

After Phase 3 implementation:

```
ignis/modules/control_center/
├── __init__.py
├── control_center.py          # Main window
├── panel_manager.py            # NEW - Navigation system
├── quick_settings.py           # UPDATED - Modern grid
├── qs_button.py               # UPDATED - Noctalia style
├── panels/                     # NEW
│   ├── __init__.py
│   ├── base.py                # Base Panel class
│   ├── calendar.py            # Calendar panel
│   ├── audio.py               # Audio devices
│   ├── network.py             # WiFi panel
│   └── bluetooth.py           # Bluetooth panel
├── widgets/                    # Shared widgets
│   ├── device_row.py
│   ├── network_row.py
│   └── header.py
└── menu.py                     # Existing

ignis/scss/
├── control_center.scss        # UPDATED - Noctalia design
└── panels.scss                # NEW - Panel styles
```

## Testing Plan

### Unit Tests
- [x] Panel navigation system
- [x] Panel registration
- [x] Back button navigation
- [x] Device list population

### Integration Tests
- [x] Panel transitions
- [x] Quick settings to panels
- [x] Service integration
- [x] State persistence

### Visual Tests
- [x] Blackhole tokens applied
- [x] Animations smooth
- [x] Responsive layouts
- [x] Dark mode support

### Performance Tests
- [x] Control Center open time <200ms
- [x] Panel transitions <300ms
- [x] No layout shifts
- [x] Memory usage acceptable

## Success Criteria

- ✅ Control Center uses Blackhole design tokens
- ✅ Panel navigation system implemented
- ✅ All 4 panels created (Calendar, Audio, WiFi, Bluetooth)
- ✅ Quick settings grid modernized
- ✅ Smooth panel transitions
- ✅ Back button navigation works
- ✅ All tests passing
- ✅ Performance targets met

## Time Estimate

**Total:** 33-41 hours (4-5 days)

### Breakdown:
- Task 1: Control Center Base - 3-4 hours
- Task 2: Panel Navigation - 4-5 hours
- Task 3: Quick Settings - 3-4 hours
- Task 4: Calendar Panel - 4-5 hours
- Task 5: Audio Panel - 5-6 hours
- Task 6: Network Panel - 5-6 hours
- Task 7: Bluetooth Panel - 5-6 hours
- Task 8: Integration & Polish - 4-5 hours

## Dependencies

### Completed (Phase 2):
- ✅ Blackhole design tokens
- ✅ Color scheme system
- ✅ Bar and Dock implementation
- ✅ Settings infrastructure

### Required Services:
- AudioService (Ignis built-in)
- NetworkService (Ignis built-in)
- BluetoothService (Ignis built-in)
- Calendar widget (GTK built-in)

## Next Phase

**Phase 4: OSD & Animations** will include:
- On-Screen Display redesign
- Volume/brightness OSD
- Animation polish
- Tooltip system
- Micro-interactions

## References

- Noctalia Shell: https://github.com/noctalia-dev/noctalia-shell
- Noctalia Control Center: Components/ControlCenter/
- Ignis Services: https://ignis-shell.readthedocs.io/en/latest/services/
- Material Design 3: Panels and Navigation
