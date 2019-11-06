#!/usr/bin/env python

import sys, argparse
from pprint import pprint

parser = argparse.ArgumentParser(description = 'comparehists: compare all histograms in multiple files or multiple directories',
                                 usage = '%(prog)s [options] file1.root [file2.root ... fileN.root] dir1_path [dir2_path ... dirN_path] plot_path')

parser.add_argument('positional', nargs='*')

parser.add_argument('--recurse', action='store_true',
                    help='Recurse down the directory structure, i.e. use all histograms in the given directory and all subdirectories.')
parser.add_argument('--sort-names', action='store_true',
                    help='Process the histograms in alphabetical order (default is to use the order found in the ROOT directory).')
parser.add_argument('--show-progress', type=int, default=10,
                    help='Print how far along we are processing the histograms: if this is 10 (default), a line is printed for every 1/10 chunk. Disable with value <= 0.')
parser.add_argument('--only-n-first', type=int, default=-1,
                    help='Only do the first ONLY_N_FIRST histograms (default: do all).')
parser.add_argument('--raise-on-incompatibility', action='store_true',
                    help='If histograms are not comparable (e.g. different binning), raise an exception if True, else skip that one (default).')
parser.add_argument('--per-page', type=int, default=100,
                    help='Put PER_PAGE histograms per html page (default: 100 per page).')
parser.add_argument('--opt-stat', type=int, default=1112211,
                    help='The value for SetOptStat (default: %(default)s).')
parser.add_argument('--size', nargs=2, type=int, default=(600,600), metavar='SIZE',
                    help='Set the plot size to SIZEX x SIZEY (default %(default)s.')
parser.add_argument('--ps-args', default='',
                    help='Other args for plot_saver.')
parser.add_argument('--nice', nargs='+', default=[],
                    help='Nice names for the files (default is file1, file2, ...).')
parser.add_argument('--colors', nargs='+', default=['ROOT.kRed', 'ROOT.kBlue', 'ROOT.kGreen+2', 'ROOT.kMagenta', 'ROOT.kCyan', 'ROOT.kOrange+2'],
                    help='Colors for the files: may be a python snippet, e.g. the default %(default)s.')

lambda_fmt = 'lambda name, hists, curr: (%s)'
group = parser.add_argument_group('Callback function snippets: will be of the form ' + lambda_fmt % '<snippet here>')
group.add_argument('--no-stats', default='False',
                    help='Snippet for no_stats lambda (default: %(default)s).')
group.add_argument('--stat-size', default='(0.2,0.2)',
                    help='Snippet for stat_size lambda (default: %(default)s).')
group.add_argument('--apply-commands', default='None',
                  help='Snippet for apply_commands (default: %(default)s).')
group.add_argument('--separate-plots', default='None',
                  help='Snippet for separate_plots (default: %(default)s).')
group.add_argument('--skip', default='None',
                  help='Snippet for skip lambda (default: %(default)s).')
group.add_argument('--draw-command', default='""',
                   help='Snippet for draw_command lambda (default: %(default)s).')
group.add_argument('--scaling', default='1.',
                   help='Snippet for scaling lambda (default: %(default)s).')
group.add_argument('--ratio', default='True',
                   help='Snippet for ratio lambda (default: %(default)s).')
group.add_argument('--x-range', default='None',
                   help='Snippet for x_range lambda (default: %(default)s).')
group.add_argument('--move-overflows', default='"under over"',
                   help='Snippet for move_overflows lambda (default: %(default)s).')
group.add_argument('--profile', default='None',
                   help='Snippet for profile lambda (default: %(default)s).')

options = parser.parse_args()

if len(options.positional) < 3:
    print 'Required args missing, including at least one filename\n'
    parser.print_help()
    sys.exit(1)

from JMTucker.Tools.ROOTTools import *

options.file_dirs = []
options.files = []
options.dir_paths = []
for x in options.positional[:-1]:
    if '.root:' in x:
        options.file_dirs.append(x)
    elif '.root' in x:
        options.files.append(x)
    else:
        options.dir_paths.append(x)
options.plot_path = options.positional[-1]

if options.file_dirs:
    if options.files and options.dir_paths:
        raise ValueError('if doing file.root:directory/path, must specify only that way')
else:
    if not options.files or not options.dir_paths:
        raise ValueError('no files/directories specified')

nfiles = len(options.file_dirs) if options.file_dirs else len(options.files) * len(options.dir_paths)

options.nice = options.nice[:nfiles]
while len(options.nice) < nfiles:
    options.nice.append('file%i' % (len(options.nice) + 1))

options.colors = options.colors[:nfiles]
options.colors = [eval(c) for c in options.colors]
ncolors = len(options.colors)
while len(options.colors) < nfiles:
    options.colors.append(ROOT.kMagenta + 1 + len(options.colors) - ncolors)

def lambda_it(options, name):
    l = lambda_fmt % getattr(options, name)
    o = eval(l)
    setattr(options, name, l)
    setattr(options, 'lambda_' + name, o)
    return o

lambda_kwargs = {}
for name in 'no_stats', 'stat_size', 'apply_commands', 'separate_plots', 'skip', 'draw_command', 'scaling', 'ratio', 'x_range', 'move_overflows', 'profile':
    lambda_kwargs[name] = lambda_it(options, name)

print 'comparehists running with these options:'
pprint({x:y for x,y in vars(options).iteritems() if not x.startswith('lambda_')})

#import sys ; print 'argv:', sys.argv ; raise 1 ; sys.exit(1)

########################################################################

set_style()
ROOT.gStyle.SetOptStat(options.opt_stat)

if options.ps_args:
    options.ps_args = ', ' + options.ps_args
ps = eval("plot_saver(options.plot_path, size=options.size, per_page=options.per_page%s)" % options.ps_args)

if options.file_dirs:
    file_dirs = [file.split(':', 1) for file in options.file_dirs]
    files, dirs = [], []
    for fn, dir_path in file_dirs:
        f = ROOT.TFile.Open(fn)
        if not f.IsOpen():
            raise ValueError('file %s not readable' % fn)
        files.append(f)
        d = f.Get(dir_path)
        dirs.append(d)
else:
    files = [ROOT.TFile.Open(file) for file in options.files]
    for i,f in enumerate(files):
        if not f.IsOpen():
            raise ValueError('file %s not readable' % options.files[i])

    dirs = []
    for dir_path in options.dir_paths:
        if dir_path == '' or dir_path == '/':
            dirs += [file for file in files]
        else:
            dirs += [file.Get(dir_path) for file in files]
            for i,d in enumerate(dirs):
                if not issubclass(type(d), ROOT.TDirectory):
                    raise ValueError('dir %s not found in file %s' % (dir_path, options.files[i]))

compare_hists(ps,
              samples = zip(options.nice, dirs, options.colors),
              recurse = options.recurse,
              sort_names = options.sort_names,
              show_progress = options.show_progress,
              only_n_first = options.only_n_first,
              raise_on_incompatibility = options.raise_on_incompatibility,
              **lambda_kwargs)
