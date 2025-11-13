# Ignis Blackhole Shell - Development Guide

## Project Overview

**Ignis Blackhole Shell** is a modern, Material Design 3-themed desktop shell configuration for Wayland compositors (Hyprland, Niri). Built with Python and GTK4 using the Ignis framework, it provides a complete desktop environment including a top bar, control center, launcher, notification system, OSD, and settings interface.

### Key Features
- **Material Design 3 theming** with dynamic color generation from wallpapers
- **Multi-monitor support** for all UI components
- **Wallpaper slideshow system** with transitions via swww
- **Performance-optimized** with lazy loading and caching (5s cold start)
- **Modular architecture** with separate services and UI modules
- **Live CSS reloading** for rapid theme development
- **GTK4/Adwaita design patterns** for modern GNOME aesthetics

### Project Structure
```
ignis-blackholeshell/
├── ignis/                          # Main configuration directory
│   ├── config.py                   # Entry point, initializes all modules
│   ├── user_options.py            # User settings/options manager
│   ├── modules/                    # UI components
│   │   ├── bar/                   # Top panel
│   │   ├── control_center/        # Quick settings panel
│   │   ├── launcher/              # Application launcher
│   │   ├── notification_popup/    # Notification display
│   │   ├── osd/                   # Volume/brightness OSD
│   │   ├── powermenu/             # Power options menu
│   │   ├── settings/              # Settings window
│   │   └── wallpaper_picker/      # Wallpaper management
│   ├── services/                   # Backend services
│   │   ├── material/              # Material You color generation
│   │   └── wallpaper_slideshow/   # Wallpaper rotation service
│   ├── scss/                       # Stylesheets (SCSS)
│   └── icons/                      # Custom icons
├── ref-ignis/                      # Ignis framework (git submodule)
└── docs/                           # Project documentation
    ├── OPTIMIZATION_SUMMARY.md
    ├── MATUGEN_MIGRATION_PLAN.md
    └── PERFORMANCE_ANALYSIS.md
```

## Technology Stack

### Core Technologies
- **Python 3.13+** - Primary language
- **GTK4** - UI framework (via PyGObject)
- **Ignis Framework** - Custom shell framework built on GTK4
- **SCSS/Sass** - Styling with dynamic variable injection
- **GLib/Gio** - Async operations and system integration

### Key Dependencies
- **PyGObject (gi)** - GTK4 Python bindings
- **matugen** - Material You color palette generation (migrating to)
- **materialyoucolor** - Current color generation library (being phased out)
- **swww** - Wayland wallpaper daemon with transitions
- **Hyprland/Niri** - Wayland compositor integration

### Services & APIs
- WallpaperService - Wallpaper management
- MaterialService - Dynamic color theming
- NetworkService - Network status (via NetworkManager)
- BluetoothService - Bluetooth management
- AudioService - Volume/audio control
- NotificationService - System notifications
- MprisService - Media player control
- RecorderService - Screen recording
- HyprlandService - Window manager integration

## Development Environment Setup

### Prerequisites
```bash
# Install system dependencies (Arch Linux example)
sudo pacman -S python python-gobject gtk4 libadwaita sassc

# Install matugen for color generation
# See: https://github.com/InioX/matugen

# Install swww for wallpaper transitions
# See: https://github.com/LGFae/swww
```

### Getting Started
1. Clone the repository with submodules:
   ```bash
   git clone --recursive <repository-url>
   cd ignis-blackholeshell
   ```

2. Set up Python virtual environment (if needed):
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt  # if exists
   ```

3. Test the configuration:
   ```bash
   ignis init --config ignis/config.py
   ```

4. For performance profiling:
   ```bash
   ignis init --config ignis/config_profiled_v2.py
   cat /tmp/ignis_profile.log
   ```

## Development Best Practices

### 1. Python Code Style

#### Follow PEP 8 with GTK-specific conventions:
```python
# Good: Type hints for better IDE support
from ignis.widgets import Widget
from gi.repository import Gtk

def create_button(label: str, on_click: callable) -> Widget.Button:
    return Widget.Button(label=label, on_clicked=on_click)

# Good: Explicit imports
from ignis.services.audio import AudioService
from ignis.services.network import NetworkService

# Bad: Star imports (except for Ignis widgets module exports)
from ignis.services import *
```

#### Use descriptive naming:
```python
# Good
def get_formatted_battery_percentage() -> str:
    return f"{battery.percentage}%"

