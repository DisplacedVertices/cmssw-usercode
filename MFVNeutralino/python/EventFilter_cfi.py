import FWCore.ParameterSet.Config as cms
from JMTucker.Tools.PATTupleSelection_cfi import jtupleParams

mfvEventFilter = cms.EDFilter('MFVEventFilter',
                              mode = cms.string('either'),
                              jets_src = cms.InputTag('selectedPatJets'),
                              trigger_results_src = cms.InputTag('TriggerResults', '', 'HLT'),
                              jet_cut = jtupleParams.jetCut,
                              min_njets = cms.int32(4),
                              min_pt_for_ht = cms.double(40),
                              min_ht = cms.double(1200),
                              muons_src = cms.InputTag('selectedPatMuons'),
                              muon_cut = jtupleParams.muonCut,
                              min_muon_pt = cms.double(27),
                              electrons_src = cms.InputTag('selectedPatElectrons'),
                              electron_cut = jtupleParams.electronCut,
                              min_electron_pt = cms.double(35),
                              min_nleptons = cms.int32(1),
                              veto_bjet_triggers = cms.bool(False),
                              triggers_to_veto = cms.vstring('HLT_DoublePFJets100MaxDeta1p6_DoubleCaloBTagCSV_p33_v',
                                                             'HLT_PFHT300PT30_QuadPFJet_75_60_45_40_TriplePFBTagCSV_3p0_v'),
                                                             #'HLT_DoublePFJets116MaxDeta1p6_DoubleCaloBTagDeepCSV_p71_v',
                                                             #'HLT_PFHT330PT30_QuadPFJet_75_60_45_40_TriplePFBTagDeepCSV_4p5_v',
                                                             #'HLT_QuadJet45_TripleBTagCSV_p087_v',
                                                             #'HLT_DoubleJet90_Double30_TripleBTagCSV_p087_v',
                                                             #'HLT_DoubleJetsC100_DoubleBTagCSV_p014_DoublePFJetsC100MaxDeta1p6_v'),
                              debug = cms.untracked.bool(False),
                              )

mfvEventFilterJetsOnly = mfvEventFilter.clone(mode = 'jets only')
mfvEventFilterLowHT = mfvEventFilter.clone(mode = 'low HT', min_ht = cms.double(450.0), min_njets = cms.int32(2))
mfvEventFilterLeptonsOnly = mfvEventFilter.clone(mode = 'leptons only', min_electron_pt = cms.double(999), min_muon_pt = cms.double(27))
mfvEventFilterDileptonOnly = mfvEventFilter.clone(mode = 'dilepton only', min_electron_pt = cms.double(20), min_muon_pt = cms.double(20), min_nleptons = cms.int32(2))
mfvEventFilterHTORBjetsORDisplacedDijet = mfvEventFilter.clone(mode = 'HT OR bjets OR displaced dijet', min_ht = cms.double(-1))
mfvEventFilterBjetsORDisplacedDijet = mfvEventFilter.clone(mode = 'bjets OR displaced dijet', min_ht = cms.double(-1))
mfvEventFilterBjetsORDisplacedDijetVetoHT = mfvEventFilter.clone(mode = 'bjets OR displaced dijet veto HT', min_ht = cms.double(-1))
mfvEventFilterDisplacedDijetVetoBjets = mfvEventFilter.clone(mode = 'bjets OR displaced dijet veto HT', min_ht = cms.double(200), min_nleptons = cms.int32(0), veto_bjet_triggers = cms.bool(True))
