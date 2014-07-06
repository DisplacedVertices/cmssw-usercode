#include "Fitter.h"

#include <cmath>

#include "TFile.h"
#include "TH2.h"
#include "TMinuit.h"
#include "TRandom3.h"
#include "TTree.h"

#include "Random.h"

namespace mfv {
  namespace fit {
    int n_bins = -1;
    TH1D* h_data = 0;
    Template* curr_bkg_template = 0;
    TH1D* h_sig = 0;

    double twolnL(double mu_sig, double mu_bkg) {
      const TH1D* h_bkg = curr_bkg_template->h_final;
      double lnL = 0;
      for (int i = 1; i <= n_bins; ++i) {
        const double nu_sig = mu_sig * h_sig->GetBinContent(i);
        const double nu_bkg = mu_bkg * h_bkg->GetBinContent(i);
        const double nu_sum = nu_sig + nu_bkg;
        const double nu = nu_sum > 0 ? nu_sum : 1e-300;
        const double n = h_data->GetBinContent(i);
        const double dlnL = -nu + n * log(nu); // log(nu/n);
        lnL += dlnL;
        printf("i: %i   mu_sig, mu_bkg (%f, %f)   nu_bkg: %f  nu_sig: %f  nu: %f  n: %f    dlnL: %f   lnL: %f\n",
               i, mu_sig, mu_bkg, nu_bkg, nu_sig, nu, n, dlnL, lnL);
      }
      return 2*lnL;
    }

    void minfcn(int&, double*, double& f, double* par, int) {
      f = -twolnL(par[0], par[1]); // + curr_bkg_template->chi2();
    }
  }

  const int Fitter::npars = 2 + Template::max_npars;

  Fitter::Fitter(const std::string& name_, TFile* f, TRandom* r)
    : name (name_.size() ? " " + name_ : ""),
      uname(name_.size() ? "_" + name_ : ""),

      env("mfvo2t_fitter" + uname),
      print_level(env.get_int("print_level", 2)),

      fout(f),
      dout(f->mkdir(TString::Format("Fitter%s", uname.c_str()))),
      dtoy(0),
      rand(r),
      seed(r->GetSeed() - jmt::seed_base)
  {
    printf("Fitter%s config:\n", name.c_str());
    printf("seed: %i\n", seed);
    fflush(stdout);

    book_trees();
  }

  void Fitter::book_trees() {
    dout->cd();

    TTree* t_config = new TTree("t_config", "");
    t_config->Branch("seed", const_cast<int*>(&seed), "seed/I");
    t_config->Fill();


    t_fit_info = new TTree("t_fit_info", "");
    t_fit_info->Branch("seed", const_cast<int*>(&seed), "seed/I");
    t_fit_info->Branch("toy", &toy, "toy/I");
  }    

  std::vector<double> Fitter::binning() const {
    std::vector<double> bins;
    for (int i = 0; i < 20; ++i)
      bins.push_back(i * 0.01);
    bins.push_back(0.2);
    bins.push_back(0.4);
    bins.push_back(0.6);
    bins.push_back(1);
    bins.push_back(2);
    bins.push_back(3);
    if (fit::n_bins < 0)
      fit::n_bins = bins.size() - 1;
    return bins;
  }

  TH1D* Fitter::hist_with_binning(const TString& name_, const TString& title) {
    std::vector<double> bins = binning();
    return new TH1D(name_, title, bins.size()-1, &bins[0]);
  }

  TH1D* Fitter::finalize_binning(TH1D* h) {
    std::vector<double> bins = binning();
    TH1D* hh = (TH1D*)h->Rebin(bins.size()-1, TString::Format("%s_rebinned", h->GetName()), &bins[0]);
    const int nb = hh->GetNbinsX();
    const double l  = hh->GetBinContent(nb);
    const double le = hh->GetBinError  (nb);
    const double o  = hh->GetBinContent(nb+1);
    const double oe = hh->GetBinError  (nb+1);
    hh->SetBinContent(nb, l + o);
    hh->SetBinError  (nb, sqrt(le*le + oe*oe));
    hh->SetBinContent(nb+1, 0);
    hh->SetBinError  (nb+1, 0);
    return hh;
  }

  TH1D* Fitter::finalize_template(TH1D* h) {
    TH1D* hh = finalize_binning(h);
    hh->Scale(1./hh->Integral());
    return hh;
  }

  void Fitter::fit_globals_ok() {
    if (fit::n_bins < 0 || fit::h_data == 0 || fit::curr_bkg_template == 0 || fit::h_sig == 0)
      jmt::vthrow("fit globals not set up properly: n_bins: %i  h_data: %p  curr_bkg_template: %p  h_sig: %p",
                  fit::n_bins, fit::h_data, fit::curr_bkg_template, fit::h_sig);
  }

