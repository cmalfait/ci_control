%define debug_package %{nil}

Summary: Collectd Deploy - Deploys and configures collectd based on system location
Name: collectd-deploy
Version: 0.1.0
Release: 1 
License: ASL 2.0
Group: Applications
Source: file:///var/tmp/collectd-deploy-0.1.0.tar.gz
Distribution: CentOS Linux
Packager: Chad Malfait<chad.malfait@autodesk.com>

%description
Deploys and configures collectd based on system location 

%prep
rm -rf %{_builddir}/*
rm -rf %{buildroot}/*

%setup -q

%build
#go build -o %{buildroot}/opt/collectd-deploy/bin/collectd-deploy src/collectd-deploy.go

%install
mkdir -p %{buildroot}/opt/collectd-deploy/bin
mkdir -p %{buildroot}/opt/collectd-deploy/templates
mkdir -p %{buildroot}/opt/collectd-deploy/etc
cp %{_builddir}/collectd-deploy-0.1.0/collectd-deploy %{buildroot}/opt/collectd-deploy/bin
cp -rp %{_builddir}/collectd-deploy-0.1.0/src/config/* %{buildroot}/opt/collectd-deploy/etc
cp -rp %{_builddir}/collectd-deploy-0.1.0/src/templates/* %{buildroot}/opt/collectd-deploy/templates

%clean

%post
/opt/collectd-deploy/bin/collectd-deploy

%files
/opt/collectd-deploy/bin/collectd-deploy
/opt/collectd-deploy/etc/*
/opt/collectd-deploy/templates/*

%dir 
