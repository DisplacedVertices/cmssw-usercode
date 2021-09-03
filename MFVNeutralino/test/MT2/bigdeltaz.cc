#include "TH2.h"
#include "DVCode/MFVNeutralino/interface/Ntuple.h"
#include "DVCode/Tools/interface/ExtValue.h"
#include "DVCode/Tools/interface/NtupleReader.h"
#include "DVCode/Tools/interface/StatCalculator.h"

typedef std::vector<std::pair<int, int>> top_t; 
top_t top_n(const std::map<int,int>& x, size_t n) {
  top_t top(n);
  std::partial_sort_copy(x.begin(), x.end(), top.begin(), top.end(), [](const auto& l, const auto& r) { return l.second > r.second; });
  return top;
}

int main(int argc, char** argv) {
  jmt::NtupleReader<mfv::MiniNtuple2> nr;
  nr.init_options("mfvMiniTree2/t", "MiniHistsV25m_bigdeltaz", "nr_minintuplev25mv1", "ttbar=False, data=False");
  if (!nr.parse_options(argc, argv) || !nr.init()) return 1;
  auto& nt = nr.nt();
  auto& pvs = nt.pvs();
  auto& tks = nt.tracks();
  auto& vs = nt.vertices();

  ////

  auto h_maxpvcount_mindeltaz = new TH2D("h_maxpvcount_mindeltaz", "", 30, 0, 30, 30, 0, 30);
  auto h_maxpvcount_minmissd = new TH2D("h_maxpvcount_minmissd", "", 30, 0, 30, 30, 0, 30);

  auto h_deltamaxpvcount_mindeltaz = new TH1D("h_deltamaxpvcount_mindeltaz", "", 30, 0, 30);
  auto h_deltamaxpvcount_minmissd = new TH1D("h_deltamaxpvcount_minmissd", "", 30, 0, 30);

  auto h_dz = new TH1D("h_dz", "", 100, 0, 20);
  auto h_dphi = new TH1D("h_dphi", "", 100, -M_PI, M_PI);
  auto h_dz_v_dphi = new TH2D("h_dz_v_dphi", "", 100, 0, M_PI, 100, 0, 20);

  auto h_maxdz = new TH1D("h_maxdz", "", 100, 0, 20);
  auto h_maxdphi = new TH1D("h_maxdphi", "", 100, 0, M_PI);
  auto h_maxdz_v_maxdphi = new TH2D("h_maxdz_v_maxdphi", "", 100, 0, M_PI, 100, 0, 20);

  auto h_zdev = new TH1D("h_zdev", "", 100, 0, 100);
  auto h_phidev = new TH1D("h_phidev", "", 100, 0, 100);
  auto h_zdev_v_phidev = new TH2D("h_zdev_v_phidev", "", 100, 0, 100, 100, 0, 100);

  auto h_maxzdev = new TH1D("h_maxzdev", "", 100, 0, 100);
  auto h_maxzdev_v_dbv = new TH2D("h_maxzdev_v_dbv", "", 100, 0, 2.5, 100, 0, 100);
  auto h_maxzdev_v_dbv_big = new TH2D("h_maxzdev_v_dbv_big", "", 100, 0, 2.5, 200, 0, 2000);
  auto h_maxzdev_v_maxdphi = new TH2D("h_maxzdev_v_maxdphi", "", 100, 0, M_PI, 100, 0, 100);
  auto h_maxphidev = new TH1D("h_maxphidev", "", 100, 0, 100);
  auto h_maxzdev_v_maxphidev = new TH2D("h_maxzdev_v_maxphidev", "", 100, 0, 100, 100, 0, 100);

  auto h_maxzdevdphi0pi = new TH1D("h_maxzdevdphi0pi", "", 100, 0, 100);
  auto h_maxzdevdphi0pi_v_dbv = new TH2D("h_maxzdevdphi0pi_v_dbv", "", 100, 0, 2.5, 100, 0, 100);

  nr.loop([&]() {
      const double w = nr.weight();

      if (!nt.gentruth().valid() && nt.event().vcode() != 5) // only 3t1v for bkg
        return std::make_pair(true, w);

      for (int iv = 0, ive = vs.n(); iv < ive; ++iv) {
        const float dbv = vs.dbv(iv, nt.bs()); 
        const std::vector<int> v_tracks = nt.vertex_tracks(iv);
        const int vntk = vs.ntracks(iv); // assert(vntk == v_tracks.size());

        if (nt.gentruth().valid()) {
          if (!vs.genmatch(iv) || vntk < 5) // only look at signal vertices that match to generated vertices
            continue;
        }
        else if (vntk != 3) // only look at 3-track bkg, should be redundant
          continue;

        std::vector<double> vz, phi;
        for (int itk : v_tracks) {
          vz.push_back(tks.vz(itk));
          phi.push_back(tks.phi(itk));
        }

        jmt::StatCalculator d_vz(vz, true), d_phi(phi, true);
        jmt::MaxValue maxdz, maxdphi, maxzdev, maxphidev;
        std::map<int,int> min_deltaz_ipv_count, min_missd_ipv_count;

        for (int iitk = 0; iitk < vntk; ++iitk) {
          const int itk = v_tracks[iitk];

          jmt::MinValue min_deltaz, min_missd;

          const TVector3 tkn = tks.p3(itk).Unit();
          const TVector3 tkv = tks.v(itk);

          for (int ipv = 0, ipve = pvs.n(); ipv < ipve; ++ipv) {
            min_deltaz(ipv, fabs(tks.vz(itk) - pvs.z(ipv)));
            min_missd (ipv, tkn.Cross(tkv - pvs.pos(ipv)).Mag());
          }

          ++min_deltaz_ipv_count[min_deltaz.i()];
          ++min_missd_ipv_count[min_missd.i()];

          const double zdev = fabs(tks.vz(itk) - d_vz.avg[iitk]) / d_vz.rms[iitk];
          const double phidev = fabs(TVector2::Phi_mpi_pi(tks.phi(itk) - d_phi.avg[iitk])) / d_phi.rms[iitk];
          nr.fill(h_zdev, zdev);
          nr.fill(h_phidev, phidev);
          nr.fill(h_zdev_v_phidev, phidev, zdev);
          maxzdev(zdev);
          maxphidev(phidev);

          for (int jjtk = iitk+1; jjtk < vntk; ++jjtk) {
            const int jtk = v_tracks[jjtk];

            const double dz = fabs(tks.vz(itk) - tks.vz(jtk));
            const double dphi = fabs(TVector2::Phi_mpi_pi(tks.phi(itk) - tks.phi(jtk)));
            nr.fill(h_dz, dz);
            nr.fill(h_dphi, dphi);
            nr.fill(h_dz_v_dphi, dphi, dz);
            maxdz(dz);
            maxdphi(dphi);
          }
        }

        if (fabs(maxdphi) < 0.25 || fabs(maxdphi - M_PI) < 0.25) {
          nr.fill(h_maxzdevdphi0pi, maxzdev);
          nr.fill(h_maxzdevdphi0pi_v_dbv, dbv, maxzdev);
        }

        //printf("maxdphi %g maxzdev %g\n", maxdphi, maxzdev);

        nr.fill(h_maxzdev, maxzdev);
        nr.fill(h_maxzdev_v_dbv, dbv, maxzdev);
        nr.fill(h_maxzdev_v_dbv_big, dbv, maxzdev);
        nr.fill(h_maxzdev_v_maxdphi, maxdphi, maxzdev);
        nr.fill(h_maxphidev, maxphidev);
        nr.fill(h_maxzdev_v_maxphidev, maxphidev, maxzdev);

        top_t top2 = top_n(min_deltaz_ipv_count, 2);
        nr.fill(h_maxpvcount_mindeltaz, top2[0].second, top2[1].second);
        nr.fill(h_deltamaxpvcount_mindeltaz, top2[0].second - top2[1].second);

        top2 = top_n(min_missd_ipv_count, 2);
        nr.fill(h_maxpvcount_minmissd, top2[0].second, top2[1].second);
        nr.fill(h_deltamaxpvcount_minmissd, top2[0].second - top2[1].second);

        nr.fill(h_maxdz, maxdz);
        nr.fill(h_maxdphi, maxdphi);
        nr.fill(h_maxdz_v_maxdphi, maxdphi, maxdz);
      }

      return std::make_pair(true, w);
    });
}
