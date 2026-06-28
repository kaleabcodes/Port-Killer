#!/usr/bin/env bash
# ──────────────────────────────────────────────────────────────
#  Port Killer — Uninstaller
#  Removes Port Killer from the system.
# ──────────────────────────────────────────────────────────────
set -euo pipefail

APP_NAME="Port Killer"
APP_ID="com.kaleabcodes.portkiller"
INSTALL_DIR="/opt/portkiller"
BIN_LINK="/usr/local/bin/portkiller"
DESKTOP_FILE="/usr/share/applications/${APP_ID}.desktop"
ICON_FILE="/usr/share/icons/hicolor/scalable/apps/${APP_ID}.svg"

RED='\033[0;31m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
BOLD='\033[1m'
RESET='\033[0m'

info()  { echo -e "${CYAN}▸${RESET} $*"; }
ok()    { echo -e "${GREEN}✔${RESET} $*"; }
fail()  { echo -e "${RED}✖${RESET} $*"; exit 1; }

[[ $EUID -ne 0 ]] && fail "Please run with ${BOLD}sudo${RESET}:\n   sudo bash uninstall.sh"

echo ""
echo -e "${BOLD}🔌 Uninstalling ${APP_NAME}...${RESET}"
echo ""

info "Removing application files..."
rm -rf "$INSTALL_DIR"
ok "Removed ${INSTALL_DIR}"

info "Removing launcher command..."
rm -f "$BIN_LINK"
ok "Removed ${BIN_LINK}"

info "Removing desktop entry..."
rm -f "$DESKTOP_FILE"
ok "Removed desktop entry"

info "Removing icon..."
rm -f "$ICON_FILE"
ok "Removed icon"

# Update caches
if command -v update-desktop-database >/dev/null 2>&1; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi
if command -v gtk-update-icon-cache >/dev/null 2>&1; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo ""
echo -e "${GREEN}${BOLD}✅ ${APP_NAME} has been uninstalled.${RESET}"
echo ""
