Summary:	Shishi - an implementation of RFC 1510(bis) (Kerberos V5 authentication)
Summary(pl.UTF-8):	Shishi - implementacja RFC 1510(bis) (uwierzytelniania Kerberos V5)
Name:		shishi
Version:	0.0.37
Release:	1
Epoch:		0
License:	GPL v3+
Group:		Libraries
Source0:	http://josefsson.org/shishi/releases/%{name}-%{version}.tar.gz
# Source0-md5:	f5291b727621e46a395797f0a6816c31
Source1:	%{name}-shishid.init
Source2:	%{name}-shishid.sysconfig
Patch0:		%{name}-info.patch
URL:		http://josefsson.org/shishi/
BuildRequires:	autoconf >= 2.61
BuildRequires:	automake >= 1:1.10
BuildRequires:	gettext-devel >= 0.17
BuildRequires:	gnutls-devel >= 1.2.5
BuildRequires:	gtk-doc >= 1.1
BuildRequires:	libgcrypt-devel >= 1.1.43
BuildRequires:	libidn-devel >= 0.1.0
BuildRequires:	libtasn1-devel >= 1.4
BuildRequires:	libtool >= 2:1.5
BuildRequires:	pam-devel
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	texinfo
Requires(post,postun):	/sbin/ldconfig
Requires:	libtasn1 >= 1.4
Provides:	group(shishi)
Provides:	user(shishi)
# should be moved to shishi-enabled inetutils-* if such packages would exist
Obsoletes:	shishi-telnet
Obsoletes:	shishi-telnetd
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libexecdir	%{_sbindir}
%define		_localstatedir	%{_var}/lib

%description
Shishi is a (still incomplete) implementation of the RFC 1510(bis)
network authentication system (known as Kerberos V5). Shishi can be
used to authenticate users in distributed systems.

Shishi contains a library ('libshishi') that can be used by
application developers to add support for RFC 1510 and a command line
utility ('shishi') that is used by users to interface with the
library, to acquire and manage tickets (and more). Included are also a
TELNET client and server (based on GNU InetUtils) for remote network
login, and a PAM module for host security. A rudimentary key
distribution center (KDC) daemon is included.

%description -l pl.UTF-8
Shishi to (nadal niekompletna) implementacja sieciowego systemu
uwierzytelniania RFC 1510(bis) (znanego jako Kerberos V5). Shishi może
być używane do uwierzytelniania użytkowników w systemach
rozproszonych.

Shishi zawiera bibliotekę (libshishi), którą programiści mogą
wykorzystywać do dodawania obsługi RFC 1510 oraz narzędzie działające
z linii poleceń (shishi), którym użytkownicy mogą komunikować się z
biblioteką, uzyskiwać i zarządzać biletami itp. Dołączone są także
klient i serwer TELNET (oparte na GNU InetUtils) do zdalnego logowania
oraz moduł PAM do lokalnego modelu bezpieczeństwa. Demon podstawowego
centrum dystrybucji kluczy (KDC) także jest załączony.

%package devel
Summary:	Header files for Shishi library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki Shishi
Group:		Development/Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	gnutls-devel >= 1.2.5
Requires:	gtk-doc-common
Requires:	libgcrypt-devel >= 1.1.43
Requires:	libidn-devel >= 0.1.0
Requires:	libtasn1-devel >= 1.4

%description devel
Header files for Shishi library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki Shishi.

%package static
Summary:	Static Shishi library
Summary(pl.UTF-8):	Statyczna biblioteka Shishi
Group:		Development/Libraries
Requires:	%{name}-devel = %{epoch}:%{version}-%{release}

%description static
Static Shishi library.

%description static -l pl.UTF-8
Statyczna biblioteka Shishi.

%package shishid
Summary:	shishid - Kerberos 5 server
Summary(pl.UTF-8):	shishid - serwer Kerberosa 5
Group:		Networking/Daemons
Requires(post,postun):	/sbin/chkconfig
Requires(post,preun):	rc-scripts
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description shishid
shishid is a network daemon for issuing Kerberos 5 tickets.

