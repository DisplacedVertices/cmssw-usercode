#!/usr/bin/env python

import sys
from JMTucker.Tools.BasicAnalyzer_cfg import *
from JMTucker.Tools.MiniAOD_cfg import which_global_tag
from JMTucker.MFVNeutralino.Year import year

global_tag(process, which_global_tag(True, year))
process.maxEvents.input = 100

#sample_files(process, 'official_mfv_neu_tau01000um_M0300', 'main')
process.source.fileNames = ['root://xrootd2.ihepa.ufl.edu//store/mc/RunIISummer16DR80Premix/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-300_CTau-1mm_TuneCUETP8M1_13TeV-pythia8/AODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v2/110000/0EE95A6E-A8F4-E611-9339-0025905AA9F0.root']

process.TFileService.fileName = 'signaleff2016Hbug.root'

process.load('PhysicsTools.PatAlgos.triggerLayer1.triggerProducer_cfi')
process.load('PhysicsTools.PatAlgos.slimming.selectedPatTrigger_cfi')
process.load('JMTucker.MFVNeutralino.TriggerFloats_cff')
process.load('HLTrigger.HLTfilters.hltHighLevel_cfi')
process.hltHighLevel.HLTPaths = ['HLT_PFHT900_v*']

l1htts = [160, 200, 220, 240, 255, 270, 280, 300, 320]
whichs = ['event', 'my', 'mywbug']

for hlt in False, True:
    for which in whichs:
        for l1htt in l1htts:
            l1 = cms.EDAnalyzer('MFVSignalEff2016HBug',
                                l1htt_threshold = cms.int32(l1htt),
                                which_l1htt = cms.string(which),
                                )
            x = process.patTrigger * process.selectedPatTrigger * process.mfvTriggerFloats * l1
            p = cms.Path(process.hltHighLevel * x if hlt else x)
            name = 'HLT%ibugcheckL1%iuse%s' % (hlt, l1htt, which)
            setattr(process, name, l1)
            setattr(process, 'p' + name, p)

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.CondorSubmitter import CondorSubmitter
    import JMTucker.Tools.Samples as Samples 

    samples = Samples.mfv_signal_samples + \
        Samples.mfv_signal_samples_glu + \
        Samples.mfv_signal_samples_gluddbar + \
        Samples.xx4j_samples

    for sample in samples:
        sample.files_per = 100

    CondorSubmitter('L1SigEff').submit_all(samples)

elif __name__ == '__main__' and hasattr(sys, 'argv') and 'ana' in sys.argv:
    from JMTucker.Tools.ROOTTools import ROOT
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
