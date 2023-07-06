#include "TH2F.h"
#include "TVector3.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/Common/interface/AssociationMap.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "JMTucker/MFVNeutralinoFormats/interface/LeptonVertexAssociation.h"
#include "TrackingTools/Records/interface/TransientTrackRecord.h"
#include "TrackingTools/TransientTrack/interface/TransientTrack.h"
#include "TrackingTools/TransientTrack/interface/TransientTrackBuilder.h"
#include "JMTucker/Tools/interface/TrackRefGetter.h"
#include <algorithm>

class MFVLeptonVertexAssociator : public edm::EDProducer {
public:
  MFVLeptonVertexAssociator(const edm::ParameterSet&);

  virtual void produce(edm::Event&, const edm::EventSetup&);

private:
  typedef mfv::ElectronVertexAssociation ElAssociation;
  typedef mfv::MuonVertexAssociation MuAssociation;

  const bool enable;
  const edm::EDGetTokenT<pat::MuonCollection> muons_token;
  const edm::EDGetTokenT<pat::ElectronCollection> electrons_token;
  const edm::EDGetTokenT<reco::VertexRefVector> vertex_ref_token;
  const edm::EDGetTokenT<reco::VertexCollection> vertex_token;
  const bool input_is_refs;
  const double min_vertex_track_weight;
  const bool histos;
  const bool verbose;

  TH1F* h_mutrack_dr; 
  TH1F* h_mutrack_bestdr;
  TH1F* h_eltrack_dr;
  TH1F* h_eltrack_bestdr;
  TH1F* h_ele_vtx_miss_dist;
  TH1F* h_mu_vtx_miss_dist;
  TH1F* h_matchedele_vtx_miss_dist;
  TH1F* h_matchedmu_vtx_miss_dist;

};

MFVLeptonVertexAssociator::MFVLeptonVertexAssociator(const edm::ParameterSet& cfg)
  : enable(cfg.getParameter<bool>("enable")),
    muons_token(consumes<pat::MuonCollection>(cfg.getParameter<edm::InputTag>("muons_src"))),
    electrons_token(consumes<pat::ElectronCollection>(cfg.getParameter<edm::InputTag>("electrons_src"))),
    vertex_ref_token(consumes<reco::VertexRefVector>(cfg.getParameter<edm::InputTag>("vertex_src"))),
    vertex_token(consumes<reco::VertexCollection>(cfg.getParameter<edm::InputTag>("vertex_src"))),
    input_is_refs(cfg.getParameter<bool>("input_is_refs")),
    min_vertex_track_weight(cfg.getParameter<double>("min_vertex_track_weight")),
    histos(cfg.getUntrackedParameter<bool>("histos", true)),
    verbose(cfg.getUntrackedParameter<bool>("verbose"))
{
  produces<MuAssociation>(mfv::muonsby_name);
  produces<ElAssociation>(mfv::electronsby_name);

  if(histos) {
    edm::Service<TFileService> fs;

    h_mutrack_dr = fs->make<TH1F>("h_mutrack_dr", ";dr between vertex tracks and muon;arb. units", 5000, -1.0, 4.0);
    h_mutrack_bestdr = fs->make<TH1F>("h_mutrack_bestdr", ";best dr between vertex tracks and muon;arb. units", 5000, -1.0, 4.0);
    h_eltrack_dr = fs->make<TH1F>("h_eltrack_dr", ";dr between vertex tracks and electron;arb. units", 5000, -1.0, 4.0);
    h_eltrack_bestdr = fs->make<TH1F>("h_eltrack_bestdr", ";best dr between vertex tracks and electron;arb. units", 5000, -1.0, 4.0);

    h_mu_vtx_miss_dist = fs->make<TH1F>("h_mu_vtx_miss_dist", ";miss dist between muon and vertex;arb. units", 100, 0, 0.5);
    h_ele_vtx_miss_dist = fs->make<TH1F>("h_ele_vtx_miss_dist", ";miss dist between electron and vertex;arb. units", 100, 0, 0.5);
    h_matchedmu_vtx_miss_dist = fs->make<TH1F>("h_matchedmu_vtx_miss_dist", ";miss dist between matched muon and vertex;arb. units", 100, 0, 0.5);
    h_matchedele_vtx_miss_dist = fs->make<TH1F>("h_matchedele_vtx_miss_dist", ";miss dist between matched electron and vertex;arb. units", 100, 0, 0.5);

  }
}


