#!/usr/bin/env python
import csv
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def print_cleaned_data(file_handle):
    r = csv.reader(file_handle)
    for line in r:
        print '\t'.join(line)


if __name__ == '__main__':
    try: path = sys.argv[1]
    except: path = 'data/all_clean.csv'
    
    with open(path) as input_file:
        print_cleaned_data(input_file)
