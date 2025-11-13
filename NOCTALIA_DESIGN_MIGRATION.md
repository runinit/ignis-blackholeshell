# Noctalia Design Migration Plan

## Overview

This document outlines the plan to adopt Noctalia Shell's design language and layout patterns into Ignis Blackhole Shell. While Noctalia uses Quickshell (QML/Qt), we'll adapt the visual design, layout structure, and UX patterns to our GTK4/Ignis implementation.

## Key Design Philosophy

**Noctalia's Principles:**
- **Minimal & Quiet** - Stays out of the user's way
- **Warm Lavender Aesthetic** - Soft, calming color palette
- **Modular Architecture** - Separate panels for different functions
- **Floating Elements** - Bar and dock can float with rounded corners
- **Adaptive Layouts** - Components adapt to screen position (top/bottom/left/right)

## Component Comparison

### Current Ignis Blackhole Shell vs Noctalia

| Component | Current (Ignis) | Noctalia Equivalent | Changes Needed |
|-----------|-----------------|---------------------|----------------|
| Bar | Top panel with widgets | Adaptive Bar (top/bottom/left/right) | Add position flexibility, floating mode |
| Control Center | Quick settings panel | Control Center panel | Update layout structure |
| Launcher | Application launcher | Launcher panel | Similar functionality |
| Notification Popup | Notification display | Notification + Toast | Add toast system |
| OSD | Volume/brightness OSD | OSD module | Update styling |
| Powermenu | Power options | Session Menu | Rename/restyle |
| Settings | Settings window | Settings panel | Update to panel format |
| Wallpaper Picker | Wallpaper management | Wallpaper panel | Similar functionality |
| **Missing** | - | **Dock** | **NEW: Add dock module** |
| **Missing** | - | **Tooltip system** | **NEW: Add tooltips** |
| **Missing** | - | **Calendar panel** | **NEW: Add calendar** |
| **Missing** | - | **Battery panel** | **NEW: Add battery details** |
| **Missing** | - | **Audio panel** | **NEW: Add audio mixer** |
| **Missing** | - | **Bluetooth panel** | **NEW: Add BT manager** |
| **Missing** | - | **WiFi panel** | **NEW: Add WiFi manager** |
| Background | - | Background module | **NEW: Add background layer** |

## Design Token Migration

### Typography

**Noctalia Font Scale:**
```scss
// Migrate from current to Noctalia scale
$font-size-xxs: 8px;   // Tiny labels
$font-size-xs: 9px;    // Small captions
$font-size-s: 10px;    // Captions
$font-size-m: 11px;    // Body text (default)
$font-size-l: 13px;    // Subheadings
$font-size-xl: 16px;   // Headings
$font-size-xxl: 18px;  // Large headings
$font-size-xxxl: 24px; // Display text

// Font weights
$font-weight-regular: 400;
$font-weight-medium: 500;
$font-weight-semibold: 600;
$font-weight-bold: 700;
```

### Border Radius

**Noctalia Radius Scale:**
```scss
// Current approach uses fixed values
// Noctalia uses ratio-based scaling

$radius-ratio: 1.0;  // User-configurable
$screen-radius-ratio: 1.0;

$radius-xxs: 4px * $radius-ratio;   // Small buttons, chips
$radius-xs: 8px * $radius-ratio;    // Buttons
$radius-s: 12px * $radius-ratio;    // Cards, smaller panels
$radius-m: 16px * $radius-ratio;    // Panels
$radius-l: 20px * $radius-ratio;    // Large panels, popups
$radius-screen: 20px * $screen-radius-ratio;  // Screen corners
```

### Spacing

**Noctalia Spacing Scale:**
```scss
// UI scale ratio for accessibility
$ui-scale-ratio: 1.0;  // User-configurable

$spacing-xxs: 2px * $ui-scale-ratio;   // Minimal gaps
$spacing-xs: 4px * $ui-scale-ratio;    // Tight spacing
$spacing-s: 6px * $ui-scale-ratio;     // Small spacing
$spacing-m: 9px * $ui-scale-ratio;     // Medium spacing
$spacing-l: 13px * $ui-scale-ratio;    // Large spacing
$spacing-xl: 18px * $ui-scale-ratio;   // Extra large spacing
```

### Opacity Levels

**Noctalia Opacity Scale:**
```scss
$opacity-none: 0.0;
$opacity-light: 0.25;
$opacity-medium: 0.5;
$opacity-heavy: 0.75;
$opacity-almost: 0.95;
$opacity-full: 1.0;
```

### Shadows

