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

    //track rescaler takes in not only a track's pt and eta, but also the type 
    // ie if it is a general track vs. muon or electron candidate 
    TrackRescaler() : enable_(false), era_(0), which_(w_BTagDispJet), type_("") {}
    void setup(bool enable, int era, int which) { enable_ = enable; era_ = era; which_ = which; } //no need to pass track type
    //void setup(bool enable, int era, int which, std::string type) { enable_ = enable; era_ = era; which_ = which;  type_ = type; } //when need track type
    void enable(bool enable) { enable_ = enable; }

    enum { w_BTagDispJet, w_SingleLep, w_JetHT, w_max };

    void set_JetHT2017B(double pt, double eta);
    void set_JetHT2017C(double pt, double eta);
    void set_JetHT2017DE(double pt, double eta);
    void set_JetHT2017F(double pt, double eta);
    void set_JetHT2018A(double pt, double eta);
    void set_JetHT2018B(double pt, double eta);
    void set_JetHT2018C(double pt, double eta);
    void set_JetHT2018D(double pt, double eta);
    void set_BTagDispJet20161(double pt, double eta);
    void set_BTagDispJet20162(double pt, double eta);
    void set_BTagDispJet2017(double pt, double eta);
    void set_BTagDispJet2018(double pt, double eta);

    void set_SingleLep2017(double pt, double eta, std::string type);
    void set_SingleLep2018(double pt, double eta, std::string type);

    void set(double era, int which, double pt, double eta);
    void set(double pt, double eta) { set(era_, which_, pt, eta); }

    //when it is necessary to scale a track based on type
    void set(double era, int which, double pt, double eta, std::string type);
    void set(double pt, double eta, std::string type) { set(era_, which_, pt, eta, type); }

    const Scales& scales() const { return scales_; }
    bool enable() const { return enable_; }
    int era() const { return era_; }
    int which() const { return which_; }
    std::string type() const { return type_; }

#ifndef JMT_STANDALONE
    struct ret_t {
      reco::Track tk;
      reco::Track rescaled_tk;
    };

    ret_t scale(const reco::Track& tk);
    ret_t scale(const reco::Track& tk, std::string type); //when necessary to scale a track based on type
#endif

  private:
    Scales scales_;
    bool enable_;
    int era_;
    int which_;
    std::string type_;
  };
}

#endif
