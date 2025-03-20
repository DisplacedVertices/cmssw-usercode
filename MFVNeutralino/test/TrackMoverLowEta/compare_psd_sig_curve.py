import ROOT
import sys,os

from JMTucker.Tools.ROOTTools import *
cmssw_setup()

# FIXME you can replace this with the usual stuff for putting plots into our publicweb areas and generating the html
outputdir = "~/nobackup/crabdirs/TMLowEta_PSD_CURVE_M55_ctau1mm_2017p8_VH_March4"
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
h_none_emu_distcurve = none_emu_distcurve.Get('all_closeseedtks_num')
h_none_emu_distcurve.SetStats(0)
h_none_emu_distcurve.SetLineWidth(3)
h_none_emu_distcurve.SetLineColor(ROOT.kBlue)
h_none_emu_distcurve.GetYaxis().SetRangeUser(0.0,1.5)
h_none_emu_distcurve.GetXaxis().SetRangeUser(0.0,45.0)
h_none_emu_distcurve.Draw('L')

pseudo_distcurve  = ROOT.TFile(filename2)  
h_pseudo_distcurve = pseudo_distcurve.Get('all_closeseedtks_num')
h_pseudo_distcurve.SetStats(0)
h_pseudo_distcurve.SetLineWidth(3)
h_pseudo_distcurve.SetLineColor(ROOT.kViolet+1)
h_pseudo_distcurve.GetYaxis().SetRangeUser(0.0,1.5)
h_pseudo_distcurve.GetXaxis().SetRangeUser(0.0,45.0)
h_pseudo_distcurve.Draw('L same')

legend = ROOT.TLegend(0.28,0.195,0.880,0.435)
legend.AddEntry(h_none_emu_distcurve, "signal MC TOC", "L")
if ("emu_scale_toc" in filename2):
    legend.AddEntry(h_pseudo_distcurve, "signal MC TOC scaled to TM MC/signal MC", "L")
elif ("scale_toc" in filename2):
    legend.AddEntry(h_pseudo_distcurve, "signal MC TOC scaled to TM data/TM MC", "L")
elif ("emu_slide_toc" in filename2):
    legend.AddEntry(h_pseudo_distcurve, "signal MC TOC slided by 65% bin difference of signal MC to TM MC", "L")
elif ("slide_toc" in filename2):
    legend.AddEntry(h_pseudo_distcurve, "signal MC TOC slided by 65% bin difference of TM MC to TM data", "L")
else:
    legend.AddEntry(h_pseudo_distcurve, "TM data TOC", "L")
legend.Draw()
#gPad->BuildLegend(0.48,0.295,0.880,0.535,"","l");
w = ROOT.TLatex()
w.SetNDC()
if ("emulation" in fileoutname):
    w.DrawLatex(.3, .85, " signal MC with quarks' |#eta| < 1.5")
    #w.DrawLatex(.3, .80, " LLP 3D-separation > 1mm")
else:
    w.DrawLatex(.3, .85, " signal MC with quarks' |#eta| < 1.5")
c1.Print (outputdir+fileoutname+".png")


#c1.Print (outputdir+"emu_curve_comp.png")
