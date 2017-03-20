// g++ -I $CMSSW_BASE/src -g -Wall `root-config --cflags --libs --glibs` ../../src/MiniNtuple.cc 2v_from_jets.cc -o 2v_from_jets.exe && ./2v_from_jets.exe

#include <cstdlib>
#include <math.h>
#include "TCanvas.h"
#include "TF1.h"
#include "TFile.h"
#include "TH2F.h"
#include "TLegend.h"
#include "TMath.h"
#include "TRandom3.h"
#include "TTree.h"
#include "TVector2.h"
#include "JMTucker/MFVNeutralino/interface/MiniNtuple.h"

int ntracks = 3;

int bquarks = -1;
bool vary_dphi = false;

bool clearing_from_eff = true;
const char* eff_file = "eff_avg.root";

double dphi_pdf_c = 1.37;
double dphi_pdf_e = 2;
double dphi_pdf_a = 3.50;

int dvv_nbins = 40;
double dvv_bin_width = 0.01;

const char* file_path = "/uscms_data/d2/tucker/crab_dirs/MinitreeV11/2016";

const int nbkg = 4;
const char* samples[nbkg] = {"qcdht1000sum", "qcdht1500sum", "qcdht2000sum", "ttbar"};
float weights[nbkg] = {3.13184, 0.40037, 0.16549, 0.75270};

float ht(int njets, float* jet_pt) {
  double sum = 0;
  for (int i = 0; i < njets; ++i) {
    sum += jet_pt[i];
  }
  return sum;
}

int throw_jet(int njets, float* jet_pt) {
  double rand = gRandom->Rndm();
  double sumpt = 0;
  for (int j = 0; j < njets; ++j) {
    sumpt += jet_pt[j];
    if (rand < sumpt/ht(njets, jet_pt)) {
      return j;
    }
  }
  return 0;
}

float throw_phi(int ijet, float* jet_phi, double rdphi) {
  double rjetphi = jet_phi[ijet];

  double vtx_phi = 0;
  if (gRandom->Rndm() < 0.5) {
    vtx_phi = rjetphi - rdphi;
  } else {
    vtx_phi = rjetphi + rdphi;
  }

  return TVector2::Phi_mpi_pi(vtx_phi);
}

float throw_dphi(int njets, float* jet_pt, float* jet_phi, double rdphi0, double rdphi1, bool with_replacement) {
  int ijet0 = throw_jet(njets, jet_pt);
  int ijet1 = throw_jet(njets, jet_pt);

  if (!with_replacement && njets > 1) {
    while (ijet1 == ijet0) {
      ijet1 = throw_jet(njets, jet_pt);
    }
  }

  float phi0 = throw_phi(ijet0, jet_phi, rdphi0);
  float phi1 = throw_phi(ijet1, jet_phi, rdphi1);
  return TVector2::Phi_mpi_pi(phi0 - phi1);
}

