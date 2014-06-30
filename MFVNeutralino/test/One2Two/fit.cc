// rootg++ -Wall fit.cc -lMinuit -o fit.exe && ./fit.exe

#include <cassert>
#include <cmath>
#include <cstdlib>
#include <TColor.h>
#include <TF1.h>
#include <TH2.h>
#include <TCanvas.h>
#include <TROOT.h>
#include <TStyle.h>
#include <TRandom3.h>
#include <TPaveStats.h>
#include <TMinuit.h>
#include <TFile.h>
#include <TTree.h>

bool batch = true;
TFile* fin = 0;
TFile* fout = 0;
TCanvas* c = 0;

int n_bins = 100;
TH1D* h_data = 0;
TH1D* h_sig = 0;
TH1D* h_bkg[25] = {0};

const char* par_names[4] = { "mu_sig", "mu_bkg", "phi_exp", "shift" };
const int par_steps[4] = { 300, 300, 100, 100 };
const double par_min[4] = {  0,  0, 0.5, 0.   };
const double par_max[4] = {  3,  3, 6,   0.02 };

double glb_maxtwolnL = -1e300;
double glb_max_pars[4] = {1e99, 1e99, 1e99, 1e99};

int i_phi(double phi_exp) {
  return int(round(phi_exp*4));
}

int i_shift(double shift) {
  return int(shift/0.0005);
}

double twolnL(double mu_sig, double mu_bkg, double phi_exp, double shift) {
  int ip = i_phi(phi_exp);
  int is = i_shift(shift);
  TH1D* h_bkg_ip = h_bkg[ip];
  //printf("ip %i h_bkg %p\n", ip, h_bkg_ip);

  double lnL = 0;
  for (int i = 1; i <= n_bins; ++i) {
    const double nu_sig = mu_sig * h_sig ->GetBinContent(i);
    const int ifrom = i - is;
    const double nu_bkg = ifrom >= 0 ? mu_bkg * h_bkg_ip->GetBinContent(ifrom) : 0;
    const double nu_sum = nu_sig + nu_bkg;
    const double nu = nu_sum > 0 ? nu_sum : 1e-300;
    const double n = h_data->GetBinContent(i);
    const double dlnL = -nu + n * log(nu); // log(nu/n);
    lnL += dlnL;
    //printf("i: %i   mu_sig, mu_bkg, phi_exp, shift: (%f, %f, %f, %f)\n nu_bkg: %f  nu_sig: %f  nu: %f  n: %f    dlnL: %f   lnL: %f\n",
    //       i, mu_sig, mu_bkg, phi_exp, shift, nu_bkg, nu_sig, nu, n, dlnL, lnL);
  }
  return 2*lnL;
}

void minfcn(int&, double*, double& f, double* par, int) {
  f = -twolnL(par[0], par[1], par[2], par[3]);
}

int minimize_likelihood(double& min_value,
                        double& mu_sig, double& err_mu_sig,
                        double& mu_bkg, double& err_mu_bkg,
                        double& phi_exp, double& err_phi_exp,
                        double& shift, double& err_shift,
                        int print_level=-1) {
  TMinuit* m = new TMinuit(3);
  m->SetPrintLevel(print_level);
  m->SetFCN(minfcn);
  int ierr;
  m->mnparm(0, "mu_sig",   0.1, 0.01, 0, 0, ierr);
  m->mnparm(1, "mu_bkg",   1  , 0.01, 0, 0, ierr);
  m->mnparm(2, "phi_exp",  2  , 0.5,  0.1, 6, ierr);
  m->mnparm(3, "shift",    0.004, 0.001,  0, 0.019, ierr);

  m->Migrad();
  double fmin, fedm, errdef;
  int npari, nparx, istat;
  m->mnstat(fmin, fedm, errdef, npari, nparx, istat);

  min_value = -fmin;
  m->GetParameter(0, mu_sig,  err_mu_sig);
  m->GetParameter(1, mu_bkg,  err_mu_bkg);
  m->GetParameter(2, phi_exp, err_phi_exp);
  m->GetParameter(3, shift,   err_shift);

  if (print_level > -1)
    printf("minimize_likelihood: istat: %i   min_value: %e   mu_sig: %f +- %f  mu_bkg: %f +- %f   phi_exp: %f +- %f  shift: %f +- %f\n", istat, min_value, mu_sig, err_mu_sig, mu_bkg, err_mu_bkg, phi_exp, err_phi_exp, shift, err_shift);

  delete m;
  return istat;
}

