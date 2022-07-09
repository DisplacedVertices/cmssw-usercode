import FWCore.ParameterSet.Config as cms

SimpleTriggerEfficiency = cms.EDAnalyzer('SimpleTriggerEfficiency',
                                         trigger_results_src = cms.InputTag('TriggerResults', '', 'HLT'),
                                         weight_src = cms.InputTag(''),
                                         parse_randpars = cms.bool(False), 
                                         randpar_mass = cms.int32(-1),
                                         randpar_ctau = cms.string(''),
                                         randpar_dcay = cms.string(''),
                                         )

def setup_endpath(process, rp_mode, weight_src = ''):

    if rp_mode :
        rp_mass = (int)(rp_mode[rp_mode.find('M')+1 : rp_mode.find('_')])
        rp_ctau = rp_mode[rp_mode.find('t')+1 : rp_mode.find('-')]
        rp_dcay = rp_mode[rp_mode.find('H') : rp_mode.find(' M')]
        parse_randpars = True
           
        process.SimpleTriggerEfficiency = SimpleTriggerEfficiency.clone(weight_src = weight_src, parse_randpars = parse_randpars, randpar_mass = rp_mass, randpar_ctau = rp_ctau, randpar_dcay = rp_dcay)
    else :
        process.SimpleTriggerEfficiency = SimpleTriggerEfficiency.clone(weight_src = weight_src)
    
    process.SimpleTriggerEfficiency.trigger_results_src = cms.InputTag('TriggerResults', '', process.name_())
    process.RandomNumberGeneratorService = cms.Service('RandomNumberGeneratorService')
    process.RandomNumberGeneratorService.SimpleTriggerEfficiency = cms.PSet(initialSeed = cms.untracked.uint32(1220))
    if type(weight_src) == cms.InputTag:
        weight_src = weight_src.moduleLabel
    if weight_src:
        weight_obj = getattr(process, weight_src)
        process.epSimpleTriggerEfficiency = cms.EndPath(weight_obj * process.SimpleTriggerEfficiency)
    else:
        process.epSimpleTriggerEfficiency = cms.EndPath(process.SimpleTriggerEfficiency)
