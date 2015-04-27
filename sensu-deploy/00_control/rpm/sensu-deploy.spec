%define debug_package %{nil}

Summary: Sensu Deploy - Deploys and configures sensu based on system location
Name: sensu-deploy
Version: 0.1.0
Release: 1 
License: ASL 2.0
Group: Applications
Source: file:///var/tmp/sensu-deploy-0.1.0.tar.gz
Distribution: CentOS Linux
Packager: Chad Malfait<chad.malfait@autodesk.com>

%description
Deploys and configures sensu based on system location 

%prep
rm -rf %{_builddir}/*
rm -rf %{buildroot}/*

%setup -q

%build
#go build -o %{buildroot}/opt/sensu-deploy/bin/sensu-deploy src/sensu-deploy.go

%install
mkdir -p %{buildroot}/opt/sensu-deploy/bin
mkdir -p %{buildroot}/opt/sensu-deploy/templates
mkdir -p %{buildroot}/opt/sensu-deploy/etc
cp %{_builddir}/sensu-deploy-0.1.0/sensu-deploy %{buildroot}/opt/sensu-deploy/bin
cp -rp %{_builddir}/sensu-deploy-0.1.0/src/config/* %{buildroot}/opt/sensu-deploy/etc
cp -rp %{_builddir}/sensu-deploy-0.1.0/src/templates/* %{buildroot}/opt/sensu-deploy/templates

%clean

%post
/opt/sensu-deploy/bin/sensu-deploy

%files
/opt/sensu-deploy/bin/sensu-deploy
/opt/sensu-deploy/etc/*
/opt/sensu-deploy/templates/*

%dir 
