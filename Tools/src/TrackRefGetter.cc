#include "DataFormats/PatCandidates/interface/PackedCandidate.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "JMTucker/Tools/interface/Framework.h"
#include "JMTucker/Tools/interface/TrackRefGetter.h"

namespace jmt {
  void TrackRefGetter::setup_event(const edm::Event& event) {
    if (event.cacheIdentifier() == last_cacheIdentifier)
      return;

    last_cacheIdentifier = event.cacheIdentifier();

    if (input_is_miniaod)
      event.getByToken(unpacked_candidate_tracks_map_token, unpacked_candidate_tracks_map);
    for (size_t i = 0, ie = tracks_maps_tokens.size(); i < ie; ++i)
      event.getByToken(tracks_maps_tokens[i], tracks_maps[i]);

    if (verbose) {
      if (input_is_miniaod) {
        std::cout << "TrackRefGetter " << module_label << " unpacked candidate tracks map:\n";
        for (auto it : *unpacked_candidate_tracks_map) {
          std::cout << "  ";
          jmt::dump_ptr(std::cout, it.first, &event);
          std::cout << " -> ";
          jmt::dump_ref(std::cout, it.second, &event);
          std::cout << "\n";
        }
        std::cout << "TrackRefGetter " << module_label << " END unpacked candidate tracks map\n";
      }

      std::cout << "TrackRefGetter " << module_label << " # tracks maps: " << tracks_maps.size() << ":\n";
      for (size_t i = 0, ie = tracks_maps.size(); i < ie; ++i) {
        std::cout << " tracks map #" << i << ":\n";
        for (auto it : *tracks_maps[i]) {
          std::cout << "  ";
          jmt::dump_ref(std::cout, it.first, &event);
          std::cout << " -> ";
          jmt::dump_ref(std::cout, it.second, &event);
          std::cout << "\n";
        }
        std::cout << "TrackRefGetter " << module_label << " END tracks map #" << i << "\n";
      }
    }
  }

  TrackRefGetter::TrackRefGetter(const std::string& label, const edm::ParameterSet& cfg, edm::ConsumesCollector&& cc)
    : input_is_miniaod(cfg.getParameter<bool>("input_is_miniaod")),
      unpacked_candidate_tracks_map_token(cc.consumes<jmt::UnpackedCandidateTracksMap>(cfg.getParameter<edm::InputTag>("unpacked_candidate_tracks_map_src"))),
      verbose(cfg.getUntrackedParameter<bool>("verbose", false)),
      module_label(label),
      last_cacheIdentifier(0)
  {
    for (auto tag : cfg.getParameter<std::vector<edm::InputTag>>("tracks_maps_srcs"))
      tracks_maps_tokens.push_back(cc.consumes<jmt::TracksMap>(tag));
    tracks_maps.resize(tracks_maps_tokens.size());
  }

  std::vector<reco::TrackRef> TrackRefGetter::tracks(const edm::Event& event, const pat::Jet& jet) {
    setup_event(event);
    std::vector<reco::TrackRef> r;

    if (input_is_miniaod) {
      if (verbose)
        std::cout << "TrackRefGetter " << module_label << " jet " << jet.pt() << "," << jet.eta() << "," << jet.phi() << "," << jet.energy() << ":\n";

      for (const reco::CandidatePtr& p : jet.daughterPtrVector()) {
        if (verbose) {
          std::cout << "  dau " << p->charge()*p->pt() << "," << p->eta() << "," << p->phi() << " ";
          jmt::dump_ptr(std::cout, p, &event);
          std::cout << "\n";
        }

        reco::TrackRef tk = unpacked_candidate_tracks_map->find(p);
        for (auto m : tracks_maps)
          tk = m->find(tk);

        if (tk.isNonnull()) {
          r.push_back(tk);

          if (verbose) {
            std::cout << "    in map -> track " << tk->charge()*tk->pt() << "," << tk->eta() << "," << tk->phi() << "," << tk->dxy() << "," << tk->dz() << " ";
            jmt::dump_ref(std::cout, tk, &event);
            std::cout << "\n";
          }
        }
      }
    }
    else {
      for (const reco::PFCandidatePtr& pfcand : jet.getPFConstituents()) {
        reco::TrackRef tk = pfcand->trackRef();
        for (auto m : tracks_maps)
          tk = m->find(tk);
        if (tk.isNonnull())
          r.push_back(tk);
      }
    }

    return r;
  }

  std::vector<std::pair<reco::TrackRef,int>> TrackRefGetter::tracks(const edm::Event& event, const reco::VertexRef& v) {
    setup_event(event);
    std::vector<std::pair<reco::TrackRef,int>> r;

    if (input_is_miniaod) {
      for (auto ct : *unpacked_candidate_tracks_map) {
        auto c = dynamic_cast<const pat::PackedCandidate*>(&*ct.first);
        if (c->vertexRef().key() == v.key()) { // JMTBAD comparing only keys
          reco::TrackRef tk = ct.second;
          for (auto m : tracks_maps)
            tk = m->find(tk);
          if (tk.isNonnull())
            r.push_back(std::make_pair(tk, c->pvAssociationQuality()));
        }
      }
    }
    else {
      for (auto it = v->tracks_begin(), ite = v->tracks_end(); it != ite; ++it) {
        const double w = v->trackWeight(*it);
        reco::TrackRef tk = it->castTo<reco::TrackRef>();
        for (auto m : tracks_maps)
          tk = m->find(tk);
        if (tk.isNonnull())
          r.push_back(std::make_pair(tk, w > 0.5 ? pat::PackedCandidate::UsedInFitTight : pat::PackedCandidate::UsedInFitLoose));
      }
    }

    return r;
  }

  bool TrackRefGetter::has_track(const edm::Event& e, const pat::Jet& j, const reco::TrackRef& tk) {
    const auto rs = tracks(e,j);
    const bool has = std::find(rs.begin(), rs.end(), tk) != rs.end();
    if (verbose) {
      std::cout << "TrackRefGetter " << module_label << " jet " << j.pt() << "," << j.eta() << "," << j.phi() << "," << j.energy() << " has track ";
      jmt::dump_ref(std::cout, tk, &e);
      std::cout << "? " << has << "\n";
    }
    return has;
  }

  int TrackRefGetter::has_track(const edm::Event& e, const reco::VertexRef& v, const reco::TrackRef& tk) {
    for (auto rq : tracks(e,v))
      if (rq.first == tk)
        return rq.second;
    return -1;
  }
  
  /*size_t TrackRefGetter::ijet(const edm::Event& event, const pat::JetCollection& jets, const reco::TrackRef& tk) {
    for (size_t i = 0, ie = jets.size(); i < ie; ++i)
      for (reco::TrackRef r : tracks(event, jets[i]))
        if (r == tk)
          return i;

    return size_t(-1);
  }

  size_t TrackRefGetter::ivertex(const edm::Event& event, const reco::VertexCollection& vertices, const reco::TrackRef& tk) {
    for (size_t i = 0, ie = vertices->size(); i < ie; ++i)
      for (reco::TrackRef r : tracks(event, vertices[i], 0))
        if (r == tk)
          return i;

    return size_t(-1);
  }*/
}
