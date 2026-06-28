<div align="center">

# 🔌 Port Killer

**A native GTK4 / Libadwaita desktop app for Linux to view and terminate processes listening on network ports.**

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![GTK](https://img.shields.io/badge/GTK-4.0-4A90D9?style=flat&logo=gnome&logoColor=white)](https://gtk.org)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Linux-FCC624?style=flat&logo=linux&logoColor=black)](https://kernel.org)

</div>

---

<div align="center">
  <video src="assets/portkiller.mp4" width="100%" autoplay loop muted controls></video>
</div>

---

## ✨ Features

| Feature | Description |
|---|---|
| 🖥️ **Native GNOME UI** | Clean, minimal interface built with Libadwaita – looks at home in any GNOME desktop |
| 🔍 **Smart Search** | Instantly filter ports by PID, port number, or application name |
| 🗑️ **One-click Kill** | Terminate any process with a single click of the Kill button |
| 🔔 **System Tray** | Hides to the system tray on close so it's always ready in the background |
| ⚡ **Safe Termination** | Gracefully escalates from `SIGTERM` → `SIGKILL` with a timeout |
| 🌓 **Theme Aware** | Fully respects your system's light/dark mode and accent color |

---

## 📦 Prerequisites

Before you begin, make sure you have the following installed on your system:

- 🐍 **Python** `3.10+`
- 🖼️ **GTK4** and **Libadwaita** (usually pre-installed on GNOME desktops)
- 📡 **`psutil`** – for reading network and process info
- 🖼️ **`pystray`** + **`Pillow`** – for the system tray icon *(optional)*

---

## 🚀 Installation & Running

### Step 1 — Clone the repository

```bash
git clone https://github.com/kaleabcodes/port-killer.git
cd port-killer
```

### Step 2 — Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Step 3 — Install dependencies

```bash
pip install psutil pystray Pillow
```

### Step 4 — Run the app

```bash
python3 main.py
```

---

## 🗂️ Project Structure

```
PortKiller/
├── main.py              # 🚪 Entry point
├── app.py               # 🧠 Application lifecycle & actions
├── window.py            # 🪟 Main window UI layout
├── style.css            # 🎨 Custom CSS overrides
├── widgets/
│   └── port_row.py      # 📦 Port list row widget
└── utils/
    ├── process.py        # ⚙️  psutil logic (port scanning, killing)
    └── tray.py           # 🔔 System tray icon (subprocess)
```

---

## 📸 Usage

1. Launch the app — it will immediately scan all listening ports on your system.
2. Use the **search bar** to filter by name, PID, or port number.
3. Click the **Kill** button on any row to terminate that process.
4. Use the **↻ refresh** button (top-left) to re-scan ports.
5. Close the window — the app hides to the **system tray**. Right-click the tray icon for options.

---

## 📜 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

Made with ❤️ by **KaleabCodes**

</div>
