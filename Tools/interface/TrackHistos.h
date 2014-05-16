#ifndef JMTucker_Tools_TrackHistos_h
#define JMTucker_Tools_TrackHistos_h

#include "TH2F.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/SiPixelDetId/interface/PXBDetId.h"
#include "DataFormats/SiPixelDetId/interface/PXFDetId.h"
#include "DataFormats/SiStripDetId/interface/TIBDetId.h"
#include "DataFormats/SiStripDetId/interface/TOBDetId.h"
#include "DataFormats/SiStripDetId/interface/TIDDetId.h"
#include "DataFormats/SiStripDetId/interface/TECDetId.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "JMTucker/Tools/interface/TrackHistos.h"

struct TrackHistos {
  TrackHistos(const char* name, const bool use_rechits_, 
              const int par_nbins[5], const double par_lo[5], const double par_hi[5],
              const int err_nbins[5], const double err_lo[5], const double err_hi[5])
    : use_rechits(use_rechits_)
  {
    edm::Service<TFileService> fs;

    const char* par_names[5] = {"pt", "eta", "phi", "dxy", "dz"};

    for (int i = 0; i < 5; ++i)
      h_track_pars[i] = fs->make<TH1F>(TString::Format("h_%s_track_%s", name,    par_names[i]), "", par_nbins[i], par_lo[i], par_hi[i]);
    for (int i = 0; i < 5; ++i)
      h_track_errs[i] = fs->make<TH1F>(TString::Format("h_%s_track_err%s", name, par_names[i]), "", err_nbins[i], err_lo[i], err_hi[i]);
    for (int i = 0; i < 5; ++i)
      for (int j = i+1; j < 5; ++j)
        h_track_pars_v_pars[i][j] = fs->make<TH2F>(TString::Format("h_%s_track_%s_v_%s", name, par_names[j], par_names[i]), "", par_nbins[i], par_lo[i], par_hi[i], par_nbins[j], par_lo[j], par_hi[j]);
    for (int i = 0; i < 5; ++i)
      for (int j = 0; j < 5; ++j)
        h_track_errs_v_pars[i][j] = fs->make<TH2F>(TString::Format("h_%s_track_err%s_v_%s", name, par_names[j], par_names[i]), "", par_nbins[i], par_lo[i], par_hi[i], err_nbins[j], err_lo[j], err_hi[j]);

    h_track_q       = fs->make<TH1F>(TString::Format("h_%s_track_q",       name), "",  3, -1,   2);
    h_track_nhits   = fs->make<TH1F>(TString::Format("h_%s_track_nhits",   name), "", 40,  0,  40);
    h_track_npxhits = fs->make<TH1F>(TString::Format("h_%s_track_npxhits", name), "", 12,  0,  12);
    h_track_nsthits = fs->make<TH1F>(TString::Format("h_%s_track_nsthits", name), "", 28,  0,  28);
    h_track_chi2    = fs->make<TH1F>(TString::Format("h_%s_track_chi2",    name), "", 50,  0, 100);
    h_track_dof     = fs->make<TH1F>(TString::Format("h_%s_track_dof",     name), "", 50,  0, 100);
    h_track_chi2dof = fs->make<TH1F>(TString::Format("h_%s_track_chi2dof", name), "", 50,  0,  10);
    h_track_algo    = fs->make<TH1F>(TString::Format("h_%s_track_algo",    name), "", 30,  0,  30);
    h_track_quality = fs->make<TH1F>(TString::Format("h_%s_track_quality", name), "",  7,  0,   7);
    h_track_nloops  = fs->make<TH1F>(TString::Format("h_%s_track_nloops",  name), "", 10,  0,  10);

    if (use_rechits) {
      h_track_unknown_detid = fs->make<TH1F>(TString::Format("h_%s_track_unknown_detid", name), "", 1, 0, 1);

      for (int i = 1; i <= 3; ++i)
        h_track_pxb_ladder_module[i] = fs->make<TH2F>(TString::Format("h_%s_track_pxb_layer_%i_ladder_module", name, i), ";ladder;module", 256, 0, 256, 64, 0, 64);

      for (int i = 1; i <= 2; ++i)
        for (int j = 1; j <= 2; ++j)
          for (int k = 1; k <= 4; ++k)
            h_track_pxf_panel_module[i][j][k] = fs->make<TH2F>(TString::Format("h_%s_track_pxf_side_%i_disk_%i_panel_%i_blade_module", name, i, j, k), ";blade;module", 64, 0, 64, 64, 0, 64);

      for (int i = 1; i <= 2; ++i)
        for (int j = 1; j <= 4; ++j)
          h_track_tib_layer_string[i][j] = fs->make<TH2F>(TString::Format("h_%s_track_tib_side_%i_module_%i_layer_string", name, i, j), ";layer;string", 8, 0, 8, 64, 0, 64);

      for (int i = 1; i <= 2; ++i)
        for (int j = 1; j <= 8; ++j)
          h_track_tob_rod_module[i][j] = fs->make<TH2F>(TString::Format("h_%s_track_tob_side_%i_layer_%i_rod_module", name, i, j), ";rod;module", 128, 0, 128, 8, 0, 8);

      for (int i = 1; i <= 2; ++i)
        for (int j = 1; j <= 4; ++j)
          h_track_tid_ring_module[i][j] = fs->make<TH2F>(TString::Format("h_%s_track_tid_side_%i_wheel_%i_ring_module", name, i, j), ";ring;module", 4, 0, 4, 32, 0, 32);

      for (int i = 1; i <= 2; ++i)
        for (int j = 1; j <= 16; ++j)
          for (int k = 1; k <= 8; ++k)
            h_track_tec_petal_module[i][j][k] = fs->make<TH2F>(TString::Format("h_%s_track_tec_side_%i_wheel_%i_ring_%i_petal_module", name, i, j, k), ";petal;module", 16, 0, 16, 8, 0, 8);
    }
  }

