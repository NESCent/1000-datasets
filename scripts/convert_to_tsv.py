#!/usr/bin/env python
import csv
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


try: path = sys.argv[1]
except: path = 'all_clean.csv'

with open(path) as input_file:
    r = csv.reader(input_file)
    for line in r:
        print '\t'.join(line)