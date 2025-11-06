#!/usr/bin/env python3
import sys
import os
import time

# Add ignis directory to path
sys.path.insert(0, '/home/chris/src/amplifier/ignis-blackholeshell/ignis')

# Add venv to path
venv_path = "/home/chris/src/amplifier/ignis-blackholeshell/ignis/.venv/lib/python3.13/site-packages"
if os.path.exists(venv_path):
    sys.path.insert(0, venv_path)

modules_to_test = [
    "modules.bar",
    "modules.control_center",
    "modules.launcher",
    "modules.notification_popup",
    "modules.osd",
    "modules.powermenu",
    "modules.settings",
    "modules.wallpaper_picker",
]

print("Testing individual module import times:\n")
print(f"{'Module':<40} {'Time (s)':<10}")
print("=" * 50)

for module_name in modules_to_test:
    start = time.perf_counter()
    try:
        __import__(module_name)
        elapsed = time.perf_counter() - start
        print(f"{module_name:<40} {elapsed:>8.3f}s")
    except Exception as e:
        elapsed = time.perf_counter() - start
        print(f"{module_name:<40} {elapsed:>8.3f}s  ERROR: {str(e)[:30]}")
