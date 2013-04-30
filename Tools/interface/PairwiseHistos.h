#include <vector>
#include "TH1F.h"
#include "TH2F.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "JMTucker/Tools/interface/Utilities.h"

struct PairwiseHistos {
  typedef std::map<std::string, float> PairwiseValueMap;

  struct HistoDef {
    HistoDef(TString name_, TString nice_, int nbins_, float min_, float max_)
      : name(name_), nice(nice_), nbins(nbins_), min(min_), max(max_) {}
    TString name;
    TString nice;
    int nbins;
    float min;
    float max;
  };

  PairwiseHistos() : n(-1) {}

  void Init(const std::vector<HistoDef>& histos, const bool combs_only) {
    n = int(histos.size());
    combinations_only = combs_only;

    edm::Service<TFileService> fs;

    const auto b = histos.begin();
    const auto e = histos.end();
    for (auto i = b; i != e; ++i)
      h1.push_back(fs->make<TH1F>("h_" + i->name, 
				  ";" + i->nice + "; arb. units",
				  i->nbins, i->min, i->max));

    for (auto i = b; i != e; ++i)
      for (auto j = combinations_only ? i+1 : b; j != e; ++j) {
	if (i == j)
	  continue;

	h2.push_back(fs->make<TH2F>("h_" + j->name + "_v_" + i->name,
				    ";" + i->nice + ";" + j->nice,
				    i->nbins, i->min, i->max,
				    j->nbins, j->min, j->max));
      }
  }

  void Fill(const std::vector<float>& values) {
    die_if_not(n > 0, "PairwiseHistos not properly initialized");
    die_if_not(int(values.size()) == n, "wrong size for values: %i != %i expected", values.size(), h1.size());

    int h = 0;
    auto b = values.begin(), e = values.end();
    for (auto i = b; i != e; ++i) {
      int ib = i-b;
      h1[ib]->Fill(values[ib]);

      auto j = combinations_only ? i+1 : b;
      for (; j != e; ++j) {
	if (i == j)
	  continue;

	h2[h++]->Fill(values[ib], values[j-b]);
      }
    }    
  }

  int n;
  bool combinations_only;
  std::vector<TH1F*> h1;
  std::vector<TH2F*> h2;
};
