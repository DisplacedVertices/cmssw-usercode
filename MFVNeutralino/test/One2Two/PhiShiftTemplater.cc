#include "PhiShiftTemplater.h"
#include "TF1.h"
#include "TFile.h"
#include "TFitResult.h"
#include "TH2D.h"
#include "TRandom3.h"
#include "TTree.h"
#include "Phi.h"
#include "Prob.h"
#include "ProgressBar.h"
#include "ROOTTools.h"
#include "Random.h"
#include "Templates.h"

namespace mfv {
  double fcn_g_phi(const double* x, const double* par) {
    return par[0] * (par[1] + par[2]*fabs(x[0] - M_PI_2))/(par[1]*M_PI + par[2]*2.46740110);
  }

  double fcn_f_phi(const double* x, const double* par) {
    const double p1 = par[1] + 1;
    return par[0] * (par[2] + pow(fabs(x[0]), par[1])/(par[2]*M_PI + pow(M_PI, p1)/p1));
  }

  double fcn_fg_dz(const double* x, const double* par) {
    const double xx = x[0] - par[2];
    return par[0] * exp(-xx*xx/2./par[1]/par[1])/sqrt(2.*M_PI)/par[1];
  }

  double accept_prob(const double f, const double g, const double M) {
    return f/(M*g);
  }

  bool accept(TRandom* rand, const double f, const double g, const double M) {
    return rand->Rndm() < accept_prob(f, g, M);
  }

  std::vector<TemplatePar> PhiShiftTemplater::par_info() const {
    return std::vector<TemplatePar>({
        { n_phi_total, phi_exp_min, d_phi_interp },
        { n_shift, 0, Template::bin_width }
      });
  }

  PhiShiftTemplater::PhiShiftTemplater(const std::string& name_, TFile* f, TRandom* r)
    : Templater("PhiShift", name_, f, r),

      env("mfvo2t_phishift" + uname),
      d2d_cut(env.get_double("d2d_cut", 0.05)),
      sampling_type(env.get_int("sampling_type", 2)),
      sample_count(env.get_int("sample_count", -1)),
      n_phi_exp(env.get_int("n_phi_exp", 25)),
      phi_exp_min(env.get_double("phi_exp_min", 0.)),
      d_phi_exp(env.get_double("d_phi_exp", 0.25)),
      n_phi_interp(env.get_int("n_phi_interp", 20)),
      d_phi_interp(d_phi_exp/n_phi_interp),
      n_phi_total((n_phi_exp - 1) * n_phi_interp + 1),
      n_shift(env.get_int("n_shift", 40)),
      find_g_phi(env.get_bool("find_g_phi", true)),
      find_g_dz(env.get_bool("find_g_dz", true)),
      find_f_phi(env.get_bool("find_f_phi", true)),
      find_f_dz(env.get_bool("find_f_dz", false)),
      find_f_phi_bkgonly(env.get_bool("find_f_phi_bkgonly", true)),
      find_f_dz_bkgonly(env.get_bool("find_f_dz_bkgonly", false))
  {
    if (sampling_type != 2)
      jmt::vthrow("sampling_type must be 2");

    printf("PhiShiftTemplater%s config:\n", name.c_str());
    printf("seed: %i\n", seed);
    printf("d2d_cut: %f\n", d2d_cut);
    printf("sampling_type: %i\n", sampling_type);
    printf("sample_count: %i\n", sample_count);
    printf("phi_exp: %i increments of %f starting from %f\n", n_phi_exp, d_phi_exp, phi_exp_min);
    printf("n_phi_interp: %i -> d_phi overall = %f\n", n_phi_interp, d_phi_exp/n_phi_interp);
    printf("n_phi_total: %i  n_shift: %i  n_templates: %i\n", n_phi_total, n_shift, n_phi_total * n_shift);
    printf("find gs: phi? %i dz? %i   fs: phi? %i (bkgonly? %i) dz? %i (bkgonly? %i)\n", find_g_phi, find_g_dz, find_f_phi, find_f_phi_bkgonly, find_f_dz, find_f_dz_bkgonly);
    fflush(stdout);

    book_trees();
  }

