#include "SimpleClearingTemplater.h"
#include "TFile.h"
#include "TH1.h"
#include "TMath.h"
#include "TRandom3.h"
#include "TTree.h"
#include "ProgressBar.h"

namespace mfv {
  std::vector<TemplatePar> SimpleClearingTemplater::par_info() const {
    return std::vector<TemplatePar>({
        { n_clearing_sigma, clearing_sigma_start, d_clearing_sigma },
        { 1, 0, 0.1 }
      });
  }

  SimpleClearingTemplater::SimpleClearingTemplater(const std::string& name_, TFile* f, TRandom* r)
    : Templater("SimpleClearing", name_, f, r),

      env("mfvo2t_simpleclear" + uname),
      d2d_cut(env.get_double("d2d_cut", 0.05)),
      sample_count(env.get_int("sample_count", -1)),
      clearing_sigma_start(env.get_double("clearing_sigma_start", 6)),
      d_clearing_sigma(env.get_double("d_clearing_sigma", 0.25)),
      n_clearing_sigma(env.get_int("n_clearing_sigma", 24)),

      clearing_sigma_fit(10)
  {
    printf("SimpleClearingTemplater%s config:\n", name.c_str());
    printf("d2d_cut: %f\n", d2d_cut);
    printf("sample_count: %i\n", sample_count);
    printf("clearing_sigma: %i increments of %f starting from %f\n", n_clearing_sigma, d_clearing_sigma, clearing_sigma_start);

    fflush(stdout);

    book_trees();
  }

  void SimpleClearingTemplater::book_trees() {
    dout->cd();

    TTree* t_config = new TTree("t_config", "");
    t_config->Branch("seed", const_cast<int*>(&seed), "seed/I");
    t_config->Branch("d2d_cut", const_cast<double*>(&d2d_cut), "d2d_cut/D");
    t_config->Branch("sample_count", const_cast<int*>(&sample_count), "sample_count/I");
    t_config->Fill();


    t_fit_info = new TTree("t_fit_info", "");
    t_fit_info->Branch("seed", const_cast<int*>(&seed), "seed/I");
    t_fit_info->Branch("toy", &dataset.toy, "toy/I");
  }    

  void SimpleClearingTemplater::book_toy_fcns_and_histos() {
    Templater::book_hists();
  }

  bool SimpleClearingTemplater::is_sideband(const VertexSimple& v0, const VertexSimple& v1) const {
    return v0.d2d(v1) < d2d_cut;
  }

  void SimpleClearingTemplater::make_templates() {
    dataset_ok();

    printf("SimpleClearingTemplater%s making templates\n", name.c_str()); fflush(stdout);

    clear_templates();

    TDirectory* dtemp = dtoy->mkdir("templates");
    dtemp->cd();

    const int N1v_t = int(dataset.one_vertices->size());
    const int N1v = sample_count > 0 && sample_count < N1v_t ? sample_count : N1v_t;

    jmt::ProgressBar pb(50, N1v);
    pb.start();

    int iglb = 0;
    for (int isig = 0; isig < n_clearing_sigma; ++isig) {
      const double clearing_sigma = clearing_sigma_start + isig * d_clearing_sigma;

      TH1D* h = Template::hist_with_binning(TString::Format("h_template_isig%03i", isig), TString::Format("clearing pars: #sigma = %f", clearing_sigma));

      templates.push_back(new SimpleClearingTemplate(iglb++, h, clearing_sigma));
    }

    for (int iv = 0; iv < N1v; ++iv, ++pb) {
      const VertexSimple& v0 = dataset.one_vertices->at(iv);
      for (int jv = iv+1; jv < N1v; ++jv) {
        const VertexSimple& v1 = dataset.one_vertices->at(jv);
        const VertexPair p(v0, v1);
        const double d = p.d2d();
        const double n = d / p.sig();

        for (Template* t : templates) {
          SimpleClearingTemplate* sct = dynamic_cast<SimpleClearingTemplate*>(t);
          if (n > sct->clearing_sigma)
            t->h->Fill(d);
        }
      }
    }

    for (Template* t : templates)
      Template::finalize_template_in_place(t->h);

    printf("\n");
  }

  void SimpleClearingTemplater::process_imp() {
    printf("SimpleClearingTemplater%s: run toy #%i\n", name.c_str(), dataset.toy);
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
