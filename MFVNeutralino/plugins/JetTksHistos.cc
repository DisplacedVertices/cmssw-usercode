#include <stdio.h>
#include "TH2F.h"
#include "TRandom3.h"
#include "TVector2.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "DataFormats/PatCandidates/interface/PackedGenParticle.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "JMTucker/Tools/interface/ExtValue.h"
#include "JMTucker/Tools/interface/GenUtilities.h"
#include "JMTucker/Tools/interface/Utilities.h"
#include "JMTucker/MFVNeutralinoFormats/interface/MCInteractions.h"
#include "JMTucker/MFVNeutralinoFormats/interface/Event.h"
#include "JMTucker/MFVNeutralino/interface/EventTools.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "JMTucker/MFVNeutralinoFormats/interface/VertexAux.h"

class MFVJetTksHistos : public edm::EDAnalyzer {
 public:
  explicit MFVJetTksHistos(const edm::ParameterSet&);
  void analyze(const edm::Event&, const edm::EventSetup&);

 private:
  const edm::EDGetTokenT<MFVEvent> mevent_token;
  const edm::EDGetTokenT<double> weight_token;
  const edm::EDGetTokenT<MFVVertexAuxCollection> vertex_token;
  const edm::EDGetTokenT<reco::GenParticleCollection> gen_token;

  static const int CATEGORIES = 5;
  const int ALL      = 0;
  const int PASS_HLT = 1;
  const int FAIL_HLT = 2;
  const int PASS_OFF = 3;
  const int FAIL_OFF = 4;

  const double offline_csv;

  TH1F* h_w;

  TH1F* h_jet_pt[CATEGORIES];
  TH1F* h_jet_eta[CATEGORIES];
  TH1F* h_jet_phi[CATEGORIES];
  TH1F* h_jet_dbv[CATEGORIES];
  TH1F* h_jet_skeweta[CATEGORIES];
  TH1F* h_jet_skewphi[CATEGORIES];
  TH1F* h_jet_skew_dR[CATEGORIES];
  TH1F* h_jet_ntks[CATEGORIES];
  TH1F* h_jet_bdisc[CATEGORIES];
  TH1F* h_jet_bdisc_old[CATEGORIES];

  TH1F* h_jet_tks_pt[CATEGORIES];  
  TH1F* h_jet_tks_pt_rel[CATEGORIES];  
  TH1F* h_jet_tks_eta[CATEGORIES];  
  TH1F* h_jet_tks_eta_rel[CATEGORIES];  
  TH1F* h_jet_tks_dR[CATEGORIES];  
  TH1F* h_jet_tks_nsigmadxy[CATEGORIES];  
  TH1F* h_jet_tks_nsigmadxyz[CATEGORIES];  
  TH1F* h_jet_sum_nsigmadxy[CATEGORIES];  
  TH1F* h_jet_sum_nsigmadxyz[CATEGORIES];  

  TH1F* h_jet_tk_nsigmadxy_avg[CATEGORIES];
  TH1F* h_jet_tk_nsigmadxy_med[CATEGORIES];
  TH1F* h_jet_tk_nsigmadxy_0[CATEGORIES];
  TH1F* h_jet_tk_nsigmadxy_1[CATEGORIES];

  TH1F* h_jet_tk_nsigmadxyz_avg[CATEGORIES];
  TH1F* h_jet_tk_nsigmadxyz_med[CATEGORIES];
  TH1F* h_jet_tk_nsigmadxyz_0[CATEGORIES];
  TH1F* h_jet_tk_nsigmadxyz_1[CATEGORIES];

  TH1F* h_jet_sumtk_pt_ratio[CATEGORIES];
  TH1F* h_jet_sumtk_dR[CATEGORIES];

  TH2F* h_proxy_grid[CATEGORIES];
};

MFVJetTksHistos::MFVJetTksHistos(const edm::ParameterSet& cfg)
  : mevent_token(consumes<MFVEvent>(cfg.getParameter<edm::InputTag>("mevent_src"))),
    weight_token(consumes<double>(cfg.getParameter<edm::InputTag>("weight_src"))),
    vertex_token(consumes<MFVVertexAuxCollection>(cfg.getParameter<edm::InputTag>("vertex_src"))),
    gen_token(consumes<reco::GenParticleCollection>(cfg.getParameter<edm::InputTag>("gen_src"))),
    offline_csv(cfg.getParameter<double>("offline_csv"))

