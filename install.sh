#!/usr/bin/env bash
# ──────────────────────────────────────────────────────────────
#  Port Killer — Installer
#  Installs Port Killer as a native GNOME desktop application.
# ──────────────────────────────────────────────────────────────
set -euo pipefail

APP_NAME="Port Killer"
APP_ID="com.kaleabcodes.portkiller"
INSTALL_DIR="/opt/portkiller"
VENV_DIR="$INSTALL_DIR/.venv"
BIN_LINK="/usr/local/bin/portkiller"
DESKTOP_FILE="/usr/share/applications/${APP_ID}.desktop"
ICON_DIR="/usr/share/icons/hicolor/scalable/apps"
ICON_FILE="${ICON_DIR}/${APP_ID}.svg"

# ── Colors ────────────────────────────────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
BOLD='\033[1m'
RESET='\033[0m'

info()  { echo -e "${CYAN}▸${RESET} $*"; }
ok()    { echo -e "${GREEN}✔${RESET} $*"; }
fail()  { echo -e "${RED}✖${RESET} $*"; exit 1; }

# ── Pre-flight checks ────────────────────────────────────────
[[ $EUID -ne 0 ]] && fail "Please run this installer with ${BOLD}sudo${RESET}:\n   sudo bash install.sh"

command -v python3 >/dev/null 2>&1 || fail "python3 is not installed. Please install Python 3.10+."

PYTHON_VERSION=$(python3 -c 'import sys; print(sys.version_info >= (3, 10))')
[[ "$PYTHON_VERSION" != "True" ]] && fail "Python 3.10+ is required. Found: $(python3 --version)"

# Check GTK4 + Libadwaita
python3 -c "
import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw
" 2>/dev/null || fail "GTK4 and Libadwaita are required.\n   Install with: ${BOLD}sudo apt install libgtk-4-dev libadwaita-1-dev gir1.2-adw-1${RESET}"

echo ""
echo -e "${BOLD}🔌 Installing ${APP_NAME}...${RESET}"
echo ""

# ── Determine source directory ────────────────────────────────
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# ── Copy application files ────────────────────────────────────
info "Copying application files to ${INSTALL_DIR}..."
mkdir -p "$INSTALL_DIR"
cp -r "$SCRIPT_DIR"/main.py \
      "$SCRIPT_DIR"/app.py \
      "$SCRIPT_DIR"/window.py \
      "$SCRIPT_DIR"/style.css \
      "$SCRIPT_DIR"/utils \
      "$SCRIPT_DIR"/widgets \
      "$INSTALL_DIR/"
ok "Application files copied"

# ── Create virtual environment & install deps ─────────────────
info "Setting up Python virtual environment..."
python3 -m venv "$VENV_DIR"
"$VENV_DIR/bin/pip" install --quiet --upgrade pip
"$VENV_DIR/bin/pip" install --quiet psutil pystray Pillow
ok "Python dependencies installed"

# ── Create launcher script ────────────────────────────────────
info "Creating launcher command..."
cat > "$BIN_LINK" << 'LAUNCHER'
#!/usr/bin/env bash
exec /opt/portkiller/.venv/bin/python3 /opt/portkiller/main.py "$@"
LAUNCHER
chmod +x "$BIN_LINK"
ok "Launcher created at ${BIN_LINK}"

# ── Install icon ──────────────────────────────────────────────
info "Installing application icon..."
mkdir -p "$ICON_DIR"
if [[ -f "$SCRIPT_DIR/${APP_ID}.svg" ]]; then
    cp "$SCRIPT_DIR/${APP_ID}.svg" "$ICON_FILE"
    ok "Icon installed"
else
    info "Icon SVG not found, skipping (will use fallback icon)"
fi

# ── Install .desktop file ────────────────────────────────────
info "Installing desktop entry..."
cat > "$DESKTOP_FILE" << EOF
[Desktop Entry]
Name=${APP_NAME}
Comment=View and terminate processes listening on network ports
Exec=portkiller
Icon=${APP_ID}
Terminal=false
Type=Application
Categories=System;Network;Monitor;GTK;
Keywords=port;kill;process;network;socket;
StartupNotify=true
EOF
ok "Desktop entry installed"

# ── Update desktop database ───────────────────────────────────
if command -v update-desktop-database >/dev/null 2>&1; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi
if command -v gtk-update-icon-cache >/dev/null 2>&1; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo ""
echo -e "${GREEN}${BOLD}✅ ${APP_NAME} installed successfully!${RESET}"
echo ""
echo -e "   Launch from your app menu or run:  ${BOLD}portkiller${RESET}"
echo ""
