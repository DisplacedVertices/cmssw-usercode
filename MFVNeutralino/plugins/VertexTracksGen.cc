#include "TH2.h"
#include "CLHEP/Random/RandBinomial.h"
#include "CLHEP/Random/RandomEngine.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/JetReco/interface/PFJetCollection.h"
#include "DataFormats/JetReco/interface/GenJet.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/PackedCandidate.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "FWCore/Utilities/interface/RandomNumberGenerator.h"
#include "TrackingTools/IPTools/interface/IPTools.h"
#include "TrackingTools/Records/interface/TransientTrackRecord.h"
#include "TrackingTools/TransientTrack/interface/TransientTrack.h"
#include "TrackingTools/TransientTrack/interface/TransientTrackBuilder.h"
#include "JMTucker/Tools/interface/AnalysisEras.h"
#include "JMTucker/Tools/interface/TrackRescaler.h"
#include "JMTucker/MFVNeutralinoFormats/interface/MCInteractions.h"

class MFVVertexTracksGen : public edm::EDFilter {
  public:
    MFVVertexTracksGen(const edm::ParameterSet&);
    virtual bool filter(edm::Event&, const edm::EventSetup&);

  private:
    void visitdaughters(const reco::Candidate* dau, int whichLLP, int rank=0){
      if(verbose)
        std::cout << "  rank "<<rank<<"  id " << dau->pdgId() << " status " << dau->status() << " isjet " << dau->isJet() << " pt " << dau->pt() << " eta " << dau->eta() << " phi " << dau->phi() << std::endl;
      if (dau->numberOfDaughters()){
        if(verbose)
          std::cout << "daughter of " << dau->pdgId() << std::endl;
        for (size_t i=0; i<dau->numberOfDaughters(); ++i){
          visitdaughters(dau->daughter(i), whichLLP, rank+1);
        }
      }
      else{
        if (verbose)
          std::cout << "final particle" << std::endl;
        if ( (dau->status()<=3) || ( (dau->status()>=21) && (dau->status()<=29) ) || ( (dau->status()>=11) && (dau->status()<=19) ) )
          LLP_daus[whichLLP].insert(dau);
      }
    }

    bool match_track_jet(const reco::Track& tk, const pat::Jet& jet);

    //const edm::EDGetTokenT<std::vector<double>> genvtx_token;
    const edm::EDGetTokenT<reco::BeamSpot> beamspot_token;
    const edm::EDGetTokenT<reco::VertexCollection> primary_vertices_token;
    const edm::EDGetTokenT<reco::TrackCollection> tracks_token;
    const edm::EDGetTokenT<mfv::MCInteraction> mci_token;
    bool track_gen_matching;
    bool jet_gen_matching;
    bool track_genjet_matching;
    const edm::EDGetTokenT<pat::JetCollection> jets_token;
    const edm::EDGetTokenT<reco::GenJetCollection> gen_jets_token;

    const int min_n_seed_tracks;
    const double min_track_pt;
    const int min_track_hit_r;
    const int min_track_nhits;
    const int min_track_npxhits;
    const int min_track_npxlayers;
    const int min_track_nstlayers;
    const double track_genjet_match_thres;
    const double min_genparticle_pt;
    std::set<const reco::Candidate*> LLP_daus[2];

    bool verbose;
    bool histos;

    TH1F* h_n_seed_tracks;
    TH1F* h_n_matched_jets;
    TH1F* h_seed_track_sigmadxybs;
    TH1F* h_seed_track_nhits;
    TH1F* h_seed_track_npxhits;
    TH1F* h_seed_track_nsthits;
    TH1F* h_seed_track_npxlayers;
    TH1F* h_seed_track_nstlayers;
};

