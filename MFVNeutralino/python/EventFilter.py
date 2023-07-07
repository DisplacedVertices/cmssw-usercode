import FWCore.ParameterSet.Config as cms

def setup_event_filter(process,
                       path_name='p',
                       trigger_filter = True,
                       trigger_filter_name = 'mfvTriggerFilter',
                       event_filter = False,
                       event_filter_jes_mult = 2,
                       event_filter_name = 'mfvEventFilter',
                       event_filter_require_vertex = True,
                       rp_filter = False,
                       rp_mode = None,
                       rp_mass = -1,
                       rp_ctau = '',
                       rp_dcay = '',
                       input_is_miniaod = False,
                       mode = None,
                       sequence_name = 'mfvEventFilterSequence',
                       name_ex = None,
                       ):

    if name_ex:
        trigger_filter_name += name_ex
        event_filter_name += name_ex
        sequence_name += name_ex

    if mode == 'trigger only':
        pass
    elif mode == 'trigger jets only':
        trigger_filter = 'jets only'
    elif mode == 'trigger bjets only':
        trigger_filter = 'bjets only'
    elif mode == 'trigger met only':
        trigger_filter = 'met only'
    elif mode == 'trigger displaced dijet only':
        trigger_filter = 'displaced dijet only'
    elif mode == 'trigger HT OR bjets OR displaced dijet':
        trigger_filter = 'HT OR bjets OR displaced dijet'
    elif mode == 'trigger bjets OR displaced dijet veto HT':
        trigger_filter = 'bjets OR displaced dijet veto HT'
    elif mode == 'trigger muons only':
        trigger_filter = 'muons only'
    elif mode == 'trigger electrons only':
        trigger_filter = 'electrons only'
    elif mode == 'jets only':
        trigger_filter = event_filter = 'jets only'
    elif mode == 'muons only':
        trigger_filter = 'muons only'
        event_filter = 'muons only'
    elif mode == 'electrons only':
        trigger_filter = 'electrons only'
        event_filter = 'electrons only veto muons'
    elif mode == 'displeptons only':
        trigger_filter = 'displeptons only',
        event_filter = 'leptons only'
    elif mode == 'displeptons OR leptons':
        trigger_filter = 'displeptons OR leptons'
        event_filter = 'leptons only'
    elif mode == 'met only':
        trigger_filter = event_filter = 'met only'
    elif mode == 'HT OR bjets OR displaced dijet':
        trigger_filter = event_filter = 'HT OR bjets OR displaced dijet'
    elif mode == 'bjets OR displaced dijet veto HT':
        trigger_filter = event_filter = 'bjets OR displaced dijet veto HT'
    elif mode == 'jets only novtx':
        trigger_filter = event_filter = 'jets only'
        event_filter_require_vertex = False
    elif mode == 'muons only novtx':
        trigger_filter = 'muons only'
        event_filter = 'muons only'
        event_filter_require_vertex = False
    elif mode == 'electrons only novtx':
        trigger_filter = 'electrons only'
        event_filter = 'electrons only veto muons'
        event_filter_require_vertex = False
    elif mode == 'bjets OR displaced dijet veto HT novtx':
        trigger_filter = event_filter = 'bjets OR displaced dijet veto HT'
        event_filter_require_vertex = False
    elif mode == 'novtx':
        event_filter = True
        event_filter_require_vertex = False
    elif mode == 'met trigger or low met':
        event_filter = 'met only'
        trigger_filter = False
        event_filter_require_vertex = True
    elif mode:
        if mode is not True:
            raise ValueError('bad mode %r' % mode)
        event_filter = True

    if trigger_filter == 'jets only':
        from JMTucker.MFVNeutralino.TriggerFilter_cfi import mfvTriggerFilterJetsOnly as triggerFilter
    elif trigger_filter == 'bjets only':
        from JMTucker.MFVNeutralino.TriggerFilter_cfi import mfvTriggerFilterBJetsOnly as triggerFilter
    elif trigger_filter == 'met only':
        from JMTucker.MFVNeutralino.TriggerFilter_cfi import mfvTriggerFilterMETOnly as triggerFilter
    elif trigger_filter == 'displaced dijet only':
        from JMTucker.MFVNeutralino.TriggerFilter_cfi import mfvTriggerFilterDisplacedDijetOnly as triggerFilter
    elif trigger_filter == 'HT OR bjets OR displaced dijet':
        from JMTucker.MFVNeutralino.TriggerFilter_cfi import mfvTriggerFilterHTORBjetsORDisplacedDijet as triggerFilter
    elif trigger_filter == 'bjets OR displaced dijet veto HT':
        from JMTucker.MFVNeutralino.TriggerFilter_cfi import mfvTriggerFilterBjetsORDisplacedDijetVetoHT as triggerFilter
    elif trigger_filter == 'muons only':
        from JMTucker.MFVNeutralino.TriggerFilter_cfi import mfvTriggerFilterMuonsOnly as triggerFilter
    elif trigger_filter == 'electrons only':
        from JMTucker.MFVNeutralino.TriggerFilter_cfi import mfvTriggerFilterElectronsOnly as triggerFilter
    elif trigger_filter == 'displeptons only':
        from JMTucker.MFVNeutralino.TriggerFilter_cfi import mfvTriggerFilterDisplacedLeptons as triggerFilter
    elif trigger_filter == 'lep OR displaced lep':
        from JMTucker.MFVNeutralino.TriggerFilter_cfi import mfvTriggerFilterDispLeptonsORSingleLeptons as triggerFilter
    elif trigger_filter is True:
        from JMTucker.MFVNeutralino.TriggerFilter_cfi import mfvTriggerFilter as triggerFilter
    elif trigger_filter is not False:
        raise ValueError('trigger_filter %r bad: must be one of ("jets only", "muons only", "electrons only", "bjets only", "met only", "displaced dijet only", "HT OR bjets OR displaced dijet", "bjets OR displaced dijet veto HT", True, False)' % trigger_filter)

    overall = cms.Sequence()

    if trigger_filter:
        triggerFilter = triggerFilter.clone()
        setattr(process, trigger_filter_name, triggerFilter)
        overall *= triggerFilter

    if event_filter:
        print event_filter
        if event_filter == 'jets only':
            from JMTucker.MFVNeutralino.EventFilter_cfi import mfvEventFilterJetsOnly as eventFilter
        elif event_filter == 'muons only':
            from JMTucker.MFVNeutralino.EventFilter_cfi import mfvEventFilterMuonsOnly as eventFilter
        elif event_filter == 'electrons only veto muons':
            from JMTucker.MFVNeutralino.EventFilter_cfi import mfvEventFilterElectronsOnlyVetoMuons as eventFilter
        elif event_filter == 'HT OR bjets OR displaced dijet':
            from JMTucker.MFVNeutralino.EventFilter_cfi import mfvEventFilterHTORBjetsORDisplacedDijet as eventFilter
        elif event_filter == 'bjets OR displaced dijet veto HT':
            from JMTucker.MFVNeutralino.EventFilter_cfi import mfvEventFilterBjetsORDisplacedDijetVetoHT as eventFilter
        elif event_filter == 'met only':
            from JMTucker.MFVNeutralino.EventFilter_cfi import mfvEventFilterMETOnly as eventFilter
        elif event_filter is True:
            from JMTucker.MFVNeutralino.EventFilter_cfi import mfvEventFilter as eventFilter
        elif event_filter is not False:
            raise ValueError('event_filter must be one of ("jets only", "muons only", "electrons only veto muons", "HT OR bjets OR displaced dijet", "bjets OR displaced dijet veto HT", True, False)')

        eventFilter = eventFilter.clone()
        if input_is_miniaod:
            process.load('JMTucker.Tools.UpdatedJets_cff')
            overall *= process.updatedJetsSeqMiniAOD
            eventFilter.jets_src = 'updatedJetsMiniAOD'
            eventFilter.muons_src = 'slimmedMuons'
            eventFilter.electrons_src = 'slimmedElectrons'
        setattr(process, event_filter_name, eventFilter)

        if event_filter_jes_mult > 0:
            from JMTucker.Tools.JetShifter_cfi import jmtJetShifter as jetShifter
            jetShifter = jetShifter.clone()
            if input_is_miniaod:
                jetShifter.jets_src = 'updatedJetsMiniAOD'
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
                process.load('JMTucker.MFVNeutralino.Vertexer_cff')
                if input_is_miniaod:
                    process.goodOfflinePrimaryVertices.src = 'offlineSlimmedPrimaryVertices'
                    process.load('JMTucker.Tools.UnpackedCandidateTracks_cfi')
                    process.mfvVertexTracks.tracks_src = 'jmtUnpackedCandidateTracks'
                    process.jmtRescaledTracks.tracks_src = 'jmtUnpackedCandidateTracks' # JMTBAD use rescaled tracks
            vertexFilter = cms.EDFilter('VertexSelector', src = cms.InputTag('mfvVertices'), cut = cms.string('nTracks > 2'), filter = cms.bool(True))
            setattr(process, event_filter_name + 'W1Vtx', vertexFilter)
            if input_is_miniaod:
                #overall *= process.goodOfflinePrimaryVertices * process.jmtUnpackedCandidateTracks * process.mfvVertexSequenceBare * vertexFilter
                overall *= process.goodOfflinePrimaryVertices * process.updatedJetsSeqMiniAOD * process.selectedPatJets * process.jmtUnpackedCandidateTracks * process.mfvVertexSequenceBare * vertexFilter
            else:
                #overall *= process.goodOfflinePrimaryVertices                                      * process.mfvVertexSequenceBare * vertexFilter
                overall *= process.goodOfflinePrimaryVertices * process.updatedJetsSeqMiniAOD * process.selectedPatJets                                      * process.mfvVertexSequenceBare * vertexFilter
        
    setattr(process, sequence_name, overall)

    if not path_name:
        return overall
    elif hasattr(process, path_name):
        getattr(process, path_name).insert(0, overall)
    else:
        setattr(process, path_name, cms.Path(overall))
        

    if hasattr(process, 'out'):
        assert not hasattr(process.out, 'SelectEvents')
        process.out.SelectEvents = cms.untracked.PSet(SelectEvents = cms.vstring(path_name))
        
