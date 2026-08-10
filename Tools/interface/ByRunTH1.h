#ifndef JMTucker_Tools_ByRunTH1_h
#define JMTucker_Tools_ByRunTH1_h

#include <map>
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "FWCore/ServiceRegistry/interface/Service.h"

template <typename T>
class ByRunTH1 {
 public:
   ByRunTH1() : fs_(nullptr) {}

  void set(edm::Service<TFileService>* fs, const char* name, const char* title, const int nbins, const double xmin, const double xmax) {
    fs_ = fs;
    name_ = name;
    title_ = title;
    nbins_ = nbins;
    xmin_ = xmin;
    xmax_ = xmax;
  }

  T* operator[](unsigned run) {
    if (fs_ == nullptr) throw cms::Exception("NotInitialized", "ByRunTH1 instance used without call to set");
    if (hist_map_.find(run) == hist_map_.end())
      book(run); 
    return hist_map_[run];
  }

  void book(unsigned run) {
    if (fs_ == nullptr) throw cms::Exception("NotInitialized", "ByRunTH1 instance used without call to set");
    if (hist_map_.find(run) == hist_map_.end())
      hist_map_[run] = (*fs_)->make<T>(TString::Format("%s_run%u", name_.Data(), run), 
                                       TString::Format("%s (run %u)", title_.Data(), run), 
                                       nbins_,
                                       xmin_,
                                       xmax_);
  }

 private:
  edm::Service<TFileService>* fs_;
  std::map<unsigned, T*> hist_map_;

  TString name_;
  TString title_;
  int nbins_;
  double xmin_;
  double xmax_;    
};

#endif
