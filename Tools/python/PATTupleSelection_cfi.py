from textwrap import dedent
import FWCore.ParameterSet.Config as cms

def denewline(s):
    return dedent(s).replace('\n', ' ')

# JMTBAD electron H/E cut uses fixed rho number, should do it right in event producer
electron_rho95 = 43. # this is the 95% point for double_fixedGridRhoFastjetCentral__RECO.obj from one file of QCD HT2000, a wjets file wants 37 but that rho distribution has a peak at 0 (?)

jtupleParams = cms.PSet(
    jetCut = cms.string(denewline('''
                        abs(eta) < 2.7 &&
                        numberOfDaughters > 1 &&
                        neutralHadronEnergyFraction < 0.90 &&
                        neutralEmEnergyFraction < 0.90 &&
                        muonEnergyFraction < 0.8 &&
                        (abs(eta) >= 2.4 || (chargedEmEnergyFraction < 0.80 && chargedHadronEnergyFraction > 0. && chargedMultiplicity > 0))
                        ''')),

    muonCut = cms.string(denewline('''
                        isPFMuon && isGlobalMuon &&
                        globalTrack.normalizedChi2 < 10. &&
                        track.hitPattern.trackerLayersWithMeasurement > 5 &&
                        globalTrack.hitPattern.numberOfValidMuonHits > 0 &&
                        innerTrack.hitPattern.numberOfValidPixelHits > 0 &&
                        numberOfMatchedStations > 1
                        ''')),

    electronCut = cms.string(denewline('''
                       (
                        isEB &&
                        full5x5_sigmaIetaIeta < 0.0128 &&
                        abs(deltaEtaSuperClusterTrackAtVtx - superCluster.eta + superCluster.seed.eta) < 0.00523 &&
                        abs(deltaPhiSuperClusterTrackAtVtx) < 0.159 &&
                        hadronicOverEm < 0.05 + 1.12/superCluster.energy + 0.0368*%(electron_rho95)f/superCluster.energy &&
                        abs(1/ecalEnergy - eSuperClusterOverP/ecalEnergy) < 0.193 &&
                        gsfTrack.hitPattern.numberOfAllHits("MISSING_INNER_HITS") <= 2
                        ) ||
                       (
                        isEE &&
                        full5x5_sigmaIetaIeta < 0.0445 &&
                        abs(deltaEtaSuperClusterTrackAtVtx - superCluster.eta + superCluster.seed.eta) < 0.00984 &&
                        abs(deltaPhiSuperClusterTrackAtVtx) < 0.157 &&
                        hadronicOverEm < 0.05 + 0.5/superCluster.energy + 0.201*%(electron_rho95)f/superCluster.energy &&
                        abs(1/ecalEnergy - eSuperClusterOverP/ecalEnergy) < 0.0962 &&
                        gsfTrack.hitPattern.numberOfAllHits("MISSING_INNER_HITS") <= 3
                        )
                       ''' % locals())),
)
