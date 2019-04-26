#!/usr/bin/env python

import sys, argparse
from JMTucker.Tools.hadd import hadd

parser = argparse.ArgumentParser(description = 'hadd.py: run hadd wrapper',
                                 usage = '''
%(prog)s output.root file1.root file2.root [file3.root ... fileN.root]
   -or-
%(prog)s -l input_file_list.txt output.root''')

parser.add_argument('positional', nargs='*')

parser.add_argument('-l', '--list',
                    help='File containing list of filenames for input.')

options = parser.parse_args()

output_fn = None
input_files = []

if options.list:
    if len(options.positional) != 1:
        raise ValueError('when doing --list, only one positional argument allowed (the output filename)')
    output_fn = options.positional[0]
    for line in file(options.list):
        line = line.strip()
        if line:
            input_files.append(line)
else:
    if len(options.positional) < 2:
        parser.print_usage()
        sys.exit(1)
    output_fn = options.positional[0]
    input_files = options.positional[1:]

hadd(output_fn, input_files)
