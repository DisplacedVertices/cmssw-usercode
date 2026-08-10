import FWCore.ParameterSet.Config as cms

mfvByX = cms.EDAnalyzer('MFVByX',
                        event_src = cms.InputTag('mfvEvent'),
                        vertex_src = cms.InputTag(''),
                        by_run = cms.bool(False),
                        by_npu = cms.bool(False),
                        )

mfvByRun = mfvByX.clone(by_run = True)
mfvByNpu = mfvByX.clone(by_npu = True)

