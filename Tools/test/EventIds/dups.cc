// e.g. EVENTIDSREADER_PRINTS=1 EVENTIDSREADER_IS_MC=1 ./dups.exe EventIdRecorder/event_ids root://cmseos.fnal.gov//store/user/tucker/TTJets_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8/EventIdsV21m_NTkSeeds2_2017/181127_180141/0000/evids_%i.root  root://cmseos.fnal.gov//store/user/tucker/TTJets_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8/EventIdsV21m_NTkSeeds2_2017/181127_180141/0000/evids_{0..271}.root

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
    //p.first.print(stdout, true);
    if (p.second.size() > 1) {
      if (dup_count == 0)
        printf("duplicates:\n");
      p.first.print(stdout);
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
