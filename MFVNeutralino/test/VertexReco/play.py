import os, sys
from JMTucker.Tools.BasicAnalyzer_cfg import cms, process
from JMTucker.Tools.CMSSWTools import silence_messages

#process.MessageLogger.cerr.FwkReport.reportEvery = 1
process.maxEvents.input = 100
process.options.wantSummary = True
process.source.fileNames = ['file:/uscms/home/tucker/nobackup/fromt3/mfv_neutralino_tau1000um_M0400_jtuple_v6_547d3313903142038335071634b26604_pat_1_1_Dpa.root']
process.TFileService.fileName = 'play.root'
silence_messages(process, 'TwoTrackMinimumDistance')

process.load('Configuration.Geometry.GeometryIdeal_cff')
process.load('Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.GlobalTag.globaltag = 'START53_V21::All'
process.load('TrackingTools.TransientTrack.TransientTrackBuilder_cfi')

process.load('JMTucker.MFVNeutralino.VertexReco_cff')
process.mfvInclusiveVertexFinder.vertexMinAngleCosine = 0.75
process.load('JMTucker.MFVNeutralino.Vertexer_cff')
process.p = cms.Path(process.mfvVertexReco * process.mfvVertices)
#process.p = cms.Path(process.goodOfflinePrimaryVertices * process.mfvVertices)

all_anas = []

vertex_srcs = [
    ('MY', 'mfvVertices'),
    ('IVFC75MrgdS', 'mfvVertexMergerShared'),
    ]

ana = cms.EDAnalyzer('VtxRecoPlay',
                     tracks_src = cms.InputTag('generalTracks'),
                     primary_vertex_src = cms.InputTag('goodOfflinePrimaryVertices'),
                     gen_src = cms.InputTag('genParticles'),
                     vertex_src = cms.InputTag('dummy'),
                     print_info = cms.bool(False),
                     is_mfv = cms.bool(True),
                     is_ttbar = cms.bool(False),
                     do_scatterplots = cms.bool(True),
                     jet_pt_min = cms.double(30),
                     track_pt_min = cms.double(10),
                     min_sv_ntracks = cms.int32(0),
                     max_sv_chi2dof = cms.double(1e6),
                     max_sv_err2d   = cms.double(1e6),
                     min_sv_mass    = cms.double(0),
                     min_sv_drmax   = cms.double(0),
                     )

ana_qcuts = [
    ('Qno',             ana),
    ('Qntk6',           ana.clone(min_sv_ntracks = 6)),
    ('Qntk6M20',        ana.clone(min_sv_ntracks = 6, min_sv_mass = 20)),
    ]

for vertex_name, vertex_src in vertex_srcs:
    for ana_name, ana in ana_qcuts:
        obj = ana.clone(vertex_src = vertex_src)
        if 'IVF' in vertex_src:
            obj.do_scatterplots = False
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
    
def no_scatterplots():
    for ana in all_anas:
        ana.do_scatterplots = False

if 'debug' in sys.argv:
    if 'ttbar' in sys.argv:
        de_mfv()

    if 'argv' in sys.argv:
        from JMTucker.Tools.CMSSWTools import file_event_from_argv
        file_event_from_argv(process)

    process.mfvVertices.verbose = True

#no_scatterplots()
#process.add_(cms.Service('SimpleMemoryCheck'))

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    assert all_anas[0].is_mfv # de_mfv will be called for non-signal samples below

    if 'debug' in sys.argv:
        raise RuntimeError('refusing to submit jobs in debug (verbose print out) mode')

    from JMTucker.Tools.Samples import mfv_neutralino_tau0000um_M0400, mfv_neutralino_tau1000um_M0400, mfv_neutralino_tau9900um_M0400, ttbarincl, qcdht0100, qcdht0250, qcdht0500, qcdht1000
    samples = [mfv_neutralino_tau0000um_M0400, mfv_neutralino_tau1000um_M0400, mfv_neutralino_tau9900um_M0400, ttbarincl] #, qcdht0100, qcdht0250, qcdht0500, qcdht1000]

    def pset_modifier(sample):
        to_add = []
        if 'mfv' not in sample.name:
            to_add.append('de_mfv()')
        elif 'ttbar' in sample.name:
            to_add.append('sample_ttbar()')
        return to_add
        
    from JMTucker.Tools.CRABSubmitter import CRABSubmitter
    cs = CRABSubmitter('VertexRecoPlay',
                       total_number_of_events = 10000,
                       events_per_job = 1000,
                       USER_jmt_skip_input_files = 'src/EGamma/EGammaAnalysisTools/data/*',
                       pset_modifier = pset_modifier,
                       )
    cs.submit_all(samples)
