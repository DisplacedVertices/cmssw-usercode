from JMTucker.Tools.ROOTTools import *
set_style()
ROOT.TH1.AddDirectory(0)

fdata = ROOT.TFile('/publicweb/t/tucker/asdf/plots/v0bkgsub_beforeFR/!!cmp/loose_h_track_dxybs_JetHT2016BCDEF_JetHT2016GH/cmp.root')
fmc   = ROOT.TFile('/publicweb/t/tucker/asdf/plots/v0bkgsub_beforeFR/!!cmp/loose_h_track_dxybs_qcdht1000and1500_hip1p0_mit_qcdht1000and1500/cmp.root')

hdata_hip    = fdata.Get('c0').FindObject('JetHT2016BCDEF')
hdata_nonhip = fdata.Get('c0').FindObject('JetHT2016GH')

hmc_hip    = fmc.Get('c0').FindObject('qcdht1000and1500_hip1p0_mit')
hmc_nonhip = fmc.Get('c0').FindObject('qcdht1000and1500')

ilum_hip    = sum((5746.3, 2572.8, 4224.6, 3957.9, 3104.5))
ilum_nonhip = sum((7574.8, 8434.6, 216.0))
ilum_total = ilum_hip + ilum_nonhip

ps = plot_saver(plot_dir('v0bkgsub_beforeFR/guh'), size=(600,600))
#ps.c.cd()

for h in hdata_hip, hdata_nonhip, hmc_hip, hmc_nonhip:
    print h.GetNbinsX(), h.GetBinLowEdge(1), h.GetBinLowEdge(h.GetNbinsX()+1)
#    h.GetXaxis().SetRangeUser(-2,2)
  #  h.GetYaxis()
#    h.Draw()
 #   ps.save(h.GetName())

def foo(name, color, hip, nonhip):
    hip = hip.Clone(name + '_hip')
    hip.Scale(ilum_hip / ilum_total)
    nonhip = nonhip.Clone(name + '_nonhip')
    nonhip.Scale(ilum_nonhip / ilum_total)
    h = hip.Clone(name)
    h.Add(nonhip)
    h.SetLineColor(color)
    h.SetLineWidth(2)
    return h

hdata = foo('hdata', 1, hdata_hip, hdata_nonhip)
hmc   = foo('hmc',   ROOT.kRed, hmc_hip,   hmc_nonhip)

print hdata.GetEntries()
print hmc.GetEntries()

ratios_plot('track_dxy',
            [hmc, hdata],
            plot_saver=ps,
            x_range = (-0.5, 0.5),
            res_y_range = (0, 1.5),
            res_fit = False,
            res_divide_opt={'confint': propagate_ratio, 'force_le_1': False, 'allow_subset': True}
            )
