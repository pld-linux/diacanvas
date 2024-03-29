#
# Conditional build:
%bcond_without	apidocs		# gtk-doc based API documentation
%bcond_without	python		# Python (2.x) binding
%bcond_without	static_libs	# static library
#
%define		src_name	diacanvas2
Summary:	Library for easely creating diagrams
Summary(pl.UTF-8):	Biblioteka do prostego tworzenia diagramów
Name:		diacanvas
Version:	0.14.4
Release:	2
License:	LGPL v2+
Group:		X11/Libraries
Source0:	https://downloads.sourceforge.net/diacanvas/%{src_name}-%{version}.tar.gz
# Source0-md5:	b3db6c961de3023489a4d2419dab89bd
Patch0:		%{name}-fix.patch
Patch1:		%{name}-glib.patch
Patch2:		%{name}-link.patch
URL:		http://diacanvas.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
%{?with_apidocs:BuildRequires:	gtk-doc >= 1.0}
BuildRequires:	libart_lgpl-devel >= 2.0
BuildRequires:	libgnomecanvas-devel >= 2.0.0
# libgnomeprintui-devel >= 2.2.0  used for demo only
BuildRequires:	libgnomeprint-devel >= 2.2.0
BuildRequires:	libtool
BuildRequires:	pkgconfig
%if %{with python}
# for canvas.defs
BuildRequires:	python-gnome-devel >= 2.0.0
BuildRequires:	python-pygtk-devel >= 1:2.0.0
%endif
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.219
Requires:	libart_lgpl >= 2.0
Requires:	libgnomecanvas >= 2.0.0
Requires:	libgnomeprint >= 2.2.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		pydefsdir	%(pkg-config --variable=defsdir pygtk-2.0)

%description
Library for easy diagrams creation.

%description -l pl.UTF-8
Biblioteka do prostego tworzenia diagramów.

%package devel
Summary:	Diacanvas header files and development documentation
Summary(pl.UTF-8):	Pliki nagłówkowe i dokumentacja biblioteki Diacanvas
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libart_lgpl-devel >= 2.0
Requires:	libgnomecanvas-devel >= 2.0.0
Requires:	libgnomeprint-devel >= 2.2.0

%description devel
Diacanvas header files and development documentation.

%description devel -l pl.UTF-8
Pliki nagłówkowe i dokumentacja biblioteki Diacanvas.

%package static
Summary:	Diacanvas static libraries
Summary(pl.UTF-8):	Biblioteki statyczne Diacanvas
Group:		X11/Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Diacanvas static libraries.

%description static -l pl.UTF-8
Biblioteki statyczne Diacanvas.

%package apidocs
Summary:	Diacanvas API documentation
Summary(pl.UTF-8):	Dokumentacja API Diacanvas
Group:		Documentation
Requires:	gtk-doc-common
BuildArch:	noarch

%description apidocs
Diacanvas API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API Diacanvas.

%package -n python-%{name}
Summary:	Diacanvas Python bindings
Summary(pl.UTF-8):	Wiązania języka Python do biblioteki Diacanvas
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}
%pyrequires_eq	python-libs
Requires:	python-pygtk-gtk >= 1:2.0.0

%description -n python-%{name}
Diacanvas Python bindings.

%description -n python-%{name} -l pl.UTF-8
Wiązania języka Python do biblioteki Diacanvas.

%package -n python-%{name}-devel
Summary:	Diacanvas Python bindings development files
Summary(pl.UTF-8):	Pliki dla programistów wiązań języka Python do biblioteki Diacanvas
Group:		Development/Languages/Python
Requires:	%{name} = %{version}-%{release}
Requires:	python-pygtk-devel >= 1:2.0.0

%description -n python-%{name}-devel
Diacanvas Python bindings development files.

%description -n python-%{name}-devel -l pl.UTF-8
Pliki dla programistów wiązań języka Python do biblioteki Diacanvas.

%prep
%setup -q -n %{src_name}-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%{__gtkdocize}
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--enable-static%{!?with_static_libs:=no} \
	--enable-gnome-print \
	--enable-gtk-doc%{!?with_apidocs:=no} \
	%{?with_python:--enable-python} \
	%{?with_apidocs:--with-html-dir=%{_gtkdocdir}}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/libdiacanvas2.la

%if %{with python}
%py_comp $RPM_BUILD_ROOT%{py_sitedir}
%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_postclean
%{__rm} $RPM_BUILD_ROOT%{py_sitedir}/%{name}/*.la
%if %{with static_libs}
%{__rm} $RPM_BUILD_ROOT%{py_sitedir}/%{name}/*.a
%endif
%endif

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc README ChangeLog TODO NEWS AUTHORS
%attr(755,root,root) %{_libdir}/libdiacanvas2.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libdiacanvas2.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libdiacanvas2.so
%{_includedir}/diacanvas
%{_pkgconfigdir}/diacanvas2.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libdiacanvas2.a
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/diacanvas2
%endif

%if %{with python}
%files -n python-%{name}
%defattr(644,root,root,755)
%dir %{py_sitedir}/%{name}
%attr(755,root,root) %{py_sitedir}/%{name}/*module.so
%{py_sitedir}/%{name}/*.py[co]

%files -n python-%{name}-devel
%defattr(644,root,root,755)
%{pydefsdir}/dia-boxed.defs
%{pydefsdir}/diacanvas.defs
%{pydefsdir}/diageometry.defs
%{pydefsdir}/diashape.defs
%{pydefsdir}/diaview.defs
%endif
