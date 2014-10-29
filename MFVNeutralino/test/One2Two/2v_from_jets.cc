// g++ -I $CMSSW_BASE/src -g -Wall `root-config --cflags --libs --glibs` ../../src/MiniNtuple.cc 2v_from_jets.cc -o 2v_from_jets.exe && ./2v_from_jets.exe

#include <cstdlib>
#include <math.h>
#include "TCanvas.h"
#include "TFile.h"
#include "TH2F.h"
#include "TMath.h"
#include "TRandom3.h"
#include "TTree.h"
#include "TVector2.h"
#include "JMTucker/MFVNeutralino/interface/MiniNtuple.h"

double    mu_clear = 0.0300;
double sigma_clear = 0.0070;

const char* tree_path = "/uscms/home/tucker/crab_dirs/MiniTreeV20";

const int nbkg = 5;
const char* samples[nbkg] = {"qcdht0500", "qcdht1000", "ttbardilep", "ttbarhadronic", "ttbarsemilep"};
float weights[nbkg] = {2*4.849, 2*0.259, 2*0.037, 2*0.188, 2*0.075};

/*
const int nbkg = 1;
const char* samples[nbkg] = {"ttbarhadronic"};
float weights[nbkg] = {1};
*/

float sumht(int njets, float* jet_pt) {
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
    if (rand < sumpt/sumht(njets, jet_pt)) {
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

int throw_jet(int njets, float* jet_pt) {
  int jet = 0;
  double rand = gRandom->Rndm();
  double sumpt = 0;
  for (int j = 0; j < njets; ++j) {
    sumpt += jet_pt[j];
    if (rand < sumpt/sumht(njets, jet_pt)) {
      jet = j;
      break;
    }
  }
  return jet;
}

float throw_phi_from_jet(int j, float* jet_phi) {
  double rjetphi = jet_phi[j];

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
  TH1::SetDefaultSumw2();
  gRandom->SetSeed(12191982);

  //fill only-one-vertex dBV distribution
  TH1F* h_1v_dbv = new TH1F("h_1v_dbv", "only-one-vertex events;d_{BV} (cm);events", 500, 0, 2.5);
  TH1F* h_1v_phiv = new TH1F("h_1v_phiv", "only-one-vertex events;vertex #phi;events", 50, -3.15, 3.15);
  TH1F* h_1v_njets = new TH1F("h_1v_njets", "only-one-vertex events;number of jets;events", 20, 0, 20);
  TH1F* h_1v_sumht = new TH1F("h_1v_sumht", "only-one-vertex events;#Sigma H_{T} of jets (GeV);events", 200, 0, 5000);
  TH1F* h_1v_phij = new TH1F("h_1v_phij", "only-one-vertex events;jets #phi;jets", 50, -3.15, 3.15);
  TH1F* h_1v_dphijj = new TH1F("h_1v_dphijj", "only-one-vertex events;jet pair #Delta#phi;jet pairs", 50, -3.15, 3.15);
  TH1F* h_1v_dphijv = new TH1F("h_1v_dphijv", "only-one-vertex events;#Delta#phi(vertex position, jet momentum);jet-vertex pairs", 50, -3.15, 3.15);
  TH1F* h_2v_dvv = new TH1F("h_2v_dvv", "two-vertex events;d_{VV} (cm);events", 6, 0, 0.12);
  TH1F* h_2v_absdphivv = new TH1F("h_2v_absdphivv", "two-vertex events;|#Delta#phi(vertex #0, vertex #1)|;events", 5, 0, 3.15);

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
        h_1v_phiv->Fill(atan2(nt.y0,nt.x0), w);
        h_1v_njets->Fill(nt.njets, w);
        h_1v_sumht->Fill(sumht(nt.njets, nt.jet_pt), w);
        for (int k = 0; k < nt.njets; ++k) {
          h_1v_phij->Fill(nt.jet_phi[k], w);
          h_1v_dphijv->Fill(TVector2::Phi_mpi_pi(atan2(nt.y0,nt.x0) - nt.jet_phi[k]), w);
          for (int l = k+1; l < nt.njets; ++l) {
            h_1v_dphijj->Fill(TVector2::Phi_mpi_pi(nt.jet_phi[k] - nt.jet_phi[l]), w);
          }
        }
      }

      if (nt.nvtx == 2) {
        double dvv = sqrt((nt.x0-nt.x1)*(nt.x0-nt.x1) + (nt.y0-nt.y1)*(nt.y0-nt.y1));
        if (dvv > 0.11) dvv = 0.11;
        h_2v_dvv->Fill(dvv, w);
        h_2v_absdphivv->Fill(fabs(TVector2::Phi_mpi_pi(atan2(nt.y0,nt.x0)-atan2(nt.y1,nt.x1))), w);
      }
    }
  }

  //construct dvvc from only-one-vertex events
  TH1F* h_c1v_dbv = new TH1F("h_c1v_dbv", "constructed from only-one-vertex events;d_{BV} (cm);vertices", 500, 0, 2.5);
  TH1F* h_c1v_phiv = new TH1F("h_c1v_phiv", "constructed from only-one-vertex events;vertex #phi;vertices", 50, -3.15, 3.15);
  TH1F* h_c1v_dphijv = new TH1F("h_c1v_dphijv", "constructed from only-one-vertex events;#Delta#phi(vertex position, jet momentum);jet-vertex pairs", 50, -3.15, 3.15);
  TH1F* h_c1v_dvv = new TH1F("h_c1v_dvv", "constructed from only-one-vertex events;d_{VV} (cm);events", 6, 0, 0.12);
  TH1F* h_c1v_absdphivv = new TH1F("h_c1v_absdphivv", "constructed from only-one-vertex events;|#Delta#phi(vertex #0, vertex #1)|;events", 5, 0, 3.15);

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
        double dbv0 = h_1v_dbv->GetRandom();
        double dbv1 = h_1v_dbv->GetRandom();
        h_c1v_dbv->Fill(dbv0, w);
        h_c1v_dbv->Fill(dbv1, w);

        int jet0 = throw_jet(nt.njets, nt.jet_pt);
        int jet1 = throw_jet(nt.njets, nt.jet_pt);
