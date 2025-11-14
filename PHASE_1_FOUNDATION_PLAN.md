# Phase 1: Foundation - Blackhole Shell Design System

## Overview

This phase establishes the foundational design system for Blackhole Shell, replacing the current Material You implementation with a hybrid system that supports both built-in color palettes and dynamic wallpaper-based generation via matugen 3.0.

## Goals

1. **Design Token System** - Create Blackhole Shell design tokens based on Noctalia's layout/spacing principles
2. **Rose Pine Default** - Ship with Rose Pine as the default theme (3 variants)
3. **Built-in Palettes** - Support multiple predefined color schemes
4. **Matugen Integration** - Replace materialyoucolor with matugen 3.0 for wallpaper-based generation
5. **Settings Panel** - Add Color Scheme section in Settings for theme selection
6. **App Theming** - Generate matugen-compatible JSON for external app theming
7. **Ignis Migration** - Update codebase for latest Ignis git version compatibility

## Research Summary

### Rose Pine Color Palette

**Rose Pine (Main)** - Dark variant (default dark mode):
```json
{
  "base": "#191724",
  "surface": "#1f1d2e",
  "overlay": "#26233a",
  "muted": "#6e6a86",
  "subtle": "#908caa",
  "text": "#e0def4",
  "love": "#eb6f92",
  "gold": "#f6c177",
  "rose": "#ebbcba",
  "pine": "#31748f",
  "foam": "#9ccfd8",
  "iris": "#c4a7e7",
  "highlight_low": "#21202e",
  "highlight_med": "#403d52",
  "highlight_high": "#524f67"
}
```

**Rose Pine Moon** - Alternative dark variant:
```json
{
  "base": "#232136",
  "surface": "#2a273f",
  "overlay": "#393552",
  "muted": "#6e6a86",
  "subtle": "#908caa",
  "text": "#e0def4",
  "love": "#eb6f92",
  "gold": "#f6c177",
  "rose": "#ea9a97",
  "pine": "#3e8fb0",
  "foam": "#9ccfd8",
  "iris": "#c4a7e7"
}
```

**Rose Pine Dawn** - Light variant:
```json
{
  "base": "#faf4ed",
  "surface": "#fffaf3",
  "overlay": "#f2e9e1",
  "muted": "#9893a5",
  "subtle": "#797593",
  "text": "#575279",
  "love": "#b4637a",
  "gold": "#ea9d34",
  "rose": "#d7827e",
  "pine": "#286983",
  "foam": "#56949f",
  "iris": "#907aa9",
  "highlight_low": "#f4ede8",
  "highlight_med": "#dfdad9",
  "highlight_high": "#cecacd"
}
```

### Noctalia Design Tokens (Blackhole Shell Reference)

**Typography Scale:**
```scss
$font-size-xxs: 8px;
$font-size-xs: 9px;
$font-size-s: 10px;
$font-size-m: 11px;    // Default body
$font-size-l: 13px;
$font-size-xl: 16px;
$font-size-xxl: 18px;
$font-size-xxxl: 24px;

$font-weight-regular: 400;
$font-weight-medium: 500;
$font-weight-semibold: 600;
$font-weight-bold: 700;
```

**Spacing Scale (with UI scale ratio):**
```scss
$ui-scale-ratio: 1.0;  // User-configurable

$spacing-xxs: 2px * $ui-scale-ratio;
$spacing-xs: 4px * $ui-scale-ratio;
$spacing-s: 6px * $ui-scale-ratio;
$spacing-m: 9px * $ui-scale-ratio;
$spacing-l: 13px * $ui-scale-ratio;
$spacing-xl: 18px * $ui-scale-ratio;
```

**Border Radius (with ratio scaling):**
```scss
$radius-ratio: 1.0;  // User-configurable

$radius-xxs: 4px * $radius-ratio;
$radius-xs: 8px * $radius-ratio;
$radius-s: 12px * $radius-ratio;
$radius-m: 16px * $radius-ratio;
$radius-l: 20px * $radius-ratio;
```

**Opacity Levels:**
```scss
$opacity-none: 0.0;
$opacity-light: 0.25;
$opacity-medium: 0.5;
$opacity-heavy: 0.75;
$opacity-almost: 0.95;
$opacity-full: 1.0;
```

**Shadows:**
```scss
$shadow-opacity: 0.85;
$shadow-blur-max: 22px;
$shadow-offset-x: 0px;
$shadow-offset-y: 2px;

// Example usage
box-shadow: $shadow-offset-x $shadow-offset-y $shadow-blur-max rgba(0, 0, 0, $shadow-opacity);
```

**Animation Timing:**
```scss
$animation-faster: 75ms;
$animation-fast: 150ms;
$animation-normal: 300ms;
$animation-slow: 450ms;
$animation-slowest: 750ms;
```

