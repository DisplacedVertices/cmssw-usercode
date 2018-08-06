import sys
from JMTucker.Tools.BasicAnalyzer_cfg import *
from JMTucker.Tools.Year import year

cmssw_settings = CMSSWSettings()
cmssw_settings.is_mc = True

max_events(process, -1)
sample_files(process, 'wjetstolnu_2017', 'miniaod', 2)
tfileservice(process, 'triggerfloats.root')
global_tag(process, which_global_tag(cmssw_settings))
want_summary(process)

process.load('JMTucker.MFVNeutralino.TriggerFloats_cff')
process.mfvTriggerFloats.jets_src = 'slimmedJets'
#process.mfvTriggerFloats.prints = 2

if 0:
    process.load('HLTrigger.HLTfilters.hltHighLevel_cfi')
    process.hltHighLevel.HLTPaths = [ 'HLT_PFHT800_v*', 'HLT_PFHT900_v*' ]
    process.hltHighLevel.andOr = True # = OR
    process.hltHighLevel.throw = False
    process.p = cms.Path(process.hltHighLevel * process.mfvTriggerFloats)
else:
    process.p = cms.Path(process.mfvTriggerFloats)

if 0:
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
