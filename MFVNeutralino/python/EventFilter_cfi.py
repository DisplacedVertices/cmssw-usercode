import FWCore.ParameterSet.Config as cms
from JMTucker.Tools.PATTupleSelection_cfi import jtupleParams
from JMTucker.Tools.Year import year
from JMTucker.MFVNeutralino.TriggerFilter_cfi import bjet_paths_2016, bjet_paths_2017, bjet_paths_2018, lepton_paths_2016, lepton_paths_2017, lepton_paths_2018


# TriggerHelper::pass_any_version expects the HLT path prefix ending in _v,
# while hltHighLevel uses the same prefix followed by a wildcard.
def for_trigger_helper(paths):
    return [p[:-1] if p.endswith('*') else p for p in paths]

if year == 2016:
    bjet_paths_for_trigger_helper = for_trigger_helper(bjet_paths_2016)
    lepton_paths_for_trigger_helper = for_trigger_helper(lepton_paths_2016)
elif year == 2017:
    bjet_paths_for_trigger_helper = for_trigger_helper(bjet_paths_2017)
    lepton_paths_for_trigger_helper = for_trigger_helper(lepton_paths_2017)
elif year == 2018:
    bjet_paths_for_trigger_helper = for_trigger_helper(bjet_paths_2018)
    lepton_paths_for_trigger_helper = for_trigger_helper(lepton_paths_2018)
else:
    raise RuntimeError("unsupported year")


mfvEventFilter = cms.EDFilter('MFVEventFilter',
                              mode = cms.string('either'),
                              jets_src = cms.InputTag('selectedPatJets'),
                              trigger_results_src = cms.InputTag('TriggerResults', '', 'HLT'),
                              jet_cut = jtupleParams.jetCut,
                              min_njets = cms.int32(-1),
                              min_pt_for_ht = cms.double(-1), 
                              min_ht = cms.double(-1),
                              muons_src = cms.InputTag('selectedPatMuons'),
                              muon_cut = jtupleParams.muonCut,
                              min_muon_pt = cms.double(30 if year == 2017 else 27),
                              electrons_src = cms.InputTag('selectedPatElectrons'),
                              electron_cut = jtupleParams.electronCut,
                              min_electron_pt = cms.double(35 if year == 2018 else 38 if year == 2017 else 30),
                              min_nleptons = cms.int32(0),
                              rho_src = cms.InputTag('fixedGridRhoFastjetAll'),
                              veto_bjet_triggers = cms.bool(False),
                              bjet_triggers_to_veto = cms.vstring(*bjet_paths_for_trigger_helper),
                              veto_lepton_triggers = cms.bool(False),
                              lepton_triggers_to_veto = cms.vstring(*lepton_paths_for_trigger_helper),
                              electron_effective_areas = cms.FileInPath('RecoEgamma/ElectronIdentification/data/Fall17/effAreaElectrons_cone03_pfNeuHadronsAndPhotons_92X.txt'),
                              parse_randpars = cms.bool(False), 
                              randpar_mass = cms.int32(-1),
                              randpar_ctau = cms.string(''),
                              randpar_dcay = cms.string(''),
                              debug = cms.untracked.bool(False),
                              )

mfvEventFilterJetsOnly = mfvEventFilter.clone(mode = 'jets only')
mfvEventFilterMuonsOnly = mfvEventFilter.clone(mode = 'muons only', min_ht = cms.double(-1), min_njets = cms.int32(-1), min_pt_for_ht = cms.double(-1), min_nleptons = cms.int32(1))
mfvEventFilterElectronsOnlyVetoMuons = mfvEventFilter.clone(mode = 'electrons only veto muons', min_ht = cms.double(-1), min_njets = cms.int32(-1), min_pt_for_ht = cms.double(-1), min_nleptons = cms.int32(1))
mfvEventFilterLowHT = mfvEventFilter.clone(mode = 'low HT', min_ht = cms.double(450.0), min_njets = cms.int32(2))
mfvEventFilterLeptonsOnly = mfvEventFilter.clone(mode = 'leptons only', min_nleptons = cms.int32(1))
mfvEventFilterDileptonOnly = mfvEventFilter.clone(mode = 'dilepton only', min_electron_pt = cms.double(20), min_muon_pt = cms.double(20), min_nleptons = cms.int32(2))
mfvEventFilterHTORBjetsORDisplacedDijet = mfvEventFilter.clone(mode = 'HT OR bjets OR displaced dijet', min_ht = cms.double(-1))
mfvEventFilterBjetsORDisplacedDijetVetoHT = mfvEventFilter.clone(mode = 'bjets OR displaced dijet veto HT', min_ht = cms.double(-1))
mfvEventFilterBjetsORDisplacedDijetVetoLeptonHT = mfvEventFilter.clone(mode = 'bjets OR displaced dijet veto leptons and HT', min_ht = cms.double(-1))
mfvEventFilterBjetsORDisplacedDijet = mfvEventFilter.clone(mode = 'bjets OR displaced dijet', min_ht = cms.double(-1))
mfvEventFilterMETOnly = mfvEventFilter.clone(mode = 'MET only', min_ht = cms.double(-1))
# For the DispJet data stream, the positive DispJet trigger requirement is
# supplied by mfvTriggerFilterDispJetOnly. This event filter adds only the
# BTag-trigger veto, assigning BTag/DispJet trigger overlaps to BTag/JetHT.
mfvEventFilterDispJetVetoBTagTriggers = mfvEventFilterBjetsORDisplacedDijetVetoLeptonHT.clone(
    veto_bjet_triggers = cms.bool(True),
)
mfvEventFilterRandomParameters = mfvEventFilter.clone(min_pt_for_ht = cms.double(-1), min_ht = cms.double(-1), min_njets = cms.int32(-1),
                                                      min_electron_pt = cms.double(-1), min_muon_pt = cms.double(-1), min_nleptons = cms.int32(0))
