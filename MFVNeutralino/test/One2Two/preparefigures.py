from JMTucker.Tools.ROOTTools import *
from limits_input import name2isample, h_dvv, nevents

# wish I could import from scanpack but this will get arbitrary anyway
kinds = ['mfv_ddbar', 'mfv_neu']
masses = to_array(range(300, 600, 100) + range(600, 3001, 200))
taus = to_array([tau/1000. for tau in range(100, 1000, 300) + range(1000, 40000, 3000) + range(40000, 1000001, 160000)])
nmasses = len(masses) - 1
ntaus = len(taus) - 1

def signal_efficiency(in_fn='limits_input.root', out_fn='figures.root'):
    in_f = ROOT.TFile(in_fn)
    out_f = ROOT.TFile(out_fn, 'update')

    for kind in kinds:
        h = ROOT.TH2D('signal_efficiency_%s' % kind, ';mass (GeV);#tau (mm)', nmasses, masses, ntaus, taus)

        for ibin in xrange(1, nmasses+1):
            mass = h.GetXaxis().GetBinLowEdge(ibin)
            for jbin in xrange(1, ntaus+1):
                tau = h.GetYaxis().GetBinLowEdge(jbin)

                name = '%s_tau%05ium_M%04i' % (kind, int(tau*1000), mass)
                isample = name2isample(in_f, name)
                dvv = h_dvv(in_f, isample)

                n2v = int(dvv.Integral(2, 1000000)) # 2 for >=400 um, 3 for >=700um
                ngen = nevents(in_f, isample)

                e,l,u = wilson_score(n2v, ngen)
                ee = (u-l)/2

                h.SetBinContent(ibin, jbin, e)
                h.SetBinError  (ibin, jbin, ee)

        h.Write()

    out_f.Write()
    out_f.Close()

if __name__ == '__main__':
    import sys
    if 'signal_efficiency' in sys.argv:
        signal_efficiency()
    else:
        print 'dunno'
