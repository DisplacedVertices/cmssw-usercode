import ROOT
import sys,os

from JMTucker.Tools.ROOTTools import *
cmssw_setup()

# FIXME you can replace this with the usual stuff for putting plots into our publicweb areas and generating the html
outputdir = "~/nobackup/crabdirs/TMLowEta_PSD_DVV_Dec5"
outputdir += "/" # in case we forget it...
os.system("mkdir -p "+outputdir)

filename1 = sys.argv[1]
filename2 = sys.argv[2]
fileoutname = sys.argv[3] 

# FIXME should be able to do the same for our mfv events, just didn't do anything with it yet
#event_handle1  = Handle ("MFVEvent")
#event_label1 = ("mfvEvent")

# Create histograms, etc.
ROOT.gROOT.SetBatch() # don't pop up canvases

# create an output root file
distcurve = ROOT.TFile(outputdir+fileoutname+".root", "RECREATE")
curve = ROOT.TFile(outputdir+fileoutname+".root", "RECREATE")

c1 = ROOT.TCanvas()
none_emu_distcurve  = ROOT.TFile(filename1)  
h_none_emu_distcurve = none_emu_distcurve.Get('all_dvv_den')
h_none_emu_distcurve.SetStats(0)
h_none_emu_distcurve.SetLineWidth(3)
h_none_emu_distcurve.SetLineColor(ROOT.kRed)
h_none_emu_distcurve.GetYaxis().SetRangeUser(0.0,0.04)
#h_none_emu_distcurve.GetXaxis().SetRangeUser(0.0,1.0)
h_none_emu_distcurve.Draw('L')

pseudo_distcurve  = ROOT.TFile(filename2)  
h_pseudo_distcurve = pseudo_distcurve.Get('all_dvv_den')
h_pseudo_distcurve.SetStats(0)
h_pseudo_distcurve.SetLineWidth(3)
h_pseudo_distcurve.SetLineColor(ROOT.kGreen+3)
h_pseudo_distcurve.GetYaxis().SetRangeUser(0.0,0.04)
#h_pseudo_distcurve.GetXaxis().SetRangeUser(0.0,1.0)
h_pseudo_distcurve.Draw('L same')


legend = ROOT.TLegend(0.38,0.195,0.980,0.435)
if ("dvv_slide_toc_curve.root" == filename2):
    legend.AddEntry(h_pseudo_distcurve, "signal MC TOC shifted by 100um", "L")
    legend.AddEntry(h_none_emu_distcurve, "signal MC TOC", "L")
elif("dvv_slide_toc_curvedist.root" == filename2):
    legend.AddEntry(h_pseudo_distcurve, "GEN dVV x signal MC TOC shifted by 100um", "L")
    legend.AddEntry(h_none_emu_distcurve, "GEN dVV x signal MC TOC", "L")
elif("dvv_none_norm.root" == filename1):
    legend.AddEntry(h_pseudo_distcurve, "GEN dVV", "L")
    legend.AddEntry(h_none_emu_distcurve, "GEN dVV", "L")
else:
    print("something wrong")
#if("dvv_scale_toc_curve.root" == filename1):
#    legend.AddEntry(h_pseudo_distcurve, "signal MC TOC shifted by +100 um", "L")
#    legend.AddEntry(h_none_emu_distcurve, "signal MC TOC scaled by 16% down", "L")
#    legend.AddEntry(h_dvv_distcurve, "signal MC TOC", "L")
#else:
#    print("something wrong")
legend.Draw()
#gPad->BuildLegend(0.48,0.295,0.880,0.535,"","l");
w = ROOT.TLatex()
w.SetNDC()
w.DrawLatex(.3, .85, " signal MC with quarks' |#eta| < 1.5")
#w.DrawLatex(.3, .80, " LLP 3D-separation < 0.5 cm")
c1.Print (outputdir+fileoutname+".png")


#c1.Print (outputdir+"emu_curve_comp.png")
