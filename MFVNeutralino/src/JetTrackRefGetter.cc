#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "JMTucker/Tools/interface/Framework.h"
#include "JMTucker/MFVNeutralino/interface/JetTrackRefGetter.h"

namespace mfv {
  void JetTrackRefGetter::setup_event(const edm::Event& event) {
    if (!input_is_miniaod)
      return;

    if (event.cacheIdentifier() == last_cacheIdentifier)
      return;

    last_cacheIdentifier = event.cacheIdentifier();
    event.getByToken(unpacked_candidate_tracks_map_token, unpacked_candidate_tracks_map);
    for (size_t i = 0, ie = tracks_maps_tokens.size(); i < ie; ++i)
      event.getByToken(tracks_maps_tokens[i], tracks_maps[i]);

    if (verbose) {
      std::cout << "JetTrackRefGetter " << module_label << " unpacked candidate tracks map:\n";
      for (auto it : *unpacked_candidate_tracks_map) {
        std::cout << "  ";
        dump_ptr(std::cout, it.first, &event);
        std::cout << " -> ";
        dump_ref(std::cout, it.second, &event);
        std::cout << "\n";
      }
      std::cout << "JetTrackRefGetter " << module_label << " END unpacked candidate tracks map\n";

      for (size_t i = 0, ie = tracks_maps.size(); i < ie; ++i) {
        std::cout << "JetTrackRefGetter " << module_label << " tracks map #" << i << ":\n";
        for (auto it : *tracks_maps[i]) {
          std::cout << "  ";
          dump_ref(std::cout, it.first, &event);
          std::cout << " -> ";
          dump_ref(std::cout, it.second, &event);
          std::cout << "\n";
        }
        std::cout << "JetTrackRefGetter " << module_label << " END tracks map #" << i << "\n";
      }
    }
  }

  JetTrackRefGetter::JetTrackRefGetter(const std::string& label, const edm::ParameterSet& cfg, edm::ConsumesCollector&& cc)
    : input_is_miniaod(cfg.getParameter<bool>("input_is_miniaod")),
      unpacked_candidate_tracks_map_token(cc.consumes<mfv::UnpackedCandidateTracksMap>(cfg.getParameter<edm::InputTag>("unpacked_candidate_tracks_map_src"))),
      verbose(cfg.getUntrackedParameter<bool>("verbose", false)),
      module_label(label),
      last_cacheIdentifier(0)
  {
    for (auto tag : cfg.getParameter<std::vector<edm::InputTag>>("tracks_maps_srcs"))
      tracks_maps_tokens.push_back(cc.consumes<mfv::TracksMap>(tag));
    tracks_maps.resize(tracks_maps_tokens.size());
  }

  std::vector<reco::TrackRef> JetTrackRefGetter::tracks(const edm::Event& event, const pat::Jet& jet) {
    setup_event(event);

    std::vector<reco::TrackRef> r;

    if (input_is_miniaod) {
      if (verbose)
        std::cout << "JetTrackRefGetter " << module_label << " jet " << jet.pt() << "," << jet.eta() << "," << jet.phi() << "," << jet.energy() << ":\n";

      for (const reco::CandidatePtr& p : jet.daughterPtrVector()) {
        if (verbose) {
          std::cout << "  dau " << p->charge()*p->pt() << "," << p->eta() << "," << p->phi() << " ";
          dump_ptr(std::cout, p, &event);
          std::cout << "\n";
        }

        reco::TrackRef tk = unpacked_candidate_tracks_map->find(p);
        for (auto m : tracks_maps)
          tk = m->find(tk);

        if (tk.isNonnull()) {
          r.push_back(tk);

          if (verbose) {
            std::cout << "    in map -> track " << tk->charge()*tk->pt() << "," << tk->eta() << "," << tk->phi() << "," << tk->dxy() << "," << tk->dz() << " ";
            dump_ref(std::cout, tk, &event);
            std::cout << "\n";
          }
        }
      }
    }
    else {
      for (const reco::PFCandidatePtr& pfcand : jet.getPFConstituents()) {
        const reco::TrackRef& tk = pfcand->trackRef();
        if (tk.isNonnull())
          r.push_back(tk);
      }
    }

    return r;
  }
}
