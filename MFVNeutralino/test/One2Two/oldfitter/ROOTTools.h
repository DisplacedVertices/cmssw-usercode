#ifndef JMTucker_MFVNeutralino_One2Two_ROOTTools_h
#define JMTucker_MFVNeutralino_One2Two_ROOTTools_h

class TGraphAsymmErrors;
class TH1;
class TH1D;
class TPaveStats;

namespace jmt {
  void cumulate(TH1D* h, const bool do_overflow);
  void deoverflow(TH1D* h);
  void deunderflow(TH1D* h);
  void divide_by_bin_width(TH1D* h);
  double integral(const TH1* h);
  TPaveStats* move_stat_box(TPaveStats* s, double dx, double dy);
  TPaveStats* move_stat_box(TH1* h, double dx, double dy);
  TPaveStats* move_stat_box(TPaveStats* s, double x1, double y1, double x2, double y2);
  TPaveStats* move_stat_box(TH1* h, double x0, double y0, double x1, double y1);
  TGraphAsymmErrors* poisson_intervalize(const TH1D* h, const bool zero_x=false, const bool include_zero_bins=false);
  void set_root_style();
  TH1D* shift_hist(const TH1D* h, const int shift);
}

#endif