void MFVLeptonVertexAssociator::produce(edm::Event& event, const edm::EventSetup& setup) {
  edm::ESHandle<TransientTrackBuilder> tt_builder;
  setup.get<TransientTrackRecord>().get("TransientTrackBuilder", tt_builder);

  edm::Handle<pat::MuonCollection> muons;
  event.getByToken(muons_token, muons);

  edm::Handle<pat::ElectronCollection> electrons;
  event.getByToken(electrons_token, electrons);

  std::vector<reco::VertexRef> vertices;

  if (input_is_refs) {
    edm::Handle<reco::VertexRefVector> h;
    event.getByToken(vertex_ref_token, h);
    for (const reco::VertexRef& ref : *h)
      vertices.push_back(ref);
  }
  else {
    edm::Handle<reco::VertexCollection> h;
    event.getByToken(vertex_token, h);
    for (size_t i = 0; i < h->size(); ++i)
      vertices.push_back(reco::VertexRef(h, i));
  }

  const size_t n_muons = muons->size();
  const size_t n_electrons = electrons->size();
  const size_t n_vertices = vertices.size();

  if (verbose) {
    for (size_t ivtx = 0; ivtx < n_vertices; ++ivtx) {
      const reco::Vertex& vtx = *vertices.at(ivtx);
      printf("ivtx %lu ntracks %i mass %f\n", ivtx, vtx.nTracks(min_vertex_track_weight), vtx.p4().mass());
    }
  }

  // Associate leptons (muons and electrons) to vertices. For each 
  // lepton, determine if it matches to a track in a vertex. 
  //

  // Possible TODO :
  // Try taking closest in cos(angle between lepton momentum and
  // (TV-SV)), as well as the distance of closest approach ("miss
  // distance").

  // have the index == muon, but the value is which vertex the muon is
  // associated to (which starts at 0) 
  std::vector<int> mu_index_in_vertex(n_muons, -1);
  std::vector<int> el_index_in_vertex(n_electrons, -1);

// with this set up, it is possible that a muon could be associated to 
// more than one vertex -- have a printout set up but yet to cause an issue 
  if (enable) {
    if (verbose) printf("starting now to check leptons to tracks \n");      
    if (verbose) std::cout << "Nmuons: " << n_muons << " Nelectrons: " << n_electrons << std::endl;
    std::set<reco::TrackRef> mu_tracks;
    std::set<reco::TrackRef> el_tracks;
    std::vector<double> mu_dr;
    std::vector<std::vector<double>> mu_vtx_drpairs;
    std::vector<double> el_dr;
    std::vector<std::vector<double>> el_vtx_drpairs;
    std::pair<bool, Measurement1D> mu_vtx_dist;
    std::pair<bool, Measurement1D> ele_vtx_dist;
    std::vector<reco::TransientTrack> mu_ttracks;
    std::vector<reco::TransientTrack> ele_ttracks;
    std::pair<bool, Measurement1D> matchedmu_vtx_dist;
    std::pair<bool, Measurement1D> matchedele_vtx_dist;
    std::vector<reco::TransientTrack> matchedmu_ttracks;
    std::vector<reco::TransientTrack> matchedele_ttracks;

    for (size_t imuon = 0; imuon < n_muons; ++imuon) {
      const pat::Muon& muon = muons->at(imuon);
      //reco::TrackRef mtk = muon.globalTrack();
      reco::TrackRef mtk = muon.innerTrack();

      if (!mtk.isNull()) {
        mu_ttracks.push_back(tt_builder->build(mtk));
        for (size_t ivtx = 0; ivtx < n_vertices; ++ivtx) {
          std::vector<double> drpairs;
          const reco::Vertex& vtx = *vertices.at(ivtx);
          for (auto itk = vtx.tracks_begin(), itke = vtx.tracks_end(); itk != itke; ++itk) {
            if (vtx.trackWeight(*itk) >= min_vertex_track_weight) {
              reco::TrackRef tk = itk->castTo<reco::TrackRef>();

              if (mtk->pt() > 1) {
                double dr = reco::deltaR(tk->eta(), tk->phi(), mtk->eta(), mtk->phi());
                if (verbose) printf("tk pt %f eta %f phi %f in vtx %f,%f,%f \n", tk->pt(), tk->eta(), tk->phi(), vtx.x(), vtx.y(), vtx.z());
                if (verbose) printf("mu tk comparison : pt %f eta %f phi %f; dr : %f \n", mtk->pt(), mtk->eta(), mtk->phi(), dr);
                //filling the 1d vector & 2d vector 
                mu_dr.push_back(dr);
                drpairs.push_back(dr);
                if (dr < 0.001 ) {
                  mu_tracks.insert(tk);
                  matchedmu_ttracks.push_back(tt_builder->build(mtk));
                  if (mu_index_in_vertex[imuon] != -1) {
                    std::cout << "overwrite warning : found a muon attached to more than one vertex \n" << std::endl;
                  }
                  mu_index_in_vertex[imuon] = ivtx;
                }
              }
            }
          }
          mu_vtx_drpairs.push_back(drpairs);
        }
      }
    }

    if (verbose) printf("\n");
    for (size_t iel = 0; iel < n_electrons; ++iel) {
      const pat::Electron& electron = electrons->at(iel);
      reco::GsfTrackRef etk = electron.gsfTrack();
            
      if (!etk.isNull()) {
        ele_ttracks.push_back(tt_builder->build(etk));
        for (size_t ivtx = 0; ivtx < n_vertices; ++ivtx) {
          std::vector<double> drpairs;
          const reco::Vertex& vtx = *vertices.at(ivtx);
          for (auto itk = vtx.tracks_begin(), itke = vtx.tracks_end(); itk != itke; ++itk) {
            if (vtx.trackWeight(*itk) >= min_vertex_track_weight) {
              reco::TrackRef tk = itk->castTo<reco::TrackRef>();

              if (etk->pt() > 1) {
                double dr = reco::deltaR(tk->eta(), tk->phi(), etk->eta(), etk->phi());
                if (verbose) printf("tk pt %f eta %f phi %f in vtx %f,%f,%f \n", tk->pt(), tk->eta(), tk->phi(), vtx.x(), vtx.y(), vtx.z());
                if (verbose) printf("el tk comparison : pt %f eta %f phi %f; dr : %f \n", etk->pt(), etk->eta(), etk->phi(), dr);
                el_dr.push_back(dr);
                drpairs.push_back(dr);
                if (dr < 0.001 ) {
                  el_tracks.insert(tk);
                  matchedele_ttracks.push_back(tt_builder->build(etk));
                  if (el_index_in_vertex[iel] != -1) {
                    std::cout << "overwrite warning : found an electron attached to more than one vertex \n" << std::endl;
                  }
                  el_index_in_vertex[iel] = ivtx;
                }
              }
            }
          }
          el_vtx_drpairs.push_back(drpairs);
        }
      }
    }

    // finding transverse impact parameter between leptons and vertices 
    for (size_t ivtx = 0; ivtx < n_vertices; ++ivtx) {
      const reco::Vertex& vtx = *vertices.at(ivtx);
      for (auto ettk : ele_ttracks ) {
        ele_vtx_dist = IPTools::absoluteTransverseImpactParameter(ettk, vtx);
      }
      for (auto mettk : matchedele_ttracks ) {
        matchedele_vtx_dist = IPTools::absoluteTransverseImpactParameter(mettk, vtx);
       }
      for (auto mttk : mu_ttracks ) {
        mu_vtx_dist = IPTools::absoluteTransverseImpactParameter(mttk, vtx);
       }
      for (auto mmttk : matchedmu_ttracks ) {
        matchedmu_vtx_dist = IPTools::absoluteTransverseImpactParameter(mmttk, vtx);
      }
    }

    if (histos) {
      for (auto mu_deltaR : mu_dr ) {
        h_mutrack_dr->Fill(mu_deltaR);
      }
      
      for (auto el_deltaR : el_dr ) {
        h_eltrack_dr->Fill(el_deltaR);
      }
      
      for (auto& outer : mu_vtx_drpairs) {
        if (!outer.empty()) {
          auto min = std::min_element(outer.begin(), outer.end());
          h_mutrack_bestdr->Fill(*min);
        }
      }

      for (auto& outer : el_vtx_drpairs) {
        if (!outer.empty()) {
          auto min = std::min_element(outer.begin(), outer.end());
          h_eltrack_bestdr->Fill(*min);
        }
      }

      h_mu_vtx_miss_dist->Fill(mu_vtx_dist.second.value());
      h_ele_vtx_miss_dist->Fill(ele_vtx_dist.second.value());
      h_matchedmu_vtx_miss_dist->Fill(matchedmu_vtx_dist.second.value());
      h_matchedele_vtx_miss_dist->Fill(matchedele_vtx_dist.second.value());
   }
  }


  std::unique_ptr<MuAssociation> mu_assoc;
  mu_assoc.reset(new MuAssociation(&event.productGetter()));

  std::unique_ptr<ElAssociation> el_assoc;
  el_assoc.reset(new ElAssociation(&event.productGetter()));


  if (enable) {
    for (size_t ivtx = 0; ivtx < n_vertices; ++ivtx) {
      reco::VertexRef vtxref = vertices.at(ivtx);

      for (size_t imuon = 0; imuon < n_muons; ++imuon) {
        pat::MuonRef muonref(muons, imuon);

        if (mu_index_in_vertex[imuon] == int(ivtx)) {
          mu_assoc->insert(vtxref, muonref);
        }
      }

      for (size_t iel = 0; iel < n_electrons; ++iel) {
        pat::ElectronRef eleref(electrons, iel);

        if (el_index_in_vertex[iel] == int(ivtx)) {
          el_assoc->insert(vtxref, eleref);
        }
      }
    }
  }

  event.put(std::move(mu_assoc), mfv::muonsby_name);
  event.put(std::move(el_assoc), mfv::electronsby_name);
  
}

DEFINE_FWK_MODULE(MFVLeptonVertexAssociator);
