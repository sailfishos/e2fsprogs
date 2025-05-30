%define	_root_sbindir	/sbin

Summary: Utilities for managing ext2, ext3, and ext4 filesystems
Name: e2fsprogs
Version: 1.47.2
Release: 1
# License tags based on COPYING file distinctions for various components
License: GPLv2
Source0: %{name}-%{version}.tar.xz
Source1: ext2_types-wrapper.h
Patch1: 0001-Fix-build-of-tests-using-diff-from-busybox.patch
Patch2: 0002-Revert-enabling-metadata_csum-metadata_csum_seed-and.patch

Url: https://github.com/sailfishos/e2fsprogs
BuildRequires: pkgconfig(blkid)
BuildRequires: pkgconfig(uuid)

%description
The e2fsprogs package contains a number of utilities for creating,
checking, modifying, and correcting any inconsistencies in second,
third and fourth extended (ext2/ext3/ext4) filesystems. E2fsprogs
contains e2fsck (used to repair filesystem inconsistencies after an
unclean shutdown), mke2fs (used to initialize a partition to contain
an empty ext2 filesystem), debugfs (used to examine the internal
structure of a filesystem, to manually repair a corrupted
filesystem, or to create test cases for e2fsck), tune2fs (used to
modify filesystem parameters), and most of the other core ext2fs
filesystem utilities.

You should install the e2fsprogs package if you need to manage the
performance of an ext2, ext3, or ext4 filesystem.

%package libs
Summary: Ext2/3/4 filesystem-specific shared libraries and headers
License: GPLv2 and LGPLv2
Requires(post): /sbin/ldconfig

%description libs
E2fsprogs-libs contains libe2p and libext2fs, the libraries of the
e2fsprogs package.

These libraries are used to directly acccess ext2/3/4 filesystems
from userspace.

%package devel
Summary: Ext2/3/4 filesystem-specific static libraries and headers
License: GPLv2 and LGPLv2
Requires: e2fsprogs-libs = %{version}-%{release}
Requires: gawk
Requires: libcom_err-devel

%description devel
E2fsprogs-devel contains the libraries and header files needed to
develop second, third and fourth extended (ext2/ext3/ext4)
filesystem-specific programs.

You should install e2fsprogs-devel if you want to develop ext2/3/4
filesystem-specific programs. If you install e2fsprogs-devel, you'll
also want to install e2fsprogs.

%package -n libcom_err
Summary: Common error description library
License: MIT

%description -n libcom_err
This is the common error description library, part of e2fsprogs.

libcom_err is an attempt to present a common error-handling mechanism.

%package -n libcom_err-devel
Summary: Common error description library
License: MIT
Requires: libcom_err = %{version}-%{release}
Requires: pkgconfig

%description -n libcom_err-devel
This is the common error description development library and headers,
part of e2fsprogs.  It contains the compile_et commmand, used
to convert a table listing error-code names and associated messages
messages into a C source file suitable for use with the library.

libcom_err is an attempt to present a common error-handling mechanism.

%package -n libss
Summary: Command line interface parsing library
License: MIT

%description -n libss
This is libss, a command line interface parsing library, part of e2fsprogs.

This package includes a tool that parses a command table to generate
a simple command-line interface parser, the include files needed to
compile and use it, and the static libs.

It was originally inspired by the Multics SubSystem library.

%package -n libss-devel
Summary: Command line interface parsing library
License: MIT
Requires: libss = %{version}-%{release}
Requires: pkgconfig

%description -n libss-devel
This is the command line interface parsing (libss) development library
and headers, part of e2fsprogs.  It contains the mk_cmds command, which
parses a command table to generate a simple command-line interface parser.

It was originally inspired by the Multics SubSystem library.

%package doc
Summary:   Documentation for %{name}
Requires:  %{name} = %{version}-%{release}

%description doc
Man and info pages for %{name}.

%prep
%autosetup -p1 -n %{name}-%{version}/%{name}

