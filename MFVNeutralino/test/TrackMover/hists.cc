#include <cassert>
#include <iostream>
#include <boost/program_options.hpp>
#include "TH1.h"
#include "TH2.h"
#include "TFile.h"
#include "TTree.h"
#include "TVector2.h"
#include "TVector3.h"
#include "JMTucker/Tools/interface/LumiList.h"
#include "JMTucker/MFVNeutralino/interface/MovedTracksNtuple.h"
#include "BTagSFHelper.h"
#include "utils.h"

int main(int argc, char** argv) {
  std::string in_fn;
  std::string out_fn("hists.root");
  std::string tree_path("mfvMovedTree20/t");
  std::string json;
  int itau = 10000;
  bool apply_weights = true;
  bool btagsf_weights = false;
  bool pu_cross_weights = false;
  bool ntks_weights = false;

  {
    namespace po = boost::program_options;
    po::options_description desc("Allowed options");
    desc.add_options()
      ("help,h", "this help message")
      ("input-file,i",  po::value<std::string>(&in_fn),                                             "the input file (required)")
      ("output-file,o", po::value<std::string>(&out_fn)        ->default_value("hists.root"),       "the output file")
      ("tree-path,t",   po::value<std::string>(&tree_path)     ->default_value("mfvMovedTree20/t"), "the tree path")
      ("json,j",        po::value<std::string>(&json),                                              "lumi mask json file for data")
      ("tau",           po::value<int>        (&itau)          ->default_value(10000),              "tau in microns, for reweighting")
      ("weights",       po::value<bool>       (&apply_weights) ->default_value(true),               "whether to use any weights")
      ("btagsf",        po::value<bool>       (&btagsf_weights)->default_value(false),              "whether to use b-tag SF weights")
      ;

    po::variables_map vm;
    po::store(po::parse_command_line(argc, argv, desc), vm);
    po::notify(vm);

    if (vm.count("help")) {
      std::cout << desc << "\n";
      return 1;
    }

    if (in_fn == "") {
      std::cout << "value for --input-file is required\n" << desc << "\n";
      return 1;
    }

    if (tree_path.find("/") == std::string::npos) {
      tree_path += "/t";
      std::cout << "tree_path changed to " << tree_path << "\n";
    }
  }

  std::cout << argv[0] << " with options:"
            << " in_fn: " << in_fn
            << " out_fn: " << out_fn
            << " tree_path: " << tree_path
            << " json: " << (json != "" ? json : "none")
            << " tau: " << itau
            << " weights: " << apply_weights
            << " btagsf: " << btagsf_weights << "\n";

  ////
  const double pu_2017to2018[118] = { 0.8088707410249003, 0.6419315492929617, 1.0289843771164762, 1.2197433115877707, 2.0279361447384607, 2.1534273598348346, 2.828875717156401, 3.7562409631757463, 3.7723330080421347, 2.128823541813255, 1.4437282808060388, 1.0592335461744988, 0.9296008325854023, 0.8981341246581729, 0.8661838708148207, 0.8217817668661503, 0.7698094682358639, 0.736530117843042, 0.7324825824243237, 0.7464654505340651, 0.7689672475157527, 0.7962598319502678, 0.8238273378355885, 0.84709530856804, 0.8629571604669926, 0.8715575979660287, 0.8790646285472657, 0.8930068377451257, 0.9181154528911909, 0.9565916718906213, 1.0085885148613083, 1.0733677243858069, 1.1513074018453253, 1.2438041844310648, 1.350425854765928, 1.4667928985090142, 1.5852313012565622, 1.6964317350776834, 1.7888779559697383, 1.8463573710989412, 1.8483344785348048, 1.777156775240319, 1.6296890426047426, 1.4238791110873033, 1.192636304616271, 0.9691350867625012, 0.7752988582908152, 0.6194609177490059, 0.5004018080190712, 0.41258518896855334, 0.3496354676827754, 0.3057454957410425, 0.27651357625145984, 0.2587768794251079, 0.2503442053532996, 0.24978113594279056, 0.25620094485064937, 0.269077026686218, 0.2880879933617664, 0.31297537926425495, 0.34340097870928926, 0.37879522132496796, 0.4181914535828073, 0.46006239241614966, 0.5022042593864846, 0.5417448111098889, 0.5753590543126583, 0.599729908816729, 0.6121804339703449, 0.6112764589874742, 0.5971519453774672, 0.5714120667068647, 0.5366696442401658, 0.4959276770798611, 0.45203677112054097, 0.4073572740266353, 0.3636364273599529, 0.3220390572953875, 0.2832554359014485, 0.24762792649752466, 0.2152638164237845, 0.18612213801734914, 0.1600742314358133, 0.13694300589056346, 0.1165269986399804, 0.0986145541296668, 0.08299205921121872, 0.06944883162594205, 0.057780217187997036, 0.04778974199444527, 0.03929073201556682, 0.03210757396626401, 0.02607667588961756, 0.02104713973802034, 0.016881148969658692, 0.013454078923061686, 0.010654347125878181, 0.008383033422255411, 0.006553300860721036, 0.005089663013060519, 0.0039271342139648915, 0.0030102988351013078, 0.0022923603178735402, 0.001734152193216896, 0.0013032269067089236, 0.0009729254729590597, 0.0007215235730044382, 0.000531537519428578, 0.0003890108881886131, 0.0002828005460800867, 0.0002043072260251089, 0.00014647800144821486, 0.00010417815899462249, 7.364182160440637e-05, 5.127986461383892e-05, 3.7258169988485095e-05, 2.3663515932329523e-05, 1.4565424506047685e-05 };

  // from h_2_vtxntracks
  const double ntks_weight[60] = {  0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 1.674196, 1.550810, 1.459271, 1.284317, 1.187709, 1.231090, 1.242313, 1.145012, 1.182134, 1.114840, 1.093479, 0.964026, 1.039401, 0.940219, 0.907171, 0.976593, 0.918716, 0.904142, 0.867394, 0.777177, 0.814517, 0.799371, 0.829022, 0.834422, 0.609130, 0.599720, 0.726436, 0.570779, 0.677044, 0.590878, 0.540080, 0.490107, 0.561173, 0.464503, 0.537223, 0.414802, 0.426949, 0.173858, 0.267836, 0.725926, 0.237331, 0.201321, 0.121923, 0.311854, 0.193843, 0.995309, 0.000000, 0.000000, 0.000000, 0.559031, 0.810189, 0.000000, 0.000000, 0.000000 };

  const int itau_original = 10000; // JMTBAD if you change this in ntuple.py, change it here
  if (itau != itau_original)
    printf("reweighting tau distribution from %i um to %i um\n", itau_original, itau);
  const double o_tau_from = 10000./itau_original;
  const double o_tau_to = 10000./itau;

  std::unique_ptr<BTagSFHelper> btagsfhelper;
  if (btagsf_weights) btagsfhelper.reset(new BTagSFHelper);

  root_setup();

  file_and_tree fat(in_fn.c_str(), out_fn.c_str(), tree_path.c_str());
  TTree* t = fat.t;
  mfv::MovedTracksNtuple& nt = fat.nt;
  t->GetEntry(0);

  const bool is_mc = nt.run == 1;
  std::unique_ptr<jmt::LumiList> good_ll;
  if (!is_mc && json != "") good_ll.reset(new jmt::LumiList(json));

  TH1F* h_sums = is_mc ? ((TH1F*)fat.f->Get("mcStat/h_sums")) : 0;

  fat.f_out->mkdir("mfvWeight")->cd();
  fat.f->Get("mcStat/h_sums")->Clone("h_sums");
  fat.f_out->cd();

  TH1F* h_norm = new TH1F("h_norm", "", 1, 0, 1);
  if (is_mc)
    h_norm->Fill(0.5, h_sums->GetBinContent(1));

  TH1D* h_weight = new TH1D("h_weight", ";weight;events/0.01", 200, 0, 2);
  TH1D* h_btagsfweight = new TH1D("h_btagsfweight", ";weight;events/0.01", 200, 0, 2);
  TH1D* h_tau = new TH1D("h_tau", ";tau (cm);events/10 #mum", 10000, 0,10);
  TH1D* h_npu = new TH1D("h_npu", ";# PU;events/1", 100, 0, 100);

  const int num_numdens = 3;

  numdens nds[num_numdens] = {
    numdens("nocuts"),
    numdens("ntracks"),
    numdens("all")
  };

  enum { k_movedist2, k_movedist3, k_movevectoreta, k_npv, k_pvx, k_pvy, k_pvz, k_pvrho, k_pvntracks, k_pvsumpt2, k_ht, k_ntracks, k_nmovedtracks, k_npreseljets, k_npreselbjets, k_jetsume, k_jetdrmax, k_jetdravg, k_jetsumntracks, k_nvtxs }; 
  for (numdens& nd : nds) {
    nd.book(k_movedist2, "movedist2", ";movement 2-dist;events/0.01 cm", 200, 0, 2);
    nd.book(k_movedist3, "movedist3", ";movement 3-dist;events/0.01 cm", 200, 0, 2);
    nd.book(k_movevectoreta, "movevectoreta", ";move vector eta;events/0.08 cm", 100, -4, 4);
    nd.book(k_npv, "npv", ";# PV;events/1", 100, 0, 100);
    nd.book(k_pvx, "pvx", ";PV x (cm);events/1.5 #mum", 200, -0.015, 0.015);
    nd.book(k_pvy, "pvy", ";PV y (cm);events/1.5 #mum", 200, -0.015, 0.015);
    nd.book(k_pvz, "pvz", ";PV z (cm);events/0.24 cm", 200, -24, 24);
    nd.book(k_pvrho, "pvrho", ";PV #rho (cm);events/1 #mum", 200, 0, 0.02);
    nd.book(k_pvntracks, "pvntracks", ";PV # tracks;events/2", 200, 0, 400);
    nd.book(k_pvsumpt2, "pvsumpt2", ";PV #Sigma p_{T}^{2} (GeV^{2});events/200 GeV^{2}", 200, 0, 40000);
    nd.book(k_ht, "ht", ";H_{T} (GeV);events/50 GeV", 50, 0, 2500);
    nd.book(k_ntracks, "ntracks", ";# tracks;events/10", 200, 0, 2000);
    nd.book(k_nmovedtracks, "nmovedtracks", ";# moved tracks;events/2", 200, 0, 400);
    nd.book(k_npreseljets, "npreseljets", ";# preselected jets;events/1", 20, 0, 20);
    nd.book(k_npreselbjets, "npreselbjets", ";# preselected b jets;events/1", 20, 0, 20);
    nd.book(k_jetsume, "jetsume", ";#Sigma jet energy (GeV);events/5 GeV", 200, 0, 1000);
    nd.book(k_jetdrmax, "jetdrmax", ";max jet #Delta R;events/0.1", 70, 0, 7);
    nd.book(k_jetdravg, "jetdravg", ";avg jet #Delta R;events/0.1", 70, 0, 7);
    nd.book(k_jetsumntracks, "jetsumntracks", ";#Sigma jet # tracks;events/5", 200, 0, 1000);
    nd.book(k_nvtxs, "nvtxs", ";number of vertices;events/1", 8, 0, 8);
  }

  TH1D* h_vtxdbv[num_numdens] = {0};
  TH1D* h_vtxntracks[num_numdens] = {0};
  TH1D* h_vtxbs2derr[num_numdens] = {0};
  TH1D* h_vtxtkonlymass[num_numdens] = {0};
  TH1D* h_vtxs_mass[num_numdens] = {0};
  TH1D* h_vtxanglemax[num_numdens] = {0};
  TH1D* h_vtxphi[num_numdens] = {0};
  TH1D* h_vtxtheta[num_numdens] = {0};
  TH1D* h_vtxpt[num_numdens] = {0};
  TH2D* h_vtxbs2derr_v_vtxntracks[num_numdens] = {0};
  TH2D* h_vtxbs2derr_v_vtxtkonlymass[num_numdens] = {0};
  TH2D* h_vtxbs2derr_v_vtxanglemax[num_numdens] = {0};
  TH2D* h_vtxbs2derr_v_vtxphi[num_numdens] = {0};
  TH2D* h_vtxbs2derr_v_vtxtheta[num_numdens] = {0};
  TH2D* h_vtxbs2derr_v_vtxpt[num_numdens] = {0};
  TH2D* h_vtxbs2derr_v_vtxdbv[num_numdens] = {0};
  TH2D* h_vtxbs2derr_v_etamovevec[num_numdens] = {0};
  TH2D* h_vtxbs2derr_v_tksdxyerr[num_numdens] = {0};

  TH1D* h_tks_pt[num_numdens] = {0};
  TH1D* h_tks_eta[num_numdens] = {0};
  TH1D* h_tks_phi[num_numdens] = {0};
  TH1D* h_tks_dxy[num_numdens] = {0};
  TH1D* h_tks_dz[num_numdens] = {0};
  TH1D* h_tks_err_pt[num_numdens] = {0};
  TH1D* h_tks_err_eta[num_numdens] = {0};
  TH1D* h_tks_err_phi[num_numdens] = {0};
  TH1D* h_tks_err_dxy[num_numdens] = {0};
  TH1D* h_tks_err_dz[num_numdens] = {0};
  TH1D* h_tks_nsigmadxy[num_numdens] = {0};
  TH1D* h_tks_npxlayers[num_numdens] = {0};
  TH1D* h_tks_nstlayers[num_numdens] = {0};
  TH1D* h_tks_vtx[num_numdens] = {0};

  TH1D* h_vtx_tks_pt[num_numdens] = {0};
  TH1D* h_vtx_tks_eta[num_numdens] = {0};
  TH1D* h_vtx_tks_phi[num_numdens] = {0};
  TH1D* h_vtx_tks_dxy[num_numdens] = {0};
  TH1D* h_vtx_tks_dz[num_numdens] = {0};
  TH1D* h_vtx_tks_err_pt[num_numdens] = {0};
  TH1D* h_vtx_tks_err_eta[num_numdens] = {0};
  TH1D* h_vtx_tks_err_phi[num_numdens] = {0};
  TH1D* h_vtx_tks_err_dxy[num_numdens] = {0};
  TH1D* h_vtx_tks_err_dz[num_numdens] = {0};
  TH1D* h_vtx_tks_nsigmadxy[num_numdens] = {0};
  TH1D* h_vtx_tks_npxlayers[num_numdens] = {0};
  TH1D* h_vtx_tks_nstlayers[num_numdens] = {0};
  TH1D* h_vtx_tks_vtx[num_numdens] = {0};

  TH1D* h_vtx_tks_nomove_pt[num_numdens] = {0};
  TH1D* h_vtx_tks_nomove_eta[num_numdens] = {0};
  TH1D* h_vtx_tks_nomove_phi[num_numdens] = {0};
  TH1D* h_vtx_tks_nomove_dxy[num_numdens] = {0};
  TH1D* h_vtx_tks_nomove_dz[num_numdens] = {0};
  TH1D* h_vtx_tks_nomove_err_pt[num_numdens] = {0};
  TH1D* h_vtx_tks_nomove_err_eta[num_numdens] = {0};
  TH1D* h_vtx_tks_nomove_err_phi[num_numdens] = {0};
  TH1D* h_vtx_tks_nomove_err_dxy[num_numdens] = {0};
  TH1D* h_vtx_tks_nomove_err_dz[num_numdens] = {0};
  TH1D* h_vtx_tks_nomove_nsigmadxy[num_numdens] = {0};
  TH1D* h_vtx_tks_nomove_npxlayers[num_numdens] = {0};
  TH1D* h_vtx_tks_nomove_nstlayers[num_numdens] = {0};
  TH1D* h_vtx_tks_nomove_vtx[num_numdens] = {0};
  
  TH1D* h_moved_tks_pt[num_numdens] = {0};
  TH1D* h_moved_tks_eta[num_numdens] = {0};
  TH1D* h_moved_tks_phi[num_numdens] = {0};
  TH1D* h_moved_tks_dxy[num_numdens] = {0};
  TH1D* h_moved_tks_dz[num_numdens] = {0};
  TH1D* h_moved_tks_err_pt[num_numdens] = {0};
  TH1D* h_moved_tks_err_eta[num_numdens] = {0};
  TH1D* h_moved_tks_err_phi[num_numdens] = {0};
  TH1D* h_moved_tks_err_dxy[num_numdens] = {0};
  TH1D* h_moved_tks_err_dz[num_numdens] = {0};
  TH1D* h_moved_tks_nsigmadxy[num_numdens] = {0};
  TH1D* h_moved_tks_npxlayers[num_numdens] = {0};
  TH1D* h_moved_tks_nstlayers[num_numdens] = {0};
  TH1D* h_moved_tks_vtx[num_numdens] = {0};

  TH1D* h_moved_nosel_tks_pt[num_numdens] = {0};
  TH1D* h_moved_nosel_tks_eta[num_numdens] = {0};
  TH1D* h_moved_nosel_tks_phi[num_numdens] = {0};
  TH1D* h_moved_nosel_tks_dxy[num_numdens] = {0};
  TH1D* h_moved_nosel_tks_dz[num_numdens] = {0};
  TH1D* h_moved_nosel_tks_err_pt[num_numdens] = {0};
  TH1D* h_moved_nosel_tks_err_eta[num_numdens] = {0};
  TH1D* h_moved_nosel_tks_err_phi[num_numdens] = {0};
  TH1D* h_moved_nosel_tks_err_dxy[num_numdens] = {0};
  TH1D* h_moved_nosel_tks_err_dz[num_numdens] = {0};
  TH1D* h_moved_nosel_tks_nsigmadxy[num_numdens] = {0};
  TH1D* h_moved_nosel_tks_npxlayers[num_numdens] = {0};
  TH1D* h_moved_nosel_tks_nstlayers[num_numdens] = {0};
  TH1D* h_moved_nosel_tks_vtx[num_numdens] = {0};

  for (int i = 0; i < num_numdens; ++i) {
    h_vtxdbv[i] = new TH1D(TString::Format("h_%i_vtxdbv", i), ";d_{BV} of largest vertex (cm);events/50 #mum", 400, 0, 2);
    h_vtxntracks[i] = new TH1D(TString::Format("h_%i_vtxntracks", i), ";# tracks in largest vertex;events/1", 60, 0, 60);
    h_vtxbs2derr[i] = new TH1D(TString::Format("h_%i_vtxbs2derr", i), ";#sigma(d_{BV}) of largest vertex (cm);events/1 #mum", 500, 0, 0.05);
    h_vtxtkonlymass[i] = new TH1D(TString::Format("h_%i_vtxtkonlymass", i), ";track-only mass of largest vertex (GeV);events/1 GeV", 50, 0, 500);
    h_vtxs_mass[i] = new TH1D(TString::Format("h_%i_vtxs_mass", i), ";track+jets mass of largest vertex (GeV);events/1 GeV", 100, 0, 5000);
    h_vtxanglemax[i] = new TH1D(TString::Format("h_%i_vtxanglemax", i), ";biggest angle between pairs of tracks in vertex;events/0.03", 100, 0, M_PI);
    h_vtxphi[i] = new TH1D(TString::Format("h_%i_vtxphi", i), ";tracks-plus-jets-by-ntracks #phi of largest vertex;events/0.06", 100, -M_PI, M_PI);
    h_vtxtheta[i] = new TH1D(TString::Format("h_%i_vtxtheta", i), ";tracks-plus-jets-by-ntracks #theta of largest vertex; events/0.03", 100, 0, M_PI);
    h_vtxpt[i] = new TH1D(TString::Format("h_%i_vtxpt", i), ";tracks-plus-jets-by-ntracks p_{T} of largest vertex (GeV);events/1", 500, 0, 500);

    h_vtxbs2derr_v_vtxntracks[i] = new TH2D(TString::Format("h_%i_vtxbs2derr_v_vtxntracks", i), ";# tracks in largest vertex;#sigma(d_{BV}) of largest vertex (cm)", 60, 0, 60, 500, 0, 0.05);
    h_vtxbs2derr_v_vtxtkonlymass[i] = new TH2D(TString::Format("h_%i_vtxbs2derr_v_vtxtkonlymass", i), ";track-only mass of largest vertex (GeV);#sigma(d_{BV}) of largest vertex (cm)", 500, 0, 500, 500, 0, 0.05);
    h_vtxbs2derr_v_vtxanglemax[i] = new TH2D(TString::Format("h_%i_vtxbs2derr_v_vtxanglemax", i), ";biggest angle between pairs of tracks in vertex;#sigma(d_{BV}) of largest vertex (cm)", 100, 0, M_PI, 500, 0, 0.05);
    h_vtxbs2derr_v_vtxphi[i] = new TH2D(TString::Format("h_%i_vtxbs2derr_v_vtxphi", i), ";tracks-plus-jets-by-ntracks #phi of largest vertex;#sigma(d_{BV}) of largest vertex (cm)", 100, -M_PI, M_PI, 500, 0, 0.05);
    h_vtxbs2derr_v_vtxtheta[i] = new TH2D(TString::Format("h_%i_vtxbs2derr_v_vtxtheta", i), ";tracks-plus-jets-by-ntracks #theta of largest vertex;#sigma(d_{BV}) of largest vertex (cm)", 100, 0, M_PI, 500, 0, 0.05);
    h_vtxbs2derr_v_vtxpt[i] = new TH2D(TString::Format("h_%i_vtxbs2derr_v_vtxpt", i), ";tracks-plus-jets-by-ntracks p_{T} of largest vertex (GeV);#sigma(d_{BV}) of largest vertex (cm)", 500, 0, 500, 500, 0, 0.05);
    h_vtxbs2derr_v_vtxdbv[i] = new TH2D(TString::Format("h_%i_vtxbs2derr_v_vtxdbv", i), ";d_{BV} of largest vertex (cm);#sigma(d_{BV}) of largest vertex (cm)", 400, 0, 2, 500, 0, 0.05);
    h_vtxbs2derr_v_etamovevec[i] = new TH2D(TString::Format("h_%i_vtxbs2derr_v_etamovevec", i), ";eta of move vector;#sigma(d_{BV}) of largest vertex (cm)", 100, -4, 4, 500, 0, 0.05);
    h_vtxbs2derr_v_tksdxyerr[i] = new TH2D(TString::Format("h_%i_vtxbs2derr_v_tksdxyerr", i), ";track #sigma(dxy) in largest vertex (cm);#sigma(d_{BV}) of largest vertex (cm)", 100, 0, 0.1, 500, 0, 0.05);

    h_tks_pt[i] = new TH1D(TString::Format("h_%i_tks_pt", i), ";moved and selected track p_{T} (GeV);tracks/1 GeV", 200, 0, 200);
    h_tks_eta[i] = new TH1D(TString::Format("h_%i_tks_eta", i), ";moved and selected track #eta;tracks/0.16", 50, -4, 4);
    h_tks_phi[i] = new TH1D(TString::Format("h_%i_tks_phi", i), ";moved and selected track #phi;tracks/0.13", 50, -M_PI, M_PI);
    h_tks_dxy[i] = new TH1D(TString::Format("h_%i_tks_dxy", i), ";moved and selected track dxy;tracks/40 #mum", 200, -0.4, 0.4);
    h_tks_dz[i] = new TH1D(TString::Format("h_%i_tks_dz", i), ";moved and selected track dz;tracks/100 #mum", 200, -1, 1);
    h_tks_err_pt[i] = new TH1D(TString::Format("h_%i_tks_err_pt", i), ";moved and selected track #sigma(p_{T});tracks/0.01", 200, 0, 2);
    h_tks_err_eta[i] = new TH1D(TString::Format("h_%i_tks_err_eta", i), ";moved and selected track #sigma(#eta);tracks/0.0001", 200, 0, 0.02);
    h_tks_err_phi[i] = new TH1D(TString::Format("h_%i_tks_err_phi", i), ";moved and selected track #sigma(#phi);tracks/0.0001", 200, 0, 0.02);
    h_tks_err_dxy[i] = new TH1D(TString::Format("h_%i_tks_err_dxy", i), ";moved and selected track #sigma(dxy) (cm);tracks/0.001 cm", 100, 0, 0.1);
    h_tks_err_dz[i] = new TH1D(TString::Format("h_%i_tks_err_dz", i), ";moved and selected track #sigma(dz) (cm);tracks/0.001 cm", 100, 0, 0.1);
    h_tks_nsigmadxy[i] = new TH1D(TString::Format("h_%i_tks_nsigmadxy", i), ";moved and selected track n#sigma(dxy);tracks/0.1", 200, 0, 20);
    h_tks_npxlayers[i] = new TH1D(TString::Format("h_%i_tks_npxlayers", i), ";moved and selected track npxlayers;tracks/1", 20, 0, 20);
    h_tks_nstlayers[i] = new TH1D(TString::Format("h_%i_tks_nstlayers", i), ";moved and selected track nstlayers;tracks/1", 20, 0, 20);
    h_tks_vtx[i] = new TH1D(TString::Format("h_%i_tks_vtx", i), ";moved and selected track vertex-association index;tracks/1", 255, 0, 255);

    h_vtx_tks_pt[i] = new TH1D(TString::Format("h_%i_vtx_tks_pt", i), ";track p_{T} in largest vertex (GeV);tracks/1 GeV", 200, 0, 200);
    h_vtx_tks_eta[i] = new TH1D(TString::Format("h_%i_vtx_tks_eta", i), ";track #eta in largest vertex;tracks/0.16", 50, -4, 4);
    h_vtx_tks_phi[i] = new TH1D(TString::Format("h_%i_vtx_tks_phi", i), ";track #phi in largest vertex;tracks/0.13", 50, -M_PI, M_PI);
    h_vtx_tks_dxy[i] = new TH1D(TString::Format("h_%i_vtx_tks_dxy", i), ";track dxy in largest vertex;tracks/40 #mum", 200, -0.4, 0.4);
    h_vtx_tks_dz[i] = new TH1D(TString::Format("h_%i_vtx_tks_dz", i), ";track dz in largest vertex;tracks/100 #mum", 200, -1, 1);
    h_vtx_tks_err_pt[i] = new TH1D(TString::Format("h_%i_vtx_tks_err_pt", i), ";track #sigma(p_{T}) in largest vertex;tracks/0.01", 200, 0, 2);
    h_vtx_tks_err_eta[i] = new TH1D(TString::Format("h_%i_vtx_tks_err_eta", i), ";track #sigma(#eta) in largest vertex;tracks/0.0001", 200, 0, 0.02);
    h_vtx_tks_err_phi[i] = new TH1D(TString::Format("h_%i_vtx_tks_err_phi", i), ";track #sigma(#phi) in largest vertex;tracks/0.0001", 200, 0, 0.02);
    h_vtx_tks_err_dxy[i] = new TH1D(TString::Format("h_%i_vtx_tks_err_dxy", i), ";track #sigma(dxy) (cm) in largest vertex;tracks/0.001 cm", 100, 0, 0.1);
    h_vtx_tks_err_dz[i] = new TH1D(TString::Format("h_%i_vtx_tks_err_dz", i), ";track #sigma(dz) (cm) in largest vertex;tracks/0.001 cm", 100, 0, 0.1);
    h_vtx_tks_nsigmadxy[i] = new TH1D(TString::Format("h_%i_vtx_tks_nsigmadxy", i), ";track n#sigma(dxy) in largest vertex;tracks/0.1", 200, 0, 20);
    h_vtx_tks_npxlayers[i] = new TH1D(TString::Format("h_%i_vtx_tks_npxlayers", i), ";track npxlayers in largest vertex;tracks/1", 20, 0, 20);
    h_vtx_tks_nstlayers[i] = new TH1D(TString::Format("h_%i_vtx_tks_nstlayers", i), ";track nstlayers in largest vertex;tracks/1", 20, 0, 20);
    h_vtx_tks_vtx[i] = new TH1D(TString::Format("h_%i_vtx_tks_vtx", i), ";track vertex-association index in largest vertex;tracks/1", 255, 0, 255);

    h_vtx_tks_nomove_pt[i] = new TH1D(TString::Format("h_%i_vtx_tks_nomove_pt", i), ";track p_{T} in largest vertex but not moved (GeV);tracks/1 GeV", 200, 0, 200);
    h_vtx_tks_nomove_eta[i] = new TH1D(TString::Format("h_%i_vtx_tks_nomove_eta", i), ";track #eta in largest vertex but not moved;tracks/0.16", 50, -4, 4);
    h_vtx_tks_nomove_phi[i] = new TH1D(TString::Format("h_%i_vtx_tks_nomove_phi", i), ";track #phi in largest vertex but not moved;tracks/0.13", 50, -M_PI, M_PI);
    h_vtx_tks_nomove_dxy[i] = new TH1D(TString::Format("h_%i_vtx_tks_nomove_dxy", i), ";track dxy in largest vertex but not moved;tracks/40 #mum", 200, -0.4, 0.4);
    h_vtx_tks_nomove_dz[i] = new TH1D(TString::Format("h_%i_vtx_tks_nomove_dz", i), ";track dz in largest vertex but not moved;tracks/100 #mum", 200, -1, 1);
    h_vtx_tks_nomove_err_pt[i] = new TH1D(TString::Format("h_%i_vtx_tks_nomove_err_pt", i), ";track #sigma(p_{T}) in largest vertex but not moved;tracks/0.01", 200, 0, 2);
    h_vtx_tks_nomove_err_eta[i] = new TH1D(TString::Format("h_%i_vtx_tks_nomove_err_eta", i), ";track #sigma(#eta) in largest vertex but not moved;tracks/0.0001", 200, 0, 0.02);
    h_vtx_tks_nomove_err_phi[i] = new TH1D(TString::Format("h_%i_vtx_tks_nomove_err_phi", i), ";track #sigma(#phi) in largest vertex but not moved;tracks/0.0001", 200, 0, 0.02);
    h_vtx_tks_nomove_err_dxy[i] = new TH1D(TString::Format("h_%i_vtx_tks_nomove_err_dxy", i), ";track #sigma(dxy) (cm) in largest vertex but not moved;tracks/0.001 cm", 100, 0, 0.1);
    h_vtx_tks_nomove_err_dz[i] = new TH1D(TString::Format("h_%i_vtx_tks_nomove_err_dz", i), ";track #sigma(dz) (cm) in largest vertex but not moved;tracks/0.001 cm", 100, 0, 0.1);
    h_vtx_tks_nomove_nsigmadxy[i] = new TH1D(TString::Format("h_%i_vtx_tks_nomove_nsigmadxy", i), ";track n#sigma(dxy) in largest vertex but not moved;tracks/0.1", 200, 0, 20);
    h_vtx_tks_nomove_npxlayers[i] = new TH1D(TString::Format("h_%i_vtx_tks_nomove_npxlayers", i), ";track npxlayers in largest vertex but not moved;tracks/1", 20, 0, 20);
    h_vtx_tks_nomove_nstlayers[i] = new TH1D(TString::Format("h_%i_vtx_tks_nomove_nstlayers", i), ";track nstlayers in largest vertex but not moved;tracks/1", 20, 0, 20);
    h_vtx_tks_nomove_vtx[i] = new TH1D(TString::Format("h_%i_vtx_tks_nomove_vtx", i), ";track vertex-association index in largest vertex but not moved;tracks/1", 255, 0, 255);

    h_moved_tks_pt[i] = new TH1D(TString::Format("h_%i_moved_tks_pt", i), ";moved track p_{T} (GeV);tracks/1 GeV", 200, 0, 200);
    h_moved_tks_eta[i] = new TH1D(TString::Format("h_%i_moved_tks_eta", i), ";moved track #eta;tracks/0.16", 50, -4, 4);
    h_moved_tks_phi[i] = new TH1D(TString::Format("h_%i_moved_tks_phi", i), ";moved track #phi;tracks/0.13", 50, -M_PI, M_PI);
    h_moved_tks_dxy[i] = new TH1D(TString::Format("h_%i_moved_tks_dxy", i), ";moved track dxy;tracks/40 #mum", 200, -0.4, 0.4);
    h_moved_tks_dz[i] = new TH1D(TString::Format("h_%i_moved_tks_dz", i), ";moved track dz;tracks/100 #mum", 200, -1, 1);
    h_moved_tks_err_pt[i] = new TH1D(TString::Format("h_%i_moved_tks_err_pt", i), ";moved track #sigma(p_{T});tracks/0.01", 200, 0, 2);
    h_moved_tks_err_eta[i] = new TH1D(TString::Format("h_%i_moved_tks_err_eta", i), ";moved track #sigma(#eta);tracks/0.0001", 200, 0, 0.02);
    h_moved_tks_err_phi[i] = new TH1D(TString::Format("h_%i_moved_tks_err_phi", i), ";moved track #sigma(#phi);tracks/0.0001", 200, 0, 0.02);
    h_moved_tks_err_dxy[i] = new TH1D(TString::Format("h_%i_moved_tks_err_dxy", i), ";moved track #sigma(dxy) (cm);tracks/0.001 cm", 100, 0, 0.1);
    h_moved_tks_err_dz[i] = new TH1D(TString::Format("h_%i_moved_tks_err_dz", i), ";moved track #sigma(dz) (cm);tracks/0.001 cm", 100, 0, 0.1);
    h_moved_tks_nsigmadxy[i] = new TH1D(TString::Format("h_%i_moved_tks_nsigmadxy", i), ";moved track n#sigma(dxy);tracks/0.1", 200, 0, 20);
    h_moved_tks_npxlayers[i] = new TH1D(TString::Format("h_%i_moved_tks_npxlayers", i), ";moved track npxlayers;tracks/1", 20, 0, 20);
    h_moved_tks_nstlayers[i] = new TH1D(TString::Format("h_%i_moved_tks_nstlayers", i), ";moved track nstlayers;tracks/1", 20, 0, 20);
    h_moved_tks_vtx[i] = new TH1D(TString::Format("h_%i_moved_tks_vtx", i), ";moved track vertex-association index;tracks/1", 255, 0, 255);

    h_moved_nosel_tks_pt[i] = new TH1D(TString::Format("h_%i_moved_nosel_tks_pt", i), ";moved but not selected track p_{T} (GeV);tracks/1 GeV", 200, 0, 200);
    h_moved_nosel_tks_eta[i] = new TH1D(TString::Format("h_%i_moved_nosel_tks_eta", i), ";moved but not selected track #eta;tracks/0.16", 50, -4, 4);
    h_moved_nosel_tks_phi[i] = new TH1D(TString::Format("h_%i_moved_nosel_tks_phi", i), ";moved but not selected track #phi;tracks/0.13", 50, -M_PI, M_PI);
    h_moved_nosel_tks_dxy[i] = new TH1D(TString::Format("h_%i_moved_nosel_tks_dxy", i), ";moved but not selected track dxy;tracks/40 #mum", 200, -0.4, 0.4);
    h_moved_nosel_tks_dz[i] = new TH1D(TString::Format("h_%i_moved_nosel_tks_dz", i), ";moved but not selected track dz;tracks/100 #mum", 200, -1, 1);
    h_moved_nosel_tks_err_pt[i] = new TH1D(TString::Format("h_%i_moved_nosel_tks_err_pt", i), ";moved but not selected track #sigma(p_{T});tracks/0.01", 200, 0, 2);
    h_moved_nosel_tks_err_eta[i] = new TH1D(TString::Format("h_%i_moved_nosel_tks_err_eta", i), ";moved but not selected track #sigma(#eta);tracks/0.0001", 200, 0, 0.02);
    h_moved_nosel_tks_err_phi[i] = new TH1D(TString::Format("h_%i_moved_nosel_tks_err_phi", i), ";moved but not selected track #sigma(#phi);tracks/0.0001", 200, 0, 0.02);
    h_moved_nosel_tks_err_dxy[i] = new TH1D(TString::Format("h_%i_moved_nosel_tks_err_dxy", i), ";moved but not selected track #sigma(dxy) (cm);tracks/0.001 cm", 100, 0, 0.1);
    h_moved_nosel_tks_err_dz[i] = new TH1D(TString::Format("h_%i_moved_nosel_tks_err_dz", i), ";moved but not selected track #sigma(dz) (cm);tracks/0.001 cm", 100, 0, 0.1);
    h_moved_nosel_tks_nsigmadxy[i] = new TH1D(TString::Format("h_%i_moved_nosel_tks_nsigmadxy", i), ";moved but not selected track n#sigma(dxy);tracks/0.1", 200, 0, 20);
    h_moved_nosel_tks_npxlayers[i] = new TH1D(TString::Format("h_%i_moved_nosel_tks_npxlayers", i), ";moved but not selected track npxlayers;tracks/1", 20, 0, 20);
    h_moved_nosel_tks_nstlayers[i] = new TH1D(TString::Format("h_%i_moved_nosel_tks_nstlayers", i), ";moved but not selected track nstlayers;tracks/1", 20, 0, 20);
    h_moved_nosel_tks_vtx[i] = new TH1D(TString::Format("h_%i_moved_nosel_tks_vtx", i), ";moved but not selected track vertex-association index;tracks/1", 255, 0, 255);
  }

  double den = 0;
  std::map<std::string, double> nums;

  const std::vector<std::string> extra_weights_hists = {
    //"nocuts_npv_den",
    //"nocuts_pvz_den",
    //"nocuts_pvx_den",
    //"nocuts_pvy_den",
    //"nocuts_ntracks_den",
    //"nocuts_npv_den_redo"
    //"nocuts_ht_den",
    //"nocuts_pvntracks_den",
  };
  TFile* extra_weights = extra_weights_hists.size() > 0 ? TFile::Open("reweight.root") : 0;
  const bool use_extra_weights = extra_weights != 0 && extra_weights->IsOpen();
  printf("using extra weights from reweight.root? %i\n", use_extra_weights);

  long notskipped = 0, nden = 0, ndennegweight = 0, nnegweight = 0;
  double sumnegweightden = 0;

  for (long ej = 0, eje = t->GetEntries(); ej < eje; ++ej) {
    if (ej == 100000) break;
    if (t->LoadTree(ej) < 0) break;
    if (t->GetEntry(ej) <= 0) continue;
    if (ej % 250000 == 0) {
      fprintf(stderr, "\r%li/%li", ej, eje);
      fflush(stderr);
    }

    if (!is_mc && good_ll.get() && !good_ll->contains(nt))
      continue;

    ++notskipped;

    double w = 1;

    if (itau != 10000) {
      const double tau = nt.move_tau();
      const double tau_weight = o_tau_to/o_tau_from * exp((o_tau_from - o_tau_to) * tau);
      h_tau->Fill(tau, tau_weight);
      w *= tau_weight;
    }

    if (is_mc && apply_weights) {
      if (nt.weight < 0) ++nnegweight;
      w *= nt.weight;

      if (pu_cross_weights) {
	int inpu = int(nt.npu);
	w *= pu_2017to2018[inpu];
      }

      if (btagsf_weights) {
        double p_mc = 1, p_data = 1;

        for (size_t i = 0, ie = nt.nalljets(); i < ie; ++i) {
          const double pt = (*nt.p_alljets_pt)[i];
          const double eta = (*nt.p_alljets_eta)[i];
          const bool is_tagged = (*nt.p_alljets_bdisc)[i] > 0.935; // what ever
          const int hf = (*nt.p_alljets_hadronflavor)[i];

          const double sf = btagsfhelper->scale_factor(BTagSFHelper::BH, BTagSFHelper::tight, hf, eta, pt).v;
          const double e = btagsfhelper->efficiency(hf, eta, pt).v;
          assert(e > 0 && e <= 1);

          if (is_tagged) {
            p_mc   *= e;
            p_data *= e*sf;
          }
          else {
            p_mc   *= 1-e;
            p_data *= 1-e*sf;
          }
        }

        const double btagsfw = p_data / p_mc;
        h_btagsfweight->Fill(btagsfw);
        w *= btagsfw;
      }

      if (use_extra_weights) {
        for (const auto& name : extra_weights_hists) {
          TH1D* hw = (TH1D*)extra_weights->Get(name.c_str());
          assert(hw);
          const double v =
            name == "nocuts_npv_den" ? nt.npv :
            name == "nocuts_pvz_den" ? nt.pvz :
            name == "nocuts_pvx_den" ? nt.pvx :
            name == "nocuts_pvy_den" ? nt.pvy :
            name == "nocuts_ntracks_den" ? nt.ntracks :
            name == "nocuts_npv_den_redo" ? nt.npv :
            name == "nocuts_ht_den" ? nt.jetht :
            name == "nocuts_pvntracks_den" ? nt.pvntracks :
            -1e99;
          assert(v > -1e98);
          const int bin = hw->FindBin(v);
          if (bin >= 1 && bin <= hw->GetNbinsX())  
            w *= hw->GetBinContent(bin);
        }
      }
    }

    const TVector3 move_vector = nt.move_vector();
    const double movedist2 = move_vector.Perp();
    const double movedist3 = move_vector.Mag();
    const double movevectoreta = move_vector.Eta();

    const bool pass_trig = nt.pass_hlt & 1;

    double jet_sume = 0;
    double jet_drmax = 0;
    double jet_dravg = 0;
    double jet_sumntracks = 0;
    size_t nmovedjets = 0;
    for (size_t ijet = 0; ijet < nt.nalljets(); ++ijet) {
      if (nt.p_alljets_moved->at(ijet)) {
        ++nmovedjets;
        jet_sume += nt.p_alljets_energy->at(ijet);
        jet_sumntracks += nt.p_alljets_ntracks->at(ijet);

        for (size_t jjet = ijet+1; jjet < nt.nalljets(); ++jjet) {
          if (nt.p_alljets_moved->at(jjet)) {
            const double dr = nt.alljets_p4(ijet).DeltaR(nt.alljets_p4(jjet));
            jet_dravg += dr;
            if (dr > jet_drmax)
              jet_drmax = dr;
          }
        }
      }
    }
    jet_dravg /= nmovedjets * (nmovedjets - 1) / 2.;

    const size_t n_raw_vtx = nt.p_vtxs_x->size();
    std::vector<std::vector<int>> vtxs_tracks(n_raw_vtx);
    std::vector<double> vtxs_anglemax(n_raw_vtx, 0);

    for (size_t i = 0; i < n_raw_vtx; ++i) {
      vtxs_tracks[i] = nt.vtxs_tracks(i);

      for (int j = 0; j < (*nt.p_vtxs_ntracks)[i]; ++j) {
        const int jtrk = vtxs_tracks[i][j];
        const TVector3 jtrkp = nt.tks_p(jtrk);
        for (int k = j+1; k < (*nt.p_vtxs_ntracks)[i]; ++k) {
          const int ktrk = vtxs_tracks[i][k];
          const TVector3 ktrkp = nt.tks_p(ktrk);

          const double angle = jtrkp.Angle(ktrkp); // JMTBAD probably should tighten cuts on tracks used for this
          if (angle > vtxs_anglemax[i])
            vtxs_anglemax[i] = angle;
        }
      }
    }

    if (nt.jetht < 1200 ||
        nt.nalljets() < 4 ||
	!pass_trig || 
        movedist2 < 0.03 ||
        movedist2 > 2.0) {
      continue;
    }

    h_weight->Fill(w);
    h_npu->Fill(nt.npu, w);

    int n_pass_nocuts = 0;
    int n_pass_ntracks = 0;
    int n_pass_all = 0;

    std::vector<int> first_vtx_to_pass(num_numdens, -1);
    auto set_it_if_first = [](int& to_set, int to_set_to) { if (to_set == -1) to_set = to_set_to; };

    for (size_t ivtx = 0; ivtx < n_raw_vtx; ++ivtx) {
      const double dist2move = mag(nt.move_x - nt.p_vtxs_x->at(ivtx),
                                   nt.move_y - nt.p_vtxs_y->at(ivtx),
                                   nt.move_z - nt.p_vtxs_z->at(ivtx));
      if (dist2move > 0.0084)
        continue;

      const bool pass_ntracks = nt.p_vtxs_ntracks->at(ivtx) >= 5;
      const bool pass_bs2derr = nt.p_vtxs_bs2derr->at(ivtx) < 0.0025;

      if (1)                            { set_it_if_first(first_vtx_to_pass[0], ivtx); ++n_pass_nocuts;  }
      if (pass_ntracks)                 { set_it_if_first(first_vtx_to_pass[1], ivtx); ++n_pass_ntracks; }
      if (pass_ntracks && pass_bs2derr) { 
	set_it_if_first(first_vtx_to_pass[2], ivtx); 
	++n_pass_all;
	if (is_mc && apply_weights) {
	  if (ntks_weights) {
	    int ntks = nt.p_vtxs_ntracks->at(ivtx);
	    w *= ntks_weight[ntks];
	  }
	}
      }
    }

    auto Fill = [&w](TH1D* h, double v) { h->Fill(v, w); };

    for (numdens& nd : nds) {
      Fill(nd(k_movedist2)    .den, movedist2);
      Fill(nd(k_movedist3)    .den, movedist3);
      Fill(nd(k_movevectoreta).den, movevectoreta);
      Fill(nd(k_npv)          .den, nt.npv);
      Fill(nd(k_pvx)          .den, nt.pvx);
      Fill(nd(k_pvy)          .den, nt.pvy);
      Fill(nd(k_pvz)          .den, nt.pvz);
      Fill(nd(k_pvrho)        .den, mag(nt.pvx, nt.pvy));
      Fill(nd(k_pvntracks)    .den, nt.pvntracks);
      Fill(nd(k_pvsumpt2)     .den, nt.pvsumpt2);
      Fill(nd(k_ht)           .den, nt.jetht);
      Fill(nd(k_ntracks)      .den, nt.ntracks);
      Fill(nd(k_nmovedtracks) .den, nt.nmovedtracks);
      Fill(nd(k_npreseljets)  .den, nt.npreseljets);
      Fill(nd(k_npreselbjets) .den, nt.npreselbjets);
      Fill(nd(k_jetsume)      .den, jet_sume);
      Fill(nd(k_jetdrmax)     .den, jet_drmax);
      Fill(nd(k_jetdravg)     .den, jet_dravg);
      Fill(nd(k_jetsumntracks).den, jet_sumntracks);
      Fill(nd(k_nvtxs)        .den, nt.nvtxs());
    }

    ++nden;
    den += w;
    if (w < 0) { ++ndennegweight; sumnegweightden += w; }

    for (int i = 0; i < num_numdens; ++i) {
      int ivtx = first_vtx_to_pass[i];
      if (ivtx != -1) {
        h_vtxdbv[i]->Fill(mag(nt.p_vtxs_x->at(ivtx),
                              nt.p_vtxs_y->at(ivtx)));
        h_vtxntracks[i]->Fill(nt.p_vtxs_ntracks->at(ivtx), w);
        h_vtxbs2derr[i]->Fill(nt.p_vtxs_bs2derr->at(ivtx), w);
        h_vtxanglemax[i]->Fill(vtxs_anglemax[ivtx], w);
        h_vtxtkonlymass[i]->Fill(nt.p_vtxs_tkonlymass->at(ivtx), w);
        h_vtxs_mass[i]->Fill(nt.p_vtxs_mass->at(ivtx), w);
	h_vtxphi[i]->Fill(nt.p_vtxs_phi->at(ivtx), w);
	h_vtxtheta[i]->Fill(nt.p_vtxs_theta->at(ivtx), w);
	h_vtxpt[i]->Fill(nt.p_vtxs_pt->at(ivtx), w);
	h_vtxbs2derr_v_vtxntracks[i]->Fill(nt.p_vtxs_ntracks->at(ivtx), nt.p_vtxs_bs2derr->at(ivtx), w);
	h_vtxbs2derr_v_vtxtkonlymass[i]->Fill(nt.p_vtxs_tkonlymass->at(ivtx), nt.p_vtxs_bs2derr->at(ivtx), w);
	h_vtxbs2derr_v_vtxanglemax[i]->Fill(vtxs_anglemax[ivtx], nt.p_vtxs_bs2derr->at(ivtx), w);
	h_vtxbs2derr_v_vtxphi[i]->Fill(nt.p_vtxs_phi->at(ivtx), nt.p_vtxs_bs2derr->at(ivtx), w);
	h_vtxbs2derr_v_vtxtheta[i]->Fill(nt.p_vtxs_theta->at(ivtx), nt.p_vtxs_bs2derr->at(ivtx), w);
	h_vtxbs2derr_v_vtxpt[i]->Fill(nt.p_vtxs_pt->at(ivtx), nt.p_vtxs_bs2derr->at(ivtx), w);
	h_vtxbs2derr_v_vtxdbv[i]->Fill(mag(nt.p_vtxs_x->at(ivtx),nt.p_vtxs_y->at(ivtx)), nt.p_vtxs_bs2derr->at(ivtx), w);
	h_vtxbs2derr_v_etamovevec[i]->Fill(move_vector.Eta(), nt.p_vtxs_bs2derr->at(ivtx), w);

	for (size_t itk = 0; itk < nt.ntks(); itk++) {
	  if (nt.p_tks_vtx->at(itk) == ivtx) {
	    h_vtx_tks_pt[i]->Fill(nt.tks_pt(itk), w);
	    h_vtx_tks_eta[i]->Fill(nt.p_tks_eta->at(itk), w);
	    h_vtx_tks_phi[i]->Fill(nt.p_tks_phi->at(itk), w);
	    h_vtx_tks_dxy[i]->Fill(nt.p_tks_dxy->at(itk), w);
	    h_vtx_tks_dz[i]->Fill(nt.p_tks_dz->at(itk), w);
	    h_vtx_tks_err_pt[i]->Fill(nt.p_tks_err_pt->at(itk), w);
	    h_vtx_tks_err_eta[i]->Fill(nt.p_tks_err_eta->at(itk), w);
	    h_vtx_tks_err_phi[i]->Fill(nt.p_tks_err_phi->at(itk), w);
	    h_vtx_tks_err_dxy[i]->Fill(nt.p_tks_err_dxy->at(itk), w);
	    h_vtx_tks_err_dz[i]->Fill(nt.p_tks_err_dz->at(itk), w);
	    h_vtx_tks_nsigmadxy[i]->Fill(fabs(nt.p_tks_dxy->at(itk) / nt.p_tks_err_dxy->at(itk)), w);
	    h_vtx_tks_npxlayers[i]->Fill(nt.tks_npxlayers(itk), w);
	    h_vtx_tks_nstlayers[i]->Fill(nt.tks_nstlayers(itk), w);
	    h_vtx_tks_vtx[i]->Fill(nt.p_tks_vtx->at(itk), w);

	    double largest_dxyerr = nt.p_tks_err_dxy->at(itk);
	    for (size_t jtk = itk+1; jtk < nt.ntks(); jtk++) {
	      if ((nt.p_tks_vtx->at(jtk) == ivtx) && (nt.p_tks_err_dxy->at(jtk) > nt.p_tks_err_dxy->at(itk)))
		largest_dxyerr = nt.p_tks_err_dxy->at(jtk);
	    }
	    h_vtxbs2derr_v_tksdxyerr[i]->Fill(largest_dxyerr, nt.p_vtxs_bs2derr->at(ivtx), w);

	    if (!nt.p_tks_moved->at(itk)) {
	      h_vtx_tks_nomove_pt[i]->Fill(nt.tks_pt(itk), w);
	      h_vtx_tks_nomove_eta[i]->Fill(nt.p_tks_eta->at(itk), w);
	      h_vtx_tks_nomove_phi[i]->Fill(nt.p_tks_phi->at(itk), w);
	      h_vtx_tks_nomove_dxy[i]->Fill(nt.p_tks_dxy->at(itk), w);
	      h_vtx_tks_nomove_dz[i]->Fill(nt.p_tks_dz->at(itk), w);
	      h_vtx_tks_nomove_err_pt[i]->Fill(nt.p_tks_err_pt->at(itk), w);
	      h_vtx_tks_nomove_err_eta[i]->Fill(nt.p_tks_err_eta->at(itk), w);
	      h_vtx_tks_nomove_err_phi[i]->Fill(nt.p_tks_err_phi->at(itk), w);
	      h_vtx_tks_nomove_err_dxy[i]->Fill(nt.p_tks_err_dxy->at(itk), w);
	      h_vtx_tks_nomove_err_dz[i]->Fill(nt.p_tks_err_dz->at(itk), w);
	      h_vtx_tks_nomove_nsigmadxy[i]->Fill(fabs(nt.p_tks_dxy->at(itk) / nt.p_tks_err_dxy->at(itk)), w);
	      h_vtx_tks_nomove_npxlayers[i]->Fill(nt.tks_npxlayers(itk), w);
	      h_vtx_tks_nomove_nstlayers[i]->Fill(nt.tks_nstlayers(itk), w);
	      h_vtx_tks_nomove_vtx[i]->Fill(nt.p_tks_vtx->at(itk), w);
	    }
	  }
	}
      }
    }

    if (n_pass_nocuts)  nums["nocuts"]  += w;
    if (n_pass_ntracks) nums["ntracks"] += w;
    if (n_pass_all)     nums["all"]     += w;

    const int passes[num_numdens] = {
      n_pass_nocuts,
      n_pass_ntracks,
      n_pass_all
    };

    for (int i = 0; i < num_numdens; ++i) {
      if (passes[i]) {
        numdens& nd = nds[i];
        Fill(nd(k_movedist2)    .num, movedist2);
        Fill(nd(k_movedist3)    .num, movedist3);
        Fill(nd(k_movevectoreta).num, movevectoreta);
        Fill(nd(k_npv)          .num, nt.npv);
        Fill(nd(k_pvx)          .num, nt.pvx);
        Fill(nd(k_pvy)          .num, nt.pvy);
        Fill(nd(k_pvz)          .num, nt.pvz);
        Fill(nd(k_pvrho)        .num, mag(nt.pvx, nt.pvy));
        Fill(nd(k_pvntracks)    .num, nt.pvntracks);
        Fill(nd(k_pvsumpt2)     .num, nt.pvsumpt2);
        Fill(nd(k_ht)           .num, nt.jetht);
        Fill(nd(k_ntracks)      .num, nt.ntracks);
        Fill(nd(k_nmovedtracks) .num, nt.nmovedtracks);
        Fill(nd(k_npreseljets)  .num, nt.npreseljets);
        Fill(nd(k_npreselbjets) .num, nt.npreselbjets);
        Fill(nd(k_jetsume)      .num, jet_sume);
        Fill(nd(k_jetdrmax)     .num, jet_drmax);
        Fill(nd(k_jetdravg)     .num, jet_dravg);
        Fill(nd(k_jetsumntracks).num, jet_sumntracks);
        Fill(nd(k_nvtxs)        .num, passes[i]);

	for (size_t itk = 0; itk < nt.ntks(); itk++) {
	  const float pt = nt.tks_pt(itk);
	  const float dxy = nt.p_tks_dxy->at(itk);
	  const float dxyerr = nt.p_tks_err_dxy->at(itk);
	  const float nsigmadxy = fabs(dxy / dxyerr);
	  const float npxlay = nt.tks_npxlayers(itk);
	  const float nstlay = nt.tks_nstlayers(itk);

	  h_tks_pt[i]->Fill(pt, w);
	  h_tks_eta[i]->Fill(nt.p_tks_eta->at(itk), w);
	  h_tks_phi[i]->Fill(nt.p_tks_phi->at(itk), w);
	  h_tks_dxy[i]->Fill(dxy, w);
	  h_tks_dz[i]->Fill(nt.p_tks_dz->at(itk), w);
	  h_tks_err_pt[i]->Fill(nt.p_tks_err_pt->at(itk), w);
	  h_tks_err_eta[i]->Fill(nt.p_tks_err_eta->at(itk), w);
	  h_tks_err_phi[i]->Fill(nt.p_tks_err_phi->at(itk), w);
	  h_tks_err_dxy[i]->Fill(dxyerr, w);
	  h_tks_err_dz[i]->Fill(nt.p_tks_err_dz->at(itk), w);
	  h_tks_nsigmadxy[i]->Fill(nsigmadxy, w);
	  h_tks_npxlayers[i]->Fill(npxlay, w);
	  h_tks_nstlayers[i]->Fill(nstlay, w);
	  h_tks_vtx[i]->Fill(nt.p_tks_vtx->at(itk), w);

	  if (nt.p_tks_moved->at(itk)) {
	    h_moved_tks_pt[i]->Fill(pt, w);
	    h_moved_tks_eta[i]->Fill(nt.p_tks_eta->at(itk), w);
	    h_moved_tks_phi[i]->Fill(nt.p_tks_phi->at(itk), w);
	    h_moved_tks_dxy[i]->Fill(dxy, w);
	    h_moved_tks_dz[i]->Fill(nt.p_tks_dz->at(itk), w);
	    h_moved_tks_err_pt[i]->Fill(nt.p_tks_err_pt->at(itk), w);
	    h_moved_tks_err_eta[i]->Fill(nt.p_tks_err_eta->at(itk), w);
	    h_moved_tks_err_phi[i]->Fill(nt.p_tks_err_phi->at(itk), w);
	    h_moved_tks_err_dxy[i]->Fill(dxyerr, w);
	    h_moved_tks_err_dz[i]->Fill(nt.p_tks_err_dz->at(itk), w);
	    h_moved_tks_nsigmadxy[i]->Fill(nsigmadxy, w);
	    h_moved_tks_npxlayers[i]->Fill(npxlay, w);
	    h_moved_tks_nstlayers[i]->Fill(nstlay, w);
	    h_moved_tks_vtx[i]->Fill(nt.p_tks_vtx->at(itk), w);

	    const bool selected = pt > 1.0 && npxlay >= 2 && nstlay >= 6 && dxy / dxyerr > 4.0;
	    if (!selected) {
	      h_moved_nosel_tks_pt[i]->Fill(pt, w);
	      h_moved_nosel_tks_eta[i]->Fill(nt.p_tks_eta->at(itk), w);
	      h_moved_nosel_tks_phi[i]->Fill(nt.p_tks_phi->at(itk), w);
	      h_moved_nosel_tks_dxy[i]->Fill(dxy, w);
	      h_moved_nosel_tks_dz[i]->Fill(nt.p_tks_dz->at(itk), w);
	      h_moved_nosel_tks_err_pt[i]->Fill(nt.p_tks_err_pt->at(itk), w);
	      h_moved_nosel_tks_err_eta[i]->Fill(nt.p_tks_err_eta->at(itk), w);
	      h_moved_nosel_tks_err_phi[i]->Fill(nt.p_tks_err_phi->at(itk), w);
	      h_moved_nosel_tks_err_dxy[i]->Fill(dxyerr, w);
	      h_moved_nosel_tks_err_dz[i]->Fill(nt.p_tks_err_dz->at(itk), w);
	      h_moved_nosel_tks_nsigmadxy[i]->Fill(nsigmadxy, w);
	      h_moved_nosel_tks_npxlayers[i]->Fill(npxlay, w);
	      h_moved_nosel_tks_nstlayers[i]->Fill(nstlay, w);
	      h_moved_nosel_tks_vtx[i]->Fill(nt.p_tks_vtx->at(itk), w);
	    }
	  }
	}
      }
    }
  }

  printf("\r                                \n");
  printf("%li/%li (%li/%li den) events with negative weights\n", nnegweight, notskipped, ndennegweight, nden);
  printf("%.1f events in denominator (including %.1f negative)\n", den, sumnegweightden);
  printf("%20s  %12s  %12s  %10s [%10s, %10s] +%10s -%10s\n", "name", "num", "den", "eff", "lo", "hi", "+", "-");
  for (const auto& p : nums) {
    const interval i = clopper_pearson_binom(p.second, den);
    printf("%20s  %12.1f  %12.1f  %10.4f [%10.4f, %10.4f] +%10.4f -%10.4f\n", p.first.c_str(), p.second, den, i.value, i.lower, i.upper, i.upper - i.value, i.value - i.lower);
  }
}
