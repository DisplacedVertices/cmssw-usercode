#include "DataFormats/PatCandidates/interface/PackedCandidate.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "JMTucker/Formats/interface/TracksMap.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/PatCandidates/interface/Muon.h"

class JMTUnpackedCandidateTracks : public edm::EDProducer {
public:
  explicit JMTUnpackedCandidateTracks(const edm::ParameterSet&);
  virtual void produce(edm::Event&, const edm::EventSetup&);
private:
  const edm::EDGetTokenT<pat::PackedCandidateCollection> packed_candidates_token;
  const edm::EDGetTokenT<pat::MuonCollection> muons_token;
  const edm::EDGetTokenT<pat::ElectronCollection> electrons_token;
  const bool remove_lepton_overlap;
  const bool add_lost_candidates;
  const edm::EDGetTokenT<pat::PackedCandidateCollection> lost_candidates_token;
  const int cut_level;
  const bool skip_weirdos;
  const bool debug;

  void debug_cand(const pat::PackedCandidate& cand, const char* tag, const size_t i) const {
    std::cout << tag << " cand #" << i << " id " << cand.pdgId() << " pt " << cand.pt() << " eta " << cand.eta() << " charge " << cand.charge() << " hasTrackDetails? " << cand.hasTrackDetails() << " ";
  }

  void debug_tk(const reco::Track& tk, const char* tag, const size_t i) const {
    std::cout << "-> " << tag << " track #" << i << " pt " << tk.pt() << " eta " << tk.eta() << " min_r? " << tk.hitPattern().hasValidHitInPixelLayer(PixelSubdetector::PixelBarrel,1)
              << " npxlayers " << tk.hitPattern().pixelLayersWithMeasurement() << " nstlayers " << tk.hitPattern().stripLayersWithMeasurement() << " dxy " << tk.dxy() << " +- " << tk.dxyError() << " pass? " << pass_tk(tk);
  };

  bool pass_cand(const pat::PackedCandidate& cand) const {
    if (cand.charge() && cand.hasTrackDetails()) {
      if (skip_weirdos || debug) {
        const reco::Track& tk = cand.pseudoTrack();
        union U { float f; int i; } u;
        u.f = tk.dxyError();
        const bool weirdo =
          u.i == 0x3b8c70c2 ||  // 0.0042859027
          u.i == 0x3c060959 ||  // 0.0081809396
          u.i == 0x3cd24697 ||  // 0.0256684255
          u.i == 0x3dfc7c28 ||  // 0.1232836843
          u.i == 0x3e948f67;    // 0.2901565731
        if (debug) printf("(weirdo check %i %i %i %i 0x%08x %.10g) ", weirdo, pass_tk(tk,true,false,false), pass_tk(tk,true,true,false), pass_tk(tk,true,true,true), u.i, u.f);
        if (skip_weirdos && weirdo) return false;
      }
      return true;
    }
    return false;
  }


  bool pass_tk(const reco::Track& tk, bool req_base, bool req_min_r, bool req_nsigmadxy) const {
    return
      (!req_base || (tk.pt() >= 1 && tk.hitPattern().pixelLayersWithMeasurement() >= 2 && tk.hitPattern().stripLayersWithMeasurement() >= 6)) &&
      (!req_min_r || tk.hitPattern().hasValidHitInPixelLayer(PixelSubdetector::PixelBarrel,1)) &&
      (!req_nsigmadxy || fabs(tk.dxy() / tk.dxyError()) > 4);
  }

  bool pass_tk(const reco::Track& tk) const { return pass_tk(tk, cut_level >= 0, cut_level >= 1, cut_level >= 2); }


  //specific requirements for lepton tracks : 
  //noLostInnerHits : takes into account geometrical or detector inefficiencies (i.e. the hit wasn't expected to be there)
    bool pass_leptk(const reco::Track& tk, bool req_base, bool req_min_r, bool req_nsigmadxy) const {
    return
      (!req_base || (tk.pt() >= 1 && tk.hitPattern().pixelLayersWithMeasurement() >= 2 && tk.hitPattern().stripLayersWithMeasurement() >= 6)) &&
      (!req_min_r || (tk.hitPattern().hasValidHitInPixelLayer(PixelSubdetector::PixelBarrel,2) && tk.hitPattern().numberOfLostHits(reco::HitPattern::MISSING_INNER_HITS)==0)) &&
      (!req_nsigmadxy || fabs(tk.dxy() / tk.dxyError()) > 3);
  }

  bool pass_leptk(const reco::Track& tk) const { return pass_leptk(tk, cut_level >= 0, cut_level >= 1, cut_level >= 2); }


  unsigned encode_vertex_ref(const pat::PackedCandidate& c) {
    unsigned k = c.vertexRef().key();
    if (k == unsigned(-1)) return k;
    assert((k & (0x7 << 29)) == 0);
    unsigned q = c.pvAssociationQuality();
    assert(q < 8);
    return k & (q << 29);
  }
};