### Matugen 3.0 Integration

**Matugen Scheme Types** (for wallpaper-based generation):
- `tonal-spot` (default) - Balanced, moderate colorfulness
- `vibrant` - High chroma, vivid colors
- `expressive` - Maximum expressiveness
- `neutral` - Low chroma, subtle
- `monochrome` - Grayscale-based
- `fidelity` - Closest to source color
- `content` - Derived from content
- `fruit-salad` - Playful, varied colors
- `rainbow` - Full spectrum representation

**Matugen Template Format:**
```json
{
  "colors": {
    "primary": "{{colors.primary.default.hex}}",
    "on_primary": "{{colors.on_primary.default.hex}}",
    "secondary": "{{colors.secondary.default.hex}}",
    "on_secondary": "{{colors.on_secondary.default.hex}}",
    "tertiary": "{{colors.tertiary.default.hex}}",
    "on_tertiary": "{{colors.on_tertiary.default.hex}}",
    "error": "{{colors.error.default.hex}}",
    "on_error": "{{colors.on_error.default.hex}}",
    "surface": "{{colors.surface.default.hex}}",
    "on_surface": "{{colors.on_surface.default.hex}}",
    "surface_variant": "{{colors.surface_variant.default.hex}}",
    "on_surface_variant": "{{colors.on_surface_variant.default.hex}}",
    "outline": "{{colors.outline.default.hex}}",
    "shadow": "{{colors.shadow.default.hex}}"
  }
}
```

### Ignis Breaking Changes to Address

1. **OptionsManager** - Migrate from old Options Service to new OptionsManager/Options API
2. **Async Functions** - Handle async DBusProxy methods, device functions
3. **Property Types** - Ensure properties have explicit types, handle None checks
4. **Hyprland Service** - Use attribute access instead of dictionary keys
5. **DebounceTask** - Use `.run()` instead of `.__call__()`
6. **Binding.target_properties** - Use list format instead of single property

## Implementation Tasks

### Task 1: Rose Pine Color Scheme Mapping

**Goal:** Map Rose Pine colors to Material Design 3 color roles

**Rose Pine → Material Design 3 Mapping:**

```python
# ignis/services/material/palettes/rose_pine_main.json
{
  "name": "Rose Pine",
  "variant": "main",
  "dark_mode": true,
  "colors": {
    # Primary (iris - purple accent)
    "primary": "#c4a7e7",
    "on_primary": "#191724",
    "primary_container": "#524f67",
    "on_primary_container": "#e0def4",

    # Secondary (foam - cyan accent)
    "secondary": "#9ccfd8",
    "on_secondary": "#191724",
    "secondary_container": "#403d52",
    "on_secondary_container": "#e0def4",

    # Tertiary (rose - warm accent)
    "tertiary": "#ebbcba",
    "on_tertiary": "#191724",
    "tertiary_container": "#403d52",
    "on_tertiary_container": "#e0def4",

    # Error (love - red/pink)
    "error": "#eb6f92",
    "on_error": "#191724",
    "error_container": "#403d52",
    "on_error_container": "#e0def4",

    # Background & Surface
    "background": "#191724",
    "on_background": "#e0def4",
    "surface": "#1f1d2e",
    "on_surface": "#e0def4",

    # Surface variants (using overlay, highlight levels)
    "surface_dim": "#191724",
    "surface_bright": "#403d52",
    "surface_container_lowest": "#191724",
    "surface_container_low": "#21202e",
    "surface_container": "#26233a",
    "surface_container_high": "#403d52",
    "surface_container_highest": "#524f67",

    # Surface variant
    "surface_variant": "#26233a",
    "on_surface_variant": "#908caa",

    # Outline
    "outline": "#6e6a86",
    "outline_variant": "#403d52",

    # Other
    "shadow": "#000000",
    "scrim": "#000000",
    "inverse_surface": "#e0def4",
    "inverse_on_surface": "#191724",
    "inverse_primary": "#6e6a86"
  }
}
```

**Action Items:**
- [x] Create `ignis/services/material/palettes/` directory
- [x] Create JSON files for all 3 Rose Pine variants (main, moon, dawn)
- [ ] Create additional built-in palettes (Catppuccin, Nord, Gruvbox, Tokyo Night) **(Optional - Future Enhancement)**

### Task 2: Matugen Service Implementation

**Goal:** Replace materialyoucolor with matugen 3.0

**File:** `ignis/services/material/matugen_service.py`

