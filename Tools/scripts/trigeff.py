#!/usr/bin/env python

import sys, optparse

################################################################################

parser = optparse.OptionParser(usage='%prog [options] input.root [plot path]')
parser.add_option('--dir', default='SimpleTriggerEfficiency',
                  help='The directory name (i.e. the module label used for SimpleTriggerEfficiency).')
parser.add_option('--dir2',
                  help='The second directory name (if applicable, e.g. in --compare).')
parser.add_option('--table', action='store_true', default=False,
                  help='Print a table of the paths and efficiencies.')
parser.add_option('--table-nevents', action='store_true', default=False,
                  help='In the table, also print number of events instead of just the efficiencies.')
parser.add_option('--table-conf-level', type=float, default=0.6827,
                  help='Confidence level for the intervals displayed (default is %default).')
parser.add_option('--table-apply-prescales', action='store_true', default=False,
                  help='Use prescales from prescales.py in current directory.')
parser.add_option('--table-apply-prescales-in-sort', action='store_true', default=False,
                  help='Use prescaled values when sorting the table (implies --table-apply-prescales).')
parser.add_option('--table-sort-by-bit', action='store_true', default=False,
                  help='Sort by trigger bit instead of decreasing efficiency.')
parser.add_option('--compare', action='store_true', default=False,
                  help='Compare two sets of efficiencies (requires --dir2 to be specified).')
parser.add_option('--twod', action='store_true', default=False,
                  help='Not implemented.')

options, args = parser.parse_args()
#print options ; print args ; import sys ; print sys.argv ; raise 1

if not options.dir:
    raise ValueError('must supply a directory name')

if options.twod:
    raise NotImplementedError('twod')

if not any((options.table, options.compare, options.twod)):
    print 'none of --table, --compare, --twod specified, defaulting to --table'
    options.table = True

options.input_fn = args[0]
options.will_plot = options.compare or options.twod

if options.will_plot:
    if len(args) < 2:
        raise ValueError('must supply plot path when plotting')
    options.plot_path = args[1]

if options.table_apply_prescales_in_sort:
    options.table_apply_prescales = True

################################################################################

from math import log10
from JMTucker.Tools.ROOTTools import *

input_f = ROOT.TFile(options.input_fn)

if options.compare or options.twod:
    set_style()
    ps = plot_saver(options.plot_path)
    
def get_hists(dn, twod=False):
    hnum = input_f.Get(dn).Get('triggers%s_pass_num' % ('2d' if twod else ''))
    hden = input_f.Get(dn).Get('triggers%s_pass_den' % ('2d' if twod else ''))
    return hnum, hden

################################################################################

if options.table:
    hnum, hden = get_hists(options.dir)
    print 'number of events:', hden.GetBinContent(1)
    
    width = 0
    content = []
    mx = 0
    for i in xrange(1, hden.GetNbinsX() + 1):
        path = hden.GetXaxis().GetBinLabel(i)
        width = max(width, len(path))

        num = hnum.GetBinContent(i)
        den = hden.GetBinContent(i)
        eff, lo, hi = clopper_pearson(num, den, alpha=1-options.table_conf_level)

        prescaled_eff = 1
        
        if options.table_apply_prescales:
            import prescales
            l1, hlt, overall = prescales.get(path)
            if overall > 0:
                eff /= overall
                lo /= overall
                hi /= overall
            elif overall == 0:
                eff = lo = hi = 0.
        else:
            l1, hlt, overall = -1, -1, -1

        mx = max(mx, num, hi*den)
        if options.table_nevents:
            c = (i-1, path, num, int(round(lo*den)), int(round(hi*den)))
        else:
            c = (i-1, path, eff, (hi-lo)/2, lo, hi)
        if options.table_apply_prescales:
            c += (l1, hlt, overall, prescaled_eff)
        content.append(c)

    if options.table_nevents:
        num_width = '%' + str(int(round(log10(mx))) + 2) + 'i'
        fmt = '(%3i) %' + str(width + 2) + 's ' + num_width + '  68%% CL: [' + num_width + ', ' + num_width + ']'
    else:
        fmt = '(%3i) %' + str(width + 2) + 's %.3e +- %.3e 68%% CL: [%.3e, %.3e]'
    if options.table_apply_prescales:
        fmt += '   after prescales: (%10i * %10i = %10i):  %.4f'

    if options.table_sort_by_bit:
        print 'sorted by trigger bit:'
        for c in content:
            print fmt % c
        print
    else:
        print 'sorted by decreasing eff',
        if options.table_apply_prescales_in_sort:
            print '(after applying prescales):'
            key = lambda x: x[-1]
        else:
            print ':'
            key = lambda x: x[2]
        content.sort(key=key, reverse=True)
        for c in content:
            print fmt % c

################################################################################
            
if options.compare:
    hnum,  hden  = get_hists(options.dir)
    hnum2, hden2 = get_hists(options.dir2)

    eff  = histogram_divide(hnum,    hden)
    eff2 = histogram_divide(hnum_mu, hden_mu)

    eff.SetLineColor(ROOT.kRed)
    eff.Draw('APL')
    eff2.SetLineColor(ROOT.kBlue)
    eff2.Draw('P same')
    ps.save('compare')

################################################################################
            
if False and options.twod:
    hnum, hden = get_hists(options.dir, twod=True)
    hnum.Divide(hden)
    xax, yax = hnum.GetXaxis(), hnum.GetYaxis()
    for x in xrange(1, xax.GetNbins()+1):
        for y in xrange(1, yax.GetNbins()+1):
            xpath = xax.GetBinLabel(x)
            ypath = yax.GetBinLabel(y)
            # ...
