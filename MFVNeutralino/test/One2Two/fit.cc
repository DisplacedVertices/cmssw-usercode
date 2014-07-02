// rootg++ -g -std=c++0x -Wall fit.cc -lMinuit -o fit.exe && ./fit.exe

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

int n_bins = -1;
TH1D* h_data = 0;
TH1D* h_sig = 0;
std::vector<TH1D*> h_bkgs;

double glb_maxtwolnL = -1e300;
double glb_max_pars     [4] = {1e99, 1e99, 1e99, 1e99};
double glb_max_pars_errs[4] = {1e99, 1e99, 1e99, 1e99};

const int n_phi_templates = 24;
const int n_phi_interp = 20;
const int n_shift_per_phi = 40;
const double phi_orig_width = 0.25;
const double phi_interp_width = phi_orig_width/n_phi_interp;
const double shift_width = 0.0005;

const char* par_names[4] = { "mu_sig", "mu_bkg", "phi_exp", "shift" };
const int par_steps[4] = { 400, 400, 200,  40   };
const double par_min[4] = {  0,  0,  0.,   0.   };
const double par_max[4] = {100, 200, 6 - phi_interp_width, 0.02 - shift_width };


int i_phi(double phi_exp) {
  return int(phi_exp/phi_interp_width);
}

int i_shift(double shift) {
  return int(shift/shift_width);
}

TH1D* get_h_bkg(double phi_exp, double shift) {
  const int ip = i_phi(phi_exp);
  const int is = i_shift(shift);
  const int x = ip*n_shift_per_phi + is;
  //  printf("phi_exp %f ip %i shift %f is %i x %i nbkg %i\n", phi_exp, ip, shift, is, x, int(h_bkgs.size()));
  return h_bkgs[x];
}
  
