Name:		python3-distutils-pytest
Version:	0.1
Release:        1
Summary:	Call pytest from a distutils setup.py script
License:	Apache-2.0
Group:		Development/Languages/Python
Source:         distutils-pytest-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python3-devel
Requires:	python3-pytest
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

%description
This Python module adds test to the commands in the distutils package.


%prep
%setup -q -n distutils-pytest-%{version}


%build
python3 setup.py build


%install
python3 setup.py install --optimize=1 --prefix=%{_prefix} --root=%{buildroot}


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root)
%doc README.rst
%{python3_sitelib}/*
