%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}

Name:           python-whisper
Version:        0.9.12
Release:        1%{?dist}
Summary:        Simple database library for storing time-series data

Group:          Development/Libraries
License:        ASL 2.0
URL:            https://launchpad.net/graphite/

Source0:        https://github.com/downloads/graphite-project/whisper/python-whisper-0.9.12.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  python-devel, python-setuptools

%description
simple database library for storing time-series data (similar in design to RRD)

%prep
%setup -q -n python-whisper-%{version}


%build
%{__python} setup.py build


%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

# Temp mv to non .py locations
pushd $RPM_BUILD_ROOT/usr/bin/
%{__mv} rrd2whisper.py rrd2whisper
%{__mv} whisper-create.py whisper-create
%{__mv} whisper-dump.py whisper-dump
%{__mv} whisper-fetch.py whisper-fetch
%{__mv} whisper-info.py whisper-info
%{__mv} whisper-merge.py whisper-merge
%{__mv} whisper-resize.py whisper-resize
%{__mv} whisper-set-aggregation-method.py whisper-set-aggregation-method
%{__mv} whisper-update.py whisper-update
popd

 
%files
%{python_sitelib}/*
%{_bindir}/whisper*
%{_bindir}/rrd2whisper


%changelog
* Sun Sep 16 2012 Jonathan Steffan <jsteffan@fedoraproject.org> - 0.9.10-2
- Add group to be able to build against EPEL5

* Thu May 31 2012 Jonathan Steffan <jsteffan@fedoraproject.org> - 0.9.10-1
- Initial Package
