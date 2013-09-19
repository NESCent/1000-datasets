#!/usr/bin/env python
import sys
input_path1 = sys.argv[1]
input_path2 = sys.argv[2]
from collections import defaultdict


totals = {}
with open(input_path1) as input_file:
    for line in input_file:
        if not line.strip(): continue

        repo, dataset, n = line.split('\t')
        try: n = int(n)
        except: n = 0
        if not repo.strip() or not dataset.strip(): continue

        totals[repo, dataset] = n

reuse = defaultdict(lambda: 0)
no_reuse = defaultdict(lambda: 0)
with open(input_path2) as input_file:
    for line in input_file:
        if not line.strip(): continue

        n = int(line[:8])
        line = line[8:].rstrip('\n')
        confidence, reuse_status, repo = line.split('\t')
        if not repo.strip() or not dataset.strip(): continue

        if 'low' in confidence: pass
        elif 'not reused' in reuse_status:
            no_reuse[repo] += n
        elif 'reused' in reuse_status:
            reuse[repo] += n

for repo, dataset in totals:
    # total number of citations for this dataset
    total = totals.get((repo, dataset), 0)
    # output repo, dataset, weighted estimate of reuse citations
    print '\t'.join((repo, dataset)+(str(float(total) * reuse[repo] / no_reuse[repo]),))

'''for repo in reuse:
    print repo, reuse[repo], no_reuse[repo], float(reuse[repo]) / (reuse[repo] + no_reuse[repo])'''