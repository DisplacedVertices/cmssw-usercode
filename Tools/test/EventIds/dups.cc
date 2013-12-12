// rootg++ -std=c++0x -Wall -Werror dups.cc -o dups

#include <set>
#include <map>
#include <tuple>
#include "TFile.h"
#include "TTree.h"

const char* path = 0;

typedef std::tuple<unsigned, unsigned, unsigned> RLE;
std::map<RLE, std::set<int> > m;

void process_file(const char* fn, int fileno) {
  fprintf(stderr, "reading %s:%s (fileno %i)\n", fn, path, fileno);
  TFile* f = TFile::Open(fn);
  if (!f->IsOpen()) {
    fprintf(stderr, "could not open file!\n");
    exit(1);
  }
  TTree* t = (TTree*)f->Get(path);
  if (!t) {
    fprintf(stderr, "could not read tree!\n");
    exit(1);
  }

  unsigned run;
  unsigned lumi;
  unsigned event;
  t->SetBranchAddress("run", &run);
  t->SetBranchAddress("lumi", &lumi);
  t->SetBranchAddress("event", &event);

  for (long i = 0, ie = t->GetEntries(); i < ie; ++i) {
    if (t->LoadTree(i) < 0) break;
    if (t->GetEntry(i) <= 0) continue;
    if (i % 500000 == 0) {
      fprintf(stderr, "\r%li/%li", i, ie);
      fflush(stderr);
    }
    
    RLE rle(run, lumi, event);
    if (m.find(rle) == m.end())
      m[rle] = std::set<int>({fileno});
    else
      m[rle].insert(fileno);
  }
  fprintf(stderr, "\r                                     \r");
  fflush(stderr);

  delete f;
}

int main(int argc, char** argv) {
  if (argc < 3) {
    fprintf(stderr, "usage: dups path_to_tree [scan_format] input_1.root [input_2.root ...] \n");
    return 1;
  }

  path = argv[1];
  const char* fmt = argv[2];
  int startat = 3;
  int fileno = -1;
  if (strchr(fmt, '%') == 0) {
    fprintf(stderr, "not using a fileno\n");
    startat = 2;
  }
  else
    fprintf(stderr, "scanning with fmt %s\n", fmt);

  for (int i = startat; i < argc; ++i) {
    if (startat == 3) {
      int c = sscanf(argv[i], fmt, &fileno); // JMTBAD I hope you don't care about your system
      if (c != 1) {
        fprintf(stderr, "could not scan %s for file number\n", argv[i]);
        return 1;
      }
    }

    process_file(argv[i], fileno);
  }

  int dup_count = 0;
  for (auto p : m) {
    if (p.second.size() > 1) {
      if (dup_count == 0)
        printf("duplicates:\n");
      printf("%u,%u,%u : ", std::get<0>(p.first), std::get<1>(p.first), std::get<2>(p.first));
      for (int fileno : p.second)
        printf("%i ", fileno);
      printf("\n");
      ++dup_count;
    }
  }

  if (dup_count == 0)
    printf("OK!\n");

  return dup_count > 0;
}