double twolnL(double mu_sig, double mu_bkg, double phi_exp, double shift) {
  TH1D* h_bkg = get_h_bkg(phi_exp, shift);

  double lnL = 0;
  for (int i = 1; i <= n_bins; ++i) {
    const double nu_sig = mu_sig * h_sig->GetBinContent(i);
    const double nu_bkg = mu_bkg * h_bkg->GetBinContent(i);
    const double nu_sum = nu_sig + nu_bkg;
    const double nu = nu_sum > 0 ? nu_sum : 1e-300;
    const double n = h_data->GetBinContent(i);
    const double dlnL = -nu + n * log(nu); // log(nu/n);
    lnL += dlnL;
    //    printf("i: %i   mu_sig, mu_bkg, phi_exp, shift: (%f, %f, %f, %f)\n nu_bkg: %f  nu_sig: %f  nu: %f  n: %f    dlnL: %f   lnL: %f\n",
    //     i, mu_sig, mu_bkg, phi_exp, shift, nu_bkg, nu_sig, nu, n, dlnL, lnL);
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
                        bool bkg_only,
                        int print_level=-1) {
  TMinuit* m = new TMinuit(4);
  m->SetPrintLevel(print_level);
  m->SetFCN(minfcn);
  int ierr;
  m->mnparm(0, "mu_sig",   0    , 0.1,  0,   1e6,    ierr);
  m->mnparm(1, "mu_bkg",   10   , 0.1,  0,   1e6,    ierr);
  m->mnparm(2, "phi_exp",  2    , 0.05,    0.1, 6,    ierr);
  m->mnparm(3, "shift",    0.002, 0.0005,  0,   0.02, ierr);

  if (bkg_only)
    m->FixParameter(0);

  m->Migrad();
  //  m->mnmnos();
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

double significance(int& istat0, int& istat1, int print_level=-1) {
  double twolnL_sb, twolnL_b;
  double a,b,c,d,e,f,g,h;
  istat0 = minimize_likelihood(twolnL_sb, a,b,c,d,e,f,g,h, false, print_level);
  istat1 = minimize_likelihood(twolnL_b,  a,b,c,d,e,f,g,h, true,  print_level);
  return sqrt(twolnL_sb - twolnL_b);
}  

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

void draw_likelihood(int iexp, double pars[4], const char* name) {
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

    if (!batch) {
      h->Draw("colz");
      h->SetStats(0);

      TText* t = new TText(max_pars[0], max_pars[1], TString::Format(". max 2lnL = %f @ (%f, %f)", maxtwolnL, max_pars[0], max_pars[1]));
      t->SetTextColor(kWhite);
      t->SetTextSize(0.025);
      t->Draw();

      save(name);
    }
  }
}

bool scanmin_likelihood(bool bkg_only, int print_level=-1) {

  std::vector<int> istats;
  bool all_ok = true;

  glb_maxtwolnL = -1e300;

  printf("scanminning (bkg_only = %i): ", bkg_only);

  for (int ip = 0; ip < n_phi_templates; ++ip) {
    if (print_level == -1) { printf("."); fflush(stdout); }
    for (int ipi = 0; ipi < n_phi_interp; ++ipi) {
      for (int ish = 0; ish < n_shift_per_phi; ++ish) {
        const double phi_exp = ip*0.25 + ipi*phi_interp_width;
        const double shift = shift_width * ish;

        TMinuit* m = new TMinuit(4);
        m->SetPrintLevel(print_level);
        m->SetFCN(minfcn);
        int ierr;
        m->mnparm(0, "mu_sig",   0    , 0.1,  0,   1e6,    ierr);
        m->mnparm(1, "mu_bkg",   10   , 0.1,  0,   1e6,    ierr);

        m->mnparm(2, "phi_exp",  phi_exp,  0.05,   0,0, ierr); m->FixParameter(2);
        m->mnparm(3, "shift",    shift,    0.0005, 0,0, ierr); m->FixParameter(3);
        
        if (bkg_only)
          m->FixParameter(0);

        m->Migrad();
        //  m->mnmnos();
        double fmin, fedm, errdef;
        int npari, nparx, istat;
        m->mnstat(fmin, fedm, errdef, npari, nparx, istat);

        const double maxtwolnL = -fmin;
        double mu_sig, err_mu_sig, mu_bkg, err_mu_bkg;
        m->GetParameter(0, mu_sig,  err_mu_sig);
        m->GetParameter(1, mu_bkg,  err_mu_bkg);

        printf("scanmin_likelihood: phi_exp %6f shift %6f  istat: %i   maxtwolnL: %e   mu_sig: %f +- %f  mu_bkg: %f +- %f\n", phi_exp, shift, istat, maxtwolnL, mu_sig, err_mu_sig, mu_bkg, err_mu_bkg);

        if (maxtwolnL > glb_maxtwolnL) {
          printf("  ^ new global max!\n");
          glb_maxtwolnL = maxtwolnL;
          glb_max_pars[0] = mu_sig;
          glb_max_pars[1] = mu_bkg;
          glb_max_pars_errs[0] = err_mu_sig;
          glb_max_pars_errs[1] = err_mu_bkg;
          glb_max_pars[2] = phi_exp;
          glb_max_pars[3] = shift;
        }

        istats.push_back(istat);
        if (istat != 3)
          all_ok = false;

        delete m;
      }
    }
  }

  return all_ok;
}

TH1D* shift_hist(const TH1D* h, const int shift) {
  const int nbins = h->GetNbinsX();
  TH1D* hshift = (TH1D*)h->Clone(TString::Format("%s_is%i", h->GetName(), shift));
  
  for (int ibin = 1; ibin <= nbins+1; ++ibin) {
    const int ifrom = ibin - shift;
    double val = 0, err = 0;
    if (ifrom >= 1) { // don't shift in from underflow, shouldn't be any with svdist = positive quantity anyway
      val = h->GetBinContent(ifrom);
      err = h->GetBinError  (ifrom);
    }
    if (ibin == nbins+1) {
      double var = err*err;
      for (int irest = ifrom+1; irest <= nbins+1; ++irest) {
        val += h->GetBinContent(irest);
        var += pow(h->GetBinError(irest), 2);
      }
      err = sqrt(var);
    }

    hshift->SetBinContent(ibin, val);
    hshift->SetBinError  (ibin, err);
  }

  return hshift;
 }

TH1D* finalize_binning(TH1D* h) {
  std::vector<double> bins;
  for (int i = 0; i < 20; ++i)
    bins.push_back(i * 0.01);
  bins.push_back(0.2);
  bins.push_back(0.4);
  bins.push_back(0.6);
  bins.push_back(1);
  bins.push_back(2);
  bins.push_back(3);
  TH1D* hh = (TH1D*)h->Rebin(bins.size()-1, TString::Format("%s_rebinned", h->GetName()), &bins[0]);
  if (n_bins < 0)
    n_bins = hh->GetNbinsX();
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

int main(int argc, char** argv) {
  if (argc < 4) {
    fprintf(stderr, "usage: fit.exe jobnum min_ntracks signum\n");
    return 1;
  }

  const int jobnum = atoi(argv[1]);
  const int min_ntracks = atoi(argv[2]);
  const int signum = atoi(argv[3]);
  const char* signames[] = { "mfv_neutralino_tau0100um_M0400", "mfv_neutralino_tau0300um_M0400", "mfv_neutralino_tau1000um_M0400", "mfv_neutralino_tau9900um_M0400" };
  const char* signame = signames[signum >= 0 && signum < 4 ? signum : 2];


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
  TH1::SetDefaultSumw2();

  if (!batch)
    c = new TCanvas("c", "", 800, 800);

  const TString in_fn = jobnum >= 0 ? TString::Format("%i.one2two.root", jobnum) : "one2two.root";
  printf("fit.exe: input file %s\n", in_fn.Data());
  TFile* fin = new TFile(in_fn);
  if (!fin || !fin->IsOpen()) {
    fprintf(stderr, "bad fin\n");
    return 1;
  }

  TFile* fsig = new TFile("signal_templates.root");
  if (!fsig || !fsig->IsOpen()) {
    fprintf(stderr, "bad fsig\n");
    return 1;
  }

  const TString out_fn = jobnum >= 0 ? TString::Format("%i.o2tfit.root", jobnum) : "o2tfit.root";
  printf("fit.exe: output file %s\n", out_fn.Data());
  fout = new TFile(out_fn, "recreate");

  const TString data_path = TString::Format("mfvOne2Two/h_2v_toy_%i_0", jobnum >= 0 ? jobnum : 0);
  fout->cd(); h_data = finalize_binning((TH1D*) fin->Get(data_path)->Clone("h_data"));
  printf("using n_bins = %i (low edge %f)\n", n_bins, h_data->GetBinLowEdge(n_bins));

  const TString sig_path = TString::Format("h_sig_ntk%i_%s", min_ntracks, signame);
  printf("loading signal template from %s\n", sig_path.Data()); fflush(stdout);
  fout->cd(); h_sig = finalize_binning((TH1D*)fsig->Get(sig_path)->Clone("h_sig"));
  h_sig->Scale(1./h_sig->Integral());

  if (!batch) {
    h_data->Draw();
    h_data->GetXaxis()->SetRangeUser(0, 3);
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


  printf("loading background templates\n"); fflush(stdout);
  TH1D* h_templates[25] = {0};
  for (int ip = n_phi_templates; ip >= 0; --ip) {
    fout->cd();
    TH1D* h = h_templates[ip] = (TH1D*)fin->Get(TString::Format("mfvOne2Two/h_1v_template_phi%i", ip))->Clone(TString::Format("h_bkg_%i", ip));
    h->Scale(1./h->Integral());

    if (!batch) {
      if (ip < n_phi_templates)
        h->Draw("hist same");
      else
        h->Draw("hist");
      h->SetStats(0);
      h->SetTitle("phi exponent 0-6;1v pair svdist2d (cm);pairs/10 #mum");
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

  printf("morphing background templates: "); fflush(stdout);
  for (int ip = 0; ip < n_phi_templates; ++ip) {
    TDirectory* d = fout->mkdir(TString::Format("background_templates_%i", ip));

    TH1D* h0 = h_templates[ip];
    TH1D* h1 = h_templates[ip+1];
    h0->SetDirectory(d);
    h1->SetDirectory(d);

    for (int ipi = 0; ipi < n_phi_interp; ++ipi) {
      TDirectory* dd = d->mkdir(TString::Format("background_templates_%i_%i", ip, ipi));

      TH1D* h = (TH1D*)h0->Clone(TString::Format("%s_ip%i", h0->GetName(), ipi));
      h->SetDirectory(0);
      double f1 = double(ipi)/n_phi_interp;
      h->Scale(1 - f1);
      h->Add(h1, f1);

      for (int ish = 0; ish < n_shift_per_phi; ++ish) {
        TH1D* hh = shift_hist(h, ish);
        hh->SetDirectory(0);
        hh->SetTitle(TString::Format("phi_exp = %f shift = %f\n", ip * phi_orig_width + ipi * phi_interp_width, ish * shift_width));
        TH1D* hh_rebinned = finalize_binning(hh);
        hh_rebinned->SetDirectory(dd);
        delete hh;
        h_bkgs.push_back(hh_rebinned);
      }
      delete h;
      printf("."); fflush(stdout);
    }
  }
  fout->cd();
  printf(" done\n"); fflush(stdout);

  double largest_norm_diff = 0;
  for (const TH1D* h : h_bkgs) {
    double diff = fabs(h->Integral() - 1);
    if (diff > largest_norm_diff)
      largest_norm_diff = diff;
  }
  printf("largest norm diff = %f\n", largest_norm_diff);
      
  if (false && !batch) {
    printf("dumping morphed templates: "); fflush(stdout);
    c->SaveAs("plots/o2tfit/templates_rebinned_shift.pdf[");
    for (int ip = 0; ip < n_phi_templates; ++ip) {
      for (int ipi = 0; ipi < n_phi_interp; ++ipi) {
        for (int ish = 0; ish < n_shift_per_phi; ++ish) {
          TH1D* h = h_bkgs[ip*n_phi_interp*n_shift_per_phi + ipi*n_shift_per_phi + ish];
          h->SetLineColor(kBlack);
          h->SetLineWidth(2);
          h->SetStats(0);
          h->GetXaxis()->SetRangeUser(0, 0.1);
          h->GetYaxis()->SetRangeUser(0, 12);
          h->Draw("hist");
          c->SaveAs("plots/o2tfit/templates_rebinned_shift.pdf");
        }
        printf("."); fflush(stdout);
      }
    }
    c->SaveAs("plots/o2tfit/templates_rebinned_shift.pdf]");

    c->SaveAs("plots/o2tfit/templates_rebinned_phi.pdf[");
    for (int ish = 0; ish < n_shift_per_phi; ++ish) {
      for (int ip = 0; ip < n_phi_templates; ++ip) {
        for (int ipi = 0; ipi < n_phi_interp; ++ipi) {
          TH1D* h = h_bkgs[ip*n_phi_interp*n_shift_per_phi + ipi*n_shift_per_phi + ish];
          h->SetLineColor(kBlack);
          h->SetLineWidth(2);
          h->SetStats(0);
          h->GetXaxis()->SetRangeUser(0, 0.1);
          h->GetYaxis()->SetRangeUser(0, 12);
          h->Draw("hist");
          c->SaveAs("plots/o2tfit/templates_rebinned_phi.pdf");
        }
        printf("."); fflush(stdout);
      }
    }
    c->SaveAs("plots/o2tfit/templates_rebinned_phi.pdf]");
    printf(" done\n"); fflush(stdout);
  }

  //    twolnL(1,1,2,0.006);


  {
    double pars[4] = { 1e99, 1e99, 3, 0.002};
    draw_likelihood(-1, pars, "likelihood_test_phi3_shift0p002");
  }

  int sb_ok;
  int b_ok;
  double maxtwolnLsb,  maxtwolnLb;
  double sb_max_pars[4];
  double sb_max_pars_errs[4];
  double b_max_pars[4];
  double b_max_pars_errs[4];
  sb_ok = scanmin_likelihood(false);
  maxtwolnLsb = glb_maxtwolnL;
  for (int pp = 0; pp < 4; ++pp) {
    sb_max_pars[pp] = glb_max_pars[pp];
    sb_max_pars_errs[pp] = glb_max_pars_errs[pp];
  }
  printf("sig+bkg ok? %i   maxtwolnLsb: %g\n", sb_ok, maxtwolnLsb);
  {
    double pars[4] = { 1e99, 1e99, sb_max_pars[2], sb_max_pars[3] };
    draw_likelihood(100, pars, "likelihood_test_sbmax");
  }

  b_ok = scanmin_likelihood(true);
  maxtwolnLb = glb_maxtwolnL;
  for (int pp = 0; pp < 4; ++pp) {
    b_max_pars[pp] = glb_max_pars[pp];
    b_max_pars_errs[pp] = glb_max_pars_errs[pp];
  }
  printf("b only  ok? %i   maxtwolnLb : %g\n", b_ok, maxtwolnLb);
  {
    double pars[4] = { 1e99, 1e99, b_max_pars[2], b_max_pars[3] };
    draw_likelihood(200, pars, "likelihood_test_b");
  }

  double sig = sqrt(maxtwolnLsb - maxtwolnLb);
  printf("\nsig: %f\n", sig);

  fout->cd(); TTree* t_out = new TTree("t_out", "");

  for (int pp = 0; pp < 4; ++pp) {
    t_out->Branch(TString::Format("scanmin_sb_%s",     par_names[pp]), &sb_max_pars[pp],      TString::Format("scanmin_sb_%s/D",     par_names[pp]));
    t_out->Branch(TString::Format("scanmin_sb_err_%s", par_names[pp]), &sb_max_pars_errs[pp], TString::Format("scanmin_sb_err_%s/D", par_names[pp]));
  }
  t_out->Branch("maxtwolnLsb", &maxtwolnLsb, "maxtwolnLsb/D");
  for (int pp = 0; pp < 4; ++pp) {
    t_out->Branch(TString::Format("scanmin_b_%s",     par_names[pp]), &b_max_pars[pp],      TString::Format("scanmin_b_%s/D",     par_names[pp]));
    t_out->Branch(TString::Format("scanmin_b_err_%s", par_names[pp]), &b_max_pars_errs[pp], TString::Format("scanmin_b_err_%s/D", par_names[pp]));
  }
  t_out->Branch("maxtwolnLb", &maxtwolnLb, "maxtwolnLb/D");
  t_out->Branch("sig", &sig, "sig/D");

  t_out->Fill();

#if 0
  int iexp = 0;
  for (int ip = 0; ip < n_phi_templates; ++ip) {
    for (int ipi = 0; ipi < n_phi_interp; ++ipi) {
      for (int ish = 0; ish < n_shift_per_phi; ++ish) {
        double pars[4] = { 1e99, 1e99, ip*0.25 + ipi*phi_interp_width, shift_width * ish };
        draw_likelihood(iexp++, pars, TString::Format("likelihood_test_iphi%i_ishift%i", ip, ish));
      }
    }
  }
#endif

#if 0
  double min_value, minuit_pars[4], minuit_par_errs[4];
  int ret = minimize_likelihood(min_value,
                                minuit_pars[0], minuit_par_errs[0],
                                minuit_pars[1], minuit_par_errs[1],
                                minuit_pars[2], minuit_par_errs[2],
                                minuit_pars[3], minuit_par_errs[3],
                                false,
                                2);
  printf(" minuit ret %i\n", ret);

  printf("\n\n\n\nsignifififififif\n\n\n\n");
  int ret2;
  double sig = significance(ret, ret2);
  printf("significance %f\n", sig);

  fout->cd(); TTree* t_out = new TTree("t_out", "");

  for (int pp = 0; pp < 4; ++pp)
    t_out->Branch(TString::Format("manscan_%s", par_names[pp]), &glb_max_pars[pp], TString::Format("manscan_%s/D", par_names[pp]));

  for (int pp = 0; pp < 4; ++pp) {
    t_out->Branch(TString::Format("minuit_%s",     par_names[pp]), &minuit_pars[pp],     TString::Format("minuit_%s/D",     par_names[pp]));
    t_out->Branch(TString::Format("minuit_%s_err", par_names[pp]), &minuit_par_errs[pp], TString::Format("minuit_%s_err/D", par_names[pp]));
  }

  t_out->Branch("minuit_ret", &ret, "minuit_ret/I");
  t_out->Branch("minuit_ret2", &ret2, "minuit_ret/I");
  t_out->Branch("minuit_2lnLsb", &min_value, "minuit_val/D");
  t_out->Branch("sig", &sig, "sig/D");

  t_out->Fill();

#endif

  fout->Write();
  fout->Close();
  fin->Close();
  fsig->Close();
  delete fout;
  delete fin;
  delete fsig;
  delete c;
  return 0;
}
