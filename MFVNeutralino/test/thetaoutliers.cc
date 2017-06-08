// make zclustertest.exe && ./zclustertest.exe
// $fxrd/store/user/tucker/mfv_neu_tau01000um_M0800/crab_MinitreeV9_wtk_mfv_mfv_neu_tau01000um_M0800/161209_191028/0000/minitree_1.root mfv1mm.root $ZZZ_SZ && ./clustertrackstest.exe $crd/MinitreeV9_ntk5/qcdht2000ext.root qcdht2000ext.root $ZZZ_SZ && comparehists.py qcdht2000ext.root mfv1mm.root / $asdf/plots/clustertracks --nice qcdht2000ext mfv1mm --scaling '-{"qcdht2000ext": 25400*36/4016332., "mfv1mm": 36/10000.}[curr]'

#include <iostream>
#include "TCanvas.h"
#include "TFile.h"
#include "TH2.h"
#include "TTree.h"
#include "TVector2.h"
#include "JMTucker/MFVNeutralino/interface/MiniNtuple.h"

bool genmatch_only = false;
TH1F* h_val = 0;

struct stats {
  // ith value of these are the corresponding stat with the ith value
  // of the n-length input removed, value n is the stat with no input
  // values removed
  std::vector<double> min; 
  std::vector<double> max;
  std::vector<double> med;
  std::vector<double> avg;
  std::vector<double> rms;
  std::vector<double> mad;

  void calc(std::vector<double> v,
            double& min, double& max, double& med, double& avg, double& rms, double& mad) {
    std::sort(v.begin(), v.end());
    const size_t m = v.size();
    min = v.front();
    max = v.back();
    if (m % 2 == 0)
      med = (v[m/2] + v[m/2-1])/2;
    else
      med = v[m/2];

    avg = rms = 0;
    std::vector<double> v2(v.size());
    for (size_t i = 0; i < m; ++i) {
      avg += v[i];
      v2[i] = fabs(v[i] - med);
    }
    avg /= m;
    std::sort(v2.begin(), v2.end());
    if (m % 2 == 0)
      mad = (v2[m/2] + v2[m/2-1])/2;
    else
      mad = v2[m/2];

    for (auto a : v)
      rms += pow(a - avg, 2);
    rms = sqrt(rms/m); //m-1
  }

  stats(const std::vector<double>& v) {
    const size_t n = v.size();
    min.assign(n+1, 0);
    max.assign(n+1, 0);
    med.assign(n+1, 0);
    avg.assign(n+1, 0);
    rms.assign(n+1, 0);
    mad.assign(n+1, 0);

    calc(v, min[n], max[n], med[n], avg[n], rms[n], mad[n]);

    for (size_t i = 0; i < n; ++i) {
      std::vector<double> v2(v);
      v2.erase(v2.begin()+i);
      calc(v2, min[i], max[i], med[i], avg[i], rms[i], mad[i]);
    }
  }
};

bool analyze(long long j, long long je, const mfv::MiniNtuple& nt) {
  const bool prints = false;

  if (prints) std::cout << "Entry " << j << "\n";

  for (int ivtx = 0, ivtxe = std::min(int(nt.nvtx), 2); ivtx < ivtxe; ++ivtx) {
    int ntracks = 0;
    bool genmatch = false;
    const std::vector<double>* tk_vz = 0;
    const std::vector<double>* tk_px = 0;
    const std::vector<double>* tk_py = 0;
    const std::vector<double>* tk_pz = 0;

    if (ivtx == 0) {
      ntracks = nt.ntk0;
      genmatch = nt.genmatch0;
      tk_vz = nt.p_tk0_vz;
      tk_px = nt.p_tk0_px;
      tk_py = nt.p_tk0_py;
      tk_pz = nt.p_tk0_pz;
    }
    else {
      ntracks = nt.ntk1;
      genmatch = nt.genmatch1;
      tk_vz = nt.p_tk1_vz;
      tk_px = nt.p_tk1_px;
      tk_py = nt.p_tk1_py;
      tk_pz = nt.p_tk1_pz;
    }

    if (genmatch_only && !genmatch)
      continue;

    std::vector<double> thetas(ntracks);

    for (int itk = 0; itk < ntracks; ++itk) {
      const double px = (*tk_px)[itk];
      const double py = (*tk_py)[itk];
      const double pz = (*tk_pz)[itk];
      const double pt = sqrt(px*px + py*py);
      thetas[itk] = TVector2::Phi_mpi_pi(atan2(pt, pz));
    }

    stats s(thetas);
    double mx = 0;

    for (int itk = 0; itk < ntracks; ++itk) {
      const double var = fabs(thetas[itk] - s.med[itk]) / s.mad[itk];
      if (var > mx) mx = var;
    }

    h_val->Fill(mx);
  }

  return true;
}

int main(int argc, char** argv) {
  if (argc == 1) {
    std::vector<double> xx = {2.8703831, 2.8554926, 2.8583482, 0.6880658, 2.8493017};
    stats s_xx(xx);
    for (int i = 0; i < 5; ++i) {
      const double dth = fabs(xx[i] - s_xx.med[i]);
      const double dthospread = dth / s_xx.mad[i];
      printf("i %i dth %f outl %f\n", i, dth, dthospread);
    }
    return 1;
  }

  if (argc < 3) {
    fprintf(stderr, "usage: thetaoutliers.exe in_fn out_fn [genmatch]\n");
    return 1;
  }

  const char* fn = argv[1];
  const char* out_fn = argv[2];
  if (argc > 3)
    genmatch_only = strcmp(argv[3], "genmatch") == 0;
  printf("%s -> %s genmatch? %i\n", fn, out_fn, genmatch_only);

  TFile out_f(out_fn, "recreate");

  TH1::SetDefaultSumw2();

  const int nbins = 20000;
  const double vmax = 10000;
  h_val = new TH1F("h_val", ";max (trk_{i} theta - <trk theta>)/(spread trk theta);events/0.1", nbins, 0, vmax);

  mfv::loop(fn, "mfvMiniTree/t", analyze);

  out_f.cd();

  TH1F* h_cumu = (TH1F*)h_val->Clone("h_cumu");
  double integ = h_val->Integral(0,nbins+1);
  const int ntgts = 5;
  double vs[ntgts] = {-1,-1,-1,-1,-1};
  double tgt[ntgts] = {0.5, 0.8, 0.95, 0.99, 0.999};
  for (int ibin = 1; ibin <= nbins; ++ibin) {
    const double m1c  = h_cumu->GetBinContent(ibin-1);
    const double m1ce = h_cumu->GetBinError  (ibin-1);
    const double c  = h_cumu->GetBinContent(ibin);
    const double ce = h_cumu->GetBinError  (ibin);
    double cumu = m1c + c;
    h_cumu->SetBinContent(ibin, cumu);
    h_cumu->SetBinError  (ibin, sqrt(m1ce*m1ce + ce*ce));
    for (int i = 0; i < ntgts; ++i)
      if (vs[i] < 0 && cumu >= tgt[i] * integ)
        vs[i] = h_val->GetXaxis()->GetBinLowEdge(ibin);
  }

  for (int i = 0; i < ntgts; ++i) {
    TH1F* h = new TH1F(TString::Format("h_%04i", int(tgt[i]*10000)), "", nbins, 0, vmax);
    h->Fill(vs[i]);
  }

  out_f.Write();
  out_f.Close();
}
