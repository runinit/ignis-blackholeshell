# Phase 4: OSD & Animations

**Status:** In Progress
**Started:** 2025-11-14
**Phase Duration:** Week 4 of Noctalia Design Migration
**Dependencies:** Phase 3 (✅ Complete)

## Overview

Phase 4 focuses on creating a modern On-Screen Display (OSD) system for volume, brightness, and other system notifications with polished animations and micro-interactions. This includes redesigning the existing OSD widgets with Noctalia aesthetics and implementing smooth, delightful animations throughout the shell.

## Phase 4 Objectives

### Primary Goals
- ⏳ Create OSD base window system
- ⏳ Implement Volume OSD with progress bar
- ⏳ Implement Brightness OSD with progress bar
- ⏳ Add smooth fade-in/fade-out animations
- ⏳ Create timeout-based auto-hide
- ⏳ Add icon state indicators

### Secondary Goals
- Keyboard capture OSD
- Media control OSD
- Notification animations
- Tooltip system
- Micro-interactions polish

## Task Breakdown

### Task 1: OSD Base System

**Goal:** Create reusable OSD window base class

**Files to Create:**
- `ignis/modules/osd/__init__.py`
- `ignis/modules/osd/osd_window.py`
- `ignis/scss/osd.scss`

**Implementation Details:**

1. **OSD Window Base Class:**
```python
class OSDWindow(widgets.Window):
    """Base OSD window with auto-hide and animations."""

    def __init__(self, monitor: int = 0):
        self._timeout_id = None
        self._hide_delay = 2000  # 2 seconds

        super().__init__(
            namespace=f"ignis_OSD_{monitor}",
            monitor=monitor,
            anchor=["top"],
            exclusivity="ignore",
            layer="overlay",
            kb_mode="none",
            css_classes=["osd-window"],
            visible=False,
        )

    def show_osd(self, duration: int = None):
        """Show OSD with auto-hide."""
        self._cancel_timeout()
        self.set_visible(True)
        self.remove_css_class("hiding")
        self.add_css_class("showing")

        # Schedule hide
        hide_after = duration if duration else self._hide_delay
        self._timeout_id = GLib.timeout_add(hide_after, self._start_hide)

    def _start_hide(self):
        """Start hide animation."""
        self.remove_css_class("showing")
        self.add_css_class("hiding")
        GLib.timeout_add(300, self._complete_hide)
        return False

    def _complete_hide(self):
        """Complete hide after animation."""
        self.set_visible(False)
        self.remove_css_class("hiding")
        return False

    def _cancel_timeout(self):
        """Cancel pending hide timeout."""
        if self._timeout_id:
            GLib.source_remove(self._timeout_id)
            self._timeout_id = None
```

2. **SCSS Base Styling:**
```scss
.osd-window {
    background: rgba($surface-container, 0.95);
    backdrop-filter: blur(20px);
    border-radius: $radius-l;
    padding: $spacing-l;
    box-shadow: $shadow-elevation-4;

    &.showing {
        animation: osd-fade-in $animation-normal ease;
    }

    &.hiding {
        animation: osd-fade-out $animation-normal ease;
    }
}

@keyframes osd-fade-in {
    from {
        opacity: 0;
        transform: translateY(-20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes osd-fade-out {
    from {
        opacity: 1;
        transform: translateY(0);
    }
    to {
        opacity: 0;
        transform: translateY(-20px);
    }
}
```

**Testing:**
- [ ] OSD window appears on trigger
- [ ] Auto-hide after 2 seconds
- [ ] Fade animations work
- [ ] Multiple monitors supported

**Estimated Time:** 2-3 hours

---

### Task 2: Volume OSD

**Goal:** Create volume control OSD with icon and progress bar

**Files to Create:**
- `ignis/modules/osd/volume_osd.py`

**Implementation Details:**

```python
class VolumeOSD(OSDWindow):
    """Volume OSD with icon and progress bar."""

    def __init__(self, monitor: int = 0):
        self._audio = AudioService.get_default()

        # Create UI
        self._icon = widgets.Icon(
            image=self._get_volume_icon(),
            pixel_size=48,
            css_classes=["osd-icon"],
        )

        self._progress = widgets.LevelBar(
            min_value=0,
            max_value=100,
            value=self._audio.speaker.volume * 100,
            css_classes=["osd-progress"],
        )

        self._label = widgets.Label(
            label=self._get_volume_label(),
            css_classes=["osd-label"],
        )

        super().__init__(monitor)

        self.child = widgets.Box(
            orientation="vertical",
            spacing=12,
            css_classes=["osd-container"],
            child=[
                self._icon,
                self._progress,
                self._label,
            ],
        )

        # Connect to audio service
        self._audio.speaker.connect("notify::volume", self._on_volume_changed)
        self._audio.speaker.connect("notify::muted", self._on_mute_changed)

    def _on_volume_changed(self, *args):
        """Handle volume change."""
        volume = self._audio.speaker.volume * 100
        self._progress.set_value(volume)
        self._label.set_label(self._get_volume_label())
        self._icon.set_image(self._get_volume_icon())
        self.show_osd()

    def _get_volume_icon(self) -> str:
        """Get appropriate volume icon."""
        if self._audio.speaker.muted:
            return "audio-volume-muted-symbolic"

        volume = self._audio.speaker.volume
        if volume == 0:
            return "audio-volume-muted-symbolic"
        elif volume < 0.33:
            return "audio-volume-low-symbolic"
        elif volume < 0.66:
            return "audio-volume-medium-symbolic"
        else:
            return "audio-volume-high-symbolic"

    def _get_volume_label(self) -> str:
        """Get volume percentage label."""
        if self._audio.speaker.muted:
            return "Muted"
        return f"{int(self._audio.speaker.volume * 100)}%"
```

