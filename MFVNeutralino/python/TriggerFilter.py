import FWCore.ParameterSet.Config as cms

def setup_trigger_filter(process, path_name='pevtsel', filt_name='triggerFilter'):
    from HLTrigger.HLTfilters.hltHighLevel_cfi import hltHighLevel
    triggerFilter = hltHighLevel.clone()
    setattr(process, filt_name, triggerFilter)
    triggerFilter.HLTPaths = [
        "HLT_PFHT800_v*",
        "HLT_PFHT900_v*",
        "HLT_PFJet450_v*",
        "HLT_AK8PFJet450_v*"
        ]
    triggerFilter.andOr = True # = OR
    triggerFilter.throw = False
    setattr(process, path_name, cms.Path(triggerFilter))
    if hasattr(process, 'out'):
        process.out.SelectEvents = cms.untracked.PSet(SelectEvents = cms.vstring(path_name))
