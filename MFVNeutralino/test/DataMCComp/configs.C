#include <iostream>
#include <map>
#include <string>
#include <vector>
using namespace std;


const string trig = "bjet"; // "lep" or "bjet"

// Flags
const int perc_dat = 20; // Percent unblinded
const bool scale_mc_dn = true; // Scale MC down by perc_dat?
const bool scale = true;
const bool data_ax = true; // Use data or MC y-axis?
const bool scale_ratio = false; // When the ratio plot is calculated, use MC pre- or post-scale?
const bool overlay_sig = true; // Draw signal on top?
const bool scale_sig = true; // Scale signal to match data normalization?
const bool debug = true; // Print debug statements?

// Derived config globals. These are filled by init_configs(). This section does NOT compile right now
/*
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
*/


template <typename T>
T get_config_value(const map<string, T>& configs, const string& key, const string& config_name) {
  auto it = configs.find(key);
  if (it == configs.end()) {
    cerr << "ERROR: Missing key [" << key << "] in " << config_name << endl;
    cerr << "Available keys:";
    for (const auto& kv : configs) {
      cerr << " [" << kv.first << "]";
    }
    cerr << endl;
    throw std::out_of_range(config_name + " missing key " + key);
  }
  return it->second;
}


void init_configs(
    string& trig_tag, string& fn_root, string& dat_prefix, string& mc_prefix, string& sig_prefix, string& out_fn_tag,
    vector<string>& samplenames, vector<string>& samplelabels, vector<EColor>& linecolors, vector<int>& linecol_mods,
    vector<vector<string>>& signames, vector<vector<float>>& sigxsecs, vector<float>& sigBRs, vector<string>& siglabels, vector<EColor>& sigcolors, vector<int>& sigcol_mods
  ) {
  cout << "Initializing configs.C with trig = [" << trig << "]" << endl;

  trig_tag = (trig == "bjet") ? "Bjet" : "Lep";

  const map<string, string> fn_root_configs = {
    {"lep",  "/uscms/home/yuqingwu/nobackup/crabdirs/26-07-15-Histos_tag002Lepm-pT4GeVCut-VtxEtaDz-2DPlots/"},
    {"bjet", "/uscms/home/yuqingwu/nobackup/crabdirs/26-08-28-Histos_tag004BvetoLHTm-wJetInfo/"}
  };
  fn_root = get_config_value(fn_root_configs, trig, "fn_root_configs");

  const map<string, string> data_prefix_configs = {
    {"lep",  "Lepton_data_"},
    {"bjet", "Bjet_data_"}
  };
  dat_prefix = fn_root + get_config_value(data_prefix_configs, trig, "data_prefix_configs");

  mc_prefix = fn_root;
  sig_prefix = fn_root;

  const map<string, vector<string>> samplenames_configs = {
    {"lep", {
      "wjetstolnu_leptonpresel",
      "ttbar_leptonpresel",
      "dyjets_leptonpresel",
      "qcd_leptonpresel",
      "diboson_leptonpresel"
    }},
    {"bjet", {
      "ttbar_btagpresel",
      "qcd_btagpresel",
    }}
  };
  samplenames = get_config_value(samplenames_configs, trig, "samplenames_configs");

  const map<string, vector<string>> samplelabels_configs = {
    {"lep",  {"W+Jets", "TTbar", "DY+Jets", "QCD", "Diboson"}},
    {"bjet", {"TTbar", "QCD"}}
  };
  samplelabels = get_config_value(samplelabels_configs, trig, "samplelabels_configs");

  const map<string, vector<EColor>> linecolors_configs = {
    {"lep",  {kRed, kGreen, kBlue, kYellow, kMagenta}},
    {"bjet", {kGreen, kYellow}}
  };
  linecolors = get_config_value(linecolors_configs, trig, "linecolors_configs");

  const map<string, vector<int>> linecol_mods_configs = {
    {"lep",  {-6, -6, -3, -3, -5}},
    {"bjet", {-6, -3}}
  };
  linecol_mods = get_config_value(linecol_mods_configs, trig, "linecol_mods_configs");

  const map<string, vector<vector<string>>> signames_configs = {
    {"lep", {
      {
        "WplusHToSSTodddd_tau10mm_M55_",
        "WminusHToSSTodddd_tau10mm_M55_",
        "ZHToSSTodddd_tau10mm_M55_",
        "ggZHToSSTodddd_tau10mm_M55_"
      }
    }},
    {"bjet", {
      {
        "ggHToSSTodddd_tau1mm_M55_"
      }
    }}
  };
  signames = get_config_value(signames_configs, trig, "signames_configs");

  const map<string, vector<vector<float>>> sigxsecs_configs = {
    {"lep", {{
      3*(9.426e-02),
      3*(5.983e-02),
      3*(2.568e-02),
      3*(4.14e-03),
    }}},
    {"bjet", {{
      1e-2, // FIXME this isn't the right value
    }}}
  };
  sigxsecs = get_config_value(sigxsecs_configs, trig, "sigxsecs_configs");

  const map<string, vector<float>> sigBRs_configs = {
    {"lep",  {0.001}},
    {"bjet", {0.001}}
  };
  sigBRs = get_config_value(sigBRs_configs, trig, "sigBRs_configs");

  const map<string, vector<string>> siglabels_configs = {
    {"lep",  {"VH, 55GeV, 10mm"}},
    {"bjet", {"ggH, 55GeV, 1mm"}}
  };
  siglabels = get_config_value(siglabels_configs, trig, "siglabels_configs");

  const map<string, vector<EColor>> sigcolors_configs = {
    {"lep",  {kCyan}},
    {"bjet", {kCyan}}
  };
  sigcolors = get_config_value(sigcolors_configs, trig, "sigcolors_configs");

  const map<string, vector<int>> sigcol_mods_configs = {
    {"lep",  {-3}},
    {"bjet", {-3}}
  };
  sigcol_mods = get_config_value(sigcol_mods_configs, trig, "sigcol_mods_configs");

  out_fn_tag = "/uscms/home/yuqingwu/nobackup/DV-testing/26-08_BjetOverlay/" + trig_tag + "-OUT-PNG/";

  cout << "Loaded config:" << endl;
  cout << "  trig_tag = " << trig_tag << endl;
  cout << "  dat_prefix = " << dat_prefix << endl;
  cout << "  samplenames.size() = " << samplenames.size() << endl;
  cout << "  signames.size() = " << signames.size() << endl;
}


