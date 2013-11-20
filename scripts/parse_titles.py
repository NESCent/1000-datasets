#!/usr/bin/env python

import re
separator = re.compile("(\. |\.\,|, (?=[A-Z])|; (?=[A-Z]))")

def main():
    import sys
    input = sys.stdin
    for line in input:
        # file is repo [tab] accession [tab] reference
        vals = line.split('\t')
        repo, accession = vals[:2]
        ref = '\t'.join(vals[2:]).strip().replace('\n', '').replace('\r', '')
        # split on various combinations of punctuation/spaces/capital letters 
        # that seem to frequently delineate the title
        chunks = separator.split(ref)
        # the title is probably the longest chunk after splitting this way
        title = sorted(chunks, key=lambda k: len(k), reverse=True)[0]
        print '\t'.join((repo, accession, title))

if __name__ == '__main__':
    main()