import FWCore.ParameterSet.Config as cms

def setup_event_filter(process,
                       path_name='pevtsel',
                       trig_filt_name = 'triggerFilter',
                       event_filter = False,
                       event_filter_jes_mult = 2,
                       event_filter_name = 'mfvEventFilter',
                       event_filter_require_vertex = True,
                       input_is_miniaod = False,
                       ):

    from JMTucker.MFVNeutralino.TriggerFilter_cfi import mfvTriggerFilter as triggerFilter
    setattr(process, trig_filt_name, triggerFilter)

    overall = triggerFilter

    if event_filter:
        from JMTucker.MFVNeutralino.EventFilter_cfi import mfvEventFilter as eventFilter
        eventFilter = eventFilter.clone()
        if input_is_miniaod:
            eventFilter.jets_src = 'slimmedJets'
            eventFilter.muons_src = 'slimmedMuons'
            eventFilter.electrons_src = 'slimmedElectrons'
        setattr(process, event_filter_name, eventFilter)

        if event_filter_jes_mult > 0:
            from JMTucker.Tools.JetShifter_cfi import jmtJetShifter as jetShifter
            jetShifter = jetShifter.clone()
            if input_is_miniaod:
                jetShifter.jets_src = 'slimmedJets'
            jetShifter.mult = event_filter_jes_mult
            jetShifter_name = event_filter_name + 'JetsJESUp%iSig' % event_filter_jes_mult
            eventFilter.jets_src = jetShifter_name
            setattr(process, jetShifter_name, jetShifter)
            overall *= jetShifter

        overall *= eventFilter

        if event_filter_require_vertex:
            if not hasattr(process, 'mfvVertices'):
                # assume if mfvVertices is set up, then the rest of this is too
                process.load('CommonTools.ParticleFlow.goodOfflinePrimaryVertices_cfi')
                process.load('JMTucker.MFVNeutralino.Vertexer_cfi')
                if input_is_miniaod:
                    process.goodOfflinePrimaryVertices.src = 'offlineSlimmedPrimaryVertices'
                    process.load('JMTucker.MFVNeutralino.UnpackedCandidateTracks_cfi')
                    process.mfvVertices.track_src = 'mfvUnpackedCandidateTracks'
            vertexFilter = cms.EDFilter('VertexSelector', src = cms.InputTag('mfvVertices'), cut = cms.string('nTracks > 2'), filter = cms.bool(True))
            setattr(process, event_filter_name + 'W1Vtx', vertexFilter)
            if input_is_miniaod:
                overall *= process.goodOfflinePrimaryVertices * process.mfvUnpackedCandidateTracks * process.mfvVertices * vertexFilter
            else:
                overall *= process.goodOfflinePrimaryVertices                                      * process.mfvVertices * vertexFilter

    if hasattr(process, path_name):
        getattr(process, path_name).insert(0, overall)
    else:
        setattr(process, path_name, cms.Path(overall))

    if hasattr(process, 'out'):
        process.out.SelectEvents = cms.untracked.PSet(SelectEvents = cms.vstring(path_name))
