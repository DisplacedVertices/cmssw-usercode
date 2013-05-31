#!/usr/bin/env python

import optparse, sys
from JMTucker.Tools.ROOTTools import *

parser = optparse.OptionParser(usage='%prog [options] file1.root file2.root dir_path plot_path')
parser.add_option('--per-page', type=int, default=-1,
                  help='Put PER_PAGE plots per html page (default all on one page).')
parser.add_option('--size', nargs=2, type=int, default=(600,600), metavar=('SIZEX','SIZEY'),
                  help='Set the plot size to SIZEX x SIZEY (default %(default)s.')
parser.add_option('--nice1', default='file1',
                  help='Nice name for file #1 (default is %(default)s).')
parser.add_option('--nice2', default='file2',
                  help='Nice name for file #2 (default is %(default)s).')
parser.add_option('--color1', default='ROOT.kRed',
                  help='Color #1: may be a python snippet, e.g. ROOT.kRed (which is the default).')
parser.add_option('--color2', default='ROOT.kBlue',
                  help='Color #1: may be a python snippet, e.g. ROOT.kBlue (which is the default).')
parser.add_option('--no-stats', default='False',
                  help='Snippet for no_stats lambda, which takes name, hist1, hist2 as args (default is %(default)s).')
parser.add_option('--apply-commands', default='None',
                  help='Snippet for apply_commands lambda, which takes name, hist1, hist2 as args (default is %(default)s).')
options, args = parser.parse_args()

if len(args) < 4:
    print 'Required args missing:\n'
    parser.print_help()
    sys.exit(1)
    
options.file1, options.file2, options.dir_path, options.plot_path = args
options.color1 = eval(options.color1)
options.color2 = eval(options.color2)
_lambda = 'lambda name, hist1, hist2: '
options.no_stats       = eval(_lambda + options.no_stats)
options.apply_commands = eval(_lambda + options.apply_commands)

#print options ; print args ; import sys ; print sys.argv ; raise 1

########################################################################

set_style()
ps = plot_saver(options.plot_path, size=options.size, per_page=options.per_page)

f_1 = ROOT.TFile(options.file1)
f_2 = ROOT.TFile(options.file2)

compare_all_hists(ps,
                  options.nice1, f_1.Get(options.dir_path), options.color1,
                  options.nice2, f_2.Get(options.dir_path), options.color2,
                  no_stats = options.no_stats,
                  apply_commands = options.apply_commands
                  )
