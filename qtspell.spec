#
# Conditional build:
%bcond_without	apidocs		# API documentation
%bcond_without	static_libs	# static libraries
%bcond_without	qt5		# Qt5 library
%bcond_without	qt6		# Qt6 library
#
Summary:	QtSpell - Spell checking for Qt text widgets
Summary(pl.UTF-8):	QtSpell - sprawdzanie pisowni w widżetach tekstowych Qt
Name:		qtspell
Version:	1.0.1
Release:	1
License:	GPL v3+
Group:		Libraries
#Source0Download: https://github.com/manisandro/qtspell/releases
Source0:	https://github.com/manisandro/qtspell/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	3c6dda0a8b85e160b60c9fc7c00eddee
URL:		https://github.com/manisandro/qtspell
BuildRequires:	cmake >= 3.0
%{?with_apidocs:BuildRequires:	doxygen}
BuildRequires:	enchant2-devel >= 2
BuildRequires:	pkgconfig
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(find_lang) >= 1.42
BuildRequires:	rpmbuild(macros) >= 1.605
%if %{with qt5}
BuildRequires:	Qt5Core-devel >= 5
BuildRequires:	Qt5Widgets-devel >= 5
BuildRequires:	qt5-build >= 5
BuildRequires:	qt5-linguist >= 5
%endif
%if %{with qt6}
BuildRequires:	Qt6Core-devel >= 6
BuildRequires:	Qt6Widgets-devel >= 6
BuildRequires:	qt6-build >= 6
BuildRequires:	qt6-linguist >= 6
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
QtSpell adds spell-checking functionality to Qt's text widgets, using
the enchant spell-checking library.

%description -l pl.UTF-8
QtSpell dodaje funkcję sprawdzania pisowni do widżetów tekstowych Qt
przy użyciu biblioteki sprawdzania pisowni enchant.

%package qt5
Summary:	QtSpell - Spell checking for Qt5 text widgets
Summary(pl.UTF-8):	QtSpell - sprawdzanie pisowni w widżetach tekstowych Qt5
Group:		Libraries

%description qt5
QtSpell adds spell-checking functionality to Qt's text widgets, using
the enchant spell-checking library.

%description qt5 -l pl.UTF-8
QtSpell dodaje funkcję sprawdzania pisowni do widżetów tekstowych Qt
przy użyciu biblioteki sprawdzania pisowni enchant.

%package qt5-devel
Summary:	Header files for QtSpell-qt5 library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki QtSpell-qt5
Group:		Development/Libraries
Requires:	%{name}-qt5 = %{version}-%{release}
Requires:	Qt5Core-devel >= 5

%description qt5-devel
Header files for QtSpell-qt5 library.

%description qt5-devel -l pl.UTF-8
Pliki nagłówkowe biblioteki QtSpell-qt5.

%package qt5-static
Summary:	Static QtSpell-qt5 library
Summary(pl.UTF-8):	Statyczna biblioteka QtSpell-qt5
Group:		Development/Libraries
Requires:	%{name}-qt5-devel = %{version}-%{release}

%description qt5-static
Static QtSpell-qt5 library.

%description qt5-static -l pl.UTF-8
Statyczna biblioteka QtSpell-qt5.

%package qt5-apidocs
Summary:	API documentation for QtSpell-qt5 library
Summary(pl.UTF-8):	Dokumentacja API biblioteki QtSpell-qt5
Group:		Documentation
BuildArch:	noarch

%description qt5-apidocs
API documentation for QtSpell-qt5 library.

%description qt5-apidocs -l pl.UTF-8
Dokumentacja API biblioteki QtSpell-qt5.

%package qt6
Summary:	QtSpell - Spell checking for Qt5 text widgets
Summary(pl.UTF-8):	QtSpell - sprawdzanie pisowni w widżetach tekstowych Qt5
Group:		Libraries

%description qt6
QtSpell adds spell-checking functionality to Qt's text widgets, using
the enchant spell-checking library.

%description qt6 -l pl.UTF-8
QtSpell dodaje funkcję sprawdzania pisowni do widżetów tekstowych Qt
przy użyciu biblioteki sprawdzania pisowni enchant.