{
  edm::Service<TFileService> fs;

  h_w = fs->make<TH1F>("h_w", ";event weight;events/0.1", 100, 0, 10);

  for (int i = 0; i < CATEGORIES; ++i) {
    TString bres = i == 4 ? TString("fail_off") : (i == 3 ? TString("pass_off") : (i == 2 ? TString("fail_hlt") : (i == 1 ? TString("pass_hlt") : "pass_or_fail")));
    h_jet_pt[i] = fs->make<TH1F>(TString::Format("h_jet_pt_%s", bres.Data()), TString::Format(";p_{T} of jets that %s b-tag(GeV);events/10 GeV", bres.Data()), 200, 0, 800);
    h_jet_eta[i] = fs->make<TH1F>(TString::Format("h_jet_eta_%s", bres.Data()), TString::Format(";absv#eta of jets that %s b-tag;events/bin", bres.Data()), 120, 0, 2.5);
    h_jet_phi[i] = fs->make<TH1F>(TString::Format("h_jet_phi_%s", bres.Data()), TString::Format(";#phi of jets that %s b-tag;events/bin", bres.Data()), 100, -3.1416, 3.1416);
    h_jet_dbv[i] = fs->make<TH1F>(TString::Format("h_jet_dbv_%s", bres.Data()), TString::Format(";d_{BV} of jets that %s b-tag;events/bin", bres.Data()), 100, 0.0, 2.0);
    h_jet_skeweta[i] = fs->make<TH1F>(TString::Format("h_jet_skeweta_%s", bres.Data()), TString::Format(";#Delta#eta(jet, disp) for jets that %s b-tag;events/bin", bres.Data()), 120, 0, 3.0); // Original nBins = 120
    h_jet_skewphi[i] = fs->make<TH1F>(TString::Format("h_jet_skewphi_%s", bres.Data()), TString::Format(";#Delta#phi(jet, disp) for jets that %s b-tag;events/bin", bres.Data()), 100, -3.1416, 3.1416);
    h_jet_skew_dR[i] = fs->make<TH1F>(TString::Format("h_jet_skew_dR_%s", bres.Data()), TString::Format(";#DeltaR(jet, disp) for jets that %s b-tag;events/bin", bres.Data()), 100, 0, 1.6); // Original nBins = 100
    h_jet_ntks[i] = fs->make<TH1F>(TString::Format("h_jet_ntks_%s", bres.Data()), TString::Format(";#tks in jets that %s b-tag;events/bin", bres.Data()), 40, 0, 40);
    h_jet_bdisc[i] = fs->make<TH1F>(TString::Format("h_jet_bdisc_%s", bres.Data()), TString::Format(";DeepJet of jets that %s b-tag;events/bin", bres.Data()), 100, 0, 1.0);
    h_jet_bdisc_old[i] = fs->make<TH1F>(TString::Format("h_jet_bdisc_old_%s", bres.Data()), TString::Format(";CSV of jets that %s b-tag;events/bin", bres.Data()), 100, 0, 1.0);

    h_jet_tks_pt[i] = fs->make<TH1F>(TString::Format("h_jet_tks_pt_%s", bres.Data()), TString::Format(";p_{T} of all tks in jets that %s b-tag (GeV);events/bin", bres.Data()), 200, 0, 40);
    h_jet_tks_pt_rel[i] = fs->make<TH1F>(TString::Format("h_jet_tks_ptrel_%s", bres.Data()), TString::Format(";rel p_{T} of all tks in jets that %s b-tag (GeV);events/bin", bres.Data()), 200, 0, 20);
    h_jet_tks_eta[i] = fs->make<TH1F>(TString::Format("h_jet_tks_eta_%s", bres.Data()), TString::Format(";abs #eta of all tks in jets that %s b-tag;events/bin", bres.Data()), 100, 0, 4);
    h_jet_tks_eta_rel[i] = fs->make<TH1F>(TString::Format("h_jet_tks_etarel_%s", bres.Data()), TString::Format(";rel #eta of all tks in jets that %s b-tag;events/bin", bres.Data()), 300, 0, 10);
    h_jet_tks_dR[i] = fs->make<TH1F>(TString::Format("h_jet_tks_dR_%s", bres.Data()), TString::Format(";dR between jet and all tks in jets - %s b-tag;events/bin", bres.Data()), 100, 0, 0.6);
    h_jet_tks_nsigmadxy[i] = fs->make<TH1F>(TString::Format("h_jet_tks_nsigmadxy_%s", bres.Data()), TString::Format("; n #sigma(dxy) of all tks in jets which %s b-tag;events/bin", bres.Data()), 150, 0, 15);
    h_jet_tks_nsigmadxyz[i] = fs->make<TH1F>(TString::Format("h_jet_tks_nsigmadxyz_%s", bres.Data()), TString::Format("; n#sigma(dxyz) of tks in jets which %s b-tag;events/bin", bres.Data()), 150, 0, 15);
    h_jet_sum_nsigmadxy[i] = fs->make<TH1F>(TString::Format("h_jet_sum_nsigmadxy_%s", bres.Data()), TString::Format(";#Sigma n#sigma(dxy) of tks in jets which %s b-tag;events/bin", bres.Data()), 500, 0, 1500);
    h_jet_sum_nsigmadxyz[i] = fs->make<TH1F>(TString::Format("h_jet_sum_nsigmadxyz_%s", bres.Data()), TString::Format(";#Sigman#sigma(dxyz) of tks in jets which %s b-tag;events/bin", bres.Data()), 500, 0, 1500);

    h_jet_tk_nsigmadxy_avg[i] = fs->make<TH1F>(TString::Format("h_jet_tk_nsigmadxy_avg_%s", bres.Data()), TString::Format("; avg n#sigma(dxy) of tks in jets which %s b-tag; events/bin", bres.Data()), 300, 0, 30);
    h_jet_tk_nsigmadxy_med[i] = fs->make<TH1F>(TString::Format("h_jet_tk_nsigmadxy_med_%s", bres.Data()), TString::Format("; median n#sigma(dxy) of tks in jets which %s b-tag; events/bin", bres.Data()), 300, 0, 30);
    h_jet_tk_nsigmadxy_0[i] = fs->make<TH1F>(TString::Format("h_jet_tk_nsigmadxy_0_%s", bres.Data()), TString::Format("; max n#sigma(dxy) of tks in jets which %s b-tag; events/bin", bres.Data()), 300, 0, 150);
    h_jet_tk_nsigmadxy_1[i] = fs->make<TH1F>(TString::Format("h_jet_tk_nsigmadxy_1_%s", bres.Data()), TString::Format("; 2nd-leading n#sigma(dxy) of tks in jets which %s b-tag; events/bin", bres.Data()), 300, 0, 150);

    h_jet_tk_nsigmadxyz_avg[i] = fs->make<TH1F>(TString::Format("h_jet_tk_nsigmadxyz_avg_%s", bres.Data()), TString::Format("; avg n#sigma(dxyz) of tks in jets which %s b-tag; events/bin", bres.Data()), 300, 0, 30);
    h_jet_tk_nsigmadxyz_med[i] = fs->make<TH1F>(TString::Format("h_jet_tk_nsigmadxyz_med_%s", bres.Data()), TString::Format("; median n#sigma(dxyz) of tks in jets which %s b-tag; events/bin", bres.Data()), 300, 0, 30);
    h_jet_tk_nsigmadxyz_0[i] = fs->make<TH1F>(TString::Format("h_jet_tk_nsigmadxyz_0_%s", bres.Data()), TString::Format("; max n#sigma(dxyz) of tks in jets which %s b-tag; events/bin", bres.Data()), 300, 0, 150);
    h_jet_tk_nsigmadxyz_1[i] = fs->make<TH1F>(TString::Format("h_jet_tk_nsigmadxyz_1_%s", bres.Data()), TString::Format("; 2nd-leading n#sigma(dxyz) of tks in jets which %s b-tag; events/bin", bres.Data()), 300, 0, 150);

    h_jet_sumtk_pt_ratio[i] = fs->make<TH1F>(TString::Format("h_jet_sumtk_pt_ratio_%s", bres.Data()), TString::Format(";pT(jet tracks) / pT(jet) - %s b-tag;events/bin", bres.Data()), 100, 0, 4);
    h_jet_sumtk_dR[i] = fs->make<TH1F>(TString::Format("h_jet_sumtk_dR_%s", bres.Data()), TString::Format(";dR between jet and tks in jets - %s b-tag;events/bin", bres.Data()), 100, 0, 0.6);
    
    h_proxy_grid[i] = fs->make<TH2F>(TString::Format("h_proxy_grid_%s", bres.Data()), ";b-score cut value; >=3 offline proxies?", 100, 0, 1, 2, 0, 1.2);
  }

}

