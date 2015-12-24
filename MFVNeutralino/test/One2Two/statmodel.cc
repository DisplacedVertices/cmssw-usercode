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
#include "Utility.h"

int inst;
int seed;
double n1v;
double n2v;
double rho_a;
double rho_b;
double phi_a;
double phi_b;
double clear_mu;
double clear_sig;

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
  const double rho = fabs(x[0]);
  //return rho*exp(-rho_a*pow(rho, rho_b));
  double f;
  if (rho < 0.012)
    f = 1.29326e5 * exp(400 * rho);
  else if (rho >= 0.012 && rho < 0.016)
    f = 1.83632e7;
  else
    f = 1.64602e8 * exp(-214.258 * rho) + 3e10  * exp(-63.2355 * pow(rho, 0.5)) + 3e8 * exp(-20.6511 * pow(rho, 0.15));
  return f;
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
  
Vertex throw_1v() {
  return Vertex(get_rho(),
                gRandom->Rndm()*2*M_PI - M_PI);
}

VertexPair throw_2v() {
  VertexPair p;
  while (1) {
    p.first = throw_1v();
    double dphi = f_func_dphi->GetRandom();
    if (gRandom->Rndm() > 0.5) dphi *= -1;
    const double phi2 = TVector2::Phi_mpi_pi(p.first.phi() + dphi);
    p.second = Vertex(get_rho(), phi2);
    const double pb = 0.5 * TMath::Erf((p.rho() - clear_mu)/clear_sig) + 0.5;
    const double u = gRandom->Rndm();
    if (u < pb)
      break;
  }
  return p;
}

TH1D* book_1v(const char* name) {
  static const int n = 32;
  static const double bins[n] = { 
    0.000, 0.002, 0.004, 0.006, 0.008, 0.010, 0.012, 0.014, 0.016, 0.018, 0.020, 0.022, 0.024, 0.026, 0.028, 0.030, 0.032, 0.034, 0.036, 0.038,
    0.04, 0.0425, 0.045, 0.05, 0.055, 0.06, 0.07, 0.085, 0.1, 0.2, 0.4, 2.5
  };
  return new TH1D(name, "", n-1, bins);
}

TH1D* book_2v(const char* name) {
  static const int n = 7;
  static const double bins[n] = { 0., 0.02, 0.04, 0.06, 0.08, 0.1, 0.2 };
  return new TH1D(name, "", n-1, bins);
}

