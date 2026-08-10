# produce the root files below by setting min/max_npu in 2v_from_jets.cc

from JMTucker.Tools.ROOTTools import *

fns = ['%s/2v_from_jets_2016_3track_default_v14.root' % x for x in '2vdefault,2v_0_18,2v_19_22,2v_23_27,2v_28_32,2v_33_up'.split(',')]
names = ['default', '0-18', '19-22','23-27','28-32','33-']
colors = [ROOT.kBlack, ROOT.kRed-9, ROOT.kRed-7, ROOT.kRed, ROOT.kRed+1, ROOT.kRed+2]
stats = False
rebin = True

####

set_style()
ROOT.gStyle.SetOptStat(1111)
ps = plot_saver(plot_dir('construction_v_pileup'), size=(600,600))

fs = [ROOT.TFile(fn) for fn in fns]
hs = [f.Get('h_c1v_dvv') for f in fs]

for i,h in enumerate(hs):
    h.SetName(names[i])
    if rebin:
        hs[i] = h = h.Rebin(3, names[i], to_array(0,0.04,0.07,0.15))
    move_overflow_into_last_bin(h)
    h.SetLineWidth(2)
    h.SetLineColor(colors[i])
    h.Scale(1./h.Integral())
    if not stats:
        h.SetStats(0)

draw_in_order((hs, 'hist'), True)
ps.c.Update()

if stats:
    for i,h in enumerate(hs):
        differentiate_stat_box(h, (1-i/3,i%3), new_size=(0.3,0.2))

ps.save('fff')
