#include "Templater.h"
#include "TF1.h"
#include "TFile.h"
#include "TFitResult.h"
#include "TH2D.h"
#include "TRandom3.h"
#include "TStopwatch.h"
#include "TTree.h"
#include "Phi.h"
#include "Prob.h"
#include "ROOTTools.h"
#include "Random.h"
#include "Templates.h"

namespace mfv {
  const char* Templater::vt_names[Templater::n_vt] = { "2v", "2vbkg", "2vsig", "2vsb", "2vsbbkg", "2vsbsig", "1v", "1vsb", "1vsingle" };

  Templater::Templater(const std::string& dname_, const std::string& name_, TFile* f, TRandom* r)
    : dname(dname_),
      name (name_.size() ? " " + name_ : ""),
      uname(name_.size() ? "_" + name_ : ""),

      env("mfvo2t_templater" + uname),
      min_ntracks0(env.get_int("min_ntracks0", 0)),
      max_ntracks0(env.get_int("max_ntracks0", 1000000)),
      min_ntracks1(env.get_int("min_ntracks1", 0)),
      max_ntracks1(env.get_int("max_ntracks1", 1000000)),

      fout(f),
      dout(f->mkdir(TString::Format("%sTemplater%s", dname.c_str(), uname.c_str()))),
      dtoy(0),
      rand(r),
      seed(r->GetSeed() - jmt::seed_base),
      save_plots(true)
  {
    printf("Templater%s config:\n", name.c_str());
    printf("min_ntracks0: %i\n", min_ntracks0);
    printf("max_ntracks0: %i\n", max_ntracks0);
    printf("min_ntracks1: %i\n", min_ntracks1);
    printf("max_ntracks1: %i\n", max_ntracks1);

    fflush(stdout);
  }

  Templater::~Templater() {
    clear_templates();
    // JMTBAD
    if (!save_plots) {
      for (int i = 0; i < n_vt; ++i) {
        delete h_issig[i];
        delete h_issig_0[i];
        delete h_issig_1[i];
        delete h_xy[i];
        delete h_bsd2d[i];
        delete h_bsd2d0[i];
        delete h_bsd2d1[i];
        delete h_bsd2d_v_bsdz[i];
        delete h_bsdz[i];
        delete h_bsd2d_0[i];
        delete h_bsd2d_v_bsdz_0[i];
        delete h_bsdz_0[i];

        if (n_vt == n_vt_pairs)
          break;

        delete h_bsd2d_1[i];
        delete h_bsd2d_v_bsdz_1[i];
        delete h_bsdz_1[i];
        delete h_ntracks[i];
        delete h_ntracks01[i];
        delete h_d2d[i];
        delete h_phi[i];
        delete h_dz[i];
      }
    }
  }

  void Templater::book_hists() {
    dtoy = dout->mkdir(TString::Format("seed%04i_toy%04i", seed, dataset.toy));
    dtoy->cd();

    for (int i = 0; i < n_vt; ++i) {
      const char* iv = vt_names[i];
      TDirectory* div = dtoy->mkdir(iv);
      div->cd();

      h_issig  [i] = new TH1D("h_issig", "", 2, 0, 2);
      h_issig_0[i] = new TH1D("h_issig_0", "", 2, 0, 2);
      h_issig_1[i] = new TH1D("h_issig_1", "", 2, 0, 2);

      if (1) {
        std::vector<double> bins;
        for (int j = 0; j < 20; ++j)
          bins.push_back(j*0.002);
        for (double b : {0.04, 0.0425, 0.045, 0.05, 0.055, 0.06, 0.07, 0.085, 0.1, 0.2, 0.4, 2.5})
          bins.push_back(b);
        //printf("Templater: bsd2d bins: "); for (double b : bins) printf("%.3f ", b); printf("\n");

        h_bsd2d[i] = new TH1D("h_bsd2d", "", bins.size()-1, &bins[0]);
        h_bsd2d0[i] = new TH1D("h_bsd2d0", "", bins.size()-1, &bins[0]);
        h_bsd2d1[i] = new TH1D("h_bsd2d1", "", bins.size()-1, &bins[0]);
      }
      else {
        h_bsd2d[i] = new TH1D("h_bsd2d", "", 1250, 0, 2.5);
      //h_bsd2d[i] = new TH1D("h_bsd2d", "", 100, 0, 0.1);
        h_bsd2d0[i] = new TH1D("h_bsd2d0", "", 1250, 0, 2.5);
        h_bsd2d1[i] = new TH1D("h_bsd2d1", "", 1250, 0, 2.5);
      }

      h_xy             [i] = new TH2D("h_xy"             , "", 100, -0.05, 0.05, 100, 0.05, 0.05);
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
      h_d2d      [i] = new TH1D("h_d2d"      , "", Template::nbins, Template::min_val, Template::max_val);
      h_dz       [i] = new TH1D("h_dz"       , "", 20, -0.1, 0.1);
      h_phi      [i] = Phi::new_1d_hist("h_phi" , "");
    }

    if (!save_plots) {
      for (int i = 0; i < n_vt; ++i) {
        h_issig[i]->SetDirectory(0);
        h_issig_0[i]->SetDirectory(0);
        h_issig_1[i]->SetDirectory(0);
        h_xy[i]->SetDirectory(0);
        h_bsd2d[i]->SetDirectory(0);
        h_bsd2d0[i]->SetDirectory(0);
        h_bsd2d1[i]->SetDirectory(0);
        h_bsd2d_v_bsdz[i]->SetDirectory(0);
        h_bsdz[i]->SetDirectory(0);
        h_bsd2d_0[i]->SetDirectory(0);
        h_bsd2d_v_bsdz_0[i]->SetDirectory(0);
        h_bsdz_0[i]->SetDirectory(0);

        if (n_vt == n_vt_pairs)
          break;

        h_bsd2d_1[i]->SetDirectory(0);
        h_bsd2d_v_bsdz_1[i]->SetDirectory(0);
        h_bsdz_1[i]->SetDirectory(0);
        h_ntracks[i]->SetDirectory(0);
        h_ntracks01[i]->SetDirectory(0);
        h_d2d[i]->SetDirectory(0);
        h_phi[i]->SetDirectory(0);
        h_dz[i]->SetDirectory(0);
      }
    }

    dtoy->cd();
  }

