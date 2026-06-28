"""
Port Killer — GTK4 / Adwaita
Modern UI Design with improved visuals and interactions
"""
import gi

# --- Hack to allow Gtk3 (for pystray) and Gtk4 in the same process ---
def patched_require_version(namespace, version):
    if namespace == 'Gtk' and version == '3.0':
        return
    gi._old_require_version(namespace, version)

gi._old_require_version = gi.require_version
gi.require_version = patched_require_version
# --------------------------------------------------------------------

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Adw
Adw.init()

from app import PortKillerApp

def main():
    app = PortKillerApp()
    app.run()

if __name__ == "__main__":
    main()