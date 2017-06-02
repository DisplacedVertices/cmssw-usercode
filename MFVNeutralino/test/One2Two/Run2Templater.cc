#include "Run2Templater.h"
#include "TFile.h"
#include "TF1.h"
#include "TH1.h"
#include "TMath.h"
#include "TRandom3.h"
#include "TTree.h"
#include "ProgressBar.h"

namespace mfv {
  std::vector<TemplatePar> Run2Templater::par_info() const {
    return std::vector<TemplatePar>();
  }

  Run2Templater::Run2Templater(const std::string& name_, TFile* f, TRandom* r)
    : Templater("Run2", name_, f, r),

      env("mfvo2t_run2templater" + uname),
      d2d_cut(env.get_double("d2d_cut", 0.04)),
      dphi_c(env.get_double("dphi_c", 1.37)),
      dphi_e(env.get_double("dphi_e", 2)),
      dphi_a(env.get_double("dphi_a", 3.50)),
      eff_fn(env.get_string("eff_fn", "/uscms/home/jchu/public/eff_2016_v14.root")),
      eff_path(env.get_string("eff_path", "maxtk5")),
      noversamples(env.get_int("noversamples", 20)),
      sample_count(env.get_int("sample_count", -1)),

      f_dphi(0),
      h_eff(0)
  {
    printf("Run2Templater%s config:\n", name.c_str());
    printf("d2d_cut: %f\n", d2d_cut);
    printf("dphi pdf: (|phi| - %f)^%.f + %f\n", dphi_c, dphi_e, dphi_a);
    printf("eff histogram: %s/%s\n", eff_fn.c_str(), eff_path.c_str());
    printf("sample_count: %i\n", sample_count);

    fflush(stdout);

    book_trees();
  }

  void Run2Templater::book_trees() {
    dout->cd();

    TTree* t_config = new TTree("t_config", "");
    t_config->Branch("seed", const_cast<int*>(&seed), "seed/I");
    t_config->Branch("sample_count", const_cast<int*>(&sample_count), "sample_count/I");
    t_config->Fill();

    t_fit_info = new TTree("t_fit_info", "");
    t_fit_info->Branch("seed", const_cast<int*>(&seed), "seed/I");
    t_fit_info->Branch("toy", &dataset.toy, "toy/I");
  }    

  void Run2Templater::book_toy_fcns_and_histos() {
    Templater::book_hists();

    dout->cd();

    f_dphi = new TF1("f_dphi", "(abs(x)-[0])**[1] + [2]", 0, M_PI);
    f_dphi->SetParameters(dphi_c, dphi_e, dphi_a);

    TFile f_eff(eff_fn.c_str());
    if (f_eff.IsOpen()) {
      TH1D* h_eff_ = (TH1D*)f_eff.Get(eff_path.c_str());
      if (h_eff_) {
        h_eff = (TH1D*)h_eff_->Clone("h_eff");
        h_eff->SetDirectory(dout);
      }
    }
    if (!h_eff)
      jmt::vthrow("could not get h_eff");
  }

  bool Run2Templater::is_sideband(const VertexSimple& v0, const VertexSimple& v1) const {
    return v0.d2d(v1) < d2d_cut;
  }

  void Run2Templater::make_templates() {
    dataset_ok();

    printf("Run2Templater%s making templates\n", name.c_str()); fflush(stdout);

    clear_templates();

    TDirectory* dtemp = dtoy->mkdir("templates");
    dtemp->cd();

    const int N1v_t = int(dataset.one_vertices->size());
    const int N1v = sample_count > 0 && sample_count < N1v_t ? sample_count : N1v_t;

    jmt::ProgressBar pb(noversamples, noversamples);
    pb.start();

    TH1D* h = Template::hist_with_binning("h_template", "");
    templates.push_back(new Run2Template(0, h));

    TH1D* h_bsd2d0_use = h_bsd2d0[vt_1vsingle];
    TH1D* h_bsd2d1_use = h_bsd2d1[vt_1vsingle];

    for (int ioversample = 0; ioversample < noversamples; ++ioversample, ++pb) {
      for (int ijv = 0, ijve = N1v*(N1v-1)/2; ijv < ijve; ++ijv) {
        const double bsd2d0 = h_bsd2d0_use->GetRandom();
        const double bsd2d1 = h_bsd2d1_use->GetRandom();
        const double dphi = f_dphi->GetRandom();
        const double d2d = sqrt(bsd2d0*bsd2d0 + bsd2d1*bsd2d1 - 2*bsd2d0*bsd2d1*cos(dphi));
        const double w = h_eff->GetBinContent(h_eff->FindBin(d2d));

        for (Template* t : templates) {
          t->h->Fill(d2d, w);
          t->h_phi->Fill(dphi, w);
        }
      }
    }

    for (Template* t : templates) {
      Template::finalize_template_in_place(t->h);
      for (int ibin = 0; ibin <= t->h->GetNbinsX()+1; ++ibin)
        printf("ZZZ template ibin %i = %f\n", ibin, t->h->GetBinContent(ibin));
    }

    printf("\n");
  }

  void Run2Templater::process_imp() {
    printf("Run2Templater%s: run toy #%i\n", name.c_str(), dataset.toy);
    const int N1v = int(dataset.one_vertices->size());
    printf("  # 1v input: %i  2v input: %lu\n", N1v, dataset.two_vertices->size());

    book_toy_fcns_and_histos();
    fill_2v_histos();

    for (int iv = 0; iv < N1v; ++iv) {
      const VertexSimple& v0 = dataset.one_vertices->at(iv);
      fill_2v(vt_1vsingle, 1, v0, v0);
    }

    make_templates();

    t_fit_info->Fill();
  }
}
