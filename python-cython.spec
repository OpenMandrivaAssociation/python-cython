# Python module not linking to libpython
%global _disable_ld_no_undefined 1

%bcond_with	check
%define tarname cython

%global optflags %optflags -O3

Summary:	Language for writing C extensions to Python
Name:		python-cython
Version:	3.2.1
Release:	1
License:	Python
Group:		Development/Python
Url:		https://www.cython.org
Source0:	https://github.com/cython/cython/archive/%{version}/cython-%{version}.tar.gz
Source1:	%{name}.rpmlintrc
Patch0:		cython-0.29.28-missing-header.patch
BuildRequires:	dos2unix
BuildRequires:	pkgconfig(python)
BuildRequires:	python-setuptools
%if %{with check}
BuildRequires:	gdb
BuildRequires:	gomp-devel
BuildRequires:	python-numpy-devel
%endif
%rename python3-cython

%description
Cython is a language that facilitates the writing of C extensions for
the Python language. It is based on Pyrex, but provides more cutting
edge functionality and optimizations.

%prep
%autosetup -p1 -n %{tarname}-%{version}

find -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python}|'

%build
%setup_compile_flags
CFLAGS="%{optflags}" python setup.py build

%install
python setup.py install -O1 --skip-build --root %{buildroot}
rm -rf %{buildroot}%{python_sitelib}/setuptools/tests
rm -rf %{buildroot}/%{python_sitearch}/__pycache__/

%if %{with check}
%check
python runtests.py
%endif

%files 
%{_bindir}/cython
%{_bindir}/cythonize
%{_bindir}/cygdb
%{py_platsitedir}/Cython
%{py_platsitedir}/Cython-%{version}-*.egg-info
%{py_platsitedir}/cython*
%{py_platsitedir}/pyximport
#{py_platsitedir}/__pycache__/*.py?