# Bad
def get_bat_pct() -> str:
    return f"{bat.pct}%"
```

### 2. GTK4/Ignis Widget Patterns

#### Prefer Ignis widget abstractions over raw GTK:
```python
from ignis.widgets import Widget

# Good: Use Ignis widgets
container = Widget.Box(
    vertical=True,
    spacing=12,
    child=[
        Widget.Label(label="Title", css_classes=["title"]),
        Widget.Button(label="Action", on_clicked=do_action)
    ]
)

# Avoid: Raw GTK widgets (unless necessary)
box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
label = Gtk.Label()
```

#### Use CSS classes for styling:
```python
# Good: Semantic CSS classes
Widget.Button(
    label="Primary Action",
    css_classes=["primary-button", "large"]
)

# Bad: Inline styles (not supported well in GTK4)
Widget.Button(label="Action", style="color: red")
```

### 3. Service Usage Patterns

#### Use lazy initialization for services:
```python
# Good: Lazy loading pattern (already implemented in most modules)
from ignis.services.audio import AudioService

_audio = None

def get_audio():
    """Lazy load AudioService"""
    global _audio
    if _audio is None:
        _audio = AudioService.get_default()
    return _audio

class VolumeWidget:
    def __init__(self):
        # Service only initialized when widget is created
        self.audio = get_audio()
```

#### Bind to service properties reactively:
```python
# Good: Use property binding
audio = AudioService.get_default()

volume_label = Widget.Label()
audio.speaker.bind_property(
    "volume",
    volume_label,
    "label",
    transform_to=lambda _, vol: f"{int(vol * 100)}%"
)

# Bad: Manual updates
def update_volume():
    volume_label.label = f"{int(audio.speaker.volume * 100)}%"
```

### 4. Performance Considerations

#### Critical performance rules (see OPTIMIZATION_SUMMARY.md):
1. **Lazy load services** - Don't initialize services at module import time
2. **Cache expensive operations** - Color generation, image processing
3. **Defer heavy imports** - Import PIL, materialyoucolor only when needed
4. **Use cache-first patterns** - Load from cache before regenerating

```python
# Good: Cache-first loading
def get_colors(self, wallpaper_path: str, dark_mode: bool) -> dict:
    # Try cache first
    cached = self._load_from_cache(wallpaper_path, dark_mode)
    if cached:
        return cached

    # Only import heavy libraries if cache miss
    from PIL import Image
    from materialyoucolor.quantize import QuantizeCelebi

    # Generate and cache
    colors = self._generate_colors(wallpaper_path, dark_mode)
    self._save_to_cache(wallpaper_path, dark_mode, colors)
    return colors
```

#### Startup time breakdown (target: <5s):
- Import modules: ~2.3s (46%)
- Service initialization: ~1.5s (30%)
- Widget creation: ~0.8s (16%)
- CSS compilation: ~0.4s (8%)

### 5. SCSS Styling Guidelines

#### Use Material Design 3 variables:
```scss
// Good: Use Material Design tokens
.control-panel {
    background-color: $surface_container;
    color: $on_surface;
    border-radius: 12px;
    padding: 12px;

    .header {
        background-color: $surface_container_high;
        color: $on_surface_variant;
    }
}

// Bad: Hardcoded colors
.control-panel {
    background-color: #1a1a1a;
    color: #ffffff;
}
```

#### Follow GTK4/Adwaita design patterns:
```scss
// Border radius scale
$radius-small: 6px;    // Buttons, list items
$radius-medium: 12px;  // Cards, windows
$radius-large: 18px;   // Dialogs

// Spacing scale
$spacing-xs: 6px;
$spacing-sm: 12px;
$spacing-md: 18px;
$spacing-lg: 24px;
$spacing-xl: 32px;

// Elevation (use shadows, not borders)
$shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.12);
$shadow-md: 0 2px 6px rgba(0, 0, 0, 0.16);
$shadow-lg: 0 4px 12px rgba(0, 0, 0, 0.20);
```

### 6. Material Design Color System

#### Understanding the color palette:
```python
# Primary colors - main brand/accent
primary, on_primary, primary_container, on_primary_container

# Surface colors - backgrounds (ordered by elevation)
background → surface → surface_container_low → surface_container → surface_container_high

# Semantic colors
error, on_error, warning, success

