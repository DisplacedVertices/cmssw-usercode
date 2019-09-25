#include "JMTucker/MFVNeutralinoFormats/interface/Event.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "DataFormats/TrackReco/interface/Track.h"

void MFVEvent::lep_push_back(MFVEvent::lep_id_t id,
                             const reco::Candidate& lep,
                             const reco::Track& trk,
                             const double iso,
                             const std::vector<TLorentzVector>& hltleps,
                             const math::XYZPoint& beamspot,
                             const math::XYZPoint& primary_vertex) {

  lep_id_.push_back(id); // expects already el/mu encoded
  lep_qpt.push_back(lep.charge() * lep.pt());
  lep_eta.push_back(lep.eta());
  lep_phi.push_back(lep.phi());
  lep_dxy.push_back(trk.dxy(primary_vertex));
  lep_dxybs.push_back(trk.dxy(beamspot));
  lep_dz.push_back(trk.dz(primary_vertex));

  lep_pt_err.push_back(trk.ptError());
  lep_eta_err.push_back(trk.etaError());
  lep_phi_err.push_back(trk.phiError());
  lep_dxy_err.push_back(trk.dxyError());
  lep_dz_err.push_back(trk.dzError());

  lep_chi2dof.push_back(trk.normalizedChi2());
  lep_hp_push_back(trk.hitPattern().numberOfValidPixelHits(),
                   trk.hitPattern().numberOfValidStripHits(),
                   trk.hitPattern().pixelLayersWithMeasurement(),
                   trk.hitPattern().stripLayersWithMeasurement());

  lep_iso.push_back(iso);

  double hltmatchdist2 = 0.1*0.1;
  TLorentzVector hltmatch;
  for (auto hlt : hltleps) {
    const double dist2 = reco::deltaR2(lep.eta(), lep.phi(), hlt.Eta(), hlt.Phi());
    if (dist2 < hltmatchdist2) {
      hltmatchdist2 = dist2;
      hltmatch = hlt;
    }
  }
  lep_hlt_pt.push_back(hltmatch.Pt());
  lep_hlt_eta.push_back(hltmatch.Eta());
  lep_hlt_phi.push_back(hltmatch.Phi());
}

void MFVEvent::jet_hlt_push_back(const reco::Candidate& jet, const std::vector<mfv::HLTJet>& hltjets){

  // use dR = 0.4 for the matching (in eta x phi)
  double hltmatchdist2 = 0.4*0.4;
  mfv::HLTJet hltmatch;
  for (auto hlt : hltjets) {
    const double dist2 = reco::deltaR2(jet.eta(), jet.phi(), hlt.p4.Eta(), hlt.p4.Phi());
    if (dist2 < hltmatchdist2) {
      hltmatchdist2 = dist2;
      hltmatch = hlt;
    }
  }
  jet_hlt_pt.push_back(hltmatch.p4.Pt());
  jet_hlt_eta.push_back(hltmatch.p4.Eta());
  jet_hlt_phi.push_back(hltmatch.p4.Phi());
  jet_hlt_energy.push_back(hltmatch.p4.E());
}
