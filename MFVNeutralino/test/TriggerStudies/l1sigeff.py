#!/usr/bin/env python

import sys
from DVCode.Tools.BasicAnalyzer_cfg import *

import DVCode.Tools.SampleFiles as sf
process.source.fileNames = sf.get('mfv_neu_tau01000um_M0300', 'main')[1][:1]

process.TFileService.fileName = 'l1sigeff.root'

process.load('HLTrigger.HLTfilters.hltHighLevel_cfi')
process.hltHighLevel.HLTPaths = ['HLT_PFHT800_v*']

hts = range(75, 201, 25) + [240, 250, 255, 280, 300, 320]
for ht in hts:
    l1 = cms.EDFilter('MFVL1HTTFilter', threshold = cms.double(ht))
    p = cms.Path(process.hltHighLevel * l1)
    setattr(process, 'l1%i' % ht, l1)
    setattr(process, 'p%i'  % ht, p)

import DVCode.Tools.SimpleTriggerEfficiency_cfi as SimpleTriggerEfficiency
SimpleTriggerEfficiency.setup_endpath(process)

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from DVCode.Tools.CondorSubmitter import CondorSubmitter
    import DVCode.Tools.Samples as Samples 

    samples = Samples.mfv_signal_samples + \
        Samples.mfv_signal_samples_glu + \
        Samples.mfv_signal_samples_gluddbar + \
        Samples.xx4j_samples

    for sample in samples:
        sample.files_per = 100

    CondorSubmitter('L1SigEff').submit_all(samples)

elif __name__ == '__main__' and hasattr(sys, 'argv') and 'ana' in sys.argv:
    from DVCode.Tools.ROOTTools import ROOT
    for fn in sys.argv[1:]:
        f = ROOT.TFile(fn)
        h = f.Get('SimpleTriggerEfficiency/triggers_pass_num')

        num0 = None
        for i in xrange(1, h.GetNbinsX() + 1):
            path = h.GetXaxis().GetBinLabel(i)
            num = h.GetBinContent(i)
            if num0 is None:
                num0 = num
            else:
                if num - num0 > 0.01:
                    print fn, path, num, num0
