#include <memory>
template <typename T> using uptr = std::unique_ptr<T>;
#include "TCanvas.h"
#include "TError.h"
#include "TF1.h"
#include "TFile.h"
#include "TGraph.h"
#include "TH1.h"
#include "TMath.h"
#include "TRandom3.h"
#include "TStyle.h"
#include "TVector2.h"
//#include "OptionParser.h"
#include "ROOTTools.h"
#include "Utility.h"

int inst;
int seed;
double n1v;
double n2v;
int ntrue;
double phi_a;
double phi_b;
double clear_mu;
double clear_sig;

const int nbins_1v = 31;
const double bins_1v[nbins_1v+1] = { 
  0.000, 0.002, 0.004, 0.006, 0.008, 0.010, 0.012, 0.014, 0.016, 0.018, 0.020, 0.022, 0.024, 0.026, 0.028, 0.030, 0.032, 0.034, 0.036, 0.038,
  0.04, 0.0425, 0.045, 0.05, 0.055, 0.06, 0.07, 0.085, 0.1, 0.2, 0.4, 2.5
};

const int nbins_2v = 6;
const double bins_2v[nbins_2v+1] = { 0., 0.02, 0.04, 0.06, 0.08, 0.1, 0.2 };

//#define USE_H_DBV
TH1D* h_func_rho = 0;
TF1* f_func_rho = 0;
TF1* f_func_dphi = 0;

struct Vertex {
  int ntracks;
  double x, y, z;
  double cxx, cxy, cyy;

  Vertex() : ntracks(-1), x(0), y(0), z(0), cxx(0), cxy(0), cyy(0) {}
  Vertex(double x_, double y_, double z_) : ntracks(-1), x(x_), y(y_), z(z_), cxx(0), cxy(0), cyy(0) {}
  Vertex(double rho_, double phi_)
    : ntracks(-1),
      x(rho_ * cos(phi_)),
      y(rho_ * sin(phi_)),
      z(0),
      cxx(0),
      cxy(0),
      cyy(0)
    {}

  double rho() const { return jmt::mag(x, y); }
  double d3d() const { return jmt::mag(x, y, z); }
  double dz () const { return fabs(z); }
  double phi() const { return atan2(y, x); }

  double rho(const Vertex& o) const { return jmt::mag(x - o.x, y - o.y);          }
  double d3d(const Vertex& o) const { return jmt::mag(x - o.x, y - o.y, z - o.z); }
  double dz (const Vertex& o) const { return z - o.z; }
  double phi(const Vertex& o) const { return TVector2::Phi_mpi_pi(phi() - o.phi()); }

  double dxd(const Vertex& o) const { return (x - o.x) / rho(o); }
  double dyd(const Vertex& o) const { return (y - o.y) / rho(o); }
  double sig(const Vertex& o) const { return sqrt((cxx + o.cxx)*dxd(o)*dxd(o) + (cyy + o.cyy)*dyd(o)*dyd(o) + 2*(cxy + o.cxy)*dxd(o)*dyd(o)); }
 };

struct VertexPair {
  Vertex first;
  Vertex second;
  double weight;

  VertexPair() {}
  VertexPair(const Vertex& f, const Vertex& s, const double weight_=1.) : first(f), second(s), weight(weight_) {}
    
  double rho() const { return first.rho(second); }
  double d3d() const { return first.d3d(second); }
  double dz () const { return first.dz (second); }
  double phi() const { return first.phi(second); }

  double sig() const { return first.sig(second); }
};

double func_rho(double* x, double* p) {
  const long double rho(fabs(x[0]));
  long double f;
  if (rho < 0.012)
    f = 1.29326e5L * expl(400 * rho);
  else if (rho >= 0.012 && rho < 0.016)
    f = 1.83632e7L;
  else
    f = 1.64602e8L * expl(-214.258L * rho) + 3e10L * expl(-63.2355L * powl(rho, 0.5L)) + 3e8L * expl(-20.6511L * powl(rho, 0.15L));
  return double(f);
}

double func_dphi(double* x, double* p) {
  return phi_a * pow(fabs(x[0]), phi_b);
}

double get_rho() {
#ifdef USE_H_DBV
  return h_func_rho->GetRandom();
#else
  return f_func_rho->GetRandom();
#endif
}
  
Vertex throw_1v(const double phi=-1e99) {
  if (phi < -1e98)
    return Vertex(get_rho(), gRandom->Rndm()*2*M_PI - M_PI);
  else
    return Vertex(get_rho(), phi);
}

