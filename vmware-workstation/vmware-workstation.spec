%global debug_package %{nil}
%global _build_id_links none
%global __brp_check_rpaths %{nil}
%global buildver 23298084
%global pkgver %(echo %{version}_%{buildver})
%global __provides_exclude_from ^(%{_libdir}/vmware/(lib|libconf)/.*\\.so.*|%{_libdir}/vmware-installer/.*|%{_libdir}/vmware-ovftool/.*|%{_libdir}/vmware-vix/.*)$
%global __requires_exclude ^libffi|libpython3.10|libvim-types|libcroco-0.6|libbasichttp|libcds|libcrypto|libexpat|libgoogleurl|libgvmomi|libicudata|libicuuc|libssl|libssoclient|libvmacore|libvmomi|libvmwarebase|libvmwareui|libvnetlib|libbz2|libgdbm|libgdbm_compat.*$


Name:          vmware-workstation
Version:       17.5.1
Release:       1%{?dist}
Summary:       The industry standard for running multiple operating systems as virtual machines on a single Linux PC

License:       Proprietary
URL:           https://www.vmware.com/products/workstation-for-linux.html
Source0:       https://download3.vmware.com/software/WKST-%(echo %{version} | sed 's/\.//g')-LX/VMware-Workstation-Full-%{version}-%{buildver}.x86_64.bundle
Source1:       vmware-networks.service
Source2:       vmware-networks-configuration.service
Source3:       vmware-usbarbitrator.service
Source4:       vmware-networks.path
Source5:       vmware-usbarbitrator.path
Source6:       vmware-vix-bootstrap
Source7:       vmware-environment.sh
Source8:       configure-initscript.sh
Source9:       config
Source10:      vmware-bootstrap

BuildRequires: sqlite
BuildRequires: grep
BuildRequires: systemd-rpm-macros
BuildRequires: desktop-file-utils
BuildRequires: chrpath

Requires:      hicolor-icon-theme
Requires:      %{name}-kmod >= %{version}
Provides:      %{name}-kmod-common = %{version}-%{release}

ExclusiveArch: x86_64

%description
%{summary}.

%prep
%setup -T -c
extracted_dir="%{_builddir}/extracted"

bash %{SOURCE0} --extract "$extracted_dir"

%build

%install
_isoimages=(linux linuxPreGlibc25 netware solaris windows winPre2k winPreVista)
_isovirtualprinterimages=(Linux Windows)
vmware_installer_version=$(cat "%{_builddir}/extracted/vmware-installer/manifest.xml" | grep -oPm1 "(?<=<version>)[^<]+")
mkdir -p \
    "%{buildroot}/etc"/{modprobe.d,vmware} \
    "%{buildroot}/usr"/{share,bin} \
    "%{buildroot}/usr/include/vmware-vix" \
    "%{buildroot}/usr/lib64"/{vmware/setup,vmware-vix,vmware-ovftool,vmware-installer/"$vmware_installer_version"} \
    "%{buildroot}/usr/lib/modules-load.d" \
    "%{buildroot}/usr/share"/{doc/vmware-vix,licenses/"%{name}"} \
    "%{buildroot}/var/lib/vmware/Shared VMs"