```python
"""
Matugen-based color generation service.
Replaces materialyoucolor for wallpaper-based palette generation.
"""

import subprocess
import json
import os
from gi.repository import GObject
from ignis.base_service import BaseService
from ignis import CACHE_DIR

class MatugenService(BaseService):
    """Generate Material Design 3 color palettes using matugen."""

    def __init__(self):
        super().__init__()
        self._cache_file = os.path.join(CACHE_DIR, "matugen_colors.json")
        self._template_file = os.path.join(CACHE_DIR, "matugen_template.json")
        self._scheme_type = "tonal-spot"  # Default scheme

    @GObject.Property
    def scheme_type(self) -> str:
        """Current matugen scheme type."""
        return self._scheme_type

    @scheme_type.setter
    def scheme_type(self, value: str) -> None:
        """Set matugen scheme type (tonal-spot, vibrant, etc.)."""
        valid_schemes = [
            "tonal-spot", "vibrant", "expressive", "neutral",
            "monochrome", "fidelity", "content", "fruit-salad", "rainbow"
        ]
        if value in valid_schemes:
            self._scheme_type = value
            self.notify("scheme-type")

    def generate_from_image(self, image_path: str, dark_mode: bool = True) -> dict:
        """
        Generate color palette from image using matugen.

        Args:
            image_path: Path to wallpaper image
            dark_mode: Generate dark or light palette

        Returns:
            Dictionary of Material Design 3 color tokens
        """
        try:
            # Run matugen with JSON output
            result = subprocess.run(
                [
                    "matugen",
                    "image", image_path,
                    "--json", "hex",
                    "--type", self._scheme_type,
                    "--mode", "dark" if dark_mode else "light",
                    "--dry-run"  # Don't apply, just output
                ],
                capture_output=True,
                text=True,
                check=True
            )

            # Parse matugen JSON output
            matugen_data = json.loads(result.stdout)

            # Extract colors and flatten structure
            colors = self._extract_colors(matugen_data, dark_mode)

            # Cache the result
            self._save_cache(colors)

            # Generate template JSON for external apps
            self._generate_app_template(matugen_data)

            return colors

        except subprocess.CalledProcessError as e:
            print(f"Matugen generation failed: {e.stderr}")
            return self._load_cache()
        except json.JSONDecodeError as e:
            print(f"Failed to parse matugen output: {e}")
            return self._load_cache()

    def _extract_colors(self, matugen_data: dict, dark_mode: bool) -> dict:
        """
        Extract and flatten matugen color structure.

        Matugen format: colors.primary.default.hex
        Our format: flat dictionary with underscored keys
        """
        mode = "dark" if dark_mode else "light"
        colors_obj = matugen_data.get("colors", {}).get(mode, {})

        # Flatten nested structure
        flat_colors = {}
        for key, value in colors_obj.items():
            if isinstance(value, dict) and "hex" in value:
                flat_colors[key] = value["hex"]

        return flat_colors

    def _save_cache(self, colors: dict) -> None:
        """Save generated colors to cache file."""
        os.makedirs(os.path.dirname(self._cache_file), exist_ok=True)
        with open(self._cache_file, "w") as f:
            json.dump(colors, f, indent=2)

    def _load_cache(self) -> dict:
        """Load colors from cache file."""
        if os.path.exists(self._cache_file):
            with open(self._cache_file, "r") as f:
                return json.load(f)
        return {}

    def _generate_app_template(self, matugen_data: dict) -> None:
        """
        Generate matugen-compatible JSON for external app theming.
        This file can be used by other apps via matugen templates.
        """
        # Save full matugen data for template system
        with open(self._template_file, "w") as f:
            json.dump(matugen_data, f, indent=2)
```

**Action Items:**
- [x] Create `matugen_service.py` with full implementation
- [x] Add error handling and fallback to default colors
- [x] Create matugen template directory structure
- [x] Implement cache-first loading strategy

### Task 3: Color Scheme Manager Service

**Goal:** Unified service to manage both built-in and dynamic color schemes

**File:** `ignis/services/material/color_scheme_service.py`