void init_override_exact_keys(map<string, map<string, vector<string>>>& override_exact_keys, const string str_suffix = "") {
  /*
  override_exact_keys: plotter will match these exact keys
  */

  // x axis
  override_exact_keys["h_met"]["x_axis"] = {"", "400"};
  override_exact_keys["h_metnomu"]["x_axis"] = {"", "400"};
  override_exact_keys["h_sv_all_track_pt"+str_suffix]["x_axis"] = {"", "50"};
  override_exact_keys["h_sv_all_track_pt_barrel"+str_suffix]["x_axis"] = {"", "50"};
  override_exact_keys["h_sv_all_track_pt_endcap"+str_suffix]["x_axis"] = {"", "50"};
  override_exact_keys["h_sv_all_track_pt_err"+str_suffix]["x_axis"] = {"", "1"};
  override_exact_keys["h_sv_all_track_pt_err_barrel"+str_suffix]["x_axis"] = {"", "1"};
  override_exact_keys["h_sv_all_track_pt_err_endcap"+str_suffix]["x_axis"] = {"", "1"};
  override_exact_keys["h_vertex_seed_track_pt"+str_suffix]["x_axis"] = {"", "50"};
  override_exact_keys["h_vertex_seed_track_pt_barrel"+str_suffix]["x_axis"] = {"", "50"};
  override_exact_keys["h_vertex_seed_track_pt_endcap"+str_suffix]["x_axis"] = {"", "50"};
  override_exact_keys["h_vertex_seed_track_p"+str_suffix]["x_axis"] = {"", "40"};
  override_exact_keys["h_vertex_seed_track_p_barrel"+str_suffix]["x_axis"] = {"", "40"};
  override_exact_keys["h_vertex_seed_track_p_endcap"+str_suffix]["x_axis"] = {"", "40"};
  override_exact_keys["h_vertex_seed_track_err_pt"+str_suffix]["x_axis"] = {"", "0.12"};
  override_exact_keys["h_vertex_seed_track_err_pt_barrel"+str_suffix]["x_axis"] = {"", "0.12"};
  override_exact_keys["h_vertex_seed_track_err_pt_endcap"+str_suffix]["x_axis"] = {"", "0.12"};
  override_exact_keys["h_sv_all_track_dxy"+str_suffix]["x_axis"] = {"", "0.4"};

  // Ratio limit corrections
  override_exact_keys["h_sv_all_track_dxy_err"+str_suffix]["ratio_ylim"] = {"1.0", ""};
  override_exact_keys["h_sv_all_track_dxy_err_barrel"+str_suffix]["ratio_ylim"] = {"1.0", ""};
  override_exact_keys["h_sv_all_track_dxy_err_endcap"+str_suffix]["ratio_ylim"] = {"1.0", ""};
}


