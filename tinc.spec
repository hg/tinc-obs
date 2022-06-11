Name:           tinc
Version:        1.1
Release:        0
Summary:        A Virtual Private Network daemon
License:        GPL-2.0+
Group:          Productivity/Networking/Security
URL:            https://www.tinc-vpn.org

%define _svc     tinc.service tinc@.service
%define _archive tinc-%{version}

Source0:        %{_archive}.tar

BuildRequires: git
BuildRequires: meson
BuildRequires: pkgconf

%if "%{_vendor}" == "debbuild"
BuildRequires: debbuild-macros
BuildRequires: liblz4-dev
BuildRequires: liblzo2-dev
BuildRequires: libncurses5-dev
BuildRequires: libreadline-dev
BuildRequires: libssl-dev
BuildRequires: libsystemd-dev
BuildRequires: systemd
BuildRequires: zlib1g-dev
BuildRequires: texinfo
%else
BuildRequires: pkgconfig(liblz4)
BuildRequires: pkgconfig(libsystemd)
BuildRequires: pkgconfig(ncurses)
BuildRequires: pkgconfig(openssl)
BuildRequires: pkgconfig(systemd)
BuildRequires: pkgconfig(zlib)
BuildRequires: readline-devel

%if 0%{?rhel} == 8
BuildRequires: lzo-devel
%else
BuildRequires: pkgconfig(lzo2)
%endif

%if 0%{?suse_version}
BuildRequires: makeinfo
%else
BuildRequires: texinfo
%endif

%endif

%systemd_requires
Requires(post):  info
Requires(preun): info

# prevent setting auto features to 'enabled'
%define __meson_auto_features auto

%description
tinc is a Virtual Private Network (VPN) daemon that uses tunnelling
and encryption to create a secure private network between hosts on
the Internet. Because the tunnel appears to the IP level network
code as a normal network device, there is no need to adapt any
existing software. This tunnelling allows VPN sites to share
information with each other over the Internet without exposing any
information to others.

%prep
%setup -n %{_archive}

%build
%meson
%meson_build

%install
%meson_install
mkdir -p %{buildroot}/etc/tinc

%if 0%{?suse_version}
ln -s service %{buildroot}%{_sbindir}/rctinc
%endif

%pre
%{?systemd_pre:%systemd_pre %_svc}

%post
%systemd_post %_svc
install-info %{_infodir}/tinc.info %{_infodir}/dir || :

%preun
%systemd_preun %_svc
install-info --delete %{_infodir}/tinc.info %{_infodir}/dir || :

%postun
%systemd_postun_with_restart %_svc

%files
%doc NEWS README.md QUICKSTART.md doc/sample-config/
%license COPYING
%config(noreplace) /etc/tinc/

%{_mandir}/man*/tinc*.*
%{_infodir}/tinc.info*
%{_sbindir}/tinc
%{_sbindir}/tincd
%{_unitdir}/tinc*.service
%{_datadir}/bash-completion/completions/tinc

%if 0%{?suse_version}
%{_sbindir}/rctinc
%endif

%changelog

