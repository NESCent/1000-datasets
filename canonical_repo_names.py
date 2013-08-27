#!/usr/bin/env python
import sys

synonym_dict = {
'ArrayExpress': ['Array Express'],
'GEO': ['GEOROC'],
'TreeBASE': ['TreeBase'],
}

for line in sys.stdin:
    for canonical_name, synonyms in synonym_dict.items():
        for synonym in synonyms:
            line = line.replace(synonym, canonical_name)
    sys.stdout.write(line)