// rootg++ -std=c++0x -Wall -Werror common.cc -o common

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
  if (argc < 4) {
    fprintf(stderr, "usage: common path_to_tree filelist1.txt filelist2.txt\n");
    return 1;
  }

  path = argv[1];
  const char* filelist[2] = { argv[2], argv[3] };
  for (int i = 0; i < 2; ++i) {
    FILE* flist = fopen(filelist[i], "rt");
    if (!flist) {
      fprintf(stderr, "could not open %s\n", filelist[i]);
      return 1;
    }
    char line[1024];
    while (fgets(line, 1024, flist) != 0) {
      char* pos = 0;
      if ((pos = strchr(line, '\n')) != 0)
        *pos = '\0';
      process_file(line, i);
    }
    fclose(flist);
  }

  int common = 0, only1 = 0, only2 = 0;

  printf("common = [\n");
  for (auto p : m) {
    if (p.second.size() > 1) {
      printf("(%u,%u,%u),\n", std::get<0>(p.first), std::get<1>(p.first), std::get<2>(p.first));
      ++common;
    }
  }
  printf("]\n\n");

  printf("only1 = [\n");
  for (auto p : m) {
    if (p.second.size() == 1 && p.second.find(0) != p.second.end()) {
      printf("(%u,%u,%u),\n", std::get<0>(p.first), std::get<1>(p.first), std::get<2>(p.first));
      ++only1;
    }
  }
  printf("]\n\n");

  printf("only2 = [\n");
  for (auto p : m) {
    if (p.second.size() == 1 && p.second.find(1) != p.second.end()) {
      printf("(%u,%u,%u),\n", std::get<0>(p.first), std::get<1>(p.first), std::get<2>(p.first));
      ++only2;
    }
  }
  printf("]\n\n");

  fprintf(stderr, "# common: %i   # only in 1: %i   # only in 2: %i\n", common, only1, only2);
}

/*
#sed -n '/only1/,$p' out.py > out2.py

from out2 import *

no_run = True

def foo(l):
    if no_run:
        for r,l,e in l:
            print 'else if (l == %i && e == %i) return false;' % (l, e)
    else:
        for rle in l:
            print 'else if (r == %i && l == %i && e == %i) return false;' % rle

foo(only1)
foo(only2)
*/
