import FWCore.ParameterSet.Config as cms
from JMTucker.Tools.PATTupleSelection_cfi import jtupleParams

mfvEventFilter = cms.EDFilter('MFVEventFilter',
                              mode = cms.string('either'),
                              jets_src = cms.InputTag('selectedPatJets'),
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
                              parse_randpars = cms.bool(False), 
                              randpar_mass = cms.int32(-1),
                              randpar_ctau = cms.string(''),
                              randpar_dcay = cms.string(''),
                              debug = cms.untracked.bool(False),
                              )

mfvEventFilterJetsOnly = mfvEventFilter.clone(mode = 'jets only')
mfvEventFilterLeptonsOnly = mfvEventFilter.clone(mode = 'leptons only')
mfvEventFilterHTORBjetsORDisplacedDijet = mfvEventFilter.clone(mode = 'HT OR bjets OR displaced dijet', min_ht = cms.double(-1))
mfvEventFilterBjetsORDisplacedDijetVetoHT = mfvEventFilter.clone(mode = 'bjets OR displaced dijet veto HT', min_ht = cms.double(-1))
mfvEventFilterRandomParameters = mfvEventFilter.clone(min_pt_for_ht = cms.double(-1), min_ht = cms.double(-1), min_njets = cms.int32(0),
                                                      min_electron_pt = cms.double(-1), min_muon_pt = cms.double(-1), min_nleptons = cms.int32(0))