  void PhiShiftTemplater::book_trees() {
    dout->cd();

    TTree* t_config = new TTree("t_config", "");
    t_config->Branch("seed", const_cast<int*>(&seed), "seed/I");
    t_config->Branch("d2d_cut", const_cast<double*>(&d2d_cut), "d2d_cut/D");
    t_config->Branch("sampling_type", const_cast<int*>(&sampling_type), "sampling_type/I");
    t_config->Branch("sample_count", const_cast<int*>(&sample_count), "sample_count/I");
    t_config->Branch("n_phi_exp", const_cast<int*>(&n_phi_exp), "n_phi_exp/I");
    t_config->Branch("phi_exp_min", const_cast<double*>(&phi_exp_min), "phi_exp_min/D");
    t_config->Branch("d_phi_exp", const_cast<double*>(&d_phi_exp), "d_phi_exp/D");
    t_config->Branch("n_phi_interp", const_cast<int*>(&n_phi_interp), "n_phi_interp/I");
    t_config->Branch("n_shift", const_cast<int*>(&n_shift), "n_shift/I");
    t_config->Branch("find_g_phi", const_cast<bool*>(&find_g_phi), "find_g_phi/O");
    t_config->Branch("find_g_dz", const_cast<bool*>(&find_g_dz), "find_g_dz/O");
    t_config->Branch("find_f_phi", const_cast<bool*>(&find_f_phi), "find_f_phi/O");
    t_config->Branch("find_f_dz", const_cast<bool*>(&find_f_dz), "find_f_dz/O");
    t_config->Branch("find_f_phi_bkgonly", const_cast<bool*>(&find_f_phi_bkgonly), "find_f_phi_bkgonly/O");
    t_config->Branch("find_f_dz_bkgonly", const_cast<bool*>(&find_f_dz_bkgonly), "find_f_dz_bkgonly/O");
    t_config->Fill();


    t_fit_info = new TTree("t_fit_info", "");
    t_fit_info->Branch("seed", const_cast<int*>(&seed), "seed/I");
    t_fit_info->Branch("toy", &dataset.toy, "toy/I");
    t_fit_info->Branch("g_phi_mean", &b_g_phi_mean, "g_phi_mean/F");
    t_fit_info->Branch("g_phi_mean_err", &b_g_phi_mean_err, "g_phi_mean_err/F");
    t_fit_info->Branch("g_phi_rms", &b_g_phi_rms, "g_phi_rms/F");
    t_fit_info->Branch("g_phi_rms_err", &b_g_phi_rms_err, "g_phi_rms_err/F");
    t_fit_info->Branch("g_phi_fit_offset", &b_g_phi_fit_offset, "g_phi_fit_offset/F");
    t_fit_info->Branch("g_phi_fit_offset_err", &b_g_phi_fit_offset_err, "g_phi_fit_offset_err/F");
    t_fit_info->Branch("g_phi_fit_slope", &b_g_phi_fit_slope, "g_phi_fit_slope/F");
    t_fit_info->Branch("g_phi_fit_slope_err", &b_g_phi_fit_slope_err, "g_phi_fit_slope_err/F");
    t_fit_info->Branch("g_phi_fit_chi2", &b_g_phi_fit_chi2, "g_phi_fit_chi2/F");
    t_fit_info->Branch("g_phi_fit_ndf", &b_g_phi_fit_ndf, "g_phi_fit_ndf/F");
    t_fit_info->Branch("g_dz_mean", &b_g_dz_mean, "g_dz_mean/F");
    t_fit_info->Branch("g_dz_mean_err", &b_g_dz_mean_err, "g_dz_mean_err/F");
    t_fit_info->Branch("g_dz_rms", &b_g_dz_rms, "g_dz_rms/F");
    t_fit_info->Branch("g_dz_rms_err", &b_g_dz_rms_err, "g_dz_rms_err/F");
    t_fit_info->Branch("g_dz_fit_sigma", &b_g_dz_fit_sigma, "g_dz_fit_sigma/F");
    t_fit_info->Branch("g_dz_fit_sigma_err", &b_g_dz_fit_sigma_err, "g_dz_fit_sigma_err/F");
    t_fit_info->Branch("g_dz_fit_mu", &b_g_dz_fit_mu, "g_dz_fit_mu/F");
    t_fit_info->Branch("g_dz_fit_mu_err", &b_g_dz_fit_mu_err, "g_dz_fit_mu_err/F");
    t_fit_info->Branch("g_dz_fit_chi2", &b_g_dz_fit_chi2, "g_dz_fit_chi2/F");
    t_fit_info->Branch("g_dz_fit_ndf", &b_g_dz_fit_ndf, "g_dz_fit_ndf/F");
    t_fit_info->Branch("f_phi_mean", &b_f_phi_mean, "f_phi_mean/F");
    t_fit_info->Branch("f_phi_mean_err", &b_f_phi_mean_err, "f_phi_mean_err/F");
    t_fit_info->Branch("f_phi_rms", &b_f_phi_rms, "f_phi_rms/F");
    t_fit_info->Branch("f_phi_rms_err", &b_f_phi_rms_err, "f_phi_rms_err/F");
    t_fit_info->Branch("f_phi_asym", &b_f_phi_asym, "f_phi_asym/F");
    t_fit_info->Branch("f_phi_asym_err", &b_f_phi_asym_err, "f_phi_asym_err/F");
    t_fit_info->Branch("f_phi_fit_exp", &b_f_phi_fit_exp, "f_phi_fit_exp/F");
    t_fit_info->Branch("f_phi_fit_exp_err", &b_f_phi_fit_exp_err, "f_phi_fit_exp_err/F");
    t_fit_info->Branch("f_phi_fit_offset", &b_f_phi_fit_offset, "f_phi_fit_offset/F");
    t_fit_info->Branch("f_phi_fit_offset_err", &b_f_phi_fit_offset_err, "f_phi_fit_offset_err/F");
    t_fit_info->Branch("f_phi_fit_chi2", &b_f_phi_fit_chi2, "f_phi_fit_chi2/F");
    t_fit_info->Branch("f_phi_fit_ndf", &b_f_phi_fit_ndf, "f_phi_fit_ndf/F");
    t_fit_info->Branch("f_dz_mean", &b_f_dz_mean, "f_dz_mean/F");
    t_fit_info->Branch("f_dz_mean_err", &b_f_dz_mean_err, "f_dz_mean_err/F");
    t_fit_info->Branch("f_dz_rms", &b_f_dz_rms, "f_dz_rms/F");
    t_fit_info->Branch("f_dz_rms_err", &b_f_dz_rms_err, "f_dz_rms_err/F");
    t_fit_info->Branch("f_dz_fit_sigma", &b_f_dz_fit_sigma, "f_dz_fit_sigma/F");
    t_fit_info->Branch("f_dz_fit_sigma_err", &b_f_dz_fit_sigma_err, "f_dz_fit_sigma_err/F");
    t_fit_info->Branch("f_dz_fit_mu", &b_f_dz_fit_mu, "f_dz_fit_mu/F");
    t_fit_info->Branch("f_dz_fit_mu_err", &b_f_dz_fit_mu_err, "f_dz_fit_mu_err/F");
    t_fit_info->Branch("f_dz_fit_chi2", &b_f_dz_fit_chi2, "f_dz_fit_chi2/F");
    t_fit_info->Branch("f_dz_fit_ndf", &b_f_dz_fit_ndf, "f_dz_fit_ndf/F");
  }    

