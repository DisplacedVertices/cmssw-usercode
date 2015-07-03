import sys
import FWCore.ParameterSet.Config as cms

process = cms.Process("PVAnalyzer")
process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.INFO = cms.untracked.PSet(limit = cms.untracked.int32(-1))
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1))
process.source = cms.Source("PoolSource",
                            fileNames = cms.untracked.vstring('file:/store/mc/Summer12_DR53X/QCD_HT-1000ToInf_TuneZ2star_8TeV-madgraph-pythia6/AODSIM/PU_S10_START53_V7A-v1/00000/16716FE6-440E-E211-A50B-0024E8767D86.root'))
process.Analyzer = cms.EDAnalyzer('PVAnalyzer',primary_vertices_src = cms.InputTag('offlinePrimaryVertices'),
                                  track_src = cms.InputTag('generalTracks'),
                                  beamspot_src = cms.InputTag('offlineBeamSpot'),
                                  use_only_pv_tracks = cms.bool(True),
                                  use_only_pvs_tracks = cms.bool(True),
                                  maxNormChi2 = cms.double(20.0),
                                  minPxLayer = cms.int32(2),
                                  minSilLayer = cms.int32(5)
                                  )
process.TFileService = cms.Service("TFileService", fileName = cms.string('PVAnalyzer_histo.root'))
process.p = cms.Path(process.Analyzer)

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    import JMTucker.Tools.Samples as Samples
    samples = Samples.from_argv([Samples.qcdht1000, Samples.mfv_neutralino_tau1000um_M0400, Samples.mfv_neutralino_tau0100um_M0400])

    from JMTucker.Tools.CRABSubmitter import CRABSubmitter
    cs = CRABSubmitter('PVAnalyzer',
                       total_number_of_events = -1,
                       events_per_job = 100000,
                       )
    cs.submit_all(samples)
