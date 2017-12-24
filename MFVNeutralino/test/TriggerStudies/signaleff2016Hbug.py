#!/usr/bin/env python

import sys, os
from JMTucker.Tools.BasicAnalyzer_cfg import *
from JMTucker.Tools.MiniAOD_cfg import which_global_tag
from JMTucker.MFVNeutralino.Year import year

global_tag(process, which_global_tag(True, year, H=False, repro=False))
process.maxEvents.input = 100
#want_summary(process)

#sample_files(process, 'mfv_neu_tau01000um_M0300', 'main')
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
    import JMTucker.Tools.Samples as Samples 
    samples = Samples.mfv_signal_samples
    for sample in samples:
        sample.files_per = 5

    from JMTucker.Tools.MetaSubmitter import *
    ms = MetaSubmitter('SignalEff2016HBug')
    ms.crab.job_control_from_sample = True
    ms.submit(samples)

elif __name__ == '__main__' and hasattr(sys, 'argv') and 'ana' in sys.argv:
    from JMTucker.Tools.ROOTTools import ROOT
    for fn in sys.argv:
        if '.root' in fn:
            print os.path.basename(fn)
            f = ROOT.TFile(fn)
            ct = [0,0,0]
            for l1htt, w in (240, 0.333), (255, 0.248), (280, 0.125), (300, 0.294):
                name = 'HLT1bugcheckL1%iusemywbug' % l1htt
                d = f.Get(name)
                n = d.Get('h_gendvv_den').GetEntries()
                i = d.Get('h_gendvv_fail').GetEntries()
                r = d.Get('h_gendvv_faill1htt_l1single450').GetEntries()
                rak = d.Get('h_gendvv_faill1htt_l1single450ak').GetEntries()
                c = float(i)/n, float(r)/i, float(rak)/i
                ct = [a+w*b for a,b in zip(ct, c)]
                print name.ljust(40), '%6i / %6i = %.4f  %.4f  %.4f' % ((i, n) + c)
            print 'wavg:  %.4f  %.4f  %.4f' % tuple(ct)
            print