VertexPair throw_2v() {
  VertexPair p;
  while (1) {
    p.first = throw_1v();
    double dphi = f_func_dphi->GetRandom();
    if (gRandom->Rndm() > 0.5) dphi *= -1;
    p.second = throw_1v(TVector2::Phi_mpi_pi(p.first.phi() + dphi));
    const double pb = 0.5 * TMath::Erf((p.rho() - clear_mu)/clear_sig) + 0.5;
    const double u = gRandom->Rndm();
    if (u < pb)
      break;
  }
  return p;
}

TH1D* book_1v(const char* name) {
  return new TH1D(name, "", nbins_1v, bins_1v);
}

TH1D* book_2v(const char* name) {
  return new TH1D(name, "", nbins_2v, bins_2v);
}

int main(int argc, char** argv) {
  inst = 0;
  seed = 12919135 + inst;
  n1v = 181076;
  n2v = 251;
  ntrue = 10000000;
  
  phi_a = 1;
  phi_b = 4;

  clear_mu  = 0.0295;
  clear_sig = 0.0110;

  /////////////////////////////////////////////

  jmt::set_root_style();
  TH1::SetDefaultSumw2();

  gRandom->SetSeed(seed);

#ifdef USE_H_DBV
  uptr<TFile> fh(new TFile("h.root"));
  h_func_rho = (TH1D*)fh->Get("c1")->FindObject("h")->Clone();
  h_func_rho->SetDirectory(0);
  fh->Close();
  printf("entries in h: %f\n", h_func_rho->GetEntries());
#endif

  const double rho_min = 0;
  const double rho_max = 2.5;
  f_func_rho = new TF1("func_rho", func_rho, 0, rho_max);
  f_func_rho->SetNpx(25000);

  f_func_dphi = new TF1("func_dphi", func_dphi, 0, M_PI);
  f_func_dphi->SetNpx(1000);

  /////
  
  uptr<TCanvas> c(new TCanvas("c", "", 1972, 1000));
  c->Print("statmodel.pdf[");
  auto p    = [&c] () { c->cd(); c->Print("statmodel.pdf"); };
  auto lp   = [&c] () { c->SetLogy(1); c->Print("statmodel.pdf"); c->SetLogy(0); };
  auto lxp  = [&c] () { c->SetLogx(1); c->Print("statmodel.pdf"); c->SetLogx(0); };
  auto lxyp = [&c] () { c->SetLogx(1); c->SetLogy(1); c->Print("statmodel.pdf"); c->SetLogx(0); c->SetLogy(0); };

  ////

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

  uptr<TH1D> h_true_1v_rho(book_1v("h_true_1v_rho"));
  uptr<TH1D> h_true_1v_phi(new TH1D("h_true_1v_phi", "", 20, -M_PI, M_PI));

  uptr<TH1D> h_true_2v_rho(book_1v("h_true_2v_rho"));
  uptr<TH1D> h_true_2v_phi(new TH1D("h_true_2v_phi", "", 20, -M_PI, M_PI));

  uptr<TH1D> h_true_2v_dvv(book_2v("h_true_2v_dvv"));
  uptr<TH1D> h_true_2v_dphi(new TH1D("h_true_2v_dphi", "", 10, 0, M_PI));

  printf("1v true: ");
  for (int i = 0; i < ntrue; ++i) {
    if (i % (ntrue/5) == 0) {
      printf("%i ", i);
      fflush(stdout);
    }
    Vertex v = throw_1v();
    h_true_1v_rho->Fill(v.rho());
    h_true_1v_phi->Fill(v.phi());
  }
  printf("%i\n", ntrue);

  printf("2v true: ");
  for (int i = 0; i < ntrue; ++i) {
    if (i % (ntrue/5) == 0) {
      printf("%i ", i);
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
  printf("%i\n", ntrue);

  jmt::deoverflow(h_true_1v_rho.get());
  jmt::deoverflow(h_true_2v_dvv.get());

  uptr<TH1D> h_true_1v_rho_unzoom    ((TH1D*)h_true_1v_rho->Clone("h_true_1v_rho_unzoom"));
  uptr<TH1D> h_true_1v_rho_norm      ((TH1D*)h_true_1v_rho->Clone("h_true_1v_rho_norm"));
  uptr<TH1D> h_true_1v_rho_norm_width((TH1D*)h_true_1v_rho->Clone("h_true_1v_rho_norm_width"));
  h_true_1v_rho_norm      ->Scale(n1v/h_true_1v_rho->Integral());
  h_true_1v_rho_norm_width->Scale(n1v/h_true_1v_rho->Integral(), "width");

  printf("1v err/bin check:\n");
  for (auto* h : {h_true_1v_rho.get(), h_true_1v_rho_norm.get(), h_true_1v_rho_norm_width.get()})
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

  c->Print("statmodel.pdf]");

  // making these unique_ptrs causes segfault at end?
  delete h_func_rho;
  delete f_func_rho;
  delete f_func_dphi;
}
