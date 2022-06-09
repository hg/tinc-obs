%define svc tinc@.service

Name:           tinc
Version:        1.1
Release:        0
Summary:        A virtual private network daemon
License:        GPL-2.0+
Group:          Productivity/Networking/Security
URL:            https://www.tinc-vpn.org/

Source0:        tinc-%{version}.tar

BuildRequires: meson
BuildRequires: texinfo
BuildRequires: pkgconf

%if 0%{?suse_version}
BuildRequires: readline-devel

BuildRequires: pkgconfig(libsystemd)
BuildRequires: pkgconfig(lzo2)
BuildRequires: pkgconfig(ncurses)
BuildRequires: pkgconfig(openssl)
BuildRequires: pkgconfig(zlib)
%endif

%if 0%{?fedora_version}
BuildRequires: util-linux-core
BuildRequires: glibc-langpack-en

BuildRequires: openssl-devel
BuildRequires: pkgconfig(liblz4)
BuildRequires: pkgconfig(libsystemd)
BuildRequires: pkgconfig(lzo2)
BuildRequires: pkgconfig(ncurses)
BuildRequires: pkgconfig(openssl)
BuildRequires: pkgconfig(readline)
BuildRequires: pkgconfig(systemd)
BuildRequires: pkgconfig(zlib)
%endif

%if 0%{?debian} || 0%{?ubuntu}
BuildRequires: bzr
BuildRequires: debbuild-macros

BuildRequires: liblz4-dev
BuildRequires: liblzo2-dev
BuildRequires: libncurses5-dev
BuildRequires: libreadline-dev
BuildRequires: libssl-dev
BuildRequires: libsystemd-dev
BuildRequires: zlib1g-dev
%endif

Requires(post):   systemd info
Requires(preun):  systemd info
Requires(postun): systemd

%description
tinc is a Virtual Private Network (VPN) daemon that uses tunnelling
and encryption to create a secure private network between hosts on
the Internet. Because the tunnel appears to the IP level network
code as a normal network device, there is no need to adapt any
existing software. This tunnelling allows VPN sites to share
information with each other over the Internet without exposing any
information to others.

%define debug_package %{nil}
%define __meson_auto_features auto

%prep
%setup -n tinc-%{version}

%build
%meson
%meson_build

%install
%meson_install

%files
%doc AUTHORS COPYING.README NEWS README.md THANKS doc/sample*
%license COPYING
%{_mandir}/man*/tinc*.*
%{_infodir}/tinc.info*
%{_sbindir}/tinc
%{_sbindir}/tincd
%{_unitdir}/tinc*.service
%{_datadir}/bash-completion/completions/tinc

################################################################################
# SLES & OpenSUSE
################################################################################
%if 0%{?suse_version}
%pre
%service_add_pre %{svc}

%post
%service_add_post %{svc}
install-info %{_infodir}/tinc.info %{_infodir}/dir || :

%preun
%service_del_preun %{svc}
install-info --delete %{_infodir}/tinc.info %{_infodir}/dir || :

%postun
%service_del_postun %{svc}
%endif

################################################################################
# Fedora, Debian, Ubuntu
################################################################################
%if 0%{?debian} || 0%{?ubuntu} || 0%{?fedora_version}
%post
%systemd_post %{svc}
install-info %{_infodir}/tinc.info %{_infodir}/dir || :

%preun
%systemd_preun %{svc}
install-info --delete %{_infodir}/tinc.info %{_infodir}/dir || :
%endif

%changelog

