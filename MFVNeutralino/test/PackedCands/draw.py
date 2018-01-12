#!/usr/bin/env python

import sys
from JMTucker.Tools.ROOTTools import *
set_style()
ROOT.TH1.AddDirectory(0)

ps = plot_saver(plot_dir('packedcands'), size=(600,600), log=False)

ff = ROOT.TFile('/uscms_data/d2/tucker/crab_dirs/PackedCandsV0/mfv_neu_tau10000um_M1600.root')

def get_em(path):
    f = ff.Get(path)
    def skip(name, obj):
        return False
    def rebin(name, obj):
        return obj

    l = []
    for key in f.GetListOfKeys():
        name = key.GetName()
        obj = f.Get(name)
        if skip(name, obj):
            continue
        obj = rebin(name, obj)
        l.append(obj)
    return l

all_tracks = get_em('mfvPackedCands/all')
highpurity = get_em('mfvPackedCands/highpurity')
seed = get_em('mfvPackedCands/seed')
match = get_em('mfvPackedCands/match')
match_pass = get_em('mfvPackedCands/match_pass')
nomatch = get_em('mfvPackedCands/nomatch')
nomatch_highpurity = get_em('mfvPackedCands/nomatch_highpurity')
nomatch_highpurity_goodptres = get_em('mfvPackedCands/nomatch_highpurity')

zz = [
    ('all+highpurity+seed', (all_tracks, highpurity, seed)),
    ('seed+match+match-pass', (seed, match, match_pass)),
    ('seed+nomatch+nomatch-highpurity+nomatch-highpurity-goodptres', (seed, nomatch, nomatch_highpurity, nomatch_highpurity_goodptres)),
    ]

colors = [ROOT.kRed, ROOT.kGreen+2, ROOT.kBlue, 9]

for namebase, z in zz:
    assert len(set(len(y) for y in z)) == 1
    for hists in zip(*z):
        name = None
        for i,h in enumerate(hists):
            if name is None:
                name = h.GetName()
            else:
                assert name == h.GetName()
            h.SetLineColor(colors[i])
            h.SetLineWidth(2)
        ratios_plot(namebase + '_' + name, 
                    hists,
                    plot_saver=ps,
                    res_fit=False,
                    res_divide_opt={'confint': clopper_pearson},
                    statbox_size=(0.2,0.2),
                    res_y_range=0.05,
                    )