  void PhiShiftTemplater::book_toy_fcns_and_histos() {
    Templater::book_hists();

    g_phi = new TF1("g_phi", fcn_g_phi, Phi::min, Phi::max, 3);
    f_phi = new TF1("f_phi", fcn_f_phi, Phi::min, Phi::max, 3);
    g_dz  = new TF1("g_dz", fcn_fg_dz, -40, 40, 3);
    f_dz  = new TF1("f_dz", fcn_fg_dz, -40, 40, 3);
    g_phi->SetParNames("norm", "offset", "slope");
    f_phi->SetParNames("norm", "exp", "offset");
    for (TF1* fcn : {g_dz, f_dz})
      fcn->SetParNames("norm", "sigma", "mu");
    for (TF1* fcn : {g_phi, f_phi, g_dz, f_dz})
      fcn->FixParameter(0, 1.);


    h_1v_g_phi  = Phi::new_1d_hist("h_1v_g_phi",  "");
    h_fcn_g_phi = Phi::new_1d_hist("h_fcn_g_phi", "");
    h_1v_g_dz  = new TH1D("h_1v_g_dz",  "", 200, -40,  40);
    h_fcn_g_dz = new TH1D("h_fcn_g_dz", "",  20, -40,  40);

    h_fcn_f_phi = Phi::new_1d_hist("h_fcn_f_phi", "");
    h_fcn_f_dz = new TH1D("h_fcn_f_dz", "", 20, -0.1, 0.1);

    h_fcn_f_phis.clear();
    for (int i_phi_exp = 0; i_phi_exp < n_phi_exp; ++i_phi_exp) {
      double phi_exp = phi_exp_min + i_phi_exp * d_phi_exp;
      h_fcn_f_phis.push_back(Phi::new_1d_hist(TString::Format("h_fcn_f_phis_%i", i_phi_exp), TString::Format("phi_exp = %f", phi_exp)));
    }
  }

