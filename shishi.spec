# TODO:
# - init scripts for shishid
Summary:	Shishi - an implementation of RFC 1510(bis) (Kerberos V5 authentication)
Summary(pl):	Shishi - implementacja RFC 1510(bis) (uwierzytelniania Kerberos V5)
Name:		shishi
Version:	0.0.13
Release:	0.1
Epoch:		0
License:	GPL
Group:		Libraries
Source0:	http://josefsson.org/shishi/releases/%{name}-%{version}.tar.gz
# Source0-md5:	fd240f295f58b201112bfbac5fca4bcb
Patch0:		%{name}-info.patch
URL:		http://josefsson.org/shishi/
BuildRequires:	autoconf >= 2.57
BuildRequires:	automake >= 1.7
BuildRequires:	gnutls-devel >= 1.0.0
BuildRequires:	gtk-doc >= 1.1
BuildRequires:	libgcrypt-devel >= 1.1.43
BuildRequires:	libidn-devel >= 0.1.0
BuildRequires:	libtasn1-devel >= 0.2.5
BuildRequires:	libtool >= 2:1.5
BuildRequires:	pam-devel
BuildRequires:	texinfo
Requires(post,postun):	/sbin/ldconfig
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

# we don't have libtool 1.5a
%{__perl} -pi -e 's/AC_LIBTOOL_TAGS//' configure.ac
# incompatible with ksh
rm -f m4/libtool.m4

%build
# blegh, lt incompatible with ksh - must rebuild
%{__libtoolize}
%{__aclocal} -I gl/m4 -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure

%{__make}
%{__make} extra

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__make} -C extra install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/%{_lib}/security
mv -f $RPM_BUILD_ROOT%{_libdir}/pam_shishi.so* $RPM_BUILD_ROOT/%{_lib}/security
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
%doc AUTHORS ChangeLog NEWS README* THANKS
%attr(755,root,root) %{_bindir}/shisa
%attr(755,root,root) %{_bindir}/shishi
%attr(755,root,root) %{_sbindir}/shishid
%attr(755,root,root) %{_libdir}/libshis*.so.*.*.*
%dir %{_sysconfdir}/shishi
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/shishi/shisa.conf
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/shishi/shishi.conf
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/shishi/shishi.keys
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/shishi/shishi.skel
%attr(700,root,root) %dir %{_localstatedir}/%{name}
%{_mandir}/man1/shisa.1*
%{_mandir}/man1/shishi.1*
%{_mandir}/man1/shishid.1*
%{_infodir}/shishi.info*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libshis*.so
%{_libdir}/libshis*.la
%{_includedir}/shis*.h
%{_pkgconfigdir}/shishi.pc
%{_mandir}/man3/*

%files static
%defattr(644,root,root,755)
%{_libdir}/libshis*.a

%files -n pam-pam_shishi
%defattr(644,root,root,755)
%attr(755,root,root) /%{_lib}/security/pam_shishi.so*
