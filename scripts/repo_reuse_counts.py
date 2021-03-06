#!/usr/bin/env python
'''Determines the number of citations within the subsample that were considered
to have been instances of reuse with high confidence.

>>> test = {'HEPData': 154, 'ArrayExpress': 157, 'GEOROC': 170, 'Pangaea': 160, 'ICPSR/IQSS': 180, 'Journal Archives': 168, 'TreeBASE': 164, 'GEO': 162, 'PDB': 157, 'BMRB': 211}
>>> test_sorted = sorted(test.items(), key=lambda (a,b): b)
>>> data_sorted = sorted(candidate_counts['wos'].items(), key=lambda (a,b): b)
'''
from collections import defaultdict
from process_dataset_list import clean_repo_name
import re

count_re = re.compile('^ *[0-9]+ ')

keys = ('wos', 'gs')
reuse_counts = {key:defaultdict(lambda: 0) for key in keys}
candidate_counts = {key:defaultdict(lambda: 0) for key in keys}

for key in keys:
    with open('data/reuse_subsample_%s' % key) as input_file:
        for line in input_file:
            line = line.rstrip()
            if not line or line.startswith('#'): continue

            try:            
                count = count_re.findall(line)[0]
            except IndexError:
                raise Exception("Invalid input. reuse_subsample_%s should contain output from uniq -c." % key)
            n = int(count)
            line = line[len(count):].rstrip('\n')
            confidence, reuse_status, repo = line.split('\t')
            if not reuse_status: continue
            repo = clean_repo_name(repo)
            if repo is None: continue
            
            if 'low' in confidence:
                pass
            elif 'not reused' in reuse_status:
                pass
            elif 'reused' in reuse_status:
                reuse_counts[key][repo] += n
            
            candidate_counts[key][repo] += n
        
if __name__ == '__main__':
    for key in keys:
        for repo in sorted(reuse_counts):
            print key + '\t' + repo + '\t' + str(reuse_counts[key][repo]) + '\t' + str(candidate_counts[key][repo])