  bool PhiShiftTemplater::is_sideband(const VertexSimple& v0, const VertexSimple& v1) const {
    return v0.d2d(v1) < d2d_cut;
  }

  void PhiShiftTemplater::fit_envelopes() {
    if (!dataset.ok())
      jmt::vthrow("PhiShiftTemplater::fit_envelopes: must set vertices before using them");

    printf("PhiShiftTemplater%s: fitting envelopes\n", name.c_str()); fflush(stdout);

    const VertexSimples& v1v = *dataset.one_vertices;
    const int N1v = sample_count > 0 ? sample_count : int(v1v.size());

    // Fill the envelope histos to be fit with all unique 1v pairs.
    for (int i = 0; i < N1v; ++i) {
      for (int j = i+1; j < N1v; ++j) {
        const double phi = v1v[i].phi(v1v[j]);
        h_1v_g_phi->Fill(Phi::use_abs ? fabs(phi) : phi);
        h_1v_g_dz->Fill(v1v[i].dz(v1v[j]));
      }
    }

    if (find_g_phi) {
      h_1v_g_phi->Scale(1./h_1v_g_phi->Integral());
      const double integxwidth = h_1v_g_phi->Integral() * h_1v_g_phi->GetXaxis()->GetBinWidth(1);
      TF1* g_phi_temp = new TF1("g_phi_temp", fcn_g_phi, g_phi->GetXmin(), g_phi->GetXmax(), 3);
      for (int i = 0; i < 3; ++i)
        g_phi_temp->SetParName(i, g_phi->GetParName(i));
      g_phi_temp->FixParameter(0, integxwidth);
      g_phi_temp->SetParameter(1, 0.125);
      g_phi_temp->SetParameter(2, 5e-4);
      TFitResultPtr res = h_1v_g_phi->Fit("g_phi_temp", "0RQS");
      printf("  h_1v_g_phi mean %.3f +- %.3f  rms %.3f +- %.3f   g_phi fit offset %.4f +- %.4f  slope %.4f +- %.4f  chi2/ndf = %6.3f/%i = %6.3f   prob: %g\n",
             h_1v_g_phi->GetMean(), h_1v_g_phi->GetMeanError(),
             h_1v_g_phi->GetRMS(),  h_1v_g_phi->GetRMSError(),
             res->Parameter(1), res->ParError(1),
             res->Parameter(2), res->ParError(2),
             res->Chi2(), res->Ndf(), res->Chi2()/res->Ndf(), res->Prob());
      g_phi->FixParameter(1, res->Parameter(1));
      g_phi->FixParameter(2, res->Parameter(2));

      b_g_phi_mean           = h_1v_g_phi->GetMean();
      b_g_phi_mean_err       = h_1v_g_phi->GetMeanError();
      b_g_phi_rms            = h_1v_g_phi->GetRMS();
      b_g_phi_rms_err        = h_1v_g_phi->GetRMSError();
      b_g_phi_fit_offset     = res->Parameter(1);
      b_g_phi_fit_offset_err = res->ParError (1);
      b_g_phi_fit_slope      = res->Parameter(2);
      b_g_phi_fit_slope_err  = res->ParError (2);
      b_g_phi_fit_chi2       = res->Chi2();
      b_g_phi_fit_ndf        = res->Ndf();

      delete g_phi_temp;
    }
    else {
      g_phi->FixParameter(1, Phi::use_abs ? M_1_PI : 0.5/M_PI);
      g_phi->FixParameter(2, 0);
    }

    if (find_g_dz) {
      h_1v_g_dz->Scale(1./h_1v_g_dz->Integral());
      const double integxwidth = h_1v_g_dz->Integral() * h_1v_g_dz->GetXaxis()->GetBinWidth(1);
      TF1* g_dz_temp = new TF1("g_dz_temp", fcn_fg_dz, g_dz->GetXmin(), g_dz->GetXmax(), 3);
      for (int i = 0; i < 3; ++i)
        g_dz_temp->SetParName(i, g_dz->GetParName(i));
      g_dz_temp->FixParameter(0, integxwidth);
      g_dz_temp->SetParameter(1, 10.);
      g_dz_temp->SetParameter(2, 0.);
      TFitResultPtr res = h_1v_g_dz->Fit(g_dz_temp, "0RQS");
      printf("  h_1v_g_dz mean %.3f +- %.3f  rms %.3f +- %.3f   g_dz fit sigma %6.3f +- %6.3f  mu %6.3f +- %6.3f   chi2/ndf = %6.3f/%i = %6.3f   prob: %g\n",
             h_1v_g_dz->GetMean(), h_1v_g_dz->GetMeanError(),
             h_1v_g_dz->GetRMS(),  h_1v_g_dz->GetRMSError(),
             res->Parameter(1), res->ParError(1),
             res->Parameter(2), res->ParError(2),
             res->Chi2(), res->Ndf(), res->Chi2()/res->Ndf(), res->Prob());
      g_dz->FixParameter(1, res->Parameter(1));
      g_dz->FixParameter(2, res->Parameter(2));

      b_g_dz_mean          = h_1v_g_dz->GetMean();
      b_g_dz_mean_err      = h_1v_g_dz->GetMeanError();
      b_g_dz_rms           = h_1v_g_dz->GetRMS();
      b_g_dz_rms_err       = h_1v_g_dz->GetRMSError();
      b_g_dz_fit_sigma     = res->Parameter(1);
      b_g_dz_fit_sigma_err = res->ParError (1);
      b_g_dz_fit_mu        = res->Parameter(2);
      b_g_dz_fit_mu_err    = res->ParError (2);
      b_g_dz_fit_chi2      = res->Chi2();
      b_g_dz_fit_ndf       = res->Ndf();

      delete g_dz_temp;
    }
    else {
      g_dz->FixParameter(1, 9.25);
      g_dz->FixParameter(2, 0);
    }

    // Fill histos with 1e5 samples of each to check things went OK.
    h_fcn_g_phi->FillRandom("g_phi", 100000);
    h_fcn_g_dz ->FillRandom("g_dz",  100000);
  }

