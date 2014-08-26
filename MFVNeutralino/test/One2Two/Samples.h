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
  };

  struct Samples {
    const Sample invalid;
    std::vector<Sample> samples;

    Samples()
      : samples({
          //{1, "qcdht0100", 1.04e7, 50129518/2},
          //{2, "qcdht0250", 2.76e5, 27062078/2},
          {3, "qcdht0500", 8.43e3, 30599292/2},
          {4, "qcdht1000", 2.04e2, 13843863/2},

          {5, "ttbarhadronic", 245.8 * 0.457, 10537444/2},
          {6, "ttbarsemilep",  245.8 * 0.438, 25424818/2},
          {7, "ttbardilep",    245.8 * 0.105, 12119013/2},
        })
    {
      int i = -1;
      const std::vector<int> masses = { 200, 300, 400, 600, 800, 1000 };
      const std::vector<int> taus = { 100, 300, 1000, 9900 };
      char buf[128];
      for (int t : taus)
        for (int m : masses) {
          snprintf(buf, 128, "mfv_neutralino_tau%04ium_M%04i", t, m);
          samples.push_back({i--, std::string(buf), 1e-3, 100000});
        }
      i = -99;
      samples.push_back({i, "sigsyst", 1e-3, 100000});
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
