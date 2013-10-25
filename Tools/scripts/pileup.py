#!/usr/bin/env python

import os, sys, JMTucker.Tools.argparse as argparse

parser = argparse.ArgumentParser(description = 'pileup.py: use analysis JSONs to get lumi-weighted pileup distribution and derive set of weights for a MC sample.',
                                 usage = '%(prog)s <required options>')

parser.add_argument('--ana-json',
                    help='The JSON file produced from crab -report (or multiple crab reports, added together with mergeJSON.py).')
parser.add_argument('--lumi-json', default='/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions12/8TeV/PileUp/pileup_latest.txt',
                    help='The centrally produced lumi-weighted pileup JSON (default %(default)s).')
parser.add_argument('--max-npu', type=int, default=65,
                    help='The maximum pileup bin (default %(default)s).')
parser.add_argument('--pileupcalc-mode', default='true',
                    help='The mode for pileupCalc.py: "true" or "observed" (default %(default)s).')
parser.add_argument('--pileupcalc-mbxsec', default=69400, type=int,
                    help='The minbias cross section for pileupCalc.py, in microbarn (default %(default)s).')
parser.add_argument('--data-fn', default='pileup.root',
                    help='The output filename for pileupCalc.py (default %(default)s).')
parser.add_argument('--data-path', default='pileup',
                    help='The name of the histogram for pileupCalc.py to produce in the file given by --data-fn (default %(default)s).')
parser.add_argument('--no-run-pileupcalc', action='store_false', dest='run_pileupcalc', default=True,
                    help='If specified, do not run pileupCalc.py, but assume that the data distribution already exists in the file given by --data-fn.')
parser.add_argument('--mc-fn', default='pileup_mc.root',
                    help='The input filename for the MC distribution (default %(default)s).')
parser.add_argument('--mc-path', default='pileup',
                    help='The name of the input MC histogram in the file given by --mc-fn (default %(default)s).')

options = parser.parse_args()

if options.ana_json is None:
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
    h.Scale(1/h.Integral(1, h.GetNbinsX()+1))

norm(data_h)
norm(mc_h)

ndata = data_h.GetNbinsX()
nmc = mc_h.GetNbinsX()
assert ndata == nmc # JMTBAD

weights = []

for i in xrange(1, ndata+1):
    d = data_h.GetBinContent(i)
    m = mc_h.GetBinContent(i)
    w = -1
    if m == 0:
        if d > 1e-12:
            raise ValueError('m == 0 and d = %e != 0 for i = %i' % (d, i))
        w = 0
    else:
        w = d/m
    weights.append(w)

print 'sum weights =', sum(weights), 'average weight =', sum(weights)/len(weights)
while weights[-1] == 0:
    weights.pop()
print '\npython:\n'
print 'weights = %r' % weights
print '\nc++:\n'
print 'const int max_npu = %i;' % len(weights)
print 'const double pileup_weights[max_npu] = {'
print ', '.join(repr(w) for w in weights)
print '};'
