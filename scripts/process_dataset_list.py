#!/usr/bin/env python
'''This script is used to convert synonyms of repository names into a single
canonical version. Works on tab-delimited files where the first column is the
repository name.'''
import sys
from canonical_repo_names import bad_names

def processed_line(line):
    '''Return the synonym-replaced version of a single line of text.
    
    >>> processed_line('Array Express\\t1\\t2\\t3')
    'ArrayExpress\\t1\\t2\\t3'
    >>> processed_line('pangaea.de\\t1\\t2')
    'Pangaea\\t1\\t2'
    '''
    repo = line.split('\t')[0]
    rest_of_line = '\t'.join(line.split('\t')[1:])
    if 'pangaea.de' in repo:
        line = 'Pangaea\t' + rest_of_line
    elif repo in bad_names:
        line = bad_names[repo] + '\t' + rest_of_line
    return line


if __name__ == '__main__':
    for line in sys.stdin:
        line = processed_line(line)
        if not line is None: sys.stdout.write(line)
