import sys, FWCore.ParameterSet.Config as cms

version = 'v19'

################################################################################

def pat_tuple_process(runOnMC=True, suppress_stdout=True):
    process = cms.Process('PAT')
    process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(100))
    process.source = cms.Source('PoolSource', fileNames = cms.untracked.vstring('/store/mc/Summer12_DR53X/TTJets_HadronicMGDecays_8TeV-madgraph/AODSIM/PU_S10_START53_V7A-v1/00001/FCAF3F92-5A16-E211-ACCC-E0CB4E19F95A.root' if runOnMC else '/store/data/Run2012B/MultiJet1Parked/AOD/05Nov2012-v2/10000/0003D331-5C49-E211-8210-00259020081C.root'))
    process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(False))
    process.load('FWCore.MessageLogger.MessageLogger_cfi')
    process.MessageLogger.cerr.FwkReport.reportEvery = 1000000
    process.MessageLogger.cerr.threshold = 'INFO'
    process.MessageLogger.categories.append('PATSummaryTables')
    process.MessageLogger.cerr.PATSummaryTables = cms.untracked.PSet(limit = cms.untracked.int32(-1))
    for category in ['TwoTrackMinimumDistance']:
        process.MessageLogger.categories.append(category)
        setattr(process.MessageLogger.cerr, category, cms.untracked.PSet(limit=cms.untracked.int32(0)))
    process.load('Configuration.Geometry.GeometryIdeal_cff')
    process.load('Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff')
    process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
    process.GlobalTag.globaltag = 'START53_V27::All' if runOnMC else 'FT53_V21A_AN6::All'
    
    from PhysicsTools.PatAlgos.patEventContent_cff import patEventContent
    process.out = cms.OutputModule('PoolOutputModule',
                                   fileName = cms.untracked.string('pat.root'),
                                   SelectEvents = cms.untracked.PSet(SelectEvents = cms.vstring('p')),
                                   outputCommands = cms.untracked.vstring(*patEventContent),
                                   )
    process.outp = cms.EndPath(process.out)
    
    process.load('JMTucker.Tools.PATTupleSelection_cfi')
    
    # Event cleaning, with MET cleaning recommendations from
    # https://twiki.cern.ch/twiki/bin/view/CMS/MissingETOptionalFilters
    process.load('HLTrigger.special.hltPhysicsDeclared_cfi')
    process.hltPhysicsDeclared.L1GtReadoutRecordTag = 'gtDigis'
    from DPGAnalysis.Skims.goodvertexSkim_cff import noscraping as FilterOutScraping
    process.FilterOutScraping = FilterOutScraping
    process.load('CommonTools.ParticleFlow.goodOfflinePrimaryVertices_cfi')
    process.goodOfflinePrimaryVertices.filter = cms.bool(True)
    process.load('RecoMET.METFilters.metFilters_cff')
    process.trackingFailureFilter.VertexSource = 'goodOfflinePrimaryVertices'
    
    # Instead of filtering out events at tupling time, schedule separate
    # paths for all the "good data" filters so that the results of them
    # get stored in a small TriggerResults::PAT object, which can be
    # accessed later. Make one path for each so they can be accessed
    # separately in the TriggerResults object; the "All" path that is the
    # product of all of the filters isn't necessary but it's nice for
    # convenience.
    process.eventCleaningAll = cms.Path()
    for name in process.jtupleParams.eventFilters.value():
        negate = name.startswith('~')
        name = name.replace('~', '')
        filter_obj = getattr(process, name)
        if negate:
            filter_obj = ~filter_obj
        setattr(process, 'eventCleaning' + name, cms.Path(filter_obj))
        process.eventCleaningAll *= filter_obj
    
    ################################################################################
    
    # PAT/PF2PAT configuration inspired by TopQuarkAnalysis/Configuration
    # (test/patRefSel_allJets_cfg.py and included modules) with tag
    # V07-00-01.
    
    # First, turn off stdout so that the spam from PAT/PF2PAT doesn't
    # flood the screen (especially useful in batch job submission).
    if suppress_stdout:
        print 'tuple.py: PAT would spam a lot of stuff to stdout... hiding it.'
        from cStringIO import StringIO
        old_stdout = sys.stdout
        sys.stdout = buf = StringIO()
    
    jecLevels = ['L1FastJet', 'L2Relative', 'L3Absolute']
    if not runOnMC:
        jecLevels.append('L2L3Residual')
    #jecLevels += ['L5Flavor', 'L7Parton']
    
    postfix = 'PF'
    def processpostfix(name):
        return getattr(process, name + postfix)
    def setprocesspostfix(name, obj):
        setattr(process, name + postfix, obj)
    def InputTagPostFix(name):
        return cms.InputTag(name + postfix)
    
    process.load('PhysicsTools.PatAlgos.patSequences_cff')
    from PhysicsTools.PatAlgos.tools.pfTools import usePF2PAT
    usePF2PAT(process,
              runPF2PAT = True,
              runOnMC = runOnMC,
              jetAlgo = 'AK5',
              postfix = postfix,
              jetCorrections = ('AK5PFchs', jecLevels), # 'chs': using PFnoPU
              typeIMetCorrections = True,
              pvCollection = cms.InputTag('goodOfflinePrimaryVertices'),
              )
    
    processpostfix('pfNoPileUp')  .enable = True  # usePFnoPU
    processpostfix('pfNoMuon')    .enable = True  # useNoMuon
    processpostfix('pfNoElectron').enable = True  # useNoElectron
    processpostfix('pfNoJet')     .enable = True  # useNoJet
    processpostfix('pfNoTau')     .enable = True  # useNoTau
    
    processpostfix('pfPileUp').checkClosestZVertex = False
    processpostfix('pfPileUpIso').checkClosestZVertex = False
    
    processpostfix('pfMuonsFromVertex').d0Cut = processpostfix('pfElectronsFromVertex').d0Cut = 2
    processpostfix('pfMuonsFromVertex').dzCut = processpostfix('pfElectronsFromVertex').dzCut = 2
    
    processpostfix('pfSelectedMuons').cut = 'pt > 5.'
    #processpostfix('pfSelectedMuons').cut += process.jtupleParams.muonCut
    processpostfix('pfIsolatedMuons').isolationCut = 0.2
    
    if False: # pfMuonIsoConeR03
        processpostfix('pfIsolatedMuons').isolationValueMapsCharged  = cms.VInputTag(InputTagPostFix('muPFIsoValueCharged03'))
        processpostfix('pfIsolatedMuons').deltaBetaIsolationValueMap = InputTagPostFix('muPFIsoValuePU03')
        processpostfix('pfIsolatedMuons').isolationValueMapsNeutral  = cms.VInputTag(InputTagPostFix('muPFIsoValueNeutral03'), InputTagPostFix('muPFIsoValueGamma03'))
        processpostfix('pfMuons').isolationValueMapsCharged  = cms.VInputTag(InputTagPostFix('muPFIsoValueCharged03'))
        processpostfix('pfMuons').deltaBetaIsolationValueMap = InputTagPostFix('muPFIsoValuePU03')
        processpostfix('pfMuons').isolationValueMapsNeutral  = cms.VInputTag(InputTagPostFix('muPFIsoValueNeutral03'), InputTagPostFix('muPFIsoValueGamma03'))
        processpostfix('patMuons').isolationValues.pfNeutralHadrons   = InputTagPostFix('muPFIsoValueNeutral03')
        processpostfix('patMuons').isolationValues.pfChargedAll       = InputTagPostFix('muPFIsoValueChargedAll03')
        processpostfix('patMuons').isolationValues.pfPUChargedHadrons = InputTagPostFix('muPFIsoValuePU03')
        processpostfix('patMuons').isolationValues.pfPhotons          = InputTagPostFix('muPFIsoValueGamma03')
        processpostfix('patMuons').isolationValues.pfChargedHadrons   = InputTagPostFix('muPFIsoValueCharged03')
    
    processpostfix('pfSelectedElectrons').cut = 'pt > 5. && gsfTrackRef.isNonnull && gsfTrackRef.trackerExpectedHitsInner.numberOfLostHits < 2'
    #processpostfix('pfSelectedElectrons').cut += ' && ' + process.jtupleParams.electronCut # disabled by default, but can use minimal (veto) electron selection cut on top of pfElectronSelectionCut
    processpostfix('pfIsolatedElectrons').isolationCut = 0.2
    
    if True: # pfElectronIsoConeR03
        processpostfix('pfIsolatedElectrons').isolationValueMapsCharged  = cms.VInputTag(InputTagPostFix('elPFIsoValueCharged03PFId'))
        processpostfix('pfIsolatedElectrons').deltaBetaIsolationValueMap = InputTagPostFix('elPFIsoValuePU03PFId')
        processpostfix('pfIsolatedElectrons').isolationValueMapsNeutral  = cms.VInputTag(InputTagPostFix('elPFIsoValueNeutral03PFId'), InputTagPostFix('elPFIsoValueGamma03PFId'))
        processpostfix('pfElectrons').isolationValueMapsCharged  = cms.VInputTag(InputTagPostFix('elPFIsoValueCharged03PFId'))
        processpostfix('pfElectrons').deltaBetaIsolationValueMap = InputTagPostFix('elPFIsoValuePU03PFId')
        processpostfix('pfElectrons').isolationValueMapsNeutral  = cms.VInputTag(InputTagPostFix('elPFIsoValueNeutral03PFId'), InputTagPostFix('elPFIsoValueGamma03PFId'))
        processpostfix('patElectrons').isolationValues.pfNeutralHadrons   = InputTagPostFix('elPFIsoValueNeutral03PFId')
        processpostfix('patElectrons').isolationValues.pfChargedAll       = InputTagPostFix('elPFIsoValueChargedAll03PFId')
        processpostfix('patElectrons').isolationValues.pfPUChargedHadrons = InputTagPostFix('elPFIsoValuePU03PFId')
        processpostfix('patElectrons').isolationValues.pfPhotons          = InputTagPostFix('elPFIsoValueGamma03PFId')
        processpostfix('patElectrons').isolationValues.pfChargedHadrons   = InputTagPostFix('elPFIsoValueCharged03PFId')
    
    process.load('EgammaAnalysis.ElectronTools.electronIdMVAProducer_cfi')
    processpostfix('patElectrons').electronIDSources.mvaTrigV0    = cms.InputTag("mvaTrigV0")
    processpostfix('patElectrons').electronIDSources.mvaNonTrigV0 = cms.InputTag("mvaNonTrigV0")
    processpostfix('patMuons').embedTrack = True
    processpostfix('patJets').addTagInfos = True
    processpostfix('selectedPatElectrons').cut = process.jtupleParams.electronCut
    processpostfix('selectedPatMuons').cut = process.jtupleParams.muonCut
    processpostfix('selectedPatJets').cut = process.jtupleParams.jetCut
    
    process.load('CMGTools.External.pujetidsequence_cff')
    for x in (process.puJetId, process.puJetMva, process.puJetIdChs, process.puJetMvaChs):
        x.jets = InputTagPostFix('selectedPatJets')
        # fix bug in V00-03-04 of CMGTools/External
        if hasattr(x, 'algos'):
            bad, good = 'RecoJets/JetProducers', 'CMGTools/External'
            for ps in x.algos:
                if hasattr(ps, 'tmvaWeights'):
                    s = ps.tmvaWeights.value()
                    if s.startswith(bad):
                        ps.tmvaWeights = s.replace(bad, good)
    
    from PhysicsTools.PatAlgos.tools.coreTools import runOnData, removeSpecificPATObjects
    if not runOnMC:
        runOnData(process, names = ['All'], postfix = postfix)
    removeSpecificPATObjects(process, names = ['Photons'], postfix = postfix) # will also remove cleaning
    
    # Make some extra SV producers for MFV studies. JMTBAD postfix junk
    for cut in (1., 1.5, 2., 2.5, 3., 3.5, 4., 4.5, 5., 5.5, 6.):
        cut_name = ('%.1f' % cut).replace('.', 'p')
                     
        tag_info_name = 'secondaryVertexMaxDR%sTagInfosAODPF' % cut_name
        tag_info_obj = process.secondaryVertexTagInfosAODPF.clone()
        tag_info_obj.vertexCuts.maxDeltaRToJetAxis = cut
        setattr(process, tag_info_name, tag_info_obj)
        process.patJetsPF.tagInfoSources.append(cms.InputTag(tag_info_name))
    
        processpostfix('patPF2PATSequence').replace(processpostfix('patJets'), tag_info_obj * processpostfix('patJets'))
    
    from JMTucker.Tools.PATTupleSelection_cfi import makeLeptonProducers
    makeLeptonProducers(process, postfix=postfix, params=process.jtupleParams)
    
    common_seq = cms.ignore(process.goodOfflinePrimaryVertices) + cms.ignore(process.mvaTrigV0) + cms.ignore(process.mvaNonTrigV0) + processpostfix('patPF2PATSequence') + process.puJetIdSqeuenceChs
    
    process.load('JMTucker.MFVNeutralino.Vertexer_cff')
    common_seq *= process.mfvVertices
    
    # Require numbers of jets based on the trigger: hadronic channel will
    # have at least a 4-jet trigger (maybe 6!), while semileptonic uses a
    # 3-jet trigger. Dileptonic has no jets in trigger, but we'll require
    # at least one b-tag anyway.
    setprocesspostfix('countPatJetsHadronic',     processpostfix('countPatJets').clone(minNumber = 4))
    setprocesspostfix('countPatJetsSemileptonic', processpostfix('countPatJets').clone(minNumber = 3))
    setprocesspostfix('countPatJetsDileptonic',   processpostfix('countPatJets').clone(minNumber = 1))
    
    channels = ('Hadronic', 'Semileptonic', 'Dileptonic')
    for channel in channels:
        setattr(process, 'p' + channel, cms.Path(common_seq))
    
    process.pHadronic     *= processpostfix('countPatJetsHadronic')
    process.pSemileptonic *= processpostfix('countPatJetsSemileptonic') + process.jtupleSemileptonSequence + process.countSemileptons
    process.pDileptonic   *= processpostfix('countPatJetsDileptonic')   + process.jtupleDileptonSequence   + process.countDileptons
    
    process.out.SelectEvents.SelectEvents = ['p' + channel for channel in channels]
    process.out.outputCommands = [
        'drop *',
        'keep *_selectedPatElectrons*_*_*',
        'keep *_selectedPatMuons*_*_*',
        'keep *_selectedPatJets*_*_*',
        'drop *_selectedPatJetsForMETtype1p2CorrPF_*_*',
        'drop *_selectedPatJetsForMETtype2CorrPF_*_*',
        'keep *_mfvVertices*_*_*',
        'drop CaloTowers_*_*_*',
        'keep *_patMETs*_*_*',
        'keep *_goodOfflinePrimaryVertices_*_*',
        'keep edmTriggerResults_TriggerResults__PAT', # for post-tuple filtering on the goodData paths
        'keep *_puJet*_*_*',
        ]
    
    # The normal TrigReport doesn't state how many events are written
    # total to the file in case of OutputModule's SelectEvents having
    # multiple paths. Add a summary to stdout that so that it is easy to
    # see what the total number of events should be (for debugging CRAB
    # jobs). (This means we can kill the normal TrigReport.)
    process.ORTrigReport = cms.EDAnalyzer('ORTrigReport',
                                          results_src = cms.InputTag('TriggerResults', '', process.name_()),
                                          paths = process.out.SelectEvents.SelectEvents
                                          )
    process.pORTrigReport = cms.EndPath(process.ORTrigReport) # Must be on an EndPath.
    
    # As a simple check of the paths' efficiencies, add some lines to the
    # summary showing stats on events with generator-level muons/electrons
    # in acceptance from W decays.
    if runOnMC:
        for name, cut in [('Muon',     'abs(pdgId) == 13 && abs(eta) < 2.4 && abs(mother.pdgId) == 24 && pt > 20'),
                          ('Electron', 'abs(pdgId) == 11 && abs(eta) < 2.5 && abs(mother.pdgId) == 24 && pt > 20'),
                          ('Lepton',   '((abs(pdgId) == 13 && abs(eta) < 2.4) || (abs(pdgId) == 11 && abs(eta) < 2.5)) && abs(mother.pdgId) == 24 && pt > 20'),
                          ]:
            name = 'gen' + name + 's'
            filter = cms.EDFilter('CandViewSelector', src = cms.InputTag('genParticles'), cut = cms.string(cut))
            counter = cms.EDFilter('CandViewCountFilter', src = cms.InputTag(name), minNumber = cms.uint32(1))
            setattr(process, name,           filter)
            setattr(process, name + 'Count', counter)
            setattr(process, 'p' + name + 'Count', cms.Path(filter*counter))
    
    # Check that the stdout spam from PAT was what we expect.
    if suppress_stdout:
        pat_output = buf.getvalue()
        sys.stdout = old_stdout
        buf.close()
        hsh = hash(pat_output)
        #open('pat_spam.txt', 'wt').write(pat_output)
        hsh_expected = 6563257886911239637 if runOnMC else 3125511795667431709
        print 'PAT is done (spam hash %s, expected %s).' % (hsh, hsh_expected)
        if hsh != hsh_expected:
            from JMTucker.Tools.general import big_warn
            big_warn('Unexpected spam hash! Did you change an option?')

    return process, common_seq

