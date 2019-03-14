#!/usr/bin/env python

import re
from JMTucker.Tools.CMSSWTools import cmssw_base

def _parse(_r=re.compile(r'w_\["(.*)"\] = std::vector<double>\(\{(.*)\}\);')):
    w = {}
    for line in open(cmssw_base('src/JMTucker/Tools/interface/PileupWeights.h')):
        mo = _r.search(line)
        if mo:
            k, v = mo.groups()
            v = eval('[%s]' % v)
            w[k] = v
            try:
                w[int(k)] = v
            except ValueError:
                pass
    return w

pileup_weights = _parse()

def get_pileup_weights(sample, cross=None):
    from JMTucker.Tools.Year import year
    weights = pileup_weights.get(sample, pileup_weights[year])
    if cross:
        cross = 'cross_%s' % cross
        weights = [a*b for a,b in zip(weights, pileup_weights[cross])]
    return weights

########################################################################

class derive_weights(object):
    def __init__(self, data_fn, mc_fn, data_path='pileup', mc_path='PileupDist/h_npu', tol=1e-9, raise_tol=True):
        from JMTucker.Tools.ROOTTools import ROOT

        self.data_f = ROOT.TFile(data_fn)
        self.mc_f   = ROOT.TFile(mc_fn)
        self.data_h = self.data_f.Get(data_path)
        self.mc_h   = self.mc_f.Get(mc_path)

        def norm(h):
            h = h.Clone(h.GetName() + '_norm')
            h.Sumw2()
            h.Scale(1/h.Integral(1, h.GetNbinsX()+1))
            return h

        self.data_h_orig = self.data_h
        self.mc_h_orig   = self.mc_h

        self.data_h = norm(self.data_h)
        self.mc_h   = norm(self.mc_h)

        self.ndata = self.data_h.GetNbinsX()
        assert self.ndata == self.mc_h.GetNbinsX() # JMTBAD

        self.weights = []

        for i in xrange(1, self.ndata+1):
            d = self.data_h.GetBinContent(i)
            m = self.mc_h.GetBinContent(i)
            w = -1
            if m == 0:
                if d > tol:
                    msg = 'm == 0 and d = %g > tol=%g for i = %i' % (d, tol, i)
                    if raise_tol:
                        raise ValueError(msg)
                    else:
                        print msg
                w = 0
            else:
                w = d/m
            self.weights.append(w)

        while self.weights[-1] == 0:
            self.weights.pop()

    def draw(self, fn):
        from JMTucker.Tools.ROOTTools import ROOT, draw_in_order, differentiate_stat_box
        self.data_h.SetLineColor(ROOT.kBlack)
        self.mc_h.SetLineColor(ROOT.kRed)
        self.data_h.SetLineWidth(2)
        self.mc_h.SetLineWidth(2)
        c = ROOT.TCanvas('c','',1000,800)
        draw_in_order([[self.data_h, self.mc_h], ''], sames=True)
        c.Update()
        differentiate_stat_box(self.mc_h)
        if '.' in os.path.basename(fn):
            c.SaveAs(fn)
        else:
            c.SaveAs(fn + '.png')
            c.SaveAs(fn + '.root')

if __name__ == '__main__':
    import os
    from sys import argv, exit

    if len(argv) > 1:
        if argv[1] == 'cross':
            if len(argv) < 4:
                exit('usage: %s cross num_fn den_fn' % argv[0])
            print derive_weights(argv[2], argv[3], mc_path='pileup', raise_tol=False).weights
        else:
            if len(argv) < 3:
                exit('usage: %s data_fn mc_fn [mc_fn2 ...]' % argv[0])
            data_fn = argv[1]
            for mc_fn in argv[2:]:
                ww = derive_weights(data_fn, mc_fn, raise_tol=False)
                print mc_fn, '[',
                for w in ww.weights:
                    print '%.6g,' % w,
                print ']'
                #ww.draw(os.path.basename(mc_fn).replace('.root', ''))
