#!/usr/bin/env python

# for when hadding takes too long and you want a plot now

from DVCode.Tools.ROOTTools import *

ROOT.TH1.AddDirectory(0)

ws= [
    [19.860832,5.955227,3.108760,0.402823,0.166630],
    [19.834705,5.913319,3.131839,0.400370,0.165487],
    ]

ps = [
    '/uscms_data/d2/tucker/crab_dirs/HistosV11_15',
    '/uscms_data/d2/tucker/crab_dirs/HistosV11_16_part',
    ]

bns = 'qcdht0500sum.root qcdht0700sum.root qcdht1000sum.root qcdht1500sum.root qcdht2000sum.root'.split()

fs = [
    [ROOT.TFile(ps[0] + '/' + bn) for bn in bns],
    [ROOT.TFile(ps[1] + '/' + bn) for bn in bns],
    ]

set_style()
ps = plot_saver(plot_dir('dddd'), size=(600,600))

hns = [
    'mfvVertexHistosOnlyOneVtx/h_sv_best0_bsbs2ddist',
    'vtxHst1VNoBs2derr/h_sv_best0_bs2derr',
    ]

cs = [ROOT.kRed, ROOT.kBlue]

for hn in hns:
    nn = hn.replace('/', '_')
    hs = []
    for j in xrange(2):
        hh = None
        for i, bn in enumerate(bns):
            h = fs[j][i].Get(hn)
            if hh is None:
                hh = h.Clone(nn)
                hh.Scale(ws[j][i])
            else:
                hh.Add(h, ws[j][i])

        hh.SetLineWidth(2)
        hh.SetLineColor(cs[j])
        if hn == 'mfvVertexHistosOnlyOneVtx/h_sv_best0_bsbs2ddist':
            hh.GetXaxis().SetRangeUser(0, 0.5)

        if hn != 'vtxHst1VNoBs2derr/h_sv_best0_bs2derr':
            hh.Scale(1./hh.Integral())

        hs.append(hh)

    hs[0].Draw()
    ps.c.Update()
    differentiate_stat_box(hs[0], 0, new_size=(0.3, 0.2))
    hs[1].Draw('sames')
    ps.c.Update()
    differentiate_stat_box(hs[1], 1, new_size=(0.3, 0.2))
    ps.save(nn)