################################################################################

def input_is_fastsim(process):
    for name in 'HBHENoiseFilter CSCTightHaloFilter'.split():
        delattr(process, 'eventCleaning' + name)
        process.eventCleaningAll.remove(getattr(process, name))
    process.pfNoPileUp.bottomCollection = 'FSparticleFlow'
    process.pfPileUp.PFCandidates = 'FSparticleFlow'
    process.pfNoPileUpPF.bottomCollection = 'FSparticleFlow'
    process.pfPileUpPF.PFCandidates = 'FSparticleFlow'
    process.pfCandsNotInJet.bottomCollection = 'FSparticleFlow'
    process.pfCandsNotInJetPF.bottomCollection = 'FSparticleFlow'

def input_is_pythia8(process):
    process.patJetPartonMatch.mcStatus = cms.vint32(21,22,23,24,25,26,27,28,29)
    process.patJetPartonMatchPF.mcStatus = cms.vint32(21,22,23,24,25,26,27,28,29)

def keep_general_tracks(process):
    process.out.outputCommands.append('keep *_generalTracks_*_*')

def keep_selected_tracks(process):
    process.selectTracks = cms.EDFilter('TrackSelector',
                                        src = cms.InputTag('generalTracks'),
                                        filter = cms.bool(False),
                                        cut = cms.string('pt > 0.8 && abs(eta) < 2.5 && hitPattern.numberOfValidHits > 7'),
                                        )
    for p in (process.pHadronic, process.pSemileptonic, process.pDileptonic):
        p.insert(0, process.selectTracks)
    process.out.outputCommands.append('keep *_selectTracks_*_*')

