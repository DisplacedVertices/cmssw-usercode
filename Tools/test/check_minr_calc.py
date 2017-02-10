import sys
from JMTucker.Tools.BasicAnalyzer_cfg import *
from JMTucker.Tools.MiniAOD_cfg import which_global_tag

is_mc = True

process.TFileService.fileName = 'checkminrcalc.root'
file_event_from_argv(process)

geometry_etc(process, which_global_tag(is_mc))
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
        s.files_per = 50

    from JMTucker.Tools.CondorSubmitter import CondorSubmitter
    cs = CondorSubmitter('CheckMinRCalc')
    cs.submit_all(samples)
