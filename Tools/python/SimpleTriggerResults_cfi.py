import sys, FWCore.ParameterSet.Config as cms

SimpleTriggerResults = cms.EDAnalyzer('SimpleTriggerResults',
                                      trigger_results_src = cms.InputTag('TriggerResults', '', 'HLT'),
                                      deversion = cms.bool(True)
                                      )
