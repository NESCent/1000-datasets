#!/usr/bin/env python
'''Quick script to convert text to title case.'''

def title_case(text):
    '''Returns the input text converted to title case.
    
    >>> title_case('abc')
    'Abc'
    >>> title_case('apple banana')
    'Apple Banana'
    '''
    return text.title()


if __name__ == '__main__':
    import sys
    print title_case(sys.stdin.read()),
