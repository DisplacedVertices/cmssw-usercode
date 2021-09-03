#include "DataFormats/Common/interface/Wrapper.h"
#include "DVCode/Formats/interface/MergeablePOD.h"
#include "DVCode/Formats/interface/TracksMap.h"

namespace DVCode_Formats {
  struct dictionary {
    jmt::MergeablePOD<int> mi;
    jmt::MergeablePOD<float> mf;
    edm::Wrapper<jmt::MergeablePOD<int> > wmi;
    edm::Wrapper<jmt::MergeablePOD<float> > wmf;

    edm::Wrapper<jmt::UnpackedCandidateTracksMap> wuctm;
    edm::Wrapper<jmt::TracksMap> wtm;
  };
}
