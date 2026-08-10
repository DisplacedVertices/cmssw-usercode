#include "DataFormats/Common/interface/Wrapper.h"
#include "JMTucker/Formats/interface/MergeablePOD.h"
#include "JMTucker/Formats/interface/TracksMap.h"

namespace JMTucker_Formats {
  struct dictionary {
    jmt::MergeablePOD<int> mi;
    jmt::MergeablePOD<float> mf;
    edm::Wrapper<jmt::MergeablePOD<int> > wmi;
    edm::Wrapper<jmt::MergeablePOD<float> > wmf;

    edm::Wrapper<jmt::UnpackedCandidateTracksMap> wuctm;
    edm::Wrapper<jmt::TracksMap> wtm;
  };
}
