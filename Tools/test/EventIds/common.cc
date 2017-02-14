#include "EventIdsReader.h"

int main(int argc, char** argv) {
  if (argc < 5) {
    fprintf(stderr, "usage: common path1 filelist1.txt path2 filelist2.txt\n");
    return 1;
  }

  EventIdsReader reader;
  //reader.prints = true;

  const char* paths[2] = { argv[1], argv[3] };
  const char* filelist[2] = { argv[2], argv[4] };
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

      try {
        reader.process_file(line, paths[i], i);
      }
      catch (const std::exception& e) {
        fprintf(stderr, "exception caught: %s\n", e.what());
        return 1;
      }
    }

    fclose(flist);
  }

  int common = 0, only1 = 0, only2 = 0;

#if 0
  printf("common = [\n");
  for (auto p : reader.m) {
    if (p.second.size() > 1) {
      p.first.print();
      printf(",\n");
      ++common;
    }
  }
  printf("]\n\n");
#endif

  printf("only1 = [\n");
  for (auto p : reader.m) {
    if (p.second.size() == 1 && p.second.find(0) != p.second.end()) {
      p.first.print();
      printf(",\n");
      ++only1;
    }
  }
  printf("]\n\n");

  printf("only2 = [\n");
  for (auto p : reader.m) {
    if (p.second.size() == 1 && p.second.find(1) != p.second.end()) {
      p.first.print();
      printf(",\n");
      ++only2;
    }
  }
  printf("]\n\n");

  printf("# common: %i   # only in 1: %i   # only in 2: %i\n", common, only1, only2);
}

/*
#sed -n '/only1/,$p' out.py > out2.py

from out2 import *

no_run = True

def foo(s):
    if no_run:
        for r,l,e in s:
            print 'else if (l == %i && e == %i) return false;' % (l, e)
    else:
        for rle in s:
            print 'else if (r == %i && l == %i && e == %i) return false;' % rle

foo(only1)
foo(only2)
*/
