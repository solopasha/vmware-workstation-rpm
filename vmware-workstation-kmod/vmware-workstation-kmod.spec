# buildforkernels macro hint: when you build a new version or a new release
# that contains bugfixes or other improvements then you must disable the
# "buildforkernels newest" macro for just that build; immediately after
# queuing that build enable the macro again for subsequent builds; that way
# a new akmod package will only get build when a new one is actually needed
%if 0%{?fedora}
%global buildforkernels akmod
%global debug_package %{nil}
%endif

%global forgeurl https://github.com/mkubecek/vmware-host-modules
%global commit 2c6d66f3f1947384038b765c897b102ecdb18298

Name:          vmware-workstation-kmod
Version:       17.5.1
Release:       1%{?dist}
Summary:       VMware kernel modules

%forgemeta

License:       GPLv2
URL:           %{forgeurl}
Source:        %{forgesource}

BuildRequires:  kmodtool

# kmodtool does its magic here
%{expand:%(kmodtool --target %{_target_cpu} --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null) }

%description
The VMware %{version} driver kernel modules for kernel %{kversion}.

%prep
# error out if there was something wrong with kmodtool
%{?kmodtool_check}
# print kmodtool output for debugging purposes:
kmodtool --target %{_target_cpu} --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null
%forgesetup

for kernel_version  in %{?kernel_versions} ; do
    mkdir _kmod_build_${kernel_version%%___*}
    cp -a vmmon-only _kmod_build_${kernel_version%%___*}/vmmon-only
    cp -a vmnet-only _kmod_build_${kernel_version%%___*}/vmnet-only
done

%build
for kernel_version in %{?kernel_versions} ; do
    for modules in vmmon-only vmnet-only ; do
        ls "${PWD}/_kmod_build_${kernel_version%%___*}"
        make V=1 -C "${kernel_version##*___}" M="${PWD}/_kmod_build_${kernel_version%%___*}/${modules}" SRCROOT="${PWD}/_kmod_build_${kernel_version%%___*}/${modules}" VM_UNAME=${kernel_version%%___*} HEADER_DIR="${kernel_version##*___}/include" modules
    done
done

%install
for kernel_version in %{?kernel_versions}; do
    mkdir -p  $RPM_BUILD_ROOT/%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/
    install -D -m 0755 $(find _kmod_build_${kernel_version%%___*} -name "*.ko") \
         $RPM_BUILD_ROOT/%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/
done
%{?akmod_install}

%changelog
* Sun Apr 07 2024 solopasha <daron439@gmail.com> - 17.5.1-1
- Update to 17.5.1

* Tue Sep 06 2022 solopasha <daron439@gmail.com> - 16.2.4-1
- Initial packaging
