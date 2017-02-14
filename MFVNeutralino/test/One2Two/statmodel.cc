#include <cassert>
#include <memory>
template <typename T> using uptr = std::unique_ptr<T>;
#include "TCanvas.h"
#include "TError.h"
#include "TF1.h"
#include "TFile.h"
#include "TGraph.h"
#include "TH1.h"
#include "TLatex.h"
#include "TLine.h"
#include "TMath.h"
#include "TRandom3.h"
#include "TStyle.h"
#include "TVector2.h"
#include "ConfigFromEnv.h"
#include "Prob.h"
#include "ROOTTools.h"
#include "Utility.h"

// Helper classes for vertices and pairs of vertices (simplified version of those used in the fitter)

struct Vertex {
  double r, p;
  double x, y;

  Vertex() : r(0), p(0), x(0), y(0) {}
  Vertex(double rho_, double phi_)
    : r(rho_),
      p(phi_),
      x(rho_ * cos(phi_)),
      y(rho_ * sin(phi_))
    {}

  double rho() const { return r; }
  double phi() const { return p; }

  double rho(const Vertex& o) const { return jmt::mag(x - o.x, y - o.y);          }
  double phi(const Vertex& o) const { return TVector2::Phi_mpi_pi(phi() - o.phi()); }
 };

struct VertexPair {
  Vertex first;
  Vertex second;

  VertexPair() {}
  VertexPair(const Vertex& f, const Vertex& s) : first(f), second(s) {}
    
  double rho() const { return first.rho(second); }
  double phi() const { return first.phi(second); }
};

// Globals: parameters for the throwing fcns and the fcns themselves, and the binning for 1v/2v hists

int ntracks;
long double rho_tail_norm;
long double rho_tail_slope;
double phi_c;
double phi_e;
double phi_a;

const int nbins_1v = 26;
const double bins_1v[nbins_1v+1] = { 
  0.010, 0.012, 0.014, 0.016, 0.018, 0.020, 0.022, 0.024, 0.026, 0.028, 0.030, 0.032, 0.034, 0.036, 0.038,
  0.04, 0.0425, 0.045, 0.05, 0.055, 0.06, 0.07, 0.085, 0.1, 0.2, 0.4, 2.5
};

//const int nbins_2v = 11;
//const double bins_2v[nbins_2v+1] = { 0., 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.2 };
const int nbins_2v = 3;
const double bins_2v[nbins_2v+1] = { 0., 0.04, 0.07, 0.11 };

//#define USE_H_DBV
TH1D* h_func_rho = 0;
TF1* f_func_rho = 0;
TF1* f_func_dphi = 0;
TH1F* h_eff = 0;

double func_rho(double* x, double*) {
  const long double rho(fabs(x[0]));
  long double f = 1e-6;
  const long double p[3][10] = {
    { 2.87190e-04L, 3.35391e-08L, 3.56126e+02L, 6.74967e+02L, 2.19970e+01L, 1.07814e+06L, 5.97512e+01L },
    { 6.72207e-10L, 8.71486e-03L, 2.50698e+00L, 1.30699e+03L, 2.63253e+01L, 2.84286e+04L, 3.09081e+01L },
    { 8.91883e-04L, 2.12659e-01L, 1.32012e+01L, 5.11276e+03L, 3.63974e+01L, 3.30855e+06L, 4.13659e+02L }
  };

  const size_t i = ntracks - 3;
  f = p[i][0] + p[i][1] * expl(-p[i][2] * rho) + p[i][3] * expl(-p[i][4] * powl(rho, 0.5L)) + rho_tail_norm * p[i][5] * expl(-p[i][6] * rho_tail_slope * powl(rho, 0.15L));

  return double(f);
}

double func_dphi(double* x, double*) {
  return pow(x[0] - phi_c, phi_e) + phi_a;
}

double throw_rho() {
  //return gRandom->Rndm();
#ifdef USE_H_DBV
  return h_func_rho->GetRandom();
#else
  return f_func_rho->GetRandom();
#endif
}

double throw_dphi() {
  double dphi = f_func_dphi->GetRandom();
  if (gRandom->Rndm() > 0.5) dphi *= -1;
  return dphi;
}

Vertex throw_1v(const double phi=-1e99) {
  if (phi < -1e98)
    return Vertex(throw_rho(), gRandom->Rndm()*2*M_PI - M_PI);
  else
    return Vertex(throw_rho(), phi);
}