def no_skimming_cuts(process):
    try:
        del process.out.SelectEvents
    except AttributeError:
        pass

def drop_gen_particles(process):
    process.out.outputCommands.append('drop *_genParticles_*_*')

def aod_plus_pat(process):
    if runOnMC:
        from Configuration.EventContent.EventContent_cff import AODSIMEventContent as aod
        aod.outputCommands += ['keep *_mfvTrackMatches_*_*']
    else:
        from Configuration.EventContent.EventContent_cff import AODEventContent as aod
    old_cmds = [x for x in process.out.outputCommands.value() if x.strip() != 'drop *']
    process.out.outputCommands = aod.outputCommands + old_cmds
    process.out.fileName = 'aodpat.root'

def keep_random_state(process):
    process.out.outputCommands.append('keep *_randomEngineStateProducer_*_*')

def keep_mixing_info(process):
    process.out.outputCommands.append('keep CrossingFramePlaybackInfoExtended_*_*_*')

def disable_nopileup(process):
    processpostfix('pfNoPileUp').enable = False

def re_pat(process, name='PAT2', old_name='PAT'):
    process.source.inputCommands = cms.untracked.vstring('keep *', 'drop *_*_*_%s' % old_name)
    process.setName_(name)
    process.ORTrigReport.results_src.setProcessName(name)
    process.out.outputCommands.append('keep edmTriggerResults_TriggerResults__%s' % name)

