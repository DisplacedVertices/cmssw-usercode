import FWCore.ParameterSet.Config as cms

def setup_trigger_filter(process,
                         path_name='pevtsel',
                         trig_filt_name = 'triggerFilter',
                         event_filter = False,
                         event_filter_jes_mult = 2,
                         event_filt_name = 'jetFilter'
                         ):

    from HLTrigger.HLTfilters.hltHighLevel_cfi import hltHighLevel
    triggerFilter = hltHighLevel.clone()
    setattr(process, trig_filt_name, triggerFilter)
    triggerFilter.HLTPaths = [
        "HLT_PFHT800_v*",
        "HLT_PFHT900_v*",
        "HLT_PFJet450_v*",
        "HLT_AK8PFJet450_v*",
        ]
    triggerFilter.andOr = True # = OR
    triggerFilter.throw = False

    overall = triggerFilter

    if event_filter:
        if not hasattr(process, 'patJets'):
            raise NotImplementedError('need to understand how to include pat_tuple jets_only here')

        from JMTucker.Tools.JetFilter_cfi import jmtJetFilter as jetFilter
        setattr(process, event_filt_name, jetFilter)

        if event_filter_jes_mult > 0:
            from JMTucker.Tools.JetShifter_cfi import jmtJetShifter as shifter
            shifter.mult = event_filter_jes_mult
            shifter_name = event_filt_name + 'JESUncUp%i' % event_filter_jes_mult
            jetFilter.jets_src = shifter_name
            setattr(process, shifter_name, shifter)

            overall *= shifter * jetFilter
        else:
            overall *= jetFilter
            
    if hasattr(process, path_name):
        getattr(process, path_name).insert(0, overall)
    else:
        setattr(process, path_name, cms.Path(overall))

    if hasattr(process, 'out'):
        process.out.SelectEvents = cms.untracked.PSet(SelectEvents = cms.vstring(path_name))