double get_eff(double rho) {
  if (h_eff)
    return h_eff->GetBinContent(h_eff->FindBin(rho));
  return 1;
}

VertexPair throw_2v() {
  VertexPair p;
  while (1) {
    p.first = throw_1v();
    const double dphi = throw_dphi();
    p.second = throw_1v(TVector2::Phi_mpi_pi(p.first.phi() + dphi));
    const double eff = get_eff(p.rho());
    const double u = gRandom->Rndm();
    if (u < eff)
      break;
  }
  return p;
}

TH1D* book_1v(const char* name) { return new TH1D(name, "", nbins_1v, bins_1v); }
TH1D* book_2v(const char* name) { return new TH1D(name, "", nbins_2v, bins_2v); }

int main(int, char**) {
  // Defaults and command-line configurables.

  jmt::ConfigFromEnv env("sm", true);

  const double default_n1v[6] = { -1, -1, -1, 195827, 26746, 4404 };
  const double default_n2v[6] = { -1, -1, -1,   1323,    22,    1 };

  const int inst = env.get_int("inst", 0);
  const int seed = env.get_int("seed", 12919135 + inst);
  const int ntoys = env.get_int("ntoys", 100000);
  const std::string out_fn = env.get_string("out_fn", "statmodel");
  ntracks = env.get_int("ntracks", 3);
  assert(ntracks >= 3 && ntracks <= 5);
  const double n1v = env.get_double("n1v", default_n1v[ntracks]);
  const double n2v = env.get_double("n2v", default_n2v[ntracks]);
  const std::string true_fn = env.get_string("true_fn", "");
  const bool true_from_file = true_fn != "";
  const long ntrue_1v = env.get_long("ntrue_1v", 1000000000L);
  const long ntrue_2v = env.get_long("ntrue_2v", 100000000L);
  const double oversample = env.get_double("oversample", 1);
  rho_tail_norm = env.get_long_double("rho_tail_norm", 1L);
  rho_tail_slope = env.get_long_double("rho_tail_slope", 1L);
  phi_c = env.get_double("phi_c", 1.35);
  phi_e = env.get_double("phi_e", 2);
  phi_a = env.get_double("phi_a", 3.66);
  const std::string eff_fn = env.get_string("eff_fn", "eff_avg.root");
  const std::string eff_path = env.get_string("eff_path", TString::Format("average%i", ntracks).Data());

  /////////////////////////////////////////////

  // Set up ROOT and globals (mainly the fcns from which we throw)

  jmt::set_root_style();
  TH1::SetDefaultSumw2();
  TH1::AddDirectory(0);

  gRandom->SetSeed(seed);

  uptr<TFile> out_f(new TFile((out_fn + ".root").c_str(), "recreate"));

#ifdef USE_H_DBV
  uptr<TFile> fh(new TFile("h.root"));
  h_func_rho = (TH1D*)fh->Get("c1")->FindObject("h")->Clone();
  h_func_rho->SetDirectory(0);
  fh->Close();
  printf("entries in h: %f\n", h_func_rho->GetEntries());
#endif

  const double rho_min = 0.01;
  const double rho_max = 2.;
  f_func_rho = new TF1("func_rho", func_rho, rho_min, rho_max);
  f_func_rho->SetNpx(25000); // need lots of points when you want to sample a fcn with such a big y range

  f_func_dphi = new TF1("func_dphi", func_dphi, 0, M_PI);
  f_func_dphi->SetNpx(1000);

  if (eff_fn != "") {
    uptr<TFile> eff_f(new TFile(eff_fn.c_str()));
    h_eff = (TH1F*)eff_f->Get(eff_path.c_str())->Clone("h_eff");
    eff_f->Close();
  }

  uptr<TCanvas> c(new TCanvas("c", "", 1972, 1000));
  TVirtualPad* pd = 0;
  TString pdf_fn = (out_fn + ".pdf").c_str();
  c->Print(pdf_fn + "[");
  auto p = [&] () { c->cd(); c->Print(pdf_fn); };
  //auto lp   = [&] () { c->SetLogy(1); c->Print(pdf_fn); c->SetLogy(0); };
  //auto lxp  = [&] () { c->SetLogx(1); c->Print(pdf_fn); c->SetLogx(0); };
  //auto lxyp = [&] () { c->SetLogx(1); c->SetLogy(1); c->Print(pdf_fn); c->SetLogx(0); c->SetLogy(0); };

  /////////////////////////////////////////////

  // 1st page of output: show the rho fcn itself lin/log

  const double func_rho_max   = f_func_rho->GetMaximum();
  const double func_rho_max_x = f_func_rho->GetMaximumX();
  printf("max of 1v fcn %f at %f\n", func_rho_max, func_rho_max_x);
  c->Divide(2,1);
  c->cd(1)->SetLogy();
  f_func_rho->SetRange(0., 0.2);
  f_func_rho->DrawCopy();
  c->cd(2)->SetLogy();
  f_func_rho->SetRange(rho_min, rho_max);
  f_func_rho->Draw();
  p();
  c->Clear();

  // Generate the true 1v & 2v distributions from func_rho and
  // func_dphi. Takes a while, so if true_fn is set on cmd line, will
  // take these + the rng state from that file.

  uptr<TH1D> h_true_1v_rho(book_1v("h_true_1v_rho"));
  uptr<TH1D> h_true_1v_phi(new TH1D("h_true_1v_phi", "", 20, -M_PI, M_PI));

  uptr<TH1D> h_true_2v_rho(book_1v("h_true_2v_rho"));
  uptr<TH1D> h_true_2v_phi(new TH1D("h_true_2v_phi", "", 20, -M_PI, M_PI));

  uptr<TH1D> h_true_2v_dvv(book_2v("h_true_2v_dvv"));
  uptr<TH1D> h_true_2v_dphi(new TH1D("h_true_2v_dphi", "", 10, 0, M_PI));

  if (true_from_file) {
    gRandom->ReadRandom(true_fn.c_str());

    printf("reading 1 and 2v true hists from file\n");
    uptr<TFile> true_f(new TFile(true_fn.c_str()));
    if (!true_f->IsOpen()) {
      fprintf(stderr, "can't open %s\n", true_fn.c_str());
      return 1;
    }

    for (auto* h : {h_true_1v_rho.get(), h_true_1v_phi.get(), h_true_2v_rho.get(), h_true_2v_phi.get(), h_true_2v_dvv.get(), h_true_2v_dphi.get()})
      h->Add((TH1D*)true_f->Get(h->GetName()));
  }
  else {
    printf("1v true: ");
    for (long i = 0; i < ntrue_1v; ++i) {
      if (i % (ntrue_1v/10) == 0) {
        printf("%li", i/(ntrue_1v/10));
        fflush(stdout);
      }
      Vertex v = throw_1v();
      h_true_1v_rho->Fill(v.rho());
      h_true_1v_phi->Fill(v.phi());
    }
    printf(" %li\n", ntrue_1v);

    printf("2v true: ");
    for (long i = 0; i < ntrue_2v; ++i) {
      if (i % (ntrue_2v/10) == 0) {
        printf("%li", i/(ntrue_2v/10));
        fflush(stdout);
      }
      VertexPair vp = throw_2v();
      h_true_2v_rho->Fill(vp.first .rho());
      h_true_2v_rho->Fill(vp.second.rho());
      h_true_2v_phi->Fill(vp.first .phi());
      h_true_2v_phi->Fill(vp.second.phi());
      h_true_2v_dvv->Fill(vp.rho());
      h_true_2v_dphi->Fill(fabs(vp.phi()));
    }
    printf(" %li\n", ntrue_2v);

    gRandom->Write();
  }

  assert(h_true_1v_rho->GetBinContent(h_true_1v_rho->GetNbinsX()+1) < 1e-12);
  //jmt::deoverflow(h_true_1v_rho.get());
  jmt::deoverflow(h_true_2v_dvv.get());

  // 2nd-7th pages of output: the true_1v histogram + comparison to
  // fcn (for debugging),

  uptr<TH1D> h_true_1v_rho_unzoom    ((TH1D*)h_true_1v_rho->Clone("h_true_1v_rho_unzoom"));
  uptr<TH1D> h_true_1v_rho_norm      ((TH1D*)h_true_1v_rho->Clone("h_true_1v_rho_norm"));
  uptr<TH1D> h_true_1v_rho_norm_one  ((TH1D*)h_true_1v_rho->Clone("h_true_1v_rho_norm_one"));
  uptr<TH1D> h_true_1v_rho_norm_width((TH1D*)h_true_1v_rho->Clone("h_true_1v_rho_norm_width"));
  h_true_1v_rho_norm      ->Scale(n1v/h_true_1v_rho->Integral());
  h_true_1v_rho_norm_one  ->Scale( 1./h_true_1v_rho->Integral());
  h_true_1v_rho_norm_width->Scale(n1v/h_true_1v_rho->Integral(), "width");

  printf("1v err/bin check:\n");
  for (auto* h : {h_true_1v_rho.get(), h_true_1v_rho_norm.get(), h_true_1v_rho_norm_one.get(), h_true_1v_rho_norm_width.get()})
    printf("%40s: %10.4f/%10.4f = %0.3f\n", h->GetName(), h->GetBinError(nbins_1v), h->GetBinContent(nbins_1v), h->GetBinError(nbins_1v)/h->GetBinContent(nbins_1v));

  uptr<TH1D> h_true_2v_rho_unzoom    ((TH1D*)h_true_2v_rho->Clone("h_true_2v_rho_unzoom"));
  uptr<TH1D> h_true_2v_rho_norm      ((TH1D*)h_true_2v_rho->Clone("h_true_2v_rho_norm"));
  uptr<TH1D> h_true_2v_rho_norm_width((TH1D*)h_true_2v_rho->Clone("h_true_2v_rho_norm_width"));
  h_true_2v_rho_norm      ->Scale(n2v/h_true_2v_rho->Integral());
  h_true_2v_rho_norm_width->Scale(n2v/h_true_2v_rho->Integral(), "width");

  c->Divide(2,2);
  c->cd(1)->SetLogy();
  h_true_1v_rho_unzoom->SetTitle("true 1v, raw counts, unzoomed;#rho (cm);counts");
  h_true_1v_rho_unzoom->Draw("histe");
  c->cd(2)->SetLogy();
  h_true_1v_rho->GetXaxis()->SetRangeUser(0,0.4);
  h_true_1v_rho->SetTitle("true 1v, raw counts;#rho (cm);counts");
  h_true_1v_rho->Draw("histe");
  c->cd(3)->SetLogy();
  h_true_1v_rho_norm->SetTitle(TString::Format("true 1v, scaled to %.1f events;#rho (cm);events", n1v));
  h_true_1v_rho_norm->GetXaxis()->SetRangeUser(0,0.4);
  h_true_1v_rho_norm->Draw("histe");
  c->cd(4)->SetLogy();
  h_true_1v_rho_norm_width->SetTitle(TString::Format("true 1v, scaled to %.1f events, bin width;#rho (cm);events/cm", n1v));
  h_true_1v_rho_norm_width->GetXaxis()->SetRangeUser(0,0.4);
  h_true_1v_rho_norm_width->Draw("histe");
  p();
  c->Clear();

  uptr<TH1D> h_true_1v_rho_integ     (book_1v("h_true_1v_rho_integ"));
  uptr<TH1D> h_true_1v_rho_integ_diff(book_1v("h_true_1v_rho_integ_diff"));

  h_true_1v_rho_integ->SetTitle("integral of fcn;#rho (cm);fraction");
  h_true_1v_rho_integ_diff->SetTitle("abs. diff. in integral and thrown hist;#rho (cm)");
  
  for (int i = 0; i < nbins_1v; ++i)
    h_true_1v_rho_integ->SetBinContent(i+1, f_func_rho->Integral(bins_1v[i], bins_1v[i+1]));
  h_true_1v_rho_integ->Scale(1./h_true_1v_rho_integ->Integral());

  for (int ibin = 1; ibin <= nbins_1v; ++ibin) {
    const double integ = h_true_1v_rho_integ   ->GetBinContent(ibin);
    const double hist  = h_true_1v_rho_norm_one->GetBinContent(ibin);
    const double histe = h_true_1v_rho_norm_one->GetBinError  (ibin);
    h_true_1v_rho_integ_diff->SetBinContent(ibin, hist - integ);
    h_true_1v_rho_integ_diff->SetBinError  (ibin, histe);
  }

  c->Divide(2,1);
  pd = c->cd(1); pd->SetLogx(); pd->SetLogy();
  h_true_1v_rho_integ->Draw("hist");
  c->cd(2)->SetLogx();
  h_true_1v_rho_integ_diff->SetStats(0);
  h_true_1v_rho_integ_diff->Draw("e");
  p();
  c->Clear();

  c->Divide(2,2);
  c->cd(1)->SetLogy();
  h_true_2v_rho_unzoom->SetTitle("true 2v, raw counts, unzoomed;#rho (cm);counts");
  h_true_2v_rho_unzoom->Draw("histe");
  c->cd(2)->SetLogy();
  h_true_2v_rho->GetXaxis()->SetRangeUser(0,0.4);
  h_true_2v_rho->SetTitle("true 2v, raw counts;#rho (cm);counts");
  h_true_2v_rho->Draw("histe");
  c->cd(3)->SetLogy();
  h_true_2v_rho_norm->SetTitle(TString::Format("true 2v, scaled to %.1f events;#rho (cm);events", n2v));
  h_true_2v_rho_norm->GetXaxis()->SetRangeUser(0,0.4);
  h_true_2v_rho_norm->Draw("histe");
  c->cd(4)->SetLogy();
  h_true_2v_rho_norm_width->SetTitle(TString::Format("true 2v, scaled to %.1f events, bin width;#rho (cm);events/cm", n2v));
  h_true_2v_rho_norm_width->GetXaxis()->SetRangeUser(0,0.4);
  h_true_2v_rho_norm_width->Draw("histe");
  p();
  c->Clear();

  c->Divide(2,1);
  c->cd(1);
  h_true_1v_phi->SetMinimum(0);
  h_true_1v_phi->SetTitle("true 1v;#phi;counts");
  h_true_1v_phi->Draw("histe");
  c->cd(1)->Update();
  jmt::move_stat_box(h_true_1v_phi.get(), 0., -0.15);
  c->cd(2);
  h_true_2v_phi->SetMinimum(0);
  h_true_2v_phi->SetTitle("true 2v;#phi;counts");
  h_true_2v_phi->Draw("histe");
  c->cd(2)->Update();
  jmt::move_stat_box(h_true_2v_phi.get(), 0., -0.15);
  p();
  c->Clear();

  uptr<TH1D> h_true_2v_dvv_norm((TH1D*)h_true_2v_dvv->Clone("h_true_2v_dvv_norm"));
  h_true_2v_dvv_norm->Scale(n2v/h_true_2v_dvv->Integral());
  uptr<TH1D> h_true_2v_dphi_norm((TH1D*)h_true_2v_dphi->Clone("h_true_2v_dphi_norm"));
  h_true_2v_dphi_norm->Scale(n2v/h_true_2v_dphi->Integral());
  
  printf("2v err/bin check:\n");
  for (auto* h : {h_true_2v_dvv.get(), h_true_2v_dvv_norm.get()})
    printf("%40s: %10.4f/%10.4f = %0.3f\n", h->GetName(), h->GetBinError(nbins_2v), h->GetBinContent(nbins_2v), h->GetBinError(nbins_2v)/h->GetBinContent(nbins_2v));

  c->Divide(2,1);
  c->cd(1)->SetLogy();
  h_true_2v_dvv->SetTitle("true, raw counts;d_{VV} (cm);counts");
  h_true_2v_dvv->Draw("histe");
  c->cd(2)->SetLogy();
  h_true_2v_dvv_norm->SetTitle(TString::Format("true, scaled to %.1f events;d_{VV} (cm);events", n2v));
  h_true_2v_dvv_norm->Draw("histe");
  p();
  c->Clear();

  c->Divide(2,1);
  c->cd(1);
  h_true_2v_dphi->SetMinimum(0);
  h_true_2v_dphi->SetTitle("true, raw counts;#Delta #phi_{VV};counts");
  h_true_2v_dphi->Draw("histe");
  c->cd(1)->Update();
  jmt::move_stat_box(h_true_2v_dphi.get(), -0.5, 0);
  c->cd(2);
  h_true_2v_dphi_norm->SetMinimum(0);
  h_true_2v_dphi_norm->SetTitle(TString::Format("true, scaled to %.1f events;#Delta #phi_{VV};events", n2v));
  h_true_2v_dphi_norm->Draw("histe");
  c->cd(2)->Update();
  jmt::move_stat_box(h_true_2v_dphi_norm.get(), -0.5, 0);
  p();
  c->Clear();

  /////////////////////////////////////////////

  // Output pg 8-XX: distribution in toys of total n1v, n1v in each
  // dbv bin, and n2v in each dvv bin, each compared to truth from
  // fcn.

  uptr<TH1D> h_n1v(new TH1D("h_n1v", "", 20, n1v - 5*sqrt(n1v), n1v + 5*sqrt(n1v)));
  std::vector<uptr<TH1D>> h_1v_rho_bins;
  std::vector<uptr<TH1D>> h_2v_dvvc_bins;

  for (int ibin = 1; ibin <= nbins_1v; ++ibin) {
    const double tru = h_true_1v_rho_norm->GetBinContent(ibin);
    const double pb = 2.87e-7;
    jmt::interval iv = jmt::garwood_poisson(tru, pb, pb);
    if (iv.lower < 1) iv.lower = 0;
    h_1v_rho_bins.emplace_back(new TH1D(TString::Format("h_1v_rho_bins_%i", ibin), TString::Format("#rho bin %i", ibin), 25, iv.lower, iv.upper));
  }

  for (int ibin = 1; ibin <= nbins_2v; ++ibin) {
    const double tru = h_true_2v_dvv_norm->GetBinContent(ibin);
    const double pb = 1.35e-3;
    jmt::interval iv = jmt::garwood_poisson(tru, pb, pb);
    if (iv.lower < 1) iv.lower = 0;
    h_2v_dvvc_bins.emplace_back(new TH1D(TString::Format("h_2v_dvvc_bins_%i", ibin), TString::Format("d_{VV}^{C} bin %i", ibin), 200, iv.lower, iv.upper));
  }

  // Throw the toys and fill the above hists.
  // First throw the one vertex sample, then construct dvvc from it.
  // The toy is saved in the h_1v/2v*bins vectors.

  printf("toys: ");
  for (int itoy = 0; itoy < ntoys; ++itoy) {
    // make the toy dataset
    uptr<TH1D> h_1v_rho(book_1v("h_1v_rho"));
    const int i1v = gRandom->Poisson(n1v);
    h_n1v->Fill(i1v);

    for (int i = 0; i < i1v; ++i) {
      Vertex v = throw_1v();
      h_1v_rho->Fill(v.rho());
    }

    for (int ibin = 1; ibin <= nbins_1v; ++ibin)
      h_1v_rho_bins[ibin-1]->Fill(h_1v_rho->GetBinContent(ibin));

    // The construction
    uptr<TH1D> h_2v_dvvc(book_2v("h_2v_dvvc"));

    for (int i = 0, ie = int(i1v * oversample); i < ie; ++i) {
      const double rho0 = h_1v_rho->GetRandom();
      const double rho1 = h_1v_rho->GetRandom();
      const double dphi = throw_dphi();
      const double dvvc = sqrt(rho0*rho0 + rho1*rho1 - 2*rho0*rho1*cos(dphi));
      const double w = get_eff(dvvc);
      h_2v_dvvc->Fill(dvvc, w);
    }

    jmt::deoverflow(h_2v_dvvc.get());
    h_2v_dvvc->Scale(n2v/h_2v_dvvc->Integral());
    
    for (int ibin = 1; ibin <= nbins_2v; ++ibin)
      h_2v_dvvc_bins[ibin-1]->Fill(h_2v_dvvc->GetBinContent(ibin));

    if (ntoys > 10 && itoy % (ntoys/10) == 0) {
      printf("%i", itoy/(ntoys/10));
      fflush(stdout);
    }
  }
  printf(" %i\n", ntoys);

  h_n1v->Draw("hist");
  p();
  c->Clear();

  TLatex tl;
  tl.SetTextFont(42);

  /////////////////////////////////////////////

  // Output pg XX: display and compare the mean and rms to the true
  // distributions. The right plot on output pg-1, "2v bin-by-bin
  // rms/true" gives the fractional uncertainties in each bin due to
  // the statistics of the 1v distribution, and the last page shows
  // the closure of the construction procedure.

  uptr<TH1D> h_1v_rho_bins_means      (book_1v("h_1v_rho_bins_means"));
  uptr<TH1D> h_1v_rho_bins_rmses      (book_1v("h_1v_rho_bins_rmses"));
  uptr<TH1D> h_1v_rho_bins_rmses_norm (book_1v("h_1v_rho_bins_rmses_norm"));
  uptr<TH1D> h_1v_rho_bins_diffs      (book_1v("h_1v_rho_bins_diffs"));
  uptr<TH1D> h_1v_rho_bins_diffs_norm (book_1v("h_1v_rho_bins_diffs_norm"));

  uptr<TH1D> h_2v_dvvc_bins_means     (book_2v("h_2v_dvvc_bins_means"));
  uptr<TH1D> h_2v_dvvc_bins_rmses     (book_2v("h_2v_dvvc_bins_rmses"));
  uptr<TH1D> h_2v_dvvc_bins_rmses_norm(book_2v("h_2v_dvvc_bins_rmses_norm"));
  uptr<TH1D> h_2v_dvvc_bins_diffs     (book_2v("h_2v_dvvc_bins_diffs"));
  uptr<TH1D> h_2v_dvvc_bins_diffs_norm(book_2v("h_2v_dvvc_bins_diffs_norm"));

  printf("1v bins means:\n");
  printf("%3s %28s  %28s  %28s\n", "bin", "bin mean", "scaled true", "diff");
  for (int i_base = 0; i_base < nbins_1v; i_base += 4) {
    c->Divide(2,2);
    for (int i = i_base; i < std::min(i_base + 4, nbins_1v); ++i) {
      c->cd(i%4+1);
      h_1v_rho_bins[i]->Draw("hist");
      const double b  = h_1v_rho_bins[i]->GetMean();
      const double be = h_1v_rho_bins[i]->GetMeanError();
      const double r  = h_1v_rho_bins[i]->GetRMS();
      const double re = h_1v_rho_bins[i]->GetRMSError();
      const double t  = h_true_1v_rho_norm->GetBinContent(i+1);
      const double te = h_true_1v_rho_norm->GetBinError  (i+1);
      const double d  = b - t;
      const double de = sqrt(be*be + te*te);
      printf("%3i %12.4f +- %12.4f  %12.4f +- %12.4f  %12.4f +- %12.4f\n", i+1, b, be, t, te, d, de);
      if (d > 2*de)
        tl.SetTextColor(kRed);
      else if (d > de)
        tl.SetTextColor(kOrange+2);
      else
        tl.SetTextColor(kBlack);
      tl.DrawLatexNDC(0.6, 0.4, TString::Format("#splitline{true: %.3f #pm %.3f}{diff: %.3f #pm %.3f}", t, te, d, de));

      h_1v_rho_bins_means->SetBinContent(i+1, b);
      h_1v_rho_bins_means->SetBinError  (i+1, be);

      h_1v_rho_bins_rmses->SetBinContent(i+1, r);
      h_1v_rho_bins_rmses->SetBinError  (i+1, re);

      h_1v_rho_bins_rmses_norm->SetBinContent(i+1, r/t);
      h_1v_rho_bins_rmses_norm->SetBinError  (i+1, sqrt(re*re/r/r + te*te/t/t)); // JMTBAD

      h_1v_rho_bins_diffs->SetBinContent(i+1, d);
      h_1v_rho_bins_diffs->SetBinError  (i+1, de);

      h_1v_rho_bins_diffs_norm->SetBinContent(i+1, d/t);
      h_1v_rho_bins_diffs_norm->SetBinError  (i+1, sqrt(be*be/b/b + te*te/t/t)); // JMTBAD
    }
    p();
    c->Clear();
  }

  printf("2v bins means:\n");
  printf("%3s %28s  %28s  %28s  %28s\n", "bin", "bin mean", "scaled true", "diff", "rms");
  for (int i_base = 0; i_base < nbins_2v; i_base += 4) {
    c->Divide(2,2);
    for (int i = i_base; i < std::min(i_base + 4, nbins_2v); ++i) {
      c->cd(i%4+1);
      h_2v_dvvc_bins[i]->Draw("hist");
      const double b  = h_2v_dvvc_bins[i]->GetMean();
      const double be = h_2v_dvvc_bins[i]->GetMeanError();
      const double r  = h_2v_dvvc_bins[i]->GetRMS();
      const double re = h_2v_dvvc_bins[i]->GetRMSError();
      const double t  = h_true_2v_dvv_norm->GetBinContent(i+1);
      const double te = h_true_2v_dvv_norm->GetBinError  (i+1);
      const double d  = b - t;
      const double de = sqrt(be*be + te*te);
      printf("%3i %12.4f +- %12.4f  %12.4f +- %12.4f  %12.4f +- %12.4f  %12.4f +- %12.4f\n", i+1, b, be, t, te, b-t, sqrt(be*be + te*te), r, re);
      if (d > 2*de)
        tl.SetTextColor(kRed);
      else if (d > de)
        tl.SetTextColor(kOrange+2);
      else
        tl.SetTextColor(kBlack);
      tl.DrawLatexNDC(0.6, 0.4, TString::Format("#splitline{true: %.3f #pm %.3f}{diff: %.3f #pm %.3f}", t, te, d, de));

      h_2v_dvvc_bins_means->SetBinContent(i+1, b);
      h_2v_dvvc_bins_means->SetBinError  (i+1, be);

      h_2v_dvvc_bins_rmses->SetBinContent(i+1, r);
      h_2v_dvvc_bins_rmses->SetBinError  (i+1, re);

      h_2v_dvvc_bins_rmses_norm->SetBinContent(i+1, r/t);
      h_2v_dvvc_bins_rmses_norm->SetBinError  (i+1, sqrt(re*re/r/r + te*te/t/t)); // JMTBAD

      h_2v_dvvc_bins_diffs->SetBinContent(i+1, d);
      h_2v_dvvc_bins_diffs->SetBinError  (i+1, de);

      h_2v_dvvc_bins_diffs_norm->SetBinContent(i+1, d/t);
      h_2v_dvvc_bins_diffs_norm->SetBinError  (i+1, sqrt(be*be/b/b + te*te/t/t)); // JMTBAD
    }
    p();
    c->Clear();
  }

  TLine l1;
  l1.SetLineStyle(2);

  c->Divide(2,1);
  pd = c->cd(1); pd->SetLogx(); pd->SetLogy();
  h_1v_rho_bins_means->SetStats(0);
  h_1v_rho_bins_means->SetTitle("1v bin-by-bin mean;#rho (cm)");
  h_1v_rho_bins_means->Draw("histe");
  c->cd(2)->SetLogx();
  h_1v_rho_bins_diffs->SetStats(0);
  h_1v_rho_bins_diffs->SetTitle("1v bin-by-bin mean/true - 1;#rho (cm)");
  h_1v_rho_bins_diffs->Draw("e");
  l1.DrawLine(0,0,2.5,0);
  p();
  c->Clear();

  c->Divide(2,1);
  c->cd(1)->SetLogy();
  h_2v_dvvc_bins_means->SetStats(0);
  h_2v_dvvc_bins_means->SetTitle("2v bin-by-bin mean;d_{VV}^{C} (cm)");
  h_2v_dvvc_bins_means->Draw("histe");
  c->cd(2);
  //h_2v_dvvc_bins_rmses->GetYaxis()->SetRangeUser(0,0.6);
  h_2v_dvvc_bins_rmses->SetStats(0);
  h_2v_dvvc_bins_rmses->SetTitle("2v bin-by-bin rms;d_{VV}^{C} (cm)");
  h_2v_dvvc_bins_rmses->Draw("histe");
  p();
  c->Clear();

  c->Divide(2,1);
  c->cd(1);
  h_2v_dvvc_bins_rmses->SetStats(0);
  h_2v_dvvc_bins_rmses->SetTitle("2v bin-by-bin rms;d_{VV}^{C} (cm)");
  h_2v_dvvc_bins_rmses->Draw("histe");
  c->cd(2);
  h_2v_dvvc_bins_rmses_norm->SetStats(0);
  h_2v_dvvc_bins_rmses_norm->SetTitle("2v bin-by-bin rms/true;d_{VV}^{C} (cm)");
  h_2v_dvvc_bins_rmses_norm->Draw("histe");
  p();
  c->Clear();

  c->Divide(2,1);
  c->cd(1);
  h_2v_dvvc_bins_diffs->SetStats(0);
  h_2v_dvvc_bins_diffs->SetTitle("2v bin-by-bin mean - true;d_{VV} (cm)");
  h_2v_dvvc_bins_diffs->Draw("e");
  l1.DrawLine(0,0,0.2,0);
  c->cd(2);
  h_2v_dvvc_bins_diffs_norm->SetStats(0);
  h_2v_dvvc_bins_diffs_norm->SetTitle("2v bin-by-bin mean/true - 1;d_{VV} (cm)");
  h_2v_dvvc_bins_diffs_norm->Draw("e");
  l1.DrawLine(0,0,0.2,0);
  p();
  c->Clear();

  c->Print(pdf_fn + "]");

  out_f->cd();
  for (auto* h : {h_true_1v_rho.get(), h_true_1v_phi.get(), h_true_2v_rho.get(), h_true_2v_phi.get(), h_true_2v_dvv.get(), h_true_2v_dphi.get()})
    h->Write();

  // making these unique_ptrs causes segfault at end?
  delete h_func_rho;
  delete f_func_rho;
  delete f_func_dphi;
  delete h_eff;
}
