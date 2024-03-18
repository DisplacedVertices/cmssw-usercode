import sys
from JMTucker.Tools.ROOTTools import *
set_style()

ps = plot_saver(plot_dir('v0bkgsub_slicep'), size=(600,600))

f = ROOT.TFile(sys.argv[1])
h = f.Get('v0effon/K0_2pi/h_vtx_rho_vs_p')
for ibin in xrange(1, h.GetNbinsX()+1):
    mom = '%.1f-%.1f' % (h.GetXaxis().GetBinLowEdge(ibin), h.GetXaxis().GetBinLowEdge(ibin+1))
    p = h.ProjectionY(str(ibin), ibin, ibin, 'e d')
    p.SetTitle(mom)
    ps.save(mom)
