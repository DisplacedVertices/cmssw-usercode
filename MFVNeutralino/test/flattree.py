import sys
from JMTucker.Tools.BasicAnalyzer_cfg import *

process.options.emptyRunLumiMode = cms.untracked.string('doNotHandleEmptyRunsAndLumis')
process.source.fileNames = ['/store/user/tucker/QCD_HT-1000ToInf_TuneZ2star_8TeV-madgraph-pythia6/mfvntuple_v18/c761ddfa7f093d8f86a338439e06a1d4/ntuple_1_1_URD.root']
process.source.noEventSort = cms.untracked.bool(True)
process.source.duplicateCheckMode = cms.untracked.string('noDuplicateCheck')
process.TFileService.fileName = 'flattree.root'

process.mfvFlatTree = cms.EDAnalyzer('MFVFlatTreer',
                                     event_src = cms.InputTag('mfvEvent'),
                                     vertex_src = cms.InputTag('mfvVerticesAux'),
                                     sample = cms.int32(0),
                                     )

process.p = cms.Path(process.mfvFlatTree)
        
if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    import JMTucker.Tools.Samples as Samples
    samples = [Samples.mfv_neutralino_tau0100um_M0400,
               Samples.mfv_neutralino_tau1000um_M0400,
               Samples.mfv_neutralino_tau0300um_M0400,
               Samples.mfv_neutralino_tau9900um_M0400] + Samples.ttbar_samples + Samples.qcd_samples

    def modify(sample):
        ndx = samples.index(sample)
        id = ndx - 3
        to_add = ['process.mfvFlatTree.sample = %i' % id]
        return to_add, []

    from JMTucker.Tools.CRABSubmitter import CRABSubmitter
    cs = CRABSubmitter('FlatTreeV18',
                       pset_modifier = modify,
                       get_edm_output = True,
                       data_retrieval = 'fnal',
                       job_control_from_sample = True,
                       use_ana_dataset = True,
                       run_half_mc = True,
                       )
    cs.submit_all(samples)
