#!/usr/bin/env python

from base import *

fn_pattern = 'jen_crab/mfv*root'
plot_dir = 'plots/o2t_signal_templates'
binning = [0.02*i for i in xrange(5)] + [0.1, 0.2, 0.4, 0.8, 1.6, 3.2]
binning = array('d', binning)
nbins = len(binning) - 1
min_ntracks = 5

ps = plot_saver(plot_dir, size=(1000,600))

fns = glob.glob(fn_pattern)
fns.sort()

hs = []

colors = [2,3,4,6]
titles = [
    '#tau = 100 #mum',
    '#tau = 300 #mum',
    '#tau = 1 mm',
    '#tau = 9.9 mm',
    ]
first = True
leg = ROOT.TLegend(0.502, 0.620, 0.848, 0.861)


f = ROOT.TFile('allbkg.root')
h = f.Get('ClearedJetsTemplater/seed0000_toy0000/templates/imu_21/h_template_imu021_isig009')
h.SetStats(0)
h.SetLineWidth(2)
h.GetXaxis().SetRangeUser(2e-2, 3.2)
h.Scale(1/h.Integral())
h.SetTitle(';d_{VV} (cm);frac. / bin width')
for ibin in xrange(1, h.GetNbinsX()+1):
    h.SetBinContent(ibin, h.GetBinContent(ibin) / h.GetBinWidth(ibin))
h.Draw('hist e')
h.SetDirectory(0)
hs.append(h)
leg.AddEntry(h, 'Bkg: #mu_{clear} = 210 #mum, #sigma_{clear} = 50 #mum', 'L')

for fn in fns:
    if 'M0400' not in fn:
        continue

    print fn
    sig_name = os.path.basename(fn).replace('.root','')
    f, t = get_f_t(fn, None)
    
    name = 'h_sig_ntk%i_%s' % (min_ntracks, sig_name)
    h = ROOT.TH1D(name, '', nbins, binning)
    h.SetDirectory(0)
    hs.append(h)
    x = detree(t, 'svdist', 'nvtx >= 2 && ntk0 >= %i && ntk1 >= %i' % (min_ntracks, min_ntracks), lambda x: (float(x[0]),))
    for (d,) in x:
        if d > 3.2:
            d = 3.2-1e-4
        h.Fill(d)

    h.Scale(1./h.Integral())
    for ibin in xrange(1, nbins+1):
        h.SetBinContent(ibin, h.GetBinContent(ibin) / h.GetBinWidth(ibin))
    h.SetTitle(';d_{VV} (cm);frac. / bin width')
    h.SetStats(0)
    h.GetXaxis().SetRangeUser(2e-2,3.2)
    h.SetLineColor(colors.pop(0))
    h.SetLineWidth(2)
    h.Draw('same hist e')
    leg.AddEntry(h, 'Sig: ' + titles.pop(0), 'L')

leg.SetBorderSize(0)
leg.Draw()
ps.c.SetLogx()
ps.save(name)
