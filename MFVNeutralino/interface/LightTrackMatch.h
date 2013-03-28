#ifndef JMTucker_MFVNeutralino_LightTrackMatch_h
#define JMTucker_MFVNeutralino_LightTrackMatch_h

struct LightTrackMatch {
  LightTrackMatch(double qual, double pt, double eta, double phi, int ndx, bool other, bool lsp) : quality(qual), gen_pt(pt), gen_eta(eta), gen_phi(phi), gen_ndx(ndx), other_matches(other), matches_lsp(lsp) {}
  LightTrackMatch() {}

  double quality;
  double gen_pt;
  double gen_eta;
  double gen_phi;
  int gen_ndx;
  bool other_matches;
  bool matches_lsp;
};

#endif
