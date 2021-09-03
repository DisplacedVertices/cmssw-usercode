from array import array
from DVCode.Tools.ROOTTools import *
from DVCode.Tools.Samples import ttbar
import DVCode.MFVNeutralino.AnalysisConstants as ac 

set_style()
ps = plot_saver('plots/negweights', size=(600,600))

f = ROOT.TFile('/uscms_data/d2/tucker/crab_dirs/MinitreeV6_testweights/testweights_ttbar.root')

h_norm = f.Get('mfvWeight/h_sums')
nevents_total = h_norm.GetBinContent(1)
sum_weight_total = h_norm.GetBinContent(2)
sum_weight = h_norm.GetBinContent(7)

partial_weight = ttbar.xsec * ac.int_lumi

t = f.Get('mfvMiniTree/t')

N1v, n1v, N2v, n2v = 0,0,0,0
for nvtx, weight in detree(t, 'nvtx:weight', xform=lambda x: (int(x[0]), float(x[1]))):
    if nvtx == 1:
        N1v += 1
        n1v += weight
    else:
        N2v += 1
        n2v += weight

old_weight = partial_weight / nevents_total
new_weight = partial_weight / sum_weight_total

eN1v = N1v**0.5 * old_weight # same e for n (skellam)
eN2v = N2v**0.5 * old_weight
print 'old prediction (ignoring weight signs):'
print '#1v: %5.1f +- %5.1f' % (N1v * old_weight, eN1v)
print '#2v: %5.2f +- %5.2f' % (N2v * old_weight, eN2v)
print 'new prediction (using weight signs):'
print '#1v: %5.1f +- %5.1f' % (n1v * new_weight, eN1v)
print '#2v: %5.2f +- %5.2f' % (n2v * new_weight, eN2v)

dbv_binses = [    
    ('old', [j*0.005 for j in range(8)] + [0.04, 0.05, 0.06, 0.07, 0.085, 0.1, 0.2, 0.4]),
    ('rdx', [j*0.005 for j in range(7)] + [0.035, 0.4]),
    ]

for name, dbv_bins in dbv_binses:
    dbv_bins = array('d', dbv_bins)
    n_dbv_pos = 'h_dbv_pos_' + name
    n_dbv_neg = 'h_dbv_neg_' + name
    h_dbv_pos = ROOT.TH1F(n_dbv_pos, ';d_{BV} (cm);raw events', len(dbv_bins)-1, dbv_bins)
    h_dbv_neg = ROOT.TH1F(n_dbv_neg, ';d_{BV} (cm);raw events', len(dbv_bins)-1, dbv_bins)

    t.Draw('dist0>>' + n_dbv_pos, 'nvtx==1 && weight > 0')
    t.Draw('dist0>>' + n_dbv_neg, 'nvtx==1 && weight < 0')
    h_dbv_pos.SetLineColor(ROOT.kBlue)
    h_dbv_neg.SetLineColor(ROOT.kRed)
    h_dbv_pos.SetLineWidth(2)
    h_dbv_neg.SetLineWidth(2)
    h_dbv_pos.Draw()
    h_dbv_neg.Draw('sames')
    ps.c.Update()
    differentiate_stat_box(h_dbv_pos, 0, new_size=(0.2, 0.2))
    differentiate_stat_box(h_dbv_neg, 1, new_size=(0.2, 0.2))
    ps.save('dbv_pos_neg_' + name)

    h_dbv = h_dbv_pos.Clone('h_dbv_' + name)
    h_dbv.Add(h_dbv_neg, -1)
    h_dbv.Draw()
    ps.save('dbv_' + name)

    for ibin in xrange(1, h_dbv.GetNbinsX()+1):
        c = h_dbv.GetBinContent(ibin)
        h_dbv.SetBinContent(ibin, c / h_dbv.GetBinWidth(ibin))
    h_dbv.GetYaxis().SetTitle('events/bin width')
    h_dbv.Draw()
    ps.save('dbv_scale_' + name)

t.Draw('svdist>>h_dvv_pos(100, 0, 0.1)', 'nvtx >= 2 && weight > 0')
t.Draw('svdist>>h_dvv_neg(100, 0, 0.1)', 'nvtx >= 2 && weight < 0')
ROOT.h_dvv_pos.SetTitle(';d_{VV} (cm);events')
ROOT.h_dvv_pos.SetLineColor(ROOT.kBlue)
ROOT.h_dvv_neg.SetLineColor(ROOT.kRed)
ROOT.h_dvv_pos.SetLineWidth(2)
ROOT.h_dvv_neg.SetLineWidth(2)
ROOT.h_dvv_pos.Draw()
ROOT.h_dvv_neg.Draw('sames')
ps.c.Update()
differentiate_stat_box(ROOT.h_dvv_pos, 0, new_size=(0.2, 0.2))
differentiate_stat_box(ROOT.h_dvv_neg, 1, new_size=(0.2, 0.2))
ps.save('dvv_pos_neg')