  void Templater::fill_2v(const int ih, const double w, const VertexSimple& v0, const VertexSimple& v1) {
    if ((ih == vt_2vsb || ih == vt_2vsbbkg || ih == vt_2vsbsig || ih == vt_1vsb) && !is_sideband(v0, v1))
      return;

    if ((ih == vt_2vsig || ih == vt_2vsbsig) && (!v0.is_sig || !v1.is_sig))
      return;

    if ((ih == vt_2vbkg || ih == vt_2vsbbkg) && (v0.is_sig || v1.is_sig))
      return;

    h_issig[ih]->Fill(v0.is_sig, w);
    h_issig_0[ih]->Fill(v0.is_sig, w);
    h_xy[ih]->Fill(v0.x, v0.y, w);
    h_bsd2d[ih]->Fill(v0.d2d(), w);
    if (v0.ntracks >= min_ntracks0 && v0.ntracks <= max_ntracks0)
      h_bsd2d0[ih]->Fill(v0.d2d(), w);
    if (v0.ntracks >= min_ntracks1 && v0.ntracks <= max_ntracks1)
      h_bsd2d1[ih]->Fill(v0.d2d(), w);
    h_bsd2d_0[ih]->Fill(v0.d2d(), w);
    h_bsd2d_v_bsdz[ih]->Fill(v0.z, v0.d2d(), w);
    h_bsd2d_v_bsdz_0[ih]->Fill(v0.z, v0.d2d(), w);
    h_bsdz[ih]->Fill(v0.z, w);
    h_bsdz_0[ih]->Fill(v0.z, w);

    if (ih == vt_1vsingle)
      return;

    h_issig[ih]->Fill(v1.is_sig, w);
    h_issig_1[ih]->Fill(v1.is_sig, w);
    h_xy[ih]->Fill(v1.x, v1.y, w);
    h_bsd2d[ih]->Fill(v1.d2d(), w);
    h_bsd2d_1[ih]->Fill(v1.d2d(), w);
    h_bsd2d_v_bsdz[ih]->Fill(v1.z, v1.d2d(), w);
    h_bsd2d_v_bsdz_1[ih]->Fill(v1.z, v1.d2d(), w);
    h_bsdz[ih]->Fill(v1.z, w);
    h_bsdz_1[ih]->Fill(v1.z, w);

    h_ntracks[ih]->Fill(v0.ntracks, v1.ntracks, w);
    h_ntracks01[ih]->Fill(v0.ntracks + v1.ntracks, w);
    h_d2d[ih]->Fill(v0.d2d(v1), w);
    h_dz[ih]->Fill(v0.dz(v1), w);
    const double p = v0.phi(v1);
    h_phi[ih]->Fill(Phi::use_abs ? fabs(p) : p, w);
  }

  void Templater::dataset_ok() {
    if (!dataset.ok())
      jmt::vthrow("must set dataset pointers before using them: e1v: %p  1v: %p  e2v: %p  2v: %p", dataset.events_1v, dataset.one_vertices, dataset.events_2v, dataset.two_vertices);
  }

  void Templater::fill_2v_histos() {
    dataset_ok();

    printf("%sTemplater%s: fill 2v histos\n", dname.c_str(), name.c_str()); fflush(stdout);
    for (const VertexPair& p : *dataset.two_vertices)
      for (int ih = 0; ih < n_vt_2v; ++ih)
        fill_2v(ih, 1, p.first, p.second);
  }

  void Templater::clear_templates() {
    for (Template* t : templates)
      delete t;
    templates.clear();
  }

  void Templater::process(const Dataset& dataset_) {
    TStopwatch tsw;
    dataset = dataset_;
    process_imp();
    printf("Templater stopwatch: "); tsw.Print();
  }
}
