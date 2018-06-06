import sys
from JMTucker.Tools.BasicAnalyzer_cfg import *
from JMTucker.Tools.CMSSWTools import *

max_events(process, -1)
sample_files(process, 'qcdht2000_2017', 'miniaod', 1)
tfileservice(process, 'pileup.root')

process.load('JMTucker.Tools.MCStatProducer_cff')

process.PileupDist = cms.EDAnalyzer('PileupDist',
                                    primary_vertices_src = cms.InputTag('offlineSlimmedPrimaryVertices'),
                                    pileup_info_src = cms.InputTag('slimmedAddPileupInfo'),
                                    pileup_weights = cms.vdouble(),
                                    )

process.PileupDistHLT    = process.PileupDist.clone()
process.PileupDistPreSel = process.PileupDist.clone()

process.load('HLTrigger.HLTfilters.hltHighLevel_cfi')
process.hltHighLevel.HLTPaths = ['HLT_PFHT1050_v*']
process.hltHighLevel.andOr = True
process.hltHighLevel.throw = False

process.load('JMTucker.Tools.PATTupleSelection_cfi')
process.load('PhysicsTools.PatAlgos.selectionLayer1.jetSelector_cfi')
process.selectedPatJets.src = 'slimmedJets'
process.selectedPatJets.cut = process.jtupleParams.jetCut

process.load('JMTucker.Tools.JetFilter_cfi')

process.p = cms.Path(process.PileupDist * process.hltHighLevel * process.PileupDistHLT * process.selectedPatJets * process.jmtJetFilter * process.PileupDistPreSel)

pileup_weights = [] # for changing minbias xsec study
for xsec, weights in pileup_weights:
    pud = process.PileupDist.clone(pileup_weights = weights)
    pudh, pudj = pud.clone(), pud.clone()
    setattr(process, 'PileupDist%i'       % xsec, pud)
    setattr(process, 'PileupDistHLT%i'    % xsec, pudh)
    setattr(process, 'PileupDistPreSel%i' % xsec, pudj)
    setattr(process, 'p%i' % xsec, cms.Path(pud * process.hltHighLevel * pudh * process.jmtJetFilter * pudj))

    
if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.MetaSubmitter import MetaSubmitter, set_splitting
    from JMTucker.Tools.Year import year
    import JMTucker.Tools.Samples as Samples 

    if year == 2017:
        samples = Samples.ttbar_samples_2017 + Samples.qcd_samples_2017 + Samples.leptonic_samples_2017 + Samples.all_signal_samples_2017

    set_splitting(samples, 'miniaod', 'default', default_files_per=50)

    ms = MetaSubmitter('PileupDistV2', dataset='miniaod')
    ms.common.ex = year
    ms.crab.job_control_from_sample = True
    ms.submit(samples)
