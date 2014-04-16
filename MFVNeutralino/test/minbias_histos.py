import sys
from JMTucker.Tools.BasicAnalyzer_cfg import cms, process
from JMTucker.Tools import SampleFiles

process.TFileService.fileName = 'minbias_histos.root'
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(20) )

process.minbiasHistos = cms.EDAnalyzer('MinBiasHistos',
                                    jet_src = cms.InputTag('ak5GenJets'),
                                    btag_src = cms.InputTag('combinedSecondaryVertexBjetTags'),
                                    jet_pt_min = cms.double(20),
                                    bdisc_min = cms.double(0.679),
                                    )


process.p = cms.Path(process.minbiasHistos)

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.Samples import TupleOnlyMCSample
    from JMTucker.Tools.CRABSubmitter import CRABSubmitter

    blah = TupleOnlyMCSample('MinBias','/MinBias_TuneZ2star_8TeV-pythia6/Summer12-START50_V13-v3/GEN-SIM',500000)
    
    cs = CRABSubmitter('MinBiasHistosV1',
                       job_control_from_sample = True,                       
                       )
    cs.submit_all([blah])
