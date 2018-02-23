Name:		apper
Summary:	KDE PackageKit Interface
Group:		System/Configuration/Packaging
Version:	1.0.0
Release:	1
License:	GPLv2+
URL:		http://www.opendesktop.org/content/show.php/Apper?content=84745
Source0:	http://download.kde.org/stable/apper/%{version}/src/%{name}-%{version}.tar.xz
BuildRequires:	desktop-file-utils
BuildRequires:	chrpath
BuildRequires:	gettext
BuildRequires:	cmake(KDED)
BuildRequires:	cmake(KF5Config)
BuildRequires:	cmake(KF5DocTools)
BuildRequires:	cmake(KF5GuiAddons)
BuildRequires:	cmake(KF5I18n)
BuildRequires:	cmake(KF5KCMUtils)
BuildRequires:	cmake(KF5DBusAddons)
BuildRequires:	cmake(KF5KIO)
BuildRequires:	cmake(KF5Notifications)
BuildRequires:	cmake(KF5KDELibs4Support)
BuildRequires:	cmake(LibKWorkspace)
BuildRequires:	cmake(Qt5Quick)
BuildRequires:	cmake(Qt5Sql)
BuildRequires:	cmake(Qt5Widgets)
BuildRequires:	cmake(Qt5XmlPatterns)
BuildRequires:	cmake(ecm)
BuildRequires:	qt5-macros
BuildRequires:	pkgconfig(dbus-1)
BuildRequires:	pkgconfig(packagekitqt5)

Requires:	packagekit >= 0.6.17
Provides:	packagekit-gui = %{version}-%{release}

%description
KDE interface for PackageKit.

%files
%doc TODO
%license COPYING
%{_kf5_bindir}/apper
%{_kf5_datadir}/apper/
%{_kf5_datadir}/applications/org.kde.apper.desktop
%{_kf5_datadir}/applications/org.kde.apper_installer.desktop
%{_kf5_datadir}/applications/org.kde.apper_settings.desktop
%{_kf5_datadir}/applications/org.kde.apper_updates.desktop
%{_kf5_libdir}/apper/
%{_qt5_importdir}/org/kde/apper/
%{_libexecdir}/apper-pk-session
%{_datadir}/dbus-1/services/kde-org.freedesktop.PackageKit.service
%{_qt5_plugindir}/kcm_apper.so
%{_kf5_datadir}/kservices5/kcm_apper.desktop
%{_qt5_plugindir}/kded_apperd.so
%{_kf5_datadir}/kservices5/kded/apperd.desktop
%{_kf5_datadir}/apperd/
%{_mandir}/man1/apper.1*
%{_datadir}/appdata/org.kde.apper.appdata.xml

#--------------------------------------------------------------------

%if %{with applet}
%package updater
Summary:	Plasma updater applet for Apper
Group:		System/Packaging
Requires:	%{name} = %{version}-%{release}

%description updater
This package provides the Plasma applet for Apper.

%files updater
%{_kf5_datadir}/kservices5/plasma-applet-org.packagekit.updater.desktop
%{_kf5_datadir}/plasma/plasmoids/org.packagekit.updater/
%endif
#--------------------------------------------------------------------

%prep
%autosetup -p1

# disable update applet by default
sed -i \
  -e 's|X-KDE-PluginInfo-EnabledByDefault=.*|X-KDE-PluginInfo-EnabledByDefault=false|g' \
    plasmoid/package/metadata.desktop

%build
# PackageKit-Dnf doesn't yet support autoremove from frontends
%cmake_kf5 -DAUTOREMOVE:BOOL=OFF
%make_build

%install
%make_install -C build

desktop-file-install \
		     --dir %{buildroot}%{_kf5_datadir}/applications \
		     --remove-mime-type='application/x-deb' \
		     %{buildroot}%{_kf5_datadir}/applications/*.desktop

# hack around rpath oddness
chrpath --list %{buildroot}%{_kf5_bindir}/apper
chrpath --replace %{_kf5_libdir}/apper %{buildroot}%{_kf5_bindir}/apper

# hack around gnome-packagekit conflict
# (cg) Note that this is a rubbish hack: While the files names may no longer
# conflict they are still trying to bus-activate the same service. This can
# never work properly when you have both installed anyway, so it's probably
# better to have the packages conflict IMO.
mv %{buildroot}%{_datadir}/dbus-1/services/org.freedesktop.PackageKit.service \
  %{buildroot}%{_datadir}/dbus-1/services/kde-org.freedesktop.PackageKit.service

%if ! %{with applet}
# Remove applet files
rm -fv %{buildroot}%{_kf5_datadir}/kservices5/plasma-applet-org.packagekit.updater.desktop
rm -rfv %{buildroot}%{_kf5_datadir}/plasma/plasmoids/org.packagekit.updater
%endif


