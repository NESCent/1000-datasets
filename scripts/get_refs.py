#!/usr/bin/env python
'''This script pulls out valid bibliographic references from the data
spreadsheet, which could be in several columns (or sometimes missing).

Outputs three tab-separated columns with repo, accession, and reference,
with one dataset per line.'''

import sys

def main(file_path):
    with open(file_path) as input_file:
        input_file.readline()
        for line in input_file:
            if not line.strip(): continue
            vals = line.split('\t')
            repo = vals[1]
            accession = vals[2]
            longest = sorted(vals, key=lambda k: len(k), reverse=True)[0].replace('\n', '').replace('\r', '')
            if longest.startswith('http'): continue
            if len(longest) < 100: continue
            print '\t'.join((repo, accession, longest))

if __name__ == '__main__':
    try: file_path = sys.argv[1]
    except IndexError: file_path = 'data/old_all_datasets.tsv'
    
    main(file_path)