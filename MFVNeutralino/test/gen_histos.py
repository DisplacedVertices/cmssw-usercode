import sys
from JMTucker.Tools.BasicAnalyzer_cfg import *
debug = 'debug' in sys.argv

sample_files(process, 'official_mfv_neu_tau10000um_M0800', 'main', 1)
process.TFileService.fileName = 'gen_histos.root'
file_event_from_argv(process)

process.load('JMTucker.MFVNeutralino.GenParticles_cff')
#process.load('JMTucker.MFVNeutralino.GenParticleFilter_cfi')
#process.mfvGenParticleFilter.required_num_leptonic = 0

process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.mfvGenHistos = cms.EDAnalyzer('MFVGenHistos',
                                      gen_src = cms.InputTag('genParticles'),
                                      gen_jet_src = cms.InputTag('ak4GenJets'),
                                      mci_src = cms.InputTag('mfvGenParticles'),
                                      )

#process.p = cms.Path(process.mfvGenParticles * process.mfvGenParticleFilter * process.mfvGenHistos)
process.p = cms.Path(process.mfvGenParticles * process.mfvGenHistos)

if debug:
    process.mfvGenParticles.debug = True

    process.printList = cms.EDAnalyzer('JMTParticleListDrawer',
                                       src = cms.InputTag('genParticles'),
                                       printVertex = cms.untracked.bool(True),
                                       )
    process.p.insert(0, process.printList)

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    
    from JMTucker.Tools.Sample import anon_samples

    samples = anon_samples('''
/mfv_neu_tau00100um_M0400/tucker-gen-30031245991cdc59a4e779a57f211d2a/USER
/mfv_neu_tau00100um_M0800/tucker-gen-30031245991cdc59a4e779a57f211d2a/USER
/mfv_neu_tau00100um_M1200/tucker-gen-30031245991cdc59a4e779a57f211d2a/USER
/mfv_neu_tau00100um_M1600/tucker-gen-30031245991cdc59a4e779a57f211d2a/USER
/mfv_neu_tau00300um_M0400/tucker-gen-297aaf8461e8651140243c6762af3145/USER
/mfv_neu_tau00300um_M0800/tucker-gen-297aaf8461e8651140243c6762af3145/USER
/mfv_neu_tau00300um_M1200/tucker-gen-297aaf8461e8651140243c6762af3145/USER
/mfv_neu_tau00300um_M1600/tucker-gen-297aaf8461e8651140243c6762af3145/USER
/mfv_neu_tau01000um_M0400/tucker-gen-80424ff51c64a4a42ab32d70ea13233c/USER
/mfv_neu_tau01000um_M0800/tucker-gen-80424ff51c64a4a42ab32d70ea13233c/USER
/mfv_neu_tau01000um_M1200/tucker-gen-80424ff51c64a4a42ab32d70ea13233c/USER
/mfv_neu_tau01000um_M1600/tucker-gen-80424ff51c64a4a42ab32d70ea13233c/USER
/mfv_neu_tau10000um_M0400/tucker-gen-d9ae25c69fb344d73087168fa6b951ad/USER
/mfv_neu_tau10000um_M0800/tucker-gen-d9ae25c69fb344d73087168fa6b951ad/USER
/mfv_neu_tau10000um_M1200/tucker-gen-d9ae25c69fb344d73087168fa6b951ad/USER
/mfv_neu_tau10000um_M1600/tucker-gen-d9ae25c69fb344d73087168fa6b951ad/USER
''', dbs_inst='phys03')

    from JMTucker.Tools.CRAB3Submitter import CRABSubmitter
    cs = CRABSubmitter('GenHistos',
                       splitting = 'EventAwareLumiBased',
                       units_per_job = 20000,
                       total_units = -1,
                       )
    cs.submit_all(samples)