  void PhiShiftTemplater::update_f_weighting_pars() {
    const double gdpmax = g_phi->GetMaximum();
    const double fdpmax = f_phi->GetMaximum();
    Mdp = fdpmax/gdpmax;

    const double gdzmax = g_dz->GetMaximum();
    const double fdzmax = f_dz->GetMaximum();
    Mdz = fdzmax/gdzmax;

    printf("weighting pars updated: phi: g %f f %f M %f   dz:  g %f f %f M %f\n", gdpmax, fdpmax, Mdp, gdzmax, fdzmax, Mdz);
  }

  void PhiShiftTemplater::fit_fs_in_sideband() {
    // Fit f_phi and f_dz from the 2v events in the sideband.

    printf("PhiShiftTemplater%s: fitting fs in sideband\n", name.c_str()); fflush(stdout);

    const TString opt = "0LIRQS";

    if (find_f_phi) {
      const int vt_which = find_f_phi_bkgonly ? vt_2vsbbkg : vt_2vsb;
      const double integxwidth = h_phi[vt_which]->Integral()*h_phi[vt_which]->GetXaxis()->GetBinWidth(1);
      TF1* f_phi_temp = new TF1("f_phi_temp", fcn_f_phi, Phi::use_abs ? 0 : -M_PI, M_PI, 3);
      for (int i = 0; i < 3; ++i)
        f_phi_temp->SetParName(i, f_phi->GetParName(i));
      f_phi_temp->FixParameter(0, integxwidth);
      f_phi_temp->SetParameter(1, 2.);
      f_phi_temp->SetParameter(2, 0.);
      f_phi_temp->SetParLimits(2, 0., 1);
      TFitResultPtr res = h_phi[vt_which]->Fit(f_phi_temp, opt);
      double err1, err2;
      const double integ1 = h_phi[vt_which]->IntegralAndError(1,5, err1);
      const double integ2 = h_phi[vt_which]->IntegralAndError(6,8, err2);
      const double N1 = pow(integ1/err1, 2);
      const double N2 = pow(integ2/err2, 2);
      const jmt::interval asym = jmt::clopper_pearson_poisson_means_ratio(N1, N2);
      printf("  h_phi[%s] mean %.3f +- %.3f  rms %.3f +- %.3f  asym %.3f +- %.3f   f_phi fit exp = %6.3f +- %6.3f  offset = %6.3f +- %6.3f  chi2/ndf = %6.3f/%i = %6.3f   prob: %g\n",
             vt_names[vt_which],
             h_phi[vt_which]->GetMean(), h_phi[vt_which]->GetMeanError(),
             h_phi[vt_which]->GetRMS(),  h_phi[vt_which]->GetRMSError(),
             asym.value, asym.error(),
             res->Parameter(1), res->ParError(1),
             res->Parameter(2), res->ParError(2),
             res->Chi2(), res->Ndf(), res->Chi2()/res->Ndf(), res->Prob());
      f_phi->FixParameter(1, res->Parameter(1));
      f_phi->FixParameter(2, res->Parameter(2));

      b_f_phi_mean        = h_phi[vt_which]->GetMean();
      b_f_phi_mean_err    = h_phi[vt_which]->GetMeanError();
      b_f_phi_rms         = h_phi[vt_which]->GetRMS();
      b_f_phi_rms_err     = h_phi[vt_which]->GetRMSError();
      b_f_phi_asym        = asym.value;
      b_f_phi_asym_err    = asym.error();
      b_f_phi_fit_exp     = res->Parameter(1);
      b_f_phi_fit_exp_err = res->ParError (1);
      b_f_phi_fit_offset     = res->Parameter(2);
      b_f_phi_fit_offset_err = res->ParError (2);
      b_f_phi_fit_chi2    = res->Chi2();
      b_f_phi_fit_ndf     = res->Ndf();

      delete f_phi_temp;
    }
    else
      f_phi->FixParameter(1, 2.);

    if (find_f_dz) {
      const int vt_which = find_f_dz_bkgonly ? vt_2vsbbkg : vt_2vsb;
      const double integxwidth =  h_dz[vt_which]->Integral() * h_dz[vt_which]->GetXaxis()->GetBinWidth(1);
      TF1* f_dz_temp = new TF1("f_dz_temp", fcn_fg_dz, f_dz->GetXmin(), f_dz->GetXmax(), 3);
      for (int i = 0; i < 3; ++i)
        f_dz_temp->SetParName(i, f_dz->GetParName(i));
      f_dz_temp->FixParameter(0, integxwidth);
      f_dz_temp->SetParameter(1, 0.2);
      f_dz_temp->SetParameter(2, 0.);
      TFitResultPtr res = h_dz[vt_which]->Fit(f_dz_temp, opt);
      printf("  h_2v_dz[%s] mean %.3f +- %.3f  rms %.3f +- %.3f  f_dz fit gaus sigma = %6.3f +- %6.3f  mu = %6.3f +- %6.3f  chi2/ndf = %6.3f/%i = %6.3f   prob: %g\n",
             vt_names[vt_which],
             h_dz[vt_which]->GetMean(), h_dz[vt_which]->GetMeanError(),
             h_dz[vt_which]->GetRMS(),  h_dz[vt_which]->GetRMSError(),
             res->Parameter(1), res->ParError(1),
             res->Parameter(2), res->ParError(2),
             res->Chi2(), res->Ndf(), res->Chi2()/res->Ndf(), res->Prob());
      f_dz->FixParameter(1, res->Parameter(1));
      f_dz->FixParameter(2, res->Parameter(2));

      b_f_dz_mean          = h_dz[vt_which]->GetMean();
      b_f_dz_mean_err      = h_dz[vt_which]->GetMeanError();
      b_f_dz_rms           = h_dz[vt_which]->GetRMS();
      b_f_dz_rms_err       = h_dz[vt_which]->GetRMSError();
      b_f_dz_fit_sigma     = res->Parameter(1);
      b_f_dz_fit_sigma_err = res->ParError (1);
      b_f_dz_fit_mu        = res->Parameter(2);
      b_f_dz_fit_mu_err    = res->ParError (2);
      b_f_dz_fit_chi2      = res->Chi2();
      b_f_dz_fit_ndf       = res->Ndf();

      delete f_dz_temp;
    }
    else {
      f_dz->FixParameter(1, 0.02);
      f_dz->FixParameter(2, 0.);
    }

    update_f_weighting_pars();

    h_fcn_f_phi->FillRandom("f_phi", 100000);
    h_fcn_f_dz ->FillRandom("f_dz",  100000);
  }

