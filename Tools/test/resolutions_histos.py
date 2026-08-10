import os, sys
from JMTucker.Tools.BasicAnalyzer_cfg import *
from JMTucker.Tools.PATTupleSelection_cfi import jtupleParams

input_files(process, '/store/mc/RunIIFall17MiniAOD/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/MINIAODSIM/94X_mc2017_realistic_v10-v1/20000/32C049AF-E201-E811-AA77-34E6D7BEAF01.root')
max_events(process, 100)
tfileservice(process, 'resolutions_histos.root')

process.load('JMTucker.Tools.MCStatProducer_cff')
process.load('CommonTools.ParticleFlow.goodOfflinePrimaryVertices_cfi')
process.load('HLTrigger.HLTfilters.hltHighLevel_cfi')

process.load('PhysicsTools.PatAlgos.selectionLayer1.jetSelector_cfi')

process.goodOfflinePrimaryVertices.src = 'offlineSlimmedPrimaryVertices'
process.hltHighLevel.HLTPaths = ['HLT_IsoMu27_v*', 'HLT_Ele35_WPTight_Gsf_v*']

process.histos = cms.EDAnalyzer('ResolutionsHistogrammer',
                                vertex_src = cms.InputTag('goodOfflinePrimaryVertices'),
                                jets_src = cms.InputTag('slimmedJets'),
                                muons_src = cms.InputTag('slimmedMuons'),
                                electrons_src = cms.InputTag('slimmedElectrons'),
                                met_src = cms.InputTag('patMETsNoHF'),
                                jet_cut = jtupleParams.jetCut,
                                muon_cut = jtupleParams.muonCut,
                                electron_cut = jtupleParams.electronCut,
                                b_discriminators = cms.vstring('pfCombinedInclusiveSecondaryVertexV2BJetTags', 'pfCombinedInclusiveSecondaryVertexV2BJetTags', 'pfCombinedInclusiveSecondaryVertexV2BJetTags'),
                                b_discriminator_mins = cms.vdouble(0.46, 0.8, 0.935),
                                max_muon_dxy = cms.double(1e99),
                                max_muon_dz = cms.double(1e99),
                                max_electron_dxy = cms.double(1e99),
                                max_electron_dz = cms.double(1e99),
                                )

process.histosWithTrigger = process.histos.clone()

process.p0 = cms.Path(                       process.goodOfflinePrimaryVertices * process.histos)
process.p1 = cms.Path(process.hltHighLevel * process.goodOfflinePrimaryVertices * process.histosWithTrigger)
