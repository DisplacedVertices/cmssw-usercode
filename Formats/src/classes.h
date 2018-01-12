#include "DataFormats/Common/interface/Wrapper.h"
#include "JMTucker/Formats/interface/MergeablePOD.h"

namespace JMTucker_Formats {
  struct dictionary {
    jmt::MergeablePOD<int> mi;
    jmt::MergeablePOD<float> mf;
    edm::Wrapper<jmt::MergeablePOD<int> > wmi;
    edm::Wrapper<jmt::MergeablePOD<float> > wmf;
  };
}