  void PhiShiftTemplater::set_phi_exp(double phi_exp) {
    f_phi->FixParameter(1, phi_exp);
    f_phi->FixParameter(2, 0.);
    update_f_weighting_pars();
  }

  double PhiShiftTemplater::prob_1v_pair(const VertexSimple& v0, const VertexSimple& v1) const {
    const double phi = v0.phi(v1);
    const double dp = Phi::use_abs ? fabs(phi) : phi;
    const double dz = v0.z - v1.z;

    return
      accept_prob(f_phi->Eval(dp), g_phi->Eval(dp), Mdp) *
      accept_prob(f_dz ->Eval(dz), g_dz ->Eval(dz), Mdz);
  }

  void PhiShiftTemplater::loop_over_1v_pairs(std::function<void(const VertexPair&)> fcn) {
    dataset_ok();

    const int N1v_t = int(dataset.one_vertices->size());
    const int N1v = sample_count > 0 && sample_count < N1v_t ? sample_count : N1v_t;

    jmt::ProgressBar pb(50, N1v*(N1v-1)/2);
    pb.start();

    for (int iv = 0; iv < N1v; ++iv) {
      const VertexSimple& v0 = dataset.one_vertices->at(iv);
      for (int jv = iv+1; jv < N1v; ++jv, ++pb) {
        const VertexSimple& v1 = dataset.one_vertices->at(jv);
        VertexPair p(v0, v1);
        p.weight = prob_1v_pair(v0, v1);
        fcn(p);
      }
    }
    printf("\n");
  }

