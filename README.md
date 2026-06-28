<div align="center">

# 🔌 Port Killer

**A native GTK4 / Libadwaita desktop app for Linux to view and terminate processes listening on network ports.**

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![GTK](https://img.shields.io/badge/GTK-4.0-4A90D9?style=flat&logo=gnome&logoColor=white)](https://gtk.org)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Linux-FCC624?style=flat&logo=linux&logoColor=black)](https://kernel.org)
[![Release](https://img.shields.io/github/v/release/kaleabcodes/port-killer?style=flat&color=blueviolet&label=Release)](https://github.com/kaleabcodes/port-killer/releases/latest)

</div>

---

<div align="center">
  <img src="assets/portkiller.gif" alt="Port Killer Demo" width="100%">
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

- 🐧 **Linux** with GNOME desktop
- 🐍 **Python** `3.10+`
- 🖼️ **GTK4** and **Libadwaita** (usually pre-installed on GNOME desktops)

  ```bash
  # Ubuntu / Debian — install if not already present
  sudo apt install libgtk-4-dev libadwaita-1-dev gir1.2-adw-1
  ```

---

## 🚀 Installation

> Download the latest package from the [**Releases**](https://github.com/kaleabcodes/port-killer/releases/latest) page.

### 🐧 Debian / Ubuntu / Pop!_OS / Mint (`.deb`)

```bash
sudo dpkg -i portkiller_1.0.0_all.deb
sudo apt-get install -f    # fix any missing dependencies
```

### 🎩 Fedora / RHEL / openSUSE (`.rpm`)

```bash
sudo rpm -i portkiller-1.0.0-1.noarch.rpm
```

### 📦 Generic Linux (`.tar.gz`)

```bash
tar -xzf portkiller-v1.0.0-linux.tar.gz
cd portkiller-v1.0.0-linux
sudo bash install.sh
```

After installation, launch **Port Killer** from your app menu or run:

```bash
portkiller
```

### 🛠️ Build from source *(for development)*

```bash
git clone https://github.com/kaleabcodes/port-killer.git
cd port-killer
python3 -m venv .venv
source .venv/bin/activate
pip install psutil pystray Pillow
python3 main.py
```

---

## 🗑️ Uninstall

```bash
# Debian / Ubuntu
sudo apt remove portkiller

# Fedora / RHEL
sudo rpm -e portkiller

# Generic (tar.gz install)
sudo bash uninstall.sh
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
