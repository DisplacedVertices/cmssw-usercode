#!/usr/bin/env python

from JMTucker.Tools.ROOTTools import *
import JMTucker.Tools.Samples as Samples
import JMTucker.MFVNeutralino.AnalysisConstants as ac

set_style()

ntk = 5
tree_path = 'mfvMiniTree/t'
if ntk == 3:
    tree_path = 'tre33/t'
if ntk == 4:
    tree_path = 'tre44/t'

path = 'MinitreeV11/2016'
ps = plot_saver('../../plots/bkgest/%s_ntk%i' % (path, ntk), size=(700,700), root=False)
trees = '/uscms_data/d2/tucker/crab_dirs/%s' % path

def book_dbv(n):
    return ROOT.TH1F(n, '', 40, 0, 0.2)

sc = ac.int_lumi * ac.scale_factor

h_dbv_sum = book_dbv('dbv_sum')
h_dbv_nob = book_dbv('dbv_nob')
h_dbv_b = book_dbv('dbv_b')
h_dbv_qcdb = book_dbv('dbv_qcdb')

hs_nob = []
for sn in 'qcdht0700sum qcdht1000sum qcdht1500sum qcdht2000sum ttbar'.split():
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
for sn in 'qcdht0700sum qcdht1000sum qcdht1500sum qcdht2000sum ttbar'.split():
    f = ROOT.TFile('%s/%s.root' % (trees,sn))
    t = f.Get(tree_path)
    s = getattr(Samples, sn)

    if sn != 'ttbar':
        n = sn + ', b quarks'
    else:
        n = sn
    h_dbv = book_dbv(n)
    t.Draw('dist0>>%s' % n, 'nvtx == 1 && gen_flavor_code == 2')
    h_dbv_sum.Add(h_dbv, sc * s.partial_weight_orig)
    h_dbv_b.Add(h_dbv, sc * s.partial_weight_orig)
    if sn != 'ttbar':
        h_dbv_qcdb.Add(h_dbv, sc * s.partial_weight_orig)
    ps.save(n)

    h = h_dbv.Clone()
    h.SetDirectory(0)
    hs_b.append(h)

h_dbv_sum.Draw()
ps.save('dbv_sum')


h_dbv_sum.SetTitle('%s-track one-vertex events;d_{BV} (cm);arb. units' % ntk)
h_dbv_sum.SetStats(0)
h_dbv_sum.SetLineColor(ROOT.kBlack)
h_dbv_sum.SetLineWidth(3)
h_dbv_sum.Scale(1./h_dbv_sum.Integral())
h_dbv_sum.GetYaxis().SetRangeUser(1e-5,1)
h_dbv_sum.Draw()

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


h_dbv_sum.Draw()
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
hs_b[4].DrawNormalized('sames')
l.AddEntry(hs_b[4], 'ttbar: mean d_{BV} = %4.1f #pm %2.1f #mum' % (10000*hs_b[4].GetMean(), 10000*hs_b[4].GetMeanError()))
l.SetFillColor(0)
l.Draw()
ps.save('dbv_qcdb')


h_dbv_sum.Draw()
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

print '%d-track: difference in mean dBV (b quarks - no b quarks) = %4.1f +/- %2.1f um' % (ntk, 10000*h_dbv_b.GetMean() - 10000*h_dbv_nob.GetMean(), ((10000*h_dbv_b.GetMeanError())**2 + (10000*h_dbv_nob.GetMeanError())**2)**0.5)
