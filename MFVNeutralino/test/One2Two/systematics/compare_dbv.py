#!/usr/bin/env python

from JMTucker.Tools.ROOTTools import *
import JMTucker.Tools.Samples as Samples
import JMTucker.MFVNeutralino.AnalysisConstants as ac

set_style()
ROOT.TH1.SetDefaultSumw2()

year = 2017
sns = 'qcdht0700_2017 qcdht1000_2017 qcdht1500_2017 qcdht2000_2017 ttbarht0600_2017 ttbarht0800_2017 ttbarht1200_2017 ttbarht2500_2017'.split()
sc = ac.int_lumi_2017 * ac.scale_factor_2017

if year == 2015:
    sns = 'qcdht0700sum_2015 qcdht1000sum_2015 qcdht1500sum_2015 qcdht2000sum_2015 ttbar_2015'.split()
    sc = ac.int_lumi_2015 * ac.scale_factor_2015

ntk = 4
tree_path = 'mfvMiniTree/t'
if ntk == 3:
    tree_path = 'mfvMiniTreeNtk3/t'
if ntk == 4:
    tree_path = 'mfvMiniTreeNtk4/t'

bquarkpt = False

path = 'MiniTreeV21m'
if bquarkpt:
    path = 'MiniTreeV15_v4_bquarkpt'
ps = plot_saver(plot_dir('compare_dbv_%s_%s_ntk%i' % (path, year, ntk)), size=(700,700), root=False)
trees = '/uscms_data/d2/tucker/crab_dirs/%s' % path

def book_dbv(n):
    return ROOT.TH1F(n, '', 40, 0, 0.2)
def book_pt(n):
    return ROOT.TH1F(n, '', 50, 0, 500)
def book_dbv_pt(n):
    return ROOT.TH2F(n, '', 50, 0, 500, 40, 0, 0.2)

h_dbv_sum = book_dbv('dbv_sum')
h_dbv_nob = book_dbv('dbv_nob')
h_dbv_b = book_dbv('dbv_b')
h_dbv_qcdb = book_dbv('dbv_qcdb')
h_dbv_ttbarb = book_dbv('dbv_ttbarb')
h_bquarkpt = book_pt('bquarkpt')
h_dbv_bquarkpt = book_dbv_pt('dbv_bquarkpt')

hs_nob = []
for sn in sns:
    f = ROOT.TFile('%s/%s.root' % (trees,sn))
    t = f.Get(tree_path)
    s = getattr(Samples, sn)

    n = sn + ', no b quarks'
    h_dbv = book_dbv(n)
    t.Draw('dist0>>%s' % n, 'nvtx == 1 && gen_flavor_code != 2')
    h_dbv_sum.Add(h_dbv, sc * s.partial_weight_orig)
    h_dbv_nob.Add(h_dbv, sc * s.partial_weight_orig)
    ps.save(n)

    h = h_dbv.Clone()
    h.SetDirectory(0)
    hs_nob.append(h)

hs_b = []
for sn in sns:
    f = ROOT.TFile('%s/%s.root' % (trees,sn))
    t = f.Get(tree_path)
    s = getattr(Samples, sn)

    if 'ttbar' not in sn:
        n = sn + ', b quarks'
    else:
        n = sn
    h_dbv = book_dbv(n)
    t.Draw('dist0>>%s' % n, 'nvtx == 1 && gen_flavor_code == 2')
    h_dbv_sum.Add(h_dbv, sc * s.partial_weight_orig)
    h_dbv_b.Add(h_dbv, sc * s.partial_weight_orig)
    if 'ttbar' not in sn:
        h_dbv_qcdb.Add(h_dbv, sc * s.partial_weight_orig)
    else:
        h_dbv_ttbarb.Add(h_dbv, sc * s.partial_weight_orig)
    ps.save(n)

    h = h_dbv.Clone()
    h.SetDirectory(0)
    hs_b.append(h)

    if bquarkpt:
        h_pt = book_pt('pt')
        t.Draw('gen_bquark_pt>>pt', 'nvtx == 1')
        h_bquarkpt.Add(h_pt, sc * s.partial_weight_orig)

        h_dbv_pt = book_dbv_pt('dbv_pt')
        t.Draw('dist0:gen_bquark_pt>>dbv_pt', 'nvtx == 1 && gen_flavor_code == 2')
        h_dbv_bquarkpt.Add(h_dbv_pt, sc * s.partial_weight_orig)

if bquarkpt:
    h_bquarkpt.Draw()
    ps.save('bquarkpt')

    h_dbv_bquarkpt.Draw('colz')
    ps.save('dbv_bquarkpt')

    pfx = h_dbv_bquarkpt.ProfileX()
    pfx.SetTitle('%s-track one-vertex events;b quark p_{T} (GeV);mean d_{BV} (cm)' % ntk)
    pfx.SetMaximum(0.05)
    pfx.SetLineColor(ROOT.kPink)
    pfx.Draw()
    ps.c.Update()
    differentiate_stat_box(pfx, movement=0, new_size=(0.2,0.2))
    ps.save('dbv_bquarkpt_pfx')

h_dbv_sum.Draw()
ps.save('dbv_sum')


