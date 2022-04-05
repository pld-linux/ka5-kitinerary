#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeappsver	21.12.3
%define		kframever	5.56.0
%define		qtver		5.10.0
%define		kaname		kitinerary
Summary:	KDE Itinerary - digital travel assistent
Summary(pl.UTF-8):	KDE Itinerary - cyfrowy asystent podróży
Name:		ka5-%{kaname}
Version:	21.12.3
Release:	1
License:	GPL v2+/LGPL v2.1+
Group:		X11/Libraries
Source0:	http://download.kde.org/stable/release-service/%{kdeappsver}/src/%{kaname}-%{version}.tar.xz
# Source0-md5:	446c1eed5e43a87a267831ec0b27f85c
Patch0:		poppler-0.82.patch
Patch1:		poppler-0.83.patch
URL:		https://community.kde.org/KDE_PIM/KDE_Itinerary
BuildRequires:	Qt5Core-devel >= %{qtver}
BuildRequires:	Qt5Gui-devel
BuildRequires:	Qt5Gui-devel
BuildRequires:	Qt5Network-devel >= 5.11.1
BuildRequires:	Qt5Qml-devel
BuildRequires:	Qt5Test-devel
BuildRequires:	Qt5Test-devel
BuildRequires:	cmake >= 3.5
BuildRequires:	gettext-devel
BuildRequires:	ka5-kmime-devel >= %{kdeappsver}
BuildRequires:	ka5-kpkpass-devel >= %{kdeappsver}
BuildRequires:	kf5-extra-cmake-modules >= %{kframever}
BuildRequires:	kf5-karchive-devel >= %{kframever}
BuildRequires:	kf5-kcalendarcore-devel >= %{kframever}
BuildRequires:	kf5-kcontacts-devel >= %{kframever}
BuildRequires:	kf5-ki18n-devel >= %{kframever}
BuildRequires:	libphonenumber-devel
BuildRequires:	libstdc++-devel >= 6:5
BuildRequires:	libxml2-devel >= 2
BuildRequires:	ninja
BuildRequires:	poppler-devel
BuildRequires:	qt5-build >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.605
BuildRequires:	shared-mime-info
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRequires:	zlib-devel
BuildRequires:	zxing-cpp-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Kitinerary is a library which provides a data model and a system to
extract information from travel reservations.

%description -l pl.UTF-8
Kitinerary to biblioteka dostarczająca model danych oraz system do
wydobywania informacji z rezerwacji podróżnych.

%package devel
Summary:	Header files for %{kaname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kaname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for %{kaname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kaname}.

%prep
%setup -q -n %{kaname}-%{version}

%build
install -d build
cd build
%cmake \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DHTML_INSTALL_DIR=%{_kdedocdir} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	..
%ninja_build

%if %{with tests}
ctest
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%find_lang %{kaname} --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{kaname}.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_libexecdir}/kf5/kitinerary-extractor
%attr(755,root,root) %{_libdir}/libKPimItinerary.so.*.*.*
%ghost %{_libdir}/libKPimItinerary.so.5
%{_datadir}/mime/packages/application-vnd-kde-itinerary.xml
%{_datadir}/qlogging-categories5/org_kde_kitinerary.categories

%files devel
%defattr(644,root,root,755)
%{_libdir}/libKPimItinerary.so
%{_includedir}/KPim/KItinerary
%{_includedir}/KPim/kitinerary
%{_includedir}/KPim/kitinerary_version.h
%{_libdir}/cmake/KPimItinerary
