#ifndef JMTucker_MFVNeutralinoFormats_UnpackedCandidateTracksMap_h
#define JMTucker_MFVNeutralinoFormats_UnpackedCandidateTracksMap_h

namespace mfv {
  class UnpackedCandidateTracksMap {
  public:
    reco::TrackRef find(const reco::CandidatePtr& a) const {
      for (size_t i = 0, ie = map_.size(); i < ie; ++i)
        if (a == map_[i].first)
          return map_[i].second;
      return reco::TrackRef();
    }

    reco::CandidatePtr find(const reco::TrackRef& b) const {
      for (size_t i = 0, ie = map_.size(); i < ie; ++i)
        if (b == map_[i].second)
          return map_[i].first;
      return reco::CandidatePtr();
    }

    void insert(const reco::CandidatePtr& a, const reco::TrackRef& b) {
      for (size_t i = 0, ie = map_.size(); i < ie; ++i) {
        if (a == map_[i].first)  { map_[i].second = b; return; }
        if (b == map_[i].second) { map_[i].first  = a; return; }
      }
      map_.push_back(std::make_pair(a,b));
    }

    typedef std::vector<std::pair<reco::CandidatePtr, reco::TrackRef>> map_t;
    typedef map_t::iterator iterator;
    typedef map_t::const_iterator const_iterator;
    iterator begin() { return map_.begin(); }
    iterator end() { return map_.end(); }
    const_iterator begin() const { return map_.begin(); }
    const_iterator end() const { return map_.end(); }
    const_iterator cbegin() const { return map_.cbegin(); }
    const_iterator cend() const { return map_.cend(); }

  private:
    std::vector<std::pair<reco::CandidatePtr, reco::TrackRef>> map_;
  };
}

#endif
