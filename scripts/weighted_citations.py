#!/usr/bin/env python
''' 
This script is used to estimate the number of citations that were actual
instances of data reuse. This is estimated based on a subsample of citations
which have been manually evaluated.

Necessary input files:
    data/citation_distribution
        Total number of citations per dataset, one dataset per line.
        Includes 3 tab-separated columns:
            repository,accession,number of citations
            
    data/reuse_subsample
        For each repository, this gives the number of manually-verified
        citations with each reuse status (reused, not reused, ambiguous, etc.)
        
        
Outputs to stdout, which is captured and saved as data/reuse_estimates.
'''

if __name__ == '__main__':
    import sys
    from collections import defaultdict
    from process_dataset_list import clean_repo_name
    
    totals = {'wos': {}, 'gs': {}}
    datasets = set()
    with open('data/all_datasets.tsv') as input_file:
        input_file.readline()
        for line in input_file:
            if not line.strip(): continue
            
            repo, dataset, wos, gs = line.split('\t')
            repo = clean_repo_name(repo)
            if repo is None or not dataset.strip(): continue
            
            wos, gs = int(wos), int(gs)
            
            datasets.add((repo,dataset))
            totals['wos'][repo, dataset] = wos
            totals['gs'][repo, dataset] = gs
    
    reuse = {key: defaultdict(lambda: 0) for key in ('wos', 'gs')}
    no_reuse = {key: defaultdict(lambda: 0) for key in ('wos', 'gs')}
    for key in ('wos', 'gs'):
        with open('data/reuse_subsample_%s' % key) as input_file:
            for line in input_file:
                if not line.strip(): continue
                
                n = int(line[:8])
                line = line[8:].rstrip('\n')
                confidence, reuse_status, repo = line.split('\t')
                repo = clean_repo_name(repo)
                if repo is None or not dataset.strip(): continue
                
                if 'low' in confidence: pass
                elif 'not reused' in reuse_status:
                    no_reuse[key][repo] += n
                elif 'reused' in reuse_status:
                    reuse[key][repo] += n
            
    for repo, dataset in datasets:
        # total number of citations for this dataset
        total = 0
        for key in ('wos', 'gs'):
            n = totals[key].get((repo, dataset), 0)
            try: weight = reuse[key][repo] / float(reuse[key][repo] + no_reuse[key][repo])
            except: weight = 0
            total += n * weight
            
        # output repo, dataset, weighted estimate of reuse citations
        print '\t'.join(map(str, (repo, dataset, total)))
        
    
    for repo in reuse['wos']:
        print '#', repo, [(reuse[key][repo], no_reuse[key][repo], 
                           float(reuse[key][repo]) / 
                                 max(1, (reuse[key][repo] + no_reuse[key][repo]))) 
                          for key in ('wos', 'gs')]
