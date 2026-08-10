#include <vector>
#include "TH2.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "JMTucker/Tools/interface/Utilities.h"

struct PairwiseHistos {
  typedef float Value;
  typedef std::map<std::string, Value> ValueMap;
  Value get(const ValueMap& m, const std::string& s, bool allow_default=false, Value default_=0) {
    auto it = m.find(s);
    if (it == m.end()) {
      if (!allow_default)
	throw cms::Exception("PairwiseHistos") << s << " not found in ValueMap";
      return default_;
    }
    return it->second;
  }

  struct HistoDef {
    HistoDef(const std::string& name_, const std::string& nice_, int nbins_, float min_, float max_)
      : name(name_), nice(nice_), nbins(nbins_), min(min_), max(max_) {}
    std::string name;
    std::string nice;
    int nbins;
    float min;
    float max;
  };

  struct HistoDefs {
    typedef std::vector<HistoDef> C;
    C defs;

    size_t size() const { return defs.size(); }
    C::const_iterator begin() const { return defs.begin(); }
    C::const_iterator end()   const { return defs.end();   }

    void add(const TString& name, const TString& nice, int nbins, float min, float max) {
      defs.push_back(HistoDef(name.Data(), nice.Data(), nbins, min, max));
    }
  };

  PairwiseHistos() : n(-1) {}

  void Init(const std::string& name, const HistoDefs& histos, const bool combs_only, const bool do2d, const int sumto=-1) {
    n = int(histos.size());
    do_2d = do2d;
    combinations_only = combs_only;

    sums_mode = sumto > 0;
    sum_to = sumto;
    sums.clear();

    edm::Service<TFileService> fs;

    const auto b = histos.begin();
    const auto e = histos.end();
    for (auto i = b; i != e; ++i) {
      names.push_back(i->name);
      h1.insert({i->name,
                    fs->make<TH1F>((name + "_" + i->name).c_str(), 
                                   (";" + i->nice + "; arb. units").c_str(),
                                   i->nbins, i->min, i->max)
                    });
    }

    if (!do_2d)
      return;

    for (auto i = b; i != e; ++i)
      for (auto j = combinations_only ? i+1 : b; j != e; ++j) {
        if (i == j)
          continue;

        h2.insert({std::make_pair(i->name, j->name),
                      fs->make<TH2F>((name + "_" + j->name + "_v_" + i->name).c_str(),
                                     (";" + i->nice + ";" + j->nice).c_str(),
                                     i->nbins, i->min, i->max,
                                     j->nbins, j->min, j->max)
                      });
      }
  }

  void Fill(const ValueMap& values, const int fill_num=-1, const double weight=1.) {
    die_if_not(n > 0, "PairwiseHistos not properly initialized");
    if (int(values.size()) != n) {
      cms::Exception ce("PairwiseHistos", "wrong size for values: ");
      ce << values.size() << " != " << h1.size() << " expected:\nvalues' names:\n";
      for (const auto& v : values)
        ce << v.first << "\n";
      ce << "expected names:\n";
      for (const auto& v : h1)
        ce << v.first << "\n";
      throw ce;
    }

    const auto b = names.begin();
    const auto e = names.end();

    for (auto i = b; i != e; ++i)
      die_if_not(values.find(*b) != values.end(), "var %s not found in value map and allow_default=false", b->c_str());

    if (sums_mode) {
      if (fill_num < sum_to)
        for (auto i = b; i != e; ++i)
          sums[*i] = get(values, *i) + get(sums, *i, true, 0);

      if (fill_num != sum_to - 1)
        return;
    }
      
    const ValueMap& to_fill = sums_mode ? sums : values;

    for (auto i = b; i != e; ++i) {
      const float vi = get(to_fill, *i);
      h1[*i]->Fill(vi, weight);
      
      if (!do_2d)
        continue;

      auto j = combinations_only ? i+1 : b;
      for (; j != e; ++j) {
	if (i == j)
	  continue;

	const float vj = get(to_fill, *j);
	h2[std::make_pair(*i, *j)]->Fill(vi, vj, weight);
      }
    }

    if (sums_mode)
      sums.clear();
  }

  int n;
  bool do_2d;
  bool combinations_only;
  std::vector<std::string> names;
  std::map<std::string, TH1F*> h1;
  std::map<std::pair<std::string, std::string>, TH2F*> h2;

  bool sums_mode;
  int sum_to;
  ValueMap sums;
};
