#!/usr/bin/env python

import sys, os
from array import array
from math import pi
from JMTucker.Tools.ROOTTools import *
set_style()
ROOT.TH1.AddDirectory(0)
ROOT.gStyle.SetOptStat(2222222)
ROOT.gStyle.SetOptFit(2222)

def arrit(l):
    return array('d', l)

ntracks = 5
input_fn = [x for x in sys.argv if x.endswith('.root') and os.path.isfile(x)][0]
ps = plot_saver('plots/one2two/ntracks%i_%s_phifits' % (ntracks, os.path.basename(input_fn).replace('.root', '')), size=(600,600))

f = ROOT.TFile(input_fn)
t = f.Get('mfvOne2Two/t')

t.SetAlias('svdist', 'sqrt((x0-x1)**2 + (y0-y1)**2)')
t.SetAlias('svdphi', 'TVector2::Phi_mpi_pi(atan2(y0,x0)-atan2(y1,x1))')

t.Draw('svdist>>hdist(100,0,0.1)', 'nvtx == 2')
probs = arrit([0.2, 0.4, 0.6, 0.8, 1.0])
n_probs = len(probs)
quantiles = arrit([0]*n_probs)
ROOT.hdist.GetQuantiles(n_probs, quantiles, probs)
quantiles = [0.] + list(quantiles)

dists = [
    ('all', 0, 10),
    ('to48', 0, 0.048),
    ]

dists += [('bin%i' % i, a, b) for i,(a,b) in enumerate(zip(quantiles, quantiles[1:]))]

bestexps = []

for distname, distmin, distmax in dists:
    histname = 'h_dphi_dist' + distname
    t.Draw('abs(svdphi)>>%s(8, 0, %f)' % (histname, pi), 'nvtx == 2 && ntk0 >= %i && ntk1 >= %i && svdist > %f && svdist < %f' % (ntracks, ntracks, distmin, distmax))
    h = getattr(ROOT, histname)

    steps = range(60)
    reses = []
    for expstep in steps:
        exp = 1 + 0.1*expstep
        integ = 2*pi**(exp+1)/(exp+1)
        expform = '[0]*abs(x)**%.1f/%.6f' % (exp, integ)
        fcn = ROOT.TF1('f%i' % expstep, expform, -pi, pi)
        reses.append((exp, integ, fcn, h.Fit(fcn, 'ILRQS')))

    g = ROOT.TGraph(len(reses), array('d', [res[0] for res in reses]), array('d', [res[-1].Chi2() for res in reses]))
    g.SetMarkerStyle(20)
    g.SetMarkerSize(1)
    g.Draw('ALP')
    ps.save(distname + '_chi2s')

    best = max(reses, key=lambda x: x[-1].Prob())
    bestexps.append(best[0])
    h.Fit(best[2], 'ILRQ')
    h.SetTitle('best fit exp = %.1f;#Delta #phi;blah' % best[0])
    ps.save(distname)

g = ROOT.TGraph(len(bestexps[2:]), arrit(quantiles), arrit(bestexps))
g.SetMarkerStyle(20)
g.SetMarkerSize(1)
g.Draw('ALP')
ps.save('bestexps')
