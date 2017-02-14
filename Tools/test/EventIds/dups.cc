#include "EventIdsReader.h"

int main(int argc, char** argv) {
  if (argc < 3) {
    fprintf(stderr, "usage: dups path_to_tree [scan_format] input_1.root [input_2.root ...] \n");
    return 1;
  }

  EventIdsReader reader;

  const char* path = argv[1];
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

    reader.process_file(argv[i], path, fileno);
  }

  int dup_count = 0;
  for (auto p : reader.m) {
    if (p.second.size() > 1) {
      if (dup_count == 0)
        printf("duplicates:\n");
      p.first.print();
      printf(" : [");
      for (int fno : p.second)
        printf("%i, ", fno);
      printf("]\n");
      ++dup_count;
    }
  }

  if (dup_count == 0)
    printf("OK!\n");

  return dup_count > 0;
}