# Neutral colors
outline, outline_variant, surface_variant
```

#### Color generation workflow:
1. User selects wallpaper
2. MaterialService generates palette using matugen/materialyoucolor
3. Colors cached to JSON for fast startup
4. SCSS variables injected into style.scss
5. CSS recompiled and applied to all windows

### 7. Creating New Modules

#### Module structure template:
```python
# modules/my_module/__init__.py
from .window import MyModule

__all__ = ["MyModule"]

# modules/my_module/window.py
from ignis.widgets import Widget
from ignis.services.something import SomethingService

class MyModule(Widget.Window):
    def __init__(self):
        # Lazy load services
        self.service = SomethingService.get_default()

        super().__init__(
            namespace="my-module",
            layer="top",
            anchor=["top", "right"],
            exclusivity="normal",
            kb_mode="on_demand",
            visible=False,
            child=self._build_ui()
        )

    def _build_ui(self) -> Widget.Box:
        return Widget.Box(
            vertical=True,
            css_classes=["my-module"],
            child=[
                self._build_header(),
                self._build_content(),
            ]
        )

    def _build_header(self) -> Widget.Box:
        return Widget.Box(
            css_classes=["header"],
            child=[
                Widget.Label(label="My Module", css_classes=["title"]),
            ]
        )

    def _build_content(self) -> Widget.Box:
        # Module content here
        pass
```

#### Register module in config.py:
```python
from modules import MyModule

# After other module initializations
MyModule()
```

### 8. Creating New Services

#### Service structure template:
```python
# services/my_service/service.py
from gi.repository import GObject
from ignis.base_service import BaseService

class MyService(BaseService):
    __gsignals__ = {
        "changed": (GObject.SignalFlags.RUN_FIRST, GObject.TYPE_NONE, ()),
    }

    def __init__(self):
        super().__init__()
        self._data = None

    @GObject.Property
    def data(self) -> str:
        return self._data

    @data.setter
    def data(self, value: str) -> None:
        self._data = value
        self.emit("changed")
        self.notify("data")

    def do_something(self) -> None:
        """Service method"""
        self.data = "new value"

# services/my_service/__init__.py
from .service import MyService
__all__ = ["MyService"]
```

### 9. Testing and Debugging

#### Live testing workflow:
```bash
# 1. Start Ignis with your config
ignis init --config ignis/config.py

# 2. Make changes to Python/SCSS files

# 3. Reload Ignis (Ctrl+Shift+R or restart)
pkill ignis && ignis init --config ignis/config.py

# 4. For CSS-only changes, trigger reload:
# CSS manager watches files and auto-reloads
```

#### Debug logging:
```python
from ignis import utils

# Use Ignis logging utilities
utils.notify("Debug Message", "Detailed info here")

# Or standard Python logging
import logging
logging.info("Service initialized")
logging.error("Failed to load wallpaper", exc_info=True)
```

#### Common debugging commands:
```bash
# Check if Ignis is running
pgrep -a ignis

# View Ignis logs
journalctl --user -u ignis -f

# Test SCSS compilation
echo '$primary: #ff0000; .test { color: $primary; }' | sassc -t expanded -
```

### 10. Git Workflow

#### Branch naming:
- Feature branches: `feature/short-description`
- Bug fixes: `fix/short-description`
- Refactoring: `refactor/short-description`
- Documentation: `docs/short-description`

#### Commit messages:
```bash
# Good commit messages
git commit -m "feat: add wallpaper slideshow service"
git commit -m "fix: Settings window Material Design color variables"
git commit -m "perf: lazy load services to reduce startup time by 70ms"
git commit -m "refactor: extract color generation to separate service"
git commit -m "docs: add development guide for contributors"

# Commit message format
<type>: <short description>

[optional body with more details]

[optional footer with breaking changes or issue references]

# Types: feat, fix, perf, refactor, style, docs, test, chore
```

#### Before committing:
1. Test all affected modules work correctly
2. Verify no syntax errors: `python -m py_compile ignis/**/*.py`
3. Check SCSS compiles: `sassc ignis/style.scss /tmp/test.css`
4. Run profiled config to check performance impact
5. Update documentation if adding/changing features

## Common Tasks

### Adding a New Quick Settings Toggle
```python
# 1. Create widget in modules/control_center/widgets/quick_settings/
from ignis.widgets import Widget
from services.my_service import MyService

def my_toggle() -> Widget.Button:
    service = MyService.get_default()

    return Widget.Button(
        css_classes=["qs-button"],
        on_clicked=lambda x: service.toggle(),
        child=Widget.Box(
            vertical=True,
            child=[
                Widget.Icon(image="my-icon", pixel_size=24),
                Widget.Label(label="My Setting")
            ]
        )
    )

