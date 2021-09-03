#!/usr/bin/env python

import sys, os, argparse
from pprint import pprint

parser = argparse.ArgumentParser(description = 'extracthists: extract hists from fileA and put in fileB, with renaming',
                                 usage = '%(prog)s [options] fileA.root fileB.root pathA1 pathB1 [pathA2 pathB2 ...]')

parser.add_argument('positional', nargs='*')

parser.add_argument('-f', '--force', action='store_true',
                    help='Overwrite fileB.root, if it exists.')

options = parser.parse_args()

if len(options.positional) < 4:
    print 'Required args missing, including at least two filenames and two paths\n'
    parser.print_help()
    sys.exit(1)

fnA, fnB = options.positional[:2]

if not os.path.isfile(fnA):
    raise IOError('file %s does not exist' % fnA)
if os.path.isfile(fnB) and not options.force:
    raise IOError('file %s already exists, -f to force' % fnB)

paths = options.positional[2:]

if len(paths) % 2 != 0:
    raise ValueError('paths must come in pairs')

paths = [(paths[i], paths[i+1]) for i in xrange(0, len(paths), 2)]
srcs = [x[0] for x in paths]
dsts = [x[1] for x in paths]
if sorted(set(srcs)) != sorted(srcs) or sorted(set(dsts)) != sorted(dsts):
    raise ValueError('each of srcs and dsts must be separately unique')

print 'copying from', fnA, 'to', fnB, 'these objects:'
maxlen = max(len(src) for src in srcs)
for src, dst in paths:
    print src.ljust(maxlen + 2), '->  ', dst

########################################################################

from DVCode.Tools.ROOTTools import *

fA = ROOT.TFile.Open(fnA)
if not fA.IsOpen():
    raise IOError('could not open input file %s' % fnA)

src_objs = []
for src in srcs:
    obj = fA.Get(src)
    if repr(obj) == '<ROOT.TObject object at 0x(nil)>':
        raise NameError('path "%s" not found in input file' % src)
    src_objs.append(obj)

fB = ROOT.TFile.Open(fnB, 'recreate' if options.force else 'create')
if not fB.IsOpen():
    raise IOError('could not open output file %s' % fnB)

dst_objs = []
for src_obj, dst_path in zip(src_objs, dsts):
    num_slashes = dst_path.count('/')
    if num_slashes:
        if num_slashes > 1:
            raise ValueError('nested directories not supported yet')
        dst_dir, dst_name = os.path.split(dst_path)
        dst_dir_obj = fB.Get(dst_dir)
        if repr(dst_dir_obj) == '<ROOT.TObject object at 0x(nil)>':
            dst_dir_obj = fB.mkdir(dst_dir)
        dst_obj = src_obj.Clone(dst_name)
        dst_obj.SetDirectory(dst_dir_obj)
    else:
        dst_obj = src_obj.Clone(dst_path)
        dst_obj.SetDirectory(fB)
    dst_objs.append(dst_obj)

fB.Write()
fB.Close()
fA.Close()
