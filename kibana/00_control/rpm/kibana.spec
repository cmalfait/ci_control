Summary: Vvisualize logs and time-stamped data 
Name: kibana
Version: 3.1.0
Release: 1 
License: GPL
Group: Applications
Source: https://download.elasticsearch.org/kibana/kibana/kibana-3.1.0.tar.gz 
URL: http://elasticsearch.org/  
Distribution: CentOS Linux
Vendor: Elasticsearch 
Packager: Chad Malfait<chad.malfait@autodesk.com>

%description
visualize logs and time-stamped data

%prep
rm -rf %{_builddir}/kibana*
rm -rf %{_buildroot}/kibana*

%setup -q

%build
mkdir -p %{buildroot}/var/www/html/kibana
cp -r %{_builddir}/kibana*/* %{buildroot}/var/www/html/kibana

%install

%clean

%post

%files
/var/www/html/*

%dir 
