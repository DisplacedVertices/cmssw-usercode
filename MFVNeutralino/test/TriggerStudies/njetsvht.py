import sys, os
from array import array
from DVCode.Tools.ROOTTools import *
import DVCode.Tools.Samples as Samples

set_style()
ROOT.gStyle.SetOptStat(0)
ps = plot_saver('plots/QuadJetTrigEff_arc_njetsvht', size=(600,600), log=False)
ROOT.TH1.AddDirectory(0)

data_f = ROOT.TFile('crab/QuadJetTrigEff_arc/SingleMu2012.root')

sigs = Samples.mfv_signal_samples
sigs = [Samples.mfv_neutralino_tau1000um_M0300, Samples.mfv_neutralino_tau1000um_M1000]
for sig in sigs:
    sig.fn = os.path.join('crab/QuadJetTrigEff_arc_sig', sig.name + '.root')
    sig.f = ROOT.TFile(sig.fn)

def get(name, f):
    h = f.Get('Mu14C0pfnum/h_njets_v_ht').Clone(name)
    h.RebinX(2)
    p = h.ProfileX(name + '_prof') #, 1, -1, 's')
    p.SetLineWidth(2)
    p.GetYaxis().SetRangeUser(0, 12)
    p.SetTitle(';PF #Sigma H_{T} (GeV);<# PF jets>')
    return p

data_p = get('data', data_f)
sig_ps = [get(sig.name, sig.f) for sig in sigs]

data_p.Draw()
for isig, sig_p in enumerate(sig_ps):
    sig_p.SetFillStyle(3001)
    sig_p.SetFillColor(2+2*isig)
    sig_p.Draw('E2 same')

ps.save('hi')

    
