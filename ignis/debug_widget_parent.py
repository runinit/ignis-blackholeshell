"""
Debug helper to identify widget re-parenting issues.
This patches Gtk.Box.append to log when widgets already have parents.
"""
from gi.repository import Gtk
import traceback
import sys

_original_append = Gtk.Box.append

def debug_append(self, child):
    """Wrapper for Gtk.Box.append that logs parent conflicts."""
    if child.get_parent() is not None:
        print("\n" + "="*80, file=sys.stderr)
        print("ERROR: Attempting to append widget that already has a parent!", file=sys.stderr)
        print(f"  Widget type: {type(child).__name__}", file=sys.stderr)
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
print("Widget parent debugging enabled", file=sys.stderr)
