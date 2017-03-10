#!/usr/bin/env python

import os, sys, JMTucker.Tools.argparse as argparse

parser = argparse.ArgumentParser(description = 'pileup.py: use analysis JSONs to get lumi-weighted pileup distribution and derive set of weights for a MC sample.',
                                 usage = '%(prog)s <required options>')

parser.add_argument('--year', type=int, choices=[2015, 2016],
                    help='Which year to use.')
parser.add_argument('--ana-json',
                    help='The JSON file produced from crab -report (or multiple crab reports, added together with mergeJSON.py).')
parser.add_argument('--lumi-json', default='default',
                    help='The centrally produced lumi-weighted pileup JSON (default /afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions%(two-digit-year)i/13TeV/PileUp/pileup_latest.txt).')
parser.add_argument('--max-npu', type=int, default=100,
                    help='The maximum pileup bin (default %(default)s).')
parser.add_argument('--pileupcalc-mode', default='true',
                    help='The mode for pileupCalc.py: "true" or "observed" (default %(default)s).')
parser.add_argument('--pileupcalc-mbxsec', default=-1, type=int,
                    help='The minbias cross section for pileupCalc.py, in microbarn (default 69000 for 2015 and 69200 for 2016).')
parser.add_argument('--data-fn', default='default',
                    help='The output filename for pileupCalc.py (default %(default)s).')
parser.add_argument('--data-path', default='pileup',
                    help='The name of the histogram for pileupCalc.py to produce in the file given by --data-fn (default pileup_%(year)i.root).')
parser.add_argument('--no-run-pileupcalc', action='store_false', dest='run_pileupcalc', default=True,
                    help='If specified, do not run pileupCalc.py, but assume that the data distribution already exists in the file given by --data-fn.')
parser.add_argument('--mc-fn', default='pileup_mc.root',
                    help='The input filename for the MC distribution (default %(default)s).')
parser.add_argument('--mc-path', default='MCPileupDist/h_npu',
                    help='The name of the input MC histogram in the file given by --mc-fn (default %(default)s).')
parser.add_argument('--tol', type=float, default=1e-9,
                    help='The tolerance for the data npu value when the MC npu value is == 0 (default %(default)g).')
parser.add_argument('--plots', default='',
                    help='Whether to make an overlay plot of the input histograms and the derived weights.')

options = parser.parse_args()

if options.lumi_json == 'default':
    options.lumi_json = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions%i/13TeV/PileUp/pileup_latest.txt' % (options.year-2000)
if options.pileupcalc_mbxsec == -1:
    options.pileupcalc_mbxsec = 69000 if options.year == 2015 else 69200
if options.data_fn == 'default':
    options.data_fn = 'pileup_%i.root' % options.year

if options.ana_json is None and options.run_pileupcalc:
    raise ValueError('need an ana JSON input')

################################################################################

if options.run_pileupcalc:
    cmd = 'pileupCalc.py -i %s --inputLumiJSON %s --calcMode %s --minBiasXsec %s --maxPileupBin=%i --numPileupBins=%i --pileupHistName=%s %s' % (options.ana_json, options.lumi_json, options.pileupcalc_mode, options.pileupcalc_mbxsec, options.max_npu, options.max_npu, options.data_path, options.data_fn)
    print cmd
    ret = os.system(cmd)
    if ret != 0:
        raise ValueError('pileupCalc returned failure (%i)' % ret)

from JMTucker.Tools.ROOTTools import ROOT

data_f = ROOT.TFile(options.data_fn)
mc_f   = ROOT.TFile(options.mc_fn)
data_h = data_f.Get(options.data_path)
mc_h   = mc_f.Get(options.mc_path)

def norm(h):
    h = h.Clone(h.GetName() + '_norm')
    h.Sumw2()
    h.Scale(1/h.Integral(1, h.GetNbinsX()+1))
    return h

data_h.SetMarkerStyle(20)
data_h.SetMarkerSize(1)
mc_h.SetLineColor(ROOT.kRed)
mc_h.SetLineWidth(2)

data_h_orig = data_h
mc_h_orig = mc_h

data_h = norm(data_h)
mc_h = norm(mc_h)

ndata = data_h.GetNbinsX()
nmc = mc_h.GetNbinsX()
assert ndata == nmc # JMTBAD

weights = []

for i in xrange(1, ndata+1):
    d = data_h.GetBinContent(i)
    m = mc_h.GetBinContent(i)
    w = -1
    if m == 0:
        if d > options.tol:
            raise ValueError('m == 0 and d = %g > %g for i = %i (see --tol)' % (d, options.tol, i))
        w = 0
    else:
        w = d/m
    weights.append(w)

while weights[-1] == 0:
    weights.pop()
print 'average weight =', sum(weights)/len(weights)

print '\npython:\n'
print 'weights = %r' % weights
print '\nc++:\n'
print 'const int max_npu = %i;' % len(weights)
print 'const double pileup_weights[max_npu] = {'
print ', '.join(repr(w) for w in weights)
print '};'

if options.plots:
    from JMTucker.Tools.ROOTTools import *
    set_style()
    ps = plot_saver(options.plots, size=(600,600))

    draw_in_order([(data_h_orig, 'e'), (mc_h_orig, 'e')], sames=True)
    ps.c.Update()
    differentiate_stat_box(data_h_orig, 0, new_size=(0.3, 0.2))
    differentiate_stat_box(mc_h_orig,   1, new_size=(0.3, 0.2))
    ps.save('dists')

    draw_in_order([(data_h, 'e'), (mc_h, 'e')], sames=True)
    ps.c.Update()
    differentiate_stat_box(data_h, 0, new_size=(0.3, 0.2))
    differentiate_stat_box(mc_h,   1, new_size=(0.3, 0.2))
    ps.save('dists_normalized')

    h_w = ROOT.TH1F('h_w', ';;weight', ndata, data_h.GetXaxis().GetXmin(), data_h.GetXaxis().GetXmax())
    for i,w in enumerate(weights):
        h_w.SetBinContent(i+1, w)

    h_w.Draw()
    ps.save('weights')
