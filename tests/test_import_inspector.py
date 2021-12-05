import os
from greenpeace.import_inspector import to_package_candidates, get_imports, inspect_imports


def __get_file(name: str) -> str:
    return os.path.join(os.path.dirname(__file__), 'files', name)


def test_get_imports():
    py_file = __get_file('_script.py')
    imports = get_imports(py_file)

    assert imports == set(['math', 'numpy', 'pandas', 'random', 'datetime', 'greenpeace.pypi_server', '_other'])


def test_to_package_candidates():
    candidates = to_package_candidates('numpy')
    assert candidates == ['numpy']

    candidates = to_package_candidates('django.config')
    assert candidates == ['django', 'django.config']

    candidates = to_package_candidates('a.b.c')
    assert candidates == ['a', 'a.b', 'a.b.c']


def test_inspect_imports():
    py_file = __get_file('_script.py')
    packages, modules = inspect_imports(py_file)

    assert packages == ['numpy', 'pandas', 'requests', 'yarg']
    
    assert modules[0]['Name'] == '_other'
    assert modules[0]['RelativePath'] == '_other.py'
    assert modules[0]['AbsolutePath'].endswith('\\tests\\files\\_other.py')
    assert modules[1]['Name'] == 'greenpeace.pypi_server'
    assert modules[1]['RelativePath'] == 'greenpeace\\pypi_server.py'
    assert modules[1]['AbsolutePath'].endswith('\\greenpeace\\pypi_server.py')