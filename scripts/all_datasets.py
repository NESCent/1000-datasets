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
import re
from process_dataset_list import clean_repo_name

year_regex = re.compile('[(\[ ]([1-2][0-9]{3})[)\].]')

data_files = fnmatch.filter(os.listdir('data/repo_datasets/'), 
                            '*_datasets.csv')

if __name__ == '__main__':
    print 'repo\tid\twos\tgs\tyear'
    
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
            
            date_cols = [n for n, x in enumerate(header)
                         if 'date' in x.lower() or 'year' in x.lower()]
            try:
                assert len(date_cols) == 1
                date_col = date_cols[0]
            except AssertionError:
                if len(date_cols) > 1:
                    print repo, date_cols
                    raise Exception("Couldn't find date column (%s, %s)" % (repo, date_cols))
                else:
                    # if there's not a date column, try to parse it out of each 
                    # line with regular expressions
                    date_col = None
            
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

                    if date_col is None:
                        years = set(year_regex.findall(','.join(line)))
                        try:
                            assert len(years)>0
                            date = min(years)
                        except AssertionError:
                            date = ''
                    else:
                        date = line[date_col]

                    vals.append(date)
                    
                except IndexError:
                    continue
                
                print '\t'.join(map(str, vals))