#if 0
double significance(int& istat0, int& istat1) {
  double twolnL_sb, twolnL_b;
  double mu_qcd, err_mu_qcd, mu_ttbar, err_mu_ttbar, mu_stop, err_mu_stop;
  istat0 = minimize_likelihood(twolnL_sb, mu_qcd, err_mu_qcd, mu_ttbar, err_mu_ttbar, mu_stop, err_mu_stop, false);
  istat1 = minimize_likelihood(twolnL_b,  mu_qcd, err_mu_qcd, mu_ttbar, err_mu_ttbar, mu_stop, err_mu_stop, true);
  return sqrt(twolnL_sb - twolnL_b);
}  
#endif

void save(const TString& base_fn) {
  if (batch)
    return;

  static bool mkdired = false;
  if (!mkdired) {
    system("mkdir -p plots/o2tfit");
    mkdired = true;
  }
  c->SaveAs(TString::Format("plots/o2tfit/%s.root", base_fn.Data()));
  c->SaveAs(TString::Format("plots/o2tfit/%s.png",  base_fn.Data()));
  const int lg = c->GetLogy();
  c->SetLogy();
  c->SaveAs(TString::Format("plots/o2tfit/%s_log.png",  base_fn.Data()));
  c->SetLogy(lg);
}

void draw_likelihood(int iexp, double pars[4]) {
  double d_par[4] = {0};

  int found = 0;
  int ipar = -1, jpar = -1;
  int apar = -1, bpar = -1, cpar = -1;
  for (int i = 0; i < 4; ++i) {
    d_par[i] = (par_max[i] - par_min[i]) / par_steps[i];

    if (pars[i] >= 1e99) {
      if (ipar == -1)
        ipar = i;
      else
        jpar = i;
      ++found;
    }
    else {
      if (apar == -1)
        apar = i;
      else
        bpar = i;
    }
  }
  assert(found <= 2);

  //  printf("ipar %i jpar %i ; apar %i bpar %i cpar %i\n", ipar, jpar, apar, bpar, cpar);

  TH2F* h = new TH2F(TString::Format("h_likelihood_%04i_scan%i%i", iexp, ipar, jpar),
                     TString::Format("par[%i] (%s) = %f, par[%i] (%s) = %f%s;%s;%s",
                                     apar, par_names[apar], pars[apar],
                                     bpar, par_names[bpar], pars[bpar],
                                     cpar != -1 ? TString::Format(", par[%i] (%s) = %f", cpar, par_names[cpar], pars[cpar]).Data() : "",
                                     par_names[ipar], par_names[jpar]),
                     par_steps[ipar], par_min[ipar], par_max[ipar],
                     par_steps[jpar], par_min[jpar], par_max[jpar]);

  h->SetDirectory(fout);

  double maxtwolnL = -1e300;
  double max_pars[4] = {1e99, 1e99, 1e99, 1e99};

  for (int i = 1; i <= par_steps[ipar]; ++i) {
    pars[ipar] = par_min[ipar] + i * d_par[ipar];

    for (int j = 1; j <= par_steps[jpar]; ++j) {
      pars[jpar] = par_min[jpar] + j * d_par[jpar];

      //      printf("i: %3i pari: %f  j: %3i parj: %f\n", i, pars[ipar], j, pars[jpar]);

      const double tolnL = twolnL(pars[0], pars[1], pars[2], pars[3]);
      if (tolnL > maxtwolnL) {
        maxtwolnL = tolnL;
        for (int pp = 0; pp < 4; ++pp)
          max_pars[pp] = pars[pp];
      }
      h->SetBinContent(i, j, tolnL);
    }
  }
  printf("%s (%s) max 2lnL = %f  for  %s = %f  %s = %f\n", h->GetName(), h->GetTitle(), maxtwolnL, par_names[ipar], max_pars[0], par_names[jpar], max_pars[1]);

  if (maxtwolnL > glb_maxtwolnL) {
    printf("  ^ new global max!\n");
    glb_maxtwolnL = maxtwolnL;
    for (int pp = 0; pp < 4; ++pp)
      glb_max_pars[pp] = max_pars[pp];
  }

  if (!batch) {
    h->Draw("colz");
    h->SetStats(0);

    TText* t = new TText(max_pars[0], max_pars[1], TString::Format(". max 2lnL = %f @ (%f, %f)", maxtwolnL, max_pars[0], max_pars[1]));
    t->SetTextColor(kWhite);
    t->SetTextSize(0.025);
    t->Draw();
  }
}

