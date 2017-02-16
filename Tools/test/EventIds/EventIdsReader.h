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
  class RLE {
    static const unsigned runmin_ = 254231;
    static const unsigned runmax_ = 284044;

    unsigned short run_;
    unsigned short lumi_;
    unsigned long long event_;
  public:
    unsigned run() const { return run_ + runmin_; }
    void run(unsigned r) { if (r < runmin_ || r > runmax_) throw std::runtime_error("run outside limits"); run_ = r - runmin_; }
    unsigned lumi() const { return lumi_; }
    void lumi(unsigned l) { if (l > 65535) throw std::runtime_error("lumi outside limits"); lumi_ = l; }
    unsigned long long event() const { return event_; }
    void event(unsigned long long e) { event_ = e; }

    RLE(unsigned r, unsigned l, unsigned long long e) {
      run(r);
      lumi(l);
      event(e);
    }

    void print(FILE* f) const { fprintf(f, "(%u,%u,%llu)", run(), lumi(), event()); }
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

    unsigned run, lumi;
    unsigned long long event;
    t->SetBranchAddress("run",   &run);
    t->SetBranchAddress("lumi",  &lumi);
    t->SetBranchAddress("event", &event);

    for (long i = 0, ie = t->GetEntries(); i < ie; ++i) {
      if (t->LoadTree(i) < 0) break;
      if (t->GetEntry(i) <= 0) continue;

      if (prints && i % 500000 == 0) {
        fprintf(stderr, "\r%li/%li", i, ie);
        fflush(stderr);
      }

      RLE rle(run, lumi, event);
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
  if (a.run() != b.run())
    return a.run() < b.run();
  else {
    if (a.lumi() != b.lumi())
      return a.lumi() < b.lumi();
    else
      return a.event() < b.event();
  }
}

#endif
