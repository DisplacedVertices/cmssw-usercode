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

  const double min_all_track_pt = 1;
  const double min_all_track_sigmadxy = 4;
  const int min_all_track_nhits = 8;
  const int min_all_track_npxhits = 2;

  const double pileup_weights[40] = { 99.15056679507543, 172.99847243562277, 121.89056539480684, 36.648532815731905, 15.130284226820047, 3.388892702882986, 1.986252356518944, 2.553598893553273, 3.391463356559057, 3.329138633709162, 3.078061196234216, 2.7655190007638786, 2.183863508534957, 1.4521096234256572, 0.8040188219328743, 0.3713065789043111, 0.15067662959667333, 0.061442166758053925, 0.029481930242311164, 0.015649765632974884, 0.007675085464470436, 0.003212647741405869, 0.0011654706818925956, 0.0003947719988503597, 0.00013783918071098118, 5.240303150410027e-05, 2.121092370685294e-05, 8.720595168624445e-06, 3.5144188113130866e-06, 1.3327213104566867e-06, 4.428988947779108e-07, 1.1797413268628033e-07, 2.422301652608736e-08, 3.9984662880098295e-09, 5.655318026602206e-10, 7.135693975440923e-11, 8.180332652856529e-12, 8.590503460873983e-13, 8.181362972336421e-14, 7.046437100909094e-15 };

  TFile* f_out = new TFile(out_fn, "recreate");

  TH1F* h_norm = new TH1F("h_norm", "", 1, 0, 1);
  TH1F* h_npu = new TH1F("h_npu", "", 50, 0, 50);
  TH1F* h_npv = new TH1F("h_npv", "", 50, 0, 50);
  TH1F* h_pvbsx = new TH1F("h_pvbsx", "", 100, -0.5, 0.5);
  TH1F* h_pvbsy = new TH1F("h_pvbsy", "", 100, -0.5, 0.5); 
  TH1F* h_pvbsz = new TH1F("h_pvbsz", "", 200, -5, 5); 

  TH1F* h_n_all_tracks = new TH1F("h_n_all_tracks",  "", 40, 0, 2000);
  TH1F* h_n_seed_tracks = new TH1F("h_n_seed_tracks", "", 50, 0,  50);
  TH1F* h_n_seed_nosigcut_tracks = new TH1F("h_n_seed_nosigcut_tracks", "", 50, 0,  200);

  const char* par_names[6] = {"pt", "eta", "phi", "dxybs", "dxypv", "dz"};
  const int par_nbins[6] = { 50, 50, 50, 4000, 100, 80 };
  const double par_lo[6] = { 0, -2.5, -3.15, -0.2, -0.2, -20 };
  const double par_hi[6] = { 10,  2.5,  3.15,  0.2,  0.2,  20 };
  const double err_lo[6] = { 0 };
  const double err_hi[6] = { 0.15, 0.01, 0.01, 0.2, 0.2, 0.4 };

  TH1F* h_all_track_pars[6];
  TH1F* h_all_track_errs[6];
  TH2F* h_all_track_dxybs_v_pars[1][6];
  TH2F* h_all_track_dxyerr_v_pars[1][6];
  for (int i = 0; i < 6; ++i)
    h_all_track_pars[i] = new TH1F(TString::Format("h_all_track_%s", par_names[i]), "", par_nbins[i], par_lo[i], par_hi[i]);
  for (int i = 0; i < 6; ++i) 
    h_all_track_errs[i] = new TH1F(TString::Format("h_all_track_err%s", par_names[i]), "", par_nbins[i], err_lo[i], err_hi[i]);
  for (int i = 0; i < 6; ++i) 
    h_all_track_dxybs_v_pars[0][i] = new TH2F(TString::Format("h_all_track_dxybs_v_%s", par_names[i]), "", par_nbins[i], par_lo[i], par_hi[i], par_nbins[3], par_lo[3], par_hi[3]);
  for (int i = 0; i < 6; ++i) 
    h_all_track_dxyerr_v_pars[0][i] = new TH2F(TString::Format("h_all_track_dxyerr_v_%s", par_names[i]), "", par_nbins[i], err_lo[i], err_hi[i], par_nbins[3], par_lo[3], par_hi[3]);
  TH2F* h_all_track_eta_v_phi[1][1];
  h_all_track_eta_v_phi[0][0] = new TH2F("h_all_track_eta_v_phi", "", par_nbins[2], par_lo[2], par_hi[2], par_nbins[1], par_lo[1], par_hi[1]);
  TH1F* h_all_track_nhits = new TH1F("h_all_track_nhits", "",  40, 0, 40);
  TH1F* h_all_track_sigmadxybs = new TH1F("h_all_track_sigmadxybs", "", 1000, -10, 10);

  TH1F* h_seed_track_pars[6];
  TH1F* h_seed_track_errs[6];
  TH2F* h_seed_track_dxybs_v_pars[1][6];
  TH2F* h_seed_track_dxyerr_v_pars[1][6];
  for (int i = 0; i < 6; ++i) 
    h_seed_track_pars[i] = new TH1F(TString::Format("h_seed_track_%s", par_names[i]), "", par_nbins[i], par_lo[i], par_hi[i]);
  for (int i = 0; i < 6; ++i) 
    h_seed_track_errs[i] = new TH1F(TString::Format("h_seed_track_err%s", par_names[i]), "", par_nbins[i], err_lo[i], err_hi[i]);
  for (int i = 0; i < 6; ++i) 
    h_seed_track_dxybs_v_pars[0][i] = new TH2F(TString::Format("h_seed_track_dxybs_v_%s", par_names[i]), "", par_nbins[i], par_lo[i], par_hi[i], par_nbins[3], par_lo[3], par_hi[3]);
  for (int i = 0; i < 6; ++i) 
    h_seed_track_dxyerr_v_pars[0][i] = new TH2F(TString::Format("h_seed_track_dxyerr_v_%s", par_names[i]), "", par_nbins[i], err_lo[i], err_hi[i], par_nbins[3], par_lo[3], par_hi[3]);
  TH2F* h_seed_track_eta_v_phi[1][1];
  h_seed_track_eta_v_phi[0][0] = new TH2F("h_seed_track_eta_v_phi", "", par_nbins[2], par_lo[2], par_hi[2], par_nbins[1], par_lo[1], par_hi[1]);
  TH1F* h_seed_track_nhits = new TH1F("h_seed_track_nhits", "", 40, 0, 40);
  TH1F* h_seed_track_sigmadxybs = new TH1F("h_seed_track_sigmadxybs", "", 200, -10, 10);

  TH1F* h_seed_nosigcut_track_pars[6];
  TH1F* h_seed_nosigcut_track_errs[6];
  TH2F* h_seed_nosigcut_track_dxybs_v_pars[1][6];
  TH2F* h_seed_nosigcut_track_dxyerr_v_pars[1][6];
  for (int i = 0; i < 6; ++i) 
    h_seed_nosigcut_track_pars[i] = new TH1F(TString::Format("h_seed_nosigcut_track_%s", par_names[i]), "", par_nbins[i], par_lo[i], par_hi[i]);
  for (int i = 0; i < 6; ++i) 
    h_seed_nosigcut_track_errs[i] = new TH1F(TString::Format("h_seed_nosigcut_track_err%s", par_names[i]), "", par_nbins[i], err_lo[i], err_hi[i]); 
  for (int i = 0; i < 6; ++i) 
    h_seed_nosigcut_track_dxybs_v_pars[0][i] = new TH2F(TString::Format("h_seed_nosigcut_track_dxybs_v_%s", par_names[i]), "", par_nbins[i], par_lo[i], par_hi[i], par_nbins[3], par_lo[3], par_hi[3]);
  for (int i = 0; i < 6; ++i) 
    h_seed_nosigcut_track_dxyerr_v_pars[0][i] = new TH2F(TString::Format("h_seed_nosigcut_track_dxyerr_v_%s", par_names[i]), "", par_nbins[i], err_lo[i], err_hi[i], par_nbins[3], par_lo[3], par_hi[3]);
  TH2F* h_seed_nosigcut_track_eta_v_phi[1][1];
  h_seed_nosigcut_track_eta_v_phi[0][0] = new TH2F("h_seed_nosigcut_track_eta_v_phi", "", par_nbins[2], par_lo[2], par_hi[2], par_nbins[1], par_lo[1], par_hi[1]);
  TH1F* h_seed_nosigcut_track_nhits = new TH1F("h_seed_nosigcut_track_nhits", "", 40, 0, 40);
  TH1F* h_seed_nosigcut_track_sigmadxybs = new TH1F("h_seed_nosigcut_track_sigmadxybs", "", 1000, -10, 10);

  for (const std::string& fn : fns) {
    std::cout << fn << std::endl;
    file_and_tree fat(fn.c_str());
    TrackingTree& nt = fat.nt;

    if (is_mc)
      h_norm->Fill(0.5, ((TH1F*)fat.f->Get("mcStat/h_sums"))->GetBinContent(1));

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

      for (int ipv = 0, ipve = nt.npvs(); ipv < ipve; ++ipv) {
 	const double pvbsx = nt.p_pv_x->at(ipv) - nt.bs_x;
	const double pvbsy = nt.p_pv_y->at(ipv) - nt.bs_y;
	const double pvbsz = nt.p_pv_z->at(ipv) - nt.bs_z;
	h_pvbsx->Fill(pvbsx, w);
	h_pvbsy->Fill(pvbsy, w);
	h_pvbsz->Fill(pvbsz, w);
      }

      for (int itk = 0, itke = nt.ntks(); itk < itke; ++itk) {
	const double pt = nt.p_tk_qpt->at(itk);
	const double sigmadxy = nt.p_tk_dxybs->at(itk) / nt.p_tk_err_dxy->at(itk);
	const int nhits = nt.p_tk_nsthit->at(itk);
	const int npxhits = nt.p_tk_npxhit->at(itk);

	const bool use = pt > min_all_track_pt && nhits >= min_all_track_nhits && npxhits >= min_all_track_npxhits && fabs(sigmadxy) > min_all_track_sigmadxy;
	const bool use_nosigcut = pt > min_all_track_pt && nhits >= min_all_track_nhits && npxhits >= min_all_track_npxhits;

	const double pars[6] = {pt, nt.p_tk_eta->at(itk), nt.p_tk_phi->at(itk), nt.p_tk_dxybs->at(itk), nt.p_tk_dxypv->at(itk), nt.p_tk_dz->at(itk)};
	const double errs[6] = {nt.p_tk_err_qpt->at(itk), nt.p_tk_err_eta->at(itk), nt.p_tk_err_phi->at(itk), nt.p_tk_err_dxy->at(itk), nt.p_tk_err_dxy->at(itk), nt.p_tk_err_dz->at(itk)};

	if (use) {
	  ++n_seed_tracks;
	  h_seed_track_eta_v_phi[0][0]->Fill(pars[2], pars[1], w);
	  h_seed_track_nhits->Fill(nhits, w);
	  h_seed_track_sigmadxybs->Fill(sigmadxy, w);
	}

	if (use_nosigcut) {
	  ++n_seed_nosigcut_tracks;
	  h_seed_nosigcut_track_eta_v_phi[0][0]->Fill(pars[2], pars[1], w);
	  h_seed_nosigcut_track_nhits->Fill(nhits, w);
	  h_seed_nosigcut_track_sigmadxybs->Fill(sigmadxy, w);
	}

	for (int i = 0; i < 6; ++i) {
	  h_all_track_pars[i]->Fill(pars[i], w);
	  h_all_track_errs[i]->Fill(errs[i], w);
	  h_all_track_dxybs_v_pars[0][i]->Fill(pars[i], pars[3], w);
	  h_all_track_dxyerr_v_pars[0][i]->Fill(errs[i], pars[3], w);
	  if (use) {
	    h_seed_track_pars[i]->Fill(pars[i], w);
	    h_seed_track_errs[i]->Fill(errs[i], w);
	    h_seed_track_dxybs_v_pars[0][i]->Fill(pars[i], pars[3], w);
	    h_seed_track_dxyerr_v_pars[0][i]->Fill(errs[i], pars[3], w);
	  }
	  if (use_nosigcut) {
	    h_seed_nosigcut_track_pars[i]->Fill(pars[i], w);
	    h_seed_nosigcut_track_errs[i]->Fill(errs[i], w); 
	    h_seed_nosigcut_track_dxybs_v_pars[0][i]->Fill(pars[i], pars[3], w);
	    h_seed_nosigcut_track_dxyerr_v_pars[0][i]->Fill(errs[i], pars[3], w);
	  }
	}
	
	h_all_track_eta_v_phi[0][0]->Fill(pars[2], pars[1], w);
	h_all_track_nhits->Fill(nhits, w);
        h_all_track_sigmadxybs->Fill(sigmadxy, w);
      }

      h_n_all_tracks->Fill(nt.ntks(), w);
      h_n_seed_tracks->Fill(n_seed_tracks, w);
      h_n_seed_nosigcut_tracks->Fill(n_seed_nosigcut_tracks, w);
    }

    printf("\r%li/%li\n", jj, jje);
  }

  f_out->Write();
  f_out->Close();
  delete f_out;
}
