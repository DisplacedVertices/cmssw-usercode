import os,sys
import ROOT

dirpath = "/uscms/home/joeyr/crabdirs/TrigEff2017v0p6/"
#dirpath = "/uscms/home/joeyr/crabdirs/TrigEff2017v0p6_require6jets/"
#dirpath = "/uscms/home/joeyr/crabdirs/TrigEff2017v0p5_tighterbjetpt/"

dibjet_nums = [
"numDoublePFJets100MaxDeta1p6_DoubleCaloBTagCSV_inc_tight_meas_leg0",
"numDoublePFJets100MaxDeta1p6_DoubleCaloBTagCSV_inc_tight_meas_leg1",
]

dibjet_dens = [
"denDoublePFJets100MaxDeta1p6_DoubleCaloBTagCSV_inc_tight_meas_leg0",
"denDoublePFJets100MaxDeta1p6_DoubleCaloBTagCSV_inc_tight_meas_leg1",
]

tribjet_nums = [
"numPFHT300PT30_QuadPFJet_75_60_45_40_TriplePFBTagCSV_inc_tight_meas_leg0",
"numPFHT300PT30_QuadPFJet_75_60_45_40_TriplePFBTagCSV_inc_tight_meas_leg1",
"numPFHT300PT30_QuadPFJet_75_60_45_40_TriplePFBTagCSV_inc_tight_meas_leg2",
]

tribjet_dens = [
"denPFHT300PT30_QuadPFJet_75_60_45_40_TriplePFBTagCSV_inc_tight_meas_leg0",
"denPFHT300PT30_QuadPFJet_75_60_45_40_TriplePFBTagCSV_inc_tight_meas_leg1",
"denPFHT300PT30_QuadPFJet_75_60_45_40_TriplePFBTagCSV_inc_tight_meas_leg2",
]

hnames = ["h_bjet_leg_pt", "h_bjet_leg_eta"]

ls = os.listdir(dirpath)

for fname in ls :

    # only want root files
    if not fname.endswith(".root") : continue

    f = ROOT.TFile(dirpath+fname, "UPDATE")
    f.cd()

    for hname in hnames :
    
        dibjet_nums_hists = [f.Get(dibjet_num+"/"+hname) for dibjet_num in dibjet_nums]
        dibjet_dens_hists = [f.Get(dibjet_den+"/"+hname) for dibjet_den in dibjet_dens]
        tribjet_nums_hists = [f.Get(tribjet_num+"/"+hname) for tribjet_num in tribjet_nums]
        tribjet_dens_hists = [f.Get(tribjet_den+"/"+hname) for tribjet_den in tribjet_dens]

        dibjet_nums_hist = dibjet_nums_hists[0].Clone(hname+"_dibjet_nums")
        dibjet_nums_hist.Reset()
        dibjet_dens_hist = dibjet_dens_hists[0].Clone(hname+"_dibjet_dens")
        dibjet_dens_hist.Reset()
        tribjet_nums_hist = tribjet_nums_hists[0].Clone(hname+"_tribjet_nums")
        tribjet_nums_hist.Reset()
        tribjet_dens_hist = tribjet_dens_hists[0].Clone(hname+"_tribjet_dens")
        tribjet_dens_hist.Reset()

        for hist in dibjet_nums_hists :
            dibjet_nums_hist.Add(hist)
        for hist in dibjet_dens_hists :
            dibjet_dens_hist.Add(hist)
        for hist in tribjet_nums_hists :
            tribjet_nums_hist.Add(hist)
        for hist in tribjet_dens_hists :
            tribjet_dens_hist.Add(hist)

        f.Write() 
