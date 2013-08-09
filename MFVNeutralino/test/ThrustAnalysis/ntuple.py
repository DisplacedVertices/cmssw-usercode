import sys, os
from JMTucker.Tools.BasicAnalyzer_cfg import cms, process
process.load('Configuration.Geometry.GeometryIdeal_cff')
process.load('Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.GlobalTag.globaltag = 'START53_V21::All'
process.load('TrackingTools.TransientTrack.TransientTrackBuilder_cfi')
process.load('CommonTools.ParticleFlow.goodOfflinePrimaryVertices_cfi')
process.goodOfflinePrimaryVertices.filter = cms.bool(False)

process.load('JMTucker.MFVNeutralino.Vertexer_cff')
process.MessageLogger.cerr.FwkReport.reportEvery = 1

process.TFileService.fileName = 'ass_thrust.root'
process.maxEvents.input = 100
process.options.SkipEvent = cms.untracked.vstring('ProductNotFound')

file = open('files.txt', 'r')
myfilelist = cms.untracked.vstring()
for line in file:
	string = "/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/"+line
    # add as many files as you wish this way
	myfilelist.extend( [string] )

process.source = cms.Source('PoolSource', fileNames = myfilelist)

process.thrustNtuple = cms.EDAnalyzer('MFVThrustAnalysis',
                                      gen_particles_src = cms.InputTag('genParticles'),
                                      gen_jets_src = cms.InputTag('ak5GenJets'),
                                      gen_met_src = cms.InputTag('genMetTrue'),
                                      met_src = cms.InputTag('patMETsPF'),
                                      jets_src = cms.InputTag('selectedPatJetsPF'),
                                      muon_src = cms.InputTag('selectedPatMuonsPF'),
                                      map_src = cms.InputTag('mfvVerticesToJets'),
                                      pt_cut = cms.double(30),
                                      eta_cut = cms.double(3),
                                      loose_pt_cut = cms.double(30), # 20
                                      loose_eta_cut = cms.double(3), # 3.5
                                      lepton_pt_cut = cms.double(30), # 20
                                      lepton_eta_cut = cms.double(2.1), # 3.5
                                      )

process.p = cms.Path(process.mfvVertexSequence*process.thrustNtuple)

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    crab_cfg = '''
[CRAB]
jobtype = cmssw
scheduler = %(scheduler)s

[CMSSW]
%(dbs_url)s
datasetpath = %(dataset)s
pset = ntuple.py
%(job_control)s

[USER]
ui_working_dir = crab/ThrustAnalysis/crab_ThAn_%(name)s
return_data = 1
additional_input_files = dict_C.so
jmt_skip_input_files = src/EGamma/EGammaAnalysisTools/data/*
'''

    os.system('mkdir -p crab/ThrustAnalysis')
    just_testing = 'testing' in sys.argv

    def submit(sample):
        open('crab.cfg', 'wt').write(crab_cfg % sample)
        if not just_testing:
            os.system('crab -create -submit')
            os.system('rm -f crab.cfg mfvgen_analyzer_crab.py mfvgen_analyzer_crab.pyc')

    from JMTucker.Tools.Samples import mfv_gluino_tau1000um_M0400, ttbarnocut
    mfv_gluino_tau1000um_M0400_old = {'dbs_url':'dbs_url = https://cmsdbsprod.cern.ch:8443/cms_dbs_ph_analysis_02_writer/servlet/DBSServlet','scheduler':'glite','name':'old_mfv3j_gluino_tau1000um_M0400', 'dataset':'/mfv_genfsimreco_gluino_tau1000um_M400/tucker-mfv_genfsimreco_gluino_tau1000um_M400-e47fc4979466aacf88f2c30cc52afb0f/USER', 'job_control': 'total_number_of_events = 10000\nevents_per_job=1000\n'}
    for sample in (mfv_gluino_tau1000um_M0400, mfv_gluino_tau1000um_M0400_old, ttbarnocut):
        submit(sample)