%build
%configure --enable-elf-shlibs --enable-nls --disable-uuidd --disable-fsck \
           --disable-e2initrd-helper --disable-libblkid --disable-libuuid \
           --disable-fuse2fs --with-udev-rules-dir=no --with-crond-dir=no \
           --with-systemd-unit-dir=no
# Remove the m_hugefile test as it fails when built on tmpfs workers
rm -f tests/m_hugefile/script
%make_build

%install
export PATH=/sbin:$PATH
%make_install install-libs \
      root_sbindir=%{_root_sbindir} root_libdir=%{_libdir}

# ugly hack to allow parallel install of 32-bit and 64-bit -devel packages:
%define multilib_arches %{ix86} x86_64

%ifarch %{multilib_arches}
mv -f $RPM_BUILD_ROOT%{_includedir}/ext2fs/ext2_types.h \
      $RPM_BUILD_ROOT%{_includedir}/ext2fs/ext2_types-%{_arch}.h
install -p -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_includedir}/ext2fs/ext2_types.h
%endif

mkdir -p $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
install -m0644 -t $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version} \
        README

%find_lang %{name}

chmod -R u+w $RPM_BUILD_ROOT/*

%check
# Tests are not run on OBS:
%if ! 0%{?qemu_user_space_build}
# One test currently does not pass because it requires a newer version of dd 
# from a post-GPLv3 version.
make check
%endif

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%post -n libcom_err -p /sbin/ldconfig
%postun -n libcom_err -p /sbin/ldconfig

%post -n libss -p /sbin/ldconfig
%postun -n libss -p /sbin/ldconfig

%lang_package


%files 
%license NOTICE

%config /etc/mke2fs.conf
%config /etc/e2scrub.conf
%{_root_sbindir}/badblocks
%{_root_sbindir}/debugfs
%{_root_sbindir}/dumpe2fs
%{_root_sbindir}/e2fsck
%{_root_sbindir}/e2image
%{_root_sbindir}/e2label
%{_root_sbindir}/e2mmpstatus
%{_root_sbindir}/e2scrub
%{_root_sbindir}/e2scrub_all
%{_root_sbindir}/e2undo
%{_root_sbindir}/fsck.ext2
%{_root_sbindir}/fsck.ext3
%{_root_sbindir}/fsck.ext4
%{_root_sbindir}/logsave
%{_root_sbindir}/mke2fs
%{_root_sbindir}/mkfs.ext2
%{_root_sbindir}/mkfs.ext3
%{_root_sbindir}/mkfs.ext4
%{_root_sbindir}/resize2fs
%{_root_sbindir}/tune2fs

%{_sbindir}/filefrag
%{_sbindir}/e2freefrag
%{_sbindir}/e4defrag
%{_sbindir}/e4crypt
%{_sbindir}/mklost+found

%{_bindir}/chattr
%{_bindir}/lsattr

%files libs
%license NOTICE
%{_libdir}/libe2p.so.*
%{_libdir}/libext2fs.so.*

%files devel
%{_libdir}/libe2p.a
%{_libdir}/libe2p.so
%{_libdir}/libext2fs.a
%{_libdir}/libext2fs.so
%{_libdir}/pkgconfig/e2p.pc
%{_libdir}/pkgconfig/ext2fs.pc

%{_includedir}/e2p
%{_includedir}/ext2fs

%files -n libcom_err
%{_libdir}/libcom_err.so.*

%files -n libcom_err-devel
%{_bindir}/compile_et
%{_libdir}/libcom_err.a
%{_libdir}/libcom_err.so
%{_datadir}/et
%{_includedir}/et
%{_includedir}/com_err.h
%{_libdir}/pkgconfig/com_err.pc

%files -n libss
%license NOTICE
%{_libdir}/libss.so.*

%files -n libss-devel
%{_bindir}/mk_cmds
%{_libdir}/libss.a
%{_libdir}/libss.so
%{_datadir}/ss
%{_includedir}/ss
%{_libdir}/pkgconfig/ss.pc

%files doc
%{_mandir}/man*/*.*
%{_docdir}/%{name}-%{version}
