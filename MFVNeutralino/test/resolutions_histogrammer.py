import os, sys, FWCore.ParameterSet.Config as cms

process = cms.Process('ResolutionsHistogrammer')
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1))
process.source = cms.Source('PoolSource', fileNames = cms.untracked.vstring('/store/user/tucker/mfvneutralino_genfsimreco_tau10um/sstoptuple_v3_mfvN3jtau10um/ffbc82b68f588f5f183a150670744b16/pat_1_1_6Sq.root'))
process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(False))
process.TFileService = cms.Service('TFileService', fileName = cms.string('mfv_resolutions_histos.root'))
process.load('FWCore.MessageLogger.MessageLogger_cfi')
process.MessageLogger.cerr.FwkReport.reportEvery = 100000

from HLTrigger.HLTfilters.hltHighLevel_cfi import hltHighLevel
process.goodDataFilter = hltHighLevel.clone()
process.goodDataFilter.TriggerResultsTag = cms.InputTag('TriggerResults', '', 'PAT')
process.goodDataFilter.HLTPaths = ['eventCleaningAll'] # can set to just 'goodOfflinePrimaryVertices', for example
process.goodDataFilter.andOr = False # = AND

process.triggerFilter = hltHighLevel.clone()
process.triggerFilter.HLTPaths = ['HLT_IsoMu17_eta2p1_TriCentralPFNoPUJet30_v*']

import JMTucker.Tools.PATTupleSelection_cfi
selection = JMTucker.Tools.PATTupleSelection_cfi.jtupleParams

bdiscs = [
    ('combinedSecondaryVertexBJetTags',      (0.244, 0.679, 0.898)),
    ('jetProbabilityBJetTags',               (0.275, 0.545, 0.790)),
    ('jetBProbabilityBJetTags',              (1.33, 2.55, 3.74)),
    ('simpleSecondaryVertexHighEffBJetTags', (1.74, 3.05)),
    ('simpleSecondaryVertexHighPurBJetTags', (2., 2.)),
    ('trackCountingHighEffBJetTags',         (1.7, 3.3, 10.2)),
    ('trackCountingHighPurBJetTags',         (1.19, 1.93, 3.41)),
    ]
    
process.histos = cms.EDAnalyzer('MFVNeutralinoResolutionsHistogrammer',
                                reweight_pileup = cms.bool(True),
                                force_weight = cms.double(-1),
                                vertex_src = cms.InputTag('goodOfflinePrimaryVertices'),
                                met_src = cms.InputTag('patMETsPF'),
                                jet_src = cms.InputTag('selectedPatJetsPF'),
                                b_discriminators = cms.vstring(*[name for name, discs in bdiscs]),
                                b_discriminator_mins = cms.vdouble(*[discs[1] for name, discs in bdiscs]),
                                muon_src = cms.InputTag('selectedPatMuonsPF'),
                                max_muon_dxy = cms.double(0.2),
                                max_muon_dz = cms.double(0.5),
                                muon_semilep_cut = selection.semilepMuonCut,
                                muon_dilep_cut = selection.dilepMuonCut,
                                electron_src = cms.InputTag('selectedPatElectronsPF'),
                                max_semilep_electron_dxy = cms.double(0.02),
                                max_dilep_electron_dxy = cms.double(0.04),
                                electron_semilep_cut = selection.semilepElectronCut,
                                electron_dilep_cut = selection.dilepElectronCut,
                                print_info = cms.bool(False),
                                )

process.p = cms.Path(process.goodDataFilter * process.triggerFilter * process.histos)

if 'debug' in sys.argv:
    process.MessageLogger.cerr.FwkReport.reportEvery = 1
    process.histos.print_info = True
    process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
    process.printList = cms.EDAnalyzer('ParticleListDrawer',
                                       maxEventsToPrint = cms.untracked.int32(100),
                                       src = cms.InputTag('genParticles'),
                                       printOnlyHardInteraction = cms.untracked.bool(False),
                                       useMessageLogger = cms.untracked.bool(False)
                                       )
    process.p *= process.printList

def run_on_data():
    if 'debug' in sys.argv:
        process.p.remove(process.printList)

#run_on_data()

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    raise 'no'
