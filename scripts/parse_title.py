#!/usr/bin/env python

import re
separator = re.compile("(\. |\.\,|, (?=[A-Z]))")

def main():
    import sys
    input = sys.stdin
    for line in input:
        vals = line.split('\t')
        repo, accession = vals[:2]
        ref = '\t'.join(vals[2:]).strip().replace('\n', '').replace('\r', '')
        chunks = separator.split(ref)
        title = sorted(chunks, key=lambda k: len(k), reverse=True)[0]
        print repo, accession, title

if __name__ == '__main__':
    main()