#!/usr/bin/env python
import sys

synonym_dict = {
'ArrayExpress': ['Array Express'],
'TreeBASE': ['TreeBase'],
'ICPSR/IQSS': ['ICPSR', 'IQSS'],
'Journal Archives': ['journalarchives'],
}

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