**Noctalia Shadow System:**
```scss
// Sophisticated shadow with offset and blur
$shadow-opacity: 0.85;
$shadow-blur-ratio: 1.0;
$shadow-max-blur: 22px;
$shadow-offset-x: 0px;  // From settings
$shadow-offset-y: 2px;  // From settings

// Computed shadow
box-shadow:
    $shadow-offset-x
    $shadow-offset-y
    ($shadow-max-blur * $shadow-blur-ratio)
    rgba(0, 0, 0, $shadow-opacity);
```

### Animation

**Noctalia Animation System:**
```scss
// Animation speeds (user-configurable via animationSpeed multiplier)
$animation-faster: 75ms;
$animation-fast: 150ms;
$animation-normal: 300ms;
$animation-slow: 450ms;
$animation-slowest: 750ms;

// Delays
$delay-tooltip: 300ms;
$delay-tooltip-long: 1200ms;
$delay-pill: 500ms;

// Easing functions
// Use: cubic-bezier for custom easing
// OutBack for overshoot effects on scale
```

### Colors - Lavender Theme

**Noctalia's Warm Lavender Palette:**
```scss
// Noctalia uses a warm lavender base
// We'll create a similar palette while keeping Material You generation

// Primary - Lavender accent
$primary: #b4a5d8;              // Soft lavender
$primary-bright: #c7b8eb;       // Lighter lavender
$primary-dim: #9987bf;          // Darker lavender

// Backgrounds (Dark mode)
$background-dark: #1a1720;       // Deep purple-black
$surface-dark: #221e2b;          // Slightly lighter
$surface-container-low: #2a2533;
$surface-container: #322d3c;
$surface-container-high: #3a3545;

// Backgrounds (Light mode)
$background-light: #faf8fc;      // Nearly white with purple tint
$surface-light: #f4f1f8;
$surface-container-low: #eee9f4;
$surface-container: #e8e2f0;
$surface-container-high: #e1dae8;

// Semantic colors
$on-surface: rgba(255, 255, 255, 0.87);  // Dark mode text
$on-surface-variant: rgba(255, 255, 255, 0.60);
$outline: rgba(255, 255, 255, 0.20);
$outline-variant: rgba(255, 255, 255, 0.10);
```

## Layout Structure Changes

### 1. Bar Module Redesign

**Current Structure:**
```
Top bar (fixed position)
├── Left section (workspaces, apps)
├── Center section (clock)
└── Right section (system tray, indicators)
```

**Noctalia Structure:**
```
Adaptive Bar (top/bottom/left/right)
├── Floating mode toggle (with margins)
├── Three sections (start/center/end)
├── Dynamic widget loading system
├── Corner radius adaptation
│   ├── No radius (-1): Square corners
│   ├── Normal (0): Standard rounded
│   ├── Inverted (1-2): Inverted corners
└── Right-click → Open Control Center
```

**Implementation Plan:**
1. Add `position` option: "top", "bottom", "left", "right"
2. Add `floating` option (boolean) with margins
3. Implement widget loader system for dynamic sections
4. Add corner radius states
5. Update SCSS for all position variants

### 2. Dock Module (NEW)

**Noctalia Dock Features:**
```
Bottom-anchored application dock
├── Auto-hide with peek window (1px trigger zone)
├── Icon size based on density setting
├── Three app states:
│   ├── Running pinned (full opacity)
│   ├── Not running pinned (60% opacity)
│   └── Running non-pinned (full opacity)
├── Active indicator bar (small colored bar under icon)
├── Colorization shader for inactive apps
├── Scale animation on hover (Easing.OutBack)
└── Spacing adjustment for bar collision
```

**Implementation Plan:**
1. Create `modules/dock/` directory
2. Implement app tracking via ApplicationsService
3. Add pinning system (stored in user_options)
4. Implement auto-hide with hover detection
5. Style with Noctalia aesthetics (radius-l, shadows)
6. Add smooth animations (GTK4 transitions)

### 3. Panel System Architecture

**Current Approach:**
- Windows for each component
- Mix of regular windows and layer shell

**Noctalia Approach:**
- Unified panel system
- Panels slide in/out from screen edges
- Panels can be anchored or floating
- Panel backdrop/scrim for focus

**Migration:**
- Keep current window-based approach (GTK4 layer shell)
- Add panel manager service to coordinate showing/hiding
- Implement slide-in animations
- Add backdrop overlay for modal panels

### 4. Control Center Redesign

**Current Layout:**
```
Control Center (slide from right)
├── Header
├── Quick Settings Grid
├── Sliders (brightness, volume)
├── Media Player
└── Notification Center
```

**Noctalia Layout:**
```
Control Center (slide from edge, near bar button)
├── Header with sections
├── Quick Settings Capsules (rounded buttons)
│   ├── WiFi → Opens WiFi panel
│   ├── Bluetooth → Opens Bluetooth panel
│   ├── Audio → Opens Audio panel
│   └── Battery → Opens Battery panel
├── Sliders (horizontal, with value indicators)
├── Calendar widget
└── Notification list
```