# 2. Import and add to control_center/widgets/quick_settings/grid.py
from .my_toggle import my_toggle

# Add to grid
```

### Changing Theme Colors
```python
# 1. Modify user_options.py if adding new options
class Material(OptionsGroup):
    accent_color: str = "#ff0000"  # New option

# 2. Update services/material/service.py color generation

# 3. Add SCSS variable in config.py patch_style_scss():
scss_colors += format_scss_var("accent", user_options.material.accent_color)

# 4. Use in SCSS files:
.my-widget {
    color: $accent;
}
```

### Adding Wallpaper Transition Effects
```bash
# swww supports multiple transition types
swww img /path/to/wallpaper.jpg \
    --transition-type fade \
    --transition-duration 2 \
    --transition-fps 60

# Available transitions: fade, slide, grow, outer, wipe, wave
```

## Architecture Decisions

### Why Lazy Loading?
Reduces startup time by deferring service initialization until actually needed. Services like BluetoothService or RecorderService may never be used in a session.

### Why Cache-First for Colors?
Material You color generation is expensive (200ms+). Caching ensures instant startup with last-used colors, regenerating only on wallpaper change.

### Why SCSS over CSS?
SCSS allows:
- Variable injection for dynamic theming
- Nested selectors for better organization
- Mixins for reusable style patterns
- Math operations for computed values

### Why GTK4 over GTK3?
- Better Wayland support
- Improved performance
- Modern widget APIs
- Future-proof (GTK3 maintenance mode)

## Troubleshooting

### Ignis won't start
```bash
# Check for Python errors
ignis init --config ignis/config.py 2>&1 | less

# Verify GTK4 installation
python -c "from gi.repository import Gtk; print(Gtk.MAJOR_VERSION)"
```

### SCSS compilation errors
```bash
# Test SCSS manually
sassc ignis/style.scss /tmp/test.css

# Check for undefined variables
grep -r '\$[a-zA-Z_]' ignis/scss/
```

### Services not responding
```bash
# Check if services are running (e.g., swww)
pgrep -a swww

# Restart swww daemon
pkill swww && swww-daemon &
```

### Performance regression
```bash
# Profile startup
ignis init --config ignis/config_profiled_v2.py
cat /tmp/ignis_profile.log

# Compare with baseline (5.018s target)
```

## Resources

### Documentation
- [Ignis Framework Docs](https://github.com/linkfrg/ignis) - Framework documentation
- [GTK4 Python Tutorial](https://docs.gtk.org/gtk4/) - GTK4 reference
- [Material Design 3](https://m3.material.io/) - Design guidelines
- [GNOME HIG](https://developer.gnome.org/hig/) - GNOME design patterns

### Related Projects
- [Hyprland](https://hyprland.org/) - Wayland compositor
- [swww](https://github.com/LGFae/swww) - Wallpaper daemon
- [matugen](https://github.com/InioX/matugen) - Material You color generator

## Project Status & Roadmap

### Completed
- ✅ Core desktop shell modules (bar, launcher, control center, etc.)
- ✅ Material You color theming with wallpaper integration
- ✅ Wallpaper slideshow service with transitions
- ✅ Performance optimization (5s startup, 46% in imports)
- ✅ Multi-monitor support
- ✅ Settings UI with persistent options

### In Progress
- ⏳ Migration from materialyoucolor to matugen (see MATUGEN_MIGRATION_PLAN.md)
- ⏳ GTK4/Adwaita design alignment (GNOME 48 styling)
- ⏳ Settings window HeaderBar implementation

### Planned
- 🔲 Additional quick settings toggles
- 🔲 Widget customization UI
- 🔲 Plugin system for custom modules
- 🔲 Theme presets and sharing
- 🔲 Automated testing suite

## Contributing

When contributing to this project:

1. **Understand the architecture** - Read this guide fully
2. **Check existing issues** - Avoid duplicate work
3. **Follow code style** - Maintain consistency
4. **Test thoroughly** - Verify all modules still work
5. **Document changes** - Update relevant .md files
6. **Keep performance in mind** - Profile if adding heavy operations
7. **Use semantic commits** - Follow commit message conventions

## License

See LICENSE file for details.

---

**Last Updated**: 2025-11-13
**Maintainer**: See git history for contributors
**Version**: Development (pre-1.0)