MFVVertexTracksGen::MFVVertexTracksGen(const edm::ParameterSet& cfg)
  : //genvtx_token(consumes<std::vector<double>>(cfg.getParameter<edm::InputTag>("genvtx_src"))),
    beamspot_token(consumes<reco::BeamSpot>(cfg.getParameter<edm::InputTag>("beamspot_src"))),
    tracks_token(consumes<reco::TrackCollection>(cfg.getParameter<edm::InputTag>("tracks_src"))),
    mci_token(consumes<mfv::MCInteraction>(cfg.getParameter<edm::InputTag>("mci_src"))),
    track_gen_matching(cfg.getParameter<bool>("track_gen_matching")),
    jet_gen_matching(cfg.getParameter<bool>("jet_gen_matching")),
    track_genjet_matching(cfg.getParameter<bool>("track_genjet_matching")),
    jets_token(jet_gen_matching ? consumes<pat::JetCollection>(cfg.getParameter<edm::InputTag>("jets_src")) : edm::EDGetTokenT<pat::JetCollection>()),
    gen_jets_token(track_genjet_matching ? consumes<reco::GenJetCollection>(cfg.getParameter<edm::InputTag>("gen_jets_src")) : edm::EDGetTokenT<reco::GenJetCollection>()),
    min_n_seed_tracks(cfg.getParameter<int>("min_n_seed_tracks")),
    min_track_pt(cfg.getParameter<double>("min_track_pt")),
    min_track_hit_r(cfg.getParameter<int>("min_track_hit_r")),
    min_track_nhits(cfg.getParameter<int>("min_track_nhits")),
    min_track_npxhits(cfg.getParameter<int>("min_track_npxhits")),
    min_track_npxlayers(cfg.getParameter<int>("min_track_npxlayers")),
    min_track_nstlayers(cfg.getParameter<int>("min_track_nstlayers")),
    track_genjet_match_thres(cfg.getParameter<double>("track_genjet_match_thres")),
    min_genparticle_pt(cfg.getParameter<double>("min_genparticle_pt")),
    verbose(cfg.getUntrackedParameter<bool>("verbose")),
    histos(cfg.getUntrackedParameter<bool>("histos"))
{
  if(int(track_gen_matching) + int(jet_gen_matching) + int(track_genjet_matching)>1)
    throw cms::Exception("MFVVertexTracksGen") << "track_gen_matching and jet_gen_matching can't both be true";

  produces<std::vector<reco::TrackRef>>("seed");
  produces<reco::TrackCollection>("seed");

  if (histos) {
    edm::Service<TFileService> fs;
    h_n_seed_tracks         = fs->make<TH1F>("h_n_seed_tracks",         "", 200,  0,200);
    h_n_matched_jets        = fs->make<TH1F>("h_n_matched_jets",        "", 10,   0, 10);
    h_seed_track_sigmadxybs = fs->make<TH1F>("h_seed_track_sigmadxybs", "", 40, -10, 10);
    h_seed_track_nhits      = fs->make<TH1F>("h_seed_track_nhits",      "", 40,   0, 40);
    h_seed_track_npxhits    = fs->make<TH1F>("h_seed_track_npxhits",    "", 12,   0, 12);
    h_seed_track_nsthits    = fs->make<TH1F>("h_seed_track_nsthits",    "", 28,   0, 28);
    h_seed_track_npxlayers  = fs->make<TH1F>("h_seed_track_npxlayers",  "", 10,   0, 10);
    h_seed_track_nstlayers  = fs->make<TH1F>("h_seed_track_nstlayers",  "", 30,   0, 30);

  }
}

