#!/usr/bin/env python
'''Uses the individual CSV files in data/repo_datasets/*.csv to generate a
single combined data file called all_datasets.tsv containing repo, accession,
WoS citations, and GS search results.

>>> len(data_files)
11
'''

import csv
import os
import fnmatch
from process_dataset_list import clean_repo_name

data_files = fnmatch.filter(os.listdir('data/repo_datasets/'), 
                            '*_datasets.csv')

if __name__ == '__main__':
    print 'repo\tid\twos\tgs'
    
    for data_file in data_files:
        path = os.path.join('data/repo_datasets', data_file)
        repo = clean_repo_name(data_file[:-len('_datasets.csv')])
        with open(path) as input_file:
            r = csv.reader(input_file)
            header = next(r)
            
            # find the WoS citation column by looking at the column titles
            wos_cols = [n for n, x in enumerate(header) 
                        if 'wos cited by how many' in x.lower()]
            assert len(wos_cols) == 1
            wos_col = wos_cols[0]
            
            # find the GS search results column by looking at the column titles
            gs_cols = [n for n, x in enumerate(header)
                       if 'results' in x.lower()
                       and ('gs' in x.lower() or 'google' in x.lower()
                            or 'search' in x.lower())]
            try:
                gs_col = gs_cols[0]
            except IndexError:
                gs_col = None
            
            for line in r:
                if len(line) <= 1: continue
                
                try:
                    vals = [repo, line[0]]
                    
                    wos = line[wos_col].split()[0]
                    if not wos.strip(): wos = 0
                    vals.append(wos)
                    
                    if gs_col is None: gs = 0
                    else: 
                        gs = line[gs_col].split()[0]
                        if not gs.strip(): gs = 0
                    vals.append(gs)
                    
                except IndexError:
                    continue
                
                print '\t'.join(map(str, vals))
