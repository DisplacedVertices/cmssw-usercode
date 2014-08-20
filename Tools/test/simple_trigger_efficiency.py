import sys, os
from JMTucker.Tools.BasicAnalyzer_cfg import cms, process

process.TFileService.fileName = 'simple_trigger_efficiency.root'

process.genMus = cms.EDFilter('CandViewSelector', src = cms.InputTag('genParticles'), cut = cms.string('abs(pdgId) == 13 && abs(mother.pdgId) == 24'))
process.genMuCount = cms.EDFilter('CandViewCountFilter', src = cms.InputTag('genMus'), minNumber = cms.uint32(1))
                                
process.genEls = cms.EDFilter('CandViewSelector', src = cms.InputTag('genParticles'), cut = cms.string('abs(pdgId) == 11 && abs(mother.pdgId) == 24'))
process.genElCount = cms.EDFilter('CandViewCountFilter', src = cms.InputTag('genEls'), minNumber = cms.uint32(1))
                                
process.genMusInAcc = cms.EDFilter('CandViewSelector', src = cms.InputTag('genParticles'), cut = cms.string('abs(pdgId) == 13 && abs(mother.pdgId) == 24 && pt > 26 && abs(eta) < 2.1'))
process.genElsInAcc = cms.EDFilter('CandViewSelector', src = cms.InputTag('genParticles'), cut = cms.string('abs(pdgId) == 11 && abs(mother.pdgId) == 24 && pt > 30 && abs(eta) < 2.5'))
process.genMuInAccCount = cms.EDFilter('CandViewCountFilter', src = cms.InputTag('genMusInAcc'), minNumber = cms.uint32(1))
process.genElInAccCount = cms.EDFilter('CandViewCountFilter', src = cms.InputTag('genElsInAcc'), minNumber = cms.uint32(1))

process.RandomNumberGeneratorService = cms.Service('RandomNumberGeneratorService')
process.RandomNumberGeneratorService.SimpleTriggerEfficiency = cms.PSet(initialSeed = cms.untracked.uint32(1219))
process.RandomNumberGeneratorService.SimpleTriggerEfficiencyMu = cms.PSet(initialSeed = cms.untracked.uint32(1220))
process.RandomNumberGeneratorService.SimpleTriggerEfficiencyMuInAcc = cms.PSet(initialSeed = cms.untracked.uint32(1221))

#import prescales
process.load('JMTucker.Tools.SimpleTriggerEfficiency_cfi')
process.SimpleTriggerEfficiency.prescale_paths  = cms.vstring()  #*prescales.prescales.keys()),
process.SimpleTriggerEfficiency.prescale_values = cms.vuint32()  #*[o for l,h,o in prescales.prescales.itervalues()]),

process.SimpleTriggerEfficiencyMu      = process.SimpleTriggerEfficiency.clone()
process.SimpleTriggerEfficiencyMuInAcc = process.SimpleTriggerEfficiency.clone()
process.SimpleTriggerEfficiencyEl      = process.SimpleTriggerEfficiency.clone()
process.SimpleTriggerEfficiencyElInAcc = process.SimpleTriggerEfficiency.clone()

process.p1 = cms.Path(process.SimpleTriggerEfficiency)
process.p2 = cms.Path(process.genMus      * process.genMuCount      * process.SimpleTriggerEfficiencyMu)
process.p3 = cms.Path(process.genMusInAcc * process.genMuInAccCount * process.SimpleTriggerEfficiencyMuInAcc)
process.p4 = cms.Path(process.genEls      * process.genElCount      * process.SimpleTriggerEfficiencyEl)
process.p5 = cms.Path(process.genElsInAcc * process.genElInAccCount * process.SimpleTriggerEfficiencyElInAcc)

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.Samples import mfv_signal_samples 
    from JMTucker.Tools.CRABSubmitter import CRABSubmitter

    cs = CRABSubmitter('SimpleTrigEff',
                       total_number_of_events = -1,
                       events_per_job = 200000,
                       )
    cs.submit_all(mfv_signal_samples)
