import sys
from JMTucker.Tools.ROOTTools import *
ROOT.TH1.AddDirectory(0)
xxx = [
('/uscms_data/d2/tucker/crab_dirs/MinitreeV10/mfv_neu_tau00100um_M0800.root', 10.),
('/uscms_data/d2/tucker/crab_dirs/MinitreeV10/mfv_neu_tau00300um_M0800.root', 1.),
('/uscms_data/d2/tucker/crab_dirs/MinitreeV10/mfv_neu_tau01000um_M0800.root', 1.),
('/uscms_data/d2/tucker/crab_dirs/MinitreeV10/mfv_neu_tau10000um_M0800.root', 1.),
('/uscms_data/d2/tucker/crab_dirs/MinitreeV10/xx4j_tau00001mm_M0700.root', 1.),
('/uscms_data/d2/tucker/crab_dirs/MinitreeV10/xx4j_tau00010mm_M0700.root', 1.),
]
sigfn, xsec = xxx[int(sys.argv[1])]
f = ROOT.TFile(sigfn)
t = f.Get('mfvMiniTree/t')
eff = t.Draw('svdist>>hsig(80,0,0.4)', 'nvtx>=2') / 10000.
hsig = ROOT.hsig.Clone('hsig')
hsig.Scale(xsec * 39.5 / 10000)
print sigfn, 'xsec', xsec, 'eff', eff, 'integral', hsig.Integral(1,1000)
hsig = cumulative_histogram(hsig)

f = ROOT.TFile('2v_from_jets_5track_average5_c1p35_e2_a3p66.root')
h = f.Get('h_c1v_dvv')

norm = 0.45
h.Scale(norm/h.Integral())

h = cumulative_histogram(h)

zgt = zgammatauwrong

fmt = '%3i %5.3f %8.2f %8.5f %8.5f'
print '%3s %5s %8s %8s %8s %8s %5s %5s  %5s %5s  %5s %5s' % ('bin', 'cut', 's', 'b', 'unc', 'f.unc', 'tau', 't.unc', 'zbi0', 'zbi1', 'zgt0', 'zgt1')
for (ibin,), dvv_cut, b in bin_iterator(h, True):
    if ibin == 0:
        continue
    s = hsig.GetBinContent(ibin)
    b_uncert = h.GetBinError(ibin)
    print fmt % (ibin, dvv_cut, s, b, b_uncert),
    if b > 0:
        frac = b_uncert / b
        print '%8.5f' % frac,
        tau = (norm - b) / b
        tau_uncert = frac * tau
        print '%5.2f %5.2f  %5.2f %5.2f  %5.2f %5.2f' % (tau, tau_uncert, zbi(s,0,tau), zbi(s,1,tau), zgt(s,0,tau,tau_uncert), zgt(s,1,tau,tau_uncert))
    else:
        print '*'
    if dvv_cut > 0.1:
        break

