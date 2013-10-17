#!/usr/bin/env python
'''Returns the total number of datasets per repository.

>>> 160 <= dataset_counts['Journal Archives'] <= 180
True
>>> 100 <= dataset_counts['BMRB'] <= 120
True
>>> dataset_counts['treebase']
0
'''
from collections import defaultdict
from process_dataset_list import clean_repo_name

dataset_counts = defaultdict(lambda: 0)

with open('data/all_datasets.tsv', 'r') as input_file:
    input_file.readline()
    
    for line in input_file:
        line = line.strip()
        if not line or line.startswith('#'): continue
        
        vals = line.split('\t')
        repo, n = vals[0], int(vals[2]) + int(vals[3])
        
        repo = clean_repo_name(repo)
        if repo is None: continue
        
        if n: dataset_counts[repo] += 1
        
if __name__ == '__main__':
    for key in sorted(dataset_counts):
        print key + '\t' + str(dataset_counts[key])