h_dbv_sum.SetTitle('%s-track one-vertex events;d_{BV} (cm);arb. units' % ntk)
h_dbv_sum.SetStats(0)
h_dbv_sum.SetLineColor(ROOT.kBlack)
h_dbv_sum.SetLineWidth(3)
h_dbv_sum.Scale(1./h_dbv_sum.Integral())
h_dbv_sum.GetYaxis().SetRangeUser(1e-5,1)
h_dbv_sum.Draw('hist')

l = ROOT.TLegend(0.3,0.6,0.9,0.9)
l.AddEntry(h_dbv_sum, 'total background: mean d_{BV} = %4.1f #pm %2.1f #mum' % (10000*h_dbv_sum.GetMean(), 10000*h_dbv_sum.GetMeanError()))

for i,h in enumerate(hs_nob):
    h.SetStats(0)
    h.SetLineColor(ROOT.kBlue + i)
    h.SetLineWidth(3)
    if h.GetEntries() != 0:
        h.DrawNormalized('sames')
        l.AddEntry(h, '%s: mean d_{BV} = %4.1f #pm %2.1f #mum' % (h.GetName(), 10000*h.GetMean(), 10000*h.GetMeanError()))

for i,h in enumerate(hs_b):
    h.SetStats(0)
    h.SetLineColor(ROOT.kPink + i)
    h.SetLineWidth(3)
    if h.GetEntries() != 0:
        h.DrawNormalized('sames')
        l.AddEntry(h, '%s: mean d_{BV} = %4.1f #pm %2.1f #mum' % (h.GetName(), 10000*h.GetMean(), 10000*h.GetMeanError()))

l.SetFillColor(0)
l.Draw()
ps.save('dbv')


h_dbv_sum.Draw('hist')
l = ROOT.TLegend(0.3,0.78,0.9,0.9)
l.AddEntry(h_dbv_sum, 'total background: mean d_{BV} = %4.1f #pm %2.1f #mum' % (10000*h_dbv_sum.GetMean(), 10000*h_dbv_sum.GetMeanError()))
h_dbv_nob.SetStats(0)
h_dbv_nob.SetLineColor(ROOT.kBlue)
h_dbv_nob.SetLineWidth(3)
h_dbv_nob.DrawNormalized('sames')
l.AddEntry(h_dbv_nob, 'qcd, no b quarks: mean d_{BV} = %4.1f #pm %2.1f #mum' % (10000*h_dbv_nob.GetMean(), 10000*h_dbv_nob.GetMeanError()))
h_dbv_qcdb.SetStats(0)
h_dbv_qcdb.SetLineColor(ROOT.kPink)
h_dbv_qcdb.SetLineWidth(3)
h_dbv_qcdb.DrawNormalized('sames')
l.AddEntry(h_dbv_qcdb, 'qcd, b quarks: mean d_{BV} = %4.1f #pm %2.1f #mum' % (10000*h_dbv_qcdb.GetMean(), 10000*h_dbv_qcdb.GetMeanError()))
h_dbv_ttbarb.DrawNormalized('sames')
l.AddEntry(h_dbv_ttbarb, 'ttbar: mean d_{BV} = %4.1f #pm %2.1f #mum' % (10000*h_dbv_ttbarb.GetMean(), 10000*h_dbv_ttbarb.GetMeanError()))
l.SetFillColor(0)
l.Draw()
ps.save('dbv_qcdb')


h_dbv_sum.Draw('hist')
l = ROOT.TLegend(0.3,0.65,0.9,0.9)
l.AddEntry(h_dbv_sum, 'total background:')
l.AddEntry(h_dbv_sum, '  mean d_{BV} = %4.1f #pm %2.1f #mum' % (10000*h_dbv_sum.GetMean(), 10000*h_dbv_sum.GetMeanError()), '')
h_dbv_nob.SetStats(0)
h_dbv_nob.SetLineColor(ROOT.kBlue)
h_dbv_nob.SetLineWidth(3)
h_dbv_nob.DrawNormalized('sames')
l.AddEntry(h_dbv_nob, 'background, no b quarks:')
l.AddEntry(h_dbv_nob, '  mean d_{BV} = %4.1f #pm %2.1f #mum' % (10000*h_dbv_nob.GetMean(), 10000*h_dbv_nob.GetMeanError()), '')
h_dbv_b.SetStats(0)
h_dbv_b.SetLineColor(ROOT.kPink)
h_dbv_b.SetLineWidth(3)
h_dbv_b.DrawNormalized('sames')
l.AddEntry(h_dbv_b, 'background, b quarks:')
l.AddEntry(h_dbv_b, '  mean d_{BV} = %4.1f #pm %2.1f #mum' % (10000*h_dbv_b.GetMean(), 10000*h_dbv_b.GetMeanError()), '')
l.SetFillColor(0)
l.Draw()
ps.save('dbv_b')

print '%d %d-track: difference in mean dBV (b quarks - no b quarks) = %4.1f +/- %2.1f um' % (year, ntk, 10000*h_dbv_b.GetMean() - 10000*h_dbv_nob.GetMean(), ((10000*h_dbv_b.GetMeanError())**2 + (10000*h_dbv_nob.GetMeanError())**2)**0.5)