**Implementation Plan:**
1. Reorganize layout hierarchy
2. Update quick settings to "capsule" style
3. Add sub-panel navigation (WiFi, Bluetooth, etc.)
4. Integrate calendar widget
5. Update slider styling
6. Add panel stacking for sub-panels

### 5. New Panel Modules

**Priority 1 - Essential Panels:**

**Calendar Panel:**
```python
# modules/panels/calendar.py
- Month view calendar
- Day/event list
- Integration with system calendar
- Noctalia styling (rounded, shadows)
```

**Audio Panel:**
```python
# modules/panels/audio.py
- Application volume mixer
- Output device selector
- Input device selector
- Volume balance controls
```

**WiFi Panel:**
```python
# modules/panels/wifi.py
- Available networks list
- Saved networks
- Network strength indicators
- Connect/disconnect actions
```

**Bluetooth Panel:**
```python
# modules/panels/bluetooth.py
- Paired devices list
- Available devices
- Connection status
- Pairing interface
```

**Priority 2 - Enhancement Panels:**

**Battery Panel:**
```python
# modules/panels/battery.py
- Battery percentage graph
- Time remaining estimate
- Power profile selector
- Battery health info
```

**Session Menu:**
```python
# modules/panels/session_menu.py
- Rename from Powermenu
- User avatar
- Lock, logout, suspend, restart, shutdown
- User switching
```

### 6. Widget System

**Noctalia Custom Widgets (adapt to Ignis):**

Priority widgets to create:
- `NButton` → Capsule-style button with hover states
- `NToggle` → Toggle switch (vs checkbox)
- `NSlider` → Horizontal slider with value display
- `NIconButton` → Circular icon button
- `NIcon` → Icon with proper sizing
- `NDivider` → Subtle divider line
- `NHeader` → Panel header with back button
- `NScrollView` → Scrollable area with fade effects

### 7. OSD Updates

**Current OSD:**
```
Volume/Brightness popup
├── Icon
├── Progress bar
└── Percentage text
```

**Noctalia OSD:**
```
Floating rounded popup (screen center or edge)
├── Icon (larger, centered)
├── Circular progress indicator
├── Value text
├── Fade in/out animations
└── Auto-hide timer
```

## Color Theme Strategy

### Dual Approach

1. **Default Lavender Theme** (Noctalia-inspired)
   - Pre-defined lavender palette
   - Warm, purple-tinted neutrals
   - Ships as default

2. **Material You Dynamic** (Keep existing)
   - Generate from wallpaper
   - User can toggle between static lavender and dynamic
   - Option in settings: "Use wallpaper colors" (boolean)

### Implementation

```python
# user_options.py
class Material(OptionsGroup):
    use_wallpaper_colors: bool = False  # False = Lavender, True = Dynamic
    dark_mode: bool = True
    colors: dict[str, str] = {}
    # ... existing options

# services/material/service.py
def get_colors(self):
    if not user_options.material.use_wallpaper_colors:
        # Return static lavender palette
        return self._load_lavender_theme()
    else:
        # Use existing dynamic generation
        return self._generate_from_wallpaper()
```

## File Structure Changes

### New Directories

```
ignis/
├── modules/
│   ├── dock/                    # NEW: Dock module
│   │   ├── __init__.py
│   │   ├── dock.py
│   │   └── dock_item.py
│   ├── panels/                  # NEW: Panel subdirectory
│   │   ├── __init__.py
│   │   ├── audio.py
│   │   ├── battery.py
│   │   ├── bluetooth.py
│   │   ├── calendar.py
│   │   └── wifi.py
│   └── background/              # NEW: Background layer
│       ├── __init__.py
│       └── background.py
├── widgets/                     # NEW: Custom widgets
│   ├── __init__.py
│   ├── n_button.py
│   ├── n_toggle.py
│   ├── n_slider.py
│   ├── n_icon_button.py
│   ├── n_header.py
│   └── n_divider.py
└── scss/
    ├── _noctalia_tokens.scss    # NEW: Noctalia design tokens
    ├── dock.scss                # NEW: Dock styling
    ├── panels.scss              # NEW: Panel styling
    └── widgets.scss             # NEW: Custom widget styling
```

### Updated Files

```
ignis/
├── user_options.py              # Add dock options, panel options
├── config.py                    # Initialize new modules
├── scss/
│   ├── bar.scss                 # Update for adaptive positioning
│   ├── control_center.scss      # Redesign layout
│   ├── osd.scss                 # Update styling
│   └── style.scss               # Import new SCSS files
└── services/
    └── material/
        ├── lavender_theme.json  # NEW: Static lavender palette
        └── service.py           # Add theme switching logic
```

