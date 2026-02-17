#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeplasmaver	6.6.0
%define		qtver		6.10.0
%define		kpname		plasma-setup

Summary:	Plasma Setup
Name:		kp6-%{kpname}
Version:	6.6.0
Release:	1
License:	LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/plasma/%{kdeplasmaver}/%{kpname}-%{version}.tar.xz
# Source0-md5:	b08f6455ba7b3ebdcef9b7cb12f2df11
URL:		http://www.kde.org/
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	Qt6Gui-devel >= %{qtver}
BuildRequires:	cmake >= 3.16.0
BuildRequires:	gettext-tools
BuildRequires:	kf6-extra-cmake-modules >= 6.22.0
BuildRequires:	kp6-libkscreen-devel
BuildRequires:	kp6-plasma-workspace-devel
BuildRequires:	ninja
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	xz
Requires(post,postun):	desktop-file-utils
%requires_eq_to Qt6Core Qt6Core-devel
Obsoletes:	kp5-%{kpname} < 6
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		qt6dir		%{_libdir}/qt6

%description
The Out-of-the-box (OOTB) experience that greets a user after system
installation or when starting up a new computer. Guides the user in
creating the system's first user account and configuring initial
settings.

%prep
%setup -q -n %{kpname}-%{version}

%build
%cmake -B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	-DKDE_INSTALL_DOCBUNDLEDIR=%{_kdedocdir}
%ninja_build -C build

%if %{with tests}
ctest
%endif

%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%find_lang %{kpname} --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
%update_desktop_database_post

%postun
/sbin/ldconfig
%update_desktop_database_postun

%files -f %{kpname}.lang
%defattr(644,root,root,755)
/etc/xdg/plasmasetuprc
%{_prefix}%{systemdunitdir}/plasma-setup.service
%{_prefix}/lib/sysusers.d/plasma-setup-sysuser.conf
%{systemdtmpfilesdir}/plasma-setup-tmpfiles.conf
%{_libdir}/libcomponentspluginplugin.a
%{_libdir}/qt6/plugins/kf6/packagestructure/plasmasetup.so
%{_libdir}/qt6/qml/org/kde/plasmasetup
%attr(755,root,root) %{_prefix}/libexec/kf6/kauth/plasma-setup-auth-helper
%attr(755,root,root) %{_prefix}/libexec/plasma-setup
%attr(755,root,root) %{_prefix}/libexec/plasma-setup-bootutil
%{_datadir}/dbus-1/system-services/org.kde.plasmasetup.service
%{_datadir}/dbus-1/system.d/org.kde.plasmasetup.conf
%{_datadir}/metainfo/org.kde.plasmasetup.keyboard.appdata.xml
%{_datadir}/plasma-setup/kglobalaccelrc
%{_datadir}/plasma-setup/plasma-setup.desktop
%{_datadir}/plasma/packages/org.kde.plasmasetup.account
%{_datadir}/plasma/packages/org.kde.plasmasetup.finished
%{_datadir}/plasma/packages/org.kde.plasmasetup.hostname
%{_datadir}/plasma/packages/org.kde.plasmasetup.keyboard
%{_datadir}/plasma/packages/org.kde.plasmasetup.language
%{_datadir}/plasma/packages/org.kde.plasmasetup.prepare
%{_datadir}/plasma/packages/org.kde.plasmasetup.time
%{_datadir}/plasma/packages/org.kde.plasmasetup.wifi
%{_datadir}/polkit-1/actions/org.kde.plasmasetup.policy
%{_datadir}/polkit-1/rules.d/plasma-setup-polkit.rules
%{_datadir}/qlogging-categories6/plasmasetup.categories
