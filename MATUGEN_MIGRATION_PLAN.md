# Matugen Migration & GTK4/Adwaita Styling Plan

## Overview
Replace materialyoucolor-based color generation with matugen 3.0 and update styling to match modern GTK4/Adwaita design patterns (GNOME 48-style).

## Phase 1: Matugen Integration

### 1.1 Create MatugenService
- Replace `services/material/service.py` with matugen-based implementation
- Use `matugen --json hex --dry-run` for color generation
- Maintain cache-first approach for performance
- Keep default_colors.json for fallback

**Key differences from materialyoucolor:**
```python
# OLD (materialyoucolor)
from PIL import Image
from materialyoucolor.quantize import QuantizeCelebi
colors = self.get_colors_from_img(path, dark_mode)

# NEW (matugen)
import subprocess, json
result = subprocess.run(['matugen', 'image', path, '--json', 'hex', '--dry-run'], 
                       capture_output=True, text=True)
data = json.loads(result.stdout)
colors = self._extract_colors(data, dark_mode)
```

### 1.2 Update Color Template
Current template (`services/material/templates/colors.scss`) uses Jinja2 syntax with flat structure:
```scss
$primary: {{ primary }};
$background: {{ background }};
```

Matugen JSON has nested structure:
```json
{
  "colors": {
    "primary": {"dark": "#ffb2ba", "light": "#8f4953"},
    "background": {"dark": "#1a1112", "light": "#fff8f7"}
  }
}
```

Need to flatten for template or update template system.

### 1.3 Regenerate Default Colors
Run matugen on sample_wall.png and save to default_colors.json in new format.

## Phase 2: GTK4/Adwaita Styling Update

### 2.1 Settings Window Titlebar (PRIORITY)
**Current Issue:** Settings uses `widgets.RegularWindow` with no titlebar styling

**GNOME 48 Titlebar Requirements:**
- Use `widgets.HeaderBar` with proper Adwaita styling
- Rounded top corners (12px border-radius)
- Integrated close/minimize/maximize buttons
- Proper spacing and padding (12px horizontal, 6px vertical)
- Title and subtitle support
- Consistent with libadwaita AdwHeaderBar

**Implementation:**
```python
# OLD
class Settings(widgets.RegularWindow):
    def __init__(self):
        super().__init__(
            default_width=1200,
            default_height=700,
            child=widgets.Box(child=[sidebar, content])
        )

# NEW
class Settings(widgets.RegularWindow):
    def __init__(self):
        headerbar = widgets.HeaderBar(
            title="Settings",
            show_title=True,
            css_classes=["settings-headerbar"]
        )
        
        super().__init__(
            default_width=1200,
            default_height=700,
            titlebar=headerbar,  # Set titlebar
            child=widgets.Box(child=[sidebar, content])
        )
```

**CSS Updates:**
```scss
// Add to settings.scss
.settings-headerbar {
    background-color: $surface_container;
    border-bottom: 1px solid $outline_variant;
    border-top-left-radius: 12px;
    border-top-right-radius: 12px;
    padding: 6px 12px;
}

window.settings {
    border-radius: 12px;
}
```

### 2.2 General Adwaita Alignment

**Key Adwaita Design Patterns:**
1. **Surface Hierarchy:**
   - background → surface → surface_container → surface_container_high
   - Use progressive elevation with container variants

2. **Border Radius:**
   - Windows: 12px top corners
   - Cards: 12px all corners
   - Buttons: 6px
   - List items: 6px

3. **Spacing:**
   - Small: 6px
   - Medium: 12px
   - Large: 18px
   - XLarge: 24px

4. **Typography:**
   - Display: 2.5rem (40px)
   - Title: 1.75rem (28px)
   - Heading: 1.25rem (20px)
   - Body: 1rem (16px)
   - Caption: 0.875rem (14px)

5. **Shadows:**
   - Use box-shadow for elevation instead of borders
   - Light: 0 1px 3px rgba(0,0,0,0.12)
   - Medium: 0 2px 6px rgba(0,0,0,0.16)
   - High: 0 4px 12px rgba(0,0,0,0.20)

### 2.3 Component Updates

**Control Center:**
- Update to use surface_container_low for sidebar
- Add proper shadows for elevation
- Round corners on popover

**Launcher:**
- Update search bar to match Adwaita entry style
- Add proper focus rings (2px primary color)

**Notification Center:**
- Use surface_container for notification cards
- Add proper spacing between notifications (12px)

**OSD:**
- Update to floating card style
- Add shadow for elevation
- Round corners (12px)

## Phase 3: Color Mapping

Map matugen colors to current variables:

| Current Variable | Matugen Equivalent |
|-----------------|-------------------|
| primary_paletteKeyColor | palettes.primary.40 (light) / 80 (dark) |
| background | colors.background |
| surface | colors.surface |
| surfaceContainer | colors.surface_container |
| surfaceContainerHigh | colors.surface_container_high |
| primary | colors.primary |
| onPrimary | colors.on_primary |
| outline | colors.outline |
| outlineVariant | colors.outline_variant |

## Phase 4: Implementation Order

1. ✅ Test matugen JSON output format
2. ⏳ Create new MatugenService
3. ⏳ Generate new default_colors.json with matugen
4. ⏳ Update color template for matugen format
5. ⏳ Add HeaderBar to Settings window
6. ⏳ Update settings.scss for GNOME 48 styling
7. ⏳ Test Settings window
8. ⏳ Update other component styling
9. ⏳ Test full UI

## Files to Modify

**Services:**
- `services/material/service.py` → Create matugen-based version
- `services/material/default_colors.json` → Regenerate with matugen
- `services/material/templates/colors.scss` → Update for matugen format

**Settings:**
- `modules/settings/settings.py` → Add HeaderBar
- `scss/settings.scss` → GNOME 48 styling

**Other Components:**
- `scss/control_center.scss` → Adwaita alignment
- `scss/launcher.scss` → Adwaita alignment  
- `scss/notification_center.scss` → Adwaita alignment
- `scss/osd.scss` → Adwaita alignment

## Testing Checklist

- [ ] Matugen color generation works
- [ ] Default colors load on first run
- [ ] Colors update when wallpaper changes
- [ ] Settings window has proper titlebar
- [ ] Settings titlebar looks like GNOME 48
- [ ] All UI components render correctly
- [ ] Dark mode switching works
- [ ] Performance is maintained
