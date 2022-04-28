from JMTucker.Tools.CMSSWTools import *
from JMTucker.Tools.Year import year

ntuple_version_ = 'V27'
use_btag_triggers = False
if use_btag_triggers : 
    ntuple_version_ += "B" # for "Btag triggers"; also includes DisplacedDijet triggers
ntuple_version_use = ntuple_version_ + 'm'
dataset = 'ntuple' + ntuple_version_use.lower()

def run_n_tk_seeds(process, mode, settings, output_commands):
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

def prepare_vis(process, mode, settings, output_commands):
    if mode:
        process.load('JMTucker.MFVNeutralino.VertexSelector_cfi')
        process.p *= process.mfvSelectedVerticesSeq

        for x in process.mfvSelectedVerticesTight, process.mfvSelectedVerticesTightNtk3, process.mfvSelectedVerticesTightNtk4:
            x.produce_vertices = True
            x.produce_tracks = True
            x.vertex_src = 'mfvVertices'

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

        if settings.is_mc:
            output_commands += ['keep *_mfvGenParticles_*_*']

def minitree_only(process, mode, settings, output_commands):
    if mode:
        mode = str(mode)

        if 'both' not in mode:
            del process.out
            del process.outp

        if '2' in mode:
            from JMTucker.Tools.NtupleFiller_cff import jmtNtupleFiller_pset
            process.load('JMTucker.MFVNeutralino.VertexSelector_cfi')
            process.load('JMTucker.MFVNeutralino.AnalysisCuts_cfi')
            from JMTucker.MFVNeutralino.Vertexer_cfi import kvr_params
            process.mfvMiniTree2 = cms.EDAnalyzer('MFVMiniTreer2',
                                                  jmtNtupleFiller_pset(settings.is_miniaod, True),
                                                  kvr_params = kvr_params,
                                                  vertices_src = cms.InputTag('mfvVertices'),
                                                  auxes_src = cms.InputTag('mfvVerticesAuxPresel'),
                                                  vertex_sel = cms.string('tight' if 'tight' in mode else 'loose'),
                                                  )
            weight_obj = process.jmtWeightMiniAOD if settings.is_miniaod else process.jmtWeight
            process.p *= weight_obj * process.mfvMiniTree2
        else:
            process.load('JMTucker.MFVNeutralino.MiniTree_cff')
            process.mfvWeight.throw_if_no_mcstat = False
            for p in process.pMiniTree, process.pMiniTreeNtk3, process.pMiniTreeNtk4, process.pMiniTreeNtk3or4:
                p.insert(0, process.pmcStat._seq)
                p.insert(0, process.p._seq)

        process.TFileService.fileName = 'minintuple.root'

#updated event_filter : takes in two modes; the default and rp_mode, indexed at 0 & 1 respectfully  
def event_filter(process, mode, settings, output_commands, **kwargs):
    if mode[0] or mode[1]:
        from JMTucker.MFVNeutralino.EventFilter import setup_event_filter
        setup_event_filter(process, input_is_miniaod=settings.is_miniaod, mode=mode[0], rp_mode=mode[1], **kwargs)

########################################################################

class NtupleSettings(CMSSWSettings):
    def __init__(self):
        super(NtupleSettings, self).__init__()

        self.run_n_tk_seeds = False
        self.minitree_only = False
        self.prepare_vis = False
        self.keep_all = False
        self.keep_gen = False
        self.event_filter = True
        self.randpars_filter = False


    @property
    def version(self):
        if self.is_miniaod:
            return ntuple_version_ + 'm'
        else:
            return ntuple_version_

    def normalize(self):
        if self.run_n_tk_seeds:
            self.event_filter = 'trigger jets only' # JMTBAD

        if not self.keep_all and self.prepare_vis:
            print 'setting keep_all True because prepare_vis is True'
            self.keep_all = True

        if self.keep_all and self.event_filter:
            print 'setting event_filter to False because keep_all is True'
            self.event_filter = False

        if len(filter(None, (self.run_n_tk_seeds, self.minitree_only, self.prepare_vis))) > 1:
            raise ValueError('only one of run_n_tk_seeds, minitree_only, prepare_vis allowed')

    def batch_name(self):
        s = 'Ntuple' + self.version

        if self.run_n_tk_seeds:
            s += '_NTkSeeds'
        elif self.minitree_only:
            s += '_MiniNtuple'
        elif self.prepare_vis:
            s += '_PrepareVis'

        if self.keep_gen:
            s += '_WGen'

        if not self.event_filter:
            s += '_NoEF'

        return s

