Name:		wso2-wsf-php
Version:	2.1.0
Release:	1%{?dist}
Summary:	WSO2 Web Services Framework for PHP

Group:		Development/Tools
License:	Apache License V2.0
URL:		http://wso2.com/products/web-services-framework/php
Source0:	http://dist.wso2.org/products/wsf/php/%{version}/%{name}-src-%{version}.tar.gz
# Push DESTDIR to all installable components and allow proper setting of the
# libary install directory from configure
# https://wso2.org/jira/browse/WSFCPP-137
Patch0:		wso2-wsf-php.fixbuild.patch
# Allow definition of library path for services
# https://issues.apache.org/jira/browse/AXIS2C-1544
Patch1:		wso2-wsf-php.msg_rcvr_lib.patch
# Allow shared libs to be loaded using literal filenames as well as original inferred style
# https://issues.apache.org/jira/browse/AXIS2C-1549
Patch2:		wso2-wsf-php.literal_lib_name.patch
# Make stream support more complete for SSL
# https://issues.apache.org/jira/browse/AXIS2C-1556
Patch3:		wso2-wsf-php.generic_streams_for_ssl.patch
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:	php-devel, openssl-devel, libxml2-devel
Requires:	php, php-xml

%description
The WSO2 Web Services Framework for PHP is a PHP extension that delivers comprehensive WS-* based Web services support for the PHP world.
With WSO2 Web Services Framework for PHP, your PHP applications can acquire enterprise grade Web services capabilities and seamlessly integrate with other Java or .Net systems.

%prep
%setup -q -n %{name}-src-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
%configure --prefix=%{_libdir}/php/modules/wsf_c --libdir=%{_libdir}/php/modules/wsf_c/lib

# We should remove rpaths, but this would break the module. The libs are in a non-standard
# location.
#find . -name libtool | xargs sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g'
#find . -name libtool | xargs sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g'

make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot} INSTALL_ROOT=%{buildroot}

# Remove axis2_http_server
rm -f %{buildroot}%{_bindir}/axis2_http_server

# Remove docs from /usr/share
rm -f %{buildroot}%{_datarootdir}/*

# Remove samples, as they contain binaries that refer to unavailable libssl.
rm -rf %{buildroot}%{_libdir}/php/modules/wsf_c/samples

# Create config file
mkdir -p %{buildroot}%{_sysconfdir}/php.d
cat > %{buildroot}%{_sysconfdir}/php.d/wsf.ini  <<EOT
; Enable wsf extension module
extension=wsf.so
EOT

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc README NEWS LICENSE NOTICE INSTALL README.INSTALL AUTHORS COPYING
%doc samples
%config %{_sysconfdir}/php.d/wsf.ini
%{_libdir}/php/modules/wsf.so
%{_libdir}/php/modules/wsf_c

%changelog

* Mon Dec 20 2011 - maarten
- Created a working version

* Sat Dec 17 2011 - maarten
- Initial implementation
