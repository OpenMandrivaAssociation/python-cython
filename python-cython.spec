%bcond_without	python2
%bcond_with	check
%define tarname Cython
%define py2dir	python2

Summary:	Language for writing C extensions to Python
Name:		python-cython
Version:	0.29.2
Release:	1
License:	Python
Group:		Development/Python
Url:		http://www.cython.org
Source0:	https://pypi.io/packages/source/C/Cython/Cython-%{version}.tar.gz
Source1:	%{name}.rpmlintrc
BuildRequires:	dos2unix
BuildRequires:	pkgconfig(python3)
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

%if %{with python2}
%package -n python2-cython
Summary:	Language for writing C extensions to Python
Group:		Development/Python
BuildRequires:	pkgconfig(python2)
BuildRequires:	python2-setuptools
%description -n python2-cython
Cython is a language that facilitates the writing of C extensions for
the Python language. It is based on Pyrex, but provides more cutting
edge functionality and optimizations.
%endif

%prep
%setup -qn %{tarname}-%{version}
%if %{with python2}
rm -rf %{py2dir}
mkdir %{py2dir}
tar -xvf %{SOURCE0} -C %{py2dir}
find %{py2dir} -name '*.py' | xargs sed -i '1s|^#!python|#!python2|'
%endif # with_python2

find -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python}|'

%build 
CFLAGS="%{optflags}" %py_build
%if %{with python2}
pushd %{py2dir}/%{tarname}-%{version}
CFLAGS="%{optflags}" python2 setup.py build
popd
%endif # with_python2

%install
# Must do the python2 install first because the scripts in /usr/bin are
# overwritten with every setup.py install (and we want the python3 version
# to be the default).
%if %{with python2}
pushd %{py2dir}/%{tarname}-%{version}
python2 setup.py install --skip-build --root %{buildroot}
mv %{buildroot}/usr/bin/cython %{buildroot}/usr/bin/cython2
mv %{buildroot}/usr/bin/cygdb %{buildroot}/usr/bin/cygdb2
rm -rf %{buildroot}%{py_puresitedir}/setuptools/tests
popd
%endif

python setup.py install -O1 --skip-build --root %{buildroot}
rm -rf %{buildroot}%{py_puresitedir}/setuptools/tests
rm -rf %{buildroot}/%{py_platsitedir}/__pycache__/

%if %{with check}
%check
python runtests.py
%if %{with python2}
pushd %{py2dir}/%{tarname}-%{version}
python2 setup.py test
popd
%endif # with_python2
%endif

%files 
%{_bindir}/cython
%{_bindir}/cythonize
%{_bindir}/cygdb
%{py_platsitedir}/Cython
%{py_platsitedir}/Cython-%{version}-*.egg-info
%{py_platsitedir}/cython*
%{py_platsitedir}/pyximport
%{py_platsitedir}/__pycache__/*.py?

%if %{with python2}
%files -n python2-cython
%{_bindir}/cython2
%{_bindir}/cygdb2
%{py2_platsitedir}/Cython
%{py2_platsitedir}/Cython-%{version}-*.egg-info
%{py2_platsitedir}/cython*
%{py2_platsitedir}/pyximport
%endif
