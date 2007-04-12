Summary: A capable mail handling system with a command line interface.
Name: nmh
Obsoletes: mh
Provides: mh
Version: 1.2
Release: %mkrel 1
License: BSD-style
Url: http://savannah.nongnu.org/projects/nmh/
Group: Networking/Mail
Source0: ftp://ftp.mhost.com/pub/nmh/nmh-%{version}.tar.bz2
Source1: procmailrc.example
#
# XXX this patch was applied to nmh-0.27 and is included for reference.
Patch2: nmh-0.27-security.patch
Patch3: nmh-1.0.3-compat21.patch
Patch4: nmh-1.2-prefer_db4.patch

BuildRequires:	db4-devel
BuildRequires:	flex
BuildRequires:	libtermcap-devel
BuildRoot: %{_tmppath}/%{name}-root

%description
Nmh is an email system based on the MH email system and is intended to
be a (mostly) compatible drop-in replacement for MH.  Nmh isn't a
single comprehensive program.  Instead, it consists of a number of
fairly simple single-purpose programs for sending, receiving, saving,
retrieving and otherwise manipulating email messages.  You can freely
intersperse nmh commands with other shell commands or write custom
scripts which utilize nmh commands.  If you want to use nmh as a true
email user agent, you'll want to also install exmh to provide a user
interface for it--nmh only has a command line interface.

If you'd like to use nmh commands in shell scripts, or if you'd like to
use nmh and exmh together as your email user agent, you should install
nmh.

%prep
%setup -q

#
# XXX this patch was applied to nmh-0.27 and is included for reference.
#%patch2 -p1 -b .security
%patch3 -p0 -b .compat21
%patch4 -p0 -b .prefer_db4

# XXX add promailrc.example
cp %SOURCE1 .

%build
autoconf
# XXX is this still needed? breaks on 5.2 ...
%configure --with-editor=/bin/vi --with-mts=sendmail \
		--libdir=%_libdir/nmh \
		--sysconfdir=%_sysconfdir/nmh \
		--with-locking=fcntl

make

%install
rm -rf ${RPM_BUILD_ROOT}

# XXX unnecessary because DOT_LOCKING is disabled
make DESTDIR=${RPM_BUILD_ROOT} MAIL_SPOOL_GRP=$(id -gn) install

%clean
rm -rf ${RPM_BUILD_ROOT}

%post

if [ ! -d %{_bindir}/mh -a ! -L %{_bindir}/mh ] ; then
    ln -s . %{_bindir}/mh
fi
if [ ! -d %{_libdir}/mh -a ! -L %{_libdir}/mh ] ; then
    ln -s nmh %{_libdir}/mh
fi
if [ -d /etc/smrsh -a ! -L /etc/smrsh/slocal ] ; then
    ln -sf %{_libdir}/%{name}/slocal /etc/smrsh/slocal
fi


%triggerpostun -- mh, nmh <= 0.27-7
if [ ! -d %{_bindir}/mh -a ! -L %{_bindir}/mh ] ; then
    ln -s . %{_bindir}/mh
fi
if [ ! -d %{_libdir}/mh -a ! -L %{_libdir}/mh ] ; then
    ln -s nmh %{_libdir}/mh
fi

%preun
if [ $1 = 0 ]; then
    [ ! -L %{_bindir}/mh ] || rm -f %{_bindir}/mh
    [ ! -L %{_libdir}/mh ] || rm -f %{_libdir}/mh
    [ ! -d /etc/smrsh -a -L /etc/smrsh/slocal ] || rm -f /etc/smrsh/slocal
fi

%files
%defattr(-,root,root)
%doc docs/COMPLETION-* docs/DIFFERENCES docs/FAQ docs/MAIL.FILTERING docs/TODO docs/README* COPYRIGHT README VERSION
%doc procmailrc.example
%{_bindir}/*
%dir %{_sysconfdir}/nmh
%config (noreplace) %{_sysconfdir}/nmh/*

# XXX use of _libdir appears incorrect, should be libexecdir?
%dir %{_libdir}/nmh
%{_libdir}/nmh/*

%{_mandir}/man[158]/*


