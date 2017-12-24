#ifndef JMTucker_MFVNeutralino_One2Two_Samples
#define JMTucker_MFVNeutralino_One2Two_Samples

namespace mfv {
  struct Sample {
    bool use;
    int key;
    std::string name;
    double xsec;
    double nevents;
    Sample() : key(0), name("invalid"), xsec(0), nevents(0) {}
    Sample(int k, const std::string& nm, double x, int ne) : key(k), name(nm), xsec(x), nevents(ne) {}

    double partial_weight() const { return xsec / nevents; }
    double weight(double int_lumi) const { return partial_weight() * int_lumi; }
    bool is_sig() const { return key < 0; }
    bool is_data() const { return key == 0; }
  };

  struct Samples {
    const Sample invalid;
    std::vector<Sample> samples;

    Samples()
      : samples({
          //{0, "JetHT", -1, -1},

          //{4, "qcdht0500sum", , },
          //{5, "qcdht0700sum", , },
          //{6, "qcdht1000sum", , },
          {7, "qcdht1500sum", 120,    11839357},
          {8, "qcdht2000sum", 25.3,    6039005},

          {9, "ttbar", 832., 43662343},

          {99, "bkgsyst", 245.8 * 0.457, 5000000},
        })
    {
      int i = -1;
#if 0
      const std::vector<int> masses = { 400, 800, 1200, 1600 };
      const std::vector<int> taus = { 100, 300, 1000, 10000 };
      char buf[128];
      for (int t : taus)
        for (int m : masses) {
          snprintf(buf, 128, "mfv_neu_tau%05ium_M%04i", t, m);
          samples.push_back({i--, std::string(buf), 1e-3, 10000});
        }
#else
#include "signals.h"
#endif
      i = -99;
      samples.push_back({i, "sigsyst", 1e-3, 10000});

      printf("Samples():\n");
      for (const Sample& s : samples)
        printf("key = %3i: name = %40s\n", s.key, s.name.c_str());
    }

    const Sample& get(int i) const {
      for (const Sample& s : samples)
        if (s.key == i)
          return s;
      return invalid;
    }

    const Sample& get(const std::string& n) const {
      for (const Sample& s : samples)
        if (s.name == n)
          return s;
      return invalid;
    }
  };
}

#endif
