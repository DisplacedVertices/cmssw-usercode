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
process.p = cms.Path(process.mfvVertexReco)

all_anas = []

for suffix in ('', 'Cos75'):
    vertex_srcs = [
        ('IVF', 'mfvInclusiveVertexFinder'),
        ('IVFMrgd', 'mfvVertexMerger'),
        ('IVFMrgdArbd', 'mfvTrackVertexArbitrator'),
        ('IVFMrgdArbdMrgd', 'mfvInclusiveMergedVertices'),
        ('IVFMrgdS', 'mfvVertexMergerShared'),
        ('IVFMrgdSArbd', 'mfvTrackVertexArbitratorShared'),
        ('IVFMrgdSArbdMrgdS', 'mfvInclusiveMergedVerticesShared'),
        ]

    if suffix:
        from JMTucker.MFVNeutralino.VertexReco_cff import clone_all
        objs = clone_all(process, suffix)
        if suffix == 'Cos75':
            objs[0].vertexMinAngleCosine = 0.75
        process.p *= objs[-1] # this vtx reco sequence
        
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
        ('Qntk6M20DRM1',    ana.clone(min_sv_ntracks = 6, min_sv_mass = 20, min_sv_drmax = 1)),
        ]
    
    for name, src in vertex_srcs:
        for ana_name, ana in ana_qcuts:
            obj = ana.clone(vertex_src = src + suffix)
            setattr(process, 'play' + name + suffix + ana_name, obj)
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

    from JMTucker.Tools.CMSSWTools import file_event_from_argv
    file_event_from_argv(process)

no_scatterplots()

#process.add_(cms.Service('SimpleMemoryCheck'))
#print len(all_anas)
#for a in all_anas[2:]:
#    process.p.remove(a)

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    assert all_anas[0].is_mfv # de_mfv will be called for non-signal samples below

    if 'debug' in sys.argv:
        raise RuntimeError('refusing to submit jobs in debug (verbose print out) mode')

    crab_cfg = '''
[CRAB]
jobtype = cmssw
scheduler = %(scheduler)s 

[CMSSW]
%(dbs_url)s
datasetpath = %(dataset)s
pset = play_crab.py
total_number_of_events = 100000
events_per_job = 2000

[USER]
ui_working_dir = crab/VertexRecoPlay/crab_mfv_vtxplay_%(name)s
jmt_skip_input_files = src/EGamma/EGammaAnalysisTools/data/*
return_data = 1
'''

    testing = 'testing' in sys.argv
    from JMTucker.Tools.Samples import mfv_neutralino_tau0000um_M0400, mfv_neutralino_tau1000um_M0400, mfv_neutralino_tau9900um_M0400, ttbarincl, qcdht0100, qcdht0250, qcdht0500, qcdht1000
    samples = [mfv_neutralino_tau0000um_M0400, mfv_neutralino_tau1000um_M0400, mfv_neutralino_tau9900um_M0400, ttbarincl, qcdht0100, qcdht0250, qcdht0500, qcdht1000]

    for sample in samples:
        sample.scheduler_name = 'glite' if 'mfv' in sample.name else 'condor'
        open('crab.cfg', 'wt').write(crab_cfg % sample)
        new_py = open('play.py').read()
        if 'mfv' not in sample.name:
            new_py += '\nde_mfv()\n'
        if 'ttbar' in sample.name:
            new_py += '\nsample_ttbar()\n'
        open('play_crab.py', 'wt').write(new_py)
        if not testing:
            os.system('crab -create -submit')
            os.system('rm crab.cfg play_crab.py play_crab.pyc')
