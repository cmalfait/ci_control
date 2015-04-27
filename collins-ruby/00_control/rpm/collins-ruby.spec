%define _prefix /opt/collins/collins-ruby

Summary: An interpreter of object-oriented scripting language

Name: collins-ruby
Version: 2.0.645 
Release: 1%{?dist}
License: (Ruby or BSD) and Public Domain
Group: Development/Languages 
URL: http://ruby-lang.org/

Source: ftp://ftp.ruby-lang.org/pub/%{name}-%{version}.tar.gz

BuildRequires: autoconf
BuildRequires: gdbm-devel
BuildRequires: ncurses-devel
BuildRequires: db4-devel
BuildRequires: libffi-devel
BuildRequires: openssl-devel
BuildRequires: libyaml-devel
BuildRequires: readline-devel
BuildRequires: tk-devel
BuildRequires: cmake

# Needed to pass test_set_program_name(TestRubyOptions)
BuildRequires: procps
BuildRequires: systemtap-sdt-devel
# Unbundle cert.pem
BuildRequires: ca-certificates

%description
Ruby is the interpreted scripting language for quick and easy
object-oriented programming.  It has many features to process text
files and to do system management tasks (as in Perl).  It is simple,
straight-forward, and extensible.

%prep
%setup -q -n collins-ruby-%{version}

%build

autoconf

%configure 

make %{?_smp_mflags} COPY="cp -p" Q=

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}


%pre
getent group collins >/dev/null || groupadd -r collins
getent passwd collins >/dev/null || \
    useradd -r -g collins -d /opt/collins -s /sbin/nologin \
    -c "collins role account" collins
exit 0

%post 
/sbin/ldconfig

%postun 
userdel collins
/sbin/ldconfig

%files
%attr(-, collins, collins) /opt/*
%attr(-, collins, collins) /usr/share/man/man1/erb.1.gz
%attr(-, collins, collins) /usr/share/man/man1/irb.1.gz
%attr(-, collins, collins) /usr/share/man/man1/rake.1.gz
%attr(-, collins, collins) /usr/share/man/man1/ri.1.gz
%attr(-, collins, collins) /usr/share/man/man1/ruby.1.gz
