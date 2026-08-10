import sys, os
from JMTucker.Tools.ROOTTools import *
set_style()
ROOT.TH1.AddDirectory(0)

batch = sys.argv[1]

fdata = ROOT.TFile(os.path.join(batch, 'JetHT2017B.root'))
fmc   = ROOT.TFile(os.path.join(batch, 'background_2017.root'))

hdata = fdata.Get('h_tracks_dxy/hsig')
hmc   = fmc  .Get('h_tracks_dxy/hsig')

ps = plot_saver(plot_dir('v0bkgsub_%s/effvsdxy' % batch), size=(600,600))

for h in hdata, hmc:
    h.SetLineWidth(2)
    h.Rebin(4)
hdata.SetLineColor(1)
hmc.SetLineColor(2)

ib = hmc.GetXaxis().FindBin(0.)
mc0 = hmc.GetBinContent(ib)
data0 = hdata.GetBinContent(ib)
hmc.Scale(data0/mc0)

print 'data', get_integral(hdata)
print 'mc', get_integral(hmc)

ratios_plot('track_dxy',
            [hmc, hdata],
            plot_saver=ps,
            #x_range = (-0.05, 0.05),
            res_y_range = (0.7, 1.3),
            res_fit = 'pol1',
            res_divide_opt={'confint': propagate_ratio, 'force_le_1': False, 'allow_subset': True}
            )