/*
        float nm1_jet_pt[50];
        for (int k = 0; k < nt.njets; ++k) {
          if (k == jet0) {
            nm1_jet_pt[k] = 0;
          } else {
            nm1_jet_pt[k] = nt.jet_pt[k];
          }
        }
        int jet1 = throw_jet(nt.njets, nm1_jet_pt);
*/

        double phi0 = throw_phi_from_jet(jet0, nt.jet_phi);
        double phi1 = throw_phi_from_jet(jet1, nt.jet_phi);

        //double phi0 = throw_phi(nt.njets, nt.jet_pt, nt.jet_phi);
        //double phi1 = throw_phi(nt.njets, nt.jet_pt, nt.jet_phi);
        double dphi = TVector2::Phi_mpi_pi(phi0 - phi1);
        h_c1v_phiv->Fill(phi0, w);
        h_c1v_phiv->Fill(phi1, w);

        for (int k = 0; k < nt.njets; ++k) {
          h_c1v_dphijv->Fill(TVector2::Phi_mpi_pi(phi0 - nt.jet_phi[k]), w);
          h_c1v_dphijv->Fill(TVector2::Phi_mpi_pi(phi1 - nt.jet_phi[k]), w);
        }

        double dvvc = sqrt(dbv0*dbv0 + dbv1*dbv1 - 2*dbv0*dbv1*cos(fabs(dphi)));

        double p = 0.5 * TMath::Erf((dvvc - mu_clear)/sigma_clear) + 0.5;
        if (dvvc > 0.11) dvvc = 0.11;
        h_c1v_dvv->Fill(dvvc, w * p);
        h_c1v_absdphivv->Fill(fabs(dphi), w * p);
      }
    }
  }

  TFile* fh = TFile::Open("2v_from_jets.root", "recreate");

  h_1v_dbv->Write();
  h_1v_phiv->Write();
  h_1v_njets->Write();
  h_1v_sumht->Write();
  h_1v_phij->Write();
  h_1v_dphijj->Write();
  h_1v_dphijv->Write();
  h_2v_dvv->Write();
  h_2v_absdphivv->Write();

  h_c1v_dbv->Write();
  h_c1v_phiv->Write();
  h_c1v_dphijv->Write();
  h_c1v_dvv->Write();
  h_c1v_absdphivv->Write();

  TCanvas* c_dvv = new TCanvas("c_dvv", "c_dvv", 700, 700);
  h_2v_dvv->SetLineColor(kBlue);
  h_2v_dvv->SetLineWidth(3);
  h_2v_dvv->Scale(251./h_2v_dvv->Integral());
  h_2v_dvv->Draw();
  h_c1v_dvv->SetLineColor(kRed);
  h_c1v_dvv->SetLineWidth(3);
  h_c1v_dvv->Scale(251./h_c1v_dvv->Integral());
  h_c1v_dvv->Draw("sames");
  c_dvv->Write();

  TCanvas* c_absdphivv = new TCanvas("c_absdphivv", "c_absdphivv", 700, 700);
  h_2v_absdphivv->SetLineColor(kBlue);
  h_2v_absdphivv->SetLineWidth(3);
  h_2v_absdphivv->Scale(251./h_2v_absdphivv->Integral());
  h_2v_absdphivv->Draw();
  h_c1v_absdphivv->SetLineColor(kRed);
  h_c1v_absdphivv->SetLineWidth(3);
  h_c1v_absdphivv->Scale(251./h_c1v_absdphivv->Integral());
  h_c1v_absdphivv->Draw("sames");
  c_absdphivv->Write();

  fh->Close();
}
