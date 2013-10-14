#!/usr/bin/env python
'''Returns the total number of citations per repository.

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
