# Ignis-Blackholeshell Performance Analysis

**Date:** 2025-11-04
**Total Startup Time:** ~2.5 seconds
**Status:** ✅ Root cause identified

## Executive Summary

Startup performance bottleneck identified in MaterialService initialization that happens at module import time.

## Profiling Results

```
Total Startup: 2.562s

Breakdown:
- Import modules:        2.309s (90%)  ⚠️ BOTTLENECK
- Create ControlCenter:  0.156s (6%)
- Apply CSS:             0.026s (1%)
- Everything else:       0.071s (3%)
```

## Root Cause

**MaterialService** initialization (called when importing `control_center/widgets/media.py`):

1. **PIL Image Loading** - Opens wallpaper image
2. **Image Resizing** - BICUBIC resampling
3. **Color Quantization** - QuantizeCelebi algorithm on 128 colors
4. **Color Scheme Generation** - Material You color scheme computation
5. **Template Rendering** - Jinja2 template generation

**Location:** `ignis/services/material/service.py:26-40`

**Why it's slow:**
- Heavy image processing at import time
- Happens EVERY startup (no caching of generated colors)
- Synchronous operations block startup

## Optimization Strategies

### Priority 1: Lazy Initialization ⭐

**Impact:** Reduce startup by ~2s
**Effort:** Medium

**Change:** Don't initialize MaterialService until first use

```python
# Current (BAD):
material = MaterialService.get_default()  # Runs at import!

# Proposed (GOOD):
material = None  # Lazy initialize only when needed

def get_material_service():
    global material
    if material is None:
        material = MaterialService.get_default()
    return material
```

### Priority 2: Color Caching

**Impact:** Reduce subsequent startups to <0.5s
**Effort:** Low

**Change:** Cache generated colors to disk

```python
# Cache file: ~/.cache/ignis/material_colors.json
{
    "wallpaper_hash": "abc123...",
    "dark_mode": true,
    "colors": {...},
    "generated_at": "2025-11-04T20:00:00"
}
```

If wallpaper hasn't changed, load from cache instead of regenerating.

### Priority 3: Async Color Generation

**Impact:** UI shows faster, colors load in background
**Effort:** High

**Change:** Generate colors asynchronously

```python
async def generate_colors_async(self, path: str) -> None:
    # Use default colors first
    # Generate real colors in background
    # Update UI when ready
```

### Priority 4: Import Optimization

**Impact:** Reduce import overhead by ~0.3s
**Effort:** Low

**Changes:**
1. Move heavy imports inside functions where needed
2. Use lazy imports for materialyoucolor
3. Import PIL only when actually processing images

## Quick Wins (Implement First)

### 1. Remove Eager MaterialService Init

**File:** `modules/control_center/widgets/media.py`

```python
# Line 8-15: BEFORE
from services.material import MaterialService
...
material = MaterialService.get_default()

# AFTER
from services.material import MaterialService
...
# Don't initialize at module level!
# Initialize only when Player widget is created
```

### 2. Cache Color Generation

**File:** `services/material/service.py`

Add method:
```python
def load_cached_colors(self, wallpaper_path: str) -> dict | None:
    cache_file = f"{MATERIAL_CACHE_DIR}/colors_cache.json"
    if not os.path.exists(cache_file):
        return None

    # Check if wallpaper changed
    # Return cached colors if still valid
```

### 3. Use Default Colors First

Generate colors in background while showing default Material You palette.

## Expected Results

**Before optimization:**
```
Total startup: 2.5s
- Module imports: 2.3s
```

**After Quick Wins (1+2):**
```
Total startup: 0.5s
- Module imports: 0.3s
- First run: 2.5s (generates cache)
- Subsequent: 0.2s (uses cache)
```

**After Full Async (1+2+3):**
```
Total startup: 0.3s
- UI visible immediately
- Colors load in <1s background
```

## Deprecation Warnings

Separate issue to fix:

1. **Gio.DesktopAppInfo** → Use **GioUnix.DesktopAppInfo**
   - File: `/usr/lib/python3.13/site-packages/ignis/services/applications/`
   - Impact: None (just warnings)
   - Fix: Update ignis library or ignore

2. **Gdk.Texture.new_for_pixbuf** deprecated
   - File: `/usr/lib/python3.13/site-packages/ignis/widgets/picture.py:112`
   - Impact: None (just warnings)
   - Fix: Update ignis library

## Next Steps

1. ✅ Profiling complete
2. ⏭️ Implement Quick Win #1 (remove eager init)
3. ⏭️ Implement Quick Win #2 (color caching)
4. ⏭️ Test startup performance
5. ⏭️ Implement async generation if needed

## Notes

- MaterialService is well-designed for runtime color changes
- The issue is only startup performance
- Solution: Don't run heavy computations at import time
- Keep the architecture, just make it lazy

---

**Analysis complete.** Ready to implement optimizations.
