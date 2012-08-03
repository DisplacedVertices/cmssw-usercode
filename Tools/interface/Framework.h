#ifndef JMTucker_Tools_Framework_h
#define JMTucker_Tools_Framework_h

#include <sstream>
#include "FWCore/Framework/interface/Event.h"

template <typename T>
void dump_ref(std::ostream& out, const edm::Ref<T>& ref, const edm::Event* event=0) {
  out << "ref with product id " << ref.id().id();
  if (ref.id().id() == 0) {
    out << "\n";
    return;
  }
  if (event) {
    edm::Provenance prov = event->getProvenance(ref.id());
    out << ", branch " << prov.branchName() << " (id " << prov.branchID().id() << "),";
  }
  out << " with index " << ref.index() << "\n";
}

#endif
