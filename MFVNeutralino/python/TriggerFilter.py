import FWCore.ParameterSet.Config as cms

def setup_trigger_filter(process):
    from HLTrigger.HLTfilters.hltHighLevel_cfi import hltHighLevel
    process.triggerFilter = hltHighLevel.clone()
    process.triggerFilter.HLTPaths = ['HLT_QuadJet50_v*']
    process.triggerFilter.andOr = True # = OR
    for name, path in process.paths.items():
        if not name.startswith('eventCleaning'):
            path.insert(0, process.triggerFilter)
    process.pevtsel = cms.Path(process.triggerFilter)
    if hasattr(process, 'out'):
        process.out.SelectEvents = cms.untracked.PSet(SelectEvents = cms.vstring('pevtsel'))
