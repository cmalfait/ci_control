%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}

Name:           python-carbon
Version:        0.9.12
Release:        2%{?dist}
Summary:        Back-end data caching and persistence daemon for Graphite
Group:          System Environment/Daemons

License:        ASL 2.0
URL:            https://launchpad.net/graphite/
Source0:        https://github.com/downloads/graphite-project/carbon/python-carbon-0.9.12.tar.gz
Source1:        %{name}-cache.init
Source2:        %{name}-relay.init
Source3:        %{name}-aggregator.init
Source4:        %{name}.sysconfig
Patch0:         python-carbon-0.9.12.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  python-devel, python-setuptools
Requires:       python-whisper, python-twisted-core >= 8.0
Requires(post): chkconfig
Requires(pre):  shadow-utils
Requires(preun): chkconfig, initscripts


%description
Twisted daemon that listens for time-series data and writes this data
out to whisper databases, relays the data or aggregates the data.
Carbon is a data collection and storage agent.


%prep
%setup -q -n python-carbon-%{version}
# Patch for Filesystem Hierarchy Standard
%patch0 -p1


%build
%{__python} setup.py build


%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

# Temp mv to non .py locations
pushd %{buildroot}/usr/bin/
%{__mv} carbon-aggregator.py carbon-aggregator
%{__mv} carbon-cache.py carbon-cache
%{__mv} carbon-client.py carbon-client
%{__mv} carbon-relay.py carbon-relay
%{__mv} validate-storage-schemas.py validate-storage-schemas
popd

%{__mkdir_p} %{buildroot}%{_sysconfdir}/carbon
%{__mkdir_p} %{buildroot}%{_localstatedir}/log/carbon
%{__mkdir_p} %{buildroot}%{_localstatedir}/run/carbon
%{__mkdir_p} %{buildroot}%{_sharedstatedir}/carbon

# Install system configuration and init scripts
%{__install} -Dp -m0755 %{SOURCE1} %{buildroot}%{_sysconfdir}/init.d/carbon-cache
%{__install} -Dp -m0755 %{SOURCE2} %{buildroot}%{_sysconfdir}/init.d/carbon-relay
%{__install} -Dp -m0755 %{SOURCE3} %{buildroot}%{_sysconfdir}/init.d/carbon-aggregator
%{__install} -Dp -m0644 %{SOURCE4} %{buildroot}%{_sysconfdir}/sysconfig/carbon

# Install default configuration files
%{__mkdir_p} %{buildroot}%{_sysconfdir}/carbon
%{__install} -Dp -m0644 conf/carbon.conf.example %{buildroot}%{_sysconfdir}/carbon/carbon.conf
%{__install} -Dp -m0644 conf/storage-schemas.conf.example %{buildroot}%{_sysconfdir}/carbon/storage-schemas.conf

%{__mv}  %{buildroot}/usr/conf/* %{buildroot}%{_sysconfdir}/carbon


%pre
getent group carbon >/dev/null || groupadd -r carbon
getent passwd carbon >/dev/null || \
    useradd -r -g carbon -d %{_sharedstatedir}/carbon \
    -s /sbin/nologin -c "Carbon cache daemon" carbon


%preun
if [ $1 -eq 0 ] ; then
    /sbin/service carbon-cache stop >/dev/null 2>&1
    /sbin/chkconfig --del carbon-cache
    /sbin/service carbon-relay stop >/dev/null 2>&1
    /sbin/chkconfig --del carbon-relay
    /sbin/service carbon-aggregator stop >/dev/null 2>&1
    /sbin/chkconfig --del carbon-aggregator
fi


%post
/sbin/chkconfig --add carbon-cache
/sbin/chkconfig --add carbon-relay
/sbin/chkconfig --add carbon-aggregator


%postun
if [ $1 = 0 ]; then
  getent passwd carbon >/dev/null && \
      userdel -r carbon 2>/dev/null
fi


%files
%doc LICENSE conf/*
%dir %{_sysconfdir}/carbon
%dir %{_localstatedir}/run/carbon
%{_bindir}/carbon*
%{_bindir}/validate-storage-schemas
%{_sysconfdir}/init.d/carbon-*
%config(noreplace) %{_sysconfdir}/carbon/*
%config(noreplace) %{_sysconfdir}/sysconfig/carbon
#%attr(0755,-,-) %{python_sitelib}/carbon/amqp_publisher.py
#%attr(0755,-,-) %{python_sitelib}/carbon/amqp_listener.py
%{python_sitelib}/*
%attr(-,carbon,carbon) %{_localstatedir}/log/carbon
%attr(-,carbon,carbon) %{_sharedstatedir}/carbon


%changelog
* Sat Nov 24 2012 Jonathan Steffan <jsteffan@fedoraproject.org> - 0.9.10-2
- Update spec to build on el5
- Fix python_sitelib definition

* Wed May 30 2012 Jonathan Steffan <jsteffan@fedoraproject.org> - 0.9.10-1
- Initial Package
