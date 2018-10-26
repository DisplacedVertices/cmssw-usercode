import FWCore.ParameterSet.Config as cms

def event_histos(process, mode):
    if mode:
        process.load('JMTucker.MFVNeutralino.WeightProducer_cfi')
        process.load('JMTucker.MFVNeutralino.EventHistos_cfi')
        process.load('JMTucker.MFVNeutralino.AnalysisCuts_cfi')

        process.mfvEventForHistos = process.mfvEvent.clone(vertex_seed_tracks_src = cms.InputTag('mfvVertexTracks', 'seed'))
        process.mfvWeightForHistos = process.mfvWeight.clone(mevent_src = 'mfvEventForHistos', throw_if_no_mcstat = False)
        process.mfvAnalysisCutsForJetHistos = process.mfvAnalysisCuts.clone(mevent_src = 'mfvEventForHistos', apply_vertex_cuts = False)
        process.mfvAnalysisCutsForLeptonHistos = process.mfvAnalysisCutsForJetHistos.clone(apply_presel = 2)

        process.mfvEventHistosJetPreSel = process.mfvEventHistos.clone(mevent_src = 'mfvEventForHistos', weight_src = 'mfvWeightForHistos')
        process.mfvEventHistosLeptonPreSel = process.mfvEventHistosJetPreSel.clone()

        process.eventHistosPreSeq = cms.Sequence(process.mfvTriggerFilter * process.goodOfflinePrimaryVertices *
                                                 process.selectedPatJets * process.selectedPatMuons * process.selectedPatElectrons *
                                                 process.mfvTriggerFloats * process.mfvGenParticles *
                                                 process.mfvUnpackedCandidateTracks * process.mfvVertexTracks *
                                                 process.mfvEventForHistos * process.mfvWeightForHistos)

        process.pEventHistosJetPreSel = cms.Path(process.eventHistosPreSeq * process.mfvAnalysisCutsForJetHistos    * process.mfvEventHistosJetPreSel)
        process.pEventHistosLepPreSel = cms.Path(process.eventHistosPreSeq * process.mfvAnalysisCutsForLeptonHistos * process.mfvEventHistosLeptonPreSel)

        if mode == 'only':
            del process.out
            del process.outp
            del process.p
