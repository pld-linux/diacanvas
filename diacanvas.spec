#
# Conditional build:
%bcond_without  apidocs     # disable gtk-doc
%bcond_without  static_libs # don't build static library

%define		src_name	diacanvas2

Summary:	Library for easely creating diagrams
Summary(pl):	Biblioteka do prostego tworzenia diagramów
Name:		diacanvas
Version:	0.14.3
Release:	1
License:	GPL
Group:		X11/Libraries
Source0:	http://dl.sourceforge.net/diacanvas/%{src_name}-%{version}.tar.gz
# Source0-md5:	cc1dc41aff8084cb9e4514a0edbaf8b4
URL:		http://diacanvas.sourceforge.net/
%{?with_apidocs:BuildRequires:  gtk-doc >= 1.0}
BuildRequires:	libgnomeprintui-devel >= 2.2.0
BuildRequires:	libtool
BuildRequires:	pkgconfig
# for canvas.defs
BuildRequires:	python-gnome-devel >= 2.0.0
BuildRequires:	python-pygtk-devel >= 1:2.0.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		pydefsdir	%(pkg-config --variable=defsdir pygtk-2.0)

%description
Library for easy diagrams creation.

%description -l pl
Biblioteka do prostego tworzenia diagramów.

%package devel
Summary:	Diacanvas header files and development documentation
Summary(pl):	Pliki nag³ówkowe i dokumentacja biblioteki Diacanvas
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Diacanvas header files and development documentation.

%description devel -l pl
Pliki nag³ówkowe i dokumentacja biblioteki Diacanvas.

%package static
Summary:	Diacanvas static libraries
Summary(pl):	Biblioteki statyczne Diacanvas
Group:		X11/Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Diacanvas static libraries.

%description static -l pl
Biblioteki statyczne Diacanvas.

%package apidocs
Summary:    Diacanvas API documentation
Group:      Documentation
Requires:   gtk-doc-common

%description apidocs
Diacanvas API documentation.

%package -n python-%{name}
Summary:	Diacanvas Python bindings
Summary(pl):	Wi±zania jêzyka Python do biblioteki Diacanvas
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}
%pyrequires_eq	python-libs
Requires:	python-pygtk-gtk >= 1.99.16

%description -n python-%{name}
Diacanvas Python bindings.

%description -n python-%{name} -l pl
Wi±zania jêzyka Python do biblioteki Diacanvas.

%package -n python-%{name}-devel
Summary:	Diacanvas Python bindings development files
Summary(pl):	Pliki dla programistów wi±zañ jêzyka Python do biblioteki Diacanvas
Group:		Development/Languages/Python
Requires:	%{name} = %{version}-%{release}

%description -n python-%{name}-devel
Diacanvas Python bindings development files.

%description -n python-%{name}-devel -l pl
Pliki dla programistów wi±zañ jêzyka Python do biblioteki Diacanvas.

%prep
%setup -q -n %{src_name}-%{version}

%build
%configure \
    --%{?with_static_libs:en}%{!?with_static_libs:dis}able-static \
	--enable-gnome-print \
	--enable-python \
    --%{?with_apidocs:en}%{!?with_apidocs:dis}able-gtk-doc \
    %{?with_apidocs:--with-html-dir=%{_gtkdocdir}}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%py_comp $RPM_BUILD_ROOT%{py_sitedir}
%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_postclean
rm -f $RPM_BUILD_ROOT%{py_sitedir}/%{name}/*.{la,a}

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc README ChangeLog TODO NEWS AUTHORS
%attr(755,root,root) %{_libdir}/*.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/*.so
%{_libdir}/*.la
%{_includedir}/diacanvas
%{_pkgconfigdir}/*

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/*
%endif

%files -n python-%{name}
%defattr(644,root,root,755)
%dir %{py_sitedir}/%{name}
%attr(755,root,root) %{py_sitedir}/%{name}/*.so
%{py_sitedir}/%{name}/*.py[co]

%files -n python-%{name}-devel
%defattr(644,root,root,755)
%{pydefsdir}/*
