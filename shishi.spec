Summary:	Shishi - an implementation of RFC 1510(bis) (Kerberos V5 authentication)
Summary(pl):	Shishi - implementacja RFC 1510(bis) (uwierzytelniania Kerberos V5)
Name:		shishi
Version:	0.0.22
Release:	1
Epoch:		0
License:	GPL
Group:		Libraries
Source0:	http://josefsson.org/shishi/releases/%{name}-%{version}.tar.gz
# Source0-md5:	f613e538ed0bb990f3644bbe5f0ab444
Source1:	%{name}-shishid.init
Source2:	%{name}-shishid.sysconfig
Patch0:		%{name}-info.patch
Patch1:		%{name}-gnutls.patch
Patch2:		%{name}-fix.patch
URL:		http://josefsson.org/shishi/
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake >= 1:1.9
BuildRequires:	gettext-devel >= 0.12.1
BuildRequires:	gnutls-devel >= 1.2.5
BuildRequires:	gtk-doc >= 1.1
BuildRequires:	libgcrypt-devel >= 1.1.43
BuildRequires:	libidn-devel >= 0.1.0
BuildRequires:	libtasn1-devel >= 0.2.5
BuildRequires:	libtool >= 2:1.5
BuildRequires:	pam-devel
BuildRequires:	rpmbuild(macros) >= 1.159
BuildRequires:	texinfo
Requires(post,postun):	/sbin/ldconfig
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
Requires:	%{name} = %{epoch}:%{version}-%{release}
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
Requires:	%{name}-devel = %{epoch}:%{version}-%{release}

%description static
Static Shishi library.

%description static -l pl
Statyczna biblioteka Shishi.

%package shishid
Summary:	shishid - Kerberos 5 server
Summary(pl):	shishid - serwer Kerberosa 5
Group:		Networking/Daemons
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/useradd
Requires(pre):	/usr/sbin/groupadd
Requires(post,postun):	/sbin/chkconfig
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description shishid
shishid is a network daemon for issuing Kerberos 5 tickets.

%description shishid -l pl
shishid to sieciowy demon s³u¿±cy do wydawania biletów Kerberosa 5.

%package -n pam-pam_shishi
Summary:	PAM module for RFC 1510 (Kerberos V5) authentication
Summary(pl):	Modu³ PAM do uwierzytelniania RFC 1510 (Kerberos V5)
Group:		Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}
Obsoletes:	pam_shishi

%description -n pam-pam_shishi
PAM module for RFC 1510 (Kerberos V5) authentication.

%description -n pam-pam_shishi -l pl
Modu³ PAM do uwierzytelniania RFC 1510 (Kerberos V5).

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

rm -f po/stamp-po

# doesn't build on sparc (too few B* constants) and wasn't packaged anyway
%{__perl} -pi -e 's/^(SUBDIRS.*) rsh-redone/$1/' extra/Makefile.am

%build
# blegh, lt incompatible with ksh - must rebuild
%{__libtoolize}
%{__aclocal} -I gl/m4 -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--with-libgcrypt

%{__make}
%{__make} extra

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/%{_lib}/security,/etc/{sysconfig,rc.d/init.d}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__make} -C extra install \
	DESTDIR=$RPM_BUILD_ROOT

mv -f $RPM_BUILD_ROOT%{_libdir}/pam_shishi.so* $RPM_BUILD_ROOT/%{_lib}/security
rm -f $RPM_BUILD_ROOT%{_libdir}/pam_shishi.{la,a}

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/shishid
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/shishid

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
if [ -f /var/lock/subsys/shishid ]; then
	/etc/rc.d/init.d/shishid restart >&2
else
	echo "Run \"/etc/rc.d/init.d/shishid start\" to start shishid daemon." >&2
fi

%preun shishid
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/shishid ]; then
		/etc/rc.d/init.d/shishid stop >&2
	fi
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
%attr(755,root,root) %{_bindir}/shisa
%attr(755,root,root) %{_bindir}/shishi
%attr(755,root,root) %{_libdir}/libshis*.so.*.*.*
%dir %{_sysconfdir}/shishi
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/shishi/shisa.conf
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/shishi/shishi.conf
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/shishi/shishi.keys
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/shishi/shishi.skel
%attr(700,root,root) %dir %{_localstatedir}/%{name}
%{_mandir}/man1/shisa.1*
%{_mandir}/man1/shishi.1*
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

%files shishid
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/shishid
%attr(754,root,root) /etc/rc.d/init.d/shishid
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/sysconfig/shishid
%{_mandir}/man1/shishid.1*

%files -n pam-pam_shishi
%defattr(644,root,root,755)
%attr(755,root,root) /%{_lib}/security/pam_shishi.so*
