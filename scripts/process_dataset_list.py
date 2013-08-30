#!/usr/bin/env python
import sys
from canonical_repo_names import synonym_dict

for line in sys.stdin:
    archive = line.split('\t')[0]
    if 'pangaea.de' in archive:
        line = 'Pangaea\t' + '\t'.join(line.split('\t')[1:])
    elif not archive in synonym_dict: continue
    sys.stdout.write(line)
