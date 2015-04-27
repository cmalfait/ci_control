%global debug_package %{nil}

Name:           collins-jdk
Version:        1.7.0_75
Release:        1%{?dist}
Summary:        collins
Group:          System Environment/Daemons
License:        BCL 
URL:            http://tumblr.github.io/collins/index.html#about 
Source:         file:///var/tmp/collins-jdk-1.7.0_75.tar.gz 
BuildArch:      x86_64

AutoReqProv: no

Requires(pre): /usr/sbin/useradd, /usr/bin/getent
Requires(pre): shadow-utils
Requires(postun): /usr/sbin/userdel

%description
Collins JDK

%prep
rm -rf %{_builddir}/*
rm -rf %{_buildroot}/*

%setup -q 

%build

%install
mkdir -p %{buildroot}/opt/collins/jdk%{version}
cp -rp %{_builddir}/%{name}-%{version}/* %{buildroot}/opt/collins/jdk%{version}

%clean

%pre
getent group collins >/dev/null || groupadd -r collins
getent passwd collins >/dev/null || \
    useradd -m -r -g collins -d /opt/collins -s /sbin/nologin \
    -c "collins role account" collins
exit 0

%files
%attr(-, collins, collins) /opt/collins/jdk%{version}/*

%dir
#%attr(-, collins, collins) /opt/collins/jdk%{version}
#%attr(-, collins, collins) %{_localstatedir}/run/collins
