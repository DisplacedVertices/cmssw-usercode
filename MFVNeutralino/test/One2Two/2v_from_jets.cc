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

bool clearing_from_eff = false;

bool dphi_from_hist = false;

bool dphi_from_pdf = true;
double dphi_pdf_c = 0;
double dphi_pdf_e = 2;
double dphi_pdf_a = 4.3;

int dvv_nbins = 40;
double dvv_bin_width = 0.01;

double    mu_clear = 0.0000;
double sigma_clear = 0.0000;

int min_ntracks0 = 0;
int max_ntracks0 = 1000000;
int min_ntracks1 = 0;
int max_ntracks1 = 1000000;

const char* tree_path = "/uscms_data/d3/jchu/crab_dirs/mfv_763p2/MinitreeV6p1_76x_nstlays3_8";

const int nbkg = 4;
const char* samples[nbkg] = {"qcdht1000", "qcdht1500", "qcdht2000", "ttbar"};
float weights[nbkg] = {6.166, 0.7894, 0.3320, 0.5620};

double n2v = 1121.;

float ht(int njets, float* jet_pt) {
  double sum = 0;
  for (int i = 0; i < njets; ++i) {
    sum += jet_pt[i];
  }
  return sum;
}

float throw_phi(int njets, float* jet_pt, float* jet_phi) {
  double rjetphi = 0;
  double rand = gRandom->Rndm();
  double sumpt = 0;
  for (int j = 0; j < njets; ++j) {
    sumpt += jet_pt[j];
    if (rand < sumpt/ht(njets, jet_pt)) {
      rjetphi = jet_phi[j];
      break;
    }
  }

  double rdphi = gRandom->Gaus(1.57, 0.4);

  double vtx_phi = 0;
  if (gRandom->Rndm() < 0.5) {
    vtx_phi = rjetphi - rdphi;
  } else {
    vtx_phi = rjetphi + rdphi;
  }

  return TVector2::Phi_mpi_pi(vtx_phi);
}

