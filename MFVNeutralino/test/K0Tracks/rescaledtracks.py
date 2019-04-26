import sys, os
from JMTucker.Tools.ROOTTools import *
set_style()

batch = sys.argv[1]
ps = plot_saver(plot_dir('v0bkgsub_%s/cfrescaled' % batch), size=(600,600), log=False)

samples = ['background_2017', 'JetHT2017B']
fs = [ROOT.TFile(os.path.join(batch, '%s.root' % s)) for s in samples]
hs = [f.Get('h_tracks_dxyerr_v_pt/hsig') for f in fs]
mc, data = pfs = [h.ProfileX('%s_%s' % (s, h.GetName())) for s,h in zip(samples,hs)]

mc.SetLineColor(2)
data.SetLineColor(1)
mc.nice, data.nice = '2017 MC', 'JetHT2017B'

for pf in pfs:
    pf.SetLineWidth(2)
    pf.GetYaxis().SetTitle('<dxyerr> (cm)')

fcn1 = ROOT.TF1('2017Betalt1p5', '(x<=5)*([p0]+[p1]*x)+(x>5&&x<=10)*([p2]+[p3]*x)+(x>10&&x<=19)*([p4]+[p5]*x)+(x>19&&x<=200)*([p6]+[p7]*x)+(x>200)*([p6]+[p7]*200)', 0,25)
fcn1.SetParameters(1.003954411196716, 0.04680608038556485, 1.1651640253424076, 0.010686515626581808, 1.2423728669230774, 0.002510211465163767, 1.301491397216935, -0.0005992241020962791)
fcn2 = ROOT.TF1('2017Betagt1p5', '(x<=5)*([p0]+[p1]*x)+(x>5&&x<=10)*([p2]+[p3]*x)+(x>10&&x<=19)*([p4]+[p5]*x)+(x>19&&x<=200)*([p6]+[p7]*x)+(x>200)*([p6]+[p7]*200)', 0,25)
fcn2.SetParameters(0.9809194238515303, 0.02988345020861421, 1.0494209346433279, 0.01638247946618149, 1.1747904134913318, 0.004173705981459077, 1.27170013468283, -0.0015234534159011834)
fcns = [fcn1,fcn2]
for fcn in fcns:
    fcn.SetLineWidth(1)
    fcn.SetLineStyle(10)
fcn1.SetLineColor(4)
fcn2.SetLineColor(6)

rp = ratios_plot('dxyerr_v_pt', pfs,
                 plot_saver=ps,
                 legend=(0.4,0.8,0.8,0.9),
                 x_range=(0,25),
                 y_range=(0, 0.009),
                 res_divide_opt={'confint': propagate_ratio, 'force_le_1': False},
                 res_fit=False,
                 res_y_title='data/MC',
                 res_y_range=(0.8,1.8),
                 res_fcns = fcns,
                 )
