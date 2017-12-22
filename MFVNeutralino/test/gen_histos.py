import sys
from JMTucker.Tools.BasicAnalyzer_cfg import *
debug = 'debug' in sys.argv

sample_files(process, 'mfv_neuudmu_tau10000um_M1200', 'main', 1)
process.TFileService.fileName = 'gen_histos.root'
file_event_from_argv(process)

process.load('JMTucker.MFVNeutralino.GenParticles_cff')
#process.load('JMTucker.MFVNeutralino.GenParticleFilter_cfi')
#process.mfvGenParticleFilter.required_num_leptonic = 0

process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.mfvGenHistos = cms.EDAnalyzer('MFVGenHistos',
                                      gen_src = cms.InputTag('genParticles'),
                                      gen_jet_src = cms.InputTag('ak4GenJetsNoNu'),
                                      gen_vertex_src = cms.InputTag('mfvGenParticles', 'genVertex'),
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
    pass
