import sys
from JMTucker.Tools.BasicAnalyzer_cfg import *
from JMTucker.Tools.CMSSWTools import *

from_miniaod = True
dataset = 'miniaod' if from_miniaod else 'main'

max_events(process, -1)
sample_files(process, 'qcdht2000_2017', dataset, 1)
tfileservice(process, 'pileup.root')

process.load('JMTucker.Tools.MCStatProducer_cff')

process.PileupDist = cms.EDAnalyzer('PileupDist',
                                    primary_vertices_src = cms.InputTag('offlineSlimmedPrimaryVertices' if from_miniaod else 'offlinePrimaryVertices'),
                                    pileup_info_src = cms.InputTag('slimmedAddPileupInfo' if from_miniaod else 'addPileupInfo'),
                                    pileup_weights = cms.vdouble(),
                                    )

process.PileupDistHLT    = process.PileupDist.clone()
process.PileupDistPreSel = process.PileupDist.clone()

process.load('HLTrigger.HLTfilters.hltHighLevel_cfi')
process.hltHighLevel.HLTPaths = ['HLT_PFHT1050_v*']
process.hltHighLevel.andOr = True
process.hltHighLevel.throw = False

process.p = cms.Path(process.PileupDist * process.hltHighLevel * process.PileupDistHLT)

if from_miniaod:
    process.load('PhysicsTools.PatAlgos.selectionLayer1.jetSelector_cfi')
    process.load('JMTucker.Tools.JetFilter_cfi')
    process.load('JMTucker.Tools.PATTupleSelection_cfi')
    process.selectedPatJets.src = 'slimmedJets'
    process.selectedPatJets.cut = process.jtupleParams.jetCut

    process.p *= process.selectedPatJets * process.jmtJetFilter * process.PileupDistPreSel

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

    set_splitting(samples, dataset, 'default', default_files_per=50)

    batch_name = 'PileupDistV3p1'
    if not from_miniaod:
        batch_name += '_aod'
    ms = MetaSubmitter(batch_name, dataset=dataset)
    ms.submit(samples)
