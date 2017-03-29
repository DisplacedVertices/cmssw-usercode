from JMTucker.Tools.ROOTTools import *

year = 2016

set_style()
ps = plot_saver('../plots/bkgest/average_eff_%s' % year, size=(700,700), log=False, root=False)

f1 = ROOT.TFile('eff_%s.root' % year)
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

fh = ROOT.TFile('eff_avg_%s.root' % year, 'recreate')
for i in [3,4,5]:
    h1 = f1.Get('maxtk%i'%i)
    hh = f2.Get('ntk%i_deltasvgaus_wevent'%i)
    hh.Rebin(100)
    hh.Scale(0.01)
    hh.SetBinContent(hh.GetNbinsX()+1, hh.GetBinContent(hh.GetNbinsX()))
    h2 = ROOT.TH1F(hh.GetName(), ';d_{VV} (cm);Efficiency', 400, 0, 4)
    h2.SetStats(0)
    for j in range(1, h2.GetNbinsX()+2):
        h2.SetBinContent(j, hh.GetBinContent(j))
    h = ROOT.TH1F('average%i'%i, 'average (%s, %s);d_{VV} (cm);efficiency' % (h1.GetName(), h2.GetName()), 400, 0, 4)
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

f = ROOT.TFile('eff_avg_%s.root' % year)
l = ROOT.TLegend(0.50,0.15,0.85,0.30)
for i in [3,4,5]:
    h = f.Get('average%i'%i)
    h.SetStats(0)
    h.SetLineWidth(3)
    h.SetLineColor(colors[i])
    if i == 3:
        h.SetTitle(';d_{VV} (cm);Efficiency')
        h.GetXaxis().SetRangeUser(0,0.4)
        h.Draw()
    else:
        h.Draw('sames')
    l.AddEntry(h, '%i-track'%i)
l.SetFillColor(0)
l.Draw()
ps.save('average')


ROOT.TH1.AddDirectory(0)

fn1 = ['2v_from_jets_%s_3track_default_v12.root' % year, '2v_from_jets_%s_3track_noclearing_v12.root' % year]
fn2 = ['2v_from_jets_%s_4track_default_v12.root' % year, '2v_from_jets_%s_4track_noclearing_v12.root' % year]
fn3 = ['2v_from_jets_%s_5track_default_v12.root' % year, '2v_from_jets_%s_5track_noclearing_v12.root' % year]

fns = [fn1, fn2, fn3]
ntk = ['3-track', '4-track', '5-track']
n2v = [1323., 22., 1.]

for i in range(3):
    h0 = ROOT.TFile(fns[i][0]).Get('h_c1v_dvv')
    h0.SetTitle(';d_{VV}^{C} (cm);Events')
    h0.SetStats(0)
    h0.SetLineColor(ROOT.kRed)
    h0.SetLineWidth(2)
    h0.Scale(n2v[i]/h0.Integral())
    if i == 2:
        h0.GetYaxis().SetRangeUser(0,0.4)
    h0.Draw('hist e')

    h1 = ROOT.TFile(fns[i][1]).Get('h_c1v_dvv')
    h1.SetStats(0)
    h1.SetLineColor(ROOT.kBlack)
    h1.SetLineWidth(2)
    h1.Scale(n2v[i]/h1.Integral())
    h1.Draw('hist e sames')

    l = ROOT.TLegend(0.35,0.75,0.85,0.85)
    l.AddEntry(h1, 'without efficiency correction')
    l.AddEntry(h0, 'with efficiency correction')
    l.SetFillColor(0)
    l.Draw()
    ps.save(ntk[i])
