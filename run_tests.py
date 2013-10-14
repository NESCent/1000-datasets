import doctest
import os
import fnmatch
import importlib


def locate(pattern, root=os.curdir):
    '''Locate all files matching supplied filename pattern in and below
    supplied root directory.'''
    for path, dirs, files in os.walk(os.path.abspath(root)):
        for filename in fnmatch.filter(files, pattern):
            yield os.path.join(path, filename)

# run doctest unit tests in all source Python scripts
failures = 0
scripts = [x for x in locate('*.py', root='.')]
for script in scripts:
    script = (os.path.relpath(script)[:-len('.py')]).replace('/', '.')
    print '** testing', script, '**'
    mod = importlib.import_module(script)
    result = doctest.testmod(mod, verbose=True)
    failures += result.failed

doctest.testfile('README.md', verbose=True)

print
if failures > 0: raise Exception('** %s tests failed. **' % failures)
else: print '** All tests passed. **'
