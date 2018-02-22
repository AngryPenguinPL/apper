Name:		apper
Summary:	KDE PackageKit Interface
Group:		System/Configuration/Packaging
Version:	1.0.0
Release:	1
License:	GPLv2+
URL:		http://www.opendesktop.org/content/show.php/Apper?content=84745
Source0:	http://download.kde.org/stable/apper/%{version}/src/%{name}-%{version}.tar.xz
BuildRequires:	desktop-file-utils
BuildRequires:	kdelibs4-devel
BuildRequires:	kdebase4-workspace-devel
BuildRequires:	qt4-qtdbus
BuildRequires:	packagekit-qt-devel >= 0.9.0
Requires:	packagekit >= 0.6.17
Provides:	packagekit-gui = %{version}-%{release}
%rename		kpackagekit
%rename		kpackagekit-common

%description
KDE interface for PackageKit.

%files -f %{name}.lang
%{_datadir}/dbus-1/services/*.service
%{_kde_bindir}/apper
%{_kde_libdir}/kde4/*apper*.so
%{_kde_libdir}/kde4/imports/org/kde/apper
%{_kde_libdir}/apper/libapper.so
%{_kde_appsdir}/?pper*/
%{_kde_appsdir}/plasma/plasmoids/org.packagekit.updater
%{_kde_libdir}/kde4/libexec/apper-pk-session
%{_kde_applicationsdir}/apper*.desktop
%{_kde_services}/kcm_apper.desktop
%{_kde_services}/kded/apperd.desktop
%{_kde_services}/plasma-applet-org.packagekit.updater.desktop
%{_kde_mandir}/man1/apper.1.*
%{_datadir}/appdata/%{name}.appdata.xml
#--------------------------------------------------------------------
%prep
%setup -q
%apply_patches

%build
%cmake_kde4 -DAUTOREMOVE:BOOL=OFF -DCMAKE_SKIP_RPATH:BOOL=OFF
%make

%install
%makeinstall_std -C build

desktop-file-install --vendor='' \
	--dir %{buildroot}%{_kde_datadir}/applications/kde4 \
	--remove-category='System' \
	--add-category='Settings' \
	--remove-mime-type='application/x-deb' \
	%{buildroot}%{_kde_datadir}/applications/kde4/*.desktop

%find_lang %{name} --all-name

%check
for file in apper apper_installer; do
  desktop-file-validate %{buildroot}%{_kde_datadir}/applications/kde4/$file.desktop
done

