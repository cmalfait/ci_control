Name:           graphite-web

Version:        0.9.12
Release:        1%{?dist}
Summary:        A Django webapp for enterprise scalable realtime graphing

License:        ASL 2.0
URL:            https://launchpad.net/graphite/
Source0:        https://github.com/downloads/graphite-project/graphite-web/graphite-web-0.9.12.tar.gz
Source1:        graphite-web-vhost.conf
Source2:        graphite-web-README.fedora
Source3:        graphite-web-logrotate.fedora
Source4:        graphite-web-README.selinux
Patch0:         graphite-web-0.9.12.patch
BuildRoot:      %{_tmppath}/graphite-web-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  python-devel
Requires:       python-whisper, mod_wsgi, pytz, python-simplejson
Requires:       dejavu-sans-fonts, dejavu-serif-fonts, pycairo, django-tagging
#Requires:       python-django
#Requires:       pyparsing

#%if 0%{?fedora} <= 17
#Requires:       python-sqlite2, Django
#%else
#%endif


%description
Graphite consists of a storage backend and a web-based visualization frontend.
Client applications send streams of numeric time-series data to the Graphite
backend (called carbon), where it gets stored in fixed-size database files
similar in design to RRD. The web frontend provides user interfaces
for visualizing this data in graphs as well as a simple URL-based API for
direct graph generation.

Graphite's design is focused on providing simple interfaces (both to users and
applications), real-time visualization, high-availability, and enterprise
scalability.


%package selinux
Summary:        SELinux labeling for graphite files
Requires:       %name = %version-%release
Requires(post): policycoreutils-python
Requires(postun): policycoreutils-python


%description selinux
SELinux labeling for graphite files.


%prep
%setup -q -n graphite-web-%{version}
# Patch for Filesystem Hierarchy Standard
# Remove thridparty libs
# https://github.com/hggh/graphite-web-upstream/commit/47361a2707f904a8b817ca96deeddabcdbaaa534.patch
%patch0 -p1
%{__install} -m 644 %{SOURCE2} README.fedora
%{__install} -m 644 %{SOURCE4} README.selinux


%build
%{__python} setup.py build

%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

# Create directories 
%{__mkdir_p} %{buildroot}%{_localstatedir}/lib/graphite-web
%{__mkdir_p} %{buildroot}%{_localstatedir}/log/graphite-web
%{__mkdir_p} %{buildroot}%{_localstatedir}/logrotate.d
%{__mkdir_p} %{buildroot}%{_sysconfdir}/graphite-web

# Install some default configurations and wsgi
%{__install} -Dp -m0644 conf/dashboard.conf.example %{buildroot}%{_sysconfdir}/graphite-web/dashboard.conf
%{__install} -Dp -m0644 webapp/graphite/local_settings.py.example %{buildroot}%{_sysconfdir}/graphite-web/local_settings.py
%{__install} -Dp -m0644 conf/graphite.wsgi.example %{buildroot}%{_datarootdir}/graphite/graphite-web.wsgi
%{__install} -Dp -m0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/httpd/conf.d/graphite-web.conf
%{__install} -Dp -m0644 %{SOURCE3} %{buildroot}%{_sysconfdir}/logrotate.d/graphite-web

# Configure django /media/ location
sed -i 's|##PYTHON_SITELIB##|%{python_sitelib}|' %{buildroot}%{_sysconfdir}/httpd/conf.d/graphite-web.conf

# Create local_settings symlink
pushd %{buildroot}%{python_sitelib}/graphite
%{__ln_s} %{_sysconfdir}/graphite-web/local_settings.py
popd

# Don't ship bins that are not needed for prodcution
%{__rm} %{buildroot}%{_bindir}/{build-index.sh,run-graphite-devel-server.py}

# Fix permissions
%{__chmod} 0644 %{buildroot}%{_datarootdir}/graphite/webapp/content/js/window/*
%{__chmod} 0644 conf/graphite.wsgi.example
%{__chmod} 0755 %{buildroot}%{python_sitelib}/graphite/manage.py

# Don't ship thirdparty
%{__rm} -rf %{buildroot}%{python_sitelib}/graphite/thirdparty
%{__rm} -rf %{_sysconfdir}/graphite-web/local_settings.pyc
%{__rm} -rf %{_sysconfdir}/graphite-web/local_settings.pyo

%post selinux
semanage fcontext -a -t httpd_sys_content_t '%{_localstatedir}/lib/graphite-web(/.*)?' 2>/dev/null || :
restorecon -R %{_localstatedir}/lib/graphite-web || :

%postun selinux
if [ $1 -eq 0 ] ; then
semanage fcontext -d -t httpd_sys_content_t '%{_localstatedir}/lib/graphite-web(/.*)?' 2>/dev/null || :
fi

%files
%doc README.fedora LICENSE conf/* examples/*
%{python_sitelib}/graphite*
%{_datarootdir}/graphite
%config(noreplace) %{_sysconfdir}/logrotate.d/graphite-web
%config(noreplace) %{_sysconfdir}/httpd/conf.d/graphite-web.conf
%config(noreplace) %{_sysconfdir}/graphite-web/local_settings.py
%config(noreplace) %{_sysconfdir}/graphite-web/dashboard.conf
#%exclude %{_sysconfdir}/graphite-web/local_settings.pyc
#%exclude %{_sysconfdir}/graphite-web/local_settings.pyo
%attr(-,apache,apache) %dir %{_localstatedir}/log/graphite-web
%attr(-,apache,apache) %dir %{_sharedstatedir}/graphite-web

%files selinux
%doc README.selinux

%changelog
* Wed Mar 13 2013 Jonathan Steffan <jsteffan@fedoraproject.org> - 0.9.10-7
- Update required fonts to actually include fonts (RHBZ#917361)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.10-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Dec 30 2012 Jonathan Steffan <jsteffan@fedoraproject.org> - 0.9.10-5
- Conditionally require python-sqlite2
- Conditionally require new Django namespace

* Sat Dec 29 2012 Jonathan Steffan <jsteffan@fedoraproject.org> - 0.9.10-4
- Update to use mod_wsgi
- Update vhost configuration file to correctly work on multiple python
  versions

* Sat Nov 24 2012 Jonathan Steffan <jsteffan@fedoraproject.org> - 0.9.10-3
- Address all rpmlint errors
- Add SELinux subpackage README
- Patch out thirdparty code, Require it instead

* Fri Nov 09 2012 Jonathan Steffan <jsteffan@fedoraproject.org> - 0.9.10-2
- Add logrotate

* Thu May 31 2012 Jonathan Steffan <jsteffan@fedoraproject.org> - 0.9.10-1
- Initial Package
