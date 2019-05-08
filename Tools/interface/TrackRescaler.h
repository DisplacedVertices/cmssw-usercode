#ifndef JMTucker_Tools_TrackRescaler_h
#define JMTucker_Tools_TrackRescaler_h

#include "DataFormats/TrackReco/interface/Track.h"

namespace jmt {
  class TrackRescaler {
    struct scales_t {
      scales_t() : dxyerr(1), dszerr(1), dxydszcov(1) {}
      double dxyerr;
      double dszerr;
      double dxydszcov;
    } scales_;

  public:
    enum { w_JetHT, w_max };

    void set_JetHT2017B(double pt, double eta);
    void set_JetHT2017C(double pt, double eta);
    void set_JetHT2017DE(double pt, double eta);
    void set_JetHT2017F(double pt, double eta);
    void set_JetHT2018A(double pt, double eta);
    void set_JetHT2018B(double pt, double eta);
    void set_JetHT2018C(double pt, double eta);
    void set_JetHT2018D(double pt, double eta);

    void set(double era, int which, double pt, double eta);

    struct ret_t {
      //reco::TrackBase::ParameterVector val;
      reco::TrackBase::CovarianceMatrix cov;
    };

    ret_t scale(const reco::Track& tk, bool enable, int era, int which);
  };
}

#endif
