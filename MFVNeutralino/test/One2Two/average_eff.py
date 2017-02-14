from JMTucker.Tools.ROOTTools import *
set_style()
ps = plot_saver('../plots/bkgest/average_eff', size=(700,700), log=False, root=False)

f1 = ROOT.TFile('eff.root')
f2 = ROOT.TFile('~tucker/public/export_smoothed.root')

colors = [0, 0, 0, ROOT.kRed, ROOT.kBlue, ROOT.kGreen+2]
for n in ['', '_merge']:
    l = ROOT.TLegend(0.50,0.15,0.85,0.30)
    for i in [3,4,5]:
        h = f1.Get('maxtk%i%s' % (i,n))
        h.SetLineColor(colors[i])
        if i == 3:
            h.SetTitle('maxtk%s;d_{VV} (cm);efficiency' % n)
            h.Draw()
        else:
            h.Draw('sames')
        l.AddEntry(h, h.GetName())
    l.SetFillColor(0)
    l.Draw()
    ps.save('maxtk%s' % n)

for n in ['', '_wevent', '_deltasvgaus', '_deltasvgaus_wevent']:
    l = ROOT.TLegend(0.50,0.15,0.85,0.30)
    for i in [3,4,5]:
        h = f2.Get('ntk%i%s' % (i,n))
        h.SetStats(0)
        h.SetLineColor(colors[i])
        if i == 3:
            h.SetTitle('ntk%s;d_{VV} (cm);efficiency' % n)
            h.Draw()
        else:
            h.Draw('sames')
        l.AddEntry(h, h.GetName())
    l.SetFillColor(0)
    l.Draw()
    ps.save('ntk%s' % n)

fh = ROOT.TFile('eff_avg.root', 'recreate')
for i in [3,4,5]:
    h1 = f1.Get('maxtk%i'%i)
    hh = f2.Get('ntk%i_deltasvgaus_wevent'%i)
    hh.Rebin(100)
    hh.Scale(0.01)
    hh.SetBinContent(hh.GetNbinsX()+1, hh.GetBinContent(hh.GetNbinsX()))
    h2 = ROOT.TH1F(hh.GetName(), ';d_{VV} (cm);Efficiency', 100, 0, 1)
    h2.SetStats(0)
    for j in range(1, h2.GetNbinsX()+2):
        h2.SetBinContent(j, hh.GetBinContent(j))
    h = ROOT.TH1F('average%i'%i, 'average (%s, %s);d_{VV} (cm);efficiency' % (h1.GetName(), h2.GetName()), 100, 0, 1)
    h.SetStats(0)
    h.GetYaxis().SetRangeUser(0,1.05)
    for j in range(1, h.GetNbinsX()+2):
        h.SetBinContent(j, 0.5 * (h1.GetBinContent(j) + h2.GetBinContent(j)))
    h1.SetLineColor(ROOT.kRed)
    h2.SetLineColor(ROOT.kBlue)
    h.SetLineColor(ROOT.kViolet)
    h.Draw()
    h1.Draw('sames')
    h2.Draw('sames')
    l = ROOT.TLegend(0.50,0.15,0.85,0.30)
    l.AddEntry(h1, h1.GetName())
    l.AddEntry(h2, h2.GetName())
    l.AddEntry(h, 'average')
    l.SetFillColor(0)
    l.Draw()
    ps.save(h.GetName())
 
    fh.cd()
    h.Write()

    if i == 5:
        h.SetTitle(';d_{VV} (cm);Efficiency')
        h.GetXaxis().SetRangeUser(0,0.4)
        h.SetLineWidth(3)
        h.Draw()
        ps.save('efficiency5')

        h1.SetLineWidth(3)
        h2.SetLineWidth(3)
        h1.Draw('hist sames')
        h2.Draw('sames')
        l = ROOT.TLegend(0.50,0.15,0.85,0.30)
        l.AddEntry(h1, 'vertexer method')
        l.AddEntry(h2, 'overlay method')
        l.AddEntry(h, 'average')
        l.SetFillColor(0)
        l.Draw()
        ps.save('compare_efficiency')

fh.Close()

f = ROOT.TFile('eff_avg.root')
for n in ['']:
    l = ROOT.TLegend(0.50,0.15,0.85,0.30)
    for i in [3,4,5]:
        h = f.Get('average%i%s' % (i,n))
        h.SetStats(0)
        h.SetLineColor(colors[i])
        if i == 3:
            h.SetTitle('average%s;d_{VV} (cm);efficiency' % n)
            h.Draw()
        else:
            h.Draw('sames')
        l.AddEntry(h, h.GetName())
    l.SetFillColor(0)
    l.Draw()
    ps.save('average%s' % n)