void init_override_keys(map<string, map<string, vector<string>>>& override_keys) {
  /*
  override_keys: plotter will check if a substring matches
  */

  // EventHistos
  override_keys["_pt"]["x_axis"] = {"", "400"};
  override_keys["_energy"]["x_axis"] = {"", "600"};
  override_keys["_ht"]["x_axis"] = {"", "600"};
  override_keys["_iso"]["x_axis"] = {"", "0.2"};
  override_keys["_njets"]["x_axis"] = {"", "15"};
  override_keys["_n_vertex_seed_tracks"]["x_axis"] = {"", "40"};
  override_keys["_jet_nseedtrack"]["x_axis"] = {"", "20"};
  override_keys["_pvscore"]["x_axis"] = {"", "120e3"};
  override_keys["_pvsscore"]["x_axis"] = {"", "120"};
  override_keys["track_dxy_barrel"]["x_axis"] = {"", ""};
  override_keys["track_dxy_endcap"]["x_axis"] = {"", ""};
  override_keys["_absdxybs"]["x_axis"] = {"", "0.05"};
  // override_keys["_nsigmadxy"]["x_axis"] = {"-10", "10"}; // I forgot what this targeted, but it overrides _nsigmadxy
  override_keys["vertex_seed_track_nsigmadxy"]["x_axis"] = {"-50", "50"};
  override_keys["_dxybs"]["x_axis"] = {"", "0.05"};
  override_keys["_dxyerr"]["x_axis"] = {"", "0.03"};
  override_keys["_track_err_dxy"]["x_axis"] = {"", "0.03"};
  override_keys["_dxy_rescale_err"]["x_axis"] = {"", "0.03"};
  override_keys["_nlayers"]["x_axis"] = {"", "25"};
  override_keys["_nstlayers"]["x_axis"] = {"", "20"};
  override_keys["_nhits"]["x_axis"] = {"", "40"};
  override_keys["_nsthits"]["x_axis"] = {"", "30"};
  override_keys["_pvntracks"]["x_axis"] = {"", "120"};
  // override_keys["_dz"]["x_axis"] = {"-0.5", "0.5"}; // Also overrides seed_track_dz, err_dz
  override_keys["_track_err_dz"]["x_axis"] = {"", "0.12"};
  override_keys["_absdz"]["x_axis"] = {"", "0.2"};
  override_keys["_npv"]["x_axis"] = {"", "80"};
  override_keys["_pvrho"]["x_axis"] = {"", "0.015"};
  override_keys["_pvsrho"]["x_axis"] = {"", "0.05"};
  // VertexHistos
  override_keys["jetsntkp"]["x_axis"] = {"", "600"};
  override_keys["_tkonlyp"]["x_axis"] = {"", "200"};
  override_keys["tkmass"]["x_axis"] = {"", "600"};
  override_keys["_tkonlymass"]["x_axis"] = {"", "200"};
  override_keys["_eta_err"]["x_axis"] = {"", "0.006"};
  override_keys["_phi_err"]["x_axis"] = {"", "0.006"};
  override_keys["_bsbs2ddist"]["x_axis"] = {"", "1.0"};
  override_keys["_bs2derr"]["x_axis"] = {"", "0.01"};
  override_keys["_gen2derr"]["x_axis"] = {"", "0.02"};
  override_keys["_gen3derr"]["x_axis"] = {"", "0.04"};
  override_keys["pverr"]["x_axis"] = {"", "0.02"};
  override_keys["pv2derr"]["x_axis"] = {"", "0.015"};
  override_keys["_dxy_err"]["x_axis"] = {"", "0.02"};
  override_keys["sv_all_track_nsigmadxy"]["x_axis"] = {"0", "50"};
  override_keys["_refit_dist2"]["x_axis"] = {"", "0.4"};
  override_keys["_refit_dist3"]["x_axis"] = {"", "0.6"};
  override_keys["_refit_distz"]["x_axis"] = {"", "0.4"};
  override_keys["_maxdz"]["x_axis"] = {"", "5"};
  override_keys["_pvdz"]["x_axis"] = {"", "0.5"};

  // Ratio limit corrections
  override_keys["_jet_pt"]["ratio_ylim"] = {"0.5", ""};
  override_keys["_eta"]["ratio_ylim"] = {"0.3", ""};
  override_keys["_njets"]["ratio_ylim"] = {"2.0", ""};
  override_keys["_nbtags"]["ratio_ylim"] = {"1.0", ""};
  override_keys["_nsv"]["ratio_ylim"] = {"2.0", ""};
  override_keys["_n_vertex_seed_tracks"]["ratio_ylim"] = {"2.0", ""};
  override_keys["_jet_nseedtrack"]["ratio_ylim"] = {"0.4", ""};
  override_keys["track_dxy"]["ratio_ylim"] = {"0.8", ""};
  override_keys["_trackdxy"]["ratio_ylim"] = {"0.5", ""};
  override_keys["track_err_dxy"]["ratio_ylim"] = {"1.0", ""};
  override_keys["track_dxy_err"]["ratio_ylim"] = {"1.0", ""};
  override_keys["_nhits"]["ratio_ylim"] = {"0.8", ""};
  override_keys["_npxhits"]["ratio_ylim"] = {"0.8", ""};
  override_keys["_nsthits"]["ratio_ylim"] = {"0.8", ""};
  override_keys["_nlayers"]["ratio_ylim"] = {"0.8", ""};
  override_keys["_npxlayers"]["ratio_ylim"] = {"0.8", ""};
  override_keys["_nstlayers"]["ratio_ylim"] = {"0.8", ""};
  override_keys["_chi2"]["ratio_ylim"] = {"0.6", ""};
  override_keys["_seed_track_pt"]["ratio_ylim"] = {"1.0", ""};
  override_keys["_err_pt"]["ratio_ylim"] = {"0.8", ""};
  override_keys["_sumdbv"]["ratio_ylim"] = {"0.8", ""};
  override_keys["_bs2derr"]["ratio_ylim"] = {"0.4", ""};
  override_keys["_bs2dsig"]["ratio_ylim"] = {"0.4", ""};
  override_keys["_pv2ddist"]["ratio_ylim"] = {"0.5", ""};
  override_keys["_pv2derr"]["ratio_ylim"] = {"0.5", ""};
  override_keys["_pv2dsig"]["ratio_ylim"] = {"0.5", ""};
  override_keys["_pv3ddist"]["ratio_ylim"] = {"0.5", ""};
  override_keys["_pv3derr"]["ratio_ylim"] = {"0.5", ""};
  override_keys["_pv3dsig"]["ratio_ylim"] = {"0.5", ""};
  override_keys["_nsigmadxy"]["ratio_ylim"] = {"0.5", ""};

  // Y-axis
  override_keys["_seed_track_pt"]["y_axis"] = {"10", ""};
  override_keys["_sv_all_track_pt"]["y_axis"] = {"10", ""};
  override_keys["_phi"]["y_axis"] = {"0", ""};
  override_keys["ntkphi"]["y_axis"] = {"0", ""};
  override_keys["tkonlyphi"]["y_axis"] = {"0", ""};
  override_keys["_track_dz"]["y_axis"] = {"0", ""};
  override_keys["_pveta"]["y_axis"] = {"0", ""};

  // Log-y
  override_keys["_nbtags"]["log_y"] = {"true", ""};
  override_keys["_nsv"]["log_y"] = {"true", ""};
  override_keys["_track_pt"]["log_y"] = {"true", ""}; // This should catch _pt_err too
  // Move overflow
  //override_keys["_xxxxxx"]["overflow"] = {"false", ""};
}

