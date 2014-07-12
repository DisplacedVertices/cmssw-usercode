from JMTucker.Tools.ROOTTools import *
set_style()
ps = plot_saver('plots/o2t_interp', size=(600,600))

f = ROOT.TFile('one2two_sampleall_sigcontam2_sigscale10.root')

xmax = 0.1
rebin = 4

hists = [f.Get('mfvOne2Two/h_1v_template_phi%i' % i) for i in xrange(25)]
diffs = []
rats = []

for i in xrange(24,-1,-1):
    h = hists[i]
    h.Rebin(rebin)
    h.SetLineColor(ROOT.kRed+i)
    h.GetXaxis().SetRangeUser(0, xmax)
    h.SetStats(0)
    h.SetTitle('')
    print '%02i: %f' % (i, h.Integral())
    h.Scale(1/h.Integral())
    if i == 24:
        h.Draw('hist')
    else:
        h.Draw('hist same')

ps.save('all')

for i in xrange(23):
    h0, h1, h2 = hists[i:i+3]
    name = 'hint%i' % (i+1)
    hint = h0.Clone(name)
    hint.SetLineColor(ROOT.kBlue)
    h1.SetLineColor(ROOT.kBlack)
    hint.Scale(0.5)
    hint.Add(h2, 0.5)
    hint.Draw()
    h1.Draw('same')
    ps.save(name)

    hdiff = hint.Clone(name + '_diff')
    diffs.append(hdiff)
    hdiff.Add(h1,-1)
    hdiff.Draw()
    l = ROOT.TLine(0, 0, xmax, 0)
    l.SetLineStyle(ROOT.kDashed)
    l.Draw()
    ps.save(name + '_diff')

    hrat = hint.Clone(name + '_rat')
    rats.append(hrat)
    hrat.Divide(h1)
    hrat.Draw()
    l = ROOT.TLine(0, 1, xmax, 1)
    l.SetLineStyle(ROOT.kDashed)
    l.Draw()
    ps.save(name + '_rat')


for i,h in enumerate(diffs):
    h.SetLineColor(ROOT.kRed+i)
    h.SetLineWidth(2)
    if i == 0:
        h.Draw('hist')
    else:
        h.Draw('hist same')

ps.save('diffs')


for i,h in enumerate(rats):
    h.SetLineColor(ROOT.kRed+i)
    h.SetLineWidth(2)
    if i == 0:
        h.Draw('hist')
    else:
        h.Draw('hist same')

ps.save('rats')
