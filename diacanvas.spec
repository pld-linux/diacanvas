
%include	/usr/lib/rpm/macros.python

%define src_name diacanvas2

Summary:	Library for easely creating diagrams
Summary(pl):	Biblioteka do prostego tworzenia diagramów
Name:		diacanvas
Version:	0.10.0
Release:	1
License:	GPL
Group:		X11/Libraries
Source0:	http://dl.sourceforge.net/sourceforge/%{name}/%{src_name}-%{version}.tar.gz
# Source0-md5:	26087d205ad833341fcfab047d70837f
Patch0:		%{name}-no_check.patch
URL:		http://diacanvas.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libgnomeprintui-devel >= 1.116.0
BuildRequires:	libtool
BuildRequires:	python-gnome-devel >= 1.99.13
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define pydefsdir %(pkg-config --variable=defsdir pygtk-2.0)

%description
Library for easy diagrams creation.

%description -l pl
Biblioteka do prostego tworzenia diagramów.

%package devel
Summary:	Diacanvas header files and development documentation
Summary(pl):	Pliki nag³ówkowe i dokumentacja biblioteki Diacanvas
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}

%description devel
Diacanvas header files and development documentation.

%description devel -l pl
Pliki nag³ówkowe i dokumentacja biblioteki Diacanvas.

%package static
Summary:	Diacanvas static libraries
Summary(pl):	Biblioteki statyczne Diacanvas
Group:		X11/Development/Libraries
Requires:	%{name}-devel = %{version}

%description static
Diacanvas static libraries.

%description static -l pl
Biblioteki statyczne Diacanvas.

%package -n python-%{name}
Summary:	Diacanvas Python bindings
Summary(pl):	Wi±zania jêzyka Python do biblioteki Diacanvas
Group:		Libraries/Python
Requires:	%{name} = %{version}
Requires:	python-pygtk-gtk >= 1.99.16

%description -n python-%{name}
Diacanvas Python bindings.

%description -n python-%{name} -l pl
Wi±zania jêzyka Python do biblioteki Diacanvas.

%package -n python-%{name}-devel
Summary:	Diacanvas Python bindings development files
Summary(pl):	Pliki dla programistów wi±zañ jêzyka Python do biblioteki Diacanvas
Group:		Development/Languages/Python
Requires:	%{name} = %{version}

%description -n python-%{name}-devel
Diacanvas Python bindings development files.

%description -n python-%{name}-devel -l pl
Pliki dla programistów wi±zañ jêzyka Python do biblioteki Diacanvas.

%prep
%setup -q -n %{src_name}-%{version}
%patch0 -p1

%build
rm -f missing
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--enable-static \
	--enable-gnome-print \
	--enable-python

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc README ChangeLog TODO NEWS AUTHORS
%attr(755,root,root) %{_libdir}/*.so.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/*.so
%{_libdir}/*.la
%{_includedir}/diacanvas
%{_datadir}/gtk-doc/html/%{src_name}
%{_pkgconfigdir}/*

%files static
%defattr(644,root,root,755)
%{_libdir}/*.a

%files -n python-%{name}
%defattr(644,root,root,755)
%dir %{py_sitedir}/%{name}
%attr(755,root,root) %{py_sitedir}/%{name}/*.so
%{py_sitedir}/%{name}/*.la
%{py_sitedir}/%{name}/*.py[co]

%files -n python-%{name}-devel
%defattr(644,root,root,755)
%{pydefsdir}/*
