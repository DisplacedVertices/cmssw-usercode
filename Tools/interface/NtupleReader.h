#ifndef JMTucker_Tools_NtupleReader_h
#define JMTucker_Tools_NtupleReader_h

#include <iostream>
#include <string>
#include "TFile.h"
#include "TTree.h"

namespace jmt {
  template <typename T>
  struct NtupleReader {
  public:
    TFile* f;
    TTree* t;
    T nt;
    TFile* f_out;

    NtupleReader(const std::string& in_fn, const std::string& out_fn, const std::string& tree_path)
    : f(nullptr), t(nullptr), f_out(nullptr)
    {
      f = TFile::Open(in_fn.c_str());
      if (!f || !f->IsOpen()) {
        std::cerr << "could not open " << in_fn << "\n";
        exit(1);
      }

      t = (TTree*)f->Get(tree_path.c_str());
      if (!t) {
        std::cerr << "could not get tree " << tree_path << " from " << in_fn << "\n";
        exit(1);
      }

      nt.read_from_tree(t);

      if (out_fn.compare(0, 3, "n/a") == 0)
        f_out = 0;
      else
        f_out = new TFile(out_fn.c_str(), "recreate");
    }

    ~NtupleReader(){
      if (f_out) {
        f_out->Write();
        f_out->Close();
      }
      f->Close();

      delete f;
      delete f_out;
    }
  };
}

#endif
