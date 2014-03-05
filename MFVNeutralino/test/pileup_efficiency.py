#!/usr/bin/env python

from JMTucker.Tools.ROOTTools import ROOT, histogram_divide

samples = ["mfv_neutralino_tau0100um_M0400", "mfv_neutralino_tau1000um_M0400", "ttbarhadronic", "ttbarsemilep", "ttbardilep", "qcdht0100", "qcdht0250", "qcdht0500", "qcdht1000"]
for sample in samples:
    file = ROOT.TFile("crab/PileupV11/%s_mangled.root" % sample)
    max1 = 0
    for i in range(file.ABCD.GetNbinsX()):
        if (file.trigger.GetBinContent(i+1) == 0):
            continue
        if (file.ABCD.GetBinContent(i+1)/file.trigger.GetBinContent(i+1)):
            max1 = file.ABCD.GetBinContent(i+1)/file.trigger.GetBinContent(i+1)
    max2 = 0
    for i in range(file.tight.GetNbinsX()):
        if (file.trigger.GetBinContent(i+1) == 0):
            continue
        if (file.tight.GetBinContent(i+1)/file.trigger.GetBinContent(i+1)):
            max2 = file.tight.GetBinContent(i+1)/file.trigger.GetBinContent(i+1)
    c1 = ROOT.TCanvas()
    c1.Divide(2,2)
    c1.cd(1)
    eff1 = histogram_divide(file.ABCD, file.nocuts)
    eff1.SetTitle("ABCD_nocuts")
#    max = 0
#    for i in range(file.ABCD.GetNbinsX()):
#        if (file.nocuts.GetBinContent(i+1) == 0):
#            continue
#        if (file.ABCD.GetBinContent(i+1)/file.nocuts.GetBinContent(i+1)):
#            max = file.ABCD.GetBinContent(i+1)/file.nocuts.GetBinContent(i+1)
    eff1.SetMaximum(max1)
    eff1.Draw("AP")
    c1.cd(2)
    eff2 = histogram_divide(file.ABCD, file.trigger)
    eff2.SetTitle("ABCD_trigger")
    eff2.SetMaximum(max1)
    eff2.Draw("AP")
    c1.cd(3)
    eff3 = histogram_divide(file.tight, file.nocuts)
    eff3.SetTitle("tight_nocuts")
#    for i in range(file.ABCD.GetNbinsX()):
#        if (file.nocuts.GetBinContent(i+1) == 0):
#            continue
#        if (file.tight.GetBinContent(i+1)/file.nocuts.GetBinContent(i+1)):
#            max = file.tight.GetBinContent(i+1)/file.nocuts.GetBinContent(i+1)
    eff3.SetMaximum(max2)
    eff3.Draw("AP")
    c1.cd(4)
    eff4 = histogram_divide(file.tight, file.trigger)
    eff4.SetTitle("tight_trigger")
#    for i in range(file.ABCD.GetNbinsX()):
#        if (file.trigger.GetBinContent(i+1) == 0):
#            continue
#        if (file.tight.GetBinContent(i+1)/file.trigger.GetBinContent(i+1)):
#            max = file.tight.GetBinContent(i+1)/file.trigger.GetBinContent(i+1)
    eff4.SetMaximum(max2)
    eff4.Draw("AP")
    c1.SaveAs("plots/PileupEfficiency/%s.pdf" % sample)