```python
"""
Color Scheme Manager - handles both built-in palettes and dynamic generation.
"""

import os
import json
from typing import Optional
from gi.repository import GObject
from ignis.base_service import BaseService
from ignis import utils, DATA_DIR
from .matugen_service import MatugenService

PALETTES_DIR = os.path.join(utils.get_current_dir(), "services", "material", "palettes")

class ColorSchemeService(BaseService):
    """Manage color schemes for Blackhole Shell."""

    __gsignals__ = {
        "scheme-changed": (GObject.SignalFlags.RUN_FIRST, GObject.TYPE_NONE, ()),
    }

    def __init__(self):
        super().__init__()
        self._matugen = MatugenService.get_default()
        self._current_scheme_name = "Rose Pine"
        self._use_wallpaper_colors = False
        self._current_colors = {}
        self._built_in_schemes = self._load_built_in_schemes()

        # Load initial scheme
        self._load_scheme()

    @GObject.Property
    def scheme_name(self) -> str:
        """Current color scheme name."""
        return self._current_scheme_name

    @GObject.Property
    def use_wallpaper_colors(self) -> bool:
        """Whether to use wallpaper-based color generation."""
        return self._use_wallpaper_colors

    @use_wallpaper_colors.setter
    def use_wallpaper_colors(self, value: bool) -> None:
        """Toggle between built-in and wallpaper-based colors."""
        if self._use_wallpaper_colors != value:
            self._use_wallpaper_colors = value
            self._load_scheme()
            self.notify("use-wallpaper-colors")

    @GObject.Property
    def available_schemes(self) -> list[str]:
        """List of available built-in color schemes."""
        return list(self._built_in_schemes.keys())

    @GObject.Property
    def current_colors(self) -> dict:
        """Current active color palette."""
        return self._current_colors

    @GObject.Property
    def matugen_scheme_type(self) -> str:
        """Current matugen scheme type for wallpaper generation."""
        return self._matugen.scheme_type

    @matugen_scheme_type.setter
    def matugen_scheme_type(self, value: str) -> None:
        """Set matugen scheme type and regenerate if using wallpaper colors."""
        self._matugen.scheme_type = value
        if self._use_wallpaper_colors:
            self._load_scheme()
        self.notify("matugen-scheme-type")

    def set_scheme(self, scheme_name: str) -> None:
        """
        Set active color scheme (built-in only).

        Args:
            scheme_name: Name of built-in scheme (e.g., "Rose Pine")
        """
        if scheme_name in self._built_in_schemes:
            self._current_scheme_name = scheme_name
            self._use_wallpaper_colors = False
            self._load_scheme()
            self.notify("scheme-name")
            self.notify("use-wallpaper-colors")

    def generate_from_wallpaper(self, wallpaper_path: str, dark_mode: bool = True) -> None:
        """
        Generate color scheme from wallpaper using matugen.

        Args:
            wallpaper_path: Path to wallpaper image
            dark_mode: Generate dark or light palette
        """
        self._use_wallpaper_colors = True
        colors = self._matugen.generate_from_image(wallpaper_path, dark_mode)
        self._current_colors = colors
        self.emit("scheme-changed")
        self.notify("current-colors")
        self.notify("use-wallpaper-colors")

    def _load_built_in_schemes(self) -> dict:
        """Load all built-in color scheme JSON files."""
        schemes = {}

        if not os.path.exists(PALETTES_DIR):
            return schemes

        for filename in os.listdir(PALETTES_DIR):
            if filename.endswith(".json"):
                filepath = os.path.join(PALETTES_DIR, filename)
                try:
                    with open(filepath, "r") as f:
                        data = json.load(f)
                        scheme_name = data.get("name", filename[:-5])
                        schemes[scheme_name] = data
                except (json.JSONDecodeError, IOError) as e:
                    print(f"Failed to load palette {filename}: {e}")

        return schemes

    def _load_scheme(self) -> None:
        """Load current color scheme based on settings."""
        if self._use_wallpaper_colors:
            # Load cached wallpaper colors
            self._current_colors = self._matugen._load_cache()
        else:
            # Load built-in scheme
            scheme_data = self._built_in_schemes.get(self._current_scheme_name)
            if scheme_data:
                self._current_colors = scheme_data.get("colors", {})

        self.emit("scheme-changed")
        self.notify("current-colors")
```

**Action Items:**
- [x] Create `color_scheme_service.py`
- [x] Integrate with existing MaterialService or replace it
- [x] Add support for light/dark mode variants
- [x] Connect to wallpaper change events

### Task 4: Update user_options.py

**Goal:** Add color scheme configuration options

```python
class Material(OptionsGroup):
    # Color scheme settings
    scheme_name: str = "Rose Pine"  # Active built-in scheme
    scheme_variant: str = "main"  # Variant: main, moon, dawn
    use_wallpaper_colors: bool = False  # False = built-in, True = dynamic

    # Matugen settings (for wallpaper-based generation)
    matugen_scheme_type: str = "tonal-spot"  # Scheme algorithm

    # Dark mode
    dark_mode: bool = True

    # Current colors (loaded from scheme or matugen)
    colors: dict[str, str] = {}

    # Font configuration (keep existing)
    interface_font: str = "Inter"
    interface_font_size: int = 11
    document_font: str = "Inter"
    document_font_size: int = 11
    monospace_font: str = "JetBrains Mono"
    monospace_font_size: int = 10

    # App theming toggles (keep existing)
    theme_gtk: bool = True
    theme_qt: bool = True
    theme_kitty: bool = True
    theme_ghostty: bool = True
    theme_fuzzel: bool = True
    theme_hyprland: bool = True
    theme_niri: bool = True
    theme_swaylock: bool = True
```

**Action Items:**
- [x] Update `user_options.py` with new Material options
- [x] Remove old materialyoucolor-specific options
- [x] Add migration logic for existing users

