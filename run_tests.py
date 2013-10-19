import doctest
import os
import fnmatch
import importlib


# run doctest unit tests in all source Python scripts
failures = 0
scripts = [x for x in os.listdir('scripts') if x.endswith('.py')]
for script in scripts:
    script = (os.path.relpath(script)[:-len('.py')]).replace('/', '.')
    print '** testing', script, '**'
    mod = importlib.import_module('scripts.' + script)
    result = doctest.testmod(mod, verbose=True)
    failures += result.failed

doctest.testfile('README.md', verbose=True)

print
if failures > 0: raise Exception('** %s tests failed. **' % failures)
else: print '** All tests passed. **'
