Summary: Lightweight library for embedding a webserver in applications
Name: libmicrohttpd
Version: 0.9.59
Release: 1%{?dist}
Group: Development/Libraries
License: LGPLv2+
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
URL: http://www.gnu.org/software/libmicrohttpd/
Source0: ftp://ftp.gnu.org/gnu/libmicrohttpd/%{name}-%{version}.tar.gz

BuildRequires:  autoconf, automake, libtool
%if 0%{?rhel} == 5
BuildRequires:	curl-devel
%endif
%if 0%{?fedora} >= 11 || 0%{?rhel} >= 6
BuildRequires:	libcurl-devel
%endif
BuildRequires:  gnutls-devel
BuildRequires:  libgcrypt-devel
BuildRequires:  graphviz
BuildRequires:  doxygen

Requires(post): info
Requires(preun): info

%description
GNU libmicrohttpd is a small C library that is supposed to make it
easy to run an HTTP server as part of another application.
Key features that distinguish libmicrohttpd from other projects are:

* C library: fast and small
* API is simple, expressive and fully reentrant
* Implementation is http 1.1 compliant
* HTTP server can listen on multiple ports
* Support for IPv6
* Support for incremental processing of POST data
* Creates binary of only 25k (for now)
* Three different threading models

%package devel
Summary:        Development files for libmicrohttpd
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description devel
Development files for libmicrohttpd

%package doc
Summary:        Documentation for libmicrohttpd
Group:          Documentation
Requires:       %{name} = %{version}-%{release}
%if 0%{?fedora} >= 11 || 0%{?rhel} >= 6
BuildArch:      noarch
%endif

%description doc
Doxygen documentation for libmicrohttpd and some example source code

%prep
%setup -q

%build
# Required because patches modify .am files
# autoreconf --force
%configure --disable-static --with-gnutls
make %{?_smp_mflags}
cd doc/doxygen && make full && cd -

# Disabled for now due to problems reported at
# https://gnunet.org/bugs/view.php?id=1619
#check
#make check %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

rm -f %{buildroot}%{_libdir}/libmicrohttpd.la
rm -f %{buildroot}%{_infodir}/dir

# Install some examples in /usr/share/doc/libmicrohttpd-${version}/examples
mkdir examples
install -m 644 src/examples/*.c examples

# Install the doxygen documentation in /usr/share/doc/libmicrohttpd-${version}/html
cp -R doc/doxygen/html html

%clean
rm -rf %{buildroot}

%post doc
/sbin/install-info %{_infodir}/libmicrohttpd.info.gz %{_infodir}/dir || :
/sbin/install-info %{_infodir}/libmicrohttpd-tutorial.info.gz %{_infodir}/dir || :

%preun doc
if [ $1 = 0 ] ; then
/sbin/install-info --delete %{_infodir}/libmicrohttpd.info.gz %{_infodir}/dir || :
/sbin/install-info --delete %{_infodir}/libmicrohttpd-tutorial.info.gz %{_infodir}/dir || :
fi

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc COPYING
%{_libdir}/libmicrohttpd.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/microhttpd.h
%{_libdir}/libmicrohttpd.so
%{_libdir}/pkgconfig/libmicrohttpd.pc

%files doc
%defattr(-,root,root,-)
%{_mandir}/man3/libmicrohttpd.3.gz
%{_infodir}/libmicrohttpd.info.gz
%{_infodir}/libmicrohttpd-tutorial.info.gz
%{_infodir}/libmicrohttpd_performance_data.png.gz
%doc AUTHORS README ChangeLog
%doc examples
%doc html

%changelog
* Thu May 7 2020 Alessandro Polidori <alessandro.polidori@nethesis.it> - 0.9.59-1
- Upgrade to version 0.9.59 - NethServer/dev#6135

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 0.9.33-2
- Mass rebuild 2014-01-24

* Tue Jan 14 2014 Václav Pavlín <vpavlin@redhat.com> - 0.9.33
- Update to latest uptsream release 0.9.33 due to
  security issues.
  Resolves: rhbz#1039393, rhbz#1039387

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 0.9.27-2
- Mass rebuild 2013-12-27

* Mon May 6 2013 Václav Pavlín <vpavlin@redhat.com> - 0.9.27-1
- Update to latest uptsream release 0.9.27

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.24-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jan 8 2013 Václav Pavlín <vpavlin@redhat.com> - 0.9.24-1
- Update to latest uptsream release 0.9.24

* Thu Sep 27 2012 Tim Niemueller <tim@niemueller.de> - 0.9.22-1
- Update to latest uptsream release 0.9.22

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Feb 27 2011 Tim Niemueller <tim@niemueller.de> - 0.9.7-1
- Update to new upstream release 0.9.7
- Remove upstreamed patches

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 26 2011 Tim Niemueller <tim@niemueller.de> - 0.9.6-1
- Update to new upstream release 0.9.6

* Mon Jan 24 2011 Tim Niemueller <tim@niemueller.de> - 0.9.5-1
- Update to new upstream release 0.9.5

* Tue Nov 16 2010 Tim Niemueller <tim@niemueller.de> - 0.9.2-3
- Add missing BR gnutls-devel and libgcrypt-devel
- Added patch to fix test apps (NSS instead of GnuTLS/OpenSSL curl,
  implicit DSO linking)
- Disable test cases for now due to false errors, reported upstream

* Tue Nov 16 2010 Tim Niemueller <tim@niemueller.de> - 0.9.2-2
- Re-enable HTTPS, configure flags had unexpected result

* Sun Nov 7 2010 Tim Niemueller <tim@niemueller.de> - 0.9.2-1
- Update to 0.9.2

* Fri Jun 4 2010 Erik van Pienbroek <epienbro@fedoraproject.org> - 0.4.6-1
- Update to 0.4.6

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jul 21 2009 Erik van Pienbroek <epienbro@fedoraproject.org> - 0.4.2-1
- Update to version 0.4.2
- Drop upstreamed patch

* Fri Feb 27 2009 Erik van Pienbroek <info@nntpgrab.nl> - 0.4.0a-1
- Update to version 0.4.0a
- Drop upstreamed patch
- Added a new patch to fix a 64bit issue
- The -devel package now contains a pkgconfig file
- The configure script is now run with '--enable-messages --enable-https'
- Made the -doc subpackage noarch (F11+)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Feb 14 2009 Erik van Pienbroek <info@nntpgrab.nl> - 0.4.0-1
- Update to version 0.4.0
- This version introduces a API bump (which is required for
  supporting large files on 32bit environments)
- The license issues we had with version 0.3.1 of this package (as
  discussed in #457924) are resolved in this version. The license
  of this package is now changed to LGPLv2+
- Added a patch to fix two testcases on 64bit environments (upstream bug #1454)

* Sat Sep 6 2008 Erik van Pienbroek <info@nntpgrab.nl> - 0.3.1-3
- Changed license to GPLv3+ and added some comments
  regarding the license issues with this package

* Sun Aug 10 2008 Erik van Pienbroek <info@nntpgrab.nl> - 0.3.1-2
- Changed license to LGPLv2+
- Moved the COPYING file to the main package

* Tue Aug 5 2008 Erik van Pienbroek <info@nntpgrab.nl> - 0.3.1-1
- Initial release

