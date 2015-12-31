import FWCore.ParameterSet.Config as cms

emu = cms.EDFilter('MFVEmulateHT800',
                   trigger_results_src = cms.InputTag('TriggerResults', '', 'HLT'),
                   trigger_objects_src = cms.InputTag('selectedPatTrigger'),
                   throw_not_found = cms.bool(False),
                   return_actual = cms.bool(True),
                   return_ht900 = cms.bool(False),
                   prints = cms.untracked.bool(False),
                   histos = cms.untracked.bool(False),
                   )
