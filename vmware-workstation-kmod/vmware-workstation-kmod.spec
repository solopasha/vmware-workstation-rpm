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
%global commit   5389d2915b66da4d614d9134411a72099ef0e1ab
%forgemeta

Name:          vmware-workstation-kmod
Version:       16.2.4
# Taken over by kmodtool
Release:       2%{?dist}
Summary:       VMware kernel modules
License:       GPLv2
URL:           %{forgeurl}

Source0:       %{forgesource}

# needed for plague to make sure it builds for i586 and i686
ExclusiveArch:  x86_64

# get the needed BuildRequires (in parts depending on what we build for)
BuildRequires:  %{_bindir}/kmodtool

%{!?kernels:BuildRequires: gcc, elfutils-libelf-devel, buildsys-build-rpmfusion-kerneldevpkgs-%{?buildforkernels:%{buildforkernels}}%{!?buildforkernels:current}-%{_target_cpu} }
# kmodtool does its magic here
%{expand:%(kmodtool --target %{_target_cpu} --repo rpmfusion --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null) }

%description
The VMware %{version} driver kernel modules for kernel %{kversion}.

%prep
# error out if there was something wrong with kmodtool
%{?kmodtool_check}
# print kmodtool output for debugging purposes:
kmodtool --target %{_target_cpu} --repo rpmfusion --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null
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
* Tue Sep 06 2022 solopasha <pasha@solopasha.ru> - 16.2.4-1
- Initial packaging
