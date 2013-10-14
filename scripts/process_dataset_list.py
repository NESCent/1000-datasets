#!/usr/bin/env python
'''This script is used to convert synonyms of repository names into a single
canonical version. Works on tab-delimited files where the first column is the
repository name.'''
import sys
from canonical_repo_names import synonym_dict, bad_names


def clean_repo_name(repo):
    '''
    >>> clean_repo_name('abc')
    >>> clean_repo_name('treebase')
    'TreeBASE'
    '''
    if 'pangaea.de' in repo:
        # these values refer to Pangaea
        repo = 'Pangaea'
    elif repo in bad_names:
        # replace with canonical synonym
        repo = bad_names[repo]
    elif repo in synonym_dict:
        # this is already a canonical synonym
        pass
    else:
        # first value of this line is unrecognizable
        return None
    
    return repo

def clean_line(line):
    '''Return the synonym-replaced version of a single line of text.
    
    >>> clean_line('Array Express\\t1\\t2\\t3')
    'ArrayExpress\\t1\\t2\\t3'
    >>> clean_line('pangaea.de\\t1\\t2')
    'Pangaea\\t1\\t2'
    '''
    repo = line.split('\t')[0]
    rest_of_line = '\t'.join(line.split('\t')[1:])
    
    repo = clean_repo_name(repo)
    if repo is None: return None
    
    return repo + ('\t' + rest_of_line if rest_of_line else '')


if __name__ == '__main__':
    for line in sys.stdin:
        line = clean_line(line)
        if not line is None: sys.stdout.write(line)
