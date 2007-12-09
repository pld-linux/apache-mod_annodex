%define 	apxs		/usr/sbin/apxs
Summary:	mod_annodex - full support for Annodex.net media for Apache
Summary(pl.UTF-8):	mod_annodex - pełna obsługa mediów Annodex.net dla Apache'a
Name:		apache-mod_annodex
Version:	0.2.2
Release:	1
License:	Apache v1.1
Group:		Networking/Daemons
Source0:	http://www.annodex.net/software/mod_annodex/download/mod_annodex-ap20-%{version}.tar.gz
# Source0-md5:	54d3fd4237d7789206797eb0c6de9af2
URL:		http://www.annodex.net/software/mod_annodex/index.html
BuildRequires:	%{apxs}
BuildRequires:	apache-devel >= 2.0
BuildRequires:	libannodex-devel
BuildRequires:	libcmml-devel
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	apache(modules-api) = %apache_modules_api
Requires:	apr >= 1:1.0.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)
%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)

%description
mod_annodex is a handler for type application/x-annodex. It provides
the following features:
 - dynamic generation of Annodex media from CMML files.
 - handling of timed query offsets, such as
        http://media.example.com/fish.anx?t=npt:01:20.8
   or
        http://media.example.com/fish.anx?id=Preparation
 - dynamic retrieval of CMML summaries, if the Accept: header prefers
   type text/x-cmml over application/x-annodex.

%description -l pl.UTF-8
mod_annodex to moduł obsługi dla typu application/x-annodex. Ma
następujące możliwości:
 - dynamiczne generowanie mediów Annodex z plików CMML
 - obsługę czasowych offsetów zapytań, takich jak
        http://media.example.com/fish.anx?t=npt:01:20.8
   albo
        http://media.example.com/fish.anx?id=Preparation
 - dynamiczne odtwarzanie podsumowań CMML, jeśli nagłówek Accept:
   preferuje typ text/x-cmml ponad application/x-annodex

%prep
%setup -q -n mod_annodex-ap20-%{version}

# regenerate Makefile
%{apxs} -n annodex -g
mv -f annodex/Makefile .
rm -rf annodex

%build
%{__make} \
	top_builddir=%{_pkglibdir} \
	APXS=%{apxs} \
	SH_LIBS=`pkg-config --libs annodex cmml`

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_sysconfdir}/httpd.conf}

install .libs/mod_annodex.so $RPM_BUILD_ROOT%{_pkglibdir}

cat annodex.load annodex.conf > $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf/90_mod_annodex.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%service -q httpd restart

%postun
if [ "$1" = "0" ]; then
	%service -q httpd restart
fi

%files
%defattr(644,root,root,755)
%doc LICENSE README
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf/90_mod_annodex.conf
%attr(755,root,root) %{_pkglibdir}/mod_annodex.so
