# TODO:
# - wait for libgcrypt 1.1.13, uncomment BR and remove marked files
# - init scripts for shishid and shishi-telnetd
Summary:	Shishi - an implementation of RFC 1510(bis) (Kerberos V5 authentication)
Summary(pl):	Shishi - implementacja RFC 1510(bis) (uwierzytelniania Kerberos V5)
Name:		shishi
Version:	0.0.0
Release:	0.1
License:	GPL
Group:		Libraries
Source0:	http://savannah.nongnu.org/download/shishi/unstable.pkg/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	29441804f9e6f39f549d0dfe7bb25d3e
Patch0:		%{name}-info.patch
URL:		http://www.nongnu.org/shishi/
BuildRequires:	gtk-doc >= 0.6
# contains copy of libgcrypt 1.1.13-cvs
#BuildRequires:	libgcrypt-devel >= 1.1.13
BuildRequires:	libidn-devel >= 0.1.0
BuildRequires:	libtasn1-devel >= 0.2.0
BuildRequires:	pam-devel
BuildRequires:	texinfo
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libexecdir	%{_sbindir}

%description
Shishi is a (still incomplete) implementation of the RFC 1510(bis)
network authentication system (known as Kerberos V5). Shishi can be
used to authenticate users in distributed systems.

Shishi contains a library ('libshishi') that can be used by
application developers to add support for RFC 1510 and a command line
utility ('shishi') that is used by users to interface with the
library, to acquire and manage tickets (and more). Included are also
a TELNET client and server (based on GNU InetUtils) for remote network
login, and a PAM module for host security. A rudimentary key
distribution center (KDC) daemon is included.

%description -l pl
Shishi to (nadal niekompletna) implementacja sieciowego systemu
uwierzytelniania RFC 1510(bis) (znanego jako Kerberos V5). Shishi mo¿e
byæ u¿ywane do uwierzytelniania u¿ytkowników w systemach
rozproszonych.

Shishi zawiera bibliotekê (libshishi), któr± programi¶ci mog±
wykorzystywaæ do dodawania obs³ugi RFC 1510 oraz narzêdzie dzia³aj±ce
z linii poleceñ (shishi), którym u¿ytkownicy mog± komunikowaæ siê z
bibliotek±, uzyskiwaæ i zarz±dzaæ biletami itp. Do³±czone s± tak¿e
klient i serwer TELNET (oparte na GNU InetUtils) do zdalnego logowania
oraz modu³ PAM do lokalnego modelu bezpieczeñstwa. Demon podstawowego
centrum dystrybucji kluczy (KDC) tak¿e jest za³±czony.

%package devel
Summary:	Header files for Shishi library
Summary(pl):	Pliki nag³ówkowe biblioteki Shishi
Group:		Development/Libraries
Requires:	%{name} = %{version}

%description devel
Header files for Shishi library.

%description devel -l pl
Pliki nag³ówkowe biblioteki Shishi.

%package static
Summary:	Static Shishi library
Summary(pl):	Statyczna biblioteka Shishi
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}

%description static
Static Shishi library.

%description static -l pl
Statyczna biblioteka Shishi.

%package telnet
Summary:	Kerberized Telnet client
Summary(pl):	Klient skerberyzowanego Telneta
Group:		Networking/Utilities
Requires:	%{name} = %{version}

%description telnet
Kerberized Telnet client.

%description telnet -l pl
Klient skerberyzowanego Telneta.

%package telnetd
Summary:	Kerberized DARPA TELNET protocol server
Summary(pl):	Serwer skerberyzowanego protoko³u DARPA TELNET
Group:		Networking/Daemons
PreReq:		rc-inetd
Requires:	%{name} = %{version}

%description telnetd
Kerberized DARPA TELNET protocol server.

%description telnetd -l pl
Serwer skerberyzowanego protoko³u DARPA TELNET.

%package -n pam_shishi
Summary:	PAM module for RFC 1510 (Kerberos V5) authentication
Summary(pl):	Modu³ PAM do uwierzytelniania RFC 1510 (Kerberos V5)
Group:		Libraries
Requires:	%{name} = %{version}

%description -n pam_shishi
PAM module for RFC 1510 (Kerberos V5) authentication.

%description -n pam_shishi -l pl
Modu³ PAM do uwierzytelniania RFC 1510 (Kerberos V5).

%prep
%setup -q

%build
%configure \
	--with-html-dir=%{_gtkdocdir}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/lib/security
mv -f $RPM_BUILD_ROOT%{_libdir}/pam_shishi.so* $RPM_BUILD_ROOT/lib/security
rm -f $RPM_BUILD_ROOT%{_libdir}/pam_shishi.{la,a}

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc ANNOUNCE AUTHORS ChangeLog NEWS README* THANKS
%attr(755,root,root) %{_bindir}/shishi
%attr(755,root,root) %{_sbindir}/shishid
%attr(755,root,root) %{_libdir}/libshishi.so.*.*.*
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/shishi.conf
%{_datadir}/%{name}
%{_mandir}/man1/shishi.1*
%{_infodir}/shishi.info*
# TODO: remove
%attr(755,root,root) %{_libdir}/libgcrypt.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libshishi.so
%{_libdir}/libshishi.la
%{_includedir}/shishi.h
%{_pkgconfigdir}/shishi.pc
%{_gtkdocdir}/shishi
# TODO: remove
%attr(755,root,root) %{_libdir}/libgcrypt.so
%{_libdir}/libgcrypt.la
%{_includedir}/gcrypt.h
%{_aclocaldir}/libgcrypt.m4
%{_infodir}/gcrypt.info*

%files static
%defattr(644,root,root,755)
%{_libdir}/libshishi.a
# TODO: remove
%{_libdir}/libgcrypt.a

%files telnet
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/shishi-telnet
%{_mandir}/man1/shishi-telnet.1*

%files telnetd
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/shishi-telnetd
%{_mandir}/man8/shishi-telnetd.8*

%files -n pam_shishi
%defattr(644,root,root,755)
%attr(755,root,root) /lib/security/pam_shishi.so*
