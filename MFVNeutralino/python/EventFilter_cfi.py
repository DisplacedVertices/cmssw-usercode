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
                              min_muon_pt = cms.double(29),
                              electrons_src = cms.InputTag('selectedPatElectrons'),
                              electron_cut = jtupleParams.electronCut,
                              min_electron_pt = cms.double(38),
                              min_nleptons = cms.int32(1),
                              rho_src = cms.InputTag('fixedGridRhoFastjetAll'),
                              electron_effective_areas = cms.FileInPath('RecoEgamma/ElectronIdentification/data/Fall17/effAreaElectrons_cone03_pfNeuHadronsAndPhotons_92X.txt'),
                              parse_randpars = cms.bool(False), 
                              randpar_mass = cms.int32(-1),
                              randpar_ctau = cms.string(''),
                              randpar_dcay = cms.string(''),
                              debug = cms.untracked.bool(False),
                              )

mfvEventFilterJetsOnly = mfvEventFilter.clone(mode = 'jets only')
mfvEventFilterMuonsOnly = mfvEventFilter.clone(mode = 'muons only', min_ht = cms.double(-1), min_njets = cms.int32(2), min_pt_for_ht = cms.double(-1))
mfvEventFilterElectronsOnly = mfvEventFilter.clone(mode = 'electrons only', min_ht = cms.double(-1), min_njets = cms.int32(2), min_pt_for_ht = cms.double(-1))
#mfvEventFilterLeptonsOnly = mfvEventFilter.clone(mode = 'leptons only', min_ht = cms.double(-1), min_pt_for_ht = cms.double(-1))
mfvEventFilterHTORBjetsORDisplacedDijet = mfvEventFilter.clone(mode = 'HT OR bjets OR displaced dijet', min_ht = cms.double(-1))
mfvEventFilterBjetsORDisplacedDijetVetoHT = mfvEventFilter.clone(mode = 'bjets OR displaced dijet veto HT', min_ht = cms.double(-1))
mfvEventFilterMETOnly = mfvEventFilter.clone(mode = 'MET only', min_ht = cms.double(-1))
mfvEventFilterRandomParameters = mfvEventFilter.clone(min_pt_for_ht = cms.double(-1), min_ht = cms.double(-1), min_njets = cms.int32(0),
                                                      min_electron_pt = cms.double(-1), min_muon_pt = cms.double(-1), min_nleptons = cms.int32(0))

# mfvEventFilterEle35 = mfvEventFilter.clone(mode = 'ele35', min_ht = cms.double(-1), min_njets = cms.int32(2), min_pt_for_ht = cms.double(-1))
# mfvEventFilterEle115 = mfvEventFilter.clone(mode = 'ele115', min_ht = cms.double(-1), min_njets = cms.int32(2), min_pt_for_ht = cms.double(-1), min_electron_pt = cms.double(120))
# mfvEventFilterEle50 = mfvEventFilter.clone(mode = 'ele50', min_ht = cms.double(-1), min_njets = cms.int32(2), min_pt_for_ht = cms.double(-1), min_electron_pt = cms.double(55))
# mfvEventFilterMu27 = mfvEventFilter.clone(mode = 'mu27', min_ht = cms.double(-1), min_njets = cms.int32(2), min_pt_for_ht = cms.double(-1))
# mfvEventFilterMu50 = mfvEventFilter.clone(mode = 'mu50', min_ht = cms.double(-1), min_njets = cms.int32(2), min_pt_for_ht = cms.double(-1), min_muon_pt = cms.double(53))
