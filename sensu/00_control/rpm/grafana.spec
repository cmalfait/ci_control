Name:           grafana 
Version:        1.5.4
Release:        1%{?dist}
Summary:        An open source, feature rich metrics dashboard and graph editor for Graphite & InfluxDB. 

Group:          Development/Libraries
License:        ASL 2.0
URL:            http://grafana.org/ 

Source0:        http://grafanarel.s3.amazonaws.com/grafana-1.5.4.tar.gz 
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch

%description
An open source, feature rich metrics dashboard and graph editor for Graphite & InfluxDB. 

%prep

%setup 

%build

%install
 
%files

%changelog
