import FWCore.ParameterSet.Config as cms

from JMTucker.Tools.L1GtUtils_cff import l1GtUtilsTags

emu = cms.EDFilter('MFVEmulateHT800',
                   l1GtUtilsTags,
                   trigger_results_src = cms.InputTag('TriggerResults', '', 'HLT'),
                   trigger_objects_src = cms.InputTag('selectedPatTrigger'),
                   throw_not_found = cms.bool(False),
                   return_actual = cms.bool(True),
                   return_ht900 = cms.bool(True),
                   prints = cms.untracked.bool(False),
                   histos = cms.untracked.bool(False),
                   )
