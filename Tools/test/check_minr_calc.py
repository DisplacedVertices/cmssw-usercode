import sys
from JMTucker.Tools.BasicAnalyzer_cfg import *
from JMTucker.Tools.MiniAOD_cfg import which_global_tag

is_mc = True

process.TFileService.fileName = 'checkminrcalc.root'
file_event_from_argv(process)

geometry_etc(process, which_global_tag(is_mc, 2016))
add_analyzer(process, 'CheckMinRCalc')

import JMTucker.Tools.SampleFiles as sf
sf.set_process(process, 'ttbar', 'main')
process.maxEvents.input = 1000

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    import JMTucker.Tools.Samples as Samples 

    samples = Samples.ttbar_samples + Samples.qcd_samples + Samples.qcd_samples_ext + \
        [Samples.mfv_neu_tau00100um_M0800, Samples.mfv_neu_tau00300um_M0800, Samples.mfv_neu_tau01000um_M0800, Samples.mfv_neu_tau10000um_M0800] + \
        [Samples.xx4j_tau00001mm_M0300, Samples.xx4j_tau00010mm_M0300, Samples.xx4j_tau00001mm_M0700, Samples.xx4j_tau00010mm_M0700]

    for s in samples:
        s.files_per = 20

    from JMTucker.Tools.CondorSubmitter import CondorSubmitter
    cs = CondorSubmitter('CheckMinRCalc')
    cs.submit_all(samples)

elif __name__ == '__main__' and hasattr(sys, 'argv') and 'check' in sys.argv:
    from JMTucker.Tools.ROOTTools import *
    from JMTucker.Tools.colors import red, green
    for arg in sys.argv:
        if arg.endswith('.root'):
            f = ROOT.TFile(arg)
            h = f.Get('CheckMinRCalc/ok')
            c = h.GetBinContent
            b = h.FindBin
            n = h.GetEntries()
            c00 = c(5)
            c11 = c(10)
            c10 = c(6)
            c01 = c(9)
            print arg.ljust(80), 'off diag: %15.f %15.f on diag: %15.f %15.f nentries %15.f' % (c01, c10, c00, c11, n),
            if c01 or c10:
                print red('problem')
            else:
                print green('OK!')
