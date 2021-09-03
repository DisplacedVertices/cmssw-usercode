#ifndef DVCode_Tools_Framework_h
#define DVCode_Tools_Framework_h

#include <sstream>
#include "DataFormats/Common/interface/Ref.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

namespace jmt {
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
    out << " with index " << ref.index();
  }

  template <typename T>
    void dump_ptr(std::ostream& out, const edm::Ptr<T>& ptr, const edm::Event* event=0) {
    out << "ptr with product id " << ptr.id().id();
    if (ptr.id().id() == 0) {
      out << "\n";
      return;
    }
    if (event) {
      edm::Provenance prov = event->getProvenance(ptr.id());
      out << ", branch " << prov.branchName() << " (id " << prov.branchID().id() << "),";
    }
    out << " with key " << ptr.key();
  }

  template <typename T>
    void dump_ref2base(std::ostream& out, const edm::RefToBase<T>& ref, const edm::Event* event=0) {
    out << "ref2base with product id " << ref.id().id();
    if (ref.id().id() == 0) {
      out << "\n";
      return;
    }
    if (event) {
      edm::Provenance prov = event->getProvenance(ref.id());
      out << ", branch " << prov.branchName() << " (id " << prov.branchID().id() << "),";
    }
    out << " with key " << ref.key();
  }

  template <typename T, typename T2>
    T getProcessModuleParameter(const edm::Event& event, const T2& consumer, const std::string& module, const std::string& parameter) {
    edm::ParameterSet process_ps;
    if (!event.getProcessParameterSet(consumer->moduleDescription().processName(), process_ps))
      throw cms::Exception("getProcessModuleParameter", "could not get ParameterSet from event provenance");
    const edm::ParameterSet& module_ps = process_ps.getParameterSet(module); // may throw if module not found, consider catching exception and rethrowing with "better" reason
    return module_ps.getParameter<T>(parameter);
  }
}

#endif
