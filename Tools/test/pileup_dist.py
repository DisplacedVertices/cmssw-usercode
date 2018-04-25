import sys
from JMTucker.Tools.MiniAOD_cfg import *
from JMTucker.Tools.CMSSWTools import *
from JMTucker.Tools.Year import year

from_miniaod = False
is_mc = True
H = False
repro = False

process = pat_tuple_process(None, is_mc, year, H, repro)
jets_only(process)

process.maxEvents.input = -1
dataset = 'miniaod' if from_miniaod else 'main'
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

process.load('JMTucker.Tools.JetFilter_cfi')

process.p = cms.Path(process.PileupDist * process.hltHighLevel * process.PileupDistHLT * process.jmtJetFilter * process.PileupDistPreSel)

associate_paths_to_task(process)

pileup_weights = [
    ]

for xsec, weights in pileup_weights:
    pud = process.PileupDist.clone(pileup_weights = weights)
    pudh, pudj = pud.clone(), pud.clone()
    setattr(process, 'PileupDist%i'       % xsec, pud)
    setattr(process, 'PileupDistHLT%i'    % xsec, pudh)
    setattr(process, 'PileupDistPreSel%i' % xsec, pudj)
    setattr(process, 'p%i' % xsec, cms.Path(pud * process.hltHighLevel * pudh * process.jmtJetFilter * pudj))

    
if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.MetaSubmitter import *
    import JMTucker.Tools.Samples as Samples 

    if year == 2015:
        samples = Samples.data_samples_2015 + Samples.ttbar_samples_2015 + Samples.qcd_samples_2015 + Samples.qcd_samples_ext_2015
    elif year == 2016:
        samples = Samples.data_samples + Samples.ttbar_samples + Samples.qcd_samples + Samples.qcd_samples_ext
    elif year == 2017:
        samples = Samples.ttbar_samples_2017 + Samples.qcd_samples_2017

    from JMTucker.Tools.MetaSubmitter import set_splitting
    set_splitting(samples, dataset, 'default', data_json='jsons/ana_2015p6.json')

    ms = MetaSubmitter('PileupDistV1_2017', dataset=dataset)
    ms.common.ex = year
    ms.common.pset_modifier = chain_modifiers(is_mc_modifier, H_modifier, repro_modifier)
    ms.crab.job_control_from_sample = True
    ms.submit(samples)
