#ifndef EventIdsReader_h
#define EventIdsReader_h

#include <map>
#include <set>
#include <stdexcept>
#include <sstream>
#include "TFile.h"
#include "TTree.h"

class EventIdsReader {
public:
  struct RLE {
    unsigned run;
    unsigned lumi;
    unsigned long long event;
    void print(FILE* f) const { fprintf(f, "(%u,%u,%llu)", run, lumi, event); }
  };

  bool prints;
  std::map<RLE, std::set<int>> m;

  void process_file(const char* fn, const char* path, int fileno) {
    if (prints) fprintf(stderr, "read from %s:%s in file #%i\n", fn, path, fileno);

    TFile* f = TFile::Open(fn);
    if (!f->IsOpen()) {
      std::ostringstream os;
      os << "could not open file " << fn;
      throw std::runtime_error(os.str());
    }
    TTree* t = (TTree*)f->Get(path);
    if (!t) {
      std::ostringstream os;
      os << "could not read tree " << path << " from " << fn;
      throw std::runtime_error(os.str());
    }

    RLE rle;
    t->SetBranchAddress("run",   &rle.run);
    t->SetBranchAddress("lumi",  &rle.lumi);
    t->SetBranchAddress("event", &rle.event);

    for (long i = 0, ie = t->GetEntries(); i < ie; ++i) {
      if (t->LoadTree(i) < 0) break;
      if (t->GetEntry(i) <= 0) continue;

      if (prints && i % 500000 == 0) {
        fprintf(stderr, "\r%li/%li", i, ie);
        fflush(stderr);
      }
    
      if (m.find(rle) == m.end())
        m[rle] = std::set<int>({fileno});
      else
        m[rle].insert(fileno);
    }

    if (prints) {
      fprintf(stderr, "\r                                     \r");
      fflush(stderr);
    }

    delete f;
  }
};

bool operator<(const EventIdsReader::RLE& a, const EventIdsReader::RLE& b) {
  if (a.run != b.run)
    return a.run < b.run;
  else {
    if (a.lumi != b.lumi)
      return a.lumi < b.lumi;
    else
      return a.event < b.event;
  }
}

#endif
