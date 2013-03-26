#include <map>
#include "DataFormats/Common/interface/Wrapper.h"

namespace {
  namespace {
    std::map<int, std::pair<double, double> > dummymutddb;
    edm::Wrapper<std::map<int, std::pair<double, double> > > dummymutddbW;
  }
}