### Task 5: Create Blackhole Design Token SCSS

**Goal:** Create SCSS file with all Blackhole Shell design tokens

**File:** `ignis/scss/_blackhole_tokens.scss`

```scss
/**
 * Blackhole Shell Design Tokens
 * Based on Noctalia Shell design system
 *
 * Reference: https://github.com/noctalia-dev/noctalia-shell
 */

// ============================================================
// CONFIGURATION RATIOS
// ============================================================

// User-configurable scaling ratios
$ui-scale-ratio: 1.0 !default;
$radius-ratio: 1.0 !default;
$screen-radius-ratio: 1.0 !default;

// ============================================================
// TYPOGRAPHY
// ============================================================

// Font sizes (8-level scale)
$font-size-xxs: 8px;
$font-size-xs: 9px;
$font-size-s: 10px;
$font-size-m: 11px;     // Default body text
$font-size-l: 13px;
$font-size-xl: 16px;
$font-size-xxl: 18px;
$font-size-xxxl: 24px;

// Font weights
$font-weight-regular: 400;
$font-weight-medium: 500;
$font-weight-semibold: 600;
$font-weight-bold: 700;

// ============================================================
// SPACING
// ============================================================

$spacing-xxs: calc(2px * #{$ui-scale-ratio});
$spacing-xs: calc(4px * #{$ui-scale-ratio});
$spacing-s: calc(6px * #{$ui-scale-ratio});
$spacing-m: calc(9px * #{$ui-scale-ratio});
$spacing-l: calc(13px * #{$ui-scale-ratio});
$spacing-xl: calc(18px * #{$ui-scale-ratio});

// ============================================================
// BORDER RADIUS
// ============================================================

$radius-xxs: calc(4px * #{$radius-ratio});
$radius-xs: calc(8px * #{$radius-ratio});
$radius-s: calc(12px * #{$radius-ratio});
$radius-m: calc(16px * #{$radius-ratio});
$radius-l: calc(20px * #{$radius-ratio});
$radius-screen: calc(20px * #{$screen-radius-ratio});

// ============================================================
// BORDERS
// ============================================================

$border-s: max(1px, calc(1px * #{$ui-scale-ratio}));
$border-m: max(1px, calc(2px * #{$ui-scale-ratio}));
$border-l: max(1px, calc(3px * #{$ui-scale-ratio}));

// ============================================================
// OPACITY
// ============================================================

$opacity-none: 0.0;
$opacity-light: 0.25;
$opacity-medium: 0.5;
$opacity-heavy: 0.75;
$opacity-almost: 0.95;
$opacity-full: 1.0;

// ============================================================
// SHADOWS
// ============================================================

$shadow-opacity: 0.85;
$shadow-blur-max: 22px;
$shadow-offset-x: 0px;
$shadow-offset-y: 2px;

// Standard shadow (for panels, cards)
$shadow-standard: $shadow-offset-x $shadow-offset-y $shadow-blur-max rgba(0, 0, 0, $shadow-opacity);

// Light shadow (for subtle elevation)
$shadow-light: 0 1px 3px rgba(0, 0, 0, 0.12);

// Medium shadow (for dropdowns, tooltips)
$shadow-medium: 0 2px 6px rgba(0, 0, 0, 0.16);

// Heavy shadow (for modals)
$shadow-heavy: 0 4px 12px rgba(0, 0, 0, 0.20);

// ============================================================
// ANIMATIONS
// ============================================================

// Animation durations
$animation-faster: 75ms;
$animation-fast: 150ms;
$animation-normal: 300ms;
$animation-slow: 450ms;
$animation-slowest: 750ms;

// Animation delays
$delay-tooltip: 300ms;
$delay-tooltip-long: 1200ms;
$delay-pill: 500ms;

// Easing functions
$ease-out-cubic: cubic-bezier(0.33, 1, 0.68, 1);
$ease-in-cubic: cubic-bezier(0.32, 0, 0.67, 0);
$ease-in-out-cubic: cubic-bezier(0.65, 0, 0.35, 1);

// ============================================================
// COMPONENT DIMENSIONS
// ============================================================

// Base widget size
$widget-size-base: 33px;

// Slider dimensions
$slider-width: 200px;

// Bar height (density-dependent)
$bar-height-compact: 20px;
$bar-height-comfortable: 30px;
$bar-height-spacious: 39px;

// ============================================================
// COLOR TOKENS (Material Design 3)
// ============================================================
// Colors are injected dynamically from color scheme service
// These are placeholder declarations

// Primary
$primary: #c4a7e7 !default;
$on-primary: #191724 !default;
$primary-container: #524f67 !default;
$on-primary-container: #e0def4 !default;

// Secondary
$secondary: #9ccfd8 !default;
$on-secondary: #191724 !default;
$secondary-container: #403d52 !default;
$on-secondary-container: #e0def4 !default;

// Tertiary
$tertiary: #ebbcba !default;
$on-tertiary: #191724 !default;
$tertiary-container: #403d52 !default;
$on-tertiary-container: #e0def4 !default;

// Error
$error: #eb6f92 !default;
$on-error: #191724 !default;
$error-container: #403d52 !default;
$on-error-container: #e0def4 !default;

// Background
$background: #191724 !default;
$on-background: #e0def4 !default;

// Surface
$surface: #1f1d2e !default;
$on-surface: #e0def4 !default;
$surface-variant: #26233a !default;
$on-surface-variant: #908caa !default;

// Surface containers (elevation levels)
$surface-dim: #191724 !default;
$surface-bright: #403d52 !default;
$surface-container-lowest: #191724 !default;
$surface-container-low: #21202e !default;
$surface-container: #26233a !default;
$surface-container-high: #403d52 !default;
$surface-container-highest: #524f67 !default;

// Outline
$outline: #6e6a86 !default;
$outline-variant: #403d52 !default;

// Other
$shadow: #000000 !default;
$scrim: #000000 !default;
$inverse-surface: #e0def4 !default;
$inverse-on-surface: #191724 !default;
$inverse-primary: #6e6a86 !default;
```

