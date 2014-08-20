import FWCore.ParameterSet.Config as cms

SimpleTriggerEfficiency = cms.EDAnalyzer('SimpleTriggerEfficiency',
                                         trigger_results_src = cms.InputTag('TriggerResults', '', 'HLT'),
                                         weight_src = cms.InputTag(''),
                                         )

def setup_endpath(process, weight_src = ''):
    process.SimpleTriggerEfficiency = SimpleTriggerEfficiency.clone(weight_src = weight_src)
    process.SimpleTriggerEfficiency.trigger_results_src = cms.InputTag('TriggerResults', '', process.name_())
    if type(weight_src) == cms.InputTag:
        weight_src = weight_src.moduleLabel
    weight_obj = getattr(process, weight_src)
    process.epSimpleTriggerEfficiency = cms.EndPath(weight_obj * process.SimpleTriggerEfficiency)
