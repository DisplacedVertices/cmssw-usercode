import os, sys
from JMTucker.Tools.BasicAnalyzer_cfg import cms, process
from JMTucker.Tools.CMSSWTools import silence_messages

#process.MessageLogger.cerr.FwkReport.reportEvery = 1
process.maxEvents.input = 100
process.options.wantSummary = True
process.source.fileNames = ['/store/user/tucker/mfv_gensimhlt_gluino_tau9900um_M0400/reco/a3f0d9ac5e396df027589da2067010b0/reco_1_1_ohS.root']
process.TFileService.fileName = 'play.root'
silence_messages(process, 'TwoTrackMinimumDistance')

process.load('Configuration.Geometry.GeometryIdeal_cff')
process.load('Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.GlobalTag.globaltag = 'START53_V21::All'
process.load('TrackingTools.TransientTrack.TransientTrackBuilder_cfi')

process.load('JMTucker.MFVNeutralino.GenParticleFilter_cfi')
process.mfvGenParticleFilter.min_rho0 = 0.02 # 200 um
process.mfvGenParticleFilter.min_rho1 = 0.02

process.load('JMTucker.MFVNeutralino.VertexReco_cff')

#process.p = cms.Path(process.mfvGenParticleFilter * process.mfvVertexReco)
process.p = cms.Path(process.mfvVertexReco)

all_anas = []

for suffix in ('', 'Cos75'):
    vertex_srcs = [
        ('IVF', 'mfvInclusiveVertexFinder'),
        ('IVFMrgd', 'mfvVertexMerger'),
#        ('IVFMrgdArbd', 'mfvTrackVertexArbitrator'),
#        ('IVFMrgdArbdMrgd', 'mfvInclusiveMergedVertices'),
#        ('IVFMrgdArbdMrgdFltd', 'mfvInclusiveMergedVerticesFiltered'),
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
                         do_scatterplots = cms.bool(True),
                         jet_pt_min = cms.double(30),
                         track_pt_min = cms.double(10),
                         min_sv_ntracks = cms.int32(0),
                         max_sv_chi2dof = cms.double(1e6),
                         max_sv_err2d   = cms.double(1e6),
                         )

    ana_qcuts = [
        ('Qno',             ana),
        ('Qntk5',           ana.clone(min_sv_ntracks = 5)),
        ('Qntk5err2d0p015', ana.clone(min_sv_ntracks = 5, max_sv_err2d = 0.015)),
        ]
    
    for name, src in vertex_srcs:
        for ana_name, ana in ana_qcuts:
            obj = ana.clone(vertex_src = src + suffix)
            setattr(process, 'play' + name + suffix + ana_name, obj)
            all_anas.append(obj)
            process.p *= obj

def de_mfv():
    process.mfvGenParticleFilter.cut_invalid = False
    for ana in all_anas:
        ana.is_mfv = False

if 'test_ttbar' in sys.argv:
    process.source.fileNames = ['/store/mc/Summer12_DR53X/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/C6577DA8-32E2-E111-AC51-0030487E55BB.root']
    de_mfv()

if 'debug' in sys.argv:
    process.source.fileNames = ['/store/user/tucker/mfv_gensimhlt_gluino_tau1000um_M0400/reco/a3f0d9ac5e396df027589da2067010b0/reco_28_1_VIC.root']
    from JMTucker.Tools.CMSSWTools import set_events_to_process
    set_events_to_process(process, [(1,112,1)])

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    assert all_anas[0].is_mfv # de_mfv will be called for non-signal samples below

    if 'debug' in sys.argv:
        raise RuntimeError('refusing to submit jobs in debug (verbose print out) mode')

    crab_cfg = '''
[CRAB]
jobtype = cmssw
scheduler = condor

[CMSSW]
%(dbs_url)s
datasetpath = %(dataset)s
pset = play_crab.py
total_number_of_events = 6000
events_per_job = 1000

[USER]
ui_working_dir = crab/VertexRecoPlay/crab_mfv_vtxplay_%(name)s
jmt_skip_input_files = src/EGamma/EGammaAnalysisTools/data/*
return_data = 1
'''

    testing = 'testing' in sys.argv
    from JMTucker.Tools.Samples import mfv_gluino_tau0000um_M0400, mfv_gluino_tau1000um_M0400, mfv_gluino_tau9900um_M0400, ttbarnocut, TupleOnlyMCSample
    samples = [mfv_gluino_tau0000um_M0400, mfv_gluino_tau1000um_M0400, mfv_gluino_tau9900um_M0400, ttbarnocut]

    nu = TupleOnlyMCSample('mfv_neutralino_tau1000um_M0400_test', '/mfv_gensimhlt_neutralino_tau1000um_M0400/tucker-recotest-a3f0d9ac5e396df027589da2067010b0/USER')
    nu.dbs_url_num = 2
    samples.append(nu)

    for sample in samples:
        open('crab.cfg', 'wt').write(crab_cfg % sample)
        new_py = open('play.py').read()
        if 'ttbar' in sample.name:
            new_py += '\nde_mfv()\n'
        open('play_crab.py', 'wt').write(new_py)
        if not testing:
            os.system('crab -create -submit')
            os.system('rm crab.cfg play_crab.py play_crab.pyc')
