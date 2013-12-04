// rootg++ -std=c++0x dups.cc -o dups

#include <tuple>
#include "TFile.h"
#include "TTree.h"

int main(int argc, char** argv) {
  if (argc < 3) {
    fprintf(stderr, "usage: eiddups input.root path_to_tree\n");
    return 1;
  }

  printf("reading %s:%s\n", argv[1], argv[2]);
  TFile* f = TFile::Open(argv[1]);
  TTree* t = (TTree*)f->Get(argv[2]);

  unsigned run;
  unsigned lumi;
  unsigned event;
  t->SetBranchAddress("run", &run);
  t->SetBranchAddress("lumi", &lumi);
  t->SetBranchAddress("event", &event);

  typedef std::tuple<unsigned, unsigned, unsigned> RLE;
  std::map<RLE, int> m;

  for (long i = 0, ie = t->GetEntries(); i < ie; ++i) {
    if (t->LoadTree(i) < 0) break;
    if (t->GetEntry(i) <= 0) continue;
    if (i % 500000 == 0) {
      printf("\r%li/%li", i, ie);
      fflush(stdout);
    }
    
    RLE rle(run, lumi, event);

    if (m.find(rle) == m.end())
      m[rle] = 1;
    else
      ++m[rle];
  }
  printf("\r                        \r");
  fflush(stdout);

  int dup_count = 0;
  std::vector<RLE> dups;
  for (auto p : m) {
    if (p.second > 1) {
      dups.push_back(p.first);
      ++dup_count;
    }
  }

  delete f;

  if (dup_count) {
    printf("duplicates:\n");
    for (const RLE& r : dups)
      printf("%u,%u,%u\n", std::get<0>(r), std::get<1>(r), std::get<2>(r));
    return 1;
  }
}
