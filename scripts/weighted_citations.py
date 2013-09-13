#!/usr/bin/env python
import sys
input_path1 = sys.argv[1]
input_path2 = sys.argv[2]


totals = {}
with open(input_path1) as input_file:
    for line in input_file:
        if not line.strip(): continue

        repo, dataset, n = line.split('\t')
        try: n = int(n)
        except: n = 0
        if not repo.strip() or not dataset.strip(): continue

        totals[repo, dataset] = n

reuse = {}
no_reuse = {}
with open(input_path2) as input_file:
    for line in input_file:
        if not line.strip(): continue

        n = int(line[:8])
        line = line[8:].rstrip('\n')
        reuse_status, repo, dataset = line.split('\t')
        if not repo.strip() or not dataset.strip(): continue

        collection = None
        if 'not reused' in reuse_status:
            collection = no_reuse
        elif 'reused' in reuse_status:
            collection = reuse
        if not collection is None:
            if not (repo, dataset) in collection:
                collection[(repo, dataset)] = 0
            collection[(repo, dataset)] += n

all_datasets = set.union(set(reuse.keys()), set(no_reuse.keys()), set(totals.keys()))
for dataset in all_datasets:
    # total number of citations for this dataset
    total = totals.get(dataset, 0)
    # number of subset that were marked as reuse
    n = reuse.get(dataset, 0)
    # total size of subset
    subset = n + no_reuse.get(dataset, 0)
    if subset == 0: freq = 1
    else: freq = float(n)/subset
    n = max(n, subset)
    # output repo, dataset, weighted estimate of reuse citations
    print '\t'.join(dataset+(str(n * freq),))