def make_output_commands(process, settings):
    output_commands = [
        'drop *',
        'keep *_mcStat_*_*',
        'keep MFVVertexAuxs_mfvVerticesAux_*_*',
        'keep MFVEvent_mfvEvent__*',
        ]

    if settings.keep_gen:
        if settings.is_miniaod:
            output_commands += ['keep *_prunedGenParticles_*_*', 'keep *_packedGenParticles_*_*', 'keep *_slimmedGenJets_*_*']
        else:
            output_commands += ['keep *_genParticles_*_HLT',     'keep *_ak4GenJetsNoNu_*_HLT']

    if settings.keep_all:
        def dedrop(l):
            return [x for x in l if not x.strip().startswith('drop')]
        our_output_commands = output_commands
        import Configuration.EventContent.EventContent_cff as ec
        output_commands = ec.AODSIMEventContent.outputCommands if settings.is_mc else ec.AODEventContent.outputCommands
        if settings.is_miniaod:
            output_commands += dedrop(ec.MINIAODSIMEventContent.outputCommands if settings.is_mc else ec.MINIAODEventContent.outputCommands)
        output_commands += dedrop(our_output_commands)

    return output_commands

def set_output_commands(process, cmds):
    if hasattr(process, 'out'):
        process.out.outputCommands = cmds

def aod_ntuple_process(settings):
    settings.normalize()

    from JMTucker.Tools import MiniAOD_cfg as mcfg
    process = mcfg.pat_tuple_process(settings)
    mcfg.remove_met_filters(process)
    process.out.fileName = 'ntuple.root'
    # turn off embedding so we can match leptons by track to vertices
    process.patMuons.embedTrack = False
    process.patElectrons.embedTrack = False

    random_service(process, {'mfvVertexTracks': 1222})
    tfileservice(process, 'vertex_histos.root')

    for x in process.patAlgosToolsTask, process.slimmingTask, process.packedPFCandidatesTask, process.patTask, process.pfNoPileUpJMETask:
        x.remove(process.goodOfflinePrimaryVertices)
    process.load('JMTucker.Tools.AnalysisEras_cff')
    process.load('JMTucker.Tools.GoodPrimaryVertices_cfi')
    process.load('JMTucker.Tools.WeightProducer_cfi')
    process.load('JMTucker.MFVNeutralino.Vertexer_cff')
    process.load('JMTucker.MFVNeutralino.TriggerFilter_cfi')
    process.load('JMTucker.MFVNeutralino.TriggerFloats_cff')
    process.load('JMTucker.MFVNeutralino.EventProducer_cfi')

    process.p = cms.Path(process.goodOfflinePrimaryVertices *
                         process.mfvVertexSequence *
                         process.mfvTriggerFloats *
                         process.mfvEvent)

    process.mfvEvent.misc_srcs = [x for x in process.mfvEvent.misc_srcs if x.moduleLabel != 'prefiringweight'] # JMTBAD doesn't work with miniaod-on-fly here

    output_commands = make_output_commands(process, settings)

    mods = [
        (prepare_vis,    settings.prepare_vis),
        (run_n_tk_seeds, settings.run_n_tk_seeds),
        (event_filter,   settings.event_filter),
        (minitree_only,  settings.minitree_only),
        ]
    for modifier, mode in mods:
        modifier(process, mode, settings, output_commands)

    set_output_commands(process, output_commands)

    mcfg.associate_paths_to_task(process)

    #bef, aft, diff = ReferencedTagsTaskAdder().modules_to_add('patJets', 'patMuons', 'patElectrons', 'mfvEvent')
    #print 'may need to add:', ' '.join(diff)
    # but remove things already in AOD

    return process

