// g++ -I $CMSSW_BASE/src -g -Wall `root-config --cflags --libs --glibs` ../../src/MiniNtuple.cc 2v_from_jets.cc -o 2v_from_jets.exe && ./2v_from_jets.exe

#include <cstdlib>
#include <math.h>
#include "TCanvas.h"
#include "TFile.h"
#include "TH2F.h"
#include "TLegend.h"
#include "TMath.h"
#include "TRandom3.h"
#include "TTree.h"
#include "TVector2.h"
#include "JMTucker/MFVNeutralino/interface/MiniNtuple.h"

double    muclear = 0.028;
double sigmaclear = 0.005;

const char* tree_path = "/uscms/home/tucker/crab_dirs/MiniTreeV20";
//const char* sample_name = "ttbarhadronic";
//const int n1v = 18508;

//predicted number of one-vertex-only events in 17.6/fb of data
//qcdht1000 + ttbardilep + ttbarhadronic + ttbarsemilep
const int n1v = 9235 + 99 + 3598 + 1274;
float bs2ddist[n1v];
float vtx_phis[n1v];
unsigned short njets[n1v];
float jet_pts[n1v][50];
float jet_phis[n1v][50];
float puweights[n1v];

float x[n1v], y[n1v], z[n1v], cxx[n1v], cxy[n1v], cxz[n1v], cyy[n1v], cyz[n1v], czz[n1v];

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

float throw_uniform_phi() {
  return gRandom->Uniform(-M_PI, M_PI);
}

