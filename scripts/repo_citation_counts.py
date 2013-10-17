#!/usr/bin/env python
'''Returns the total number of citations per repository.

>>> 1900 <= citation_counts['TreeBASE'] <= 2000
True
>>> 7500 <= citation_counts['GEO'] <= 7700
True
>>> citation_counts['treebase']
0
'''
from collections import defaultdict

citation_counts = defaultdict(lambda: 0)

with open('data/all_datasets.tsv', 'r') as input_file:
    input_file.readline()
    
    for line in input_file:
        line = line.strip()
        if not line or line.startswith('#'): continue
        
        vals = line.split('\t')
        repo, n = vals[0], int(vals[2]) + int(vals[3])
        
        try: n = int(n)
        except ValueError: continue
        
        citation_counts[repo] += n
        
if __name__ == '__main__':
    for key in sorted(citation_counts):
        print key + '\t' + str(citation_counts[key])
