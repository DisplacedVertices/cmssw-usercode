import sys
from JMTucker.Tools.BasicAnalyzer_cfg import cms, process
from JMTucker.Tools import SampleFiles

process.TFileService.fileName = 'minbias_histos.root'
#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(20) )

process.source.fileNames = ['file:root://xrootd.unl.edu//store/mc/Summer12/MinBias_TuneZ2star_8TeV-pythia6/GEN-SIM/START50_V13-v3/0000/0005E496-3661-E111-B31E-003048F0E426.root']

process.minbiasHistos = cms.EDAnalyzer('MinBiasHistos',
                                    jet_src = cms.InputTag('ak4GenJets'),
                                    btag_src = cms.InputTag('combinedSecondaryVertexBjetTags'),
                                    gen_particle_src = cms.InputTag('genParticles'),
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
