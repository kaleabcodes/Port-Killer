Name:           portkiller
Version:        %{_app_version}
Release:        1%{?dist}
Summary:        View and terminate processes listening on network ports
License:        MIT
URL:            https://github.com/kaleabcodes/port-killer
BuildArch:      noarch

Requires:       python3 >= 3.10
Requires:       python3-venv
Requires:       gtk4
Requires:       libadwaita

%description
Port Killer is a native GTK4 / Libadwaita desktop application for Linux
to view and terminate processes listening on network ports. It provides
a clean GNOME-native interface with smart search, one-click kill,
and system tray integration.

%install
mkdir -p %{buildroot}/opt/portkiller
mkdir -p %{buildroot}/usr/bin
mkdir -p %{buildroot}/usr/share/applications
mkdir -p %{buildroot}/usr/share/icons/hicolor/scalable/apps

cp -r %{_sourcedir}/app/* %{buildroot}/opt/portkiller/
install -m 0755 %{_sourcedir}/portkiller %{buildroot}/usr/bin/portkiller
install -m 0644 %{_sourcedir}/com.kaleabcodes.portkiller.desktop %{buildroot}/usr/share/applications/
install -m 0644 %{_sourcedir}/com.kaleabcodes.portkiller.svg %{buildroot}/usr/share/icons/hicolor/scalable/apps/

%post
python3 -m venv /opt/portkiller/.venv
/opt/portkiller/.venv/bin/pip install --quiet --upgrade pip
/opt/portkiller/.venv/bin/pip install --quiet psutil pystray Pillow
update-desktop-database /usr/share/applications/ 2>/dev/null || true
gtk-update-icon-cache -f /usr/share/icons/hicolor/ 2>/dev/null || true

%preun
rm -rf /opt/portkiller/.venv

%files
%dir /opt/portkiller
/opt/portkiller/*
/usr/bin/portkiller
/usr/share/applications/com.kaleabcodes.portkiller.desktop
/usr/share/icons/hicolor/scalable/apps/com.kaleabcodes.portkiller.svg

%changelog
