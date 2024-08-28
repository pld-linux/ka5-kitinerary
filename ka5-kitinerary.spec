#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeappsver	23.08.5
%define		kframever	5.94.0
%define		qtver		5.15.2
%define		kaname		kitinerary
Summary:	KDE Itinerary - digital travel assistent
Summary(pl.UTF-8):	KDE Itinerary - cyfrowy asystent podróży
Name:		ka5-%{kaname}
Version:	23.08.5
Release:	1
License:	GPL v2+/LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/release-service/%{kdeappsver}/src/%{kaname}-%{version}.tar.xz
# Source0-md5:	8b3216199eef85b2f05e4955f3409199
Patch0:		kitinerary-poppler24.patch
URL:		https://community.kde.org/KDE_PIM/KDE_Itinerary
BuildRequires:	Qt5Core-devel >= %{qtver}
BuildRequires:	Qt5Gui-devel
BuildRequires:	Qt5Gui-devel
BuildRequires:	Qt5Network-devel >= 5.11.1
BuildRequires:	Qt5Qml-devel
BuildRequires:	Qt5Test-devel
BuildRequires:	Qt5Test-devel
BuildRequires:	abseil-cpp-devel
BuildRequires:	cmake >= 3.20
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
%patch0 -p1

%build
%cmake \
	-B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DHTML_INSTALL_DIR=%{_kdedocdir} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON

%ninja_build -C build

%if %{with tests}
ctest --test-dir build
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
%{_datadir}/mime/packages/application-vnd-kde-itinerary.xml
%{_datadir}/qlogging-categories5/org_kde_kitinerary.categories
%ghost %{_libdir}/libKPim5Itinerary.so.5
%attr(755,root,root) %{_libdir}/libKPim5Itinerary.so.*.*.*

%files devel
%defattr(644,root,root,755)
%{_includedir}/KPim5/KItinerary
%{_includedir}/KPim5/kitinerary
%{_includedir}/KPim5/kitinerary_version.h
%{_libdir}/cmake/KPim5Itinerary
%{_libdir}/cmake/KPimItinerary
%{_libdir}/libKPim5Itinerary.so