struct Track_Helper {
    float dr     = -9.9;
    float dz     = -9.9;
    float drerr  = -9.9;
    float dzerr  = -9.9;
    float drz    = -9.9;
    float drzerr = -9.9;
};

struct Jet_Loc_Helper {
    float vtx_jet_pt  = -9.9;
    float vtx_jet_eta = -9.9;
    float vtx_jet_phi = -9.9;
    float vtx_pt   = -9.9;
    float vtx_eta  = -9.9;
    float vtx_phi  = -9.9;
    float vtx_dx  = -9.9;
    float vtx_dy  = -9.9;
    float vtx_dz  = -9.9;
};

void MFVJetTksHistos::analyze(const edm::Event& event, const edm::EventSetup&) {
      
    edm::Handle<MFVEvent> mevent;
    event.getByToken(mevent_token, mevent);
  
    edm::Handle<reco::GenParticleCollection> gen_particles;
    event.getByToken(gen_token, gen_particles);
  
    edm::Handle<double> weight;
    event.getByToken(weight_token, weight);

    edm::Handle<MFVVertexAuxCollection> auxes;
    event.getByToken(vertex_token, auxes);
    const int nsv = int(auxes->size());
  
    const double w = *weight;
    h_w->Fill(w);
  

    std::vector<Jet_Loc_Helper> jet_loc_helper;
    for (int isv = 0; isv < nsv; isv++) {
        const MFVVertexAux& aux = auxes->at(isv);

        // The index [0] indicates that we're using ntracks to assoc.
        // a jet to a vertex. No need to worry about this right now.
        const std::vector<float> my_pts  = aux.jet_pt[0];
        const std::vector<float> my_etas = aux.jet_eta[0];
        const std::vector<float> my_phis = aux.jet_phi[0];
        int npt = int(my_pts.size());

        for (int ij=0; ij < npt; ij++) {
            Jet_Loc_Helper tmp_loc_helper;
            tmp_loc_helper.vtx_jet_pt  = my_pts[ij];
            tmp_loc_helper.vtx_jet_eta = my_etas[ij];
            tmp_loc_helper.vtx_jet_phi = my_phis[ij];

            // The index [2] indicates use tracks+jet to get pt/eta/phi
            tmp_loc_helper.vtx_pt  = aux.pt[2];
            tmp_loc_helper.vtx_eta = aux.eta[2];
            tmp_loc_helper.vtx_phi = aux.phi[2];

            tmp_loc_helper.vtx_dx  = aux.x - mevent->bsx_at_z(aux.z);
            tmp_loc_helper.vtx_dy  = aux.y - mevent->bsy_at_z(aux.z);
            tmp_loc_helper.vtx_dz  = aux.z - mevent->bsz;
            
            jet_loc_helper.push_back(tmp_loc_helper);
        }
    } 

    for (int i = 0; i < mevent->njets(); ++i) {
        bool matches_online_bjet = false;
        bool matches_online_calo = false;

        if (mevent->jet_bdisc_old[i] < offline_csv || mevent->nth_jet_pt(i) < 30.0) continue;
    
        std::vector<int> fill_hists;
        fill_hists.push_back(ALL);     // Always fill histo #0
    
        float sum_nsigmadxy = 0.0;
        float sum_nsigmadxyz = 0.0;
    
        float off_pt  = mevent->nth_jet_pt(i);
        float off_eta = mevent->nth_jet_eta(i);
        float off_phi = mevent->nth_jet_phi(i);

        float jet_dbv = 0.0;
    
        TVector3 jet_vector;
        jet_vector.SetPtEtaPhi(mevent->nth_jet_pt(i), off_eta, off_phi);       
        jet_vector.SetMag(1.0);
    
        // See if this jet matches to an online calojet (probably yes)
        int n_online_calojets = mevent->hlt_pf_jet_pt.size();
        for (int j=0; j < n_online_calojets; j++) {
            float hlt_eta = mevent->hlt_pf_jet_eta[j];
            float hlt_phi = mevent->hlt_pf_jet_phi[j];
    
            if(reco::deltaR(hlt_eta, hlt_phi, off_eta, off_phi) < 0.14) { matches_online_calo = true; break;}
        }
                      
        // If for some weird reason, there's no match btwn online/offline jets, skip this jet
        if (not matches_online_calo) continue;
    
        // See if this jet matches to some HLT jet which passes the btag filters
        int n_online_bjets = mevent->hlt_pfforbtag_jet_pt.size();
        for (int j=0; j < n_online_bjets; j++) {
            float hlt_eta = mevent->hlt_pfforbtag_jet_eta[j];
            float hlt_phi = mevent->hlt_pfforbtag_jet_phi[j];
    
            if(reco::deltaR(hlt_eta, hlt_phi, off_eta, off_phi) < 0.14) { matches_online_bjet = true; }
        }
    
        // Which histograms do we need to fill?
        fill_hists.push_back(matches_online_bjet ? PASS_HLT : FAIL_HLT);
        fill_hists.push_back(mevent->jet_bdisc_old[i] > offline_csv ? PASS_OFF : FAIL_OFF);
        
        // Try and find the point that this jet originates from. Do this by finding the closest instance of jet_loc_helper
        float closest_helper_dR  = 4.0;
        float closest_vtx_eta = -9.0;
        float closest_vtx_phi = -9.0;
        for (auto helper : jet_loc_helper) {
            float temp_dR = reco::deltaR(helper.vtx_jet_eta, helper.vtx_jet_phi, off_eta, off_phi);
            if (temp_dR < closest_helper_dR) {
                closest_helper_dR = temp_dR;
                jet_dbv = std::hypot(helper.vtx_dx, helper.vtx_dy);

                closest_vtx_eta = helper.vtx_eta;
                closest_vtx_phi = helper.vtx_phi;
            }
        }
        float closest_vtx_dR = reco::deltaR(closest_vtx_eta, closest_vtx_phi, off_eta, off_phi);

        // Fill the pre-determined histograms
        for (auto n_hist : fill_hists) {
             h_jet_pt[n_hist]->Fill(mevent->nth_jet_pt(i), w);
             h_jet_eta[n_hist]->Fill(fabs(mevent->nth_jet_eta(i)), w);
             h_jet_phi[n_hist]->Fill(mevent->nth_jet_phi(i), w);
             h_jet_dbv[n_hist]->Fill(jet_dbv, w);
             h_jet_skeweta[n_hist]->Fill(fabs(closest_vtx_eta - off_eta), w);
             h_jet_skewphi[n_hist]->Fill(TVector2::Phi_mpi_pi(closest_vtx_phi - off_phi), w);
             h_jet_skew_dR[n_hist]->Fill(closest_vtx_dR, w);
             h_jet_ntks[n_hist]->Fill((int)(mevent->n_jet_tracks(i)));
             h_jet_bdisc[n_hist]->Fill((i < (int)(mevent->jet_bdisc.size()) ? mevent->jet_bdisc[i] : -9.9), w);
             h_jet_bdisc_old[n_hist]->Fill((i < (int)(mevent->jet_bdisc_old.size()) ? mevent->jet_bdisc_old[i] : -9.9), w);
        }
    
        // Start the track portion of this code
        TVector3 jet_sumtk_vector;
        jet_sumtk_vector.SetPtEtaPhi(0.0, 0.0, 0.0);

        std::vector<Track_Helper> trackhelper;
        for (size_t ntk = 0 ; ntk < mevent->n_jet_tracks_all() ; ntk++) {
            if (mevent->jet_track_which_jet[ntk] == i) {
               
              // Vars needed to get 3D IP dist significance
              float dr = mevent->jet_track_dxy[ntk];
              float dz = mevent->jet_track_dz[ntk];
              float drerr = mevent->jet_track_dxy_err[ntk];
              float dzerr = mevent->jet_track_dz_err[ntk];
      
              // Calculate 3D IP dist significance
              float drz = std::hypot(dr, dz);
              float drzerr = std::hypot(dr*drerr/drz , dz*dzerr/drz);
      
              // Add the above variables to a temporary Track_Helper instance. Then, append it.
              Track_Helper temp_helper;
              temp_helper.dr = dr;
              temp_helper.dz = dz;
              temp_helper.drerr = drerr;
              temp_helper.dzerr = dzerr;
              temp_helper.drz = drz;
              temp_helper.drzerr = drzerr;
              trackhelper.push_back(temp_helper);
      
              TVector3 tk_vector;
              tk_vector.SetPtEtaPhi(fabs(mevent->jet_track_qpt[ntk]), mevent->jet_track_eta[ntk], mevent->jet_track_phi[ntk]);
      
              jet_sumtk_vector += tk_vector;        
              sum_nsigmadxy  += fabs(dr/drerr);
              sum_nsigmadxyz += fabs(drz/drzerr);
                 
             
              float pt_rel = (tk_vector.Cross(jet_vector)).Mag();
              float eta_rel = std::atanh( tk_vector.Dot(jet_vector) / tk_vector.Mag() );
      
              for (auto n_hist : fill_hists) {
                   h_jet_tks_pt[n_hist]->Fill(fabs(mevent->jet_track_qpt[ntk]), w);
                   h_jet_tks_pt_rel[n_hist]->Fill(pt_rel, w);
                   h_jet_tks_eta[n_hist]->Fill(fabs(mevent->jet_track_eta[ntk]), w);
                   h_jet_tks_eta_rel[n_hist]->Fill(eta_rel, w);
                   h_jet_tks_dR[n_hist]->Fill(tk_vector.DeltaR(jet_vector), w);
                   h_jet_tks_nsigmadxy[n_hist]->Fill(fabs(dr/drerr), w);
                   h_jet_tks_nsigmadxyz[n_hist]->Fill(fabs(drz/drzerr), w);
              }
      
            }
      
            for (auto n_hist : fill_hists) {
                h_jet_sum_nsigmadxy[n_hist]->Fill(sum_nsigmadxy, w);
                h_jet_sum_nsigmadxyz[n_hist]->Fill(sum_nsigmadxyz, w);
            }
    
        }
    
        // Sort the tracks in the jet by nsigma(dxyz)
        std::sort(trackhelper.begin(), trackhelper.end(), [](Track_Helper const &a, Track_Helper &b) -> bool{ return fabs(a.dr/a.drerr) > fabs(b.dr/b.drerr); } );
        //std::sort(trackhelper.begin(), trackhelper.end(), [](Track_Helper const &a, Track_Helper &b) -> bool{ return fabs(a.drz/a.drzerr) > fabs(b.drz/b.drzerr); } );
        
        // Calculate mean and median nsigmadxy
        int njtks = trackhelper.size();
        if (njtks > 0) {
            float med_nsigmadxy = -2.0;
            float avg_nsigmadxy = 0.0;
      
            float med_nsigmadxyz = -2.0;
            float avg_nsigmadxyz = 0.0;
             
            if (njtks % 2 == 0) { 
                med_nsigmadxy = fabs((trackhelper[njtks/2 - 1].dr / trackhelper[njtks/2 - 1].drerr) + (trackhelper[njtks/2].dr / trackhelper[njtks/2].drerr))/2;
                med_nsigmadxyz = fabs((trackhelper[njtks/2 - 1].drz / trackhelper[njtks/2 - 1].drzerr) + (trackhelper[njtks/2].drz / trackhelper[njtks/2].drzerr))/2;
            }
            else {
                med_nsigmadxy = fabs( trackhelper[njtks/2].dr / trackhelper[njtks/2].drerr );
                med_nsigmadxyz = fabs( trackhelper[njtks/2].drz / trackhelper[njtks/2].drzerr );
            }
      
            for (int it=0; it < njtks; it++) {
                avg_nsigmadxy += fabs(trackhelper[it].dr / trackhelper[it].drerr);
                avg_nsigmadxyz += fabs(trackhelper[it].drz / trackhelper[it].drzerr);
            }
            avg_nsigmadxy /= njtks;
            avg_nsigmadxyz /= njtks;
      
      
            for (auto n_hist : fill_hists) {
                // Plot mean and median nsigmadxy
                h_jet_tk_nsigmadxy_avg[n_hist]->Fill(avg_nsigmadxy, w);
                h_jet_tk_nsigmadxy_med[n_hist]->Fill(med_nsigmadxy, w);
            
                h_jet_tk_nsigmadxyz_avg[n_hist]->Fill(avg_nsigmadxyz, w);
                h_jet_tk_nsigmadxyz_med[n_hist]->Fill(med_nsigmadxyz, w);
            
                // While we're at it, plot max nsigmadxy
                h_jet_tk_nsigmadxy_0[n_hist]->Fill(fabs(trackhelper[0].dr / trackhelper[0].drerr), w);
                h_jet_tk_nsigmadxyz_0[n_hist]->Fill(fabs(trackhelper[0].drz / trackhelper[0].drzerr), w);
            }
        }
    
        for (auto n_hist : fill_hists) {
            if (njtks > 1) {
                h_jet_tk_nsigmadxy_1[n_hist]->Fill(fabs(trackhelper[1].dr / trackhelper[1].drerr), w);
                h_jet_tk_nsigmadxyz_1[n_hist]->Fill(fabs(trackhelper[1].drz / trackhelper[1].drzerr), w);
            }
      
            h_jet_sumtk_pt_ratio[n_hist]->Fill(mevent->nth_jet_pt(i) / jet_sumtk_vector.Pt(), w);
            h_jet_sumtk_dR[n_hist]->Fill(jet_vector.DeltaR(jet_sumtk_vector), w);
        }
            
    }
      
    //////////////////////////////////////////////////////////////////////////////
      
    for (int b = 0; b < 100; b++) {
        float b_cut = (b * 0.01)+0.00001;
        int   n_proxies = 0; // Number of jets passing whatever the proxy is
        int   n_passes  = 0; // Number of jets matching to an HLT bjet
        int n_online_bjets = mevent->hlt_pfforbtag_jet_pt.size();
    
        for (int i = 0; i < mevent->njets(); i++) {
            float b_disc = (i < (int)(mevent->jet_bdisc_old.size()) ? mevent->jet_bdisc_old[i] : -9.9);
            if (b_disc < 0.0 or mevent->nth_jet_pt(i) < 30.0) continue;
            if (b_disc > b_cut) n_proxies++;
      
            float off_eta = mevent->nth_jet_eta(i);
            float off_phi = mevent->nth_jet_phi(i);
      
            for (int j=0; j < n_online_bjets; j++) {
                float hlt_eta = mevent->hlt_pfforbtag_jet_eta[j];
                float hlt_phi = mevent->hlt_pfforbtag_jet_phi[j];
                if(reco::deltaR(hlt_eta, hlt_phi, off_eta, off_phi) < 0.14) n_passes++;
            }
        }
    
        float y_bin  = n_proxies >= 3 ? 1.0 : 0.0;
        int n_hist = n_online_bjets >= 3 ? 0 : 1;   // If this collection has at least three members, then there's enough HLT bjets to pass
        h_proxy_grid[n_hist]->Fill(b_cut, y_bin, w);
      
    }
  
}
DEFINE_FWK_MODULE(MFVJetTksHistos);
