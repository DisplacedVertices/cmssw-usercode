#include "One2TwoPhiShift.h"
#include "TF1.h"
#include "TFile.h"
#include "TFitResult.h"
#include "TH2D.h"
#include "TRandom3.h"
#include "TTree.h"
#include "Prob.h"
#include "Random.h"

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

  const char* One2TwoPhiShift::vt_names[One2TwoPhiShift::n_vt] = { "2v", "2vbkg", "2vsig", "2vsb", "2vsbbkg", "2vsbsig", "1v", "1vsb", "1vsingle" };

  One2TwoPhiShift::One2TwoPhiShift(const std::string& name_, TFile* f, TRandom* r)
    : name (name_.size() ? " " + name_ : ""),
      uname(name_.size() ? "_" + name_ : ""),

      env("mfvo2t_phishift" + uname),
      d2d_cut(env.get_double("d2d_cut", 0.05)),
      sampling_type(env.get_int("sampling_type", 2)),
      sample_count(env.get_int("sample_count", -1)),
      phi_exp_min(env.get_double("phi_exp_min", 0.)),
      phi_exp_max(env.get_double("phi_exp_max", 6.1)),
      d_phi_exp(env.get_double("d_phi_exp", 0.25)),
      use_abs_phi(env.get_bool("use_abs_phi", true)),
      template_nbins(env.get_int("template_nbins", 20000)),
      template_min(env.get_double("template_min", 0)),
      template_max(env.get_double("template_max", 10)),
      find_g_phi(env.get_bool("find_g_phi", true)),
      find_g_dz(env.get_bool("find_g_dz", true)),
      find_f_phi(env.get_bool("find_f_phi", true)),
      find_f_dz(env.get_bool("find_f_dz", true)),
      find_f_phi_bkgonly(env.get_bool("find_f_phi_bkgonly", false)),
      find_f_dz_bkgonly(env.get_bool("find_f_dz_bkgonly", false)),

      fout(f),
      dout(f->mkdir(TString::Format("One2TwoPhiShift%s", uname.c_str()))),
      dtoy(0),
      rand(r),
      seed(r->GetSeed() - jmt::seed_base),

      one_vertices(0),
      two_vertices(0),

      gdpmax(0),
      fdpmax(0),
      Mdp(0),
      gdzmax(0),
      fdzmax(0),
      Mdz(0)
  {
    if (sampling_type != 2)
      jmt::vthrow("sampling_type must be 2");

    printf("One2TwoPhiShift%s config:\n", name.c_str());
    printf("seed: %i\n", seed);
    printf("d2d_cut: %f\n", d2d_cut);
    printf("sampling_type: %i\n", sampling_type);
    printf("sample_count: %i\n", sample_count);
    printf("phi_exp: (%f - %f) in %f increments\n", phi_exp_min, phi_exp_max, d_phi_exp);
    printf("use_abs_phi: %i\n", use_abs_phi);
    printf("template binning: (%i, %f, %f)\n", template_nbins, template_min, template_max);
    printf("find gs: phi? %i dz? %i   fs: phi? %i (bkgonly? %i) dz? %i (bkgonly? %i)\n", find_g_phi, find_g_dz, find_f_phi, find_f_phi_bkgonly, find_f_dz, find_f_dz_bkgonly);
    fflush(stdout);

    book_trees();
  }

  void One2TwoPhiShift::book_trees() {
    dout->cd();

    TTree* t_config = new TTree("t_config", "");
    t_config->Branch("seed", const_cast<int*>(&seed), "seed/I");
    t_config->Branch("d2d_cut", const_cast<double*>(&d2d_cut), "d2d_cut/D");
    t_config->Branch("sampling_type", const_cast<int*>(&sampling_type), "sampling_type/I");
    t_config->Branch("sample_count", const_cast<int*>(&sample_count), "sample_count/I");
    t_config->Branch("phi_exp_min", const_cast<double*>(&phi_exp_min), "phi_exp_min/D");
    t_config->Branch("phi_exp_max", const_cast<double*>(&phi_exp_max), "phi_exp_max/D");
    t_config->Branch("d_phi_exp", const_cast<double*>(&d_phi_exp), "d_phi_exp/D");
    t_config->Branch("use_abs_phi", const_cast<bool*>(&use_abs_phi), "use_abs_phi/O");
    t_config->Branch("template_nbins", const_cast<int*>(&template_nbins), "template_nbins/I");
    t_config->Branch("template_min", const_cast<double*>(&template_min), "template_min/D");
    t_config->Branch("template_max", const_cast<double*>(&template_max), "template_max/D");
    t_config->Branch("find_g_phi", const_cast<bool*>(&find_g_phi), "find_g_phi/O");
    t_config->Branch("find_g_dz", const_cast<bool*>(&find_g_dz), "find_g_dz/O");
    t_config->Branch("find_f_phi", const_cast<bool*>(&find_f_phi), "find_f_phi/O");
    t_config->Branch("find_f_dz", const_cast<bool*>(&find_f_dz), "find_f_dz/O");
    t_config->Branch("find_f_phi_bkgonly", const_cast<bool*>(&find_f_phi_bkgonly), "find_f_phi_bkgonly/O");
    t_config->Branch("find_f_dz_bkgonly", const_cast<bool*>(&find_f_dz_bkgonly), "find_f_dz_bkgonly/O");
    t_config->Fill();


    t_fit_info = new TTree("t_fit_info", "");
    t_fit_info->Branch("seed", const_cast<int*>(&seed), "seed/I");
    t_fit_info->Branch("toy", &toy, "toy/I");
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

  void One2TwoPhiShift::book_toy_fcns_and_histos() {
    dtoy = dout->mkdir(TString::Format("seed%04i_toy%04i", seed, toy));
    dtoy->cd();

    const int phi_nbins = 8;
    const double phi_min = use_abs_phi ? 0 : -M_PI;
    const double phi_max = M_PI;

    g_phi = new TF1("g_phi", fcn_g_phi, phi_min, phi_max, 3);
    f_phi = new TF1("f_phi", fcn_f_phi, phi_min, phi_max, 3);
    g_dz  = new TF1("g_dz", fcn_fg_dz, -40, 40, 3);
    f_dz  = new TF1("f_dz", fcn_fg_dz, -40, 40, 3);
    g_phi->SetParNames("norm", "offset", "slope");
    f_phi->SetParNames("norm", "exp", "offset");
    for (TF1* fcn : {g_dz, f_dz})
      fcn->SetParNames("norm", "sigma", "mu");
    for (TF1* fcn : {g_phi, f_phi, g_dz, f_dz})
      fcn->FixParameter(0, 1.);


    h_1v_g_phi  = new TH1D("h_1v_g_phi",  "", phi_nbins, phi_min, phi_max);
    h_fcn_g_phi = new TH1D("h_fcn_g_phi", "", phi_nbins, phi_min, phi_max);
    h_1v_g_dz  = new TH1D("h_1v_g_dz",  "", 200, -40,  40);
    h_fcn_g_dz = new TH1D("h_fcn_g_dz", "",  20, -40,  40);

    h_fcn_f_phi = new TH1D("h_fcn_f_phi", "", phi_nbins, phi_min, phi_max);
    h_fcn_f_dz = new TH1D("h_fcn_f_dz", "", 20, -0.1, 0.1);

    double phi_exp = 0;
    h_fcn_f_phis.clear();
    for (int i_phi_exp = 0; ; ++i_phi_exp) {
      phi_exp = phi_exp_min + i_phi_exp * d_phi_exp;
      if (phi_exp > phi_exp_max)
        break;
      h_fcn_f_phis.push_back(new TH1D(TString::Format("h_fcn_f_phis_%i", i_phi_exp), TString::Format("phi_exp = %f", phi_exp), phi_nbins, phi_min, phi_max));
    }


    for (int i = 0; i < n_vt; ++i) {
      const char* iv = vt_names[i];
      TDirectory* div = dtoy->mkdir(iv);
      div->cd();

      h_issig  [i] = new TH1D("h_issig", "", 2, 0, 2);
      h_issig_0[i] = new TH1D("h_issig_0", "", 2, 0, 2);
      h_issig_1[i] = new TH1D("h_issig_1", "", 2, 0, 2);

      h_xy             [i] = new TH2D("h_xy"             , "", 100, -0.05, 0.05, 100, 0.05, 0.05);
      h_bsd2d          [i] = new TH1D("h_bsd2d"          , "", 100, 0, 0.1);
      h_bsd2d_v_bsdz   [i] = new TH2D("h_bsd2d_v_bsdz"   , "", 200, -20, 20, 100, 0, 0.1);
      h_bsdz           [i] = new TH1D("h_bsdz"           , "", 200, -20, 20);
      h_bsd2d_0        [i] = new TH1D("h_bsd2d_0"        , "", 100, 0, 0.1);
      h_bsd2d_v_bsdz_0 [i] = new TH2D("h_bsd2d_v_bsdz_0" , "", 200, -20, 20, 100, 0, 0.1);
      h_bsdz_0         [i] = new TH1D("h_bsdz_0"         , "", 200, -20, 20);

      if (n_vt == n_vt_pairs)
        break;

      h_bsd2d_1        [i] = new TH1D("h_bsd2d_1"        , "", 100, 0, 0.1);
      h_bsd2d_v_bsdz_1 [i] = new TH2D("h_bsd2d_v_bsdz_1" , "", 200, -20, 20, 100, 0, 0.1);
      h_bsdz_1         [i] = new TH1D("h_bsdz_1"         , "", 200, -20, 20);

      h_ntracks  [i] = new TH2D("h_ntracks"  , "", 20, 0, 20, 20, 0, 20);
      h_ntracks01[i] = new TH1D("h_ntracks01", "", 30, 0, 30);
      h_d2d      [i] = new TH1D("h_d2d"      , "", template_nbins, template_min, template_max);
      h_dz       [i] = new TH1D("h_dz"       , "", 20, -0.1, 0.1);
      h_phi      [i] = new TH1D("h_phi"      , "", phi_nbins, phi_min, phi_max);
    }
  }

  bool One2TwoPhiShift::is_sideband(const VertexSimple& v0, const VertexSimple& v1) const {
    return v0.d2d(v1) < d2d_cut;
  }

  void One2TwoPhiShift::fill_2v(const int ih, const double w, const VertexSimple& v0, const VertexSimple& v1) {
    if ((ih == vt_2vsb || ih == vt_2vsbbkg || ih == vt_2vsbsig || ih == vt_1vsb) && !is_sideband(v0, v1))
      return;

    if ((ih == vt_2vsig || ih == vt_2vsbsig) && (!v0.is_sig || !v1.is_sig))
      return;

    if ((ih == vt_2vbkg || ih == vt_2vsbbkg) && (v0.is_sig || v1.is_sig))
      return;

    h_issig[ih]->Fill(v0.is_sig, w);
    h_issig[ih]->Fill(v1.is_sig, w);
    h_issig_0[ih]->Fill(v0.is_sig, w);
    h_issig_1[ih]->Fill(v1.is_sig, w);
    h_xy[ih]->Fill(v0.x, v0.y, w);
    h_xy[ih]->Fill(v1.x, v1.y, w);
    h_bsd2d[ih]->Fill(v0.d2d(), w);
    h_bsd2d[ih]->Fill(v1.d2d(), w);
    h_bsd2d_0[ih]->Fill(v0.d2d(), w);
    h_bsd2d_1[ih]->Fill(v1.d2d(), w);
    h_bsd2d_v_bsdz[ih]->Fill(v0.z, v0.d2d(), w);
    h_bsd2d_v_bsdz[ih]->Fill(v1.z, v1.d2d(), w);
    h_bsd2d_v_bsdz_0[ih]->Fill(v0.z, v0.d2d(), w);
    h_bsd2d_v_bsdz_1[ih]->Fill(v1.z, v1.d2d(), w);
    h_bsdz[ih]->Fill(v0.z, w);
    h_bsdz[ih]->Fill(v1.z, w);
    h_bsdz_0[ih]->Fill(v0.z, w);
    h_bsdz_1[ih]->Fill(v1.z, w);

    h_ntracks[ih]->Fill(v0.ntracks, v1.ntracks, w);
    h_ntracks01[ih]->Fill(v0.ntracks + v1.ntracks, w);
    h_d2d[ih]->Fill(v0.d2d(v1), w);
    h_dz[ih]->Fill(v0.dz(v1), w);
    const double p = v0.phi(v1);
    h_phi[ih]->Fill(use_abs_phi ? fabs(p) : p, w);
  }

  void One2TwoPhiShift::fill_2v_histos() {
    if (two_vertices == 0)
      jmt::vthrow("One2TwoPhiShift::fill_2v_histos: must set vertices before using them");

    printf("One2TwoPhiShift%s: fill 2v histos\n", name.c_str()); fflush(stdout);
    for (const VertexPair& p : *two_vertices)
      for (int ih = 0; ih < n_vt_2v; ++ih)
        fill_2v(ih, 1, p.first, p.second);
  }

  void One2TwoPhiShift::fit_envelopes() {
    if (one_vertices == 0)
      jmt::vthrow("One2TwoPhiShift::fit_envelopes: must set vertices before using them");

    printf("One2TwoPhiShift%s: fitting envelopes\n", name.c_str()); fflush(stdout);

    const VertexSimples& v1v = *one_vertices;
    const int N1v = sample_count > 0 ? sample_count : int(v1v.size());

    // Fill the envelope histos to be fit with all unique 1v pairs.
    for (int i = 0; i < N1v; ++i) {
      for (int j = i+1; j < N1v; ++j) {
        const double phi = v1v[i].phi(v1v[j]);
        h_1v_g_phi->Fill(use_abs_phi ? fabs(phi) : phi);
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
      g_phi->FixParameter(1, use_abs_phi ? M_1_PI : 0.5/M_PI);
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

  void One2TwoPhiShift::update_f_weighting_pars() {
    gdpmax = g_phi->GetMaximum();
    fdpmax = f_phi->GetMaximum();
    Mdp = fdpmax/gdpmax;

    gdzmax = g_dz->GetMaximum();
    fdzmax = f_dz->GetMaximum();
    Mdz = fdzmax/gdzmax;

    printf("weighting pars updated: phi: g %f f %f M %f   dz:  g %f f %f M %f\n", gdpmax, fdpmax, Mdp, gdzmax, fdzmax, Mdz);
  }

  void One2TwoPhiShift::fit_fs_in_sideband() {
    // Fit f_phi and f_dz from the 2v events in the sideband.

    printf("One2TwoPhiShift%s: fitting fs in sideband\n", name.c_str()); fflush(stdout);

    const TString opt = "0LIRQS";

    if (find_f_phi) {
      const int vt_which = find_f_phi_bkgonly ? vt_2vsbbkg : vt_2vsb;
      const double integxwidth = h_phi[vt_which]->Integral()*h_phi[vt_which]->GetXaxis()->GetBinWidth(1);
      TF1* f_phi_temp = new TF1("f_phi_temp", fcn_f_phi, use_abs_phi ? 0 : -M_PI, M_PI, 3);
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

  void One2TwoPhiShift::set_phi_exp(double phi_exp) {
    f_phi->FixParameter(1, phi_exp);
    f_phi->FixParameter(2, 0.);
    update_f_weighting_pars();
  }

  double One2TwoPhiShift::prob_1v_pair(const VertexSimple& v0, const VertexSimple& v1) const {
    const double phi = v0.phi(v1);
    const double dp = use_abs_phi ? fabs(phi) : phi;
    const double dz = v0.z - v1.z;

    return
      accept_prob(f_phi->Eval(dp), g_phi->Eval(dp), Mdp) *
      accept_prob(f_dz ->Eval(dz), g_dz ->Eval(dz), Mdz);
  }

  void One2TwoPhiShift::loop_over_1v_pairs(std::function<void(const VertexPair&)> fcn) {
    if (one_vertices == 0)
      jmt::vthrow("One2TwoPhiShift::loop_over_1v_pairs: must set vertices before using them");

    const int N1v_t = int(one_vertices->size());
    const int N1v = sample_count > 0 && sample_count < N1v_t ? sample_count : N1v_t;

    int count = 0;
    const int ndots = 100;
    const int count_per_dot = N1v*(N1v-1)/2/ndots;
    printf("["); for (int i = 0; i < ndots; ++i) printf(" "); printf("]\r[");

    for (int iv = 0; iv < N1v; ++iv) {
      const VertexSimple& v0 = one_vertices->at(iv);
      for (int jv = iv+1; jv < N1v; ++jv) {
        const VertexSimple& v1 = one_vertices->at(jv);
        VertexPair p(v0, v1);
        p.weight = prob_1v_pair(v0, v1);
        fcn(p);

        if (++count % count_per_dot == 0) {
          printf("."); fflush(stdout);
        }
      }
    }
    printf("\n");
  }

  void One2TwoPhiShift::fill_1v_histos() {
    auto f = [this](const VertexPair& p) {
      const bool swap = p.first.ntracks < p.second.ntracks;
      const VertexSimple& first  = swap ? p.second : p.first;
      const VertexSimple& second = swap ? p.first  : p.second;
      for (int ih = vt_1v; ih <= vt_1vsb; ++ih)
        fill_2v(ih, p.weight, first, second);
    };

    printf("One2TwoPhiShift%s: fill 1v histos:\n", name.c_str()); fflush(stdout);
    loop_over_1v_pairs(f);
  }

  void One2TwoPhiShift::make_templates() {
    printf("One2TwoPhiShift%s making templates: phi = range(%f, %f, %f)\n", name.c_str(), phi_exp_min, phi_exp_max, d_phi_exp); fflush(stdout);

    h_templates.clear();
    dtoy->cd();

    double phi_exp = 0;
    for (int i_phi_exp = 0; ; ++i_phi_exp) {
      phi_exp = phi_exp_min + i_phi_exp * d_phi_exp;
      if (phi_exp > phi_exp_max)
        break;
      set_phi_exp(phi_exp);

      h_fcn_f_phis[i_phi_exp]->FillRandom("f_phi", 100000);

      TH1D* h_template = new TH1D(TString::Format("h_template_phi%i", i_phi_exp), TString::Format("phi_exp = %f\n", phi_exp), template_nbins, template_min, template_max);
      h_templates[i_phi_exp] = std::make_pair(phi_exp, h_template);

      auto f = [&h_template](const VertexPair& p) {
        h_template->Fill(p.first.d2d(p.second), p.weight);
      };

      printf("  pairing w/ phi_exp = %f\n", phi_exp); fflush(stdout);
      loop_over_1v_pairs(f);
    }

    
  }

  void One2TwoPhiShift::process(int toy_, const VertexSimples* toy_1v, const VertexPairs* toy_2v) {
    // how about toy negative if data?
    toy = toy_;
    one_vertices = toy_1v;
    two_vertices = toy_2v;

    printf("One2TwoPhiShift%s: run toy #%i\n", name.c_str(), toy);
    const int N1v = int(one_vertices->size());
    const int N1vpairs = N1v*(N1v-1)/2;
    printf("  # 1v input: %i (%i pairs)  2v input: %lu\n", N1v, N1vpairs, two_vertices->size());

    book_toy_fcns_and_histos();
    fill_2v_histos();
    fit_envelopes();
    fit_fs_in_sideband();
    t_fit_info->Fill();
    fill_1v_histos();
    make_templates();
  }
}
