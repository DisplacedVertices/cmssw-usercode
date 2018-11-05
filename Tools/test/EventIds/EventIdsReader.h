#ifndef EventIdsReader_h
#define EventIdsReader_h

#include <map>
#include <set>
#include <stdexcept>
#include <sstream>
#include "TFile.h"
#include "TTree.h"

const int mc_runmin = 1;
const int mc_runmax = 1;
const int data_runmin = 297047;
const int data_runmax = 325175;

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
        runmin = mc_runmin;
        runmax = mc_runmax;
      }
      else {
        runmin = data_runmin;
        runmax = data_runmax;
      }
    }

    unsigned run() const { return run_ + runmin; }
    void run(unsigned r) { if (r < runmin || r > runmax) { printf("run %u\n", r); throw std::runtime_error("run outside limits"); } run_ = r - runmin; }
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

    void print(FILE* f, bool newln=false) const {
      if (extra())
        fprintf(f, "(%u,%u,%llu, %f)", run(), lumi(), event(), extra());
      else
        fprintf(f, "(%u,%u,%llu)", run(), lumi(), event());
      if (newln) fprintf(f, "\n");
    }
  };

  bool use_extra;
  bool prints;
  std::map<RLE, std::vector<int>> m;

  EventIdsReader() : use_extra(false), prints(false) {
    setup_from_env();
  }

  void setup_from_env() {
    if (getenv("EVENTIDSREADER_PRINTS"))
      prints = true;
    if (getenv("EVENTIDSREADER_IS_MC") || getenv("EVENTIDSREADER_USE_EXTRA"))
      EventIdsReader::RLE::set_type(true);
    if (getenv("EVENTIDSREADER_USE_EXTRA"))
      use_extra = true;
  }

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

      m[rle].push_back(fileno);
    }

    if (prints) {
      fprintf(stderr, "\r                                     \r");
      fflush(stderr);
    }

    delete f;
  }
};

unsigned EventIdsReader::RLE::runmin = data_runmin;
unsigned EventIdsReader::RLE::runmax = data_runmax;

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
