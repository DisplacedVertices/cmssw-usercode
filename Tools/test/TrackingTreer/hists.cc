#include <fstream>
#include <iostream>
#include <string>
#include <vector>
#include "TFile.h"
#include "TH1.h"
#include "TTree.h"
#include "TVector2.h"
#include "JMTucker/Tools/interface/TrackingTree.h"
#include "utils.h"

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

  const double min_all_track_pt = 1;
  const double min_all_track_sigmadxy = 4;
  const int min_all_track_nhits = 8;
  const int min_all_track_npxhits = 2;
  
  TFile* f_out = new TFile(out_fn, "recreate");

  TH1F* h_norm = new TH1F("h_norm", "", 1, 0, 1);
  TH1F* h_npu = new TH1F("h_npu", "", 50, 0, 50);
  TH1F* h_tk_dxybs = new TH1F("h_tk_dxybs", "", 1000, -1, 1);
  TH1F* h_tk_sigmadxybs = new TH1F("h_tk_sigmadxybs", "", 1000, -10, 10);

  TH1F* h_n_all_tracks = new TH1F("h_n_all_tracks",  "", 40, 0, 2000);
  TH1F* h_all_track_pars[6];
  TH1F* h_all_track_errs[6];
  TH1F* h_all_track_nhits = new TH1F("h_all_track_nhits", "",  40, 0, 40);

  TH1F* h_n_seed_tracks = new TH1F("h_n_seed_tracks", "", 50, 0,  200);
  TH1F* h_seed_track_pars[6];
  TH1F* h_seed_track_errs[6];
  TH1F* h_seed_track_nhits = new TH1F("h_seed_track_nhits", "", 40, 0, 40);

  TH1F* h_n_seed_nosigcut_tracks = new TH1F("h_n_seed_nosigcut_tracks", "", 50, 0,  200);
  TH1F* h_seed_nosigcut_track_pars[6];
  TH1F* h_seed_nosigcut_track_errs[6];
  TH1F* h_seed_nosigcut_track_nhits = new TH1F("h_seed_nosigcut_track_nhits", "", 40, 0, 40);

  const char* par_names[6] = {"pt", "eta", "phi", "dxybs", "dxypv", "dz"};
  const int par_nbins[6] = { 50, 50, 50, 100, 100, 80 };
  const double par_lo[6] = { 0, -2.5, -3.15, -0.2, -0.2, -20 };
  const double par_hi[6] = { 10,  2.5,  3.15,  0.2,  0.2,  20 };
  const double err_lo[6] = { 0 };
  const double err_hi[6] = { 0.15, 0.01, 0.01, 0.2, 0.2, 0.4 };

  for (int i = 0; i < 6; ++i) {
    h_all_track_pars[i] = new TH1F(TString::Format("h_all_track_%s", par_names[i]), "", par_nbins[i], par_lo[i], par_hi[i]);
    h_all_track_errs[i] = new TH1F(TString::Format("h_all_track_err%s", par_names[i]), "", par_nbins[i], err_lo[i], err_hi[i]);
    h_seed_track_pars[i] = new TH1F(TString::Format("h_seed_track_%s", par_names[i]), "", par_nbins[i], par_lo[i], par_hi[i]);
    h_seed_track_errs[i] = new TH1F(TString::Format("h_seed_track_err%s", par_names[i]), "", par_nbins[i], err_lo[i], err_hi[i]);
    h_seed_nosigcut_track_pars[i] = new TH1F(TString::Format("h_seed_nosigcut_track_%s", par_names[i]), "", par_nbins[i], par_lo[i], par_hi[i]);
    h_seed_nosigcut_track_errs[i] = new TH1F(TString::Format("h_seed_nosigcut_track_err%s", par_names[i]), "", par_nbins[i], err_lo[i], err_hi[i]); 
  }

  for (const std::string& fn : fns) {
    std::cout << fn << std::endl;
    file_and_tree fat(fn.c_str());
    TrackingTree& nt = fat.nt;

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
      
      int n_seed_tracks = 0;
      int n_seed_nosigcut_tracks = 0;

      for (int itk = 0, itke = nt.ntks(); itk < itke; ++itk) {
	const double pt = nt.p_tk_qpt->at(itk);
	const double sigmadxy = nt.p_tk_dxybs->at(itk) / nt.p_tk_err_dxy->at(itk);
	const int nhits = nt.p_tk_nsthit->at(itk);
	const int npxhits = nt.p_tk_npxhit->at(itk);
	const bool use_nosigcut = pt > min_all_track_pt && nhits >= min_all_track_nhits && npxhits >= min_all_track_npxhits;
        const bool use = pt > min_all_track_pt && nhits >= min_all_track_nhits && npxhits >= min_all_track_npxhits && fabs(sigmadxy) > min_all_track_sigmadxy;

	const double pars[6] = {pt, nt.p_tk_eta->at(itk), nt.p_tk_phi->at(itk), nt.p_tk_dxybs->at(itk), nt.p_tk_dxypv->at(itk), nt.p_tk_dz->at(itk)};
	const double errs[6] = {nt.p_tk_err_qpt->at(itk), nt.p_tk_err_eta->at(itk), nt.p_tk_err_phi->at(itk), nt.p_tk_err_dxy->at(itk), nt.p_tk_err_dxy->at(itk), nt.p_tk_err_dz->at(itk)};

	if (use) 
	  ++n_seed_tracks;
	if (use_nosigcut)
	  ++n_seed_nosigcut_tracks;

	for (int i = 0; i < 6; ++i) {
	  h_all_track_pars[i]->Fill(pars[i]);
	  h_all_track_errs[i]->Fill(errs[i]);

	  if (use) {
	    h_seed_track_pars[i]->Fill(pars[i]);
	    h_seed_track_errs[i]->Fill(errs[i]);
	    h_seed_track_nhits->Fill(nhits);
	  }

	  if(use_nosigcut) {
	    h_seed_nosigcut_track_pars[i]->Fill(pars[i]);
	    h_seed_nosigcut_track_errs[i]->Fill(errs[i]); 
	    h_seed_nosigcut_track_nhits->Fill(nhits);
	  }
	}
       
	h_n_all_tracks->Fill(nt.ntks());
	h_all_track_nhits->Fill(nhits);
        h_tk_dxybs->Fill(nt.p_tk_dxybs->at(itk));
        h_tk_sigmadxybs->Fill(nt.p_tk_dxybs->at(itk) / nt.p_tk_err_dxy->at(itk));
      }

      h_n_seed_tracks->Fill(n_seed_tracks);
      h_n_seed_nosigcut_tracks->Fill(n_seed_nosigcut_tracks);
    }

    printf("\r%li/%li\n", jj, jje);
  }

  f_out->Write();
  f_out->Close();
  delete f_out;
}
