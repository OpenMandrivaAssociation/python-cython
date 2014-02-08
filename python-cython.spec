%bcond_without	python3
%bcond_without	check
%define tarname Cython
%define py3dir	python3

Summary:	Language for writing C extensions to Python
Name:		python-cython
Version:	0.19.1
Release:	2
Source0:	http://www.cython.org/release/%{tarname}-%{version}.tar.gz
License:	Apache License
Group:		Development/Python
Url:		http://www.cython.org
BuildRequires:	python-devel
BuildRequires:	dos2unix
%if %{with check}
BuildRequires:	gdb
BuildRequires:	gomp-devel
BuildRequires:	python-numpy-devel
%endif

%description
Cython is a language that facilitates the writing of C extensions for
the Python language. It is based on Pyrex, but provides more cutting
edge functionality and optimizations.

%if %{with python3}
%package -n python3-cython
Summary:    Language for writing C extensions to Python
Group:      Development/Python
BuildRequires:  python3-devel

%description -n python3-cython
Cython is a language that facilitates the writing of C extensions for
the Python language. It is based on Pyrex, but provides more cutting
edge functionality and optimizations.
%endif

%prep
%setup -q -n %{tarname}-%{version}
%if %{with python3}
rm -rf %{py3dir}
mkdir %{py3dir}
tar -xvf %{SOURCE0} -C %{py3dir}
find %{py3dir} -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python3}|'
%endif # with_python3

find -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python}|'

%build 
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build
%if %{with python3}
pushd %{py3dir}/%{tarname}-%{version}
CFLAGS="$RPM_OPT_FLAGS" %{__python3} setup.py build
popd
%endif # with_python3

%install
# Must do the python3 install first because the scripts in /usr/bin are
# overwritten with every setup.py install (and we want the python2 version
# to be the default for now).
%if %{with python3}
pushd %{py3dir}/%{tarname}-%{version}
%{__python3} setup.py install --skip-build --root %{buildroot}
mv %{buildroot}/usr/bin/cython %{buildroot}/usr/bin/cython3
mv %{buildroot}/usr/bin/cygdb %{buildroot}/usr/bin/cygdb3
rm -rf %{buildroot}%{python3_sitelib}/setuptools/tests
popd
%endif

%{__python} setup.py install -O1 --skip-build --root %{buildroot}
rm -rf %{buildroot}%{python_sitelib}/setuptools/tests
rm -rf %{buildroot}/%python3_sitearch/__pycache__/

%if %{with check}
%check
CFLAGS="%{optflags}" \
CXXFLAGS="%{optflags}" \
LDFLAGS="%{ldflags} -lm" \
%{__python} runtests.py
%if %{with python3}
pushd %{py3dir}/%{tarname}-%{version}
CFLAGS="%{optflags}" \
CXXFLAGS="%{optflags}" \
LDFLAGS="%{ldflags} -lm" \
%{__python3} runtests.py
popd
%endif # with_python3
%endif

%files 
%_bindir/cython
%_bindir/cygdb
%py_platsitedir/Cython*
%py_platsitedir/cython*
%py_platsitedir/pyximport*

%files -n python3-cython
%_bindir/cython3
%_bindir/cygdb3
%py3_platsitedir/Cython*
%py3_platsitedir/cython*
%py3_platsitedir/pyximport*
