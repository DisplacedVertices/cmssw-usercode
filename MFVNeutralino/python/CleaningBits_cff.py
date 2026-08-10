import FWCore.ParameterSet.Config as cms

mfvCleaningBits = cms.EDProducer('MFVCleaningBits',
                                 cleaning_results_src = cms.InputTag('TriggerResults', '', 'PAT')
                                 )

pmfvCleaningBits = cms.EndPath(mfvCleaningBits)
