%define kmod_name		ahci
%define kmod_vendor		redhat
%define kmod_rpm_name		kmod-redhat-ahci
%define kmod_driver_version	3.0_dup8.8
%define kmod_driver_epoch	%{nil}
%define kmod_rpm_release	1
%define kmod_kernel_version	4.18.0-477.10.1.el8_8
%define kmod_kernel_version_min	4.18.0-477
%define kmod_kernel_version_dep	4.18.0-477.el8
%define kmod_kbuild_dir		drivers/ata
%define kmod_dependencies       %{nil}
%define kmod_dist_build_deps	%{nil}
%define kmod_build_dependencies	%{nil}
%define kmod_provides           %{nil}
%define kmod_devel_package	1
%define kmod_devel_src_paths	include/linux/pci_ids.h
%define kmod_install_path	extra/kmod-redhat-ahci
%define kmod_files_package	0
%define kmod_files_noarch	1
%define kernel_pkg		kernel
%define kernel_devel_pkg	kernel-devel
%define kernel_modules_pkg	kernel-modules

%{!?dist: %define dist .el8_8}
%{!?make_build: %define make_build make}

%if "%{kmod_kernel_version_dep}" == ""
%define kmod_kernel_version_dep %{kmod_kernel_version}
%endif

%if "%{kmod_dist_build_deps}" == ""
%if (0%{?rhel} > 8) || (0%{?centos} > 8)
%define abi_list stablelist
%define kmod_dist_build_deps redhat-rpm-config kernel-abi-stablelists elfutils-libelf-devel kernel-rpm-macros kmod
%else
%if (0%{?rhel} > 7) || (0%{?centos} > 7)
%define abi_list whitelist
%define kmod_dist_build_deps redhat-rpm-config kernel-abi-whitelists elfutils-libelf-devel kernel-rpm-macros kmod
%else
%define abi_list whitelist
%define kmod_dist_build_deps redhat-rpm-config kernel-abi-whitelists
%endif
%endif
%endif

Source0:	%{kmod_name}-%{kmod_vendor}-%{kmod_driver_version}.tar.bz2
# Source code patches
Patch0:	0001-ahci-Add-support-for-Dell-S140-and-later-controllers.patch
Patch1:	9000-add-Makefile.patch
Patch2:	9001-rename-kmod.patch
Patch3:	9002-bump-version.patch
Patch4:	9003-trim-unused-parts.patch

%define findpat %( echo "%""P" )
%define __find_requires /usr/lib/rpm/redhat/find-requires.ksyms
%define __find_provides /usr/lib/rpm/redhat/find-provides.ksyms %{kmod_name} %{?epoch:%{epoch}:}%{version}-%{release}
%define sbindir %( if [ -d "/sbin" -a \! -h "/sbin" ]; then echo "/sbin"; else echo %{_sbindir}; fi )
%define dup_state_dir %{_localstatedir}/lib/rpm-state/kmod-dups
%define kver_state_dir %{dup_state_dir}/kver
%define kver_state_file %{kver_state_dir}/%{kmod_kernel_version}.%(arch)
%define dup_module_list %{dup_state_dir}/rpm-kmod-%{kmod_name}-modules

Name:		kmod-redhat-ahci
Version:	%{kmod_driver_version}
Release:	%{kmod_rpm_release}%{?dist}
%if "%{kmod_driver_epoch}" != ""
Epoch:		%{kmod_driver_epoch}
%endif
Summary:	ahci kernel module for Driver Update Program
Group:		System/Kernel
License:	GPLv2
URL:		https://www.kernel.org/
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildRequires:	%kernel_devel_pkg = %kmod_kernel_version
%if "%{kmod_dist_build_deps}" != ""
BuildRequires:	%{kmod_dist_build_deps}
%endif
ExclusiveArch:	x86_64
%global kernel_source() /usr/src/kernels/%{kmod_kernel_version}.$(arch)