## Implementation Phases

### Phase 1: Foundation (Week 1)
- ✅ Analyze Noctalia structure (DONE)
- ⏳ Create design migration document (IN PROGRESS)
- 🔲 Create `_noctalia_tokens.scss` with all design tokens
- 🔲 Create lavender theme JSON
- 🔲 Add theme switching logic to MaterialService
- 🔲 Create custom widgets directory and base widgets

### Phase 2: Core Components (Week 2)
- 🔲 Update Bar module for adaptive positioning
- 🔲 Add floating mode to Bar
- 🔲 Update Bar SCSS for all positions
- 🔲 Create Dock module (basic version)
- 🔲 Implement app tracking in Dock
- 🔲 Add auto-hide to Dock
- 🔲 Style Dock with Noctalia aesthetics

### Phase 3: Panels (Week 3)
- 🔲 Redesign Control Center layout
- 🔲 Create Calendar panel
- 🔲 Create Audio panel
- 🔲 Create WiFi panel
- 🔲 Create Bluetooth panel
- 🔲 Implement panel navigation system
- 🔲 Add panel slide animations

### Phase 4: Polish (Week 4)
- 🔲 Update OSD with new styling
- 🔲 Add tooltip system
- 🔲 Create Battery panel
- 🔲 Rename Powermenu → Session Menu
- 🔲 Update all animations to Noctalia timing
- 🔲 Add backdrop/scrim for modal panels
- 🔲 Performance testing and optimization

### Phase 5: Documentation (Week 5)
- 🔲 Update CLAUDE_INSTRUCTIONS.md
- 🔲 Create migration guide for users
- 🔲 Screenshot all new components
- 🔲 Update README with new features
- 🔲 Create video demo

## Breaking Changes for Users

### Configuration Changes

**user_options.json changes:**
```json
{
  "bar": {
    "position": "top",           // NEW: top/bottom/left/right
    "floating": false,           // NEW: floating mode
    "float_margin": 8,           // NEW: margin when floating
    "density": "comfortable"     // NEW: compact/comfortable/spacious
  },
  "dock": {                      // NEW section
    "enabled": true,
    "position": "bottom",
    "size": 1.0,
    "auto_hide": true,
    "pinned_apps": []
  },
  "material": {
    "use_wallpaper_colors": false  // NEW: false = lavender, true = dynamic
  }
}
```

### Visual Changes

- Bar can now be positioned on any edge
- New dock at screen bottom (optional)
- Control Center has reorganized layout
- Quick settings are now "capsules"
- New sub-panels for WiFi, Bluetooth, Audio
- OSD has circular progress instead of bar
- Lavender color scheme by default

## Testing Checklist

### Functionality Tests
- [ ] Bar displays correctly in all positions (top/bottom/left/right)
- [ ] Bar floating mode works with margins
- [ ] Dock shows pinned and running apps
- [ ] Dock auto-hide triggers correctly
- [ ] Dock app launching works
- [ ] Control Center opens/closes smoothly
- [ ] All sub-panels navigate correctly
- [ ] Calendar displays current month
- [ ] Audio panel shows all apps/devices
- [ ] WiFi panel lists networks
- [ ] Bluetooth panel shows devices
- [ ] OSD appears for volume/brightness
- [ ] Theme switching works (lavender ↔ dynamic)

### Visual Tests
- [ ] All components use Noctalia design tokens
- [ ] Border radius matches Noctalia scale
- [ ] Spacing is consistent across components
- [ ] Shadows render correctly
- [ ] Animations are smooth
- [ ] Dark/light mode both look good
- [ ] Multi-monitor support works
- [ ] No visual glitches or flicker

### Performance Tests
- [ ] Startup time remains under 5s
- [ ] No lag when showing panels
- [ ] Dock auto-hide is responsive
- [ ] Animations don't drop frames
- [ ] Memory usage is acceptable

## Resources

### Noctalia References
- Repository: https://github.com/noctalia-dev/noctalia-shell
- Documentation: https://docs.noctalia.dev
- Screenshots: Assets/Screenshots/*.png
- Style definitions: Commons/Style.qml
- Widget library: Widgets/*.qml

### Ignis References
- Framework docs: https://github.com/linkfrg/ignis
- Current implementation: ignis/* files
- Performance guide: OPTIMIZATION_SUMMARY.md
- Development guide: CLAUDE_INSTRUCTIONS.md

---

**Status:** Planning Phase
**Started:** 2025-11-13
**Target Completion:** 5 weeks
**Assignee:** Development team
