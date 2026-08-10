mass = 800

from JMTucker.Tools.ROOTTools import *
set_style()
ps = plot_saver(plot_dir('trigeff_weights_M%i' % mass))

ROOT.gStyle.SetOptStat(0)

fdata = ROOT.TFile('/uscms_data/d2/tucker/crab_dirs/TrigEffv6/SingleMuon2016BthruG.root')
fsig  = ROOT.TFile('/uscms_data/d2/tucker/crab_dirs/TrigEffv6/official_mfv_neu_tau01000um_M%04i.root' % mass)

hdata = fdata.Get('denht1000'  '/h_jetpt2v1')
hsig  = fsig .Get('dennomuht1000/h_jetpt2v1')

def deoverflow(h):
    assert h.GetNbinsX() == 5 and h.GetNbinsY() == 5
    for j in range(1,5):
        c = h.GetBinContent(5,j)
        h.SetBinContent(5,j, c + h.GetBinContent(6,j))
    h.SetBinContent(4,5, h.GetBinContent(4,5) + h.GetBinContent(4,6))
    h.SetBinContent(5,5, h.GetBinContent(5,5) + h.GetBinContent(5,6) + h.GetBinContent(6,6) + h.GetBinContent(6,5))

deoverflow(hdata)
deoverflow(hsig)

hdata.Draw('colz text00')
ps.save('data', logz=True)
hsig.Draw('colz text00')
ps.save('sig', logz=True)

hrat = hsig.Clone('hrat')
hrat.Scale(1./hrat.GetEntries())
hdata.Scale(1./hdata.GetEntries())
hrat.Divide(hdata)
hrat.Draw('colz text00')
ps.save('rat', logz=True)

xax = hrat.GetXaxis()
yax = hrat.GetYaxis()
for i in xrange(1,6):
    jetpt1 = xax.GetBinLowEdge(i), xax.GetBinLowEdge(i+1)
    for j in xrange(1,6):
        jetpt2 = yax.GetBinLowEdge(j), yax.GetBinLowEdge(j+1)
        c = hrat.GetBinContent(i,j)
        if c == 0:
            c = 1e-6
        if i == 5 and j == 5:
            print 'else if (jetpt1 >= %3.f && jetpt2 >= %3.f) return %e;' % (jetpt1[0], jetpt2[0], c)
        elif j == 5:
            print 'else if (jetpt1 >= %3.f && jetpt1 < %3.f && jetpt2 >= %3.f) return %e;' % (jetpt1[0], jetpt1[1], jetpt2[0], c)
        elif i == 5:
            print 'else if (jetpt1 >= %3.f && jetpt2 >= %3.f && jetpt2 < %3.f) return %e;' % (jetpt1[0], jetpt2[0], jetpt2[1], c)
        else:
            ex = 'if     ' if i == 1 and j == 1 else 'else if' 
            print '%s (jetpt1 >= %3.f && jetpt1 < %3.f && jetpt2 >= %3.f && jetpt2 < %3.f) return %e;' % (ex, jetpt1[0], jetpt1[1], jetpt2[0], jetpt2[1], c)

