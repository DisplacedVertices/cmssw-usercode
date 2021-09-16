#!/usr/bin/env python

import os, sys, tempfile, argparse

parser = argparse.ArgumentParser(description = 'pileup.py: use analysis JSONs to get lumi-weighted pileup distribution and derive set of weights for a MC sample.',
                                 usage = '%(prog)s <required options>')

parser.add_argument('--year', type=int, choices=[2017,2018], default=2017,
                    help='Which year to use.')
parser.add_argument('--ana-json',
                    help='The JSON file produced from crab -report (or multiple crab reports, added together with mergeJSON.py).')
parser.add_argument('--pileup-json', default='default',
                    help='The centrally produced pileup-weighted pileup JSON (default /afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/CollisionsYY/13TeV/PileUp/pileup_latest.txt).')
parser.add_argument('--max-npu', type=int, default=1000,
                    help='The maximum pileup bin (default %(default)s).')
parser.add_argument('--pileupcalc-mode', default='true',
                    help='The mode for pileupCalc.py: "true" or "observed" (default %(default)s).')
parser.add_argument('--pileupcalc-mbxsec', default=-1, type=int,
                    help='The minbias cross section for pileupCalc.py, in microbarn (default 69200 for 13 TeV).')
parser.add_argument('--data-fn', default='default',
                    help='The output filename for pileupCalc.py (default pileup_YYYY.root).')
parser.add_argument('--data-path', default='pileup',
                    help='The name of the histogram for pileupCalc.py to produce or look for in the file given by --data-fn.')
parser.add_argument('--no-run-pileupcalc', action='store_false', dest='run_pileupcalc', default=True,
                    help='If specified, do not run pileupCalc.py, but assume that the data distribution already exists in the file given by --data-fn.')
parser.add_argument('--mc-fn', default='pileup_mc.root',
                    help='The input filename for the MC distribution (default %(default)s).')
parser.add_argument('--mc-path', default='PileupDist/h_npu',
                    help='The name of the input MC histogram in the file given by --mc-fn (default %(default)s).')
parser.add_argument('--tol', type=float, default=1e-9,
                    help='The tolerance for the data npu value when the MC npu value is == 0 (default %(default)g).')
parser.add_argument('--plots', default='',
                    help='Whether to make an overlay plot of the input histograms and the derived weights.')

options = parser.parse_args()

if options.pileup_json == 'default':
    options.pileup_json = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions%i/13TeV/PileUp/UltraLegacy/pileup_latest.txt' % (options.year-2000)
if options.pileupcalc_mbxsec == -1:
    options.pileupcalc_mbxsec = 69200
if options.data_fn == 'default':
    options.data_fn = 'pileup_%i.root' % options.year

if options.ana_json is None and options.run_pileupcalc:
    raise ValueError('need an ana JSON input')

################################################################################

if options.run_pileupcalc:
    def print_run(cmd):
        print cmd
        return os.system(cmd)

    tmp_fn = None
    if options.pileup_json.startswith('/afs'):
        tmp_fn = tempfile.mktemp()
        cmd = 'scp lxplus.cern.ch:%s %s' % (options.pileup_json, tmp_fn)
        if print_run(cmd) != 0:
            print 'warning: scp failed, pileupCalc.py will fail next'
        options.pileup_json = tmp_fn

    cmd = 'pileupCalc.py -i %s --inputLumiJSON %s --calcMode %s --minBiasXsec %s --maxPileupBin=%i --numPileupBins=%i --pileupHistName=%s %s' % (options.ana_json, options.pileup_json, options.pileupcalc_mode, options.pileupcalc_mbxsec, options.max_npu, options.max_npu, options.data_path, options.data_fn)
    ret = print_run(cmd)
    if tmp_fn:
        os.remove(tmp_fn)
    if ret != 0:
        raise ValueError('pileupCalc returned failure (%i)' % ret)

################################################################################

from JMTucker.Tools.PileupWeights import derive_weights
ww = derive_weights(options.data_fn, options.mc_fn, options.data_path, options.mc_path, options.tol)

print 'average weight =', sum(ww.weights)/len(ww.weights)
print 'w_[""] = std::vector<double>({',
for w in ww.weights:
    print '%.6g,' % w,
print '});'

if options.plots:
    from JMTucker.Tools.ROOTTools import *
    set_style()
    ps = plot_saver(options.plots, size=(600,600))

    draw_in_order([(ww.data_h_orig, 'hist'), (ww.mc_h_orig, 'hist')], sames=True)
    ps.c.Update()
    differentiate_stat_box(ww.data_h_orig, 0, new_size=(0.3, 0.2))
    differentiate_stat_box(ww.mc_h_orig,   1, new_size=(0.3, 0.2))
    ps.save('dists')

    draw_in_order([(ww.data_h, 'hist'), (ww.mc_h, 'hist')], sames=True)
    ps.c.Update()
    differentiate_stat_box(ww.data_h, 0, new_size=(0.3, 0.2))
    differentiate_stat_box(ww.mc_h,   1, new_size=(0.3, 0.2))
    ps.save('dists_normalized')

    h_w = ROOT.TH1F('h_w', ';;weight', ww.ndata, ww.data_h.GetXaxis().GetXmin(), ww.data_h.GetXaxis().GetXmax())
    for i,w in enumerate(ww.weights):
        h_w.SetBinContent(i+1, w)

    h_w.Draw()
    ps.save('weights')
