Summary: Grafana - An open source, feature rich metrics dashboard and graph editor for Graphite, InfluxDB & OpenTSDB. 
Name: grafana
Version: 1.7.0
Release: 1 
License: GPL
Group: Applications
Source: http://grafanarel.s3.amazonaws.com/grafana-1.7.0.tar.gz
URL: http://grafana.org/  
Distribution: CentOS Linux
Vendor: Grafana 
Packager: Chad Malfait<chad.malfait@autodesk.com>

%description
An open source, feature rich metrics dashboard and graph editor for Graphite, InfluxDB & OpenTSDB.

%prep
rm -rf %{_builddir}/grafana*
rm -rf %{_buildroot}/grafana*

%setup -q

%build
mkdir -p %{buildroot}/var/www/html/grafana
cp -r %{_builddir}/grafana*/* %{buildroot}/var/www/html/grafana

%install

%clean

%post

%files
/var/www/html/*

%dir 
