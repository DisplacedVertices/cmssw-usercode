import sys
from JMTucker.Tools.BasicAnalyzer_cfg import *
from JMTucker.Tools.MiniAOD_cfg import which_global_tag
from JMTucker.MFVNeutralino.Year import year

is_mc = True
H = False
repro = False

process.source.fileNames = ['/store/mc/RunIIFall15MiniAODv2/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/40000/E4574C7F-EACB-E511-817A-001E67DDC119.root']
process.source.fileNames = ['/store/data/Run2015C_25ns/JetHT/MINIAOD/16Dec2015-v1/20000/1C42421A-49B5-E511-B76E-0CC47A4D7666.root']
process.source.fileNames = ['/store/data/Run2015D/JetHT/MINIAOD/16Dec2015-v1/50001/9E62C986-A9AA-E511-BB43-0CC47A4D9A10.root']
process.source.fileNames = ['/store/mc/RunIIFall15MiniAODv2/QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/MINIAODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/10000/C6CD95B8-45B9-E511-A12B-141877411FED.root']
process.source.fileNames = ['/store/data/Run2016H/JetHT/MINIAOD/PromptReco-v3/000/284/044/00000/BE5F4C22-D29F-E611-AEAA-02163E011C32.root']

sample_files(process, 'SingleMuon2016H2', 'trigskimv1', 4)

process.maxEvents.input = -1
process.TFileService.fileName = 'triggerfloats.root'

global_tag(process, which_global_tag(is_mc, year, H, repro))
want_summary(process, True)

process.load('JMTucker.MFVNeutralino.TriggerFloats_cff')
process.mfvTriggerFloats.jets_src = 'slimmedJets'

if False:
    process.load('HLTrigger.HLTfilters.hltHighLevel_cfi')
    process.hltHighLevel.HLTPaths = [ 'HLT_PFHT800_v*', 'HLT_PFHT900_v*' ]
    process.hltHighLevel.andOr = True # = OR
    process.hltHighLevel.throw = False
    process.p = cms.Path(process.hltHighLevel * process.mfvTriggerFloats)
else:
    process.p = cms.Path(process.mfvTriggerFloats)

process.load('JMTucker.MFVNeutralino.TriggerFloatsFilter_cfi')
#process.mfvTriggerFloatsFilter.ht_cut = 1000
process.mfvTriggerFloatsFilter.myhttwbug_m_l1htt_cut = 0.1
process.p *= process.mfvTriggerFloatsFilter

process.mfvTriggerFloatsForPrints = process.mfvTriggerFloats.clone(prints = 1)
process.p *= process.mfvTriggerFloatsForPrints

process.plots = cms.EDAnalyzer('MFVTriggerEfficiency',
                               use_weight = cms.int32(0),
                               require_hlt = cms.int32(-1),
                               require_l1 = cms.int32(-1),
                               require_muon = cms.bool(False),
                               require_4jets = cms.bool(False),
                               require_ht = cms.double(-1),
                               muons_src = cms.InputTag('slimmedMuons'),
                               muon_cut = cms.string(''),
                               genjets_src = cms.InputTag(''),
                               )
process.p *= process.plots

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    import JMTucker.Tools.Samples as Samples 
    samples = Samples.data_samples
    for sample in samples:
        sample.lumis_per = 50
        sample.json = '../jsons/ana_2015p6.json'

    from JMTucker.Tools.MetaSubmitter import *
    from JMTucker.Tools.CRAB3Submitter import CRABSubmitter
    cs = CRABSubmitter('TriggerFloats_16_trigfilt',
                       pset_modifier = chain_modifiers(is_mc_modifier, H_modifier, repro_modifier),
                       job_control_from_sample = True,
                       dataset = 'miniaod',
                       )
    cs.submit_all(samples)