JMTUnpackedCandidateTracks::JMTUnpackedCandidateTracks(const edm::ParameterSet& cfg)
  : packed_candidates_token(consumes<pat::PackedCandidateCollection>(cfg.getParameter<edm::InputTag>("packed_candidates_src"))),
    muons_token(consumes<pat::MuonCollection>(cfg.getParameter<edm::InputTag>("muons_src"))),
    electrons_token(consumes<pat::ElectronCollection>(cfg.getParameter<edm::InputTag>("electrons_src"))),
    remove_lepton_overlap(cfg.getParameter<bool>("separate_leptons")),
    add_lost_candidates(cfg.getParameter<bool>("add_lost_candidates")),
    lost_candidates_token(consumes<pat::PackedCandidateCollection>(cfg.getParameter<edm::InputTag>("lost_candidates_src"))),
    cut_level(cfg.getParameter<int>("cut_level")),
    skip_weirdos(cfg.getParameter<bool>("skip_weirdos")),
    debug(cfg.getUntrackedParameter<bool>("debug", false))
{
  produces<reco::TrackCollection>();
  produces<reco::TrackCollection>("lost");
  produces<jmt::UnpackedCandidateTracksMap>();
  produces<reco::TrackCollection>("electrons");
  produces<reco::TrackCollection>("muons");
  produces<jmt::UnpackedCandidateTracksMap>("elemap");
  produces<jmt::UnpackedCandidateTracksMap>("mumap");
  produces<std::vector<unsigned>>(); // which PV
  produces<std::vector<unsigned>>("lost");
}