  bool Fill(const reco::Track& tk) {
    bool ok = true;

    const double pars[5] = { tk.pt(),      tk.eta(),      tk.phi(),      tk.dxy(),      tk.dz()      };
    const double errs[5] = { tk.ptError(), tk.etaError(), tk.phiError(), tk.dxyError(), tk.dzError() };

    for (int i = 0; i < 5; ++i) {
      h_track_pars[i]->Fill(pars[i]);
      h_track_errs[i]->Fill(errs[i]);
      for (int j = 0; j < 5; ++j) {
        if (j >= i+1)
          h_track_pars_v_pars[i][j]->Fill(pars[i], pars[j]);
        h_track_errs_v_pars[i][j]->Fill(pars[i], errs[j]);
      }
    }

    h_track_q->Fill(tk.charge());
    h_track_nhits  ->Fill(tk.hitPattern().numberOfValidHits());
    h_track_npxhits->Fill(tk.hitPattern().numberOfValidPixelHits());
    h_track_nsthits->Fill(tk.hitPattern().numberOfValidStripHits());
    h_track_chi2->Fill(tk.chi2());
    h_track_dof->Fill(tk.ndof());
    h_track_chi2dof->Fill(tk.chi2()/tk.ndof());
    h_track_algo->Fill(int(tk.algo()));
    for (int i = 0; i < 7; ++i)
      if (tk.quality(reco::Track::TrackQuality(i))) h_track_quality->Fill(i);
    h_track_nloops->Fill(tk.nLoops());

    if (use_rechits) {
      for (int i = 0, ie = int(tk.recHitsSize()); i < ie; ++i) {
        DetId dd = tk.recHit(i)->geographicalId();
        if (dd.det() == DetId::Tracker) {
          if (dd.subdetId() == (int) PixelSubdetector::PixelBarrel) {
            PXBDetId d(dd);
            h_track_pxb_ladder_module[d.layer()]->Fill(d.ladder(), d.module());
          }
          else if (dd.subdetId() == (int) PixelSubdetector::PixelEndcap) {
            PXFDetId d(dd);
            h_track_pxf_panel_module[d.side()][d.disk()][d.panel()]->Fill(d.blade(), d.module());
          }
          else if (dd.subdetId() == StripSubdetector::TIB) {
            TIBDetId d(dd);
            h_track_tib_layer_string[d.side()][d.module()]->Fill(d.layer(), d.stringNumber());
          }
          else if (dd.subdetId() == StripSubdetector::TOB) {
            TOBDetId d(dd);
            h_track_tob_rod_module[d.side()][d.layer()]->Fill(d.rodNumber(), d.module());
          }
          else if (dd.subdetId() == StripSubdetector::TID) {
            TIDDetId d(dd);
            h_track_tid_ring_module[d.side()][d.wheel()]->Fill(d.ring(), d.moduleNumber());
          }
          else if (dd.subdetId() == StripSubdetector::TEC) {
            TECDetId d(dd);
            h_track_tec_petal_module[d.side()][d.wheel()][d.ring()]->Fill(d.petalNumber(), d.module());
          }
          else {
            ok = false;
            h_track_unknown_detid->Fill(0);
          }
        }
      }
    }

    return ok;
  }

  const bool use_rechits;
  TH1F* h_track_pars[5];
  TH1F* h_track_errs[5];
  TH2F* h_track_pars_v_pars[5][4];
  TH2F* h_track_errs_v_pars[5][5];
  TH1F* h_track_q;
  TH1F* h_track_nhits;
  TH1F* h_track_npxhits;
  TH1F* h_track_nsthits;
  TH1F* h_track_chi2;
  TH1F* h_track_dof;
  TH1F* h_track_chi2dof;
  TH1F* h_track_algo;
  TH1F* h_track_quality;
  TH1F* h_track_nloops;
  TH1F* h_track_unknown_detid;
  TH2F* h_track_pxb_ladder_module[3];
  TH2F* h_track_pxf_panel_module[3][3][5];
  TH2F* h_track_tib_layer_string[3][5];
  TH2F* h_track_tob_rod_module[3][9];
  TH2F* h_track_tid_ring_module[3][5];
  TH2F* h_track_tec_petal_module[3][17][9];
};

#endif



