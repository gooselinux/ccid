%define dropdir %(pkg-config libpcsclite --variable usbdropdir 2>/dev/null)
%define libusb_ver 0.1.7
%define pcsc_lite_ver 1.3.3
%define upstream_build 2656

Name:           ccid
Version:        1.3.9
Release:        3%{dist}
Summary:        Generic USB CCID smart card reader driver

Group:          System Environment/Libraries
License:        LGPLv2+
URL:            http://pcsclite.alioth.debian.org/ccid.html
Source0:        http://alioth.debian.org/download.php/%{upstream_build}/%{name}-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  libusb-devel >= %{libusb_ver}
BuildRequires:  pcsc-lite-devel >= %{pcsc_lite_ver}
Requires(post): initscripts
Requires(postun): initscripts
Requires:       libusb >= %{libusb_ver}
Requires:       pcsc-lite >= %{pcsc_lite_ver}
Provides:       pcsc-ifd-handler
# 390 does not have libusb or smartCards
ExcludeArch: s390 s390x


%description
Generic USB CCID (Chip/Smart Card Interface Devices) driver.


%prep
%setup -q
for f in ChangeLog README ; do
  iconv -f iso-8859-1 -t utf-8 $f > $f.utf8 ; mv $f.utf8 $f
done


%build
%configure --disable-dependency-tracking --disable-static --enable-twinserial --enable-udev
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
#make install_ccidtwin -C src DESTDIR=$RPM_BUILD_ROOT
mv $RPM_BUILD_ROOT%{_sysconfdir}/reader.conf ./GemPCTwin.reader.conf
mv $RPM_BUILD_ROOT/usr/share/doc/ccid/README_Kobil_mIDentity_switch.txt ./
%{__mkdir_p} $RPM_BUILD_ROOT/%{_sysconfdir}/udev/rules.d
%{__install} -m 644 src/pcscd_ccid.rules $RPM_BUILD_ROOT/%{_sysconfdir}/udev/rules.d/85-pcscd_ccid.rules


%clean
rm -rf $RPM_BUILD_ROOT


%post
[ -x %{_initrddir}/pcscd ] && %{_initrddir}/pcscd status >> /dev/null 2>&1 && %{_sbindir}/pcscd -H > /dev/null 2>&1
exit 0

%postun
[ -x %{_initrddir}/pcscd ] && %{_initrddir}/pcscd status >> /dev/null 2>&1 && %{_sbindir}/pcscd -H  > /dev/null 2>&1
exit 0


%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING README GemPCTwin.reader.conf README_Kobil_mIDentity_switch.txt
%{dropdir}/ifd-ccid.bundle/
%{dropdir}/serial/
%config %{_sysconfdir}/udev/rules.d/85-pcscd_ccid.rules
%{_bindir}/RSA_SecurID_getpasswd
%{_mandir}/man1/RSA_SecurID_getpasswd.1.gz
%{_mandir}/man8/Kobil_mIDentity_switch.8.gz
%{_sbindir}/Kobil_mIDentity_switch
#%doc /doc/ccid/


%changelog
* Mon Jan 11 2010  Bob Relyea <rrelyea@redhat.com> - 1.3.9-3
- 1) use normal version bumping.
- 2) update URL tag to be correct

* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 1.3.9-2.1
- Rebuilt for RHEL 6

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Bob Relyea <rrelyea@redhat.com> - 1.3.9-1
- update to ccid 1.3.9

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Aug 26 2008 Bob Relyea <rrelyea@redhat.com> - 1.3.8-1
- update to ccid 1.3.8

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.2.1-4
- Autorebuild for GCC 4.3

* Fri Aug 20 2007 Bob Relyea <rrelyea@redhat.com> - 1.2.1-3
- Update License description to the new Fedora standard

* Mon Apr 30 2007 Bob Relyea <rrelyea@redhat.com> - 1.2.1-2
- Fix the missed use of the version macro

* Tue Feb 06 2007 Bob Relyea <rrelyea@redhat.com> - 1.2.1-1
- Pick up ccid 1.2.1
- use pcscd 'hotplug' feature instead of restarting the daemon
- add enable_udev

* Mon Nov 06 2006 Bob Relyea <rrelyea@redhat.com> - 1.1.0-2
- Fix version macro to remove '-'

* Thu Nov 02 2006 Bob Relyea <rrelyea@redhat.com> - 1.1.0-1
- Pickup ccid 1.1.0

* Sun Jul 20 2006 Florian La Roche <laroche@redhat.com> - 1.0.1-5
- require initscripts for post/postun

* Sun Jul 16 2006 Florian La Roche <laroche@redhat.com> - 1.0.1-4
- fix excludearch line

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.0.1-3.1
- rebuild

* Mon Jul 10 2006 Bob Relyea <rrelyea@redhat.com> - 1.0.1-3
- remove s390 from the build

* Mon Jun  5 2006 Bob Relyea <rrelyea@redhat.com> - 1.0.1-2
- Move to Fedora Core, removed %%{_dist}.

* Sat Apr 22 2006 Ville Skyttä <ville.skytta at iki.fi> - 1.0.1-1
- 1.0.1.

* Mon Mar  6 2006 Ville Skyttä <ville.skytta at iki.fi> - 1.0.0-1
- 1.0.0, license changed to LGPL.

* Wed Feb 15 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.4.1-7
- Rebuild.

* Thu Nov  3 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.4.1-6
- Clean up build dependencies.
- Convert docs to UTF-8.

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 0.4.1-5
- rebuilt

* Fri Feb 25 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.4.1-4
- Drop Epoch: 0.
- Improve summary.
- Build with dependency tracking disabled.

* Thu Jul  1 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.4.1-0.fdr.3
- Restart pcscd in post(un)install phase if it's available and running.

* Thu May 13 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.4.1-0.fdr.2
- Provide pcsc-ifd-handler (idea from Debian).

* Sat Feb 14 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.4.1-0.fdr.1
- Update to 0.4.1.

* Fri Feb 13 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.4.0-0.fdr.1
- Update to 0.4.0.

* Wed Nov  5 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.3.2-0.fdr.1
- Update to 0.3.2.
- Update URL.

* Thu Oct 16 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.3.1-0.fdr.1
- Update to 0.3.1.

* Wed Sep 10 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.3.0-0.fdr.1
- Update to 0.3.0.

* Wed Aug 27 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.2.0-0.fdr.1
- Update to 0.2.0.

* Tue Aug 19 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.1.0-0.fdr.1
- First build.
