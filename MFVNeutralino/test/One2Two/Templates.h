#ifndef JMTucker_MFVNeutralino_One2Two_Templates_h
#define JMTucker_MFVNeutralino_One2Two_Templates_h

#include <string>
#include <vector>

class TH1D;

namespace mfv {
  struct TemplatePar {
    // std::string name;
    // double value;
    int nsteps;
    double start;
    double step;
  };

  struct Template {
    int i;
    TH1D* h;

    Template(int i_, TH1D* h_) : i(i_), h(h_) {}
    virtual double chi2() const { return 0; }
    virtual std::string name() const { return std::string("NoName"); }
    virtual std::string title() const { return std::string("NoTitle"); }
    virtual size_t npars() const { return pars.size(); }
    virtual double par(size_t) const { return 0.; }

    static const bool fine_binning;
    static const int nbins;
    static const double min_val;
    static const double max_val;
    static const double bin_width;

    static std::vector<double> binning(const bool shorten_last=false);
    static void deoverflow(TH1D* hh);
    static TH1D* hist_with_binning(const char* name, const char* title);
    static TH1D* finalize_binning(TH1D* h);
    static TH1D* finalize_template(TH1D* h);
    static void finalize_template_in_place(TH1D* h);

    static const int max_npars;
    std::vector<double> pars;
  };

  //////////////////////////////////////////////////////////////////////////////

  struct PhiShiftTemplate : public Template {
    double phi_exp;
    double shift;

    PhiShiftTemplate(int i_, TH1D* h_, const double phi_exp_, const double shift_);

    virtual double chi2() const;
    virtual std::string name() const;
    virtual std::string title() const;
    virtual double par(size_t w) const;
  };

  //////////////////////////////////////////////////////////////////////////////

  struct ClearedJetsTemplate : public Template {
    double clearing_mu;
    double clearing_sigma;

    ClearedJetsTemplate(int i_, TH1D* h_, const double mu, const double sigma);
    virtual std::string name() const;
    virtual std::string title() const;
    virtual double par(size_t w) const;
  };

  //////////////////////////////////////////////////////////////////////////////

  struct SimpleClearingTemplate : public Template {
    double clearing_sigma;

    SimpleClearingTemplate(int i_, TH1D* h_, const double sigma);
    virtual std::string name() const;
    virtual std::string title() const;
    virtual double par(size_t w) const;
  };

  //////////////////////////////////////////////////////////////////////////////

  typedef std::vector<Template*> Templates;

  //////////////////////////////////////////////////////////////////////////////

  struct TemplateInterpolator {
    static int extra_prints;

    Templates* templates;
    int n_bins;
    int n_pars;
    std::vector<TemplatePar> par_infos;

    std::vector<double>& a;

    std::vector<double> curr_pars;
    Templates Q;
    std::vector<std::vector<double> > R;

    TemplateInterpolator(Templates* templates_, int n_bins_,
                         const std::vector<TemplatePar>& par_infos_,
                         std::vector<double>& a_);
    int i_par(int i, double par) const;
    int i_Q(const std::vector<double>& pars) const;
    Template* get_Q(const std::vector<double>& pars) const;
    void interpolate(const std::vector<double>& pars, std::vector<double>* a_p=0);
    void interpolate(double par0, double par1) { interpolate(std::vector<double>({par0,par1})); }
  };
}

#endif
