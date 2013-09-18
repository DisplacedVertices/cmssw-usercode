import os, sys
from JMTucker.Tools.BasicAnalyzer_cfg import cms, process
from JMTucker.Tools.CMSSWTools import silence_messages

#process.MessageLogger.cerr.FwkReport.reportEvery = 1
process.maxEvents.input = 100
process.options.wantSummary = True
process.source.fileNames = ['/store/user/jchu/mfv_neutralino_tau1000um_M0400/jtuple_v7/5d4c2a74c85834550d3f9609274e8548/pat_1_1_hdB.root']
process.source.secondaryFileNames = cms.untracked.vstring('/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_891_1_sZ9.root','/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_948_2_lgB.root')
process.TFileService.fileName = 'play.root'
silence_messages(process, 'TwoTrackMinimumDistance')

process.load('Configuration.Geometry.GeometryIdeal_cff')
process.load('Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.GlobalTag.globaltag = 'START53_V21::All'
process.load('TrackingTools.TransientTrack.TransientTrackBuilder_cfi')
process.load('CommonTools.ParticleFlow.goodOfflinePrimaryVertices_cfi')
process.goodOfflinePrimaryVertices.filter = cms.bool(False)

process.load('JMTucker.MFVNeutralino.Vertexer_cff')
process.p = cms.Path(process.goodOfflinePrimaryVertices * process.mfvVertexSequence)

from JMTucker.Tools.general import big_warn
big_warn("\nusing vertices stored in PAT tuple, hope you didn't mean to change their reco\n")
process.p.remove(process.mfvVertices)

#process.load('JMTucker.MFVNeutralino.RedoPURemoval_cff')
#process.p *= process.mfvRedoPURemoval * process.mfvExtraVertexSequence

all_anas = []

vertex_srcs = [
    ('MY',     'mfvVertices'),
#    ('PF',     'mfvVerticesFromCands'),
#    ('PFNPU',  'mfvVerticesFromNoPUCands'),
#    ('PFNPUZ', 'mfvVerticesFromNoPUZCands'),
#    ('JPT',    'mfvVerticesFromJets'),
#    ('JPF',    'mfvVerticesFromPFJets'),
    ]

for name, src in vertex_srcs:
    getattr(process, src).histos = True

ana = cms.EDAnalyzer('VtxRecoPlay',
                     trigger_results_src = cms.InputTag('TriggerResults', '', 'HLT'),
                     pfjets_src = cms.InputTag('ak5PFJets'),
                     jets_src = cms.InputTag('selectedPatJetsPF'),
                     tracks_src = cms.InputTag('generalTracks'),
                     primary_vertex_src = cms.InputTag('goodOfflinePrimaryVertices'),
                     gen_vertices_src = cms.InputTag('mfvGenVertices'),
                     vertex_src = cms.InputTag('dummy'),
                     sv_to_jets_src = cms.InputTag('dummy'),
                     do_scatterplots = cms.bool(False),
                     do_ntuple = cms.bool(False),
                     ntuple_event_mod = cms.int32(1),
                     jet_pt_min = cms.double(30), # JMTBAD keep synchronized with Vertexer_cff
                     track_pt_min = cms.double(10),
                     track_vertex_weight_min = cms.double(0.5),
                     )

sel = process.mfvSelectedVertices.clone() # JMTBAD keep synchronized with Vertexer_cff
v2j = process.mfvVerticesToJets.clone()

sel_qcuts = [
    ('Qno',             sel),
    ('Q3derrlt0p01',    sel.clone(max_err3d = 0.01)),
    ('Q3dsiglt4',       sel.clone(max_gen3dsig = 4)),
    ('Q3dsigge6',       sel.clone(min_gen3dsig = 6)),
    ('Qntk6',           sel.clone(min_ntracks = 6)),  
    ('Qntk6Bntk',       sel.clone(min_ntracks = 6, sort_by = 'ntracks')),
    ('QM20',            sel.clone(min_mass = 20)),
    ('Qntk6M20',        sel.clone(min_ntracks = 6, min_mass = 20)),
    ('Qwow',            sel.clone(min_ntracks = 7, min_maxtrackpt = 15, max_drmin = 0.4, max_drmax = 4, max_bs2derr = 0.005)),
    ]

for vertex_name, vertex_src in vertex_srcs:
    for sel_name, sel in sel_qcuts:
        sel_obj = sel.clone(vertex_src = vertex_src)
        vertex_sel_name = 'sel' + vertex_name + sel_name
        setattr(process, vertex_sel_name, sel_obj)

        v2j_obj = v2j.clone(vertex_src = vertex_sel_name)
        v2j_name = 'v2j' + vertex_name + sel_name
        setattr(process, v2j_name, v2j_obj)
        
        ana_obj = ana.clone(vertex_src = vertex_sel_name,
                            sv_to_jets_src = v2j_name)
        all_anas.append(ana_obj)
        if sel_name == 'Qno' and vertex_name == 'MY':
            ana_obj.do_ntuple = True
        setattr(process, 'play' + vertex_name + sel_name, ana_obj)
        
        process.p *= sel_obj * v2j_obj * ana_obj

def gen_length_filter(dist):
    process.load('JMTucker.MFVNeutralino.GenParticleFilter_cfi')
    process.mfvGenParticleFilter.min_rho0 = dist
    process.mfvGenParticleFilter.min_rho1 = dist
    process.p.insert(0, process.mfvGenParticleFilter)
    
def de_mfv():
    if hasattr(process, 'mfvGenParticleFilter'):
        process.mfvGenParticleFilter.cut_invalid = False
    if hasattr(process, 'mfvGenVertices'):
        process.mfvGenVertices.is_mfv = False

def reduce_trees(factor):
    for ana in all_anas:
        if ana.do_ntuple.value():
            ana.ntuple_event_mod = factor

def sample_ttbar():
    de_mfv()
    if hasattr(process, 'mfvGenVertices'):
        process.mfvGenVertices.is_ttbar = True

def scatterplots(do):
    for ana in all_anas:
        ana.do_scatterplots = do

if 'debug' in sys.argv:
    process.mfvVertices.verbose = True

if 'ttbar' in sys.argv:
    de_mfv()

if 'argv' in sys.argv:
    from JMTucker.Tools.CMSSWTools import file_event_from_argv
    file_event_from_argv(process)

#scatterplots(True)
#process.add_(cms.Service('SimpleMemoryCheck'))
#process.playMYQno.do_scatterplots = True

if 'testttbar' in sys.argv:
    process.source.fileNames = ['']
    process.source.secondaryFileNames = ['']
    sample_ttbar()

if 'testqcd' in sys.argv:
    process.source.fileNames = ['/store/user/jchu/QCD_HT-1000ToInf_TuneZ2star_8TeV-madgraph-pythia6/jtuple_v7/fe6d9f80f9c0fe06cc80b089617fa99d/pat_1_1_NOT.root']
    process.source.secondaryFileNames = ['/store/mc/Summer12_DR53X/QCD_HT-1000ToInf_TuneZ2star_8TeV-madgraph-pythia6/AODSIM/PU_S10_START53_V7A-v1/00000/0038E6D2-860D-E211-9211-00266CFACC38.root','/store/mc/Summer12_DR53X/QCD_HT-1000ToInf_TuneZ2star_8TeV-madgraph-pythia6/AODSIM/PU_S10_START53_V7A-v1/00000/D4C0816B-870D-E211-B094-00266CF258D8.root','/store/mc/Summer12_DR53X/QCD_HT-1000ToInf_TuneZ2star_8TeV-madgraph-pythia6/AODSIM/PU_S10_START53_V7A-v1/00000/A2CEDDF1-870D-E211-A98D-00266CF258D8.root','/store/mc/Summer12_DR53X/QCD_HT-1000ToInf_TuneZ2star_8TeV-madgraph-pythia6/AODSIM/PU_S10_START53_V7A-v1/00000/9E8E388F-970D-E211-8D78-848F69FD298E.root']
    de_mfv()

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    if 'debug' in sys.argv:
        raise RuntimeError('refusing to submit jobs in debug (verbose print out) mode')

    import JMTucker.Tools.Samples as Samples
    ss = set(Samples.mfv_signal_samples)
    first = [Samples.mfv_neutralino_tau0000um_M0400, Samples.mfv_neutralino_tau0100um_M0400, Samples.mfv_neutralino_tau1000um_M0400, Samples.mfv_neutralino_tau9900um_M0400]
    for f in first:
        ss.remove(f)
    rest = sorted(ss, key=lambda s: s.name)
    samples = first + Samples.background_samples + rest

    def pset_modifier(sample):
        to_add = []
        if 'ttbar' in sample.name:
            to_add.append('sample_ttbar()')
        elif 'mfv' not in sample.name:
            to_add.append('de_mfv()')
            factor = 1
            counts = {            
                'wjetstolnu': 656405,
                'ttbarhadronic': 9738903,
                'ttbarsemilep': 7987193,
                'ttbardilep': 1389075,
                'qcdht0100': 4455967,
                'qcdht0250': 11137722,
                'qcdht0500': 4991784,
                'qcdht1000': 6968522,
                }
            if counts.has_key(sample.name):
                factor = round(counts[sample.name]/100000.)
            to_add.append('reduce_trees(%i)' % factor)
        return to_add

    from JMTucker.Tools.CRABSubmitter import CRABSubmitter
    cs = CRABSubmitter('VertexRecoPlay',
                       #total_number_of_events = 99250,
                       #events_per_job = 2500,
                       job_control_from_sample = True,
                       USER_jmt_skip_input_files = 'src/EGamma/EGammaAnalysisTools/data/*',
                       pset_modifier = pset_modifier,
                       use_ana_dataset = True,
                       use_parent = True,
                       #USER_skip_servers = 'unl_hcc-crabserver',
                       #GRID_data_location_override = 'T1_US_FNAL,T2_US_Caltech,T2_US_Florida,T2_US_MIT,T2_US_Nebraska,T2_US_Purdue,T2_US_UCSD,T2_US_Wisconsin',
                       #GRID_remove_default_blacklist = 1,
                       )
    cs.submit_all([s for s in samples if s.name == 'qcdht0100'])

'''
mergeTFileServiceHistograms -w 0.457,0.438,0.105 -i ttbarhadronic.root ttbarsemilep.root ttbardilep.root -o ttbar_merge.root
mergeTFileServiceHistograms -w 0.97336,0.025831,0.00078898,1.9093e-5 -i qcdht0100.root qcdht0250.root qcdht0500.root qcdht1000.root -o qcd_merge.root
'''
