#!/usr/bin/env python
import sys

synonym_dict = {
'ArrayExpress': ['Array Express'],
'TreeBASE': ['TreeBase'],
'ICPSR/IQSS': ['ICPSR', 'IQSS'],
'Journal Archives': ['journalarchives', 'JournalArchive'],
'BMRB': [],
'GEO': [],
'GEOROC': [],
'HEPData': [],
'Pangaea': [],
'PDB': [],
}

# create a dictionary linking bad names to canonical ones
bad_names = {}
for k, v in synonym_dict.items():
    bad_names[k.lower()] = k
    for i in v:
        bad_names[i] = k
        bad_names[i.lower()] = k

# colors for use in figures
colors = {
'ArrayExpress': 'blue',
'TreeBASE': 'cyan',
'ICPSR/IQSS': 'red',
'Journal Archives': 'black',
'BMRB': 'purple',
'GEO': 'silver',
'GEOROC': 'yellow',
'HEPData': 'green',
'Pangaea': 'brown',
'PDB': 'orange',
}

if __name__ == '__main__':
    for line in sys.stdin:
        for canonical_name, synonyms in synonym_dict.items():
            potential_replacements = ((synonym, canonical_name)
                                      for synonym in synonyms
                                      if synonym in line)

            try:
                replacement = potential_replacements.next()
                line = line.replace(*replacement)
            except StopIteration: pass
    
        sys.stdout.write(line)
