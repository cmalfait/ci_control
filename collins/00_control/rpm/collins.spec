%define __os_install_post %{nil}

Name:           collins
Version:        1.3.0
Release:        1%{?dist}
Summary:        collins
Group:          System Environment/Daemons
License:        Apache2 
URL:            http://tumblr.github.io/collins/index.html#about 
Source:         file:///var/tmp/collins-1.3.0.tar.gz 
BuildArch:      x86_64

#AutoReqProv: no

#Requires: libXt-devel
#Requires: unixODBC
Requires(pre): /usr/sbin/useradd, /usr/bin/getent
Requires(pre): shadow-utils
Requires(postun): /usr/sbin/userdel
Source91: collins.sh 
Source92: gen_passwords.sh 

%description
Collins 

%prep
rm -rf %{_builddir}/*
rm -rf %{_buildroot}/*

%setup -q 

%build

%install
mkdir -p %{buildroot}/opt/collins
mkdir -p %{buildroot}%{_localstatedir}/log/collins
mkdir -p %{buildroot}%{_localstatedir}/run/collins
cp -rp %{_builddir}/%{name}-%{version}/target/collins %{buildroot}/opt/collins
cp %{SOURCE91} %{buildroot}/opt/collins/collins/scripts
cp %{SOURCE92} %{buildroot}/opt/collins/collins/scripts

%clean

%pre
getent group collins >/dev/null || groupadd -r collins
getent passwd collins >/dev/null || \
    useradd -m -r -g collins -d /opt/collins -s /bin/bash \
    -c "collins role account" collins
exit 0

%files
%attr(-, collins, collins) /opt/collins/*

%dir
%attr(-, collins, collins) /opt/collins
%attr(-, collins, collins) %{_localstatedir}/log/collins
%attr(-, collins, collins) %{_localstatedir}/run/collins
