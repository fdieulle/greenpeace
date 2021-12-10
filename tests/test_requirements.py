from typing import Dict
import greenpeace as gp
import os


def __get_file(name: str) -> str:
    return os.path.join(os.path.dirname(__file__), 'files', name)


def __check_package(packages: Dict[str, Dict[str, str]], name, specifier, version):
    assert name in packages
    assert packages[name]['specifier'] == specifier
    assert packages[name]['version'] == version


def test_read_requirements():
    r_file = __get_file('requirements.txt')
    with open(r_file, mode='r') as f:
        lines = f.readlines()
    
    packages = gp.read_requirements(lines)

    # Requirements without Version Specifiers
    __check_package(packages, 'pytest', specifier=None, version=None)
    __check_package(packages, 'pytest-cov', specifier=None, version=None)
    __check_package(packages, 'beautifulsoup4', specifier=None, version=None)

    # Requirements with Version Specifiers
    __check_package(packages, 'docopt', specifier='==', version='0.6.1')
    __check_package(packages, 'keyring', specifier='>=', version='4.1.1')
    __check_package(packages, 'coverage', specifier='!=', version='3.5')
    __check_package(packages, 'Mopidy-Dirble', specifier='~=', version='1.1')
    __check_package(packages, 'pythonnet', specifier='@', version='git+https://github.com/pythonnet/pythonnet@09ecf1b22b9d51691c3da96eb70bf9a615bddb43')
    __check_package(packages, 'numpy', specifier='>', version='1.20.0')
    __check_package(packages, 'treebuilder', specifier='===', version='1.20.0')
    __check_package(packages, 'yarg', specifier='<', version='1.0.0')
    __check_package(packages, 'requests', specifier='<=', version='2.0.0')

    # Refer to other requirements files
    __check_package(packages, 'other-requirements.txt', specifier='-r', version=None)

    # A particular file
    __check_package(packages, './downloads/numpy-1.9.2-cp34-none-win32.whl', specifier=None, version=None)
    __check_package(packages, 'http://wxpython.org/Phoenix/snapshot-builds/wxPython_Phoenix-3.0.3.dev1820+49a8884-cp34-none-win_amd64.whl', specifier=None, version=None)

    # Additional Requirements without Version Specifiers
    __check_package(packages, 'rejected', specifier=None, version=None)
    __check_package(packages, 'green', specifier=None, version=None)


def test_freeze():
    packages = gp.freeze()

    assert 'pytest' in packages

