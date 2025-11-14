"""
Debug helper to track initialization and identify issues.
"""
from gi.repository import Gtk
import traceback
import sys

print("\n" + "="*80, file=sys.stderr)
print("IGNIS INITIALIZATION DEBUG MODE ENABLED", file=sys.stderr)
print("="*80 + "\n", file=sys.stderr)

# Track widget creation
_widget_count = {}

_original_append = Gtk.Box.append

def debug_append(self, child):
    """Wrapper for Gtk.Box.append that logs parent conflicts."""
    widget_type = type(child).__name__
    _widget_count[widget_type] = _widget_count.get(widget_type, 0) + 1

    if child.get_parent() is not None:
        print("\n" + "="*80, file=sys.stderr)
        print("ERROR: Attempting to append widget that already has a parent!", file=sys.stderr)
        print(f"  Widget type: {widget_type}", file=sys.stderr)
        print(f"  Widget: {child}", file=sys.stderr)
        print(f"  Current parent: {child.get_parent()}", file=sys.stderr)
        print(f"  New parent (Box): {self}", file=sys.stderr)
        print("\nStack trace:", file=sys.stderr)
        for line in traceback.format_stack()[:-1]:
            print(line.strip(), file=sys.stderr)
        print("="*80 + "\n", file=sys.stderr)

    return _original_append(self, child)

# Monkey patch Gtk.Box.append
Gtk.Box.append = debug_append

# Track module initialization
original_import = __builtins__.__import__

def debug_import(name, *args, **kwargs):
    result = original_import(name, *args, **kwargs)
    if name.startswith('modules.'):
        print(f"[INIT] Importing: {name}", file=sys.stderr)
    return result

__builtins__.__import__ = debug_import

print("Widget parent debugging enabled", file=sys.stderr)
print("Module import tracking enabled", file=sys.stderr)
print("", file=sys.stderr)
