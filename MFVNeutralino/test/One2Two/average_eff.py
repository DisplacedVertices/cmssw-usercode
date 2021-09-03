from DVCode.Tools.ROOTTools import *
ROOT.TH1.AddDirectory(0)

year = 2016

set_style()
ps = plot_saver('../plots/bkgest/v14/average_eff_%s' % year, size=(700,700), log=False, root=False)

f1 = ROOT.TFile('eff_%s_v14.root' % year)
f2 = ROOT.TFile('~tucker/public/mfv/overlay_eff_v14.root')

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

for n in ['overlay_']:
    l = ROOT.TLegend(0.50,0.15,0.85,0.30)
    for i in [3,4,5]:
        h = f2.Get('%sntk%i' % (n,i))
        h.SetStats(0)
        h.SetLineColor(colors[i])
        if i == 3:
            h.SetTitle('%sntk;d_{VV} (cm);efficiency' % n)
            h.Draw()
        else:
            h.Draw('sames')
        l.AddEntry(h, h.GetName())
    l.SetFillColor(0)
    l.Draw()
    ps.save('%sntk' % n)

for i in [3,4,5]:
    h1 = f1.Get('maxtk%i'%i)
    h1.SetTitle('%i-track;d_{VV} (cm);Efficiency'%i)
    h1.SetLineColor(ROOT.kRed)
    h1.SetLineWidth(3)
    h1.Draw()

    h2 = f2.Get('overlay_ntk%i'%i)
    h2.SetStats(0)
    h2.SetLineColor(ROOT.kBlue)
    h2.SetLineWidth(3)
    h2.Draw('sames')

    l = ROOT.TLegend(0.50,0.15,0.85,0.30)
    l.AddEntry(h1, 'vertexer method')
    l.AddEntry(h2, 'overlay method')
    l.Draw()
    ps.save('ntk%i'%i)
 
    h1.GetXaxis().SetRangeUser(0,0.4)
    h1.Draw('hist')
    h2.Draw('sames')
    l.Draw()
    ps.save('ntk%i_zoom'%i)

for i in [3,4,5]:
    h1 = ROOT.TFile('eff_%itkseeds_%s_v14.root' % (i,year)).Get('maxtk%i'%i)
    h1.SetTitle('%i-track;d_{VV} (cm);Efficiency'%i)
    h1.SetLineColor(ROOT.kRed)
    h1.SetLineWidth(3)
    h1.Draw()

    h2 = f2.Get('overlay_ntk%i'%i)
    h2.SetStats(0)
    h2.SetLineColor(ROOT.kBlue)
    h2.SetLineWidth(3)
    h2.Draw('sames')

    l = ROOT.TLegend(0.50,0.15,0.85,0.30)
    l.AddEntry(h1, 'ntkseeds method')
    l.AddEntry(h2, 'overlay method')
    l.Draw()
    ps.save('ntkseeds%i'%i)

    h1.GetXaxis().SetRangeUser(0,0.4)
    h1.Draw('hist')
    h2.Draw('sames')
    l.Draw()
    ps.save('ntkseeds%i_zoom'%i)


for n in ['']:
    l = ROOT.TLegend(0.50,0.15,0.85,0.30)
    for i in [3,4,5]:
        h = f1.Get('maxtk%i%s' % (i,n))
        h.SetLineColor(colors[i])
        h.SetLineWidth(3)
        h.Scale(1./h.GetBinContent(10))
        h.GetXaxis().SetRangeUser(0,0.1)
        h.GetYaxis().SetRangeUser(0,1)
        if i == 3:
            h.SetTitle('maxtk%s;d_{VV} (cm);efficiency' % n)
            h.Draw('hist')
        else:
            h.Draw('hist sames')
        l.AddEntry(h, h.GetName())
    l.SetFillColor(0)
    l.Draw()
    ps.save('maxtk%s_zoom' % n)

for n in ['overlay_']:
    l = ROOT.TLegend(0.50,0.15,0.85,0.30)
    for i in [3,4,5]:
        h = f2.Get('%sntk%i' % (n,i))
        h.SetStats(0)
        h.SetLineColor(colors[i])
        h.SetLineWidth(3)
        h.Scale(1./h.GetBinContent(10))
        h.GetXaxis().SetRangeUser(0,0.1)
        h.GetYaxis().SetRangeUser(0,1)
        if i == 3:
            h.SetTitle('%sntk;d_{VV} (cm);efficiency' % n)
            h.Draw()
        else:
            h.Draw('sames')
        l.AddEntry(h, h.GetName())
    l.SetFillColor(0)
    l.Draw()
    ps.save('%sntk_zoom' % n)
