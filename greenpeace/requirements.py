import subprocess, sys
from typing import Dict, List

SPECIFIERS = ['===', '==', '@', '>=', '<=', '>', '<', '!=', '~=']


def __try_read_specifier(packages: Dict[str, Dict[str, str]], line: str, specifier: str) -> bool:
    split = line.split(specifier)
    if len(split) >= 2:
        packages[split[0].rstrip()] = { 'specifier': specifier, 'version': str.join(specifier, split[1:]).lstrip() }
        return True
    return False


def read_requirements(lines: List[str]) -> Dict[str, Dict[str, str]]:
    packages = {}
    for line in lines:
        line = line.strip()

        # Skip empty and commented lines
        if line == '' or line.startswith('#'):
            continue
        if '#' in line:
            line = line.split('#')[0].rstrip()
        
        # Try detect any specifier
        find = next((s for s in SPECIFIERS if __try_read_specifier(packages, line, s)), None)
        if find is not None:
            continue
        
        # Try detect another requirements file
        if line.startswith('-r'):
            packages[line[2:].strip()] = {'specifier': '-r', 'version': None}
            continue

        # package without specifier or a particular file
        packages[line] = {'specifier': None, 'version': None}
        
    return packages


def freeze():
    result = subprocess.run([sys.executable, '-m', 'pip', 'freeze'], capture_output=True, text=True)
    return read_requirements(result.stdout.split('\n'))