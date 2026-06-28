import os
from gi.repository import Gtk, Adw, GLib, Gio
from widgets.port_row import PortRow
from utils.process import get_active_ports
import importlib.util
TRAY_AVAILABLE = importlib.util.find_spec("pystray") is not None

class MainWindow(Adw.ApplicationWindow):
    def __init__(self, app):
        super().__init__(application=app)
        self.set_default_size(540, 720)
        self.set_size_request(360, 500)
        self._rows = []

        # Load CSS
        provider = Gtk.CssProvider()
        css_path = os.path.join(os.path.dirname(__file__), "style.css")
        provider.load_from_path(css_path)
        Gtk.StyleContext.add_provider_for_display(
            self.get_display(), provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
        )

        self._setup_ui()
        self.load_ports()

    def _setup_ui(self):
        # Header bar
        header = Adw.HeaderBar()

        refresh_btn = Gtk.Button(icon_name="view-refresh-symbolic")
        refresh_btn.set_tooltip_text("Refresh ports")
        refresh_btn.connect("clicked", lambda *_: self.load_ports())

        menu_btn = Gtk.MenuButton()
        menu_btn.set_icon_name("open-menu-symbolic")
        menu_btn.set_tooltip_text("Menu")
        menu = Gio.Menu()
        menu.append("About Port Killer", "app.about")
        menu.append("Refresh", "app.refresh")
        menu.append("Quit", "app.quit")
        menu_btn.set_menu_model(menu)

        header.pack_end(menu_btn)
        header.pack_start(refresh_btn)

        # Search
        self._search = Gtk.SearchEntry()
        self._search.set_placeholder_text("Search by name, port, or PID…")
        self._search.connect("search-changed", self._filter)
        self._search.connect("stop-search", self._clear_search)

        # List
        self._listbox = Gtk.ListBox()
        self._listbox.set_selection_mode(Gtk.SelectionMode.NONE)
        self._listbox.add_css_class("boxed-list")
        self._listbox.set_margin_top(8)
        self._listbox.set_margin_bottom(8)

        self._prefs_group = Adw.PreferencesGroup()
        self._prefs_group.add(self._listbox)

        scroll = Gtk.ScrolledWindow()
        scroll.set_vexpand(True)
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scroll.set_child(self._prefs_group)

        # Empty state
        self._status_page = Adw.StatusPage()
        self._status_page.set_icon_name("network-offline-symbolic")
        self._status_page.set_title("No listening ports")
        self._status_page.set_description("All clear — nothing is listening right now")
        self._status_page.add_css_class("status-page")

        # Stack
        self._stack = Gtk.Stack()
        self._stack.set_transition_type(Gtk.StackTransitionType.CROSSFADE)
        self._stack.set_transition_duration(300)
        self._stack.add_named(scroll, "list")
        self._stack.add_named(self._status_page, "empty")

        # Inner layout
        inner = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=16)
        inner.set_margin_start(16)
        inner.set_margin_end(16)
        inner.set_margin_top(16)
        inner.set_margin_bottom(16)
        inner.append(self._search)
        inner.append(self._stack)

        clamp = Adw.Clamp()
        clamp.set_maximum_size(540)
        clamp.set_tightening_threshold(400)
        clamp.set_child(inner)

        toolbar_view = Adw.ToolbarView()
        toolbar_view.add_top_bar(header)
        toolbar_view.set_content(clamp)

        # Toast overlay
        self._toast_overlay = Adw.ToastOverlay()
        self._toast_overlay.set_child(toolbar_view)
        self.set_content(self._toast_overlay)

        # Close → hide to tray
        self.connect("close-request", self._on_close)

    def _clear_search(self, _):
        self._search.set_text("")
        self._filter()


    def _on_close(self, *_):
        if TRAY_AVAILABLE:
            self.set_visible(False)
            return True
        return False

    def show_window(self):
        self.set_visible(True)
        self.present()

    def load_ports(self):
        while (c := self._listbox.get_first_child()):
            self._listbox.remove(c)
        self._rows.clear()

        try:
            ports = get_active_ports()
        except PermissionError as e:
            self._set_empty("Access Denied", str(e))
            return

        for p in ports:
            row = PortRow(p["pid"], p["name"], p["ip"], p["port"], p["status"], self.load_ports, self._show_toast)
            self._rows.append(row)
            self._listbox.append(row)

        self._update_visibility()

    def _filter(self, *_):
        self._update_visibility()

    def _update_visibility(self):
        text = self._search.get_text().lower()
        visible = 0
        for row in self._rows:
            show = (not text
                    or text in row.get_title().lower()
                    or text in row.get_subtitle().lower()
                    or text in str(row.pid))
            row.set_visible(show)
            if show:
                visible += 1

        total = len(self._rows)
        if total == 0:
            self._set_empty("No listening ports", "All clear — nothing is listening right now")
        elif visible == 0:
            self._set_empty("No matches", f'Nothing matches "{self._search.get_text()}"')
        else:
            self._stack.set_visible_child_name("list")
            self._prefs_group.set_title(f"Active Ports ({visible})")

    def _show_toast(self, message):
        toast = Adw.Toast(title=message)
        toast.set_timeout(3)
        toast.set_button_label("Dismiss")
        self._toast_overlay.add_toast(toast)

    def _set_empty(self, title, sub):
        self._status_page.set_title(title)
        self._status_page.set_description(sub)
        self._stack.set_visible_child_name("empty")
