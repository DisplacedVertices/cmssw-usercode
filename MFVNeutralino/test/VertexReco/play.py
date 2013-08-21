import os, sys
from JMTucker.Tools.BasicAnalyzer_cfg import cms, process
from JMTucker.Tools.CMSSWTools import silence_messages

#process.MessageLogger.cerr.FwkReport.reportEvery = 1
process.maxEvents.input = 100
process.options.wantSummary = True
process.source.fileNames = ['/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_1_1_X2h.root']
process.TFileService.fileName = 'play.root'
silence_messages(process, 'TwoTrackMinimumDistance')

process.load('Configuration.Geometry.GeometryIdeal_cff')
process.load('Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.GlobalTag.globaltag = 'START53_V21::All'
process.load('TrackingTools.TransientTrack.TransientTrackBuilder_cfi')
process.load('CommonTools.ParticleFlow.goodOfflinePrimaryVertices_cfi')
process.goodOfflinePrimaryVertices.filter = cms.bool(False)

process.load('JMTucker.MFVNeutralino.RedoPURemoval_cff')
process.load('JMTucker.MFVNeutralino.Vertexer_cff')
process.p = cms.Path(process.goodOfflinePrimaryVertices * process.mfvVertices *
                     process.mfvRedoPURemoval * process.mfvNonPATExtraVertexSequence)

all_anas = []

vertex_srcs = [
    ('MY',     'mfvVertices'),
    ('PF',     'mfvVerticesFromCands'),
    ('PFNPU',  'mfvVerticesFromNoPUCands'),
    ('PFNZPU', 'mfvVerticesFromNoPUNoZCands'),
#    ('JPT',    'mfvVerticesFromJets'),
    ('JPF',    'mfvVerticesFromPFJets'),
    ]

ana = cms.EDAnalyzer('VtxRecoPlay',
                     trigger_results_src = cms.InputTag('TriggerResults', '', 'HLT'),
                     jets_src = cms.InputTag('ak5PFJets'),
                     tracks_src = cms.InputTag('generalTracks'),
                     primary_vertex_src = cms.InputTag('goodOfflinePrimaryVertices'),
                     gen_src = cms.InputTag('genParticles'),
                     vertex_src = cms.InputTag('dummy'),
                     print_info = cms.bool(False),
                     is_mfv = cms.bool(True),
                     is_ttbar = cms.bool(False),
                     do_scatterplots = cms.bool(False),
                     do_ntuple = cms.bool(False),
                     jet_pt_min = cms.double(30),
                     track_pt_min = cms.double(10),
                     track_vertex_weight_min = cms.double(0.5),
                     min_sv_ntracks = cms.int32(0),
                     max_sv_chi2dof = cms.double(1e6),
                     max_sv_err2d   = cms.double(1e6),
                     min_sv_mass    = cms.double(0),
                     min_sv_drmax   = cms.double(0),
                     min_sv_gen3dsig = cms.double(0),
                     max_sv_gen3dsig = cms.double(1e6),
                     )

ana_qcuts = [
    ('Qno',             ana),
    ('Q3dsiglt4',       ana.clone(max_sv_gen3dsig = 4)),
    ('Q3dsigge6',       ana.clone(min_sv_gen3dsig = 6)),
    ('Qntk6',           ana.clone(min_sv_ntracks = 6)),
    ('QM20',            ana.clone(min_sv_mass = 20)),
    ('Qntk6M20',        ana.clone(min_sv_ntracks = 6, min_sv_mass = 20)),
    ]

for vertex_name, vertex_src in vertex_srcs:
    for ana_name, ana in ana_qcuts:
        obj = ana.clone(vertex_src = vertex_src)
        if ana_name == 'Qno' and vertex_name == 'MY':
            obj.do_ntuple = True
        
        setattr(process, 'play' + vertex_name + ana_name, obj)
        all_anas.append(obj)
        process.p *= obj

def gen_length_filter(dist):
    process.load('JMTucker.MFVNeutralino.GenParticleFilter_cfi')
    process.mfvGenParticleFilter.min_rho0 = dist
    process.mfvGenParticleFilter.min_rho1 = dist
    process.p.insert(0, process.mfvGenParticleFilter)
    
def de_mfv():
    if hasattr(process, 'mfvGenParticleFilter'):
        process.mfvGenParticleFilter.cut_invalid = False
    for ana in all_anas:
        ana.is_mfv = False

def sample_ttbar():
    de_mfv()
    for ana in all_anas:
        ana.is_ttbar = True

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

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    assert all_anas[0].is_mfv # de_mfv will be called for non-signal samples below

    if 'debug' in sys.argv:
        raise RuntimeError('refusing to submit jobs in debug (verbose print out) mode')

    import JMTucker.Tools.Samples as Samples
    samples = Samples.mfv_signal_samples + Samples.background_samples + Samples.auxiliary_background_samples

    no = 'mfv_neutralino_tau0000um_M0400 mfv_neutralino_tau0010um_M0400 mfv_neutralino_tau0100um_M0400 mfv_neutralino_tau1000um_M0400 mfv_neutralino_tau9900um_M0400 qcdht0100 qcdht0250 qcdht0500 qcdht1000 ttbardilep ttbarhadronic ttbarsemilep zjetstonunuHT050 zjetstonunuHT100 zjetstonunuHT200 zjetstonunuHT400 dyjetstollM10 dyjetstollM50 qcdmu0015 qcdmu0020 qcdmu0030 qcdmu0050 qcdmu0080 qcdmu0120 qcdmu0170 qcdmu0300 qcdmu0470 qcdmu0600 qcdmu0800 qcdmu1000 qcdmupt15'.split()
    samples = [sample for sample in samples if sample.name not in no]
    for sample in samples:
        if 'mfv' not in sample.name:
            sample.scheduler_name = 'remoteGlidein'

    def pset_modifier(sample):
        to_add = []
        if 'ttbar' in sample.name:
            to_add.append('sample_ttbar()')
        elif 'mfv' not in sample.name:
            to_add.append('de_mfv()')
        return to_add

    from JMTucker.Tools.CRABSubmitter import CRABSubmitter
    cs = CRABSubmitter('VertexRecoPlay',
                       total_number_of_events = 99250,
                       events_per_job = 2500,
                       USER_jmt_skip_input_files = 'src/EGamma/EGammaAnalysisTools/data/*',
                       pset_modifier = pset_modifier,
                       )
    cs.submit_all(samples)

'''
mergeTFileServiceHistograms -w 0.457,0.438,0.105 -i ttbarhadronic.root ttbarsemilep.root ttbardilep.root -o ttbar_merge.root
mergeTFileServiceHistograms -w 0.97336,0.025831,0.00078898,1.9093e-5 -i qcdht0100.root qcdht0250.root qcdht0500.root qcdht1000.root -o qcd_merge.root
'''
