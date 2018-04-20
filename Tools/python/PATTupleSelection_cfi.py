from textwrap import dedent
import FWCore.ParameterSet.Config as cms
from JMTucker.Tools.Year import year

# JMTBAD these need to be checked
# JMTBAD get rid of semilep/dilep

# Cuts for muons and electrons, including relative isolation with
# delta beta corrections. First set (no "signal" or "semilep"/"dilep")
# is for loose cuts (e.g. for vetos), and "semilep"/"dilep" are the
# reference cuts for those channels from TWikiTopRefEventSel. // JMTBAD were those cuts anyway...
# Can/should re-do cuts in ntupler starting from loose selection,
# including impact parameter cuts that aren't included here. We store
# these strings in a process-level PSet so they can be easily gotten
# later from provenance (should also be able to get them from the
# modules' PSets).

iso = '(chargedHadronIso + max(0.,neutralHadronIso) + photonIso - 0.5*puChargedHadronIso)'
muonIso = iso + '/pt'
electronIso = iso + '/et'

def denewline(s):
    return dedent(s).replace('\n', ' ')

electron_missing_inner_hits = 'gsfTrack.hitPattern.numberOfAllHits("MISSING_INNER_HITS")'
if year < 2017:
    electron_missing_inner_hits = electron_missing_inner_hits.replace('All','')

electronId = denewline('''
(
 isEB &&
 full5x5_sigmaIetaIeta < 0.0115 &&
 abs(deltaEtaSuperClusterTrackAtVtx - superCluster.eta + superCluster.seed.eta) < 0.00749 &&
 abs(deltaPhiSuperClusterTrackAtVtx) < 0.228 &&
 hadronicOverEm < 0.356 &&
 abs(1/ecalEnergy - eSuperClusterOverP/ecalEnergy) < 0.299 &&
 %(electron_missing_inner_hits)s <= 2 &&
 passConversionVeto
 ) ||
(
 isEE &&
 full5x5_sigmaIetaIeta < 0.037 &&
 abs(deltaEtaSuperClusterTrackAtVtx - superCluster.eta + superCluster.seed.eta) < 0.00895 &&
 abs(deltaPhiSuperClusterTrackAtVtx) < 0.213 &&
 hadronicOverEm < 0.211 &&
 abs(1/ecalEnergy - eSuperClusterOverP/ecalEnergy) < 0.15 &&
 %(electron_missing_inner_hits)s <= 3 &&
 passConversionVeto
 )
''' % locals())

jetPresel = denewline('''
(
 abs(eta) <= 2.7 &&
 numberOfDaughters > 1 &&
 neutralHadronEnergyFraction < 0.90 &&
 neutralEmEnergyFraction < 0.90 &&
 muonEnergyFraction < 0.8 &&
 (abs(eta) >= 2.4 || (chargedEmEnergyFraction < 0.90 && chargedHadronEnergyFraction > 0. && chargedMultiplicity > 0))
 ) ||
(
 abs(eta) > 2.7 && abs(eta) <= 3.0 &&
 neutralEmEnergyFraction < 0.90 &&
 neutralMultiplicity > 2
 ) ||
(
 abs(eta) > 3.0 &&
 neutralEmEnergyFraction < 0.90 &&
 neutralMultiplicity > 10
 )
''')

jtupleParams = cms.PSet(
    jetPresel = cms.string(jetPresel),
    #jetCut = cms.string('pt > 20. && abs(eta) < 2.5 && (%s)' % jetPresel),
    jetCut = cms.string(denewline('''
                        pt > 20. && abs(eta) < 2.5 &&
                        numberOfDaughters > 1 &&
                        neutralHadronEnergyFraction < 0.90 &&
                        neutralEmEnergyFraction < 0.90 &&
                        muonEnergyFraction < 0.8 &&
                        (abs(eta) >= 2.4 || (chargedEmEnergyFraction < 0.90 && chargedHadronEnergyFraction > 0. && chargedMultiplicity > 0))
                        ''')),

    muonCut      = cms.string('isPFMuon && (isGlobalMuon || isTrackerMuon) && abs(eta) < 2.4'),
    dilepMuonCut = cms.string('isPFMuon && (isGlobalMuon || isTrackerMuon) && abs(eta) < 2.4'),
    semilepMuonCut = cms.string(denewline('''
                                isPFMuon && isGlobalMuon &&
                                pt > 7. && abs(eta) < 2.4 &&
                                globalTrack.normalizedChi2 < 10. &&
                                track.hitPattern.trackerLayersWithMeasurement > 5 &&
                                globalTrack.hitPattern.numberOfValidMuonHits > 0 &&
                                innerTrack.hitPattern.numberOfValidPixelHits > 0 &&
                                numberOfMatchedStations > 1
                                ''')),

    electronCut = cms.string(electronId),
    dilepElectronCut = cms.string('1'),
    semilepElectronCut = cms.string('1'),
)
