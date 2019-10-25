#ifndef JMTucker_Tools_TrackRescaler_h
#define JMTucker_Tools_TrackRescaler_h

#ifndef JMT_STANDALONE
#include "DataFormats/TrackReco/interface/Track.h"
#endif

namespace jmt {
  class TrackRescaler {
  public:
    class Scales {
    public:
      Scales() : dxyerr_(1), dszerr_(1), dxydszcov_(1) {}
      void reset() { dxyerr_ = dszerr_ = dxydszcov_ = 1; }
      void set(double dxyerr, double dszerr, double dxydszcov) {
        dxyerr_ = dxyerr;
        dszerr_ = dszerr;
        dxydszcov_ = dxydszcov;
      }

      double dxyerr() const { return dxyerr_; }
      double dszerr() const { return dszerr_; }
      double dxydszcov() const { return dxydszcov_; }
      double dxycov() const { return pow(dxyerr_, 2); }
      double dszcov() const { return pow(dszerr_, 2); }

      double dxycov(double c) const { return c * dxycov(); }
      double dszcov(double c) const { return c * dszcov(); }
      double dxydszcov(double c) const { return c * dxydszcov(); }

    private:
      double dxyerr_;
      double dszerr_;
      double dxydszcov_;
    };

    TrackRescaler() : enable_(false), era_(0), which_(w_JetHT) {}
    void setup(bool enable, int era, int which) { enable_ = enable; era_ = era; which_ = which; }
    void enable(bool enable) { enable_ = enable; }

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
    void set(double pt, double eta) { set(era_, which_, pt, eta); }

    const Scales& scales() const { return scales_; }
    bool enable() const { return enable_; }
    int era() const { return era_; }
    int which() const { return which_; }

#ifndef JMT_STANDALONE
    struct ret_t {
      reco::Track tk;
      reco::Track rescaled_tk;
    };

    ret_t scale(const reco::Track& tk);
#endif

  private:
    Scales scales_;
    bool enable_;
    int era_;
    int which_;
  };
}

#endif