cd "%{_builddir}/extracted"
cp -r \
    vmware-workstation/share/* \
    vmware-workstation/man \
    vmware-network-editor-ui/share/* \
    vmware-player-app/share/* \
    "%{buildroot}/usr/share"

cp -r \
    vmware-workstation/bin/* \
    vmware-vmx/{,s}bin/* \
    vmware-vix-core/bin/* \
    vmware-vprobe/bin/* \
    vmware-player-app/bin/* \
    "%{buildroot}/usr/bin"

cp -r \
    vmware-workstation/lib/* \
    vmware-player-app/lib/* \
    vmware-vmx/{lib/*,roms} \
    vmware-vprobe/lib/* \
    vmware-usbarbitrator/bin \
    vmware-network-editor/lib \
    "%{buildroot}/usr/lib64/vmware"

cp -r \
    vmware-player-setup/vmware-config \
    "%{buildroot}/usr/lib64/vmware/setup"

cp -r \
    vmware-vix-lib-Workstation1700/lib/Workstation-17.0.0 \
    vmware-vix-core/{lib/*,vixwrapper-config.txt} \
    "%{buildroot}/usr/lib64/vmware-vix"

cp -r \
    vmware-vix-core/doc/* \
    "%{buildroot}/usr/share/doc/vmware-vix"

chrpath -d vmware-ovftool/libcurl.so.4
cp -r \
    vmware-ovftool/* \
    "%{buildroot}/usr/lib64/vmware-ovftool"
cp -r \
    vmware-installer/{python,sopython,vmis,vmis-launcher,vmware-installer,vmware-installer.py} \
    "%{buildroot}/usr/lib64/vmware-installer/$vmware_installer_version"

cp -r \
    vmware-vix-core/include/* \
    "%{buildroot}/usr/include/vmware-vix"

for isoimage in ${_isoimages[@]}
do
    install -Dm 644 "vmware-tools-$isoimage/$isoimage.iso" "%{buildroot}/usr/lib64/vmware/isoimages/$isoimage.iso"
done

install -Dm 644 "vmware-workstation/doc/EULA" "%{buildroot}/usr/share/doc/vmware-workstation/EULA"
ln -s "/usr/share/doc/vmware-workstation/EULA" "%{buildroot}/usr/share/licenses/%{name}/VMware Workstation - EULA.txt"
ln -s "/usr/lib64/vmware-ovftool/vmware.eula" "%{buildroot}/usr/share/licenses/%{name}/VMware OVF Tool - EULA.txt"
install -Dm 644 "vmware-workstation/doc"/open_source_licenses.txt "%{buildroot}/usr/share/licenses/%{name}/VMware Workstation open source license.txt"
install -Dm 644 "vmware-workstation/doc"/ovftool_open_source_licenses.txt "%{buildroot}/usr/share/licenses/%{name}/VMware OVF Tool open source license.txt"
install -Dm 644 "vmware-vix-core"/open_source_licenses.txt "%{buildroot}/usr/share/licenses/%{name}/VMware VIX open source license.txt"
rm "%{buildroot}/usr/lib64/vmware-ovftool"/{vmware-eula.rtf,open_source_licenses.txt,manifest.xml}

install -d -m 755 "%{buildroot}/usr/lib64/vmware-installer/$vmware_installer_version"/{lib/lib,artwork}
install -Dm 755 "%{SOURCE8}" "%{buildroot}/usr/lib64/vmware-installer/$vmware_installer_version/bin/configure-initscript.sh"

install -Dm 644 "vmware-vmx/etc/modprobe.d/modprobe-vmware-fuse.conf" "%{buildroot}/etc/modprobe.d/vmware-fuse.conf"

install -Dm 644 vmware-vmx/extra/modules.xml "%{buildroot}"/usr/lib64/vmware/modules/modules.xml
install -Dm 644 vmware-installer/bootstrap "%{buildroot}"/etc/vmware-installer/bootstrap
install -Dm 644 %{SOURCE6} "%{buildroot}"/etc/vmware-vix/bootstrap
install -Dm 644 %{SOURCE10} "%{buildroot}"/etc/vmware/bootstrap
install -Dm 644 %{SOURCE9} "%{buildroot}"/etc/vmware/config

echo -e "vmw_vmci\nvmmon" > "%{buildroot}/usr/lib/modules-load.d/vmware.conf"
# systemd services
for service_file in %{SOURCE1} %{SOURCE2} %{SOURCE3} %{SOURCE4} %{SOURCE5}
do
    install -Dm 644 "$service_file" -t "%{buildroot}%{_unitdir}"
done

  # Apply permissions where necessary.

chmod +x \
"%{buildroot}/usr/bin"/* \
"%{buildroot}/usr/lib64/vmware/bin"/* \
"%{buildroot}/usr/lib64/vmware/setup"/* \
"%{buildroot}/usr/lib64/vmware/lib/libvmware-gksu.so/gksu-run-helper" \
"%{buildroot}/usr/lib64/vmware-ovftool"/{ovftool,ovftool.bin} \
"%{buildroot}/usr/lib64/vmware-installer/$vmware_installer_version"/{vmware-installer,vmis-launcher} \
"%{buildroot}/usr/lib64/vmware-vix/setup"/*

chmod +s \
"%{buildroot}/usr/bin"/vmware-authd \
"%{buildroot}/usr/lib64/vmware/bin"/{vmware-vmx,vmware-vmx-debug,vmware-vmx-stats}

# Add symlinks the installer would create.

for link in \
    licenseTool \
    vmplayer \
    vmware \
    vmware-app-control \
    vmware-enter-serial \
    vmware-fuseUI \
    vmware-gksu \
    vmware-modconfig \
    vmware-modconfig-console \
    vmware-mount \
    vmware-netcfg \
    vmware-setup-helper \
    vmware-tray \
    vmware-vmblock-fuse \
    vmware-vprobe \
    vmware-zenity
do
    ln -s /usr/lib64/vmware/bin/appLoader "%{buildroot}/usr/lib64/vmware/bin/$link"
done
for link in \
    vmrest
do
    ln -s /usr/lib64/vmware/bin/appLoader "%{buildroot}/usr/bin/$link"
done

for link in \
    vmware-fuseUI \
    vmware-mount \
    vmware-netcfg \
    vmware-usbarbitrator
do
    ln -s /usr/lib64/vmware/bin/$link "%{buildroot}/usr/bin/$link"
done

ln -s /usr/lib64/vmware/icu "%{buildroot}/etc/vmware/icu"
ln -s /usr/lib64/vmware-ovftool/ovftool "%{buildroot}/usr/bin/ovftool"
ln -s /usr/lib64/vmware-vix/libvixAllProducts.so "%{buildroot}/usr/lib64/libvixAllProducts.so"

mkdir -p %{buildroot}/usr/lib64/vmware/lib/libbz2.so.1.0
ln -s /usr/lib/libbz2.so %{buildroot}/usr/lib64/vmware/lib/libbz2.so.1.0

rm -rf %{buildroot}/usr/lib64/vmware/modules/source

  # Replace placeholder "variables" with real paths.

for file in \
    gtk-3.0/gdk-pixbuf.loaders
do
    sed -i 's,@@LIBCONF_DIR@@,/usr/lib64/vmware/libconf,g' "%{buildroot}/usr/lib64/vmware/libconf/etc/$file"
done

sed -i 's,@@BINARY@@,/usr/bin/vmware,' "%{buildroot}/usr/share/applications/vmware-workstation.desktop"
sed -i 's,@@BINARY@@,/usr/bin/vmplayer,' "%{buildroot}/usr/share/applications/vmware-player.desktop"
sed -i 's,@@BINARY@@,/usr/bin/vmware-netcfg,' "%{buildroot}/usr/share/applications/vmware-netcfg.desktop"

sed \
    -e "s/@@VERSION@@/$vmware_installer_version/" \
    -e "s,@@VMWARE_INSTALLER@@,/usr/lib64/vmware-installer/$vmware_installer_version," \
    -i "%{buildroot}/etc/vmware-installer/bootstrap"

# Create a database which contains the list of guest tools (necessary to avoid that vmware try to download them)
database_filename="%{buildroot}/etc/vmware-installer/database"
echo -n "" > "$database_filename"

sqlite3 "$database_filename" "CREATE TABLE settings(key VARCHAR PRIMARY KEY, value VARCHAR NOT NULL, component_name VARCHAR NOT NULL);"
sqlite3 "$database_filename" "INSERT INTO settings(key,value,component_name) VALUES('db.schemaVersion','2','vmware-installer');"
sqlite3 "$database_filename" "CREATE TABLE components(id INTEGER PRIMARY KEY, name VARCHAR NOT NULL, version VARCHAR NOT NULL, buildNumber INTEGER NOT NULL, component_core_id INTEGER NOT NULL, longName VARCHAR NOT NULL, description VARCHAR, type INTEGER NOT NULL);"

for isoimage in ${_isoimages[@]}
do
    version=$(cat "%{_builddir}/extracted/vmware-tools-$isoimage/manifest.xml" | grep -oPm1 "(?<=<version>)[^<]+")
    sqlite3 "$database_filename" "INSERT INTO components(name,version,buildNumber,component_core_id,longName,description,type) VALUES('vmware-tools-$isoimage','$version','%{buildver}',1,'$isoimage','$isoimage',1);"
done

# Define some environment variables for VMware and remove the tests about kernel modules
install -Dm 644 "%{SOURCE7}" "%{buildroot}/etc/conf.d/vmware"
for program in vmware vmplayer vmware-tray; do
    sed -e '/export PRODUCT_NAME/asource /etc/conf.d/vmware' \
        -e 's/if "$BINDIR"\/vmware-modconfig --appname=.*/if true ||/' \
        -i "%{buildroot}/usr/bin/$program"
