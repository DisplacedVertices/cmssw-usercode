// g++ -I $CMSSW_BASE/src -g -Wall `root-config --cflags --libs --glibs` ../../src/MiniNtuple.cc 2v_from_jets.cc -o 2v_from_jets.exe && ./2v_from_jets.exe

#include <cstdlib>
#include <math.h>
#include "TFile.h"
#include "TH1F.h"
#include "TMath.h"
#include "TRandom3.h"
#include "TTree.h"
#include "TVector2.h"
#include "JMTucker/MFVNeutralino/interface/MiniNtuple.h"

//predicted number of one-vertex-only events in 20/fb of data
//qcdht1000 + ttbardilep + ttbarhadronic + ttbarsemilep
const int n1v = 11406 + 101 + 4425 + 1458;
float bs2ddist[n1v];
unsigned short njets[n1v];
float jet_pts[n1v][50];
float jet_phis[n1v][50];

float sumht(int i) {
  double sum = 0;
  for (int j = 0; j < njets[i]; ++j) {
    sum += jet_pts[i][j];
  }
  return sum;
}

float throw_bs2ddist() {
  return bs2ddist[gRandom->Integer(n1v)];
}

float throw_phi(int i) {
  double rjetphi = 0;
  double rand = gRandom->Rndm();
  double sumpt = 0;
  for (int j = 0; j < njets[i]; ++j) {
    sumpt += jet_pts[i][j];
    if (rand < sumpt/sumht(i)) {
      rjetphi = jet_phis[i][j];
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

int toy_from_file(const char* sample, const int sn1vs, const int sn1v) {
  mfv::MiniNtuple nt;
  TFile* f = TFile::Open(TString::Format("/uscms_data/d2/tucker/crab_dirs/mfv_535/MiniTreeV18_Njets/%s.root", sample));
  if (!f || !f->IsOpen()) {
    fprintf(stderr, "bad file");
    exit(1);
  }

  TTree* t = (TTree*)f->Get("mfvMiniTree/t");
  if (!t) {
    fprintf(stderr, "bad tree");
    exit(1);
  }

  mfv::read_from_tree(t, nt);

  float sbs2ddist[sn1v];
  unsigned short snjets[sn1v];
  float sjet_pts[sn1v][50];
  float sjet_phis[sn1v][50];

  int i1v = 0;
  for (int j = 0, je = t->GetEntries(); j < je; ++j) {
    if (t->LoadTree(j) < 0) break;
    if (t->GetEntry(j) <= 0) continue;

    if (nt.nvtx == 2) continue;
    if (i1v < sn1v) {
      sbs2ddist[i1v] = sqrt(nt.x0*nt.x0 + nt.y0*nt.y0);
      snjets[i1v] = nt.njets;
      for (int i = 0; i < nt.njets; ++i) {
        sjet_pts[i1v][i] = nt.jet_pt[i];
        sjet_phis[i1v][i] = nt.jet_phi[i];
      }
    } else {
      if (gRandom->Rndm() > float(sn1v) / i1v) continue;
      int r = gRandom->Integer(sn1v);
      sbs2ddist[r] = sqrt(nt.x0*nt.x0 + nt.y0*nt.y0);
      snjets[r] = nt.njets;
      for (int i = 0; i < nt.njets; ++i) {
        sjet_pts[r][i] = nt.jet_pt[i];
        sjet_phis[r][i] = nt.jet_phi[i];
      }
    }
    i1v++;
  }
  if (i1v < sn1v) {
    printf("not enough v1vs (%d to sample %d of them)\n", i1v, sn1v);
    exit(1);
  }

  for (int i = 0; i < sn1v; ++i) {
    bs2ddist[sn1vs+i] = sbs2ddist[i];
    njets[sn1vs+i] = snjets[i];
    for (int j = 0; j < snjets[i]; ++j) {
      jet_pts[sn1vs+i][j] = sjet_pts[i][j];
      jet_phis[sn1vs+i][j] = sjet_phis[i][j];
    }
  }

  return 0;
}

int main() {
  gRandom->SetSeed(0);

  const int nbkg = 4;
  const char* samples[nbkg] = {"qcdht1000", "ttbardilep", "ttbarhadronic", "ttbarsemilep"};
  int sn1v[nbkg] = {11406, 101, 4425, 1458};
  int sn1vs = 0;
  for (int i = 0; i < nbkg; ++i) {
    toy_from_file(samples[i], sn1vs, sn1v[i]);
    sn1vs += sn1v[i];
  }

  TH1F* h_njets = new TH1F("h_njets", ";# of jets;events", 20, 0, 20);
  TH1F* h_jet_sum_ht = new TH1F("h_jet_sum_ht", ";#Sigma H_{T} of jets (GeV);events/25 GeV", 200, 0, 5000);
  TH1F* h_jetphi = new TH1F("h_jetphi", ";jets #phi (rad);jets/.063", 100, -3.1416, 3.1416);
  TH1F* h_jetpairdphi = new TH1F("h_jetpairdphi", ";jet pair #Delta#phi (rad);jet pairs/.063", 100, -3.1416, 3.1416);

  TH1F* h_sv0phi = new TH1F("h_sv0phi", ";constructed SV0 #phi (rad);events/.126", 50, -3.15, 3.15);
  TH1F* h_sv1phi = new TH1F("h_sv1phi", ";constructed SV1 #phi (rad);events/.126", 50, -3.15, 3.15);
  TH1F* h_sv0jetdphi = new TH1F("h_sv0jetdphi", ";constructed #Delta#phi(SV0, jets) (rad);jets/.126", 50, -3.15, 3.15);
  TH1F* h_sv1jetdphi = new TH1F("h_sv1jetdphi", ";constructed #Delta#phi(SV1, jets) (rad);jets/.126", 50, -3.15, 3.15);
  TH1F* h_svpairdphi = new TH1F("h_svpairdphi", ";constructed vertex pair #Delta#phi (rad);events/.126", 50, -3.15, 3.15);
  TH1F* h_svpairdphi_cut = new TH1F("h_svpairdphi_cut", "#Delta#phi with space clearing;constructed vertex pair #Delta#phi (rad);events/.126", 50, -3.15, 3.15);

  TH1F* h_sv0bs2ddist = new TH1F("h_sv0bs2ddist", ";constructed SV0 distance (cm);vertices", 500, 0, 1);
  TH1F* h_sv1bs2ddist = new TH1F("h_sv1bs2ddist", ";constructed SV1 distance (cm);vertices", 500, 0, 1);
  TH1F* h_svpairdist = new TH1F("h_svpairdist", ";constructed vertex pair distance (cm);events", 200, 0, 0.2);
  TH1F* h_svpairdist_cut = new TH1F("h_svpairdist_cut", "svdist2d with space clearing;constructed vertex pair distance (cm);events", 200, 0, 0.2);

  for (int i = 0; i < n1v; ++i) {
    h_njets->Fill(njets[i]);
    h_jet_sum_ht->Fill(sumht(i));
    for (int j = 0; j < njets[i]; ++j) {
      h_jetphi->Fill(jet_phis[i][j]);
      for (int k = j+1; k < njets[i]; ++k) {
        h_jetpairdphi->Fill(TVector2::Phi_mpi_pi(jet_phis[i][j] - jet_phis[i][k]));
      }
    }
    if (njets[i] > 0) {
      double vtx0_phi = throw_phi(i);
      double vtx1_phi = throw_phi(i);
      double dphi = TVector2::Phi_mpi_pi(vtx0_phi - vtx1_phi);

      double vtx0_dist = throw_bs2ddist();
      double vtx1_dist = throw_bs2ddist();

      h_sv0phi->Fill(vtx0_phi);
      h_sv1phi->Fill(vtx1_phi);
      for (int j = 0; j < njets[i]; ++j) {
        h_sv0jetdphi->Fill(TVector2::Phi_mpi_pi(vtx0_phi - jet_phis[i][j]));
        h_sv1jetdphi->Fill(TVector2::Phi_mpi_pi(vtx1_phi - jet_phis[i][j]));
      }
      h_svpairdphi->Fill(dphi);

      h_sv0bs2ddist->Fill(vtx0_dist);
      h_sv1bs2ddist->Fill(vtx1_dist);
      double svdist = sqrt(vtx0_dist*vtx0_dist + vtx1_dist*vtx1_dist - 2*vtx0_dist*vtx1_dist*cos(fabs(dphi)));
      h_svpairdist->Fill(svdist);

      if (TMath::Erf((svdist - 0.028)/0.005) > gRandom->Uniform(-1,1)) {
        h_svpairdphi_cut->Fill(dphi);
        h_svpairdist_cut->Fill(svdist);
      }
    }
  }
  TFile* fh = TFile::Open("2v_from_jets.root", "recreate");
  h_njets->Write();
  h_jet_sum_ht->Write();
  h_jetphi->Write();
  h_jetpairdphi->Write();

  h_sv0phi->Write();
  h_sv1phi->Write();
  h_sv0jetdphi->Write();
  h_sv1jetdphi->Write();
  h_svpairdphi->Write();
  h_svpairdphi_cut->Write();

  h_sv0bs2ddist->Write();
  h_sv1bs2ddist->Write();
  h_svpairdist->Write();
  h_svpairdist_cut->Write();

  fh->Close();
}