%description shishid -l pl.UTF-8
shishid to sieciowy demon służący do wydawania biletów Kerberosa 5.

%package -n pam-pam_shishi
Summary:	PAM module for RFC 1510 (Kerberos V5) authentication
Summary(pl.UTF-8):	Moduł PAM do uwierzytelniania RFC 1510 (Kerberos V5)
Group:		Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}
Obsoletes:	pam_shishi

%description -n pam-pam_shishi
PAM module for RFC 1510 (Kerberos V5) authentication.

%description -n pam-pam_shishi -l pl.UTF-8
Moduł PAM do uwierzytelniania RFC 1510 (Kerberos V5).

%prep
%setup -q
%patch0 -p1

# doesn't build on sparc (too few B* constants) and wasn't packaged anyway
%{__perl} -pi -e 's/^(SUBDIRS.*) rsh-redone/$1/' extra/Makefile.am

%build
%{__libtoolize}
%{__aclocal} -I gl/m4 -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--with-libgcrypt \
	--with-pam-dir=/%{_lib}/security

%{__make}
%{__make} extra

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{sysconfig,rc.d/init.d}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__make} -C extra install \
	DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT/%{_lib}/security/pam_shishi.{la,a}

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/shishid
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/shishid
rm -f $RPM_BUILD_ROOT%{_datadir}/info/dir

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir %{_infodir} >/dev/null 2>&1

%postun
/sbin/ldconfig
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir %{_infodir} >/dev/null 2>&1

%pre shishid
%groupadd -P %{name}-shishid -g 125 shishi
%useradd -P %{name}-shishid -u 125 -d /usr/share/empty -s /bin/false -c "shishi user" -g shishi shishi

%post shishid
/sbin/chkconfig --add shishid
%service shishid restart "shishid daemon"

%preun shishid
if [ "$1" = "0" ]; then
	%service shishid stop
	/sbin/chkconfig --del shishid
fi

%postun shishid
if [ "$1" = "0" ]; then
	%userremove shishi
	%groupremove shishi
fi

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README* THANKS
%attr(755,root,root) %{_bindir}/ccache2shishi
%attr(755,root,root) %{_bindir}/shisa
%attr(755,root,root) %{_bindir}/shishi
%attr(755,root,root) %{_sbindir}/keytab2shishi
%attr(755,root,root) %{_libdir}/libshisa.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libshisa.so.0
%attr(755,root,root) %{_libdir}/libshishi.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libshishi.so.0
%dir %{_sysconfdir}/shishi
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/shishi/shisa.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/shishi/shishi.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/shishi/shishi.keys
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/shishi/shishi.skel
%attr(700,root,root) %dir %{_localstatedir}/%{name}
%{_mandir}/man1/ccache2shishi.1*
%{_mandir}/man1/keytab2shishi.1*
%{_mandir}/man1/shisa.1*
%{_mandir}/man1/shishi.1*
%{_infodir}/shishi.info*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libshisa.so
%attr(755,root,root) %{_libdir}/libshishi.so
%{_libdir}/libshisa.la
%{_libdir}/libshishi.la
%{_includedir}/shisa.h
%{_includedir}/shishi*.h
%{_pkgconfigdir}/shishi.pc
%{_mandir}/man3/shisa*.3*
%{_mandir}/man3/shishi*.3*

%files static
%defattr(644,root,root,755)
%{_libdir}/libshisa.a
%{_libdir}/libshishi.a

%files shishid
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/shishid
%attr(754,root,root) /etc/rc.d/init.d/shishid
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/shishid
%{_mandir}/man1/shishid.1*

%files -n pam-pam_shishi
%defattr(644,root,root,755)
%attr(755,root,root) /%{_lib}/security/pam_shishi.so