void JMTUnpackedCandidateTracks::produce(edm::Event& event, const edm::EventSetup& setup) {
  if (debug) std::cout << "JMTUnpackedCandidateTracks::produce: run " << event.id().run() << " lumi " << event.luminosityBlock() << " event " << event.id().event() << "\n";

  edm::Handle<pat::PackedCandidateCollection> packed_candidates;
  event.getByToken(packed_candidates_token, packed_candidates);

  edm::Handle<pat::MuonCollection> muons;
  event.getByToken(muons_token, muons);

  edm::Handle<pat::ElectronCollection> electrons;
  event.getByToken(electrons_token, electrons);

  auto tracks = std::make_unique<reco::TrackCollection>();
  auto lost_tracks = std::make_unique<reco::TrackCollection>();
  auto tracks_map = std::make_unique<jmt::UnpackedCandidateTracksMap>();
  auto ele_tracks = std::make_unique<reco::TrackCollection>();
  auto mu_tracks = std::make_unique<reco::TrackCollection>();
  auto ele_tracks_map = std::make_unique<jmt::UnpackedCandidateTracksMap>();
  auto mu_tracks_map = std::make_unique<jmt::UnpackedCandidateTracksMap>();
  auto tracks_pvs = std::make_unique<std::vector<unsigned>>();
  auto lost_tracks_pvs = std::make_unique<std::vector<unsigned>>();

  reco::TrackRefProd h_output_tracks = event.getRefBeforePut<reco::TrackCollection>();
  reco::TrackRefProd h_output_mu_tracks = event.getRefBeforePut<reco::TrackCollection>();
  reco::TrackRefProd h_output_ele_tracks = event.getRefBeforePut<reco::TrackCollection>();


  int ntkpass = 0, nlosttkpass = 0, nmtkpass=0, netkpass=0;

  //https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookMiniAOD2014#Packed_ParticleFlow_Candidates

  //going to do this twice; once for electrons, once for muons ... 
  std::vector<const reco::Candidate *> mu_cand;
  std::vector<const reco::Candidate *> ele_cand;
  for (const pat::Muon &mu : *muons) mu_cand.push_back(&mu);
  for (const pat::Electron &el : *electrons) ele_cand.push_back(&el);

  std::vector<int> eidx_toremove;
  std::vector<int> midx_toremove;

  for (const reco::Candidate *muon : mu_cand) {
    // get a list of the PF candidates used to build this lepton, so to exclude them
    std::vector<reco::CandidatePtr> mu_footprint;
    for (unsigned int i = 0, n = muon->numberOfSourceCandidatePtrs(); i < n; ++i) {
      mu_footprint.push_back(muon->sourceCandidatePtr(i));
    }
    // now loop on pf candidates
    for (unsigned int i = 0, n = packed_candidates->size(); i < n; ++i) {
      const pat::PackedCandidate &cand = (*packed_candidates)[i];
      if (deltaR(cand,*muon) < 0.2) {
        // pfcandidate-based footprint removal
        if (std::find(mu_footprint.begin(), mu_footprint.end(), reco::CandidatePtr(packed_candidates,i)) != mu_footprint.end()) {
          midx_toremove.push_back(i);
          continue;
        }
      }
    }
  }
  for (const reco::Candidate *electron : ele_cand) {
    // get a list of the PF candidates used to build this lepton, so to exclude them
    std::vector<reco::CandidatePtr> ele_footprint;
    for (unsigned int i = 0, n = electron->numberOfSourceCandidatePtrs(); i < n; ++i) {
      ele_footprint.push_back(electron->sourceCandidatePtr(i));
    }
    // now loop on pf candidates
    for (unsigned int i = 0, n = packed_candidates->size(); i < n; ++i) {
      const pat::PackedCandidate &cand = (*packed_candidates)[i];
      if (deltaR(cand,*electron) < 0.2) {
        // pfcandidate-based footprint removal
        if (std::find(ele_footprint.begin(), ele_footprint.end(), reco::CandidatePtr(packed_candidates,i)) != ele_footprint.end()) {
          eidx_toremove.push_back(i);
          continue;
        }
      }
    }
  }

  for (int i = 0, n = packed_candidates->size(); i < n; ++i) {
    const pat::PackedCandidate& cand = (*packed_candidates)[i];
    if (separate_leptons) {

      if (std::find(midx_toremove.begin(), midx_toremove.end(), i) != midx_toremove.end()) {
        if (pass_cand(cand)) {
          const reco::Track& mtk = cand.pseudoTrack();
          if (debug) debug_tk(mtk, "", mu_tracks->size());

          if (pass_leptk(mtk)) {
            ++nmtkpass;
            mu_tracks->push_back(mtk);
            mu_tracks_map->insert(reco::CandidatePtr(packed_candidates, i), reco::TrackRef(h_output_mu_tracks, mu_tracks->size() - 1));
            tracks_pvs->push_back(encode_vertex_ref(cand));
          }
        }
        continue;
      }

      else if (std::find(eidx_toremove.begin(), eidx_toremove.end(), i) != eidx_toremove.end()) {
        if (pass_cand(cand)) {
          const reco::Track& etk = cand.pseudoTrack();
          if (debug) debug_tk(etk, "", ele_tracks->size());

          if (pass_leptk(etk)) {
            ++ntkpass;
            ele_tracks->push_back(etk);
            ele_tracks_map->insert(reco::CandidatePtr(packed_candidates, i), reco::TrackRef(h_output_ele_tracks, ele_tracks->size() - 1));
            tracks_pvs->push_back(encode_vertex_ref(cand));
          }
        }
        continue;
      }
    }
    if (debug) debug_cand(cand, "", i);

    if (pass_cand(cand)) {
      const reco::Track& tk = cand.pseudoTrack();
      if (debug) debug_tk(tk, "", tracks->size());

      if (pass_tk(tk)) {
        ++ntkpass;
        tracks->push_back(tk);
        tracks_map->insert(reco::CandidatePtr(packed_candidates, i), reco::TrackRef(h_output_tracks, tracks->size() - 1));
        tracks_pvs->push_back(encode_vertex_ref(cand));
      }
    }

    if (debug) std::cout << "\n";
  }

  edm::Handle<pat::PackedCandidateCollection> lost_candidates;
  event.getByToken(lost_candidates_token, lost_candidates);

  for (size_t i = 0, ie = lost_candidates->size(); i < ie; ++i) {
    const pat::PackedCandidate& cand = (*lost_candidates)[i];
    if (debug) debug_cand(cand, "lost", i);

    if (pass_cand(cand)) {
      const reco::Track& tk = cand.pseudoTrack();
      if (debug) debug_tk(tk, "lost", lost_tracks->size());

      if (pass_tk(tk)) {
        ++nlosttkpass;

        if (add_lost_candidates) {
          tracks->push_back(tk);
          tracks_map->insert(reco::CandidatePtr(lost_candidates, i), reco::TrackRef(h_output_tracks, tracks->size() - 1));
          tracks_pvs->push_back(encode_vertex_ref(cand));
        }

        lost_tracks->push_back(tk);
        lost_tracks_pvs->push_back(encode_vertex_ref(cand));
      }
    }

    if (debug) std::cout << "\n";
  }

  if (debug) std::cout << "JMTUnpackedCandidateTracks::produce: npass/ntk = " << ntkpass << " / " << tracks->size() << " npass/nlost = " << nlosttkpass << " / " << lost_tracks->size() << "\n";
  if (debug) std::cout << "JMTUnpackedCandidateTracks::produce: nmupass/nmtk = " << nmtkpass << " / " << mu_tracks->size() << " nelepass/netk = " << netkpass << " / " << ele_tracks->size() << "\n";

  event.put(std::move(tracks));
  if (separate_leptons) {
    event.put(std::move(ele_tracks), "electrons");
    event.put(std::move(mu_tracks), "muons");
    event.put(std::move(ele_tracks_map), "elemap");
    event.put(std::move(mu_tracks_map), "mumap");
  }
  event.put(std::move(lost_tracks), "lost");
  event.put(std::move(tracks_map));
  event.put(std::move(tracks_pvs));
  event.put(std::move(lost_tracks_pvs));
}

DEFINE_FWK_MODULE(JMTUnpackedCandidateTracks);