int main(int argc, char** argv) {
  inst = 0;
  seed = 12919135 + inst;
  n1v = 180000;
  n2v = 250;

  rho_a = 400;
  rho_b = 2;

  phi_a = 1;
  phi_b = 4;

  clear_mu  = 0.0295;
  clear_sig = 0.0110;

  /////////////////////////////////////////////

  gErrorIgnoreLevel = kWarning;
  gStyle->SetOptStat(111111);
  gRandom->SetSeed(seed);

#ifdef USE_H_DBV
  uptr<TFile> fh(new TFile("h.root"));
  h_func_rho = (TH1D*)fh->Get("c1")->FindObject("h")->Clone();
  h_func_rho->SetDirectory(0);
  fh->Close();
  printf("entries in h: %f\n", h_func_rho->GetEntries());
#endif

  f_func_rho = new TF1("func_rho", func_rho, 0, 2.5);
  f_func_rho->SetNpx(1000);

  f_func_dphi = new TF1("func_dphi", func_dphi, 0, M_PI);
  f_func_dphi->SetNpx(1000);

  /////
  
  uptr<TCanvas> c(new TCanvas("c", "", 1000, 800));
  c->Print("statmodel.pdf[");
  auto p  = [&c] () { c->Print("statmodel.pdf"); };
  auto lp = [&c] () { c->SetLogy(1); c->Print("statmodel.pdf"); c->SetLogy(0); };

  ////

  {
    double max = 0, max_x = 0;
    const int N = 10000;
    double X[N], Y[N];
    for (int i = 0; i < N; ++i) {
      X[i] = i*2.5/N;
      double x[1] = { X[i] };
      Y[i] = func_rho(x, 0);
      if (Y[i] > max) {
        max = Y[i];
        max_x = X[i];
      }
    }
    printf("max at %f\n", max_x);
    uptr<TGraph> g(new TGraph(N, X, Y));
    g->SetLineWidth(2);
    g->SetTitle("");
    g->Draw("AL");
    lp();
  }
      
  uptr<TH1D> h_1v_rho(book_1v("h_1v_rho"));
  uptr<TH1D> h_1v_phi(new TH1D("h_1v_phi", "", 50, -M_PI, M_PI));

  uptr<TH1D> h_2v_rho(book_1v("h_2v_rho"));
  uptr<TH1D> h_2v_phi(new TH1D("h_2v_phi", "", 50, -M_PI, M_PI));
  uptr<TH1D> h_2v_dvv(book_2v("h_2v_dvv"));
  uptr<TH1D> h_2v_dphi(new TH1D("h_2v_dphi", "", 50, -M_PI, M_PI));

  printf("1v:\n");
  for (int i = 0; i < 10000000; ++i) {
    if (i % 10000000 == 0)
      printf("%i\n", i);
    Vertex v = throw_1v();
    h_1v_rho->Fill(v.rho());
    h_1v_phi->Fill(v.phi());
  }

  printf("2v:\n");
  for (int i = 0; i < 10000000; ++i) {
    if (i % 10000000 == 0)
      printf("%i\n", i);
    VertexPair vp = throw_2v();
    h_2v_rho->Fill(vp.first .rho());
    h_2v_rho->Fill(vp.second.rho());
    h_2v_phi->Fill(vp.first .phi());
    h_2v_phi->Fill(vp.second.phi());
    h_2v_dvv->Fill(vp.rho());
    h_2v_dphi->Fill(vp.phi());
  }
  
  h_2v_dvv->SetBinContent(h_2v_dvv->GetNbinsX(), h_2v_dvv->GetBinContent(h_2v_dvv->GetNbinsX()) + h_2v_dvv->GetBinContent(h_2v_dvv->GetNbinsX()+1));
  h_2v_dvv->SetBinError(h_2v_dvv->GetNbinsX(), sqrt(pow(h_2v_dvv->GetBinError(h_2v_dvv->GetNbinsX()), 2) + pow(h_2v_dvv->GetBinError(h_2v_dvv->GetNbinsX()+1), 2)));
  h_2v_dvv->SetBinContent(h_2v_dvv->GetNbinsX()+1, 0);
  h_2v_dvv->SetBinError(h_2v_dvv->GetNbinsX()+1, 0);

  uptr<TH1D> h_1v_rho_norm((TH1D*)h_1v_rho->Clone("h_1v_rho_norm"));
  h_1v_rho_norm->Scale(1, "width");
  h_1v_rho->GetXaxis()->SetRangeUser(0,0.4);
  h_1v_rho->Draw();
  p(); lp();
  h_1v_rho_norm->GetXaxis()->SetRangeUser(0,0.4);
  h_1v_rho_norm->Draw();
  p(); lp();
  h_1v_phi->SetMinimum(0);
  h_1v_phi->Draw();
  p();

  uptr<TH1D> h_2v_rho_norm((TH1D*)h_2v_rho->Clone("h_2v_rho_norm"));
  h_2v_rho_norm->Scale(1, "width");
  h_2v_rho->GetXaxis()->SetRangeUser(0,0.4);
  h_2v_rho->Draw();
  p(); lp();
  h_2v_rho_norm->GetXaxis()->SetRangeUser(0,0.4);
  h_2v_rho_norm->Draw();
  p(); lp();
  h_2v_phi->SetMinimum(0);
  h_2v_phi->Draw();
  p();

  h_2v_dvv->Scale(251./h_2v_dvv->Integral());
  h_2v_dvv->Draw("hist");
  p(); lp();
  h_2v_dphi->SetMinimum(0);
  h_2v_dphi->Draw();
  p();

  c->Print("statmodel.pdf]");
}
