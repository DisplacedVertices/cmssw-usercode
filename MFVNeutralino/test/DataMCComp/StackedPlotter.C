#include "configs.C"
#include "apply_formatting.C"
#include "open_tfiles.C"
#include "sum_signal_hists.C"
#include "helper_functions.C"

#include <iostream>
using namespace std;


int make_plot(
    TFile*& f_dat, vector<TFile*>& tfiles, vector<vector<vector<TFile*>>>& fs_sig, const map<string, map<string, vector<string>>>& override_exact_keys, const map<string, map<string, vector<string>>>& override_keys, const string& yr, const string& ntrk, const string& fkey, const string& hname,
    const string& out_fn_tag,
    const vector<string>& samplelabels, const vector<EColor>& linecolors, const vector<int>& linecol_mods,
    const vector<vector<float>>& sigxsecs, const vector<float>& sigBRs, const vector<string>& siglabels, const vector<EColor>& sigcolors, const vector<int>& sigcol_mods
  ) {
  /*
  INPUTS:
  year, n-trk (e.g. "3or4"), file-key (e.g. "EventHistosOnlyOneVtx"), hist-loc (e.g. "jet_pt_medium")
  file-key = histType + variant
  */

  // Check flags
  assert(not( (not scale) && (scale_ratio) )); // Cannot use scaled ratio if MC isn't scaled
  assert(scale_mc_dn && data_ax && not(scale_ratio) && overlay_sig); // Prevents myself choosing stupid settings
  assert(not( (not scale_sig) && scale )); // I decided that if I'm looking at the original signal norm, MC should also be original. No reason, it just removes one set of plots no one looks at.

  string variant = fkey; // Because fkey is histType + variant
  if (fkey.find("EventHistos") == 0) variant = fkey.substr(11);
  if (fkey.find("VertexHistos") == 0) variant = fkey.substr(12);

  const int nbkg = samplelabels.size();
  const int nsig = siglabels.size();
  const EColor ratcol = kBlack;

  gStyle->SetOptStat(0); // Remove stats box
    
  // Initialize histograms and files
  vector<TH1F*> hists(nbkg);
  vector<TH1F*> hsigs(nsig);
  TH1F* h_dat = 0;
  TH1F* h_rat = 0;

  // Create stack, canvas, legend, and flags
  TCanvas* c_hs = new TCanvas("c_hs", "Stacked Canvas", 1600, 1600);
  TPad* dmc_pad = new TPad("datMC_pad", "Pad containing data vs MC", 0, 0.24, 1, 1);
  TPad* rat_pad = new TPad("ratio_pad", "Pad containing ratio", 0, 0, 1, 0.26);
  THStack* hs = new THStack("hs", "Stacked Data-MC Plot");
  TLegend* legend = new TLegend(0.65, 0.60, 0.88, 0.88);
  vector<TLine*> qt_lns_dat(2); // Quantiles
  vector<TLine*> qt_lns_mc(2);
  TLine* mn_ln_dat = new TLine(); // Mean
  TLine* mn_ln_mc = new TLine();
  TLine* rat_ln = new TLine(); // Ratio dotted line
  TLatex* tl = new TLatex();
  TLatex* perc_tl = new TLatex(); // For data percent
  TLatex* sig_tl = new TLatex(); // Signal scaling
  TLatex* brl_tl = new TLatex(); // Branch label (ex. 2017 PreSel)
  TLatex* rat_tl = new TLatex(); // Ratio label
  vector<TLatex*> tls = {tl, perc_tl, sig_tl, brl_tl, rat_tl};
  int ntl = tls.size(); // Number TLatex() objects
  
  // Make names
  const string hloc = "Ntk" + ntrk + "mfv" + fkey + "/" + hname;
  //if (debug) {cout << hloc << endl;};


  // Search overrides
  auto get_override = [&](const string& prop) {  
    auto it_exact = override_exact_keys.find(hname);
    if (it_exact != override_exact_keys.end()) {
      auto it_prop = it_exact->second.find(prop);
      if (it_prop != it_exact->second.end()) return it_prop->second;
    }
    for (const auto& kv : override_keys) {
      if (hloc.find(kv.first) != string::npos) {
        auto it = kv.second.find(prop);
        if (it != kv.second.end()) return it->second;
      }
    }
    return vector<string>{"", ""}; // <= 2 dof per override
  };
  vector<string> xaxis_settings = get_override("x_axis");
  vector<string> yaxis_settings = get_override("y_axis");
  vector<string> logy_settings = get_override("log_y");
  vector<string> raty_settings = get_override("ratio_ylim");
  vector<string> flow_settings = get_override("overflow");


  // Data draw
  h_dat = (TH1F*)f_dat->Get(hloc.c_str());
  // FORMAT Data
  format_h_dat(h_dat);


  // MC draw
  for (int i=0; i<nbkg; i++) {
    hists[i] = (TH1F*)tfiles[i]->Get(hloc.c_str());
    if (scale_mc_dn and perc_dat<100) {
      const float sf_dn = perc_dat/100.;
      hists[i]->Scale(sf_dn);
    };
    // FORMAT MC
    hists[i]->SetName(samplelabels[i].c_str()); // No effect
    hists[i]->SetFillColor(linecolors[i]+linecol_mods[i]);
    hists[i]->SetLineWidth(0);
    // MC draw
    hs->Add(hists[i]);
    legend->AddEntry(hists[i], samplelabels[i].c_str(), "f");
    if (debug) {cout << " hist " << i << " " << hists[i]->GetName() << endl;};
  }


  // Scaling
  double denom = 0.0;
  for (auto& h : hists) denom += h->Integral();
  const double scale_factor = h_dat->Integral() / denom;
  if (debug) {
    cout << "MC yield: " << denom << endl << "Data yield: " << h_dat->Integral() << endl << "Scale factor: " << scale_factor << endl;
  };
  if (scale && h_dat->Integral()!=0) {
    for (auto& h : hists) h->Scale(scale_factor);
  }


  // Stat uncertainty
  TH1* h_mc_stat = (TH1*)hs->GetStack()->Last()->Clone();
  format_mc_stat(h_mc_stat);
  gStyle->SetHatchesLineWidth(1);
  legend->AddEntry(h_mc_stat, "MC Stat", "f");


  // Data-MC ratio
  h_rat = (TH1F*)h_dat->Clone("h_rat");
  for (int i=1; i<=h_rat->GetNbinsX(); i++) {
    const float num = h_dat->GetBinContent(i);
    const float den = h_mc_stat->GetBinContent(i);
    const float ne = h_dat->GetBinError(i);
    const float de = h_mc_stat->GetBinError(i);
    if (num!=0 && den!=0) {
      const float ratio = num / den;
      h_rat->SetBinContent(i, ratio);
      h_rat->SetBinError(i, sqrt(ne*ne/(den*den) + num*num*de*de/(den*den*den*den)) );
    } else {
      h_rat->SetBinContent(i, 1.0); // Can also fill nan, 0, etc
      h_rat->SetBinError(i, 0.0);
    };
  };
  if (scale && not(scale_ratio) && h_dat->Integral()!=0) {
    h_rat->Scale(scale_factor);
  };
  // FORMAT Ratio
  const float ratio_font_scale = 3.; // Scale font by 3(?)
  format_rat(h_rat, h_dat, ratcol, ratio_font_scale);
  // Set bounds
  double rat_avg = 1.0; // What I expect the average ratio to be
  if (not scale_ratio && h_dat->Integral()!=0) {rat_avg = scale_factor;};
  double ratio_ylim = 0.50;
  if (raty_settings[0] != "") {ratio_ylim = max(ratio_ylim, stod(raty_settings[0]));};
  if (h_dat->Integral()!=0) {
    h_rat->SetMaximum( min(h_rat->GetBinContent(h_rat->GetMaximumBin())*(1+gStyle->GetHistTopMargin()), (1+ratio_ylim)*rat_avg) );
    h_rat->SetMinimum( max(max(h_rat->GetBinContent(h_rat->GetMinimumBin())*(1-gStyle->GetHistTopMargin()), (1-ratio_ylim)*rat_avg) , 0.0));
  };
  h_rat->GetYaxis()->SetNdivisions(1506, true);

  // Draw line for ratio average
  rat_ln->SetX1(h_rat->GetXaxis()->GetBinLowEdge(1));
  rat_ln->SetX2(h_rat->GetXaxis()->GetBinLowEdge(h_rat->GetXaxis()->GetNbins()+1));
  rat_ln->SetY1(rat_avg);
  rat_ln->SetY2(rat_avg);
  // FORMAT line
  format_rat_ln(rat_ln);


  // Signal draw
  if (overlay_sig) {
    for (int i=0; i<nsig; i++) {
      sum_signal_hists(hsigs[i], fs_sig[i], sigxsecs[i], sigBRs[i], yr, hloc);
      if (scale_sig) {
        if (h_dat->Integral()!=0) {
          hsigs[i]->Scale(h_dat->Integral() / hsigs[i]->Integral()); // Sig is scaled to data
        } else if (h_mc_stat->Integral()!=0) {
          hsigs[i]->Scale(h_mc_stat->Integral() / hsigs[i]->Integral());
        };
      };
      // FORMAT SIGNAL
      hsigs[i]->SetLineColor(sigcolors[i] + sigcol_mods[i]);
      hsigs[i]->SetFillColorAlpha(sigcolors[i] + sigcol_mods[i], 0.8);
      format_h_sig(hsigs[i]);
      // Signal draw
      legend->AddEntry(hsigs[i], siglabels[i].c_str(), "f");
    }
  }


  // Quantiles and mean
  const double qt_probs[2] = {0.16, 0.84};
  double qt_vals_dat[2] = {0, 0};
  double qt_vals_mc[2] = {0, 0};
  double mn_val_dat = 0;
  double mn_val_mc = 0;
  if (h_dat->Integral()!=0) {
    h_dat->GetQuantiles(2, qt_vals_dat, qt_probs);
    mn_val_dat = h_dat->GetMean();
  };
  if (h_mc_stat->Integral()!=0) {
    h_mc_stat->GetQuantiles(2, qt_vals_mc, qt_probs);
    mn_val_mc = h_mc_stat->GetMean();
  } // If all 0s, this will not make sense, but it's OK
    

  // Legend
  legend->AddEntry(h_dat, "Data", "lep");
  // Format Legend
  format_legend(legend);


  // Draw
  c_hs->cd();
  dmc_pad->Draw();
  dmc_pad->cd();
  if (data_ax) { // x- and y- limits are determined here
    h_dat->Draw();
    hs->Draw("histSAME");
  } else {
    hs->Draw("hist");
  }
  // FORMAT STACK
  hs->GetXaxis()->SetTitle(hists[0]->GetXaxis()->GetTitle());
  hs->GetYaxis()->SetTitle(hists[0]->GetYaxis()->GetTitle());

  if (overlay_sig) {
    for (int i=0; i<nsig; i++) {
      hsigs[i]->Draw("E2 SAME");
    }
  }

  // Stat uncertainty
  h_mc_stat->Draw("E2 SAME");

  h_dat->Draw("SAME");
  if (data_ax) { // Draw ticks one final time
    h_dat->Draw("axis SAME");
  } else {
    hs->Draw("axis SAME");
  }

  // Text
  for (auto& tlx : tls) { // Batch-format TLatex
    format_tlx(tlx);
  };
  rat_tl->SetTextSize(rat_tl->GetTextSize()*3); // Ratio text needs to be blown up
  if (tl) {
    if (scale) {
      tl->DrawLatex(0.66, 0.58, Form("Scale: %.3f", scale_factor));
    } else {
      tl->DrawLatex(0.66, 0.58, "Not Scaled");
    }
  }
  if (perc_tl) {
    perc_tl->DrawLatex(0.66, 0.48, ("Data %: " + to_string(perc_dat)).c_str());
  }
  if (overlay_sig) {
    string sig_txt = "";
    if (scale_sig) {
      sig_txt = "Sig Scaled to Data";
    }
    else {
      sig_txt = "Sig BR: " + to_string(sigBRs[0]*100).substr(0,5) + "%"; // FixMe: if more than one BR, need to sum
    }
    sig_tl->DrawLatex(0.66, 0.43, sig_txt.c_str()); 
  }
  if (brl_tl) {
    brl_tl->DrawLatex(0.66, 0.38, (yr + " " + variant).c_str());
  }


  // Draw ratio
  c_hs->cd();
  rat_pad->Draw();
  rat_pad->cd();
  h_rat->Draw("E1P");
  rat_ln->Draw("SAME");
  h_rat->Draw("SAME,E1P");
  if (scale_ratio) {
    rat_tl->DrawLatex(0.55, 0.82, "Scaled Data-MC Ratio");
  } else {
    rat_tl->DrawLatex(0.55, 0.82, "Unscaled Data-MC Ratio");
  }


  // Re-format using stylistic overrides
  // x axis
  if (xaxis_settings[0] != "" || xaxis_settings[1] != "") {
    double xmin = hs->GetXaxis()->GetXmin();
    double xmax = hs->GetXaxis()->GetXmax();
    if (xaxis_settings[0] != "" && stod(xaxis_settings[0]) > xmin) {
      xmin = stod(xaxis_settings[0]);
    }
    if (xaxis_settings[1] != "" && stod(xaxis_settings[1]) < xmax) {
      xmax = stod(xaxis_settings[1]);
    }
    hs->GetXaxis()->SetRangeUser(xmin, xmax);
    h_dat->GetXaxis()->SetRangeUser(xmin, xmax);
    h_rat->GetXaxis()->SetRangeUser(xmin, xmax);
    rat_ln->SetX1(xmin);
    rat_ln->SetX2(xmax);
  };
  // y axis
  // Set y-max so both plots are visible
  if (logy_settings[0] != "true") {
    const float new_max = max(hs->GetMaximum(), h_dat->GetMaximum()) * (1+gStyle->GetHistTopMargin());
    hs->SetMaximum(new_max);
    h_dat->SetMaximum(new_max);
  }
  else {
    const float new_max = max(hs->GetMaximum(), h_dat->GetMaximum()) * 2;
    hs->SetMaximum(new_max);
    h_dat->SetMaximum(new_max);
  };
  double dmc_ymin = 0.0;
  if (logy_settings[0] != "true") { dmc_ymin = max( min(h_dat->GetMinimum(), hs->GetMinimum()) *(1-gStyle->GetHistTopMargin()), -2.0);}
  else { dmc_ymin = max( min(h_dat->GetMinimum(), hs->GetMinimum()), 0.1) * 0.5;};
  hs->SetMinimum(dmc_ymin);
  h_dat->SetMinimum(dmc_ymin);
  if (yaxis_settings[0] != "" || yaxis_settings[1] != "") {
    if (yaxis_settings[0] != "" && not(logy_settings[0] == "true" && yaxis_settings[0] == "0")) { // Reject log-y because I often set blanket 0 y-axis
      hs->SetMinimum(stod(yaxis_settings[0]));
      h_dat->SetMinimum(stod(yaxis_settings[0]));
    };
    if (yaxis_settings[1] != "") {
      hs->SetMaximum(stod(yaxis_settings[1]));
      h_dat->SetMaximum(stod(yaxis_settings[1]));
    };
  };
  // log-scale y
  if (logy_settings[0] == "true") {
    dmc_pad->SetLogy();
  }
  // Over- and underflow (should not affect quantiles, axes etc)
  if (flow_settings[0]!="false") {
    move_over_under_flows(h_dat);
    for (int i=0; i<nbkg; i++) {
      move_over_under_flows(hists[i]);
    }
    move_over_under_flows(h_mc_stat);
    hs->Modified(); // Need this line to render modification
  };



  // Draw quantiles
  for (int i=0; i<2; i++) {
    qt_lns_dat[i] = new TLine();
    qt_lns_dat[i]->SetX1(qt_vals_dat[i]);
    qt_lns_dat[i]->SetX2(qt_vals_dat[i]);
    qt_lns_dat[i]->SetY1(h_dat->GetMinimum());
    qt_lns_dat[i]->SetY2(h_dat->GetMaximum());
    format_qt_ln(qt_lns_dat[i], kBlack, false);
    qt_lns_mc[i] = new TLine();
    qt_lns_mc[i]->SetX1(qt_vals_mc[i]);
    qt_lns_mc[i]->SetX2(qt_vals_mc[i]);
    qt_lns_mc[i]->SetY1(h_dat->GetMinimum());
    qt_lns_mc[i]->SetY2(h_dat->GetMaximum());
    format_qt_ln(qt_lns_mc[i], kRed, false);
  }
  mn_ln_dat->SetX1(mn_val_dat);
  mn_ln_dat->SetX2(mn_val_dat);
  mn_ln_dat->SetY1(h_dat->GetMinimum());
  mn_ln_dat->SetY2(h_dat->GetMaximum());
  format_qt_ln(mn_ln_dat, kBlack, true);
  mn_ln_mc->SetX1(mn_val_mc);
  mn_ln_mc->SetX2(mn_val_mc);
  mn_ln_mc->SetY1(h_dat->GetMinimum());
  mn_ln_mc->SetY2(h_dat->GetMaximum());
  format_qt_ln(mn_ln_mc, kRed, true);
  // Draw
  dmc_pad->cd();
  for (int i=0; i<2; i++) {
    qt_lns_dat[i]->Draw("SAME");
    qt_lns_mc[i]->Draw("SAME");
  }
  mn_ln_mc->Draw("SAME");
  mn_ln_dat->Draw("SAME");
  legend->AddEntry(mn_ln_mc, "MC mean, 16/84%", "l");
  legend->AddEntry(mn_ln_dat, "Data mean, 16/84%", "l");
  
  // Update
  legend->Draw();
  dmc_pad->Update();
  rat_pad->Update();


  // Make file
  string out_dir = out_fn_tag + yr + "-" + variant;
  if (scale_sig) {out_dir += "-SigSc";}
  else {out_dir += "-SigUns";};
  out_dir += "/";
  gSystem->mkdir(out_dir.c_str(), true);
  // Make Output Filename
  string full_filename = out_dir + yr + "_" + ntrk + fkey;
  if (scale) {full_filename += "_scaled_";}
  else {full_filename += "_unscaled_";};
  full_filename += hname + ".png";
  if (debug) {cout << "Writing: " << full_filename << endl;};
  c_hs->SaveAs(full_filename.c_str());


  delete h_dat;
  delete hs;
  delete h_mc_stat;
  delete h_rat;
  delete rat_ln;
  delete mn_ln_dat;
  delete mn_ln_mc;
  delete dmc_pad;
  delete rat_pad;
  delete c_hs;
  delete legend;
  for (int i = 0; i < nbkg; ++i) {
    delete hists[i];
  }
  for (int i = 0; i < nsig; ++i) {
    delete hsigs[i];
  }
  for (int i = 0; i < ntl; ++i) {
    delete tls[i];
  }
  for (int i=0; i<2; i++) {
    delete qt_lns_dat[i];
    delete qt_lns_mc[i];
  }

  return 0;
}






