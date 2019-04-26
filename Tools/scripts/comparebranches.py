#!/usr/bin/env python

import os, sys, argparse

parser = argparse.ArgumentParser(description = 'comparebranches: compare the branches present in two files',
                                 usage = '%(prog)s [options] file1.root file2.root')

parser.add_argument('positional', nargs='*', help='The .root files.')

parser.add_argument('--show-common', default=False,
                    help='Write the list of branches the two have in common.')
parser.add_argument('--ignore-process-names', action='store_true',
                    help='Ignore the process names (e.g. HLT, HLT2) when comparing the branch lists.')

options = parser.parse_args()

if len(options.positional) != 2:
    print 'Required positional args missing: two filenames\n'
    parser.print_help()
    sys.exit(1)

########################################################################

fn1, fn2 = options.positional

def get(fn):
    ret = []
    for line in os.popen('edmDumpEventContent --name %s' % fn):
        line = line.strip()
        if '_' in line:
            if options.ignore_process_names:
                line = '_'.join(line.split('_')[:3])
            ret.append(line)
    return set(ret)

branches1 = get(fn1)
branches2 = get(fn2)

print 'fn1:', fn1
print 'fn2:', fn2
if options.show_common:
    print
    print 'branches in common:'
    for b in sorted(branches1 & branches2):
        print b
print
print 'in fn1 but not fn2'
for b in sorted(branches1 - branches2):
    print b
print
print 'in fn2 but not fn1'
for b in sorted(branches2 - branches1):
    print b
