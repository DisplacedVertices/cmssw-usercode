import sys
from JMTucker.Tools.BasicAnalyzer_cfg import cms, process

process.TFileService.fileName = 'gen_dphi.root'
process.source.fileNames = ['/store/user/tucker/TTJets_HadronicMGDecays_8TeV-madgraph/mfvntuple_v18/c761ddfa7f093d8f86a338439e06a1d4/ntuple_100_1_NHs.root']
process.source.secondaryFileNames = cms.untracked.vstring(*'''/store/mc/Summer12_DR53X/TTJets_HadronicMGDecays_8TeV-madgraph/AODSIM/PU_S10_START53_V7A-v1/00000/0E9DCF01-0216-E211-934F-20CF3019DF0F.root
/store/mc/Summer12_DR53X/TTJets_HadronicMGDecays_8TeV-madgraph/AODSIM/PU_S10_START53_V7A-v1/00000/E0F2FA59-1016-E211-A573-00259073E3A8.root
/store/mc/Summer12_DR53X/TTJets_HadronicMGDecays_8TeV-madgraph/AODSIM/PU_S10_START53_V7A-v1/00000/5205EEA5-1016-E211-BBE1-90E6BA442F2B.root'''.split('\n'))

process.load('JMTucker.MFVNeutralino.VertexSelector_cfi')
process.load('JMTucker.MFVNeutralino.AnalysisCuts_cfi')
process.mfvAnalysisCutsOneVtx = process.mfvAnalysisCuts.clone(min_nvertex = 1)

process.GenParticleDphiOneVtx = cms.EDAnalyzer('MFVGenParticleDphi',
                                               gen_particles_src = cms.InputTag('genParticles'),
                                               mevent_src = cms.InputTag('mfvEvent'),
                                               vertices_src = cms.InputTag('mfvSelectedVerticesTight'),
                                               )
process.GenParticleDphiTwoVtx = process.GenParticleDphiOneVtx.clone()

process.p = cms.Path(process.mfvSelectedVerticesSeq * process.mfvAnalysisCutsOneVtx * process.GenParticleDphiOneVtx * process.mfvAnalysisCuts * process.GenParticleDphiTwoVtx)


if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    import JMTucker.Tools.Samples as Samples
    samples = Samples.from_argv(Samples.ttbar_samples + Samples.qcd_samples)

    from JMTucker.Tools.CRABSubmitter import CRABSubmitter
    cs = CRABSubmitter('GenDphi',
                       job_control_from_sample = True,
                       use_ana_dataset = True,
                       use_parent = True,
                       run_half_mc = True,
                       )
    cs.submit_all(samples)