int main(int argc, const char* argv[]) {
  if (argc == 6) {
    mu_clear = atof(argv[1]);
    sigma_clear = atof(argv[2]);
    dphi_pdf_c = atof(argv[3]);
    dphi_pdf_e = atof(argv[4]);
    dphi_pdf_a = atof(argv[5]);
  }
  printf("mu_clear = %f, sigma_clear = %f, dphi_pdf_c = %f, dphi_pdf_e = %f, dphi_pdf_a = %f\n", mu_clear, sigma_clear, dphi_pdf_c, dphi_pdf_e, dphi_pdf_a);

  TH1::SetDefaultSumw2();
  gRandom->SetSeed(12191982);

  //fill only-one-vertex dBV distribution
  std::vector<double> bins;
  for (int j = 0; j < 20; ++j)
    bins.push_back(j*0.002);
  double b[] = {0.04, 0.0425, 0.045, 0.05, 0.055, 0.06, 0.07, 0.085, 0.1, 0.2, 0.4, 2.5};
  for (int j = 0; j < 12; ++j)
    bins.push_back(b[j]);
  TH1D* h_1v_dbv = new TH1D("h_1v_dbv", "only-one-vertex events;d_{BV} (cm);events", bins.size()-1, &bins[0]);
  TH1D* h_1v_dbv0 = new TH1D("h_1v_dbv0", "only-one-vertex events;d_{BV}^{0} (cm);events", bins.size()-1, &bins[0]);
  TH1D* h_1v_dbv1 = new TH1D("h_1v_dbv1", "only-one-vertex events;d_{BV}^{1} (cm);events", bins.size()-1, &bins[0]);
  TH1F* h_1v_phiv = new TH1F("h_1v_phiv", "only-one-vertex events;vertex #phi;events", 50, -3.15, 3.15);
  TH1F* h_1v_njets = new TH1F("h_1v_njets", "only-one-vertex events;number of jets;events", 20, 0, 20);
  TH1F* h_1v_ht = new TH1F("h_1v_ht", "only-one-vertex events;#Sigma H_{T} of jets (GeV);events", 200, 0, 5000);
  TH1F* h_1v_phij = new TH1F("h_1v_phij", "only-one-vertex events;jets #phi;jets", 50, -3.15, 3.15);
  TH1F* h_1v_dphijj = new TH1F("h_1v_dphijj", "only-one-vertex events;jet pair #Delta#phi;jet pairs", 50, -3.15, 3.15);
  TH1F* h_1v_dphijv = new TH1F("h_1v_dphijv", "only-one-vertex events;#Delta#phi(vertex position, jet momentum);jet-vertex pairs", 50, -3.15, 3.15);
  TH1F* h_2v_dbv = new TH1F("h_2v_dbv", "two-vertex events;d_{BV} (cm);vertices", 500, 0, 2.5);
  TH2F* h_2v_dbv1_dbv0 = new TH2F("h_2v_dbv1_dbv0", "two-vertex events;d_{BV}^{0} (cm);d_{BV}^{1} (cm)", 20, 0, 0.1, 20, 0, 0.1);
  TH1F* h_2v_dvv = new TH1F("h_2v_dvv", "two-vertex events;d_{VV} (cm);events", dvv_nbins, 0, dvv_nbins * dvv_bin_width);
  TH1F* h_2v_dphivv = new TH1F("h_2v_dphivv", "two-vertex events;#Delta#phi_{VV};events", 10, -3.15, 3.15);
  TH1F* h_2v_absdphivv = new TH1F("h_2v_absdphivv", "two-vertex events;|#Delta#phi_{VV}|;events", 5, 0, 3.15);

  for (int i = 0; i < nbkg; ++i) {
    mfv::MiniNtuple nt;
    TFile* f = TFile::Open(TString::Format("%s/%s.root", tree_path, samples[i]));
    if (!f || !f->IsOpen()) { fprintf(stderr, "bad file"); exit(1); }

    TTree* t = (TTree*)f->Get("mfvMiniTree/t");
    if (!t) { fprintf(stderr, "bad tree"); exit(1); }

    mfv::read_from_tree(t, nt);
    for (int j = 0, je = t->GetEntries(); j < je; ++j) {
      if (t->LoadTree(j) < 0) break;
      if (t->GetEntry(j) <= 0) continue;

      const float w = weights[i] * nt.weight;
      if (nt.nvtx == 1) {
        h_1v_dbv->Fill(sqrt(nt.x0*nt.x0 + nt.y0*nt.y0), w);
        if (nt.ntk0 >= min_ntracks0 && nt.ntk0 <= max_ntracks0) h_1v_dbv0->Fill(sqrt(nt.x0*nt.x0 + nt.y0*nt.y0), w);
        if (nt.ntk0 >= min_ntracks1 && nt.ntk0 <= max_ntracks1) h_1v_dbv1->Fill(sqrt(nt.x0*nt.x0 + nt.y0*nt.y0), w);
        h_1v_phiv->Fill(atan2(nt.y0,nt.x0), w);
        h_1v_njets->Fill(nt.njets, w);
        h_1v_ht->Fill(ht(nt.njets, nt.jet_pt), w);
        for (int k = 0; k < nt.njets; ++k) {
          h_1v_phij->Fill(nt.jet_phi[k], w);
          h_1v_dphijv->Fill(TVector2::Phi_mpi_pi(atan2(nt.y0,nt.x0) - nt.jet_phi[k]), w);
          for (int l = k+1; l < nt.njets; ++l) {
            h_1v_dphijj->Fill(TVector2::Phi_mpi_pi(nt.jet_phi[k] - nt.jet_phi[l]), w);
          }
        }
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

  //construct dvvc from only-one-vertex events
  TH1F* h_c1v_dbv = new TH1F("h_c1v_dbv", "constructed from only-one-vertex events;d_{BV} (cm);vertices", 500, 0, 2.5);
  TH1F* h_c1v_phiv = new TH1F("h_c1v_phiv", "constructed from only-one-vertex events;vertex #phi;vertices", 50, -3.15, 3.15);
  TH1F* h_c1v_dphijv = new TH1F("h_c1v_dphijv", "constructed from only-one-vertex events;#Delta#phi(vertex position, jet momentum);jet-vertex pairs", 50, -3.15, 3.15);
  TH1F* h_c1v_dvv = new TH1F("h_c1v_dvv", "constructed from only-one-vertex events;d_{VV} (cm);events", dvv_nbins, 0, dvv_nbins * dvv_bin_width);
  TH1F* h_c1v_dphivv = new TH1F("h_c1v_dphivv", "constructed from only-one-vertex events;#Delta#phi_{VV};events", 10, -3.15, 3.15);
  TH1F* h_c1v_absdphivv = new TH1F("h_c1v_absdphivv", "constructed from only-one-vertex events;|#Delta#phi_{VV}|;events", 5, 0, 3.15);
  TH1F* h_c1v_dbv0 = new TH1F("h_c1v_dbv0", "constructed from only-one-vertex events;d_{BV}^{0} (cm);events", 500, 0, 2.5);
  TH1F* h_c1v_dbv1 = new TH1F("h_c1v_dbv1", "constructed from only-one-vertex events;d_{BV}^{1} (cm);events", 500, 0, 2.5);
  TH2F* h_c1v_dbv1_dbv0 = new TH2F("h_c1v_dbv1_dbv0", "constructed from only-one-vertex events;d_{BV}^{0} (cm);d_{BV}^{1} (cm)", 20, 0, 0.1, 20, 0, 0.1);

  TH1D* h_r1v_dbv = new TH1D("h_r1v_dbv", "random from only-one-vertex events;d_{BV} (cm);events", bins.size()-1, &bins[0]);
  h_r1v_dbv->FillRandom(h_1v_dbv, (int)h_1v_dbv->Integral());

  TF1* f_dphi = new TF1("f_dphi", "abs(x - [0])**[1] + [2]", 0, M_PI);
  f_dphi->SetParameters(dphi_pdf_c, dphi_pdf_e, dphi_pdf_a);

  TH1F* h_dphi = new TH1F("h_dphi", "input to construction;|#Delta#phi_{VV}|;probability", 5, 0, 3.15);
  h_dphi->SetBinContent(1, 0.217011258006);
  h_dphi->SetBinContent(2, 0.142219424248);
  h_dphi->SetBinContent(3, 0.149300679564);
  h_dphi->SetBinContent(4, 0.214419648051);
  h_dphi->SetBinContent(5, 0.277049005032);

  TH1F* h_eff = new TH1F("h_eff", "input to construction;d_{VV} (cm);probability", 40, 0, 0.4);
  h_eff->SetBinContent(1, 0.0887200832367);
  h_eff->SetBinContent(2, 0.26492780447);
  h_eff->SetBinContent(3, 0.424160420895);
  h_eff->SetBinContent(4, 0.540564835072);
  h_eff->SetBinContent(5, 0.612435728312);
  h_eff->SetBinContent(6, 0.666476875544);
  h_eff->SetBinContent(7, 0.700767636299);
  h_eff->SetBinContent(8, 0.716090559959);
  h_eff->SetBinContent(9, 0.736099332571);
  h_eff->SetBinContent(10, 0.748791098595);
  h_eff->SetBinContent(11, 0.760122552514);
  h_eff->SetBinContent(12, 0.771965146065);
  h_eff->SetBinContent(13, 0.770971775055);
  h_eff->SetBinContent(14, 0.781980112195);
  h_eff->SetBinContent(15, 0.781406506896);
  h_eff->SetBinContent(16, 0.78949610889);
  h_eff->SetBinContent(17, 0.790535360575);
  h_eff->SetBinContent(18, 0.790518730879);
  h_eff->SetBinContent(19, 0.797075837851);
  h_eff->SetBinContent(20, 0.791352599859);
  h_eff->SetBinContent(21, 0.80023662746);
  h_eff->SetBinContent(22, 0.807722091675);
  h_eff->SetBinContent(23, 0.806445986032);
  h_eff->SetBinContent(24, 0.804875582457);
  h_eff->SetBinContent(25, 0.807317301631);
  h_eff->SetBinContent(26, 0.816252231598);
  h_eff->SetBinContent(27, 0.812310308218);
  h_eff->SetBinContent(28, 0.819209486246);
  h_eff->SetBinContent(29, 0.818562537432);
  h_eff->SetBinContent(30, 0.822052836418);
  h_eff->SetBinContent(31, 0.823742762208);
  h_eff->SetBinContent(32, 0.824828445911);
  h_eff->SetBinContent(33, 0.833424195647);
  h_eff->SetBinContent(34, 0.828828051686);
  h_eff->SetBinContent(35, 0.830597683787);
  h_eff->SetBinContent(36, 0.829892545938);
  h_eff->SetBinContent(37, 0.837587982416);
  h_eff->SetBinContent(38, 0.835536271334);
  h_eff->SetBinContent(39, 0.8477845788);
  h_eff->SetBinContent(40, 0.850240528584);
  h_eff->SetBinContent(41, 0.840228512883);

  for (int i = 0; i < nbkg; ++i) {
    mfv::MiniNtuple nt;
    TFile* f = TFile::Open(TString::Format("%s/%s.root", tree_path, samples[i]));
    if (!f || !f->IsOpen()) { fprintf(stderr, "bad file"); exit(1); }

    TTree* t = (TTree*)f->Get("mfvMiniTree/t");
    if (!t) { fprintf(stderr, "bad tree"); exit(1); }

    mfv::read_from_tree(t, nt);
    for (int j = 0, je = t->GetEntries(); j < je; ++j) {
      if (t->LoadTree(j) < 0) break;
      if (t->GetEntry(j) <= 0) continue;

      const float w = weights[i] * nt.weight;
      if (nt.nvtx == 1 && nt.njets > 0) {
        double dbv0 = h_1v_dbv0->GetRandom();
        double dbv1 = h_1v_dbv1->GetRandom();
        h_c1v_dbv->Fill(dbv0, w);
        h_c1v_dbv->Fill(dbv1, w);

        double phi0 = throw_phi(nt.njets, nt.jet_pt, nt.jet_phi);
        double phi1 = throw_phi(nt.njets, nt.jet_pt, nt.jet_phi);
        h_c1v_phiv->Fill(phi0, w);
        h_c1v_phiv->Fill(phi1, w);
        for (int k = 0; k < nt.njets; ++k) {
          h_c1v_dphijv->Fill(TVector2::Phi_mpi_pi(phi0 - nt.jet_phi[k]), w);
          h_c1v_dphijv->Fill(TVector2::Phi_mpi_pi(phi1 - nt.jet_phi[k]), w);
        }

        double dphi = TVector2::Phi_mpi_pi(phi0 - phi1);
        if (dphi_from_pdf) {
          dphi = f_dphi->GetRandom();
        }
        if (dphi_from_hist) {
          dphi = h_dphi->GetRandom();
        }

        double dvvc = sqrt(dbv0*dbv0 + dbv1*dbv1 - 2*dbv0*dbv1*cos(fabs(dphi)));

        double p = 0.5 * TMath::Erf((dvvc - mu_clear)/sigma_clear) + 0.5;
        if (clearing_from_eff) {
          p = h_eff->GetBinContent(h_eff->FindBin(dvvc));
        }

        if (dvvc > dvv_nbins * dvv_bin_width - 0.5*dvv_bin_width) dvvc = dvv_nbins * dvv_bin_width - 0.5*dvv_bin_width;
        h_c1v_dvv->Fill(dvvc, w * p);
        h_c1v_dphivv->Fill(dphi, w * p);
        h_c1v_absdphivv->Fill(fabs(dphi), w * p);
        h_c1v_dbv0->Fill(dbv0, w * p);
        h_c1v_dbv1->Fill(dbv1, w * p);
        h_c1v_dbv1_dbv0->Fill(dbv0, dbv1, w * p);
      }
    }
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
  h_2v_dbv->Write();
  h_2v_dbv1_dbv0->Write();
  h_2v_dvv->Write();
  h_2v_dphivv->Write();
  h_2v_absdphivv->Write();

  h_r1v_dbv->Write();
  h_c1v_dbv->Write();
  h_c1v_phiv->Write();
  h_c1v_dphijv->Write();
  h_c1v_dvv->Write();
  h_c1v_dphivv->Write();
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

  TCanvas* c_dphivv = new TCanvas("c_dphivv", "c_dphivv", 700, 700);
  TLegend* l_dphivv = new TLegend(0.25,0.75,0.75,0.85);
  h_2v_dphivv->SetTitle(";#Delta#phi_{VV};events");
  h_2v_dphivv->SetLineColor(kBlue);
  h_2v_dphivv->SetLineWidth(3);
  h_2v_dphivv->Scale(n2v/h_2v_dphivv->Integral());
  h_2v_dphivv->SetStats(0);
  h_2v_dphivv->Draw();
  l_dphivv->AddEntry(h_2v_dphivv, "two-vertex events");
  h_c1v_dphivv->SetLineColor(kRed);
  h_c1v_dphivv->SetLineWidth(3);
  h_c1v_dphivv->Scale(n2v/h_c1v_dphivv->Integral());
  h_c1v_dphivv->SetStats(0);
  h_c1v_dphivv->Draw("sames");
  l_dphivv->AddEntry(h_c1v_dphivv, "constructed from only-one-vertex events");
  l_dphivv->SetFillColor(0);
  l_dphivv->Draw();
  c_dphivv->SetTickx();
  c_dphivv->SetTicky();
  c_dphivv->Write();

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

  fh->Close();
}