def pileup_removal_studies(process, keep_nopileup=True, no_closest_z_vtx=True):
    process.out.outputCommands.append('keep *_pfPileUp%s_*_*' % postfix)
    if keep_nopileup:
        process.out.outputCommands.append('keep *_pfNoPileUp%s_*_*' % postfix)
    if no_closest_z_vtx:
        setprocesspostfix('pfPileUpNoClosestZVertex',   processpostfix('pfPileUp').clone(checkClosestZVertex = False))
        setprocesspostfix('pfNoPileUpNoClosestZVertex', processpostfix('pfNoPileUp').clone(topCollection = 'pfPileUpPFNoClosestZVertex'))
        processpostfix('patPF2PATSequence').replace(processpostfix('pfPileUp'),   processpostfix('pfPileUp')   + processpostfix('pfPileUpNoClosestZVertex'))
        processpostfix('patPF2PATSequence').replace(processpostfix('pfNoPileUp'), processpostfix('pfNoPileUp') + processpostfix('pfNoPileUpNoClosestZVertex'))
        process.out.outputCommands.append('keep *_pfPileUpNoClosestZVertex%s_*_*' % postfix)
        if keep_nopileup:
            process.out.outputCommands.append('keep *_pfNoPileUpNoClosestZVertex%s_*_*' % postfix)

