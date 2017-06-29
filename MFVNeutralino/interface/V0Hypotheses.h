#ifndef JMTucker_MFVNeutralino_V0Hypotheses_h
#define JMTucker_MFVNeutralino_V0Hypotheses_h

namespace mfv {
  enum { V0_K0_2pi, V0_Lambda_p_pi, V0_X_2e, V0_Kp_3pi, n_V0_hyp };

  struct V0Hypothesis {
    const int type;
    const char* name;
    const double mass;
    const std::vector<double> charges_and_masses;
    size_t ndaughters() const { return charges_and_masses.size(); }
    int charge() const { return std::accumulate(charges_and_masses.begin(), charges_and_masses.end(), 0,
                                                [](const int a, const double x) { return a + (x > 0 ? 1 : -1); }); }
  };

  const V0Hypothesis V0_hypotheses[n_V0_hyp] = {
    { V0_K0_2pi,      "K0_2pi",      0.497611, { 0.139570, -0.139570 } },
    { V0_Lambda_p_pi, "Lambda_p_pi", 1.115683, { 0.938272, -0.139570 } },
    // ok these next two aren't "V0" but whatever
    { V0_X_2e,        "X_2e",        0.,       { 0.000511, -0.000511 } },
    { V0_Kp_3pi,      "Kp_3pi",      0.493677, { 0.139570,  0.139570, -0.139570 } },
  };
}

#endif
