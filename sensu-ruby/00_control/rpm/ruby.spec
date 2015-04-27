%define _prefix /opt/sensu/ruby

Summary: An interpreter of object-oriented scripting language
Name: sensu-ruby
Version: 2.1.2 
Release: 1%{?dist}
License: (Ruby or BSD) and Public Domain
Group: Development/Languages 
URL: http://ruby-lang.org/

Source: ftp://ftp.ruby-lang.org/pub/%{name}-%{version}.tar.gz

BuildRequires: autoconf
BuildRequires: gdbm-devel
BuildRequires: ncurses-devel
#BuildRequires: libdb-devel
BuildRequires: db4-devel
BuildRequires: libffi-devel
BuildRequires: openssl-devel
BuildRequires: libyaml-devel
BuildRequires: readline-devel
BuildRequires: tk-devel
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
%setup -q
autoconf

%build

%configure 

make %{?_smp_mflags} COPY="cp -p" Q=

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

#%check
#DISABLE_TESTS=""
#
#%ifarch armv7l armv7hl armv7hnl
## test_call_double(DL::TestDL) fails on ARM HardFP
## http://bugs.ruby-lang.org/issues/6592
#DISABLE_TESTS="-x test_dl2.rb $DISABLE_TESTS"
#%endif
#
## test_debug(TestRubyOptions) fails due to LoadError reported in debug mode,
## when abrt.rb cannot be required (seems to be easier way then customizing
## the test suite).
#touch abrt.rb
#
#make check TESTS="-v $DISABLE_TESTS"

%post 
/sbin/ldconfig

%postun 
/sbin/ldconfig

%files
/opt/*
#%{_bindir}/*
#%{_sysconfdir}/*
#%{_includedir}/*
#%{_libdir}/*
