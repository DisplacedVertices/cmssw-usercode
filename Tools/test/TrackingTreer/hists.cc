#include <fstream>
#include <iostream>
#include <string>
#include <vector>
#include "TFile.h"
#include "TH1.h"
#include "TH2.h"
#include "TTree.h"
#include "TVector2.h"
#include "JMTucker/Tools/interface/TrackingTree.h"
#include "utils.h"
#include <assert.h>

int main(int argc, char** argv) {
  if (argc < 3) {
    fprintf(stderr, "usage: hists.exe files_in.txt out.root\n");
    return 1;
  }

  const char* files_in_fn = argv[1];
  const char* out_fn = argv[2];

  root_setup();

  std::vector<std::string> fns;
  std::ifstream files_in(files_in_fn);
  std::string fn_tmp;
  while (files_in >> fn_tmp)
    fns.push_back(fn_tmp);
  printf("will read %lu files:\n", fns.size());

  bool is_mc = true;
  if (std::string(files_in_fn) == "data.txt")
    is_mc = false;

  bool z_slice = false;
  bool nhits_slice = false;
  bool pt_slice = true;
  bool eta_slice = true;

  const double z_slice_bounds[2] = { -7.5, -2.5 };
  const double nhits_slice_bounds[2] = { 0, 3 };
  const double pt_slice_bounds[2] = { 5, 1e9 };
  const double eta_slice_bounds[2] = { 1.9, 2.5 };

  const double min_all_track_pt = 1;
  const double min_all_track_sigmadxy = 4;
  //  const int min_all_track_nhits = 8;
  //  const int min_all_track_npxhits = 2;
  const int min_all_track_min_r = 1;
  const int min_all_track_npxlays = 2;
  const int min_all_track_nstlays = 4;

  //  const double pileup_weights[40] = { 99.15056679507543, 172.99847243562277, 121.89056539480684, 36.648532815731905, 15.130284226820047, 3.388892702882986, 1.986252356518944, 2.553598893553273, 3.391463356559057, 3.329138633709162, 3.078061196234216, 2.7655190007638786, 2.183863508534957, 1.4521096234256572, 0.8040188219328743, 0.3713065789043111, 0.15067662959667333, 0.061442166758053925, 0.029481930242311164, 0.015649765632974884, 0.007675085464470436, 0.003212647741405869, 0.0011654706818925956, 0.0003947719988503597, 0.00013783918071098118, 5.240303150410027e-05, 2.121092370685294e-05, 8.720595168624445e-06, 3.5144188113130866e-06, 1.3327213104566867e-06, 4.428988947779108e-07, 1.1797413268628033e-07, 2.422301652608736e-08, 3.9984662880098295e-09, 5.655318026602206e-10, 7.135693975440923e-11, 8.180332652856529e-12, 8.590503460873983e-13, 8.181362972336421e-14, 7.046437100909094e-15 };

  //  const double pileup_weights[50] = { 0.0, 0.0, 59.337367298506194, 24.8077111479546, 30.171542595767974, 1.6463976191583929, 1.3492771650541147, 1.9978387363280743, 2.4586851723072107, 2.4908183520463014, 2.4258366625729764, 2.3274230208939786, 2.0002901774528077, 1.5744241110155093, 1.1681251209776078, 0.7736292323891238, 0.4714770290840279, 0.2676959790610609, 0.15524650927133532, 0.10132520917928384, 0.08472177641430646, 0.07927574663947269, 0.08390290731362979, 0.09750091335949468, 0.12058205934514545, 0.16519259956459129, 0.1980959867482783, 0.24105092268610864, 0.4611856198417187, 0.5947794446993874, 1.029106792358867, 0.8974099002954592, 0.7882654444004721, 0.8380983397875282, 0.3218297919915704, 0.7542885512112272, 0.13871973570601948, 0.12068616474074438, 0.11174645158850818, 0.12571475930401357, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 }; // For MC 74 vs MC 76 comparison

  const double pileup_weights[40] = { 0.4430900689834877, 0.7774946230174374, 1.211532146615326, 1.5555095481485082, 1.3656299694579321, 1.9513380206283242, 1.4311409855780286, 1.2555573073998676, 1.3509572272968273, 1.3430021765269047, 1.2671533450149761, 1.1830775671347276, 1.0767805180896135, 0.9110431461207203, 0.6971726104245397, 0.48543658081115554, 0.32209366814732293, 0.22848641867558733, 0.19027360131827362, 0.15527725489164057, 0.09487219082044276, 0.04095796584834362, 0.013672759117602781, 0.003987335129679708, 0.0011389782126837726, 0.00033784224878244623, 0.00010191256127555789, 2.9928259966798484e-05, 8.357594204838038e-06, 2.2051905560049044e-06, 5.493198439639333e-07, 1.2915574040259908e-07, 2.8638852677561204e-08, 5.978815170388724e-09, 1.1718664799704302e-09, 2.147556635829967e-10, 3.658973660525496e-11, 5.759196292572524e-12, 8.200005561089732e-13, 1.0437472148786202e-13 }; // 76 weights

  TFile* f_out = new TFile(out_fn, "recreate");

  TH1D* h_norm = new TH1D("h_norm", "", 1, 0, 1);
  TH1D* h_npu = new TH1D("h_npu", ";true npu", 50, 0, 50);
  TH1D* h_npv = new TH1D("h_npv", ";number of primary vertices", 50, 0, 50);
  TH1D* h_bsx = new TH1D("h_bsx", ";beamspot x", 400, -0.15, 0.15);
  TH1D* h_bsy = new TH1D("h_bsy", ";beamspot y", 400, -0.15, 0.15);
  TH1D* h_bsz = new TH1D("h_bsz", ";beamspot z", 800, -5, 5);
  TH1D* h_bsdxdz = new TH1D("h_bsdxdz", ";beamspot dx/dz", 100, -1e-4, 5e-4);
  TH1D* h_bsdydz = new TH1D("h_bsdydz", ";beamspot dy/dz", 100, -1e-4, 1e-4);
  TH1D* h_pvbsx = new TH1D("h_pvbsx", ";pvx - bsx", 400, -0.05, 0.05);
  TH1D* h_pvbsy = new TH1D("h_pvbsy", ";pvy - bsy", 400, -0.05, 0.05); 
  TH1D* h_pvbsz = new TH1D("h_pvbsz", ";pvz - bsz", 500, -15, 15);
  TH2D* h_bsy_v_bsx = new TH2D("h_bsy_v_bsx", ";beamspot x;beamspot y", 4000, -1, 1, 4000, -1, 1);
  TH2D* h_pvy_v_pvx = new TH2D("h_pvy_v_pvx", ";pvx;pvy", 4000, -1, 1, 4000, -1, 1);

  TH1D* h_n_all_tracks = new TH1D("h_n_all_tracks",  ";all tracks", 40, 0, 2000);
  TH1D* h_n_seed_tracks = new TH1D("h_n_seed_tracks", ";seed tracks", 50, 0,  50);
  TH1D* h_n_seed_nosigcut_tracks = new TH1D("h_n_seed_nosigcut_tracks", ";seed tracks w/o sigmadxy cut", 50, 0,  200);

  const char* par_names[9] = {"pt", "eta", "phi", "dxybs", "dxypv", "dxy", "dz", "dzpv", "dzpv_zoom"};
  const int par_nbins[9] = { 50, 50, 50, 400, 400, 400, 80, 80, 100 };
  const double par_lo[9] = { 0, -2.5, -3.15, -0.2, -0.2, -0.2, -20, -20, -1.5 };
  const double par_hi[9] = { 10,  2.5,  3.15,  0.2, 0.2, 0.2, 20, 20, 1.5};
  const char* err_names[5] = { "pt", "eta", "phi", "dxy", "dz" };
  const int err_nbins[5] = { 50, 50, 50, 400, 80 }; 
  const double err_lo[5] = { 0 };
  const double err_hi[5] = { 0.15, 0.01, 0.01, 0.1, 0.4 };

  const char* hitpar_names[12] = {"nhits", "npxhits", "npxlays", "nsthits", "nstlays", "min_r", "max_r", "maxpx_r", "min_z", "max_z", "maxpx_z", "deltarpx"};
  const int hitpar_nbins[12] = {40, 12, 6, 28, 20, 16, 16, 16, 16, 16, 16, 16};
  const int hitpar_lo[12] = { 0 };
  const int hitpar_hi[12] = {40, 12, 6, 28, 20, 16, 16, 16, 16, 16, 16, 16};

  TH1D* h_all_track_pars[9];
  TH1D* h_all_track_errs[5];
  TH2D* h_all_track_dxybs_v_pars[1][9];
  TH2D* h_all_track_dxyerr_v_pars[1][9];
  for (int i = 0; i < 9; ++i)
    h_all_track_pars[i] = new TH1D(TString::Format("h_all_track_%s", par_names[i]), TString::Format(";all track %s", par_names[i]), par_nbins[i], par_lo[i], par_hi[i]);
  for (int i = 0; i < 5; ++i) 
    h_all_track_errs[i] = new TH1D(TString::Format("h_all_track_err%s", err_names[i]), TString::Format(";all track err%s", err_names[i]), err_nbins[i], err_lo[i], err_hi[i]);
  TH1D* h_all_track_hitpars[12];
  TH2D* h_all_track_dxyerr_v_hitpars[1][12];
  for (int i = 0; i < 12; ++i)
    h_all_track_hitpars[i] = new TH1D(TString::Format("h_all_track_%s", hitpar_names[i]), TString::Format(";all track %s", hitpar_names[i]), hitpar_nbins[i], hitpar_lo[i], hitpar_hi[i]);
  TH1D* h_all_track_sigmadxybs = new TH1D("h_all_track_sigmadxybs", ";all track sigmadxybs", 1000, -10, 10);
  TH1D* h_all_track_charge = new TH1D("h_all_track_charge", ";all track charge", 4, -2, 2);
  for (int i = 0; i < 9; ++i) { 
    if (i == 2)
      h_all_track_dxybs_v_pars[0][i] = new TH2D(TString::Format("h_all_track_dxybs_v_%s", par_names[i]), TString::Format(";all track %s;dxybs", par_names[i]), par_nbins[i], par_lo[i], par_hi[i], 4000, par_lo[3], par_hi[3]);
    else 
      h_all_track_dxybs_v_pars[0][i] = new TH2D(TString::Format("h_all_track_dxybs_v_%s", par_names[i]), TString::Format(";all track %s;dxybs", par_names[i]), par_nbins[i], par_lo[i], par_hi[i], par_nbins[3], par_lo[3], par_hi[3]);
  }
  for (int i = 0; i < 9; ++i) 
    h_all_track_dxyerr_v_pars[0][i] = new TH2D(TString::Format("h_all_track_dxyerr_v_%s", par_names[i]), TString::Format(";all track %s;dxyerr", par_names[i]), par_nbins[i], par_lo[i], par_hi[i], err_nbins[3], err_lo[3], err_hi[3]);
  for (int i = 0; i < 12; ++i)
    h_all_track_dxyerr_v_hitpars[0][i] = new TH2D(TString::Format("h_all_track_dxyerr_v_%s", hitpar_names[i]), TString::Format(";all track %s;dxyerr", hitpar_names[i]), hitpar_nbins[i], hitpar_lo[i], hitpar_hi[i], err_nbins[3], err_lo[3], err_hi[3]);
  TH2D* h_all_track_eta_v_phi[1][1];
  h_all_track_eta_v_phi[0][0] = new TH2D("h_all_track_eta_v_phi", ";all track phi;eta", par_nbins[2], par_lo[2], par_hi[2], par_nbins[1], par_lo[1], par_hi[1]);

  TH1D* h_seed_track_pars[9];
  TH1D* h_seed_track_errs[5];
  TH2D* h_seed_track_dxybs_v_pars[1][9];
  TH2D* h_seed_track_dxyerr_v_pars[1][9];
  for (int i = 0; i < 9; ++i)
    h_seed_track_pars[i] = new TH1D(TString::Format("h_seed_track_%s", par_names[i]), TString::Format(";seed track %s", par_names[i]), par_nbins[i], par_lo[i], par_hi[i]);
  for (int i = 0; i < 5; ++i) 
    h_seed_track_errs[i] = new TH1D(TString::Format("h_seed_track_err%s", err_names[i]), TString::Format(";seed track err%s", par_names[i]), err_nbins[i], err_lo[i], err_hi[i]);
  TH1D* h_seed_track_hitpars[12];
  TH2D* h_seed_track_dxyerr_v_hitpars[1][12];
  for (int i = 0; i < 12; ++i)
    h_seed_track_hitpars[i] = new TH1D(TString::Format("h_seed_track_%s", hitpar_names[i]), TString::Format(";seed track %s", hitpar_names[i]), hitpar_nbins[i], hitpar_lo[i], hitpar_hi[i]);
  TH1D* h_seed_track_sigmadxybs = new TH1D("h_seed_track_sigmadxybs", ";seed track sigmadxybs", 200, -10, 10);
  TH1D* h_seed_track_charge = new TH1D("h_seed_track_charge", ";seed track charge", 4, -2, 2);
  for (int i = 0; i < 9; ++i) {
    if (i == 2)
      h_seed_track_dxybs_v_pars[0][i] = new TH2D(TString::Format("h_seed_track_dxybs_v_%s", par_names[i]), TString::Format(";seed track %s;dxybs", par_names[i]), par_nbins[i], par_lo[i], par_hi[i], 4000, par_lo[3], par_hi[3]);
    else
      h_seed_track_dxybs_v_pars[0][i] = new TH2D(TString::Format("h_seed_track_dxybs_v_%s", par_names[i]), TString::Format(";seed track %s;dxybs", par_names[i]), par_nbins[i], par_lo[i], par_hi[i], par_nbins[3], par_lo[3], par_hi[3]);
  }
  for (int i = 0; i < 9; ++i) 
    h_seed_track_dxyerr_v_pars[0][i] = new TH2D(TString::Format("h_seed_track_dxyerr_v_%s", par_names[i]), TString::Format(";seed track %s;dxyerr", par_names[i]), par_nbins[i], par_lo[i], par_hi[i], err_nbins[3], err_lo[3], err_hi[3]);
  for (int i = 0; i < 12; ++i)
    h_seed_track_dxyerr_v_hitpars[0][i] = new TH2D(TString::Format("h_seed_track_dxyerr_v_%s", hitpar_names[i]), TString::Format(";seed track %s;dxyerr", hitpar_names[i]), hitpar_nbins[i], hitpar_lo[i], hitpar_hi[i], err_nbins[3], err_lo[3], err_hi[3]);
  TH2D* h_seed_track_eta_v_phi[1][1];
  h_seed_track_eta_v_phi[0][0] = new TH2D("h_seed_track_eta_v_phi", ";seed track phi;eta", par_nbins[2], par_lo[2], par_hi[2], par_nbins[1], par_lo[1], par_hi[1]);

  TH1D* h_seed_nosigcut_track_pars[9];
  TH1D* h_seed_nosigcut_track_errs[5];
  TH2D* h_seed_nosigcut_track_dxybs_v_pars[1][9];
  TH2D* h_seed_nosigcut_track_dxyerr_v_pars[1][9];
  for (int i = 0; i < 9; ++i) 
    h_seed_nosigcut_track_pars[i] = new TH1D(TString::Format("h_seed_nosigcut_track_%s", par_names[i]), TString::Format(";seed nosig track %s", par_names[i]), par_nbins[i], par_lo[i], par_hi[i]);
  for (int i = 0; i < 5; ++i) 
    h_seed_nosigcut_track_errs[i] = new TH1D(TString::Format("h_seed_nosigcut_track_err%s", err_names[i]), TString::Format(";seed nosig track err%s", par_names[i]), err_nbins[i], err_lo[i], err_hi[i]); 
  TH1D* h_seed_nosigcut_track_hitpars[12];
  TH2D* h_seed_nosigcut_track_dxyerr_v_hitpars[1][12];
  for (int i = 0; i < 12; ++i)
    h_seed_nosigcut_track_hitpars[i] = new TH1D(TString::Format("h_seed_nosigcut_track_%s", hitpar_names[i]), TString::Format(";seed nosig track %s", hitpar_names[i]), hitpar_nbins[i], hitpar_lo[i], hitpar_hi[i]);
  TH1D* h_seed_nosigcut_track_sigmadxybs = new TH1D("h_seed_nosigcut_track_sigmadxybs", ";seed nosig track sigmadxybs", 1000, -10, 10);
  TH1D* h_seed_nosigcut_track_charge = new TH1D("h_seed_nosigcut_track_charge", ";seed nosig track charge", 4, -2, 2);
  for (int i = 0; i < 9; ++i) {
    if (i == 2) 
      h_seed_nosigcut_track_dxybs_v_pars[0][i] = new TH2D(TString::Format("h_seed_nosigcut_track_dxybs_v_%s", par_names[i]), TString::Format(";seed nosig track %s;dxybs", par_names[i]), par_nbins[i], par_lo[i], par_hi[i], 4000, par_lo[3], par_hi[3]);
    else 
      h_seed_nosigcut_track_dxybs_v_pars[0][i] = new TH2D(TString::Format("h_seed_nosigcut_track_dxybs_v_%s", par_names[i]), TString::Format(";seed nosig track %s;dxybs", par_names[i]), par_nbins[i], par_lo[i], par_hi[i], par_nbins[3], par_lo[3], par_hi[3]);
  }
  for (int i = 0; i < 9; ++i) 
    h_seed_nosigcut_track_dxyerr_v_pars[0][i] = new TH2D(TString::Format("h_seed_nosigcut_track_dxyerr_v_%s", par_names[i]), TString::Format(";seed nosig track %s;dxyerr", par_names[i]), par_nbins[i], par_lo[i], par_hi[i], err_nbins[3], err_lo[3], err_hi[3]);
  for (int i = 0; i < 12; ++i)
    h_seed_nosigcut_track_dxyerr_v_hitpars[0][i] = new TH2D(TString::Format("h_seed_nosigcut_track_dxyerr_v_%s", hitpar_names[i]), TString::Format(";seed nosig track %s;dxyerr", hitpar_names[i]), hitpar_nbins[i], hitpar_lo[i], hitpar_hi[i], err_nbins[3], err_lo[3], err_hi[3]);
  TH2D* h_seed_nosigcut_track_eta_v_phi[1][1];
  h_seed_nosigcut_track_eta_v_phi[0][0] = new TH2D("h_seed_nosigcut_track_eta_v_phi", ";seed nosig track phi;eta", par_nbins[2], par_lo[2], par_hi[2], par_nbins[1], par_lo[1], par_hi[1]);

  for (const std::string& fn : fns) {
    std::cout << fn << std::endl;
    file_and_tree fat(fn.c_str());
    TrackingTree& nt = fat.nt;
    
    TH1D* h_sums = ((TH1D*)fat.f->Get("mcStat/h_sums"));
    is_mc = h_sums != 0;

    if (is_mc)
      h_norm->Fill(0.5, ((TH1D*)fat.f->Get("mcStat/h_sums"))->GetBinContent(1));
      
    long jj = 0, jje = fat.t->GetEntries();
    for (; jj < jje; ++jj) {
      if (fat.t->LoadTree(jj) < 0) break;
      if (fat.t->GetEntry(jj) <= 0) continue;
      if (jj % 2000 == 0) {
        printf("\r%li/%li", jj, jje);
        fflush(stdout);
      }

      h_npu->Fill(nt.npu);

      int inpu = int(nt.npu);
      assert(inpu >= 0);
      
      int n_all_tracks = 0;
      int n_seed_tracks = 0;
      int n_seed_nosigcut_tracks = 0;
      
      double weight;
      if (inpu >= 40)
	weight = pileup_weights[39];
      else
	weight = pileup_weights[inpu];
      
      double w = 1.0;
      if (is_mc)
	w = weight;

      h_npv->Fill(nt.npvs(), w);

      const double bsx = nt.bs_x;
      const double bsy = nt.bs_y;
      const double bsz = nt.bs_z;
      
      h_bsx->Fill(bsx, w);
      h_bsy->Fill(bsy, w);
      h_bsz->Fill(bsz, w);
      h_bsdxdz->Fill(nt.bs_dxdz, w);
      h_bsdydz->Fill(nt.bs_dydz, w);
      h_bsy_v_bsx->Fill(bsx, bsy, w);

      const double pvbsx = nt.p_pv_x->at(0) - bsx;
      const double pvbsy = nt.p_pv_y->at(0) - bsy;
      const double pvbsz = nt.p_pv_z->at(0) - bsz;
      h_pvbsx->Fill(pvbsx, w);
      h_pvbsy->Fill(pvbsy, w);
      h_pvbsz->Fill(pvbsz, w);

      h_pvy_v_pvx->Fill(nt.p_pv_x->at(0), nt.p_pv_y->at(0), w);

      for (int itk = 0, itke = nt.ntks(); itk < itke; ++itk) {
	const double pt = fabs(nt.p_tk_qpt->at(itk));
	const double sigmadxy = nt.p_tk_dxybs->at(itk) / nt.p_tk_err_dxy->at(itk);
	const int npxhits = nt.p_tk_npxhit->at(itk);
	const int nsthits = nt.p_tk_nsthit->at(itk);
	const int nhits = npxhits + nsthits;
	const int npxlays = nt.p_tk_npxlay->at(itk);
	const int nstlays = nt.p_tk_nstlay->at(itk);
	const double vz = nt.p_tk_vz->at(itk);
	const double dzpv = nt.p_tk_dzpv->at(itk);
	const int min_r = nt.tk_min_r(itk);
	const int min_z = nt.tk_min_z(itk);
	const int max_r = nt.tk_max_r(itk);
	const int max_z = nt.tk_max_z(itk);
	const int maxpx_r = nt.tk_maxpx_r(itk);
	const int maxpx_z = nt.tk_maxpx_z(itk);
	const int deltarpx = maxpx_r - min_r;
	const double eta = fabs(nt.p_tk_eta->at(itk));

	int charge;
	if (nt.p_tk_qpt->at(itk) > 0)
	  charge = 1;
	else
	  charge = -1;

	//	const bool use = pt > min_all_track_pt && nhits >= min_all_track_nhits && npxhits >= min_all_track_npxhits && fabs(sigmadxy) > min_all_track_sigmadxy && min_r == min_all_track_min_r;
	//	const bool use_nosigcut = pt > min_all_track_pt && nhits >= min_all_track_nhits && npxhits >= min_all_track_npxhits && min_r == min_all_track_min_r;
	const bool use = pt > min_all_track_pt && npxlays >= min_all_track_npxlays && nstlays >= min_all_track_nstlays && fabs(sigmadxy) > min_all_track_sigmadxy && min_r == min_all_track_min_r;
	const bool use_nosigcut = pt > min_all_track_pt && npxlays >= min_all_track_npxlays && nstlays >= min_all_track_nstlays && min_r == min_all_track_min_r;
	

	bool z_slice_use = vz > z_slice_bounds[0] && vz < z_slice_bounds[1];
	bool nhits_slice_use = nhits > nhits_slice_bounds[0] && nhits < nhits_slice_bounds[1];
	bool pt_slice_use = pt > pt_slice_bounds[0] && pt < pt_slice_bounds[1];
	bool eta_slice_use = eta > eta_slice_bounds[0] && eta < eta_slice_bounds[1];

	if (!z_slice)
	  z_slice_use = true;
	
	if (!nhits_slice)
	  nhits_slice_use = true;

	if (!pt_slice)
	  pt_slice_use = true;
	
	if (!eta_slice)
	  eta_slice_use = true;

	const double pars[9] = {pt, nt.p_tk_eta->at(itk), nt.p_tk_phi->at(itk), nt.p_tk_dxybs->at(itk), nt.p_tk_dxypv->at(itk), nt.p_tk_dxybs->at(itk), vz, dzpv, dzpv};
	const double errs[5] = {nt.p_tk_err_qpt->at(itk), nt.p_tk_err_eta->at(itk), nt.p_tk_err_phi->at(itk), nt.p_tk_err_dxy->at(itk), nt.p_tk_err_dz->at(itk)};
	const int hitpars[12] = {nhits, npxhits, npxlays, nsthits, nstlays, min_r, max_r, maxpx_r, min_z, max_z, maxpx_z, deltarpx};
	if (z_slice_use && nhits_slice_use && pt_slice_use && eta_slice_use) {
	  ++n_all_tracks;

	  if (use) {
	    ++n_seed_tracks;
	    h_seed_track_eta_v_phi[0][0]->Fill(pars[2], pars[1], w);
	    h_seed_track_sigmadxybs->Fill(sigmadxy, w);
	    h_seed_track_charge->Fill(charge);
	    for (int i = 0; i < 12; ++i) {
	      h_seed_track_hitpars[i]->Fill(hitpars[i], w);
	      h_seed_track_dxyerr_v_hitpars[0][i]->Fill(hitpars[i], errs[3], w);
	    }
	  }

	  if (use_nosigcut) {
	    ++n_seed_nosigcut_tracks;
	    h_seed_nosigcut_track_eta_v_phi[0][0]->Fill(pars[2], pars[1], w);
	    h_seed_nosigcut_track_sigmadxybs->Fill(sigmadxy, w);
	    h_seed_nosigcut_track_charge->Fill(charge);
            for (int i = 0; i < 12; ++i) {
              h_seed_nosigcut_track_hitpars[i]->Fill(hitpars[i], w);
	      h_seed_nosigcut_track_dxyerr_v_hitpars[0][i]->Fill(hitpars[i], errs[3], w);
	    }
	  }

	  for (int i = 0; i < 9; ++i) {
	    h_all_track_pars[i]->Fill(pars[i], w);
	    h_all_track_dxybs_v_pars[0][i]->Fill(pars[i], pars[3], w);
	    h_all_track_dxyerr_v_pars[0][i]->Fill(pars[i], errs[3], w);
	    if (use) {
	      h_seed_track_pars[i]->Fill(pars[i], w);
	      h_seed_track_dxybs_v_pars[0][i]->Fill(pars[i], pars[3], w);
	      h_seed_track_dxyerr_v_pars[0][i]->Fill(pars[i], errs[3], w);
	    }
	    if (use_nosigcut) {
	      h_seed_nosigcut_track_pars[i]->Fill(pars[i], w);
	      h_seed_nosigcut_track_dxybs_v_pars[0][i]->Fill(pars[i], pars[3], w);
	      h_seed_nosigcut_track_dxyerr_v_pars[0][i]->Fill(pars[i], errs[3], w);
	    }
	  }

	  for (int i = 0; i < 5; ++i) {
	    h_all_track_errs[i]->Fill(errs[i], w);
	    if (use) 
	      h_seed_track_errs[i]->Fill(errs[i], w);
	    if (use_nosigcut)
	      h_seed_nosigcut_track_errs[i]->Fill(errs[i], w);
	  }
	
	  h_all_track_eta_v_phi[0][0]->Fill(pars[2], pars[1], w);
	  h_all_track_sigmadxybs->Fill(sigmadxy, w);
	  h_all_track_charge->Fill(charge);
	  for (int i = 0; i < 12; ++i) {
	    h_all_track_hitpars[i]->Fill(hitpars[i], w);
	    h_all_track_dxyerr_v_hitpars[0][i]->Fill(hitpars[i], errs[3], w);
	  }
	}
      }

      h_n_all_tracks->Fill(n_all_tracks, w);
      h_n_seed_tracks->Fill(n_seed_tracks, w);
      h_n_seed_nosigcut_tracks->Fill(n_seed_nosigcut_tracks, w);
    }

    printf("\r%li/%li\n", jj, jje);
  }

  f_out->Write();
  f_out->Close();
  delete f_out;
}
