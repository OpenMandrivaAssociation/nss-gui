Summary:	GUI to manage contents of an NSS database
Name:		nss-gui
Version:	0.3.3
Release:	%mkrel 1
License:	MPLv1.1 or GPLv2+ or LGPLv2+
Group:		File tools
URL:		https://fedorahosted.org/nss-gui/
Source0:	https://fedorahosted.org/released/nss-gui/%{name}-%{version}.tar.bz2
Source1:	nss-16x16.png
Source2:	nss-32x32.png
Source3:	nss-48x48.png
Requires:	xulrunner
BuildRequires:	boost-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Graphical user interface to manage the content of an NSS (Network Security
Services) database, including registered CRLs and registered security devices
(PKCS#11). Based on Mozilla code.

%prep
%setup -q

cp %{SOURCE1} nss-16x16.png
cp %{SOURCE2} nss-32x32.png
cp %{SOURCE3} nss-48x48.png

%build
cd wrapnssgui
g++ %{optflags} wrapnssgui.cpp -o wrapnssgui %{ldflags} -lboost_program_options
cd ..

%install
rm -rf %{buildroot}

install -d %{buildroot}/%{_bindir}
install -d %{buildroot}/%{_datadir}/nss-gui
install -m0755 wrapnssgui/wrapnssgui %{buildroot}/%{_bindir}/nss-gui
cp -axiv xrnssgui/* %{buildroot}/%{_datadir}/nss-gui

install -d %{buildroot}%{_datadir}/applications
rm -f %{buildroot}%{_datadir}/applications/MySQLWorkbench.desktop
cat > %{buildroot}%{_datadir}/applications/mysql-workbench-oss.desktop << EOF
[Desktop Entry]
Name=NSS GUI
Comment=GUI to manage contents of an NSS database
Exec=%{_bindir}/nss-gui
Terminal=false
Type=Application
Icon=nss-gui
Categories=System;X-MandrivaLinux-MoreApplications-Databases;
EOF

install -d %{buildroot}%{_miconsdir}
install -d %{buildroot}%{_iconsdir}
install -d %{buildroot}%{_liconsdir}
install -m0644 nss-16x16.png %{buildroot}%{_miconsdir}/nss-gui.png
install -m0644 nss-32x32.png %{buildroot}%{_iconsdir}/nss-gui.png
install -m0644 nss-48x48.png %{buildroot}%{_liconsdir}/nss-gui.png

%if %mdkversion < 200900
%post
%update_menus
%endif

%if %mdkversion < 200900
%postun
%clean_menus
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_bindir}/nss-gui
%{_datadir}/nss-gui/xrnssgui.ini
%{_datadir}/nss-gui/defaults/preferences/prefs.js
%{_datadir}/nss-gui/chrome/chrome.manifest
%{_datadir}/nss-gui/chrome/branding/brand.properties
%{_datadir}/nss-gui/chrome/branding/brand.dtd
%{_datadir}/nss-gui/chrome/content/WebSitesModifyOverlay.xul
%{_datadir}/nss-gui/chrome/content/main.xul
%{_datadir}/nss-gui/chrome/content/crlManagerModify.xul
%{_datadir}/nss-gui/chrome/content/main.js
%attr(0644,root,root) %{_datadir}/applications/*.desktop
%attr(0644,root,root) %{_iconsdir}/*.png
%attr(0644,root,root) %{_liconsdir}/*.png
%attr(0644,root,root) %{_miconsdir}/*.png

