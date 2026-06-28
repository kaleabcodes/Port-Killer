import threading
import subprocess
import sys
import os
from gi.repository import Adw, Gio, GLib, Gtk
from window import MainWindow

import importlib.util
TRAY_AVAILABLE = importlib.util.find_spec("pystray") is not None

class PortKillerApp(Adw.Application):
    def __init__(self):
        super().__init__(application_id="com.kaleabcodes.portkiller",
                         flags=Gio.ApplicationFlags.DEFAULT_FLAGS)
        self._tray_proc = None
        self._win = None
        self._setup_actions()

    def _setup_actions(self):
        about_action = Gio.SimpleAction.new("about", None)
        about_action.connect("activate", self._on_about)
        self.add_action(about_action)

        refresh_action = Gio.SimpleAction.new("refresh", None)
        refresh_action.connect("activate", lambda *_: self._refresh())
        self.add_action(refresh_action)

        quit_action = Gio.SimpleAction.new("quit", None)
        quit_action.connect("activate", lambda *_: self._quit())
        self.add_action(quit_action)

    def do_activate(self):
        if not self._win:
            self._win = MainWindow(self)
            self._win.set_title("Port Killer")
            if TRAY_AVAILABLE:
                self._start_tray()
        self._win.present()

    def _refresh(self):
        if self._win:
            self._win.load_ports()

    def _start_tray(self):
        tray_script = os.path.join(os.path.dirname(__file__), "utils", "tray.py")
        try:
            self._tray_proc = subprocess.Popen(
                [sys.executable, tray_script],
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                text=True
            )
        except Exception as e:
            print("Failed to start tray:", e)
            return

        def listen():
            for line in self._tray_proc.stdout:
                cmd = line.strip()
                if cmd == "show":
                    GLib.idle_add(self._win.show_window)
                elif cmd == "refresh":
                    GLib.idle_add(self._win.load_ports)
                elif cmd == "quit":
                    GLib.idle_add(self._quit)
                    
        t = threading.Thread(target=listen, daemon=True)
        t.start()

    def _quit(self):
        if self._tray_proc:
            self._tray_proc.terminate()
        self.quit()

    def _on_about(self, *_):
        dlg = Adw.AboutDialog(
            application_name="Port Killer",
            application_icon="network-server-symbolic",
            version="3.0",
            comments="View and terminate listening ports on your system.",
            developer_name="KaleabCodes",
            copyright="© 2026 KaleabCodes",
            license_type=Gtk.License.MIT_X11,
            website="https://github.com/kaleabcodes/port-killer",
            issue_url="https://github.com/kaleabcodes/port-killer/issues",
        )
        dlg.present(self._win)
