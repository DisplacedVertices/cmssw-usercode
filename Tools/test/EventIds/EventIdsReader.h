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
    unsigned short run_;
    unsigned lumi_;
    unsigned long long event_;
    float extra_;
  public:
    static unsigned runmin;
    static unsigned runmax;

    static void set_type(bool is_mc) {
      if (is_mc) {
        runmin = 1;
        runmax = 1;
      }
      else {
        runmin = 254231;
        runmax = 284044;
      }
    }

    unsigned run() const { return run_ + runmin; }
    void run(unsigned r) { if (r < runmin || r > runmax) throw std::runtime_error("run outside limits"); run_ = r - runmin; }
    unsigned lumi() const { return lumi_; }
    void lumi(unsigned l) {
      //  if (l > 65535) throw std::runtime_error("lumi outside limits"); 
      lumi_ = l;
    }
    unsigned long long event() const { return event_; }
    void event(unsigned long long e) { event_ = e; }
    float extra() const { return extra_; }
    void extra(float e) { extra_ = e; }

    RLE(unsigned r, unsigned l, unsigned long long e) {
      run(r);
      lumi(l);
      event(e);
      extra_ = 0;
    }

    void print(FILE* f) const {
      if (extra())
        fprintf(f, "(%u,%u,%llu, %f)", run(), lumi(), event(), extra());
      else
        fprintf(f, "(%u,%u,%llu)", run(), lumi(), event());
    }
  };

  bool use_extra;
  bool prints;
  std::map<RLE, std::set<int>> m;

 EventIdsReader() : use_extra(false), prints(false) {}

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
    float extra;
    t->SetBranchAddress("run",   &run);
    t->SetBranchAddress("lumi",  &lumi);
    t->SetBranchAddress("event", &event);
    if (use_extra)
      t->SetBranchAddress("first_parton_pz", &extra);

    for (long i = 0, ie = t->GetEntries(); i < ie; ++i) {
      if (t->LoadTree(i) < 0) break;
      if (t->GetEntry(i) <= 0) continue;

      if (prints && i % 500000 == 0) {
        fprintf(stderr, "\r%li/%li", i, ie);
        fflush(stderr);
      }

      RLE rle(run, lumi, event);
      if (use_extra)
        rle.extra(extra);

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

unsigned EventIdsReader::RLE::runmin = 254231;
unsigned EventIdsReader::RLE::runmax = 284044;

bool operator<(const EventIdsReader::RLE& a, const EventIdsReader::RLE& b) {
  if (a.run() != b.run())
    return a.run() < b.run();
  else {
    if (a.lumi() != b.lumi())
      return a.lumi() < b.lumi();
    else {
      if (a.event() != b.event())
        return a.event() < b.event();
      else
        return a.extra() < b.extra();
    }
  }
}

#endif