  bool Fitter::scan_likelihood() {
    fit_globals_ok();

    const double mu_sig_min = 0;
    const double mu_sig_max = 100;
    const double mu_bkg_min = 0;
    const double mu_bkg_max = 100;
    const int mu_sig_steps = 200;
    const int mu_bkg_steps = 200;
    const double d_mu_sig = (mu_sig_max - mu_sig_min) / mu_sig_steps;
    const double d_mu_bkg = (mu_bkg_max - mu_bkg_min) / mu_bkg_steps;

    printf("scanning likelihood mu_sig (%f, %f) in %i steps and mu_bkg (%f, %f) in %i steps, with %i templates:\n", mu_sig_min, mu_sig_max, mu_sig_steps, mu_bkg_min, mu_bkg_max, mu_bkg_steps, int(bkg_templates->size()));

    glb_scan_maxtwolnL = -1e300;
    glb_scan_max_pars.assign(5, -1);
    glb_scan_max_pars_errs.assign(5, -1);

    TDirectory* d = dtoy->mkdir("scan_likelihood");
    d->cd();

    for (size_t i_template = 0, i_template_e = bkg_templates->size(); i_template < i_template_e; ++i_template) {
      Template* bkg_template = bkg_templates->at(i_template);
      fit::curr_bkg_template = bkg_template;

      TH2F* h = new TH2F(TString::Format("h_likelihood_template%s", bkg_template->name().c_str()),
                         TString::Format("%s;#mu_{sig};#mu_{bkg}", bkg_template->title().c_str()),
                         mu_sig_steps, mu_sig_min, mu_sig_max,
                         mu_bkg_steps, mu_bkg_min, mu_bkg_max);

      double maxtwolnL = -1e300;
      std::vector<double> max_pars(npars);
      max_pars[0] = max_pars[1] = -1;
      for (int ipar = 2; ipar < npars; ++ipar)
        max_pars[ipar] = bkg_template->par(ipar-2);

      for (int i_mu_sig = 0; i_mu_sig < mu_sig_steps; ++i_mu_sig) {
        const double mu_sig = mu_sig_min + i_mu_sig * d_mu_sig;
        for (int i_mu_bkg = 0; i_mu_bkg < mu_bkg_steps; ++i_mu_bkg) {
          const double mu_bkg = mu_bkg_min + i_mu_bkg * d_mu_bkg;

          const double twolnL_ = fit::twolnL(mu_sig, mu_bkg);
          h->SetBinContent(i_mu_sig+1, i_mu_bkg+1, twolnL_);

          if (twolnL_ > maxtwolnL) {
            maxtwolnL = twolnL_;
            max_pars[0] = mu_sig;
            max_pars[1] = mu_bkg;
          }
        }
      }

      printf("%s (%s) max 2lnL = %f  for  mu_sig = %f  mu_bkg = %f\n", h->GetName(), h->GetTitle(), maxtwolnL, max_pars[0], max_pars[1]);
      if (maxtwolnL > glb_scan_maxtwolnL) {
        printf("  ^ new global max!\n");
        glb_scan_maxtwolnL = maxtwolnL;
        for (int ipar = 0; ipar < npars; ++ipar)
          glb_scan_max_pars[ipar] = max_pars[ipar];
      }
    }

    return glb_scan_maxtwolnL > -1e300;
  }

  bool Fitter::scanmin_likelihood(bool bkg_only) {
    fit_globals_ok();

    std::vector<int> istats;
    bool all_ok = true;

    glb_scanmin_maxtwolnL = -1e300;
    glb_scanmin_max_pars.assign(5, -1);
    glb_scanmin_max_pars_errs.assign(5, -1);

    printf("scanminning (bkg_only = %i): ", bkg_only);

    TDirectory* d = dtoy->mkdir("scanmin_likelihood");
    d->cd();

    for (size_t i_template = 0, i_template_e = bkg_templates->size(); i_template < i_template_e; ++i_template) {
      Template* bkg_template = bkg_templates->at(i_template);
      fit::curr_bkg_template = bkg_template;

      TMinuit* m = new TMinuit(2);
      m->SetPrintLevel(print_level);
      m->SetFCN(fit::minfcn);
      int ierr;
      m->mnparm(0, "mu_sig", 0 , 0.1, 0, 0, ierr);
      m->mnparm(1, "mu_bkg", 40, 0.1, 0, 0, ierr);

      if (bkg_only)
        m->FixParameter(0);

      m->Migrad();
      //m->mnmnos();
      double fmin, fedm, errdef;
      int npari, nparx, istat;
      m->mnstat(fmin, fedm, errdef, npari, nparx, istat);

      const double maxtwolnL = -fmin;
      double mu_sig, err_mu_sig, mu_bkg, err_mu_bkg;
      m->GetParameter(0, mu_sig, err_mu_sig);
      m->GetParameter(1, mu_bkg, err_mu_bkg);

      printf("scanmin_likelihood: %s  istat: %i   maxtwolnL: %e   mu_sig: %f +- %f  mu_bkg: %f +- %f\n", bkg_template->title().c_str(), istat, maxtwolnL, mu_sig, err_mu_sig, mu_bkg, err_mu_bkg);

      if (maxtwolnL > glb_scanmin_maxtwolnL) {
        printf("  ^ new global max!\n");
        glb_scanmin_maxtwolnL = maxtwolnL;
        glb_scanmin_max_pars[0] = mu_sig;
        glb_scanmin_max_pars[1] = mu_bkg;
        glb_scanmin_max_pars_errs[0] = err_mu_sig;
        glb_scanmin_max_pars_errs[1] = err_mu_bkg;
        for (int ipar = 2; ipar < npars; ++ipar)
          glb_scanmin_max_pars[ipar] = bkg_template->par(ipar-2); 
      }

      istats.push_back(istat);
      if (istat != 3)
        all_ok = false;

      delete m;
    }

    return all_ok;
  }

  void Fitter::fit(int toy_, Templates* bkg_templates_, TH1D* sig_template, const VertexPairs& v2v) {
    toy = toy_;

    dtoy = dout->mkdir(TString::Format("seed%04i_toy%04i", seed, toy));
    TDirectory* d = dtoy->mkdir("finalized_templates");
    d->cd();

    bkg_templates = bkg_templates_;
    for (Template* t : *bkg_templates)
      t->h_final = finalize_template(t->h);

    fit::curr_bkg_template = (*bkg_templates)[0];
    fit::h_sig = finalize_template(sig_template);

    fit::h_data = hist_with_binning("h_data", TString::Format("toy %i", toy));
    for (const VertexPair& p : v2v)
      fit::h_data->Fill(p.d2d());

    scan_likelihood();
    scanmin_likelihood(false);
  }
}
