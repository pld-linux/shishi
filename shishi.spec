# TODO:
# - init scripts for shishid and shishi-telnetd
Summary:	Shishi - an implementation of RFC 1510(bis) (Kerberos V5 authentication)
Summary(pl):	Shishi - implementacja RFC 1510(bis) (uwierzytelniania Kerberos V5)
Name:		shishi
Version:	0.0.8
Release:	0.1
Epoch:		0
License:	GPL
Group:		Libraries
Source0:	http://josefsson.org/shishi/releases/%{name}-%{version}.tar.gz
# Source0-md5:	49d854d20e9ebe7d85688eeb6e63859e
Patch0:		%{name}-info.patch
URL:		http://josefsson.org/shishi/
BuildRequires:	gnutls-devel >= 0.8.8
BuildRequires:	gtk-doc >= 0.6
BuildRequires:	libgcrypt-devel >= 1.1.43
BuildRequires:	libidn-devel >= 0.1.0
BuildRequires:	libtasn1-devel >= 0.2.5
BuildRequires:	pam-devel
BuildRequires:	pkgconfig
BuildRequires:	texinfo
Requires(post,postun):	/sbin/ldconfig
# should be moved to shishi-enabled inetutils-* if such packages would exist
Obsoletes:	shishi-telnet
Obsoletes:	shishi-telnetd
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
Requires:	%{name} = %{epoch}:%{version}
Requires:	gnutls-devel >= 0.8.8
Requires:	gtk-doc-common
Requires:	libgcrypt-devel >= 1.1.43
Requires:	libidn-devel >= 0.1.0
Requires:	libtasn1-devel >= 0.2.5

%description devel
Header files for Shishi library.

%description devel -l pl
Pliki nag³ówkowe biblioteki Shishi.

%package static
Summary:	Static Shishi library
Summary(pl):	Statyczna biblioteka Shishi
Group:		Development/Libraries
Requires:	%{name}-devel = %{epoch}:%{version}

%description static
Static Shishi library.

%description static -l pl
Statyczna biblioteka Shishi.

%package -n pam-pam_shishi
Summary:	PAM module for RFC 1510 (Kerberos V5) authentication
Summary(pl):	Modu³ PAM do uwierzytelniania RFC 1510 (Kerberos V5)
Group:		Libraries
Requires:	%{name} = %{epoch}:%{version}
Obsoletes:	pam_shishi

%description -n pam-pam_shishi
PAM module for RFC 1510 (Kerberos V5) authentication.

%description -n pam-pam_shishi -l pl
Modu³ PAM do uwierzytelniania RFC 1510 (Kerberos V5).

%prep
%setup -q
%patch0 -p1

%build
%configure \
	--with-html-dir=%{_gtkdocdir}

%{__make}
%{__make} extra

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__make} -C extra install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/lib/security
mv -f $RPM_BUILD_ROOT%{_libdir}/pam_shishi.so* $RPM_BUILD_ROOT/lib/security
rm -f $RPM_BUILD_ROOT%{_libdir}/pam_shishi.{la,a}

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir %{_infodir} >/dev/null 2>&1

%postun
/sbin/ldconfig
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir %{_infodir} >/dev/null 2>&1

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

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libshishi.so
%{_libdir}/libshishi.la
%{_includedir}/shishi*.h
%{_pkgconfigdir}/shishi.pc
%{_mandir}/man3/*
%{_gtkdocdir}/shishi

%files static
%defattr(644,root,root,755)
%{_libdir}/libshishi.a

%files -n pam-pam_shishi
%defattr(644,root,root,755)
%attr(755,root,root) /lib/security/pam_shishi.so*
