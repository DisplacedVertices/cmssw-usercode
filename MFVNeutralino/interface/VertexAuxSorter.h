#ifndef JMTucker_MFVNeutralino_VertexAuxSorter_h
#define JMTucker_MFVNeutralino_VertexAuxSorter_h

#include "JMTucker/MFVNeutralinoFormats/interface/VertexAux.h"

namespace mfv {
  class VertexAuxSorter {
  public:
    enum sort_by_this { sort_by_mass, sort_by_ntracks, sort_by_ntracks_then_mass };

    VertexAuxSorter(const std::string&);
    void sort(VertexAuxCollection&) const;

  private:
    sort_by_this sort_by;
    static bool by_mass   (const MFVVertexAux& a, const MFVVertexAux& b) { return a.mass[0]   > b.mass[0];   }
    static bool by_ntracks(const MFVVertexAux& a, const MFVVertexAux& b) { return a.ntracks() > b.ntracks(); }
    static bool by_ntracks_then_mass(const MFVVertexAux& a, const MFVVertexAux& b) {
      if (a.ntracks() == b.ntracks())
        return by_mass(a,b);
      return by_ntracks_then_mass(a,b);
    }
  };
}

#endif
