// make zclustertest.exe && ./zclustertest.exe
// $fxrd/store/user/tucker/mfv_neu_tau01000um_M0800/crab_MinitreeV9_wtk_mfv_mfv_neu_tau01000um_M0800/161209_191028/0000/minitree_1.root mfv1mm.root $ZZZ_SZ && ./clustertrackstest.exe $crd/MinitreeV9_ntk5/qcdht2000ext.root qcdht2000ext.root $ZZZ_SZ && comparehists.py qcdht2000ext.root mfv1mm.root / $asdf/plots/clustertracks --nice qcdht2000ext mfv1mm --scaling '-{"qcdht2000ext": 25400*36/4016332., "mfv1mm": 36/10000.}[curr]'

#include <iostream>
#include "TCanvas.h"
#include "TFile.h"
#include "TH1.h"
#include "TTree.h"
#include "TVector2.h"
#include "JMTucker/MFVNeutralino/interface/MiniNtuple.h"

TH1F* h_deltaz = 0;
TH1F* h_deltazorms = 0;
TH1F* h_deltatheta = 0;
TH1F* h_deltathetaorms = 0;

bool analyze(long long j, long long je, const mfv::MiniNtuple& nt) {
  const bool prints = false;

  if (prints) std::cout << "Entry " << j << "\n";

  for (int ivtx = 0, ivtxe = std::min(int(nt.nvtx), 2); ivtx < ivtxe; ++ivtx) {
    int ntracks = 0;
    const std::vector<double>* tk_vz = 0;
    const std::vector<double>* tk_px = 0;
    const std::vector<double>* tk_py = 0;
    const std::vector<double>* tk_pz = 0;

    if (ivtx == 0) {
      ntracks = nt.ntk0;
      tk_vz = nt.p_tk0_vz;
      tk_px = nt.p_tk0_px;
      tk_py = nt.p_tk0_py;
      tk_pz = nt.p_tk0_pz;
    }
    else {
      ntracks = nt.ntk1;
      tk_vz = nt.p_tk1_vz;
      tk_px = nt.p_tk1_px;
      tk_py = nt.p_tk1_py;
      tk_pz = nt.p_tk1_pz;
    }

    double zmean = 0;
    double zrms = 0;
    double thetamean = 0;
    double thetarms = 0;
    std::vector<double> theta(ntracks, 0);
    for (int itk = 0; itk < ntracks; ++itk) {
      const double z = (*tk_vz)[itk];
      const double px = (*tk_px)[itk];
      const double py = (*tk_py)[itk];
      const double pz = (*tk_pz)[itk];
      const double pt = sqrt(px*px + py*py);
      theta[itk] = TVector2::Phi_mpi_pi(atan2(pt, pz));

      zmean += z;
      thetamean += theta[itk];
    }
    zmean /= ntracks;
    thetamean /= ntracks;

    for (int itk = 0; itk < ntracks; ++itk) {
      const double z = (*tk_vz)[itk];
      const double th = theta[itk];
      const double dz  = z - zmean;
      const double dth = th - thetamean;

      zrms += dz*dz;
      thetarms += dth*dth;

      h_deltaz->Fill(fabs(dz));
      h_deltatheta->Fill(fabs(dth));
    }
    zrms     = sqrt(zrms/(ntracks - 1));
    thetarms = sqrt(thetarms/(ntracks - 1));

    for (int itk = 0; itk < ntracks; ++itk) {
      const double z = (*tk_vz)[itk];
      const double th = theta[itk];
      const double dz  = z - zmean;
      const double dth = th - thetamean;

      h_deltazorms->Fill(fabs(dz)/zrms);
      h_deltathetaorms->Fill(fabs(dth)/thetarms);
    }
  }

  return true;
}

int main(int argc, char** argv) {
  assert(argc > 2);

  const char* fn = argv[1];
  const char* out_fn = argv[2];

  TFile out_f(out_fn, "recreate");

  h_deltaz     = new TH1F("h_deltaz",     ";trk_{i} vz - mean trk vz (cm);events/0.1 cm", 1000, 0, 10);
  h_deltazorms = new TH1F("h_deltazorms", ";(trk_{i} vz - mean trk vz)/(rms trk vz);events/0.1", 1000, 0, 10);
  h_deltatheta = new TH1F("h_deltatheta", ";trk_{i} theta - mean trk theta (rad);events/0.063", 1000, 0, 6.3);
  h_deltathetaorms = new TH1F("h_deltathetaorms", ";(trk_{i} theta - mean trk theta)/(rms trk theta);events/0.1", 1000, 0, 10);

  mfv::loop(fn, "mfvMiniTree/t", analyze);

  out_f.Write();
  out_f.Close();
}