float throw_gaussian_phi(int i) {
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

float throw_phi(int njets, float* jet_pt, float* jet_phi) {
  double sumht = 0;
  for (int j = 0; j < njets; ++j) {
    sumht += jet_pt[j];
  }

  double rjetphi = 0;
  double rand = gRandom->Rndm();
  double sumpt = 0;
  for (int j = 0; j < njets; ++j) {
    sumpt += jet_pt[j];
    if (rand < sumpt/sumht) {
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

int toy_from_file(const char* sample, const int sn1vs, const int sn1v) {
  mfv::MiniNtuple nt;
  TFile* f = TFile::Open(TString::Format("%s/%s.root", tree_path, sample));
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
  float svtx_phis[sn1v];
  unsigned short snjets[sn1v];
  float sjet_pts[sn1v][50];
  float sjet_phis[sn1v][50];
  float spuweights[sn1v];
  float sx[sn1v], sy[sn1v], sz[sn1v], scxx[sn1v], scxy[sn1v], scxz[sn1v], scyy[sn1v], scyz[sn1v], sczz[sn1v];

  int i1v = 0;
  for (int j = 0, je = t->GetEntries(); j < je; ++j) {
    if (t->LoadTree(j) < 0) break;
    if (t->GetEntry(j) <= 0) continue;

    if (nt.nvtx == 2) continue;
    //if (nt.npu > 17) continue;
    //if (nt.npu < 18 || nt.npu > 24) continue;
    //if (nt.npu < 25) continue;
    if (i1v < sn1v) {
      sbs2ddist[i1v] = sqrt(nt.x0*nt.x0 + nt.y0*nt.y0);
      svtx_phis[i1v] = atan2(nt.y0, nt.x0);
      snjets[i1v] = nt.njets;
      for (int i = 0; i < nt.njets; ++i) {
        sjet_pts[i1v][i] = nt.jet_pt[i];
        sjet_phis[i1v][i] = nt.jet_phi[i];
      }
      spuweights[i1v] = nt.weight;
      sx[i1v] = nt.x0; sy[i1v] = nt.y0; sz[i1v] = nt.z0; scxx[i1v] = nt.cxx0; scxy[i1v] = nt.cxy0; scxz[i1v] = nt.cxz0; scyy[i1v] = nt.cyy0; scyz[i1v] = nt.cyz0; sczz[i1v] = nt.czz0;
    } else {
      if (gRandom->Rndm() > float(sn1v) / i1v) continue;
      int r = gRandom->Integer(sn1v);
      sbs2ddist[r] = sqrt(nt.x0*nt.x0 + nt.y0*nt.y0);
      svtx_phis[r] = atan2(nt.y0, nt.x0);
      snjets[r] = nt.njets;
      for (int i = 0; i < nt.njets; ++i) {
        sjet_pts[r][i] = nt.jet_pt[i];
        sjet_phis[r][i] = nt.jet_phi[i];
      }
      spuweights[r] = nt.weight;
      sx[r] = nt.x0; sy[r] = nt.y0; sz[r] = nt.z0; scxx[r] = nt.cxx0; scxy[r] = nt.cxy0; scxz[r] = nt.cxz0; scyy[r] = nt.cyy0; scyz[r] = nt.cyz0; sczz[r] = nt.czz0;
    }
    i1v++;
  }
  if (i1v < sn1v) {
    printf("not enough v1vs (%d to sample %d of them)\n", i1v, sn1v);
    exit(1);
  }

  for (int i = 0; i < sn1v; ++i) {
    bs2ddist[sn1vs+i] = sbs2ddist[i];
    vtx_phis[sn1vs+i] = svtx_phis[i];
    njets[sn1vs+i] = snjets[i];
    for (int j = 0; j < snjets[i]; ++j) {
      jet_pts[sn1vs+i][j] = sjet_pts[i][j];
      jet_phis[sn1vs+i][j] = sjet_phis[i][j];
    }
    puweights[sn1vs+i] = spuweights[i];
    x[sn1vs+i] = sx[i]; y[sn1vs+i] = sy[i]; z[sn1vs+i] = sz[i]; cxx[sn1vs+i] = scxx[i]; cxy[sn1vs+i] = scxy[i]; cxz[sn1vs+i] = scxz[i]; cyy[sn1vs+i] = scyy[i]; cyz[sn1vs+i] = scyz[i]; czz[sn1vs+i] = sczz[i];
  }

  return 0;
}

std::vector<double> binning() {
  std::vector<double> bins;
  for (int i = 0; i < 5; ++i)
    bins.push_back(i * 0.02);
  bins.push_back(0.1);
  bins.push_back(5.0);
  return bins;
}

TH1D* hist_with_binning(const char* name, const char* title) {
  std::vector<double> bins = binning();
  return new TH1D(name, title, bins.size()-1, &bins[0]);
}

int main(int argc, const char* argv[]) {
  if (argc == 3) {
    muclear = atof(argv[1]);
    sigmaclear = atof(argv[2]);
  }

  TH1::SetDefaultSumw2();
  gRandom->SetSeed(0);

  TH1F* h_vtxjetdphi = new TH1F("h_vtxjetdphi", ";#Delta#phi(vertex position, jet momentum);arb. units", 50, -3.15, 3.15);
  TH1F* h_vtx0jetdphi = new TH1F("h_vtx0jetdphi", ";#Delta#phi(vertex0 position, jet momentum);arb. units", 50, -3.15, 3.15);
  TH1F* h_vtx1jetdphi = new TH1F("h_vtx1jetdphi", ";#Delta#phi(vertex1 position, jet momentum);arb. units", 50, -3.15, 3.15);
  TH1F* h_svdist2d = new TH1F("h_svdist2d", ";dist2d(sv #0, #1) (cm);arb. units", 30, 0, 0.3);
  TH1D* h_dvv = hist_with_binning("h_dvv", ";d_{VV} (cm);arb. units");
  TH1F* h_absdeltaphi01 = new TH1F("h_absdeltaphi01", ";abs(delta(phi of sv #0, phi of sv #1));arb. units", 5, 0, 3.15);
  TH1D* h_sigmavv = new TH1D("h_sigmavv", ";#sigma(sv #0, #1) (cm);arb. units", 10, 0, 0.01);
  TH1D* h_sigvv = new TH1D("h_sigvv", ";N#sigma(sv #0, #1);arb. units", 15, 0, 30);
  TH2F* h_sigmavv_dvv = new TH2F("h_sigmavv_dvv", "two-vertex MC;d_{vv} (cm);#sigma_{vv} (cm)", 30, 0, 0.3, 10, 0, 0.01);
  TH1F* h_dvv_low_njets = new TH1F("h_dvv_low_njets", "njets <= 6;d_{vv} (cm);arb. units", 10, 0, 0.1);
  TH1F* h_dvv_high_njets = new TH1F("h_dvv_high_njets", "njets >= 7;d_{vv} (cm);arb. units", 10, 0, 0.1);

  const int nbkg = 4;
  const char* samples[nbkg] = {"qcdht1000", "ttbardilep", "ttbarhadronic", "ttbarsemilep"};
  float weights[nbkg] = {0.259, 0.037, 0.188, 0.075};
  int sn1v[nbkg] = {9235, 99, 3598, 1274};
  int sn1vs = 0;

/*
  const int nbkg = 1;
  const char* samples[nbkg] = {sample_name};
  float weights[nbkg] = {1};
  int sn1v[nbkg] = {n1v};
  int sn1vs = 0;
*/

  TH1F* h_dbv_1v = new TH1F("h_dbv_1v", "only-one-vertex events;d_{BV};events", 500, 0, 2.5);
  TH1F* h_dvvc = new TH1F("h_dvvc", ";d_{VV}^{C} (cm);events", 6, 0, 0.12);

  for (int i = 0; i < nbkg; ++i) {
    toy_from_file(samples[i], sn1vs, sn1v[i]);
    sn1vs += sn1v[i];

    mfv::MiniNtuple nt;
    TFile* f = TFile::Open(TString::Format("%s/%s.root", tree_path, samples[i]));
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
    for (int j = 0, je = t->GetEntries(); j < je; ++j) {
      if (t->LoadTree(j) < 0) break;
      if (t->GetEntry(j) <= 0) continue;

      if (nt.nvtx == 1) {
        h_dbv_1v->Fill(sqrt(nt.x0*nt.x0 + nt.y0*nt.y0), weights[i] * nt.weight);
      }

      if (nt.nvtx == 2) {
        for (int k = 0; k < nt.njets; ++k) {
          h_vtxjetdphi->Fill(TVector2::Phi_mpi_pi(atan2(nt.y0,nt.x0) - nt.jet_phi[k]), weights[i] * nt.weight);
          h_vtxjetdphi->Fill(TVector2::Phi_mpi_pi(atan2(nt.y1,nt.x1) - nt.jet_phi[k]), weights[i] * nt.weight);
          h_vtx0jetdphi->Fill(TVector2::Phi_mpi_pi(atan2(nt.y0,nt.x0) - nt.jet_phi[k]), weights[i] * nt.weight);
          h_vtx1jetdphi->Fill(TVector2::Phi_mpi_pi(atan2(nt.y1,nt.x1) - nt.jet_phi[k]), weights[i] * nt.weight);
        }
        h_svdist2d->Fill(sqrt((nt.x0-nt.x1)*(nt.x0-nt.x1) + (nt.y0-nt.y1)*(nt.y0-nt.y1)), weights[i] * nt.weight);
        h_absdeltaphi01->Fill(fabs(TVector2::Phi_mpi_pi(atan2(nt.y0,nt.x0)-atan2(nt.y1,nt.x1))), weights[i] * nt.weight);

        float svdist2d = sqrt((nt.x0-nt.x1)*(nt.x0-nt.x1) + (nt.y0-nt.y1)*(nt.y0-nt.y1));
        float dx = (nt.x0-nt.x1) / svdist2d;
        float dy = (nt.y0-nt.y1) / svdist2d;
        float sigma = sqrt((nt.cxx0 + nt.cxx1)*dx*dx + (nt.cyy0 + nt.cyy1)*dy*dy + 2*(nt.cxy0 + nt.cxy1)*dx*dy);
        h_dvv->Fill(svdist2d, weights[i] * nt.weight);
        h_sigmavv->Fill(sigma);
        h_sigvv->Fill(svdist2d / sigma);
        h_sigmavv_dvv->Fill(svdist2d, sigma);
        if (nt.njets <= 6) {
          h_dvv_low_njets->Fill(svdist2d);
        } else {
          h_dvv_high_njets->Fill(svdist2d);
        }
      }
    }
  }

  for (int i = 0; i < nbkg; ++i) {
    mfv::MiniNtuple nt;
    TFile* f = TFile::Open(TString::Format("%s/%s.root", tree_path, samples[i]));
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
    for (int j = 0, je = t->GetEntries(); j < je; ++j) {
      if (t->LoadTree(j) < 0) break;
      if (t->GetEntry(j) <= 0) continue;

      if (nt.nvtx == 1) {
        double vtx0_phi = throw_phi(nt.njets, nt.jet_pt, nt.jet_phi);
        double vtx1_phi = throw_phi(nt.njets, nt.jet_pt, nt.jet_phi);
        double dphi = TVector2::Phi_mpi_pi(vtx0_phi - vtx1_phi);

        double vtx0_dist = h_dbv_1v->GetRandom();
        double vtx1_dist = h_dbv_1v->GetRandom();

        double svdist = sqrt(vtx0_dist*vtx0_dist + vtx1_dist*vtx1_dist - 2*vtx0_dist*vtx1_dist*cos(fabs(dphi)));

        double p = 0.5 * TMath::Erf((svdist - muclear)/sigmaclear) + 0.5;
        if (svdist > 0.11) svdist = 0.11;
        h_dvvc->Fill(svdist, weights[i] * nt.weight * p);
      }
    }
  }

  //toy_from_file("MultiJetPk2012", 0, 17390);

  TH1F* h_njets = new TH1F("h_njets", ";# of jets;events", 20, 0, 20);
  TH1F* h_jet_sum_ht = new TH1F("h_jet_sum_ht", ";#Sigma H_{T} of jets (GeV);events/25 GeV", 200, 0, 5000);
  TH1F* h_jetphi = new TH1F("h_jetphi", ";jets #phi (rad);jets/.063", 100, -3.1416, 3.1416);
  TH1F* h_jetpairdphi = new TH1F("h_jetpairdphi", ";jet pair #Delta#phi (rad);jet pairs/.063", 100, -3.1416, 3.1416);

  TH1F* h_sv0phi = new TH1F("h_sv0phi", ";constructed SV0 #phi (rad);events/.126", 50, -3.15, 3.15);
  TH1F* h_sv1phi = new TH1F("h_sv1phi", ";constructed SV1 #phi (rad);events/.126", 50, -3.15, 3.15);
  TH1F* h_svjetdphi = new TH1F("h_svjetdphi", ";#Delta#phi(vertex position, jet momentum);arb. units", 50, -3.15, 3.15);
  TH1F* h_sv0jetdphi = new TH1F("h_sv0jetdphi", ";constructed #Delta#phi(SV0, jets) (rad);jets/.126", 50, -3.15, 3.15);
  TH1F* h_sv1jetdphi = new TH1F("h_sv1jetdphi", ";constructed #Delta#phi(SV1, jets) (rad);jets/.126", 50, -3.15, 3.15);
  TH1F* h_svpairdphi = new TH1F("h_svpairdphi", ";constructed vertex pair #Delta#phi (rad);events/.126", 50, -3.15, 3.15);
  TH1F* h_svpairdphi_cut = new TH1F("h_svpairdphi_cut", "#Delta#phi with space clearing;constructed vertex pair #Delta#phi (rad);events/.126", 50, -3.15, 3.15);
  TH1F* h_svpairabsdphi = new TH1F("h_svpairabsdphi", "|#Delta#phi| with space clearing;constructed vertex pair |#Delta#phi| (rad);events/.63", 5, 0, 3.15);

  TH1F* h_bs2ddist1v = new TH1F("h_bs2ddist1v", "one-vertex-only events;bs2ddist;arb. units", 500, 0, 0.1);
  TH1F* h_sv0bs2ddist = new TH1F("h_sv0bs2ddist", ";constructed SV0 distance (cm);vertices", 500, 0, 1);
  TH1F* h_sv1bs2ddist = new TH1F("h_sv1bs2ddist", ";constructed SV1 distance (cm);vertices", 500, 0, 1);
  TH1F* h_svpairdist = new TH1F("h_svpairdist", ";constructed vertex pair distance (cm);events", 200, 0, 0.2);
  TH1F* h_svpairdist_cut = new TH1F("h_svpairdist_cut", "svdist2d with space clearing;constructed vertex pair distance (cm);events", 30, 0, 0.3);
  //TH1D* h_dvvc = hist_with_binning("h_dvvc", ";d_{VV}^{C} (cm);arb. units");

  TH1F* h_svdist2d_uniformphi = new TH1F("h_svdist2d_uniformphi", "svdist2d using uniform #phi distribution;constructed vertex pair distance (cm);events", 10, 0, 0.1);
  float sigma_clear[5] = {30, 40, 50, 60, 70};
  TH1F* h_svdist2d_sigma[5];
  TH1F* h_svdist2d_mu[5];
  float mu_clear[5] = {260, 270, 280, 290, 300};
  for (int i = 0; i < 5; ++i) {
    h_svdist2d_mu[i] = new TH1F(TString::Format("h_svdist2d_mu_%i", i), TString::Format("svdist2d with #mu_{clear} = %f #mum;constructed vertex pair distance (cm);events", mu_clear[i]), 10, 0, 0.1);
    h_svdist2d_sigma[i] = new TH1F(TString::Format("h_svdist2d_sigma_%i", i), TString::Format("svdist2d with #sigma_{clear} = %f #mum;constructed vertex pair distance (cm);events", sigma_clear[i]), 10, 0, 0.1);
  }

  TH1F* h_dvv_jets_low = new TH1F("h_dvv_jets_low", "njets <= 6;d_{vv} (cm);arb. units", 10, 0, 0.1);
  TH1F* h_dvv_jets_high = new TH1F("h_dvv_jets_high", "njets >= 7;d_{vv} (cm);arb. units", 10, 0, 0.1);

  for (int i = 0; i < n1v; ++i) {
    const float w = puweights[i];

    h_bs2ddist1v->Fill(bs2ddist[i], w);
    h_njets->Fill(njets[i], w);
    h_jet_sum_ht->Fill(sumht(i), w);
    for (int j = 0; j < njets[i]; ++j) {
      h_jetphi->Fill(jet_phis[i][j], w);
      for (int k = j+1; k < njets[i]; ++k) {
        h_jetpairdphi->Fill(TVector2::Phi_mpi_pi(jet_phis[i][j] - jet_phis[i][k]), w);
      }
      h_svjetdphi->Fill(TVector2::Phi_mpi_pi(vtx_phis[i] - jet_phis[i][j]), w);
    }
    if (njets[i] > 0) {
      double vtx0_phi = throw_gaussian_phi(i);
      double vtx1_phi = throw_gaussian_phi(i);
      double dphi = TVector2::Phi_mpi_pi(vtx0_phi - vtx1_phi);

      double vtx0_dist = throw_bs2ddist();
      double vtx1_dist = throw_bs2ddist();

      h_sv0phi->Fill(vtx0_phi, w);
      h_sv1phi->Fill(vtx1_phi, w);
      for (int j = 0; j < njets[i]; ++j) {
        h_sv0jetdphi->Fill(TVector2::Phi_mpi_pi(vtx0_phi - jet_phis[i][j]), w);
        h_sv1jetdphi->Fill(TVector2::Phi_mpi_pi(vtx1_phi - jet_phis[i][j]), w);
      }
      h_svpairdphi->Fill(dphi, w);

      h_sv0bs2ddist->Fill(vtx0_dist, w);
      h_sv1bs2ddist->Fill(vtx1_dist, w);
      double svdist = sqrt(vtx0_dist*vtx0_dist + vtx1_dist*vtx1_dist - 2*vtx0_dist*vtx1_dist*cos(fabs(dphi)));
      h_svpairdist->Fill(svdist, w);

      double p = 0.5 * TMath::Erf((svdist - muclear)/sigmaclear) + 0.5;
      h_svpairdphi_cut->Fill(dphi, w * p);
      h_svpairabsdphi->Fill(fabs(dphi), w * p);
      h_svpairdist_cut->Fill(svdist, w * p);
      //h_dvvc->Fill(svdist, w * p);

      if (njets[i] <= 6) {
        h_dvv_jets_low->Fill(svdist, w * p);
      } else {
        h_dvv_jets_high->Fill(svdist, w * p);
      }

      double dphi_uniformphi = TVector2::Phi_mpi_pi(throw_uniform_phi() - throw_uniform_phi());
      double svdist_uniformphi = sqrt(vtx0_dist*vtx0_dist + vtx1_dist*vtx1_dist - 2*vtx0_dist*vtx1_dist*cos(fabs(dphi_uniformphi)));
      h_svdist2d_uniformphi->Fill(svdist_uniformphi, w * (0.5 * TMath::Erf((svdist_uniformphi - muclear)/sigmaclear) + 0.5));

      for (int j = 0; j < 5; ++j) {
        h_svdist2d_mu[j]->Fill(svdist, w * (0.5 * TMath::Erf((svdist - mu_clear[j]/10000)/sigmaclear) + 0.5));
        h_svdist2d_sigma[j]->Fill(svdist, w * (0.5 * TMath::Erf((svdist - muclear)/(sigma_clear[j]/10000)) + 0.5));
      }
    }
  }

  TH1D* h_sigma = new TH1D("h_sigma", ";#sigma(sv #0, #1) (cm);arb. units", 10, 0, 0.01);
  TH1D* h_sig = new TH1D("h_sig", ";N#sigma(sv #0, #1);arb. units", 15, 0, 30);
  TH1D* h_svdist2d_lt4sigma = new TH1D("h_svdist2d_lt4sigma", "<  4 #sigma;dist2d(sv #0, #1) (cm);arb. units", 10, 0, 0.1);
  TH1D* h_sig_gtnsigma[7];
  TH1D* h_svdist2d_gtnsigma[7];
  for (int i = 0; i < 7; ++i) {
    h_sig_gtnsigma[i] = new TH1D(TString::Format("h_sig_gt%isigma", 2*(i+2)), TString::Format(">= %i sigma;N#sigma(sv #0, #1) (cm);arb. units", 2*(i+2)), 15, 0, 30);
    h_svdist2d_gtnsigma[i] = new TH1D(TString::Format("h_svdist2d_gt%isigma", 2*(i+2)), TString::Format(">= %i sigma;dist2d(sv #0, #1) (cm);arb. units", 2*(i+2)), 10, 0, 0.1);
  }
  TH1D* h_dvv_vtx_low = new TH1D("h_dvv_vtx_low", "njets <= 6;d_{vv} (cm);arb. units", 10, 0, 0.1);
  TH1D* h_dvv_vtx_high = new TH1D("h_dvv_vtx_high", "njets >= 7;d_{vv} (cm);arb. units", 10, 0, 0.1);

  for (int i = 0; i < n1v; ++i) {
    for (int j = i+1; j < n1v; ++j) {
      float svdist2d = sqrt((x[i] - x[j]) * (x[i] - x[j]) + (y[i] - y[j]) * (y[i] - y[j]));
      float dx = (x[i] - x[j]) / svdist2d;
      float dy = (y[i] - y[j]) / svdist2d;
      float sigma = sqrt((cxx[i] + cxx[j])*dx*dx + (cyy[i] + cyy[j])*dy*dy + 2*(cxy[i] + cxy[j])*dx*dy);
      h_sigma->Fill(sigma);
      h_sig->Fill(svdist2d / sigma);
      if (svdist2d / sigma < 4) {
        h_svdist2d_lt4sigma->Fill(svdist2d);
      }
      for (int k = 0; k < 7; ++k) {
        if (svdist2d / sigma > 2*(k+2)) {
          h_sig_gtnsigma[k]->Fill(svdist2d / sigma);
          h_svdist2d_gtnsigma[k]->Fill(svdist2d);

          if (2*(k+2) == 10) {
            if (njets[i] <= 6 && njets[j] <= 6) h_dvv_vtx_low->Fill(svdist2d);
            if (njets[i] >= 7 && njets[j] >= 7) h_dvv_vtx_high->Fill(svdist2d);
          }
        }
      }
    }
  }

  TFile* fh = TFile::Open("2v_from_jets.root", "recreate");
  h_bs2ddist1v->Write();
  h_vtxjetdphi->Write();
  h_vtx0jetdphi->Write();
  h_vtx1jetdphi->Write();
  h_svdist2d->Write();
  h_absdeltaphi01->Write();
  h_sigmavv->Write();
  h_sigvv->Write();
  h_sigmavv_dvv->Write();

  h_njets->Write();
  h_jet_sum_ht->Write();
  h_jetphi->Write();
  h_jetpairdphi->Write();

  h_sv0phi->Write();
  h_sv1phi->Write();
  h_svjetdphi->Write();
  h_sv0jetdphi->Write();
  h_sv1jetdphi->Write();
  h_svpairdphi->Write();
  h_svpairdphi_cut->Write();
  h_svpairabsdphi->Write();

  h_sv0bs2ddist->Write();
  h_sv1bs2ddist->Write();
  h_svpairdist->Write();
  h_svpairdist_cut->Write();

  h_sigma->Write();
  h_svdist2d_lt4sigma->Write();

  //overlay vertex-jet deltaphi for one-vertex and two-vertex events
  TCanvas* c_vtxjetdphi = new TCanvas("c_vtxjetdphi");
  h_svjetdphi->SetName("one-vertex");
  h_svjetdphi->SetLineColor(kBlue);
  h_svjetdphi->DrawNormalized();
  h_vtxjetdphi->SetName("two-vertex");
  h_vtxjetdphi->SetLineColor(kRed);
  h_vtxjetdphi->DrawNormalized("sames");
  h_vtx0jetdphi->SetName("two-vertex0");
  h_vtx0jetdphi->SetLineColor(kGreen);
  h_vtx0jetdphi->DrawNormalized("sames");
  h_vtx1jetdphi->SetName("two-vertex1");
  h_vtx1jetdphi->SetLineColor(kMagenta);
  h_vtx1jetdphi->DrawNormalized("sames");
  c_vtxjetdphi->SetTickx();
  c_vtxjetdphi->SetTicky();
  c_vtxjetdphi->Write();

  //overlay vertex-jet deltaphi for actual MC and our model
  TCanvas* c_svjetdphi = new TCanvas("c_svjetdphi", "c_svjetdphi", 700, 700);
  h_svjetdphi->SetLineColor(kBlue);
  h_svjetdphi->SetLineWidth(3);
  h_svjetdphi->SetStats(0);
  h_svjetdphi->Draw();
  h_sv0jetdphi->SetLineColor(kRed);
  h_sv0jetdphi->SetLineWidth(3);
  h_sv0jetdphi->SetStats(0);
  h_sv0jetdphi->Draw("sames");
  TLegend* l_svjetdphi = new TLegend(0.75, 0.9, 1, 1);
  l_svjetdphi->AddEntry(h_svjetdphi, "actual MC", "LPE");
  l_svjetdphi->AddEntry(h_sv0jetdphi, "our model", "LPE");
  l_svjetdphi->SetFillColor(0);
  l_svjetdphi->Draw();
  c_svjetdphi->SetTickx();
  c_svjetdphi->SetTicky();
  c_svjetdphi->Write();

  //overlay svdist2d for MC background, our model, and MC signal
  TCanvas* c_svdist2d_sig = new TCanvas("c_svdist2d_sig", "c_svdist2d_sig", 700, 700);
  h_svdist2d->SetLineColor(kBlue);
  h_svdist2d->SetLineWidth(3);
  h_svdist2d->SetStats(0);
  h_svdist2d->DrawNormalized();
  h_svpairdist_cut->SetLineColor(kRed);
  h_svpairdist_cut->SetLineWidth(3);
  h_svpairdist_cut->SetStats(0);
  h_svpairdist_cut->DrawNormalized("sames");

  TFile* sig_file = TFile::Open("/uscms/home/tucker/crab_dirs/HistosV20/mfv_neutralino_tau1000um_M0400.root");
  TH1F* h_svdist2d_sig = (TH1F*)sig_file->Get("mfvVertexHistosWAnaCuts/h_svdist2d");
  h_svdist2d_sig->Rebin(5);
  h_svdist2d_sig->SetLineColor(8);
  h_svdist2d_sig->SetLineWidth(3);
  h_svdist2d_sig->SetStats(0);
  h_svdist2d_sig->DrawNormalized("sames");

  TLegend* l_svdist2d_sig = new TLegend(0.25, 0.7, 0.85, 0.85);
  l_svdist2d_sig->AddEntry(h_svdist2d, "actual MC", "LPE");
  l_svdist2d_sig->AddEntry(h_svpairdist_cut, "our model", "LPE");
  l_svdist2d_sig->AddEntry(h_svdist2d_sig, "#tau = 1 mm, M = 400 GeV signal", "LPE");
  l_svdist2d_sig->SetFillColor(0);
  l_svdist2d_sig->Draw();
  c_svdist2d_sig->SetTickx();
  c_svdist2d_sig->SetTicky();
  fh->cd();
  c_svdist2d_sig->Write();
  sig_file->Close();

  //overlay svdist2d for MC background and our model
  TCanvas* c_svdist2d = new TCanvas("c_svdist2d", "c_svdist2d", 700, 700);
  h_svdist2d->GetXaxis()->SetRangeUser(0,0.1);
  h_svdist2d->SetLineColor(kBlue);
  h_svdist2d->SetLineWidth(3);
  h_svdist2d->SetStats(1);
  h_svdist2d->DrawNormalized();
  h_svpairdist_cut->SetLineColor(kRed);
  h_svpairdist_cut->SetLineWidth(3);
  h_svpairdist_cut->SetStats(1);
  h_svpairdist_cut->DrawNormalized("sames");
  c_svdist2d->SetTickx();
  c_svdist2d->SetTicky();
  c_svdist2d->Write();

  //overlay vertex-vertex deltaphi for actual MC and our model
  TCanvas* c_svpairdphi = new TCanvas("c_svpairdphi", "c_svpairdphi", 700, 700);
  h_absdeltaphi01->SetLineColor(kBlue);
  h_absdeltaphi01->SetLineWidth(3);
  h_absdeltaphi01->SetStats(0);
  h_absdeltaphi01->DrawNormalized();
  h_svpairabsdphi->SetLineColor(kRed);
  h_svpairabsdphi->SetLineWidth(3);
  h_svpairabsdphi->SetStats(0);
  h_svpairabsdphi->DrawNormalized("sames");
  TLegend* l_deltaphi = new TLegend(0.25, 0.7, 0.7, 0.85);
  l_deltaphi->AddEntry(h_absdeltaphi01, "actual MC", "LPE");
  l_deltaphi->AddEntry(h_svpairabsdphi, "our model", "LPE");
  l_deltaphi->SetFillColor(0);
  l_deltaphi->Draw();
  c_svpairdphi->SetTickx();
  c_svpairdphi->SetTicky();
  c_svpairdphi->Write();

  //overlay svdist2d for actual MC and our model with gaussian phi, uniform phi
  TCanvas* c_svdist2d_phi = new TCanvas("c_svdist2d_phi", "c_svdist2d_phi", 700, 700);
  h_svdist2d->GetXaxis()->SetRangeUser(0, 0.1);
  h_svdist2d->SetLineColor(kBlue);
  h_svdist2d->SetLineWidth(3);
  h_svdist2d->SetStats(0);
  h_svdist2d->DrawNormalized();
  h_svpairdist_cut->SetLineColor(kRed);
  h_svpairdist_cut->SetLineWidth(3);
  h_svpairdist_cut->SetStats(0);
  h_svpairdist_cut->DrawNormalized("sames");
  h_svdist2d_uniformphi->SetLineColor(8);
  h_svdist2d_uniformphi->SetLineWidth(3);
  h_svdist2d_uniformphi->SetStats(0);
  h_svdist2d_uniformphi->DrawNormalized("sames");

  TLegend* l_svdist2d_phi = new TLegend(0.5, 0.7, 0.85, 0.85);
  l_svdist2d_phi->AddEntry(h_svdist2d, "actual MC", "LPE");
  l_svdist2d_phi->AddEntry(h_svpairdist_cut, "our model, Gaussian phi", "LPE");
  l_svdist2d_phi->AddEntry(h_svdist2d_uniformphi, "our model, uniform phi", "LPE");
  l_svdist2d_phi->SetFillColor(0);
  l_svdist2d_phi->Draw();
  c_svdist2d_phi->SetTickx();
  c_svdist2d_phi->SetTicky();
  c_svdist2d_phi->Write();

  //overlay svdist2d for actual MC and our model with mu_clear = {260, 270, 280, 290, 300} mum
  TCanvas* c_svdist2d_mu = new TCanvas("c_svdist2d_mu", "c_svdist2d_mu", 700, 700);
  h_svdist2d->GetXaxis()->SetRangeUser(0, 0.1);
  h_svdist2d->SetLineColor(kBlue);
  h_svdist2d->SetLineWidth(3);
  h_svdist2d->SetStats(0);
  h_svdist2d->DrawNormalized();
  for (int i = 0; i < 5; ++i) {
    h_svdist2d_mu[i]->SetLineColor(kRed+i);
    h_svdist2d_mu[i]->SetLineWidth(2);
    h_svdist2d_mu[i]->SetStats(0);
    h_svdist2d_mu[i]->DrawNormalized("sames");
  }

  TLegend* l_svdist2d_mu = new TLegend(0.5, 0.7, 0.85, 0.85);
  l_svdist2d_mu->AddEntry(h_svdist2d, "actual MC", "LPE");
  for (int i = 0; i < 5; ++i) {
    l_svdist2d_mu->AddEntry(h_svdist2d_mu[i], TString::Format("#mu_{clear} = %i #mum", int(mu_clear[i])), "LPE");
  }
  l_svdist2d_mu->SetFillColor(0);
  l_svdist2d_mu->Draw();
  c_svdist2d_mu->SetTickx();
  c_svdist2d_mu->SetTicky();
  c_svdist2d_mu->Write();

  //overlay svdist2d for actual MC and our model with sigma_clear = {30, 40, 50, 60, 70} mum
  TCanvas* c_svdist2d_sigma = new TCanvas("c_svdist2d_sigma", "c_svdist2d_sigma", 700, 700);
  h_svdist2d->GetXaxis()->SetRangeUser(0, 0.1);
  h_svdist2d->SetLineColor(kBlue);
  h_svdist2d->SetLineWidth(3);
  h_svdist2d->SetStats(0);
  h_svdist2d->DrawNormalized();
  for (int i = 0; i < 5; ++i) {
    h_svdist2d_sigma[i]->SetLineColor(kRed+i);
    h_svdist2d_sigma[i]->SetLineWidth(2);
    h_svdist2d_sigma[i]->SetStats(0);
    h_svdist2d_sigma[i]->DrawNormalized("sames");
  }

  TLegend* l_svdist2d_sigma = new TLegend(0.5, 0.7, 0.85, 0.85);
  l_svdist2d_sigma->AddEntry(h_svdist2d, "actual MC", "LPE");
  for (int i = 0; i < 5; ++i) {
    l_svdist2d_sigma->AddEntry(h_svdist2d_sigma[i], TString::Format("#sigma_{clear} = %i #mum", int(sigma_clear[i])), "LPE");
  }
  l_svdist2d_sigma->SetFillColor(0);
  l_svdist2d_sigma->Draw();
  c_svdist2d_sigma->SetTickx();
  c_svdist2d_sigma->SetTicky();
  c_svdist2d_sigma->Write();

  //overlay sigma for two-vertex MC and all one-vertex pairs
  TCanvas* c_sigma = new TCanvas("c_sigma", "c_sigma", 700, 700);
  h_sigmavv->SetLineColor(kBlue);
  h_sigmavv->SetLineWidth(3);
  h_sigmavv->DrawNormalized();
  h_sigma->SetLineColor(kRed);
  h_sigma->SetLineWidth(3);
  h_sigma->DrawNormalized("sames");
  c_sigma->SetTickx();
  c_sigma->SetTicky();
  c_sigma->Write();

  //overlay significance for two-vertex MC and all one-vertex pairs
  TCanvas* c_sig = new TCanvas("c_sig", "c_sig", 700, 700);
  h_sigvv->SetLineColor(kBlue);
  h_sigvv->SetLineWidth(3);
  h_sigvv->DrawNormalized();
  h_sig->SetLineColor(kRed);
  h_sig->SetLineWidth(3);
  h_sig->DrawNormalized("sames");
  c_sig->SetTickx();
  c_sig->SetTicky();
  c_sig->Write();

  //overlay significance for MC background and vertex pairs > n sigma apart
  TCanvas* c_sig_gtnsigma = new TCanvas("c_sig_gtnsigma", "c_sig_gtnsigma", 700, 700);
  h_sigvv->SetStats(0);
  h_sigvv->DrawNormalized();
  int colors[7] = {kRed, kOrange, kYellow, kGreen, kCyan, kBlue, kViolet};
  for (int i = 0; i < 7; ++i) {
    h_sig_gtnsigma[i]->SetLineColor(colors[i]);
    h_sig_gtnsigma[i]->SetLineWidth(2);
    h_sig_gtnsigma[i]->SetStats(0);
    h_sig_gtnsigma[i]->DrawNormalized("sames");
  }
  TLegend* l_sig_gtnsigma = new TLegend(0.6, 0.6, 0.95, 0.95);
  l_sig_gtnsigma->AddEntry(h_sigvv, "actual MC", "LPE");
  for (int i = 0; i < 7; ++i) {
    l_sig_gtnsigma->AddEntry(h_sig_gtnsigma[i], TString::Format("d_{vv} > %i #sigma_{vv}", 2*(i+2)), "LPE");
  }
  l_sig_gtnsigma->SetFillColor(0);
  l_sig_gtnsigma->Draw();
  c_sig_gtnsigma->SetTickx();
  c_sig_gtnsigma->SetTicky();
  c_sig_gtnsigma->Write();

  //overlay svdist2d for MC background and vertex pairs > 4 sigma apart
  TCanvas* c_svdist2d_gt4sigma = new TCanvas("c_svdist2d_gt4sigma", "c_svdist2d_gt4sigma", 700, 700);
  h_svdist2d->SetStats(1);
  h_svdist2d->DrawNormalized();
  h_svdist2d_gtnsigma[0]->SetLineColor(kRed);
  h_svdist2d_gtnsigma[0]->SetLineWidth(3);
  h_svdist2d_gtnsigma[0]->DrawNormalized("sames");
  c_svdist2d_gt4sigma->SetTickx();
  c_svdist2d_gt4sigma->SetTicky();
  c_svdist2d_gt4sigma->Write();

  //overlay svdist2d for MC background and vertex pairs > n sigma apart
  TCanvas* c_svdist2d_gtnsigma = new TCanvas("c_svdist2d_gtnsigma", "c_svdist2d_gtnsigma", 700, 700);
  h_svdist2d->SetStats(0);
  h_svdist2d->DrawNormalized();
  for (int i = 0; i < 7; ++i) {
    h_svdist2d_gtnsigma[i]->SetLineColor(colors[i]);
    h_svdist2d_gtnsigma[i]->SetLineWidth(2);
    h_svdist2d_gtnsigma[i]->SetStats(0);
    h_svdist2d_gtnsigma[i]->DrawNormalized("sames");
  }
  TLegend* l_svdist2d_gtnsigma = new TLegend(0.5, 0.5, 0.85, 0.85);
  l_svdist2d_gtnsigma->AddEntry(h_svdist2d, "actual MC", "LPE");
  for (int i = 0; i < 7; ++i) {
    l_svdist2d_gtnsigma->AddEntry(h_svdist2d_gtnsigma[i], TString::Format("d_{vv} > %i #sigma_{vv}", 2*(i+2)), "LPE");
  }
  l_svdist2d_gtnsigma->SetFillColor(0);
  l_svdist2d_gtnsigma->Draw();
  c_svdist2d_gtnsigma->SetTickx();
  c_svdist2d_gtnsigma->SetTicky();
  c_svdist2d_gtnsigma->Write();

  //overlay svdist2d for two-vertex MC, cleared jets, simple clearing
  TCanvas* c_dvv = new TCanvas("c_dvv", "c_dvv", 700, 700);
  h_svdist2d->DrawNormalized();
  h_svpairdist_cut->DrawNormalized("sames");
  h_svdist2d_gtnsigma[3]->SetLineColor(8);
  h_svdist2d_gtnsigma[3]->SetLineWidth(3);
  h_svdist2d_gtnsigma[3]->DrawNormalized("sames");
  TLegend* l_dvv = new TLegend(0.4, 0.7, 0.9, 0.85);
  l_dvv->AddEntry(h_svdist2d, "two-vertex MC");
  l_dvv->AddEntry(h_svpairdist_cut, "cleared jets w/ #mu = 280 #mum, #sigma = 50 #mum");
  l_dvv->AddEntry(h_svdist2d_gtnsigma[3], "simple clearing w/ d_{vv} > 10 #sigma_{vv}");
  l_dvv->SetFillColor(0);
  l_dvv->Draw();
  c_dvv->SetTickx();
  c_dvv->SetTicky();
  c_dvv->Write();

  //overlay low-njets svdist2d for two-vertex MC, cleared jets, simple clearing
  TCanvas* c_dvv_low_njets = new TCanvas("c_dvv_low_njets", "c_dvv_low_njets", 700, 700);
  h_dvv_low_njets->SetLineColor(kBlue);
  h_dvv_low_njets->SetLineWidth(3);
  h_dvv_low_njets->SetStats(0);
  h_dvv_low_njets->DrawNormalized();
  h_dvv_jets_low->SetLineColor(kRed);
  h_dvv_jets_low->SetLineWidth(3);
  h_dvv_jets_low->SetStats(0);
  h_dvv_jets_low->DrawNormalized("sames");
  h_dvv_vtx_low->SetLineColor(kGreen);
  h_dvv_vtx_low->SetLineWidth(3);
  h_dvv_vtx_low->SetStats(0);
  h_dvv_vtx_low->DrawNormalized("sames");
  TLegend* l_dvv_low_njets = new TLegend(0.5, 0.7, 0.85, 0.85);
  l_dvv_low_njets->AddEntry(h_dvv_low_njets, "two-vertex MC");
  l_dvv_low_njets->AddEntry(h_dvv_jets_low, "cleared jets w/ #mu = 280 #mum, #sigma = 50 #mum");
  l_dvv_low_njets->AddEntry(h_dvv_vtx_low, "simple clearing w/ d_{vv} > 10 #sigma_{vv}");
  l_dvv_low_njets->SetFillColor(0);
  l_dvv_low_njets->Draw();
  c_dvv_low_njets->SetTickx();
  c_dvv_low_njets->SetTicky();
  c_dvv_low_njets->Write();

  //overlay high-njets svdist2d for two-vertex MC, cleared jets, simple clearing
  TCanvas* c_dvv_high_njets = new TCanvas("c_dvv_high_njets", "c_dvv_high_njets", 700, 700);
  h_dvv_high_njets->SetLineColor(kBlue);
  h_dvv_high_njets->SetLineWidth(3);
  h_dvv_high_njets->SetStats(0);
  h_dvv_high_njets->DrawNormalized();
  h_dvv_jets_high->SetLineColor(kRed);
  h_dvv_jets_high->SetLineWidth(3);
  h_dvv_jets_high->SetStats(0);
  h_dvv_jets_high->DrawNormalized("sames");
  h_dvv_vtx_high->SetLineColor(kGreen);
  h_dvv_vtx_high->SetLineWidth(3);
  h_dvv_vtx_high->SetStats(0);
  h_dvv_vtx_high->DrawNormalized("sames");
  TLegend* l_dvv_high_njets = new TLegend(0.5, 0.7, 0.85, 0.85);
  l_dvv_high_njets->AddEntry(h_dvv_high_njets, "two-vertex MC");
  l_dvv_high_njets->AddEntry(h_dvv_jets_high, "cleared jets w/ #mu = 280 #mum, #sigma = 50 #mum");
  l_dvv_high_njets->AddEntry(h_dvv_vtx_high, "simple clearing w/ d_{vv} > 10 #sigma_{vv}");
  l_dvv_high_njets->SetFillColor(0);
  l_dvv_high_njets->Draw();
  c_dvv_high_njets->SetTickx();
  c_dvv_high_njets->SetTicky();
  c_dvv_high_njets->Write();

  h_dvv_low_njets->Write();
  h_dvv_jets_low->Write();
  h_dvv_vtx_low->Write();
  h_dvv_high_njets->Write();
  h_dvv_jets_high->Write();
  h_dvv_vtx_high->Write();

  h_dvv->Write();
  h_dvvc->Write();
  //overlay dvv with binning
  TCanvas* c_dvvc = new TCanvas("c_dvvc", "c_dvvc", 700, 700);
  h_dvv->SetLineColor(kBlue);
  h_dvv->SetLineWidth(3);
  h_dvv->DrawNormalized();
  h_dvvc->SetLineColor(kRed);
  h_dvvc->SetLineWidth(3);
  h_dvvc->DrawNormalized("sames");
  c_dvvc->Write();

  double sum_dvv = h_dvv->Integral();
  double sum_dvvc = h_dvvc->Integral();
  TH1D* h_diff = hist_with_binning("h_diff", ";d_{VV}^{ C} - d_{VV};arb. units");
  for (int i = 1; i <= h_dvv->GetNbinsX(); ++i) {
    double dvvc = h_dvvc->GetBinContent(i);
    double dvv = h_dvv->GetBinContent(i);
    h_diff->SetBinContent(i, dvvc / sum_dvvc - dvv / sum_dvv);
    h_diff->SetBinError(i, sqrt(dvv)/sum_dvv);
  }
  h_diff->Write();

  fh->Close();

  h_dvv->Scale(1./h_dvv->Integral());
  h_dvvc->Scale(1./h_dvvc->Integral());
  double chi2 = 0;
  for (int i = 1; i <= h_dvv->GetNbinsX(); ++i) {
    double dvvc = h_dvvc->GetBinContent(i);
    double dvv = h_dvv->GetBinContent(i);
    if (dvv > 0) {
      chi2 += (dvvc - dvv) * (dvvc - dvv) / dvv;
    }
  }
  printf("muclear = %f, sigmaclear = %f, chi2 = %f\n", muclear, sigmaclear, chi2);
}
