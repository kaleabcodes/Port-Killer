import sys
import os

try:
    import pystray
    from PIL import Image, ImageDraw
except ImportError:
    sys.exit(1)

os.environ['PYSTRAY_BACKEND'] = 'appindicator'

def make_tray_image(size=64):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.ellipse([2, 2, size - 2, size - 2], fill=(30, 30, 46, 230))
    cx, cy = size // 2, size // 2
    prong_w, prong_h = size // 10, size // 5
    gap = size // 8
    d.rectangle([cx - gap - prong_w, cy - size // 3, cx - gap, cy - size // 8], fill=(137, 180, 250, 255))
    d.rectangle([cx + gap, cy - size // 3, cx + gap + prong_w, cy - size // 8], fill=(137, 180, 250, 255))
    d.rounded_rectangle([cx - size // 4, cy - size // 8, cx + size // 4, cy + size // 3], radius=size // 12, fill=(137, 180, 250, 255))
    d.rectangle([cx - size // 12, cy + size // 3, cx + size // 12, cy + size // 3 + size // 8], fill=(108, 112, 134, 255))
    return img

def on_show(icon, item):
    print("show", flush=True)

def on_refresh(icon, item):
    print("refresh", flush=True)

def on_quit(icon, item):
    print("quit", flush=True)
    icon.stop()

def run():
    menu = pystray.Menu(
        pystray.MenuItem("Show Port Killer", on_show, default=True),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem("Refresh ports", on_refresh),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem("Quit", on_quit),
    )

    img = make_tray_image(64)
    icon = pystray.Icon("portkiller", img, "Port Killer", menu)
    icon.run()

if __name__ == "__main__":
    run()