bool MFVVertexTracksGen::filter(edm::Event& event, const edm::EventSetup& setup) {
  if (verbose)
    std::cout << "MFVVertexTracksGen:: event id: " << event.id().event() << std::endl;
  
  LLP_daus[0].clear();
  LLP_daus[1].clear();

  edm::Handle<reco::BeamSpot> beamspot;
  event.getByToken(beamspot_token, beamspot);

  //edm::Handle<std::vector<double>> gen_vertex;
  //event.getByToken(genvtx_token, gen_vertex);
  //std::vector<reco::Vertex> genv;
  //for (size_t i=0; i<2; ++i){
  //  const double x = (*gen_vertex)[i*3+0];
  //  const double y = (*gen_vertex)[i*3+1];
  //  const double z = (*gen_vertex)[i*3+2];
  //  math::Error<3>::type e;
  //  math::XYZPoint p(x, y, z);
  //  reco::Vertex vg(p,e);
  //  genv.push_back(vg);
  //  evInfo->gen_vtx_x.push_back(x);
  //  evInfo->gen_vtx_y.push_back(y);
  //  evInfo->gen_vtx_z.push_back(z);
  //}

  std::unique_ptr<std::vector<reco::TrackRef>> seed_tracks(new std::vector<reco::TrackRef>);
  std::unique_ptr<reco::TrackCollection> seed_tracks_copy(new reco::TrackCollection);

  edm::Handle<pat::JetCollection> jets;
  if (jet_gen_matching){
    event.getByToken(jets_token, jets);
  }

  edm::Handle<reco::GenJetCollection> gen_jets;
  if (track_genjet_matching){
    event.getByToken(gen_jets_token, gen_jets);
  }

  std::set<size_t> matched_jets;
  edm::Handle<mfv::MCInteraction> mci;
  event.getByToken(mci_token, mci);
  if (mci->valid()){
    assert(mci->primaries().size() == 2);
    for (int i=0; i<2; ++i){
      auto secondaries = mci->secondaries(i);
      if(verbose)
        std::cout << "LLP " << i << std::endl;
      for (unsigned int i_secondary = 0; i_secondary < secondaries.size(); ++i_secondary){
        const reco::GenParticleRef& s = secondaries[i_secondary];
        if (verbose)
          std::cout << "LLP secondary " << s->pdgId() << " status " << s->status() << " isJet " << s->isJet() << " pt " << s->pt() << " eta " << s->eta() << " phi " << s->phi() << std::endl;

        if (track_gen_matching){
          if (s->pdgId()!=1000022)
            LLP_daus[i].insert(&*s);
        }
        else if (jet_gen_matching){
          if (s->pdgId()==1000022)
            continue;
          for (size_t j=0; j<jets->size(); ++j){
          //for (const auto& jet : *jets){
            const pat::Jet& jet = (*jets)[j];
            if (reco::deltaR2(jet, *s)<0.16){
              matched_jets.insert(j);
              if (verbose)
                std::cout << "  jet matched: dR2 " << reco::deltaR2(jet, *s) << " pt " << jet.pt() << " eta " << jet.eta() << " phi " << jet.phi() << std::endl; 
            }
          }
        }
        else if (track_genjet_matching){
          if (s->pdgId()==1000022)
            continue;
          for (size_t j=0; j<gen_jets->size(); ++j){
            if (matched_jets.count(j)==1) continue;
            const reco::GenJet& jet = (*gen_jets)[j];
            if (jet.pt() > 20 && fabs(jet.eta()) < 2.5 && reco::deltaR2(jet, *s)<0.16) {
              matched_jets.insert(j);
              if (verbose)
                std::cout << "  jet matched: dR2 " << reco::deltaR2(jet, *s) << " pt " << jet.pt() << " eta " << jet.eta() << " phi " << jet.phi() << " with constituents " << jet.getJetConstituents().size() << std::endl; 
              for (auto c : jet.getJetConstituents()){
                std::cout << "genjet cons position x " << c->vx() << " y " << c->vy() << " z " << c->vz() << std::endl;
                if (c->pt()<min_genparticle_pt) continue;
                LLP_daus[i].insert(&*c);
                if (verbose)
                  std::cout << "added constituent pdgid " << c->pdgId() << " pt " << c->pt() << " eta " << c->eta() << " phi " << c->phi() << std::endl;
              }
            }
          }      
        }
        if (track_gen_matching){
          //if(abs(s->pdgId()) != 5 && abs(s->pdgId()) != 24){
          if (1){
            for(unsigned int i_dau = 0; i_dau < s->numberOfDaughters(); ++i_dau){
              auto dau = s->daughter(i_dau);
              visitdaughters(dau,i);
            }
          }
        }
      }
    }
  }
  if(verbose){
    if (track_gen_matching || track_genjet_matching){
      std::cout << "LLP0 final daughter:" << LLP_daus[0].size()<<std::endl;
      for (const auto&dau:LLP_daus[0]){
        std::cout << " pdgid " << dau->pdgId() << " pt " << dau->pt() << " eta " << dau->eta() << " phi " << dau->phi() << std::endl;
      }
      std::cout << "LLP final daughter:" << LLP_daus[1].size()<<std::endl;
      for (const auto&dau:LLP_daus[1]){
        std::cout << " pdgid " << dau->pdgId() << " pt " << dau->pt() << " eta " << dau->eta() << " phi " << dau->phi() << std::endl;
      }
    }
    if (jet_gen_matching || track_genjet_matching){
      std::cout << "Jets matched with LLP secondaries: " << matched_jets.size() << std::endl;
      for (const auto& j:matched_jets){
        if (jet_gen_matching){
          const pat::Jet& jet = (*jets)[j];
          std::cout << " pt " << jet.pt() << " eta " << jet.eta() << " phi " << jet.phi() << std::endl;
        }
        if (track_genjet_matching){
          const reco::GenJet& jet = (*gen_jets)[j];
          std::cout << " pt " << jet.pt() << " eta " << jet.eta() << " phi " << jet.phi() << std::endl;
        }
      }
    }
  }

  edm::Handle<reco::TrackCollection> tracks;
  event.getByToken(tracks_token, tracks);
  for (size_t i = 0, ie = tracks->size(); i < ie; ++i){
    const reco::TrackRef& tk = reco::TrackRef(tracks, i);

    const double pt = tk->pt();
    const double dxybs = tk->dxy(*beamspot);
    const double dxyerr = tk->dxyError();
    const double sigmadxybs = dxybs / dxyerr;

    const int nhits = tk->hitPattern().numberOfValidHits();
    const int npxhits = tk->hitPattern().numberOfValidPixelHits();
    const int nsthits = tk->hitPattern().numberOfValidStripHits();
    const int npxlayers = tk->hitPattern().pixelLayersWithMeasurement();
    const int nstlayers = tk->hitPattern().stripLayersWithMeasurement();
    int min_r = 2000000000;
    for (int i = 1; i <= 4; ++i)
      if (tk->hitPattern().hasValidHitInPixelLayer(PixelSubdetector::PixelBarrel,i)) {
        min_r = i;
        break;
      }

    bool use = [&]() {

      const bool use_cheap =
        pt > min_track_pt &&
        nhits >= min_track_nhits &&
        npxhits >= min_track_npxhits &&
        npxlayers >= min_track_npxlayers &&
        nstlayers >= min_track_nstlayers &&
        (min_track_hit_r == 999 || min_r <= min_track_hit_r);

      if (!use_cheap) return false;

      return true;
    }();

    if (!use)
      continue;

    if (track_gen_matching || track_genjet_matching){
      double match_thres = 0.16;
      if (track_genjet_matching)
        match_thres = track_genjet_match_thres;
      bool match[2] = {false, false};
      for (int illp=0; illp<2; ++illp){
        for(const auto& dau:LLP_daus[illp]){
          if ((track_gen_matching)&&(dau->pdgId()!=21)&&(dau->pdgId()>=10))
            continue;
          double dr2 = reco::deltaR2(tk->eta(), tk->phi(), dau->eta(), dau->phi());
          if (dr2<match_thres){
            match[illp] = true;
            break;
          }
        }
      }
      if (match[0]||match[1]){
        seed_tracks->push_back(tk);
        seed_tracks_copy->push_back(*tk);
        if(histos){
          h_seed_track_sigmadxybs->Fill(sigmadxybs);
          h_seed_track_nhits->Fill(nhits);
          h_seed_track_npxhits->Fill(npxhits);
          h_seed_track_nsthits->Fill(nsthits);
          h_seed_track_npxlayers->Fill(npxlayers);
          h_seed_track_nstlayers->Fill(nstlayers);
        }
      }
    }

    if (jet_gen_matching){
      for (const auto& j:matched_jets){
        const pat::Jet& jet = (*jets)[j];
        if (match_track_jet(*tk, jet)){
          seed_tracks->push_back(tk);
          seed_tracks_copy->push_back(*tk);
          if(histos){
            h_seed_track_sigmadxybs->Fill(sigmadxybs);
            h_seed_track_nhits->Fill(nhits);
            h_seed_track_npxhits->Fill(npxhits);
            h_seed_track_nsthits->Fill(nsthits);
            h_seed_track_npxlayers->Fill(npxlayers);
            h_seed_track_nstlayers->Fill(nstlayers);
          }
          if (verbose)
            std::cout << "  matched track pt " << tk->pt() << " eta " << tk->eta() << " phi " << tk->phi() << std::endl;
          break;
        }
      }
    }
  }
  if (histos){
    if (jet_gen_matching || track_genjet_matching)
      h_n_matched_jets->Fill(matched_jets.size());
    else
      h_n_matched_jets->Fill(-1);
    h_n_seed_tracks->Fill(seed_tracks->size());
  }
  const bool pass_min_n_seed_tracks = int(seed_tracks->size()) >= min_n_seed_tracks;

  event.put(std::move(seed_tracks), "seed");
  event.put(std::move(seed_tracks_copy), "seed");

  return pass_min_n_seed_tracks;
}

