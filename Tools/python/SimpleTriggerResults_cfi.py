import sys, FWCore.ParameterSet.Config as cms

SimpleTriggerResults = cms.EDAnalyzer('SimpleTriggerResults',
                                      trigger_results_src = cms.InputTag('TriggerResults', '', 'HLT'),
                                      weight_src = cms.InputTag(''),
                                      deversion = cms.bool(True)
                                      )

def setup_endpath(process, weight_src = ''):
    process.SimpleTriggerResults = SimpleTriggerResults.clone(weight_src = weight_src)
    process.SimpleTriggerResults.trigger_results_src = cms.InputTag('TriggerResults', '', process.name_())
    if type(weight_src) == cms.InputTag:
        weight_src = weight_src.moduleLabel
    weight_obj = getattr(process, weight_src)
    process.epSimpleTriggerResults = cms.EndPath(weight_obj * process.SimpleTriggerResults)