  void PhiShiftTemplater::fill_1v_histos() {
    auto f = [this](const VertexPair& p) {
      const bool swap = p.first.ntracks < p.second.ntracks;
      const VertexSimple& first  = swap ? p.second : p.first;
      const VertexSimple& second = swap ? p.first  : p.second;
      for (int ih = vt_1v; ih <= vt_1vsb; ++ih)
        fill_2v(ih, p.weight, first, second);
    };

    printf("PhiShiftTemplater%s: fill 1v histos:\n", name.c_str()); fflush(stdout);
    loop_over_1v_pairs(f);
  }

  void PhiShiftTemplater::make_templates() {
    printf("PhiShiftTemplater%s making templates: phi = range(%f, %f, %f)\n", name.c_str(), phi_exp_min, (n_phi_exp+1)*d_phi_exp, d_phi_exp); fflush(stdout);

    clear_templates();

    TDirectory* dtemp = dtoy->mkdir("templates");
    dtemp->cd();
    
    Templates orig_templates;

    for (int ip = 0; ip < n_phi_exp; ++ip) {
      const double phi_exp = phi_exp_min + ip * d_phi_exp;
      set_phi_exp(phi_exp);

      h_fcn_f_phis[ip]->FillRandom("f_phi", 100000);

      TH1D* h = new TH1D(TString::Format("h_template_ip%i", ip), TString::Format("phi_exp = %f", phi_exp), Template::nbins, Template::min_val, Template::max_val);
      orig_templates.push_back(new PhiShiftTemplate(ip, h, phi_exp, 0.));

      auto f = [&h](const VertexPair& p) {
        h->Fill(p.first.d2d(p.second), p.weight);
      };

      printf("  pairing w/ phi_exp = %f\n", phi_exp); fflush(stdout);
      loop_over_1v_pairs(f);
    }

    printf("interpolating + shifting templates:\n");
    jmt::ProgressBar pb(50, n_phi_total * n_shift);
    pb.start();

    int iglb = 0;
    for (int ip = 0, ipe = int(orig_templates.size()); ip < ipe; ++ip) {
      TDirectory* d = dtemp->mkdir(TString::Format("ip%i", ip));
      d->cd();

      TH1D* h0 = orig_templates[ip  ]->h;
      TH1D* h1 = ip < ipe-1 ? orig_templates[ip+1]->h : 0;
      h0->Scale(1./h0->Integral());
      if (h1) h1->Scale(1./h1->Integral());

      for (int ipi = 0; ipi < n_phi_interp; ++ipi) {
        TDirectory* dd = d->mkdir(TString::Format("ipi%i", ipi));
        dd->cd();

        TH1D* h = 0;
        if (h1) {
          h = (TH1D*)h0->Clone(TString::Format("h_template_ip%i_ipi%i", ip, ipi));
          h->SetDirectory(0);
          double f1 = double(ipi)/n_phi_interp;
          h->Scale(1 - f1);
          h->Add(h1, f1);
        }
        else
          h = h0;

        for (int ish = 0; ish < n_shift; ++ish, ++pb) {
          TH1D* hh = jmt::shift_hist(h, ish);
          hh->SetDirectory(0);
          const double phi_exp = static_cast<PhiShiftTemplate*>(orig_templates[ip])->phi_exp + ipi * d_phi_exp / n_phi_interp;
          const double shift = ish * hh->GetBinWidth(1);
          hh->SetTitle(TString::Format("phi_exp = %f shift = %f\n", phi_exp, shift));

          TH1D* hhh = Template::finalize_template(hh);
          hhh->SetDirectory(dd);
          delete hh;

          templates.push_back(new PhiShiftTemplate(iglb++, hhh, phi_exp, shift));
        }

        if (h1)
          delete h;

        if (h1 == 0)
          break;
      }
    }
    printf("\n");

    for (Template* t : orig_templates)
      delete t;
  }

  void PhiShiftTemplater::process_imp() {
    printf("PhiShiftTemplater%s: run toy #%i\n", name.c_str(), dataset.toy);
    const int N1v = int(dataset.one_vertices->size());
    const int N1vpairs = N1v*(N1v-1)/2;
    printf("  # 1v input: %i (%i pairs)  2v input: %lu\n", N1v, N1vpairs, dataset.two_vertices->size());

    book_toy_fcns_and_histos();
    fill_2v_histos();
    fit_envelopes();
    fit_fs_in_sideband();

    phi_exp_bkgonly = f_phi->GetParameter(1);
    shift_means = h_d2d[vt_2vsbbkg]->GetMean() - h_d2d[vt_1vsb]->GetMean();

    t_fit_info->Fill();

    fill_1v_histos();
    make_templates();
  }
}