bool MFVVertexTracksGen::match_track_jet(const reco::Track& tk, const pat::Jet& jet){
  if (reco::deltaR2(tk, jet)>0.16) return false;
  //if (verbose){
  //  std::cout << "jet track matching..." << std::endl;
  //  std::cout << "  target track pt " << tk.pt() << " eta " << tk.eta() << " phi " << tk.phi() << std::endl;
  //}
  double match_thres = 1.3;
  for (size_t idau = 0, idaue = jet.numberOfDaughters(); idau < idaue; ++idau) {
    const reco::Candidate* dau = jet.daughter(idau);
    if (dau->charge() == 0)
      continue;
    const reco::Track* jtk = 0;
    const reco::PFCandidate* pf = dynamic_cast<const reco::PFCandidate*>(dau);
    if (pf) {
      const reco::TrackRef& r = pf->trackRef();
      if (r.isNonnull())
        jtk = &*r;
    }
    else {
      const pat::PackedCandidate* pk = dynamic_cast<const pat::PackedCandidate*>(dau);
      if (pk && pk->charge() && pk->hasTrackDetails())
        jtk = &pk->pseudoTrack();
    }
    if (jtk){
      double a = fabs(tk.pt()-jtk->pt())+1;
      double b = fabs(tk.eta()-jtk->eta())+1;
      double c = fabs(tk.phi()-jtk->phi())+1;
      //if (verbose)
      //  std::cout << "  jet track pt " << jtk->pt() << " eta " << jtk->eta() << " phi " << jtk->phi() << " match abc " << a*b*c << std::endl;
      if (a*b*c < match_thres){
        return true;
      }
    }
  }
  return false;
}

DEFINE_FWK_MODULE(MFVVertexTracksGen);
