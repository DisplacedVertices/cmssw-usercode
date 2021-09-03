#ifndef DVCode_Formats_UnpackedCandidateTracksMap_h
#define DVCode_Formats_UnpackedCandidateTracksMap_h

#include "DataFormats/Candidate/interface/CandidateFwd.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"

namespace jmt {
  template <typename A, typename B>
  class ITracksMap {
  public:
    B find(const A& a) const {
      for (size_t i = 0, ie = map_.size(); i < ie; ++i)
        if (a == map_[i].first)
          return map_[i].second;
      return B();
    }

    A rfind(const B& b) const {
      for (size_t i = 0, ie = map_.size(); i < ie; ++i)
        if (b == map_[i].second)
          return map_[i].first;
      return A();
    }

    void insert(const A& a, const B& b) {
      for (size_t i = 0, ie = map_.size(); i < ie; ++i) {
        if (a == map_[i].first)  { map_[i].second = b; return; }
        if (b == map_[i].second) { map_[i].first  = a; return; }
      }
      map_.push_back(std::make_pair(a,b));
    }

    typedef std::vector<std::pair<A, B>> map_t;
    typedef typename map_t::iterator iterator;
    typedef typename map_t::const_iterator const_iterator;
    iterator begin() { return map_.begin(); }
    iterator end() { return map_.end(); }
    const_iterator begin() const { return map_.begin(); }
    const_iterator end() const { return map_.end(); }
    const_iterator cbegin() const { return map_.cbegin(); }
    const_iterator cend() const { return map_.cend(); }

  private:
    map_t map_;
  };

  typedef ITracksMap<reco::CandidatePtr, reco::TrackRef> UnpackedCandidateTracksMap;
  typedef ITracksMap<reco::TrackRef, reco::TrackRef> TracksMap;
}

#endif