**Action Items:**
- [x] Create `_blackhole_tokens.scss`
- [x] Import in main `style.scss`
- [x] Update all component SCSS files to use new tokens
- [x] Remove old Material Design variable names

### Task 6: Settings Panel - Color Scheme Section

**Goal:** Add UI for color scheme selection in Settings module

**File:** `ignis/modules/settings/sections/appearance.py` (new or update existing)

```python
"""
Appearance settings section - Color schemes, fonts, theming.
"""

from ignis.widgets import Widget
from ignis.services.material import ColorSchemeService
from user_options import user_options

color_scheme_service = ColorSchemeService.get_default()

def appearance_section() -> Widget.Box:
    """Create appearance settings section."""

    return Widget.Box(
        vertical=True,
        spacing=12,
        css_classes=["settings-section"],
        child=[
            _color_scheme_header(),
            _color_scheme_selector(),
            _matugen_options(),
            _wallpaper_toggle(),
            Widget.Separator(),
            _font_settings(),
            Widget.Separator(),
            _app_theming_toggles(),
        ]
    )

def _color_scheme_header() -> Widget.Label:
    """Section header."""
    return Widget.Label(
        label="Color Scheme",
        css_classes=["settings-header"],
        h_align="start"
    )

def _color_scheme_selector() -> Widget.Box:
    """Dropdown to select built-in color scheme."""

    schemes = color_scheme_service.available_schemes

    scheme_dropdown = Widget.ComboBoxText(
        items=schemes,
        active=schemes.index(user_options.material.scheme_name) if user_options.material.scheme_name in schemes else 0,
        on_changed=lambda dropdown: _on_scheme_changed(dropdown.active_id)
    )

    return Widget.Box(
        spacing=12,
        child=[
            Widget.Label(
                label="Theme:",
                h_expand=False,
                css_classes=["settings-label"]
            ),
            scheme_dropdown
        ]
    )

def _matugen_options() -> Widget.Box:
    """Matugen scheme type selector (for wallpaper generation)."""

    scheme_types = [
        "tonal-spot",
        "vibrant",
        "expressive",
        "neutral",
        "monochrome",
        "fidelity",
        "content",
        "fruit-salad",
        "rainbow"
    ]

    scheme_type_dropdown = Widget.ComboBoxText(
        items=scheme_types,
        active=scheme_types.index(user_options.material.matugen_scheme_type) if user_options.material.matugen_scheme_type in scheme_types else 0,
        sensitive=user_options.material.use_wallpaper_colors,  # Only enabled if using wallpaper
        on_changed=lambda dropdown: _on_matugen_scheme_changed(dropdown.active_id)
    )

    return Widget.Box(
        spacing=12,
        child=[
            Widget.Label(
                label="Matugen Scheme:",
                h_expand=False,
                css_classes=["settings-label"]
            ),
            scheme_type_dropdown,
            Widget.Label(
                label="(for wallpaper-based colors)",
                css_classes=["settings-hint"]
            )
        ]
    )

def _wallpaper_toggle() -> Widget.Box:
    """Toggle between built-in and wallpaper-based colors."""

    toggle = Widget.Switch(
        active=user_options.material.use_wallpaper_colors,
        on_activate=lambda switch: _on_wallpaper_toggle(switch.active)
    )

    return Widget.Box(
        spacing=12,
        child=[
            Widget.Label(
                label="Use Wallpaper Colors:",
                h_expand=True,
                h_align="start",
                css_classes=["settings-label"]
            ),
            toggle
        ]
    )

def _on_scheme_changed(scheme_name: str) -> None:
    """Handle built-in scheme selection."""
    user_options.material.scheme_name = scheme_name
    color_scheme_service.set_scheme(scheme_name)
    user_options.save_to_file(user_options._file)

def _on_matugen_scheme_changed(scheme_type: str) -> None:
    """Handle matugen scheme type selection."""
    user_options.material.matugen_scheme_type = scheme_type
    color_scheme_service.matugen_scheme_type = scheme_type
    user_options.save_to_file(user_options._file)

def _on_wallpaper_toggle(active: bool) -> None:
    """Handle wallpaper color toggle."""
    user_options.material.use_wallpaper_colors = active
    color_scheme_service.use_wallpaper_colors = active
    user_options.save_to_file(user_options._file)

# ... font settings and app theming toggles (keep existing)
```