int main(int argc, char** argv) {
  gROOT->SetStyle("Plain");
  gStyle->SetPalette(1);
  gStyle->SetFillColor(0);
  gStyle->SetOptDate(0);
  gStyle->SetOptStat(1222222);
  gStyle->SetOptFit(2222);
  gStyle->SetPadTickX(1);
  gStyle->SetPadTickY(1);
  gStyle->SetMarkerSize(.1);
  gStyle->SetMarkerStyle(8);
  gStyle->SetGridStyle(3);
  gROOT->ProcessLine("gErrorIgnoreLevel = 1001;");
  double palinfo[4][5] = {{0,0,0,1,1},{0,1,1,1,0},{1,1,0,0,0},{0,0.25,0.5,0.75,1}};
  TColor::CreateGradientColorTable(5, palinfo[3], palinfo[0], palinfo[1], palinfo[2], 500);
  gStyle->SetNumberContours(500);

  if (!batch)
    c = new TCanvas("c", "", 800, 800);

  TFile* fin = new TFile("one2two.root");
  if (!fin) {
    fprintf(stderr, "bad fin\n");
    return 1;
  }

  fout = new TFile("o2tfit.root", "recreate");

  fout->cd(); h_data = (TH1D*) fin->Get("mfvOne2Two/h_2v_toy_0_0")->Clone("h_data");
  n_bins = h_data->GetNbinsX();
  if (n_bins < 100)
    n_bins = 100;
  while (n_bins > 100 && h_data->GetBinContent(n_bins) < 1e-6)
    --n_bins;
  printf("using n_bins = %i\n", n_bins);

  fout->cd(); h_sig = (TH1D*)fin->Get("mfvOne2Two/h_2vsig_svdist2d_all")->Clone("h_sig");

  if (!batch) {
    h_data->Draw();
    h_data->GetXaxis()->SetRangeUser(0, 0.08);
    h_sig->SetFillColor(kRed);
    h_sig->Draw("sames");
    h_sig->SetStats(0);
    c->Update();
    TPaveStats* s = (TPaveStats*)h_data->FindObject("stats");
    s->SetX1NDC(0.70);
    s->SetY1NDC(0.75);
    s->SetX2NDC(0.95);
    s->SetY2NDC(0.99);
    save("data_sig");
  }

  double data_integ = h_data->Integral();
  data_integ = ((TH1D*)fin->Get("mfvOne2Two/h_2vbkg_svdist2d_all"))->Integral();

  for (int ip = 24; ip >= 0; --ip) {
    TH1D* h = h_bkg[ip] = (TH1D*)fin->Get(TString::Format("mfvOne2Two/h_1v_template_phi%i", ip))->Clone(TString::Format("h_bkg_%i", ip));
    h->SetDirectory(fout);
    h->Scale(data_integ/h->Integral());

    if (!batch) {
      if (ip < 24)
        h->Draw("hist same");
      else
        h->Draw("hist");
      h->SetStats(0);
      h->SetTitle("phi exponent 0.5-6;1v pair svdist2d (cm);pairs/10 #mum");
      h->SetLineColor(kRed+ip-1);
      h->GetXaxis()->SetRangeUser(0, 0.08);
    }
  }

  if (!batch) {
    save("templates");
    c->SetLogy();
    save("templates_log");
    c->SetLogy(0);
  }

  //  twolnL(1,1,2,0.006);


  int iexp = 0;
  for (int ip = 0; ip <= 24; ++ip) {
    for (int is = 0; is < 10; ++is) {
      double pars[4] = { 1e99, 1e99, ip*0.25, 0.001*is };
      draw_likelihood(iexp++, pars);
      if (!batch)
        save(TString::Format("likelihood_test_iphi%i_ishift%i", ip, is));
    }
  }

  double min_value, minuit_pars[4], minuit_par_errs[4];
  int ret = minimize_likelihood(min_value,
                                minuit_pars[0], minuit_par_errs[0],
                                minuit_pars[1], minuit_par_errs[1],
                                minuit_pars[2], minuit_par_errs[2],
                                minuit_pars[3], minuit_par_errs[3],
                                2);
  printf(" minuit ret %i\n", ret);


  fout->cd(); TTree* t_out = new TTree("t_out", "");

  for (int pp = 0; pp < 4; ++pp)
    t_out->Branch(TString::Format("manscan_%s", par_names[pp]), &glb_max_pars[pp], TString::Format("manscan_%s/D", par_names[pp]));

  for (int pp = 0; pp < 4; ++pp) {
    t_out->Branch(TString::Format("minuit_%s",     par_names[pp]), &minuit_pars[pp],     TString::Format("minuit_%s/D",     par_names[pp]));
    t_out->Branch(TString::Format("minuit_%s_err", par_names[pp]), &minuit_par_errs[pp], TString::Format("minuit_%s_err/D", par_names[pp]));
  }

  t_out->Branch("minuit_ret", &ret, "minuit_ret/I");
  t_out->Branch("minuit_val", &min_value, "minuit_val/D");

  t_out->Fill();

  fout->Write();
  fout->Close();
  fin->Close();
  delete fout;
  delete fin;
  delete c;
  return 0;
}