**SCSS Styling:**
```scss
.osd-container {
    min-width: 300px;
    align-items: center;
}

.osd-icon {
    color: $on-surface;
    margin-bottom: $spacing-m;
}

.osd-progress {
    min-height: 8px;
    min-width: 280px;
    border-radius: $radius-full;
    background: $surface-container-high;

    trough {
        min-height: 8px;
        border-radius: $radius-full;
        background: $surface-container-high;
    }

    block {
        background: $primary;
        border-radius: $radius-full;
    }
}

.osd-label {
    font-size: $font-size-l;
    color: $on-surface;
    margin-top: $spacing-s;
}
```

**Testing:**
- [ ] Shows on volume key press
- [ ] Progress bar updates correctly
- [ ] Icon changes based on volume level
- [ ] Mute state handled
- [ ] Label shows percentage

**Estimated Time:** 3-4 hours

---

### Task 3: Brightness OSD

**Goal:** Create brightness control OSD

**Files to Create:**
- `ignis/modules/osd/brightness_osd.py`

**Implementation Details:**

Similar to VolumeOSD but for brightness:

```python
class BrightnessOSD(OSDWindow):
    """Brightness OSD with icon and progress bar."""

    def __init__(self, monitor: int = 0):
        # Use BrightnessService or custom implementation
        # Similar structure to VolumeOSD
        # Icons: display-brightness-symbolic variants
        pass
```

**Testing:**
- [ ] Shows on brightness key press
- [ ] Progress bar updates
- [ ] Icon changes based on level

**Estimated Time:** 2-3 hours

---

### Task 4: Integration & Polish

**Goal:** Integrate OSD with config and add polish

**Files to Modify:**
- `ignis/config.py`

**Implementation Details:**

1. **Config Integration:**
```python
from modules.osd import VolumeOSD, BrightnessOSD

# Initialize OSD for each monitor
for monitor in range(utils.get_n_monitors()):
    VolumeOSD(monitor)
    BrightnessOSD(monitor)
```

2. **Animation Polish:**
- Smooth easing curves
- Proper timing (300ms animations)
- Responsive feedback

**Testing:**
- [ ] OSD appears on all monitors
- [ ] Smooth animations
- [ ] No performance issues
- [ ] Proper layering (above other windows)

**Estimated Time:** 2-3 hours

---

## Directory Structure

After Phase 4 implementation:

```
ignis/modules/osd/
├── __init__.py
├── osd_window.py          # Base OSD window class
├── volume_osd.py          # Volume OSD
└── brightness_osd.py      # Brightness OSD

ignis/scss/
└── osd.scss               # OSD styling

ignis/
├── config.py              # UPDATED - OSD initialization
└── style.scss             # UPDATED - Import osd.scss
```

## Testing Plan

### Unit Tests
- [ ] OSD window show/hide
- [ ] Timeout functionality
- [ ] Animation states

### Integration Tests
- [ ] Volume keys trigger OSD
- [ ] Brightness keys trigger OSD
- [ ] Multi-monitor support
- [ ] Service bindings work

### Visual Tests
- [ ] Blackhole tokens applied
- [ ] Animations smooth
- [ ] Icon states correct
- [ ] Progress bars accurate

### Performance Tests
- [ ] OSD show time <50ms
- [ ] Animation smooth 60fps
- [ ] No memory leaks
- [ ] Minimal CPU usage

## Success Criteria

- ✅ OSD base system implemented
- ✅ Volume OSD functional
- ✅ Brightness OSD functional
- ✅ Smooth fade animations
- ✅ Auto-hide after timeout
- ✅ Icon state indicators
- ✅ All tests passing
- ✅ Blackhole design tokens used

## Time Estimate

**Total:** 9-13 hours (1-2 days)

### Breakdown:
- Task 1: OSD Base System - 2-3 hours
- Task 2: Volume OSD - 3-4 hours
- Task 3: Brightness OSD - 2-3 hours
- Task 4: Integration & Polish - 2-3 hours

## Dependencies

### Completed (Phase 3):
- ✅ Blackhole design tokens
- ✅ Color scheme system
- ✅ Control Center implementation

### Required Services:
- AudioService (Ignis built-in)
- Custom brightness handling or service

## Next Phase

**Phase 5: Final Polish & Optimization** will include:
- Performance optimization
- Memory leak fixes
- Final visual polish
- Documentation
- Package preparation

## References

- Noctalia Shell: OSD implementation
- GNOME Shell: OSD design patterns
- Ignis Services: https://ignis-shell.readthedocs.io/en/latest/services/
- Material Design 3: Feedback and communication