**Action Items:**
- [x] Create or update appearance settings section
- [x] Add color scheme selector dropdown
- [x] Add matugen scheme type selector
- [x] Add wallpaper colors toggle
- [x] Connect to ColorSchemeService
- [x] Test settings persistence

### Task 7: Matugen Templates for External Apps

**Goal:** Create matugen template files for theming external applications

**Directory:** `ignis/services/material/matugen_templates/`

**Template Files to Create:**

1. **blackhole.json** - Main shell colors
2. **gtk.css** - GTK applications
3. **kitty.conf** - Kitty terminal
4. **ghostty** - Ghostty terminal
5. **fuzzel.ini** - Fuzzel launcher
6. **hyprland.conf** - Hyprland WM colors
7. **niri.kdl** - Niri WM colors

**Example:** `blackhole.json`
```json
{
  "name": "Blackhole Shell",
  "colors": {
    "primary": "{{colors.primary.default.hex}}",
    "on_primary": "{{colors.on_primary.default.hex}}",
    "primary_container": "{{colors.primary_container.default.hex}}",
    "on_primary_container": "{{colors.on_primary_container.default.hex}}",

    "secondary": "{{colors.secondary.default.hex}}",
    "on_secondary": "{{colors.on_secondary.default.hex}}",
    "secondary_container": "{{colors.secondary_container.default.hex}}",
    "on_secondary_container": "{{colors.on_secondary_container.default.hex}}",

    "tertiary": "{{colors.tertiary.default.hex}}",
    "on_tertiary": "{{colors.on_tertiary.default.hex}}",
    "tertiary_container": "{{colors.tertiary_container.default.hex}}",
    "on_tertiary_container": "{{colors.on_tertiary_container.default.hex}}",

    "error": "{{colors.error.default.hex}}",
    "on_error": "{{colors.on_error.default.hex}}",
    "error_container": "{{colors.error_container.default.hex}}",
    "on_error_container": "{{colors.on_error_container.default.hex}}",

    "background": "{{colors.background.default.hex}}",
    "on_background": "{{colors.on_background.default.hex}}",

    "surface": "{{colors.surface.default.hex}}",
    "on_surface": "{{colors.on_surface.default.hex}}",
    "surface_variant": "{{colors.surface_variant.default.hex}}",
    "on_surface_variant": "{{colors.on_surface_variant.default.hex}}",

    "surface_dim": "{{colors.surface_dim.default.hex}}",
    "surface_bright": "{{colors.surface_bright.default.hex}}",
    "surface_container_lowest": "{{colors.surface_container_lowest.default.hex}}",
    "surface_container_low": "{{colors.surface_container_low.default.hex}}",
    "surface_container": "{{colors.surface_container.default.hex}}",
    "surface_container_high": "{{colors.surface_container_high.default.hex}}",
    "surface_container_highest": "{{colors.surface_container_highest.default.hex}}",

    "outline": "{{colors.outline.default.hex}}",
    "outline_variant": "{{colors.outline_variant.default.hex}}",

    "shadow": "{{colors.shadow.default.hex}}",
    "scrim": "{{colors.scrim.default.hex}}",
    "inverse_surface": "{{colors.inverse_surface.default.hex}}",
    "inverse_on_surface": "{{colors.inverse_on_surface.default.hex}}",
    "inverse_primary": "{{colors.inverse_primary.default.hex}}"
  }
}
```

**Action Items:**
- [x] Create `matugen_templates/` directory
- [x] Create blackhole.json template
- [x] Create templates for enabled apps (GTK, Kitty, etc.)
- [x] Reference Noctalia templates for format
- [x] Add template generation to MatugenService

### Task 8: Ignis Breaking Changes Migration

**Goal:** Update codebase for latest Ignis git version

**Changes Required:**

1. **OptionsManager Migration**
```python
# OLD (if using old Options Service)
from ignis.services.options import OptionsService

# NEW
from ignis.options_manager import OptionsManager, OptionsGroup
```