int main(int argc, const char* argv[]) {
  const char* tree_path;
  const char* eff_hist;
  double n1v;
  double n2v;
  int min_ntracks0 = 0;
  int max_ntracks0 = 1000000;
  int min_ntracks1 = 0;
  int max_ntracks1 = 1000000;

  if (ntracks == 3) {
    tree_path = "tre33/t";
    eff_hist = "average3";
    n1v = 297372.;
    n2v = 2117.;
  } else if (ntracks == 4) {
    tree_path = "tre44/t";
    eff_hist = "average4";
    n1v = 43003.;
    n2v = 44.;
  } else if (ntracks == 5) {
    tree_path = "mfvMiniTree/t";
    eff_hist = "average5";
    n1v = 6842.;
    n2v = 4.;
  } else if (ntracks == 7) {
    tree_path = "tre34/t";
    eff_hist = "average3";
    n1v = 339282.;
    n2v = 544.;
    min_ntracks0 = 4;
    max_ntracks0 = 4;
    min_ntracks1 = 3;
    max_ntracks1 = 3;
  } else {
    fprintf(stderr, "bad ntracks"); exit(1);
  }
  printf("tree_path = %s, eff_hist = %s, n1v = %d, n2v = %d\n", tree_path, eff_hist, int(n1v), int(n2v));

  if (argc == 6) {
    clearing_from_eff = true;
    eff_file = argv[1];
    eff_hist = argv[2];
    dphi_pdf_c = atof(argv[3]);
    dphi_pdf_e = atof(argv[4]);
    dphi_pdf_a = atof(argv[5]);
  }
  printf("eff_file = %s, eff_hist = %s, dphi_pdf_c = %f, dphi_pdf_e = %f, dphi_pdf_a = %f\n", eff_file, eff_hist, dphi_pdf_c, dphi_pdf_e, dphi_pdf_a);

  TH1::SetDefaultSumw2();
  gRandom->SetSeed(12191982);

  //fill only-one-vertex dBV distribution
  TH1D* h_1v_dbv = new TH1D("h_1v_dbv", "only-one-vertex events;d_{BV} (cm);events", 1250, 0, 2.5);
  TH1D* h_1v_dbv0 = new TH1D("h_1v_dbv0", "only-one-vertex events;d_{BV}^{0} (cm);events", 1250, 0, 2.5);
  TH1D* h_1v_dbv1 = new TH1D("h_1v_dbv1", "only-one-vertex events;d_{BV}^{1} (cm);events", 1250, 0, 2.5);
  TH1F* h_1v_phiv = new TH1F("h_1v_phiv", "only-one-vertex events;vertex #phi;events", 50, -3.15, 3.15);
  TH1F* h_1v_njets = new TH1F("h_1v_njets", "only-one-vertex events;number of jets;events", 20, 0, 20);
  TH1F* h_1v_ht = new TH1F("h_1v_ht", "only-one-vertex events;#Sigma H_{T} of jets (GeV);events", 200, 0, 5000);
  TH1F* h_1v_phij = new TH1F("h_1v_phij", "only-one-vertex events;jets #phi;jets", 50, -3.15, 3.15);
  TH1F* h_1v_dphijj = new TH1F("h_1v_dphijj", "only-one-vertex events;#Delta#phi_{JJ};jet pairs", 100, -3.1416, 3.1416);
  TH1F* h_1v_dphijv = new TH1F("h_1v_dphijv", "only-one-vertex events;#Delta#phi_{JV};jet-vertex pairs", 100, -3.1416, 3.1416);
  TH1F* h_1v_dphijvpt = new TH1F("h_1v_dphijvpt", "only-one-vertex events;p_{T}-weighted #Delta#phi_{JV};jet-vertex pairs", 100, -3.1416, 3.1416);
  TH1F* h_1v_dphijvmin = new TH1F("h_1v_dphijvmin", "only-one-vertex events;#Delta#phi_{JV}^{min};events", 50, 0, 3.1416);
  TH1F* h_2v_dbv = new TH1F("h_2v_dbv", "two-vertex events;d_{BV} (cm);vertices", 1250, 0, 2.5);
  TH2F* h_2v_dbv1_dbv0 = new TH2F("h_2v_dbv1_dbv0", "two-vertex events;d_{BV}^{0} (cm);d_{BV}^{1} (cm)", 1250, 0, 2.5, 1250, 0, 2.5);
  TH1F* h_2v_dvv = new TH1F("h_2v_dvv", "two-vertex events;d_{VV} (cm);events", dvv_nbins, 0, dvv_nbins * dvv_bin_width);
  TH1F* h_2v_dphivv = new TH1F("h_2v_dphivv", "two-vertex events;#Delta#phi_{VV};events", 10, -3.15, 3.15);
  TH1F* h_2v_absdphivv = new TH1F("h_2v_absdphivv", "two-vertex events;|#Delta#phi_{VV}|;events", 5, 0, 3.15);

  for (int i = 0; i < nbkg; ++i) {
    mfv::MiniNtuple nt;
    TFile* f = TFile::Open(TString::Format("%s/%s.root", file_path, samples[i]));
    if (!f || !f->IsOpen()) { fprintf(stderr, "bad file"); exit(1); }

    TTree* t = (TTree*)f->Get(tree_path);
    if (!t) { fprintf(stderr, "bad tree"); exit(1); }

    mfv::read_from_tree(t, nt);
    for (int j = 0, je = t->GetEntries(); j < je; ++j) {
      if (t->LoadTree(j) < 0) break;
      if (t->GetEntry(j) <= 0) continue;

      if ((bquarks == 0 && nt.gen_flavor_code == 2) || (bquarks == 1 && nt.gen_flavor_code != 2)) continue;

      const float w = weights[i] * nt.weight;
      if (nt.nvtx == 1) {
        h_1v_dbv->Fill(sqrt(nt.x0*nt.x0 + nt.y0*nt.y0), w);
        if (nt.ntk0 >= min_ntracks0 && nt.ntk0 <= max_ntracks0) h_1v_dbv0->Fill(sqrt(nt.x0*nt.x0 + nt.y0*nt.y0), w);
        if (nt.ntk0 >= min_ntracks1 && nt.ntk0 <= max_ntracks1) h_1v_dbv1->Fill(sqrt(nt.x0*nt.x0 + nt.y0*nt.y0), w);
        h_1v_phiv->Fill(atan2(nt.y0,nt.x0), w);
        h_1v_njets->Fill(nt.njets, w);
        h_1v_ht->Fill(ht(nt.njets, nt.jet_pt), w);
        double dphijvmin = M_PI;
        for (int k = 0; k < nt.njets; ++k) {
          h_1v_phij->Fill(nt.jet_phi[k], w);
          h_1v_dphijv->Fill(TVector2::Phi_mpi_pi(atan2(nt.y0,nt.x0) - nt.jet_phi[k]), w);
          h_1v_dphijvpt->Fill(TVector2::Phi_mpi_pi(atan2(nt.y0,nt.x0) - nt.jet_phi[k]), w * (nt.jet_pt[k]/ht(nt.njets, nt.jet_pt)));
          if (fabs(TVector2::Phi_mpi_pi(atan2(nt.y0,nt.x0) - nt.jet_phi[k])) < dphijvmin) dphijvmin = fabs(TVector2::Phi_mpi_pi(atan2(nt.y0,nt.x0) - nt.jet_phi[k]));
          for (int l = k+1; l < nt.njets; ++l) {
            h_1v_dphijj->Fill(TVector2::Phi_mpi_pi(nt.jet_phi[k] - nt.jet_phi[l]), w);
          }
        }
        h_1v_dphijvmin->Fill(dphijvmin, w);
      }

      if (nt.nvtx >= 2 && nt.ntk0 >= min_ntracks0 && nt.ntk0 <= max_ntracks0 && nt.ntk1 >= min_ntracks1 && nt.ntk1 <= max_ntracks1) {
        double dbv0 = sqrt(nt.x0*nt.x0 + nt.y0*nt.y0);
        double dbv1 = sqrt(nt.x1*nt.x1 + nt.y1*nt.y1);
        h_2v_dbv->Fill(dbv0, w);
        h_2v_dbv->Fill(dbv1, w);
        h_2v_dbv1_dbv0->Fill(dbv0, dbv1, w);
        double dvv = sqrt((nt.x0-nt.x1)*(nt.x0-nt.x1) + (nt.y0-nt.y1)*(nt.y0-nt.y1));
        if (dvv > dvv_nbins * dvv_bin_width - 0.5*dvv_bin_width) dvv = dvv_nbins * dvv_bin_width - 0.5*dvv_bin_width;
        h_2v_dvv->Fill(dvv, w);
        double dphi = TVector2::Phi_mpi_pi(atan2(nt.y0,nt.x0)-atan2(nt.y1,nt.x1));
        h_2v_dphivv->Fill(dphi, w);
        h_2v_absdphivv->Fill(fabs(dphi), w);
      }
    }
  }

  //construct dvvc
  TH1F* h_c1v_dbv = new TH1F("h_c1v_dbv", "constructed from only-one-vertex events;d_{BV} (cm);vertices", 1250, 0, 2.5);
  TH1F* h_c1v_dvv = new TH1F("h_c1v_dvv", "constructed from only-one-vertex events;d_{VV} (cm);events", dvv_nbins, 0, dvv_nbins * dvv_bin_width);
  TH1F* h_c1v_absdphivv = new TH1F("h_c1v_absdphivv", "constructed from only-one-vertex events;|#Delta#phi_{VV}|;events", 5, 0, 3.15);
  TH1F* h_c1v_dbv0 = new TH1F("h_c1v_dbv0", "constructed from only-one-vertex events;d_{BV}^{0} (cm);events", 1250, 0, 2.5);
  TH1F* h_c1v_dbv1 = new TH1F("h_c1v_dbv1", "constructed from only-one-vertex events;d_{BV}^{1} (cm);events", 1250, 0, 2.5);
  TH2F* h_c1v_dbv1_dbv0 = new TH2F("h_c1v_dbv1_dbv0", "constructed from only-one-vertex events;d_{BV}^{0} (cm);d_{BV}^{1} (cm)", 1250, 0, 2.5, 1250, 0, 2.5);

  TF1* f_dphi = new TF1("f_dphi", "(abs(x)-[0])**[1] + [2]", 0, M_PI);
  f_dphi->SetParameters(dphi_pdf_c, dphi_pdf_e, dphi_pdf_a);

  TF1* i_dphi = 0;
  TF1* i_dphi2 = 0;
  if (vary_dphi) {
    i_dphi = new TF1("i_dphi", "((1/([1]+1))*(x-[0])**([1]+1) + [2]*x - (1/([1]+1))*(-[0])**([1]+1)) / ((1/([1]+1))*(3.14159-[0])**([1]+1) + [2]*3.14159 - (1/([1]+1))*(-[0])**([1]+1))", 0, M_PI);
    i_dphi->SetParameters(dphi_pdf_c, dphi_pdf_e, dphi_pdf_a);
    i_dphi2 = new TF1("i_dphi2", "x/3.14159", 0, M_PI);
  }

  TH1F* h_eff = 0;
  if (clearing_from_eff) {
    h_eff = (TH1F*)TFile::Open(eff_file)->Get(eff_hist);
    h_eff->SetBinContent(h_eff->GetNbinsX()+1, h_eff->GetBinContent(h_eff->GetNbinsX()));
  }

  int bin2 = 0;
  int bin3 = 0;
  int intobin2 = 0;
  int intobin3 = 0;
  int outofbin2 = 0;
  int outofbin3 = 0;

  for (int i = 0; i < 20; ++i) {
    for (int j = 0; j < int(h_1v_dbv->GetEntries()); ++j) {
      double dbv0 = h_1v_dbv0->GetRandom();
      double dbv1 = h_1v_dbv1->GetRandom();
      h_c1v_dbv->Fill(dbv0);
      h_c1v_dbv->Fill(dbv1);

      double dphi = f_dphi->GetRandom();

      double dvvc = sqrt(dbv0*dbv0 + dbv1*dbv1 - 2*dbv0*dbv1*cos(dphi));

      if (vary_dphi) {
        double dphi2 = i_dphi2->GetX(i_dphi->Eval(dphi), 0, M_PI);
        double dvvc2 = sqrt(dbv0*dbv0 + dbv1*dbv1 - 2*dbv0*dbv1*cos(dphi2));
        if (dvvc >= 0.04 && dvvc < 0.07) ++bin2;
        if (dvvc >= 0.07) ++bin3;
        if (!(dvvc >= 0.04 && dvvc < 0.07) && (dvvc2 >= 0.04 && dvvc2 < 0.07)) ++intobin2;
        if (!(dvvc >= 0.07) && (dvvc2 >= 0.07)) ++intobin3;
        if ((dvvc >= 0.04 && dvvc < 0.07) && !(dvvc2 >= 0.04 && dvvc2 < 0.07)) ++outofbin2;
        if ((dvvc >= 0.07) && !(dvvc2 >= 0.07)) ++outofbin3;
        dphi = dphi2;
        dvvc = dvvc2;
      }

      double p = 1;
      if (clearing_from_eff) {
        p = h_eff->GetBinContent(h_eff->FindBin(dvvc));
      }

      if (dvvc > dvv_nbins * dvv_bin_width - 0.5*dvv_bin_width) dvvc = dvv_nbins * dvv_bin_width - 0.5*dvv_bin_width;
      h_c1v_dvv->Fill(dvvc, p);
      h_c1v_absdphivv->Fill(fabs(dphi), p);
      h_c1v_dbv0->Fill(dbv0, p);
      h_c1v_dbv1->Fill(dbv1, p);
      h_c1v_dbv1_dbv0->Fill(dbv0, dbv1, p);
    }
  }

  if (vary_dphi) {
    printf("bin2 = %d, bin3 = %d, intobin2 = %d, intobin3 = %d, outofbin2 = %d, outofbin3 = %d\n", bin2, bin3, intobin2, intobin3, outofbin2, outofbin3);
    printf("uncorrelated variation / default (bin 2): %f +/- %f\n", 1 + (intobin2 - outofbin2) / (1.*bin2), sqrt(bin2 + bin2 + intobin2 - outofbin2) / bin2);
    printf("  correlated variation / default (bin 2): %f +/- %f\n", 1 + (intobin2 - outofbin2) / (1.*bin2), sqrt(intobin2 + outofbin2) / bin2);
    printf("uncertainty correlated / uncorrelated (bin 2): %f\n", sqrt(intobin2 + outofbin2) / sqrt(bin2 + bin2 + intobin2 - outofbin2));
    printf("uncorrelated variation / default (bin 3): %f +/- %f\n", 1 + (intobin3 - outofbin3) / (1.*bin3), sqrt(bin3 + bin3 + intobin3 - outofbin3) / bin3);
    printf("  correlated variation / default (bin 3): %f +/- %f\n", 1 + (intobin3 - outofbin3) / (1.*bin3), sqrt(intobin3 + outofbin3) / bin3);
    printf("uncertainty correlated / uncorrelated (bin 3): %f\n", sqrt(intobin3 + outofbin3) / sqrt(bin3 + bin3 + intobin3 - outofbin3));
  }

  TFile* fh = TFile::Open("2v_from_jets.root", "recreate");

  h_1v_dbv->Write();
  h_1v_dbv0->Write();
  h_1v_dbv1->Write();
  h_1v_phiv->Write();
  h_1v_njets->Write();
  h_1v_ht->Write();
  h_1v_phij->Write();
  h_1v_dphijj->Write();
  h_1v_dphijv->Write();
  h_1v_dphijvpt->Write();
  h_1v_dphijvmin->Write();
  h_2v_dbv->Write();
  h_2v_dbv1_dbv0->Write();
  h_2v_dvv->Write();
  h_2v_dphivv->Write();
  h_2v_absdphivv->Write();

  h_c1v_dbv->Write();
  h_c1v_dvv->Write();
  h_c1v_absdphivv->Write();
  h_c1v_dbv0->Write();
  h_c1v_dbv1->Write();
  h_c1v_dbv1_dbv0->Write();

  TCanvas* c_dvv = new TCanvas("c_dvv", "c_dvv", 700, 700);
  TLegend* l_dvv = new TLegend(0.35,0.75,0.85,0.85);
  h_2v_dvv->SetTitle(";d_{VV} (cm);events");
  h_2v_dvv->SetLineColor(kBlue);
  h_2v_dvv->SetLineWidth(3);
  h_2v_dvv->Scale(n2v/h_2v_dvv->Integral());
  h_2v_dvv->SetStats(0);
  h_2v_dvv->Draw();
  l_dvv->AddEntry(h_2v_dvv, "two-vertex events");
  h_c1v_dvv->SetLineColor(kRed);
  h_c1v_dvv->SetLineWidth(3);
  h_c1v_dvv->Scale(n2v/h_c1v_dvv->Integral());
  h_c1v_dvv->SetStats(0);
  h_c1v_dvv->Draw("sames");
  l_dvv->AddEntry(h_c1v_dvv, "constructed from only-one-vertex events");
  l_dvv->SetFillColor(0);
  l_dvv->Draw();
  c_dvv->SetTickx();
  c_dvv->SetTicky();
  c_dvv->Write();

  TCanvas* c_absdphivv = new TCanvas("c_absdphivv", "c_absdphivv", 700, 700);
  TLegend* l_absdphivv = new TLegend(0.25,0.75,0.75,0.85);
  h_2v_absdphivv->SetTitle(";|#Delta#phi_{VV}|;events");
  h_2v_absdphivv->SetLineColor(kBlue);
  h_2v_absdphivv->SetLineWidth(3);
  h_2v_absdphivv->Scale(n2v/h_2v_absdphivv->Integral());
  h_2v_absdphivv->SetStats(0);
  h_2v_absdphivv->Draw();
  l_absdphivv->AddEntry(h_2v_absdphivv, "two-vertex events");
  h_c1v_absdphivv->SetLineColor(kRed);
  h_c1v_absdphivv->SetLineWidth(3);
  h_c1v_absdphivv->Scale(n2v/h_c1v_absdphivv->Integral());
  h_c1v_absdphivv->SetStats(0);
  h_c1v_absdphivv->Draw("sames");
  l_absdphivv->AddEntry(h_c1v_absdphivv, "constructed from only-one-vertex events");
  l_absdphivv->SetFillColor(0);
  l_absdphivv->Draw();
  c_absdphivv->SetTickx();
  c_absdphivv->SetTicky();
  c_absdphivv->Write();

  f_dphi->Write();
  if (clearing_from_eff) {
    h_eff->SetName("h_eff");
    h_eff->Write();
  }
  if (vary_dphi) {
    i_dphi->Write();
    i_dphi2->Write();
  }

  fh->Close();
}