def miniaod_ntuple_process(settings):
    settings.normalize()
    assert settings.is_miniaod

    process = basic_process('Ntuple')
    registration_warnings(process)
    report_every(process, 1000000)
    geometry_etc(process, which_global_tag(settings))
    random_service(process, {'mfvVertexTracks': 1222})
    tfileservice(process, 'vertex_histos.root')
    output_file(process, 'ntuple.root', [])

    process.load('PhysicsTools.PatAlgos.selectionLayer1.jetSelector_cfi')
    process.load('PhysicsTools.PatAlgos.selectionLayer1.muonSelector_cfi')
    process.load('PhysicsTools.PatAlgos.selectionLayer1.electronSelector_cfi')
    process.load('JMTucker.Tools.AnalysisEras_cff')
    process.load('JMTucker.Tools.GoodPrimaryVertices_cfi')
    process.load('JMTucker.Tools.L1ECALPrefiringWeightProducer_cfi')
    process.load('JMTucker.Tools.MCStatProducer_cff')
    process.load('JMTucker.Tools.UpdatedJets_cff')
    process.load('JMTucker.Tools.PATTupleSelection_cfi')
    process.load('JMTucker.Tools.WeightProducer_cfi')
    process.load('JMTucker.Tools.UnpackedCandidateTracks_cfi')
    process.load('JMTucker.MFVNeutralino.Vertexer_cff')
    process.load('JMTucker.MFVNeutralino.TriggerFilter_cfi')
    process.load('JMTucker.MFVNeutralino.TriggerFloats_cff')
    process.load('JMTucker.MFVNeutralino.EventProducer_cfi')

    process.goodOfflinePrimaryVertices.input_is_miniaod = True
    process.selectedPatJets.src = 'updatedJetsMiniAOD'
    process.selectedPatMuons.src = 'slimmedMuons'
    process.selectedPatElectrons.src = 'slimmedElectrons'
    process.selectedPatJets.cut = process.jtupleParams.jetCut
    #process.selectedPatMuons.cut = '' # process.jtupleParams.muonCut
    #process.selectedPatElectrons.cut = '' # process.jtupleParams.electronCut

    process.mfvGenParticles.gen_particles_src = 'prunedGenParticles'
    process.mfvGenParticles.last_flag_check = False

    process.jmtRescaledTracks.tracks_src = 'jmtUnpackedCandidateTracks'

    for x in process.mfvVerticesToJets, process.mfvVerticesAuxTmp, process.mfvVerticesAuxPresel:
        x.track_ref_getter.input_is_miniaod = True

    process.mfvEvent.input_is_miniaod = True
    process.mfvEvent.gen_particles_src = 'prunedGenParticles' # no idea if this lets gen_bquarks, gen_leptons work--may want the packed ones that have status 1 particles
    process.mfvEvent.gen_jets_src = 'slimmedGenJets'
    process.mfvEvent.pileup_info_src = 'slimmedAddPileupInfo'
    process.mfvEvent.met_src = 'slimmedMETs'

    process.p = cms.Path(process.goodOfflinePrimaryVertices *
                         process.updatedJetsSeqMiniAOD *
                         process.selectedPatJets *
                         process.selectedPatMuons *
                         process.selectedPatElectrons *
                         process.mfvTriggerFloats *
                         process.jmtUnpackedCandidateTracks *
                         process.mfvVertexSequence *
                         process.prefiringweight *
                         process.mfvEvent)

    output_commands = make_output_commands(process, settings)

    mods = [
        (prepare_vis,    settings.prepare_vis),
        (run_n_tk_seeds, settings.run_n_tk_seeds),
        (event_filter,   [settings.event_filter, settings.randpars_filter]),
        (minitree_only,  settings.minitree_only),
        ]
    for modifier, mode in mods:
        modifier(process, mode, settings, output_commands)

    set_output_commands(process, output_commands)

    return process

def ntuple_process(settings):
    if settings.is_miniaod:
        return miniaod_ntuple_process(settings)
    else:
        return aod_ntuple_process(settings)

# Used for samples stored in inclusive miniaods; currently set up for ZH and Wplus
# may need to change to handle different naming conventions 
def signal_uses_random_pars_modifier(sample): 
    to_replace = []

    if sample.is_signal:
        if sample.name.startswith('ZH_') or sample.name.startswith('Wplus'):
            magic_randpar = 'randpars_filter = False'
            
            decay = sample.name[sample.name.find('_')+1 : sample.name.find('_Z')]
            
            if sample.tau < 1000 :
                ctau = float(sample.tau)/1000
                ctau = str(ctau).replace('.', 'p')
            else :
                ctau = str(sample.tau/1000)
                
            to_replace.append((magic_randpar, "randpars_filter = 'randpar %s M%i_ct%s-'" % (decay, sample.mass, ctau), 'tuple template does not contain the magic string "%s"' % magic_randpar))
    return [], to_replace


def signals_no_event_filter_modifier(sample):
    if sample.is_signal:
        if use_btag_triggers :
            magic = "event_filter = 'bjets OR displaced dijet veto HT'"
        else :
            magic = "event_filter = 'jets only'"
        to_replace = [(magic, 'event_filter = False', 'tuple template does not contain the magic string "%s"' % magic)]
    else:
        to_replace = []
    return [], to_replace

def remove_output_module(process):
    del process.out
    del process.outp
