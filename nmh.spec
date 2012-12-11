Summary:	A capable mail handling system with a command line interface
Name:		nmh
Version:	1.4
Release:	1
License:	BSD-style
URL:		http://savannah.nongnu.org/projects/nmh/
Group:		Networking/Mail
Source0:	ftp://ftp.mhost.com/pub/nmh/nmh-%{version}.tar.gz
Source1:	procmailrc.example
BuildRequires:	db-devel
BuildRequires:	flex
BuildRequires:	termcap-devel
BuildRequires:	libtool
BuildRequires:	sendmail-command
BuildRequires:	vim-minimal
Provides:	mh
Obsoletes:	mh
BuildRoot:	%{_tmppath}/%{name}-root

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

# XXX add promailrc.example
cp %SOURCE1 .

%build
# XXX is this still needed? breaks on 5.2 ...
%configure2_5x \
    --with-editor=/bin/vi \
    --with-mts=sendmail \
    --libdir=%{_libdir}/nmh \
    --sysconfdir=%{_sysconfdir}/nmh \
    --with-locking=fcntl

make

%install
rm -rf %{buildroot}

# XXX unnecessary because DOT_LOCKING is disabled
make DESTDIR=%{buildroot} MAIL_SPOOL_GRP=$(id -gn) install

%clean
rm -rf %{buildroot}

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


%changelog
* Mon May 07 2012 Crispin Boylan <crisb@mandriva.org> 1.4-1
+ Revision: 797290
- Drop patch 1
- New release

* Mon Dec 06 2010 Oden Eriksson <oeriksson@mandriva.com> 1.3-2mdv2011.0
+ Revision: 613078
- the mass rebuild of 2010.1 packages

* Sat Jan 30 2010 Funda Wang <fwang@mandriva.org> 1.3-1mdv2010.1
+ Revision: 498552
- New version 1.3

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild

* Tue Jul 29 2008 Thierry Vignaud <tv@mandriva.org> 1.2-4mdv2009.0
+ Revision: 254015
- rebuild

* Thu Jan 03 2008 Olivier Blin <blino@mandriva.org> 1.2-2mdv2008.1
+ Revision: 141006
- restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request
    - fix summary-ended-with-dot

* Sat Sep 29 2007 Oden Eriksson <oeriksson@mandriva.com> 1.2-2mdv2008.0
+ Revision: 93847
- attempt to fix #26612 (Various nmh components segfault) by adding two debian patches

