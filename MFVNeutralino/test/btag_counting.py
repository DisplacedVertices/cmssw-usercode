import os, sys, FWCore.ParameterSet.Config as cms

process = cms.Process('MFVNeutralino')
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1))
process.source = cms.Source('PoolSource', fileNames = cms.untracked.vstring('/store/user/tucker/mfv_gensimhlt_gluino_tau1000um_M0400/jtuple_v6_mfv_gluino_tau1000um_M0400/bd05e25367130164ec2dd1b6bce4cd3c/pat_1_1_cQg.root'))
process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(False))
process.TFileService = cms.Service('TFileService', fileName = cms.string('btag_counting.root'))
process.load('FWCore.MessageLogger.MessageLogger_cfi')
process.MessageLogger.cerr.FwkReport.reportEvery = 10000

debug = 'debug' in sys.argv

process.btagCounting = cms.EDAnalyzer('MFVNeutralinoPATBTagCounting',
                                      vertex_src = cms.InputTag('goodOfflinePrimaryVertices'),
                                      jet_src = cms.InputTag('selectedPatJetsPF'),
                                      b_discriminator_name = cms.string('jetBProbabilityBJetTags'),
                                      jet_pt_min = cms.double(30),
                                      bdisc_min = cms.double(2.55),
                                      muon_src = cms.InputTag('selectedPatMuonsPF'),
                                      electron_src = cms.InputTag('selectedPatElectronsPF'),
                                      verbose = cms.bool(debug),
                                      )

process.p = cms.Path(process.btagCounting)
    
if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    if 'debug' in sys.argv:
        raise RuntimeError('refusing to submit jobs in debug (verbose print out) mode')

    crab_cfg = '''
[CRAB]
jobtype = cmssw
scheduler = condor

[CMSSW]
%(ana_dbs_url)s
datasetpath = %(ana_dataset)s
pset = btag_counting.py
total_number_of_events = -1
events_per_job = 100000

[USER]
ui_working_dir = crab/btag_counting/crab_mfv_btag_counting_%(name)s
return_data = 1
'''

    os.system('mkdir -p crab/btag_counting')
    
    testing = 'testing' in sys.argv

    from JMTucker.Tools.Samples import mfv_signal_samples
    for sample in mfv_signal_samples:
        open('crab.cfg', 'wt').write(crab_cfg % sample)
        if not testing:
            os.system('crab -create -submit')
            os.system('rm crab.cfg')
