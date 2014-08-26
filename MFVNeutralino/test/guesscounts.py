from JMTucker.Tools.Samples import *
import JMTucker.MFVNeutralino.AnalysisConstants as ac

nevs = []
nevtrigs = []
nevtrigvtxs = []

samples = qcd_samples + ttbar_samples + leptonic_background_samples + smaller_background_samples
effs = [2.67e-5, 1.08e-4, 2.37e-3, 6.27e-3, 4.15e-3, 2.45e-3, 1.5e-3]
effs += [2e-3]*(len(samples) - len(effs))

for i,s in enumerate(samples):
    nev = s.cross_section * ac.int_lumi
    nevtrig = nev * s.ana_filter_eff
    nevtrigvtx = nevtrig * effs[i]
    nevs.append(nev)
    nevtrigs.append(nevtrig)
    nevtrigvtxs.append(nevtrigvtx)
    print '%30s %10.3g %10.3g %10.3g' % (s.name, nev, nevtrig, nevtrigvtx)
print '-'*(30+11*3)
print '%30s %10.3g %10.3g %10.3g' % ('all', sum(nevs), sum(nevtrigs), sum(nevtrigvtxs))
print '%30s %10.3g %10.3g %10.3g' % ('allnoqcd100250', sum(nevs[2:]), sum(nevtrigs[2:]), sum(nevtrigvtxs[2:]))
print '%30s %10.3g %10.3g %10.3g' % ('qcd', sum(nevs[:4]), sum(nevtrigs[:4]), sum(nevtrigvtxs[:4]))
print '%30s %10.3g %10.3g %10.3g' % ('qcd>500', sum(nevs[2:4]), sum(nevtrigs[2:4]), sum(nevtrigvtxs[2:4]))
print '%30s %10.3g %10.3g %10.3g' % ('ttbar', sum(nevs[4:7]), sum(nevtrigs[4:7]), sum(nevtrigvtxs[4:7]))
print '%30s %10.3g %10.3g %10.3g' % ('lept', sum(nevs[7:10]), sum(nevtrigs[7:10]), sum(nevtrigvtxs[7:10]))
print '%30s %10.3g %10.3g %10.3g' % ('rest', sum(nevs[10:]), sum(nevtrigs[10:]), sum(nevtrigvtxs[10:]))