done

# Add StartupWMClass attribute to desktop files
sed -i '/^StartupNotify=.*/a StartupWMClass=vmware' "%{buildroot}/usr/share/applications/vmware-workstation.desktop"
sed -i '/^StartupNotify=.*/a StartupWMClass=vmplayer' "%{buildroot}/usr/share/applications/vmware-player.desktop"
sed -i '/^StartupNotify=.*/a StartupWMClass=vmware-netcfg' "%{buildroot}/usr/share/applications/vmware-netcfg.desktop"

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/vmware*.desktop

%files
%license /usr/share/licenses/%{name}/*
%doc /usr/share/doc/*
%dir "%{_sharedstatedir}/vmware/Shared VMs/"
%dir %{_sysconfdir}/vmware-vix
%{_sysconfdir}/vmware-vix/bootstrap
%dir %{_sysconfdir}/vmware-installer
%{_sysconfdir}/vmware-installer/*
%dir %{_sysconfdir}/vmware
%{_sysconfdir}/vmware/bootstrap
%{_sysconfdir}/vmware/icu
%{_sysconfdir}/modprobe.d/*
%{_bindir}/ovftool
%{_bindir}/vm*
%{_datadir}/appdata/vmware*.appdata.xml
%{_datadir}/applications/vmware-*
%{_datadir}/icons/hicolor/*
%{_datadir}/mime/packages/vmware*
%{_includedir}/vmware-vix/
%{_libdir}/libvixAllProducts.so
%{_libdir}/vmware-installer/
%{_libdir}/vmware-ovftool/
%{_libdir}/vmware-vix/
%{_libdir}/vmware/
%{_mandir}/man1/vmware.1.*
%{_prefix}/lib/modules-load.d/vmware.conf
%{_unitdir}/vmware*.service
%{_unitdir}/vmware*.path
%config(noreplace) %{_sysconfdir}/vmware/config
%config(noreplace) %{_sysconfdir}/conf.d/vmware

%post
%systemd_post vmware-networks.service vmware-networks-configuration.service vmware-usbarbitrator.service vmware-networks.path vmware-usbarbitrator.path

%preun
%systemd_preun vmware-networks.service vmware-networks-configuration.service vmware-usbarbitrator.service vmware-networks.path vmware-usbarbitrator.path

%postun
%systemd_postun vmware-networks.service vmware-networks-configuration.service vmware-usbarbitrator.service vmware-networks.path vmware-usbarbitrator.path

%changelog
* Sun Apr 07 2024 solopasha <daron439@gmail.com> - 17.5.1-1
- Update to 17.5.1

* Tue Sep 06 2022 solopasha <daron439@gmail.com> - 16.2.4-1
- Initial packaging