void get_all_hnames(map<string, vector<string>>& hnames_by_histType, const vector<string>& histTypes, const string& yr, const string& ntrk, const string& variant, const string& dat_prefix, const string& dat_suffix, const vector<string>& match_keys = vector<string>());






int StackedPlotter() {
  // Initialize all config items (have tried putting these as global variables, it totally crashed, and I give up)
  string trig_tag;
  string fn_root;
  string dat_prefix;
  string dat_suffix = ".root";
  string mc_prefix;
  string mc_suffix = ".root";
  string sig_prefix;
  string sig_suffix = ".root";
  string out_fn_tag;
  vector<string> samplenames;
  vector<string> samplelabels;
  vector<EColor> linecolors;
  vector<int> linecol_mods;
  vector<vector<string>> signames;
  vector<vector<float>> sigxsecs;
  vector<float> sigBRs;
  vector<string> siglabels;
  vector<EColor> sigcolors;
  vector<int> sigcol_mods;

  init_configs(
    trig_tag, fn_root, dat_prefix, mc_prefix, sig_prefix, out_fn_tag,
    samplenames, samplelabels, linecolors, linecol_mods,
    signames, sigxsecs, sigBRs, siglabels, sigcolors, sigcol_mods
  );

  const vector<string> yrs = {"2016", "2017", "2018"};
  const vector<string> ntrks = {"3"};
  const vector<string> histTypes = {"EventHistos", "VertexHistos"};
  const vector<string> variants = {"PreSel", "OnlyOneVtx", "FullSel"};

  const bool make_all_TH1 = true; // If true, it makes all available TH1 objects


  map<string, vector<string>> hnames_by_histType;
  if (make_all_TH1) {
    // const vector<string> match_keys = {"h_vertex_seed_track_", "h_n_vertex_seed_tracks", "h_sv_all_track_", "_ptgt4"};
    get_all_hnames(hnames_by_histType, histTypes, yrs[0], ntrks[0], variants[0], dat_prefix, dat_suffix);
  } else {
    hnames_by_histType["EventHistos"] = {
      "h_jet_pt_0", "h_jet_phi_0",
      "h_nbtags_2", "h_nbtags_2", "h_vertex_seed_track_dxy"
    };
    hnames_by_histType["VertexHistos"] = {
      "h_sv_all_track_nsigmadxy",
    };
  };


  // Add custom formatting
  map<string, map<string, vector<string>>> override_exact_keys;
  const string str_suffix = ""; // sometimes I append suffixes to temporary modifications (e.g. "ptgt2p5")
  init_override_exact_keys(override_exact_keys, str_suffix);

  map<string, map<string, vector<string>>> override_keys;
  init_override_keys(override_keys);
  

  int nbkg = samplelabels.size();
  int nsig = siglabels.size();

  for (const auto& yr : yrs) {
    // Store Data-MC TFiles
    TFile* f_dat = new TFile();
    vector<TFile*> tfiles(nbkg);
    open_mc_dat_tfiles(f_dat, tfiles, yr, dat_prefix, dat_suffix, mc_prefix, mc_suffix, samplenames, true);

    // Store Signal TFiles
    vector<vector<vector<TFile*>>> fs_sig;
    open_sig_tfiles(fs_sig, yr, sig_prefix, sig_suffix, signames, true);
    
    for (const auto& histType : histTypes) {
      const auto& hnames = hnames_by_histType[histType];
      for (const auto& variant : variants) {
        const string fkey = histType + variant;
        for (const auto& ntrk : ntrks) {
          for (const auto& hname : hnames) {
            make_plot(
              f_dat, tfiles, fs_sig, override_exact_keys, override_keys, yr, ntrk, fkey, hname,
              out_fn_tag,
              samplelabels, linecolors, linecol_mods,
              sigxsecs, sigBRs, siglabels, sigcolors, sigcol_mods

            );
          }
        }
      }
    }

    delete f_dat;
    for (int i = 0; i < nbkg; ++i) {
      delete tfiles[i];
    }
    for (int i = 0; i < nsig; ++i) {
      for (int j = 0; j < fs_sig[i].size(); ++j) {
        for (int k = 0; k < fs_sig[i][j].size(); ++k) {
          delete fs_sig[i][j][k];
        }
      }
    }
  }
  return 0;
}






void get_all_hnames(map<string, vector<string>>& hnames_by_histType, const vector<string>& histTypes, const string& yr, const string& ntrk, const string& variant, const string& dat_prefix, const string& dat_suffix, const vector<string>& match_keys = vector<string>()) {
  // Get all available TH1* objects for this configuration
  const string fn = dat_prefix + yr + dat_suffix;

  TFile* f = TFile::Open(fn.c_str(), "READ");

  for (const auto& histType : histTypes) {
    const string dname = "Ntk" + ntrk + "mfv" + histType + variant;
    TDirectory* dir = (TDirectory*)f->Get(dname.c_str());
    TIter next(dir->GetListOfKeys());
    TKey* key;

    while ((key = (TKey*)next())) {
      string cname = key->GetClassName();
      string hname = key->GetName();
      if (cname.rfind("TH1", 0) == 0) {
        bool matched = match_keys.empty(); // Ask if it's in match_keys
        for (const auto& match_key : match_keys) {
          if (hname.find(match_key) != string::npos) {
            matched = true;
            break;
          }
        }
        if (matched) {
          hnames_by_histType[histType].push_back(key->GetName());
        }
      }
    }
  }

  delete f;
}


