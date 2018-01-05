#ifndef JMTucker_Tools_TrackHistos_h
#define JMTucker_Tools_TrackHistos_h

namespace reco {
  class BeamSpot;
  class Track;
  class Vertex;
}

class TH1D;
class TH2D;

namespace jmt {
  struct TrackHistos {
    TrackHistos(const char* name, const bool use_rechits_=false);
    bool Fill(const reco::Track& tk, const reco::BeamSpot* bs=0, const reco::Vertex* pv=0);

    TH1D* h_pars[9];
    TH1D* h_errs[6];
    TH2D* h_pars_v_pars[9][9];
    TH2D* h_errs_v_pars[9][6];
    TH1D* h_dptopt;
    TH1D* h_sigmadxybs;
    TH1D* h_q;
    TH1D* h_nhits;
    TH1D* h_npxhits;
    TH1D* h_nsthits;
    TH1D* h_npxlayers;
    TH1D* h_nstlayers;
    TH1D* h_nlosthits;
    TH1D* h_nlostlayers;
    TH1D* h_chi2;
    TH1D* h_dof;
    TH1D* h_chi2dof;
    TH1D* h_algo;
    TH1D* h_quality;
    TH1D* h_highpurity;
    TH1D* h_nloops;

    const bool use_rechits;
    TH1D* h_unknown_detid;
    TH2D* h_pxb_ladder_module[3];
    TH2D* h_pxf_panel_module[3][3][5];
    TH2D* h_tib_layer_string[3][5];
    TH2D* h_tob_rod_module[3][9];
    TH2D* h_tid_ring_module[3][5];
    TH2D* h_tec_petal_module[3][17][9];
  };
}

#endif
