import FWCore.ParameterSet.Config as cms

mfvAbcdHistosTrks = cms.EDAnalyzer('ABCDHistos',
                                   mfv_event_src = cms.InputTag('mfvEvent'),
                                   weight_src = cms.InputTag('mfvWeight'),
                                   vertex_src = cms.InputTag('mfvSelectedVerticesTight'),
                                   which_mom = cms.int32(0),
                                   )

mfvAbcdHistosJets = mfvAbcdHistosTrks.clone(which_mom = 1)
mfvAbcdHistosTrksJets = mfvAbcdHistosTrks.clone(which_mom = 2)

mfvAbcdHistosSeq = cms.Sequence(mfvAbcdHistosTrks * mfvAbcdHistosJets * mfvAbcdHistosTrksJets)
