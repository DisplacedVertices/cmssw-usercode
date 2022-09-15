#include "JMTucker/MFVNeutralinoFormats/interface/Event.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "DataFormats/TrackReco/interface/Track.h"

void MFVEvent::muon_push_back(const reco::Muon& muon,
			      const reco::Track& trk,
			      const float iso,
			      const math::XYZPoint& beamspot,
			      const math::XYZPoint& primary_vertex) {

  
  muon_pt.push_back(muon.pt());
  muon_eta.push_back(muon.eta());
  muon_phi.push_back(muon.phi());
  muon_pt_err.push_back(trk.ptError());
  muon_eta_err.push_back(trk.etaError());
  muon_phi_err.push_back(trk.phiError());
  muon_x.push_back(trk.vx());
  muon_y.push_back(trk.vy());
  muon_z.push_back(trk.vz());
  muon_lxy.push_back(mag(trk.vx(), trk.vy()));
  muon_l.push_back(mag(trk.vx(), trk.vy(), trk.vz()));

  
  muon_iso.push_back(iso);
  
  muon_dxy.push_back(trk.dxy(primary_vertex));
  muon_dz.push_back(trk.dz(primary_vertex));
  muon_dxybs.push_back(trk.dxy(beamspot));
  muon_dxyerr.push_back(trk.dxyError());
  muon_dzerr.push_back(trk.dzError());
 
  

  muon_chi2dof.push_back(trk.normalizedChi2());
  
  muon_hp_push_back(trk.hitPattern().numberOfValidPixelHits(),
  		   trk.hitPattern().numberOfValidStripHits(),
  		   trk.hitPattern().pixelLayersWithMeasurement(),
                   trk.hitPattern().stripLayersWithMeasurement());
   
  
}

void MFVEvent::electron_push_back(const reco::GsfElectron& electron,
				  const reco::Track& trk,
				  const float iso,
				  const math::XYZPoint& beamspot,
				  const math::XYZPoint& primary_vertex) {

   electron_pt.push_back(electron.pt());
   electron_eta.push_back(electron.eta());
   electron_phi.push_back(electron.phi());
   electron_pt_err.push_back(trk.ptError());
   electron_eta_err.push_back(trk.etaError());
   electron_phi_err.push_back(trk.phiError());
   electron_x.push_back(trk.vx());
   electron_y.push_back(trk.vy());
   electron_z.push_back(trk.vz());
   electron_lxy.push_back(mag(trk.vx(), trk.vy()));
   electron_l.push_back(mag(trk.vx(), trk.vy(), trk.vz()));
     
   electron_iso.push_back(iso);

   electron_dxy.push_back(trk.dxy(primary_vertex));
   electron_dz.push_back(trk.dz(primary_vertex));
   electron_dxybs.push_back(trk.dxy(beamspot));
   electron_dxyerr.push_back(trk.dxyError());
   electron_dzerr.push_back(trk.dzError());
   

   electron_chi2dof.push_back(trk.normalizedChi2());
   electron_hp_push_back(trk.hitPattern().numberOfValidPixelHits(),
   			 trk.hitPattern().numberOfValidStripHits(),
   			 trk.hitPattern().pixelLayersWithMeasurement(),
   			 trk.hitPattern().stripLayersWithMeasurement());
   

}

void MFVEvent::jet_hlt_push_back(const reco::Candidate& jet, const std::vector<TLorentzVector>& hltjets, bool is_displaced_calojets){

  // use dR = 0.4 for the matching (in eta x phi)
  double hltmatchdist2 = 0.4*0.4;
  TLorentzVector hltmatch;
  for (auto hlt : hltjets) {
    const double dist2 = reco::deltaR2(jet.eta(), jet.phi(), hlt.Eta(), hlt.Phi());
    if (dist2 < hltmatchdist2) {
      hltmatchdist2 = dist2;
      hltmatch = hlt;
    }
  }

  if(is_displaced_calojets){
    displaced_jet_hlt_pt.push_back(hltmatch.Pt());
    displaced_jet_hlt_eta.push_back(hltmatch.Eta());
    displaced_jet_hlt_phi.push_back(hltmatch.Phi());
    displaced_jet_hlt_energy.push_back(hltmatch.E());
  }
  else{
    jet_hlt_pt.push_back(hltmatch.Pt());
    jet_hlt_eta.push_back(hltmatch.Eta());
    jet_hlt_phi.push_back(hltmatch.Phi());
    jet_hlt_energy.push_back(hltmatch.E());
  }
}

void MFVEvent::muon_pfiso_push_back(const float muhad_iso,
				    const float muneut_iso,
				    const float muphoton_iso,
				    const float PU_corr){

  muon_had_iso.push_back(muhad_iso);
  muon_neutral_iso.push_back(muneut_iso);
  muon_photon_iso.push_back(muphoton_iso);
  muon_PU_corr.push_back(PU_corr);
}

void MFVEvent::electron_pfiso_push_back(const float elhad_iso,
					const float elneut_iso,
					const float elphoton_iso,
					const float elcorr){
  electron_had_iso.push_back(elhad_iso);
  electron_neutral_iso.push_back(elneut_iso);
  electron_photon_iso.push_back(elphoton_iso);
  electron_corr.push_back(elcorr);
}

void MFVEvent::ele_ID_push_back(const reco::GsfElectron& electron,
			        const bool h_Escaled,
				const float ooEmooP,
				const int expectedMissingInnerHits,
				const float iso,
				const bool passveto){
				
  electron_isEB.push_back(electron.isEB());
  electron_isEE.push_back(electron.isEE());
  electron_sigmaIetaIeta5x5.push_back(electron.full5x5_sigmaIetaIeta());
  electron_dEtaAtVtx.push_back(electron.deltaEtaSuperClusterTrackAtVtx());
  electron_dPhiAtVtx.push_back(electron.deltaPhiSuperClusterTrackAtVtx());
  electron_HE.push_back(h_Escaled);
  electron_ooEmooP.push_back(ooEmooP);
  electron_expectedMissingInnerHits.push_back(expectedMissingInnerHits);
  electron_passveto.push_back(passveto);
  electron_iso.push_back(iso);

}
