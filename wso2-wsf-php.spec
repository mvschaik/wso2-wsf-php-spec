Name:		wso2-wsf-php
Version:	2.1.0
Release:	1%{?dist}
Summary:	WSO2 Web Services Framework for PHP

Group:		Development/Tools
License:	Apache License V2.0
URL:		http://wso2.com/products/web-services-framework/php
Source0:	http://dist.wso2.org/products/wsf/php/%{version}/%{name}-src-%{version}.tar.gz
Patch0:		wso2-wsf-php.fixbuild.patch
Patch1:		wso2-wsf-php.msg_rcvr_lib.patch
Patch2:		wso2-wsf-php.literal_lib_name.patch
Patch3:		wso2-wsf-php.generic_streams_for_ssl.patch
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:	php-devel, openssl-devel, libxml2-devel
Requires:	php

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
%configure

# Remove rpath
find . -name libtool | xargs sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g'
find . -name libtool | xargs sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g'

make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot} INSTALL_ROOT=%{buildroot}

# Remove the installed doc files.  The doc files are pulled from the build
# directory, not buildroot
rm -rf %{buildroot}%{_prefix}/docs
rm -f %{buildroot}%{_prefix}/CREDITS
rm -f %{buildroot}%{_prefix}/INSTALL
rm -f %{buildroot}%{_prefix}/LICENSE
rm -f %{buildroot}%{_prefix}/NEWS
rm -f %{buildroot}%{_prefix}/NOTICE
rm -f %{buildroot}%{_prefix}/README
rm -f %{buildroot}%{_prefix}/AUTHORS
rm -f %{buildroot}%{_prefix}/COPYING
rm -f %{buildroot}%{_prefix}/axis2.xml

# Remove libtool archives
rm -f %{buildroot}%{_libdir}/*.la

# Remove axis2_http_server, tcpmon, and wsclient
rm -f %{buildroot}%{_bindir}/axis2_http_server
rm -f %{buildroot}%{_bindir}/wsclient
rm -f %{buildroot}%{_bindir}/tools/tcpmon/tcpmon

# Remove -devel stuff
rm -rf %{buildroot}%{_includedir}
rm -f %{buildroot}%{_libdir}/*.a
rm -f %{buildroot}%{_libdir}/pkgconfig/axis2c.pc

# Remove docs from share dir
rm -f %{buildroot}%{_datarootdir}/*

# Remove samples
rm -rf %{buildroot}%{_prefix}/samples

# Move the modules directory
mv %{buildroot}%{_prefix}/modules %{buildroot}%{_libdir}/wso2-axis2


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc README NEWS LICENSE NOTICE INSTALL README.INSTALL AUTHORS COPYING
%doc samples
%{_libdir}/libaxis2_axiom.so*
%{_libdir}/libaxis2_engine.so*
%{_libdir}/libaxis2_http_common.so*
%{_libdir}/libaxis2_http_receiver.so*
%{_libdir}/libaxis2_http_sender.so*
%{_libdir}/libaxis2_parser.so*
%{_libdir}/libaxis2_xpath.so*
%{_libdir}/libaxutil.so*
%{_libdir}/libguththila.so*
%{_libdir}/libneethi.so*
%{_libdir}/libneethi_util.so*
%{_libdir}/librampart.so*
%{_libdir}/libsandesha2.so*
%{_libdir}/libsandesha2_client.so*
%{_libdir}/wso2-axis2
%{_libdir}/php/modules/wsf.so

%changelog