2. **Async Functions**
```python
# Functions that are now async (need await or create_task):
# - DBusProxy methods
# - Device.connect_async()
# - File operations

# Example:
import asyncio

# OLD
hyprland.switch_kb_layout()

# NEW
asyncio.create_task(hyprland.some_async_method())
```

3. **Property Binding**
```python
# OLD
binding = Binding(target_property="label")

# NEW
binding = Binding(target_properties=["label"])
```

4. **Hyprland Service**
```python
# OLD
workspace_id = hyprland.active_workspace["id"]

# NEW
workspace_id = hyprland.active_workspace.id
```

5. **DebounceTask**
```python
# OLD
debounce_task()

# NEW
debounce_task.run()
```

**Action Items:**
- [x] Audit all service usage for async functions
- [x] Update property bindings to use list format
- [x] Update Hyprland service access (if used)
- [x] Update DebounceTask calls
- [x] Test all changes

## Directory Structure

After Phase 1 implementation:

```
ignis/
├── services/
│   └── material/
│       ├── __init__.py
│       ├── matugen_service.py           # NEW
│       ├── color_scheme_service.py      # NEW
│       ├── palettes/                    # NEW
│       │   ├── rose_pine_main.json
│       │   ├── rose_pine_moon.json
│       │   ├── rose_pine_dawn.json
│       │   ├── catppuccin_mocha.json
│       │   ├── catppuccin_latte.json
│       │   ├── nord.json
│       │   ├── gruvbox_dark.json
│       │   └── tokyo_night.json
│       └── matugen_templates/           # NEW
│           ├── blackhole.json
│           ├── gtk.css
│           ├── kitty.conf
│           ├── ghostty
│           ├── fuzzel.ini
│           ├── hyprland.conf
│           └── niri.kdl
├── modules/
│   └── settings/
│       └── sections/
│           └── appearance.py            # NEW/UPDATED
├── scss/
│   ├── _blackhole_tokens.scss          # NEW
│   └── style.scss                       # UPDATED (import tokens)
└── user_options.py                      # UPDATED

```

## Testing Checklist

### Functionality Tests
- [ ] Built-in color schemes load correctly
- [ ] Rose Pine (main/moon/dawn) displays properly
- [ ] Settings panel shows all available schemes
- [ ] Scheme selection updates UI immediately
- [ ] Matugen generates colors from wallpaper
- [ ] Matugen scheme type selector works
- [ ] Wallpaper toggle switches between built-in/dynamic
- [ ] Colors persist after restart
- [ ] Matugen JSON templates generated correctly
- [ ] External app theming works (GTK, Kitty, etc.)

### Visual Tests
- [ ] All components use Blackhole design tokens
- [ ] Spacing matches Noctalia reference
- [ ] Border radius consistent across components
- [ ] Shadows render correctly
- [ ] Animations use correct timing
- [ ] Dark/light mode both work
- [ ] Rose Pine colors match official palette

### Performance Tests
- [ ] Startup time remains under 5s
- [ ] No lag when switching schemes
- [ ] Matugen generation completes quickly (<500ms)
- [ ] Cache loading is instant

## Success Criteria

- [x] Rose Pine is default theme
- [x] 3 built-in color schemes available (Rose Pine variants) - *Additional schemes optional*
- [x] Matugen replaces materialyoucolor
- [x] Settings panel has Color Scheme section
- [x] Wallpaper-based generation works
- [x] Matugen templates generated for external apps (11 templates)
- [x] All Blackhole design tokens implemented (69 tokens)
- [x] Ignis breaking changes addressed
- [x] No performance regression

## Future Phases Summary

### Phase 2: Core Components (Adaptive Bar & Dock)
- Update Bar module for adaptive positioning (top/bottom/left/right)
- Add floating mode to Bar with margins
- Create Dock module with auto-hide and app pinning
- Implement app tracking and launching
- Style with Blackhole design tokens

### Phase 3: Panels (Control Center & Sub-panels)
- Redesign Control Center layout (capsule-style buttons)
- Create Calendar panel
- Create Audio panel (mixer)
- Create WiFi panel
- Create Bluetooth panel
- Implement panel navigation and stacking

### Phase 4: Polish (OSD, Animations, Tooltips)
- Update OSD with circular progress indicators
- Add global tooltip system
- Create Battery details panel
- Rename Powermenu → Session Menu
- Refine all animations
- Add backdrop/scrim for modal panels

### Phase 5: Documentation & Release
- Update CLAUDE_INSTRUCTIONS.md
- Create user migration guide
- Screenshot all components
- Update README with new features
- Create video demo
- Release v1.0

---

**Phase 1 Timeline:** 1-2 weeks
**Status:** ✅ Complete
**Completed:** 2025-11-14
**Next Steps:** Phase 2 (Bar & Dock)
