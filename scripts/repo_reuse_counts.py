#!/usr/bin/env python
'''Determines the number of citations within the subsample that were considered
to have been instances of reuse with high confidence.

>>> test = {'HEPData': 154, 'ArrayExpress': 157, 'GEOROC': 170, 'Pangaea': 160, 'ICPSR': 85, 'Journal Archives': 168, 'IQSS': 95, 'TreeBASE': 164, 'GEO': 162, 'PDB': 157, 'BMRB': 211}
>>> test_sorted = sorted(candidate_counts.items(), key=lambda (a,b): b)
>>> data_sorted = sorted(candidate_counts.items(), key=lambda (a,b): b)
>>> [x[0] for x in data_sorted]
['ICPSR', 'IQSS', 'HEPData', 'ArrayExpress', 'PDB', 'Pangaea', 'GEO', 'TreeBase', 'journalarchives', 'GEOROC', 'BMRB']
>>> abs(data_sorted[0][1] - test_sorted[0][1]) < 20
True
>>> abs(data_sorted[-1][1] - test_sorted[-1][1]) < 20
True
'''
from collections import defaultdict
from process_dataset_list import clean_repo_name

reuse_counts = defaultdict(lambda: 0)
candidate_counts = defaultdict(lambda: 0)

with open('data/reuse_subsample') as input_file:
    for line in input_file:
        line = line.rstrip()
        if not line or line.startswith('#'): continue
        
        n = int(line[:8])
        line = line[8:].rstrip('\n')
        confidence, reuse_status, repo = line.split('\t')
        repo = clean_repo_name(repo)
        if repo is None: continue
        
        if 'low' in confidence:
            pass
        elif 'not reused' in reuse_status:
            pass
        elif 'reused' in reuse_status:
            reuse_counts[repo] += n
        
        candidate_counts[repo] += n
        
if __name__ == '__main__':
    for key in sorted(reuse_counts):
        print key + '\t' + str(reuse_counts[key]) + '\t' + str(candidate_counts[key])
