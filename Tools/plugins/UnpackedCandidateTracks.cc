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
  const bool separate_leptons;
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
      (!req_min_r || (tk.hitPattern().hasValidHitInPixelLayer(PixelSubdetector::PixelBarrel,1) || (tk.hitPattern().hasValidHitInPixelLayer(PixelSubdetector::PixelBarrel,2) && tk.hitPattern().numberOfLostHits(reco::HitPattern::MISSING_INNER_HITS)==0))) &&
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
    separate_leptons(cfg.getParameter<bool>("separate_leptons")),
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
  produces<reco::TrackCollection>("tightele");
  produces<reco::TrackCollection>("medmu");
}

void JMTUnpackedCandidateTracks::produce(edm::Event& event, const edm::EventSetup& setup) {
  if (debug) std::cout << "JMTUnpackedCandidateTracks::produce: run " << event.id().run() << " lumi " << event.luminosityBlock() << " event " << event.id().event() << "\n";

  edm::Handle<pat::PackedCandidateCollection> packed_candidates;
  event.getByToken(packed_candidates_token, packed_candidates);

  edm::Handle<pat::PackedCandidateCollection> lost_candidates;
  event.getByToken(lost_candidates_token, lost_candidates);

  edm::Handle<pat::MuonCollection> muons;
  event.getByToken(muons_token, muons);

  edm::Handle<pat::ElectronCollection> electrons;
  event.getByToken(electrons_token, electrons);

  auto tracks = std::make_unique<reco::TrackCollection>();
  auto lost_tracks = std::make_unique<reco::TrackCollection>();
  auto tracks_map = std::make_unique<jmt::UnpackedCandidateTracksMap>();
  auto ele_tracks = std::make_unique<reco::TrackCollection>();
  auto mu_tracks = std::make_unique<reco::TrackCollection>();
  auto lost_ele_tracks = std::make_unique<reco::TrackCollection>();
  auto lost_mu_tracks = std::make_unique<reco::TrackCollection>();
  auto ele_tracks_map = std::make_unique<jmt::UnpackedCandidateTracksMap>();
  auto mu_tracks_map = std::make_unique<jmt::UnpackedCandidateTracksMap>();
  auto tracks_pvs = std::make_unique<std::vector<unsigned>>();
  auto lost_tracks_pvs = std::make_unique<std::vector<unsigned>>();
 
  auto tight_ele_tracks = std::make_unique<reco::TrackCollection>();
  auto med_mu_tracks = std::make_unique<reco::TrackCollection>();

  reco::TrackRefProd h_output_tracks = event.getRefBeforePut<reco::TrackCollection>();
  reco::TrackRefProd h_output_mu_tracks = event.getRefBeforePut<reco::TrackCollection>();
  reco::TrackRefProd h_output_ele_tracks = event.getRefBeforePut<reco::TrackCollection>();


  int ntkpass = 0, nlosttkpass = 0, nmtkpass=0, netkpass=0, nlostmtkpass = 0, nlostetkpass = 0;

  //https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookMiniAOD2014#Packed_ParticleFlow_Candidates

  //going to do this twice; once for electrons, once for muons ... 
  std::vector<const reco::Candidate *> mu_cand;
  std::vector<const reco::Candidate *> ele_cand;
  for (const pat::Muon &mu : *muons) mu_cand.push_back(&mu);
  for (const pat::Electron &el : *electrons) ele_cand.push_back(&el);

  //now getting just the med muons & tight electrons 
  std::vector<const reco::Candidate *> medmu_cand;
  std::vector<const reco::Candidate *> tightele_cand;
  for (const pat::Muon &muon : *muons) {
    if (muon.passed(reco::Muon::CutBasedIdMedium)) {
      if (muon.passed(reco::Muon::PFIsoTight)) medmu_cand.push_back(&muon);
    }
  }
  for (const pat::Electron &electron : *electrons) {
    if (electron.electronID("cutBasedElectronID-Fall17-94X-V2-tight")) tightele_cand.push_back(&electron);
  }


  std::vector<int> eidx_toremove;
  std::vector<int> midx_toremove;
  std::vector<int> eidx_lost_toremove;
  std::vector<int> midx_lost_toremove;
  std::vector<int> tight_eidx_toremove;
  std::vector<int> med_midx_toremove;


  for (const reco::Candidate *muon : mu_cand) {
    // get a list of the PF candidates used to build this lepton, so to exclude them (one footprint for packed; another for lost...)
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
          if (cand.charge() != 0) {
            midx_toremove.push_back(i);
            continue;
          }
        }
      }
    }
    // //loop on lost candidates
    // for (unsigned int i = 0, ie = lost_candidates->size(); i < ie; ++i) {
    //   const pat::PackedCandidate& cand = (*lost_candidates)[i];
    //   if (deltaR(cand,*muon) < 0.002) {
    //     midx_lost_toremove.push_back(i);
    //     continue;
    //   }
    // }
  }
  for (const reco::Candidate *electron : ele_cand) {
    // get a list of the PF candidates used to build this lepton, so to exclude them
    std::vector<reco::CandidatePtr> ele_footprint;
    for (unsigned int i = 0, n = electron->numberOfSourceCandidatePtrs(); i < n; ++i) {
      if (electron->sourceCandidatePtr(i).isNonnull()) {
        ele_footprint.push_back(electron->sourceCandidatePtr(i));
      }
    }
    // now loop on pf candidates
    for (unsigned int i = 0, n = packed_candidates->size(); i < n; ++i) {
      const pat::PackedCandidate &cand = (*packed_candidates)[i];
      // pfcandidate-based footprint removal
      if (deltaR(cand,*electron) < 0.2) {
        if (std::find(ele_footprint.begin(), ele_footprint.end(), reco::CandidatePtr(packed_candidates,i)) != ele_footprint.end()) {
          if (cand.charge() != 0) {
            eidx_toremove.push_back(i);
            continue;
          }
        }
      }
    }
    //loop on lost candidates
    // for (unsigned int i = 0, ie = lost_candidates->size(); i < ie; ++i) {
    //   const pat::PackedCandidate& cand = (*lost_candidates)[i];
    //   if (deltaR(cand,*electron) < 0.002) {
    //     eidx_lost_toremove.push_back(i);
    //     continue;
    //   }
    // }
  }

  //now doing everything again, but just for the leptons that passed cutbased ID 
    for (const reco::Candidate *medmu : medmu_cand) {
    // get a list of the PF candidates used to build this lepton, so to exclude them (one footprint for packed; another for lost...)
    std::vector<reco::CandidatePtr> medmu_footprint;
    for (unsigned int i = 0, n = medmu->numberOfSourceCandidatePtrs(); i < n; ++i) {
      medmu_footprint.push_back(medmu->sourceCandidatePtr(i));
    }
    // now loop on pf candidates
    for (unsigned int i = 0, n = packed_candidates->size(); i < n; ++i) {
      const pat::PackedCandidate &cand = (*packed_candidates)[i];
      if (deltaR(cand,*medmu) < 0.2) {
        // pfcandidate-based footprint removal
        if (std::find(medmu_footprint.begin(), medmu_footprint.end(), reco::CandidatePtr(packed_candidates,i)) != medmu_footprint.end()) {
          if (cand.charge() != 0) {
            med_midx_toremove.push_back(i);
            continue;
          }
        }
      }
    }
  }
  for (const reco::Candidate *tightele : tightele_cand) {
    // get a list of the PF candidates used to build this lepton, so to exclude them
    std::vector<reco::CandidatePtr> tightele_footprint;
    for (unsigned int i = 0, n = tightele->numberOfSourceCandidatePtrs(); i < n; ++i) {
      if (tightele->sourceCandidatePtr(i).isNonnull()) {
        tightele_footprint.push_back(tightele->sourceCandidatePtr(i));
      }
    }
    // now loop on pf candidates
    for (unsigned int i = 0, n = packed_candidates->size(); i < n; ++i) {
      const pat::PackedCandidate &cand = (*packed_candidates)[i];
      // pfcandidate-based footprint removal
      if (deltaR(cand,*tightele) < 0.2) {
        if (std::find(tightele_footprint.begin(), tightele_footprint.end(), reco::CandidatePtr(packed_candidates,i)) != tightele_footprint.end()) {
          if (cand.charge() != 0) {
            tight_eidx_toremove.push_back(i);
            continue;
          }
        }
      }
    }
  }

  //////////////////////////////////////////////////////////////////////////////////////////////////

  // put tracks in their respective collections : 
  // electron tracks pt >= 20 GeV 
  // muon tracks pt >= 20 GeV 
  // all other tracks (including lepton tracks with pt < 20 GeV) 
  for (int i = 0, n = packed_candidates->size(); i < n; ++i) {
    const pat::PackedCandidate& cand = (*packed_candidates)[i];
    if (separate_leptons) {

      if (std::find(midx_toremove.begin(), midx_toremove.end(), i) != midx_toremove.end()) {
        if (pass_cand(cand)) {
          const reco::Track& mtk = cand.pseudoTrack();
          if (debug) debug_tk(mtk, "", mu_tracks->size());
          

          if (mtk.pt() >= 20.0) {
            if (pass_leptk(mtk)) {
              ++nmtkpass;
              mu_tracks->push_back(mtk);
              mu_tracks_map->insert(reco::CandidatePtr(packed_candidates, i), reco::TrackRef(h_output_mu_tracks, mu_tracks->size() - 1));
              tracks_pvs->push_back(encode_vertex_ref(cand));

              // also getting the muon tracks (w/ cutbased Med) --> they will be a subset of above, hence we can put it here. 
              if (std::find(med_midx_toremove.begin(), med_midx_toremove.end(), i) != midx_toremove.end()) {
                med_mu_tracks->push_back(mtk);
              }
            }
          }
          else {
            if (pass_tk(mtk)) {
              ++ntkpass;
              tracks->push_back(mtk);
              tracks_map->insert(reco::CandidatePtr(packed_candidates, i), reco::TrackRef(h_output_tracks, tracks->size() - 1));
              tracks_pvs->push_back(encode_vertex_ref(cand));
            }
          }
        }

        continue;
      }

      else if (std::find(eidx_toremove.begin(), eidx_toremove.end(), i) != eidx_toremove.end()) {
        if (pass_cand(cand)) {
          const reco::Track& etk = cand.pseudoTrack();
          if (debug) debug_tk(etk, "", ele_tracks->size());

          if (etk.pt() >= 20.0) {
            if (pass_leptk(etk)) {
              ++netkpass;

              ele_tracks->push_back(etk);
              ele_tracks_map->insert(reco::CandidatePtr(packed_candidates, i), reco::TrackRef(h_output_ele_tracks, ele_tracks->size() - 1));
              tracks_pvs->push_back(encode_vertex_ref(cand));

              //temporary : also getting the ele tracks (w/ cutbased Tight) --> they will be a subset of above, hence we can put it here. 
              if (std::find(tight_eidx_toremove.begin(), tight_eidx_toremove.end(), i) != eidx_toremove.end()) {
                tight_ele_tracks->push_back(etk);
              }
            }
          }
          else {
            if (pass_tk(etk)) {
              ++ntkpass;
              tracks->push_back(etk);
              tracks_map->insert(reco::CandidatePtr(packed_candidates, i), reco::TrackRef(h_output_tracks, tracks->size() - 1));
              tracks_pvs->push_back(encode_vertex_ref(cand));
            }
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



  for (size_t i = 0, ie = lost_candidates->size(); i < ie; ++i) {
    const pat::PackedCandidate& cand = (*lost_candidates)[i];
    if (separate_leptons) {
      if (std::find(midx_lost_toremove.begin(), midx_lost_toremove.end(), i) != midx_lost_toremove.end()) {
        if (pass_cand(cand)) {
          const reco::Track& mtk = cand.pseudoTrack();
          if (debug) debug_tk(mtk, "lost_mu", lost_mu_tracks->size());
          

          if (mtk.pt() >= 20.0) {
            if (pass_leptk(mtk)) {
              ++nlostmtkpass;
              if (add_lost_candidates) {
                mu_tracks->push_back(mtk);
                mu_tracks_map->insert(reco::CandidatePtr(packed_candidates, i), reco::TrackRef(h_output_mu_tracks, mu_tracks->size() - 1));
                tracks_pvs->push_back(encode_vertex_ref(cand));
              }
              lost_mu_tracks->push_back(mtk);
            }
          }
          else {
            if (pass_tk(mtk)) {
              ++nlosttkpass;
              if (add_lost_candidates) {
                tracks->push_back(mtk);
                tracks_map->insert(reco::CandidatePtr(packed_candidates, i), reco::TrackRef(h_output_tracks, tracks->size() - 1));
                tracks_pvs->push_back(encode_vertex_ref(cand));
              }
            }
            lost_tracks->push_back(mtk);
          }
        }
        continue;
      }

      else if (std::find(eidx_lost_toremove.begin(), eidx_lost_toremove.end(), i) != eidx_lost_toremove.end()) {
        if (pass_cand(cand)) {
          const reco::Track& etk = cand.pseudoTrack();
          if (debug) debug_tk(etk, "lost_ele", lost_ele_tracks->size());

          if (etk.pt() >= 20.0) {
            if (pass_leptk(etk)) {
              ++nlostetkpass;

              if (add_lost_candidates) {
                ele_tracks->push_back(etk);
                ele_tracks_map->insert(reco::CandidatePtr(packed_candidates, i), reco::TrackRef(h_output_ele_tracks, ele_tracks->size() - 1));
                tracks_pvs->push_back(encode_vertex_ref(cand));
              }
              lost_ele_tracks->push_back(etk);
            }
          }
          else {
            if (pass_tk(etk)) {
              ++nlosttkpass;

              if (add_lost_candidates) {
                tracks->push_back(etk);
                tracks_map->insert(reco::CandidatePtr(packed_candidates, i), reco::TrackRef(h_output_tracks, tracks->size() - 1));
                tracks_pvs->push_back(encode_vertex_ref(cand));
              }
              lost_tracks->push_back(etk);
            }
          }
        }
        continue;
      }
    }

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
  if (debug) std::cout << "JMTUnpackedCandidateTracks::produce: nmupass/nlostmtk = " << nlostmtkpass << " / " << lost_mu_tracks->size() << " nelepass/nlostetk = " << nlostetkpass << " / " << lost_ele_tracks->size() << "\n";

  event.put(std::move(tracks));
  if (separate_leptons) {
    event.put(std::move(ele_tracks), "electrons");
    event.put(std::move(mu_tracks), "muons");
    event.put(std::move(ele_tracks_map), "elemap");
    event.put(std::move(mu_tracks_map), "mumap");

    event.put(std::move(tight_ele_tracks), "tightele");
    event.put(std::move(med_mu_tracks), "medmu");
  }
  event.put(std::move(lost_tracks), "lost");
  event.put(std::move(tracks_map));
  event.put(std::move(tracks_pvs));
  event.put(std::move(lost_tracks_pvs));
}

DEFINE_FWK_MODULE(JMTUnpackedCandidateTracks);
