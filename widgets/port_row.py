from gi.repository import Gtk, Adw
from utils.process import kill_process

class PortRow(Adw.ActionRow):
    def __init__(self, pid, name, ip, port, status, refresh_cb, toast_cb):
        super().__init__()
        self.pid = pid
        self.refresh_cb = refresh_cb
        self.toast_cb = toast_cb
        self.is_killing = False

        # Set main content
        self.set_title(name)
        self.set_subtitle(f"PID {pid}  •  {ip}")
        self.set_title_lines(1)
        self.set_subtitle_lines(1)

        # Add CSS class for styling
        self.add_css_class("port-row")

        # Process icon
        icon = Gtk.Image(icon_name="network-server-symbolic")
        icon.set_pixel_size(24)
        icon.set_margin_start(8)
        icon.set_margin_end(8)
        icon.add_css_class("accent")
        self.add_prefix(icon)

        # Port badge
        port_badge = Gtk.Label(label=str(port))
        port_badge.add_css_class("numeric")
        self.add_suffix(port_badge)


        # Modern kill button with text
        kill_btn = Gtk.Button(label="Kill")
        kill_btn.add_css_class("destructive-action")
        kill_btn.set_tooltip_text("Terminate process")
        kill_btn.set_valign(Gtk.Align.CENTER)
        kill_btn.connect("clicked", self._on_kill, kill_btn)
        self.add_suffix(kill_btn)

        # Row should not be clickable, only the button
        self.set_activatable(False)

    def _on_kill(self, _widget, btn):
        if self.is_killing:
            return

        self.is_killing = True
        btn.set_sensitive(False)
        btn.set_label("Killing…")

        kill_process(self.pid, self._kill_success, self._kill_already_dead, self._kill_error)

    def _kill_success(self):
        self.toast_cb(f"Process {self.pid} terminated successfully")
        self.refresh_cb()

    def _kill_already_dead(self):
        self.toast_cb("Process no longer exists")
        self.refresh_cb()

    def _kill_error(self, error):
        self.is_killing = False
        self.toast_cb(f"Error: {error}")
        self.refresh_cb()
