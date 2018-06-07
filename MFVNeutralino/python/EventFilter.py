import FWCore.ParameterSet.Config as cms

def setup_event_filter(process,
                       path_name='pevtsel',
                       trig_filt_name = 'triggerFilter',
                       event_filter = False,
                       event_filter_jes_mult = 2,
                       event_filt_name = 'jetFilter',
                       input_is_miniaod = False,
                       ):

    from HLTrigger.HLTfilters.hltHighLevel_cfi import hltHighLevel
    triggerFilter = hltHighLevel.clone()
    setattr(process, trig_filt_name, triggerFilter)
    triggerFilter.HLTPaths = [
        "HLT_PFHT1050_v*",
        "HLT_Ele35_WPTight_Gsf_v*",
        "HLT_Ele115_CaloIdVT_GsfTrkIdT_v*",
        "HLT_Ele50_CaloIdVT_GsfTrkIdT_PFJet165_v*",
        "HLT_IsoMu27_v*",
        "HLT_Mu50_v*",
        "HLT_Ele15_IsoVVVL_PFHT450_v*",
        "HLT_Mu15_IsoVVVL_PFHT450_v*",
        ]
    triggerFilter.andOr = True # = OR
    triggerFilter.throw = False

    overall = triggerFilter

    if event_filter:
        if not input_is_miniaod and not hasattr(process, 'patJets'):
            raise NotImplementedError('need to understand how to include pat_tuple jets_only here')

        from JMTucker.Tools.JetFilter_cfi import jmtJetFilter as jetFilter
        jetFilter = jetFilter.clone()
        if input_is_miniaod:
            jetFilter.jets_src = 'slimmedJets'
        setattr(process, event_filt_name, jetFilter)

        if event_filter_jes_mult > 0:
            from JMTucker.Tools.JetShifter_cfi import jmtJetShifter as jetShifter
            jetShifter = jetShifter.clone()
            if input_is_miniaod:
                jetShifter.jets_src = 'slimmedJets'
            jetShifter.mult = event_filter_jes_mult
            jetShifter_name = event_filt_name + 'JESUncUp%i' % event_filter_jes_mult
            jetFilter.jets_src = jetShifter_name
            setattr(process, jetShifter_name, jetShifter)

            overall *= jetShifter * jetFilter
        else:
            overall *= jetFilter
            
    if hasattr(process, path_name):
        getattr(process, path_name).insert(0, overall)
    else:
        setattr(process, path_name, cms.Path(overall))

    if hasattr(process, 'out'):
        process.out.SelectEvents = cms.untracked.PSet(SelectEvents = cms.vstring(path_name))