%global _use_internal_dependency_generator 0
%if "%{?kmod_kernel_version_min}" != ""
Provides:	%kernel_modules_pkg >= %{kmod_kernel_version_min}.%{_target_cpu}
%else
Provides:	%kernel_modules_pkg = %{kmod_kernel_version_dep}.%{_target_cpu}
%endif
Provides:	kmod-%{kmod_name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires(post):	%{sbindir}/weak-modules
Requires(postun):	%{sbindir}/weak-modules
Requires:	kernel >= 4.18.0-477
%if 0
Requires: firmware(%{kmod_name}) = ENTER_FIRMWARE_VERSION
%endif
%if "%{kmod_build_dependencies}" != ""
BuildRequires:  %{kmod_build_dependencies}
%endif
%if "%{kmod_dependencies}" != ""
Requires:       %{kmod_dependencies}
%endif
%if "%{kmod_provides}" != ""
Provides:       %{kmod_provides}
%endif
# if there are multiple kmods for the same driver from different vendors,
# they should conflict with each other.
Conflicts:	kmod-%{kmod_name}

%description
ahci kernel module for Driver Update Program

%if 0

%package -n kmod-redhat-ahci-firmware
Version:	ENTER_FIRMWARE_VERSION
Summary:	ahci firmware for Driver Update Program
Provides:	firmware(%{kmod_name}) = ENTER_FIRMWARE_VERSION
%if "%{kmod_kernel_version_min}" != ""
Provides:	%kernel_modules_pkg >= %{kmod_kernel_version_min}.%{_target_cpu}
%else
Provides:	%kernel_modules_pkg = %{kmod_kernel_version_dep}.%{_target_cpu}
%endif
%description -n  kmod-redhat-ahci-firmware
ahci firmware for Driver Update Program


%files -n kmod-redhat-ahci-firmware
%defattr(644,root,root,755)
%{FIRMWARE_FILES}

%endif

# Development package
%if 0%{kmod_devel_package}
%package -n kmod-redhat-ahci-devel
Version:	%{kmod_driver_version}
Summary:	ahci development files for Driver Update Program

%description -n  kmod-redhat-ahci-devel
ahci development files for Driver Update Program


%files -n kmod-redhat-ahci-devel
%defattr(644,root,root,755)
/lib/modules/%{kmod_rpm_name}-%{kmod_driver_version}/
%endif

# Extra files package
%if 0%{kmod_files_package}
%package -n kmod-redhat-ahci-files
Version:	%{kmod_driver_version}
Summary:	ahci additional files for Driver Update Program
%if 0%{kmod_files_noarch}
BuildArch:	noarch
%endif
%if "%{?kmod_kernel_version_min}" != ""
Provides:	%kernel_modules_pkg >= %{kmod_kernel_version_min}.%{_target_cpu}
%else
Provides:	%kernel_modules_pkg = %{kmod_kernel_version_dep}.%{_target_cpu}
%endif

%description -n  kmod-redhat-ahci-files
ahci additional files for Driver Update Program


%files -n kmod-redhat-ahci-files
%defattr(644,root,root,755)


%endif

%post
modules=( $(find /lib/modules/%{kmod_kernel_version}.%(arch)/%{kmod_install_path} | grep '\.ko$') )
printf '%s\n' "${modules[@]}" | %{sbindir}/weak-modules --add-modules --no-initramfs

mkdir -p "%{kver_state_dir}"
touch "%{kver_state_file}"

exit 0

%posttrans
# We have to re-implement part of weak-modules here because it doesn't allow
# calling initramfs regeneration separately
if [ -f "%{kver_state_file}" ]; then
	kver_base="%{kmod_kernel_version_dep}"
	kvers=$(ls -d "/lib/modules/${kver_base%%.*}"*)

	for k_dir in $kvers; do
		k="${k_dir#/lib/modules/}"

		tmp_initramfs="/boot/initramfs-$k.tmp"
		dst_initramfs="/boot/initramfs-$k.img"

		# The same check as in weak-modules: we assume that the kernel present
		# if the symvers file exists.
		if [ -e "/boot/symvers-$k.gz" ] || [ -e "$k_dir/symvers.gz" ]; then
			/usr/bin/dracut -f "$tmp_initramfs" "$k" || exit 1
			cmp -s "$tmp_initramfs" "$dst_initramfs"
			if [ "$?" = 1 ]; then
				mv "$tmp_initramfs" "$dst_initramfs"
			else
				rm -f "$tmp_initramfs"
			fi
		fi
	done

	rm -f "%{kver_state_file}"
	rmdir "%{kver_state_dir}" 2> /dev/null
fi

rmdir "%{dup_state_dir}" 2> /dev/null

exit 0

%preun
if rpm -q --filetriggers kmod 2> /dev/null| grep -q "Trigger for weak-modules call on kmod removal"; then
	mkdir -p "%{kver_state_dir}"
	touch "%{kver_state_file}"
fi

mkdir -p "%{dup_state_dir}"
rpm -ql kmod-redhat-ahci-%{kmod_driver_version}-%{kmod_rpm_release}%{?dist}.$(arch) | \
	grep '\.ko$' > "%{dup_module_list}"

%postun
if rpm -q --filetriggers kmod 2> /dev/null| grep -q "Trigger for weak-modules call on kmod removal"; then
	initramfs_opt="--no-initramfs"
else
	initramfs_opt=""
fi

modules=( $(cat "%{dup_module_list}") )
rm -f "%{dup_module_list}"
printf '%s\n' "${modules[@]}" | %{sbindir}/weak-modules --remove-modules $initramfs_opt

rmdir "%{dup_state_dir}" 2> /dev/null

exit 0

%files
%defattr(644,root,root,755)
/lib/modules/%{kmod_kernel_version}.%(arch)
/etc/depmod.d/%{kmod_name}.conf
%doc /usr/share/doc/%{kmod_rpm_name}/greylist.txt
%if !0%{kmod_files_package}


%endif

%prep
%setup -n %{kmod_name}-%{kmod_vendor}-%{kmod_driver_version}

%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
set -- *
mkdir source
mv "$@" source/
mkdir obj

%build
rm -rf obj
cp -r source obj

PWD_PATH="$PWD"
%if "%{workaround_no_pwd_rel_path}" != "1"
PWD_PATH=$(realpath --relative-to="%{kernel_source}" . 2>/dev/null || echo "$PWD")
%endif
%{make_build} -C %{kernel_source} V=1 M="$PWD_PATH/obj/%{kmod_kbuild_dir}" \
	NOSTDINC_FLAGS="-I$PWD_PATH/obj/include -I$PWD_PATH/obj/include/uapi %{nil}" \
	EXTRA_CFLAGS="%{nil}" \
	%{nil}
# mark modules executable so that strip-to-file can strip them
find obj/%{kmod_kbuild_dir} -name "*.ko" -type f -exec chmod u+x '{}' +

kabilist="/lib/modules/kabi-current/kabi_%{abi_list}_%{_target_cpu}"
for modules in $( find obj/%{kmod_kbuild_dir} -name "*.ko" -type f -printf "%{findpat}\n" | sed 's|\.ko$||' | sort -u ) ; do
	# update depmod.conf
	module_weak_path=$(echo "$modules" | sed 's/[\/]*[^\/]*$//')
	if [ -z "$module_weak_path" ]; then
		module_weak_path=%{name}
	else
		module_weak_path=%{name}/$module_weak_path
	fi
	echo "override $(echo $modules | sed 's/.*\///')" \
	     "$(echo "%{kmod_kernel_version_dep}" |
	        sed 's/\.[^\.]*$//;
		     s/\([.+?^$\/\\|()\[]\|\]\)/\\\0/g').*" \
		     "weak-updates/$module_weak_path" >> source/depmod.conf

	# update greylist
	nm -u obj/%{kmod_kbuild_dir}/$modules.ko | sed 's/.*U //' |  sed 's/^\.//' | sort -u | while read -r symbol; do
		grep -q "^\s*$symbol\$" $kabilist || echo "$symbol" >> source/greylist
	done
done
sort -u source/greylist | uniq > source/greylist.txt

%install
export INSTALL_MOD_PATH=$RPM_BUILD_ROOT
export INSTALL_MOD_DIR=%{kmod_install_path}
PWD_PATH="$PWD"
%if "%{workaround_no_pwd_rel_path}" != "1"
PWD_PATH=$(realpath --relative-to="%{kernel_source}" . 2>/dev/null || echo "$PWD")
%endif
make -C %{kernel_source} modules_install \
	M=$PWD_PATH/obj/%{kmod_kbuild_dir}
# Cleanup unnecessary kernel-generated module dependency files.
find $INSTALL_MOD_PATH/lib/modules -iname 'modules.*' -exec rm {} \;

install -m 644 -D source/depmod.conf $RPM_BUILD_ROOT/etc/depmod.d/%{kmod_name}.conf
install -m 644 -D source/greylist.txt $RPM_BUILD_ROOT/usr/share/doc/%{kmod_rpm_name}/greylist.txt
%if 0
%{FIRMWARE_FILES_INSTALL}
%endif
%if 0%{kmod_devel_package}
install -m 644 -D $PWD/obj/%{kmod_kbuild_dir}/Module.symvers $RPM_BUILD_ROOT/lib/modules/%{kmod_rpm_name}-%{kmod_driver_version}/build/Module.symvers

if [ -n "%{kmod_devel_src_paths}" ]; then
	for i in %{kmod_devel_src_paths}; do
		mkdir -p "$RPM_BUILD_ROOT/lib/modules/%{kmod_rpm_name}-%{kmod_driver_version}/build/$(dirname "$i")"
		cp -rv "$PWD/source/$i" \
			"$RPM_BUILD_ROOT/lib/modules/%{kmod_rpm_name}-%{kmod_driver_version}/build/$i"
	done
fi
%endif



%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Tue Sep 12 2023 Eugene Syromiatnikov <esyr@redhat.com> 3.0_dup8.8-1
- 4011c4649205bce50b42d290bba04f0504d928c2
- ahci kernel module for Driver Update Program
- Resolves: #bz2233801