def closest_z_in_pu(process):
    processpostfix('pfPileUp').checkClosestZVertex = True
    processpostfix('pfPileUpIso').checkClosestZVertex = True

def disable_pujetid(process):
    for p in process.paths_():
        getattr(process, p).remove(process.puJetIdChs)
        getattr(process, p).remove(process.puJetMvaChs)

def dummy_beamspot(process, params):
    if type(params) == str:
        import JMTucker.Tools.DummyBeamSpots_cff as DummyBeamSpots
        params = getattr(DummyBeamSpots, params)

    process.myBeamSpot = cms.EDProducer('DummyBeamSpotProducer', params)

    for name, path in process.paths.items():
        path.insert(0, process.myBeamSpot)

    for name, out in process.outputModules.items():
        new_cmds = []
        for cmd in out.outputCommands:
            if 'offlineBeamSpot' in cmd:
                new_cmds.append(cmd.replace('offlineBeamSpot', 'myBeamSpot'))
        out.outputCommands += new_cmds

    import itertools
    from PhysicsTools.PatAlgos.tools.helpers import massSearchReplaceAnyInputTag
    for path_name, path in itertools.chain(process.paths.iteritems(), process.endpaths.iteritems()):
        massSearchReplaceAnyInputTag(path, cms.InputTag('offlineBeamSpot'), cms.InputTag('myBeamSpot'), verbose=True)

if __name__ == '__main__':
    # JMTBAD no idea if this works with submit_tuple.py ...
    process = pat_tuple_process()[0]
    if 'dump' in sys.argv:
        open('dumptup.py','wt').write(process.dumpPython())

    # JMTBAD does this work with straight cmsRun?
    for arg in 'input_is_fastsim input_is_pythia8 keep_general_tracks keep_selected_tracks no_skimming_cuts drop_gen_particles aod_plus_pat keep_random_state keep_mixing_info disable_nopileup re_pat pileup_removal_studies closest_z_in_pu'.split():
        if arg in sys.argv:
            exec '%s(process)' % arg
