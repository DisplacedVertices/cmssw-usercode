import FWCore.ParameterSet.Config as cms

def run_n_tk_seeds(process, mode, output_commands):
    if mode:
        process.mfvEvent.lightweight = True
        process.out.fileName = 'ntkseeds.root'
        if mode != 'full':
            output_commands.remove('keep MFVVertexAuxs_mfvVerticesAux_*_*')
        from JMTucker.MFVNeutralino.Vertexer_cff import modifiedVertexSequence
        output_commands += ['keep VertexerPairEffs_mfvVertices_*_*']
        for n_tk_seed in 3,4,5:
            ex = '%iTkSeed' % n_tk_seed
            process.p *= modifiedVertexSequence(process, ex, n_tracks_per_seed_vertex = n_tk_seed)
            output_commands += ['keep VertexerPairEffs_mfvVertices%s_*_*' % ex]
            if mode == 'full':
                output_commands += ['keep MFVVertexAuxs_mfvVerticesAux%s_*_*' % ex]

def prepare_vis(process, mode, output_commands, cmssw_settings):
    if mode:
        process.load('JMTucker.MFVNeutralino.VertexSelector_cfi')
        process.p *= process.mfvSelectedVerticesSeq

        for x in process.mfvSelectedVerticesTight, process.mfvSelectedVerticesTightNtk3, process.mfvSelectedVerticesTightNtk4:
            x.produce_vertices = True
            x.produce_tracks = True

        process.load('JMTucker.MFVNeutralino.VertexRefitter_cfi')
        process.mfvVertexRefitsDrop0 = process.mfvVertexRefits.clone(n_tracks_to_drop = 0)
        process.mfvVertexRefitsDrop2 = process.mfvVertexRefits.clone(n_tracks_to_drop = 2)
        process.p *= process.mfvVertexRefits * process.mfvVertexRefitsDrop2 *  process.mfvVertexRefitsDrop0

        output_commands += [
            'keep *_mfvVertices_*_*',
            'keep *_mfvSelectedVerticesTight*_*_*',
            'keep *_mfvVertexRefits_*_*',
            'keep *_mfvVertexRefitsDrop2_*_*',
            'keep *_mfvVertexRefitsDrop0_*_*',
            ]

        if cmssw_settings.is_mc:
            output_commands += ['keep *_mfvGenParticles_*_*']

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

def minitree_only(process, mode):
    if mode:
        del process.out
        del process.outp
        process.TFileService.fileName = 'minintuple.root'
        process.load('JMTucker.MFVNeutralino.MiniTree_cff')
        process.mfvWeight.throw_if_no_mcstat = False
        for p in process.pMiniTree, process.pMiniTreeNtk3, process.pMiniTreeNtk4, process.pMiniTreeNtk3or4:
            p.insert(0, process.pmcStat._seq)
            p.insert(0, process.p._seq)