%package qt6-devel
Summary:	Header files for QtSpell-qt6 library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki QtSpell-qt6
Group:		Development/Libraries
Requires:	%{name}-qt6 = %{version}-%{release}
Requires:	Qt6Core-devel >= 5

%description qt6-devel
Header files for QtSpell-qt6 library.

%description qt6-devel -l pl.UTF-8
Pliki nagłówkowe biblioteki QtSpell-qt6.

%package qt6-static
Summary:	Static QtSpell-qt6 library
Summary(pl.UTF-8):	Statyczna biblioteka QtSpell-qt6
Group:		Development/Libraries
Requires:	%{name}-qt6-devel = %{version}-%{release}

%description qt6-static
Static QtSpell-qt6 library.

%description qt6-static -l pl.UTF-8
Statyczna biblioteka QtSpell-qt6.

%package qt6-apidocs
Summary:	API documentation for QtSpell-qt6 library
Summary(pl.UTF-8):	Dokumentacja API biblioteki QtSpell-qt6
Group:		Documentation
BuildArch:	noarch

%description qt6-apidocs
API documentation for QtSpell-qt6 library.

%description qt6-apidocs -l pl.UTF-8
Dokumentacja API biblioteki QtSpell-qt6.

%prep
%setup -q

%build
%if %{with qt5}
install -d build-qt5
cd build-qt5
%cmake .. \
	%{?with_static_libs:-DBUILD_STATIC_LIBS=ON} \
	-DQT_VER=5

%{__make}

%if %{with apidocs}
%{__make} doc
%endif

cd ..
%endif

%if %{with qt6}
install -d build-qt6
cd build-qt6
%cmake .. \
	%{?with_static_libs:-DBUILD_STATIC_LIBS=ON} \
	-DQT_VER=6

%{__make}

%if %{with apidocs}
%{__make} doc
%endif

cd ..
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with qt5}
%{__make} -C build-qt5 install \
	DESTDIR=$RPM_BUILD_ROOT

# duplicate of es
%{__rm} $RPM_BUILD_ROOT%{_datadir}/qt5/translations/QtSpell_es_ES.qm
%endif

%if %{with qt6}
%{__make} -C build-qt6 install \
	DESTDIR=$RPM_BUILD_ROOT
%endif

%find_lang QtSpell --with-qm
%if %{with qt5}
grep /qt5/translations/ QtSpell.lang > QtSpell-qt5.lang
%endif
%if %{with qt6}
grep /qt6/translations/ QtSpell.lang > QtSpell-qt6.lang
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	qt5 -p /sbin/ldconfig
%postun	qt5 -p /sbin/ldconfig

%post	qt6 -p /sbin/ldconfig
%postun	qt6 -p /sbin/ldconfig

%if %{with qt5}
%files qt5 -f QtSpell-qt5.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README.md
%attr(755,root,root) %{_libdir}/libqtspell-qt5.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libqtspell-qt5.so.1

%files qt5-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libqtspell-qt5.so
%{_includedir}/QtSpell-qt5
%{_pkgconfigdir}/QtSpell-qt5.pc

%if %{with static_libs}
%files qt5-static
%defattr(644,root,root,755)
%{_libdir}/libqtspell-qt5.a
%endif

%if %{with apidocs}
%files qt5-apidocs
%defattr(644,root,root,755)
%doc build-qt5/doc/html/*
%endif
%endif

%if %{with qt6}
%files qt6 -f QtSpell-qt6.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README.md
%attr(755,root,root) %{_libdir}/libqtspell-qt6.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libqtspell-qt6.so.1

%files qt6-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libqtspell-qt6.so
%{_includedir}/QtSpell-qt6
%{_pkgconfigdir}/QtSpell-qt6.pc

%if %{with static_libs}
%files qt6-static
%defattr(644,root,root,755)
%{_libdir}/libqtspell-qt6.a
%endif

%if %{with apidocs}
%files qt6-apidocs
%defattr(644,root,root,755)
%doc build-qt6/doc/html/*
%endif
%endif
