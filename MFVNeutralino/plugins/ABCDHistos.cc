#include "TH2F.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/Math/interface/deltaPhi.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "JMTucker/MFVNeutralinoFormats/interface/Event.h"
#include "JMTucker/MFVNeutralinoFormats/interface/VertexAux.h"
#include "JMTucker/Tools/interface/Utilities.h"

class ABCDHistos : public edm::EDAnalyzer {
 public:
  explicit ABCDHistos(const edm::ParameterSet&);
  void analyze(const edm::Event&, const edm::EventSetup&);

 private:
  const edm::InputTag mfv_event_src;
  const edm::InputTag weight_src;
  const edm::InputTag vertex_src;
  const int which_mom;

  TH1F* h_nsv;
  TH2F* h_ntracks01_maxtrackpt01;

  TH2F* h_bs2derr_ntracks;
  TH2F* h_bs2derr_drmax;

  TH2F* h_ntracks01_sumht;
  TH2F* h_drmin_sumht;
  TH2F* h_drmax_sumht;
  TH2F* h_bs2derr_sumht;
  TH2F* h_njetsntks_sumht;
  TH2F* h_bs2dsig_sumht;
  TH2F* h_ntracksptgt3_sumht;
  TH2F* h_sumnhitsbehind_sumht;

  TH2F* h_ntracks0_sumht;
  TH2F* h_drmin0_sumht;
  TH2F* h_drmax0_sumht;
  TH2F* h_bs2derr0_sumht;
  TH2F* h_njetsntks0_sumht;
  TH2F* h_bs2dsig0_sumht;
  TH2F* h_ntracksptgt30_sumht;
  TH2F* h_sumnhitsbehind0_sumht;

  TH1F* h_absdeltaphibs01;
  TH1F* h_absdeltaphipv01;

  TH1F* h_pz01lab;
  TH1F* h_pz01cmz;

  TH1F* h_cosanglemom01lab;
  TH1F* h_cosanglemom01cmz;

  TH2F* h_betagamma0lab_betagamma1lab;
  TH2F* h_betagamma0cmz_betagamma1cmz;

  TH1F* h_avgbetagammalab;
  TH1F* h_avgbetagammacmz;

  TH2F* h_bs2ddist0_bs2ddist1;

  //mass
  TH2F* h_mass0_mass1;

  TH2F* h_bs2ddist01_mass01;
  TH2F* h_bs2ddist0_mass0;
  TH2F* h_bs2ddist1_mass1;

  TH2F* h_bs2ddist1_mass0;
  TH2F* h_bs2ddist0_mass1;

  TH2F* h_pv2ddist01_mass01;
  TH2F* h_pv2ddist0_mass0;

  TH2F* h_pv3ddist01_mass01;
  TH2F* h_pv3ddist0_mass0;

  TH2F* h_pv3dctau01_mass01;
  TH2F* h_pv3dctau0_mass0;

  TH2F* h_svdist2d_mass01;
  TH2F* h_svdist3d_mass01;

  TH2F* h_svdist2dcmz_mass01;
  TH2F* h_svdist3dcmz_mass01;

  TH2F* h_svctau2dcmz_mass01;
  TH2F* h_svctau3dcmz_mass01;

  //ntracks
  TH2F* h_ntracks0_ntracks1;

  TH2F* h_bs2ddist01_ntracks01;
  TH2F* h_bs2ddist0_ntracks01;
  TH2F* h_bs2ddist0_ntracks0;
  TH2F* h_bs2ddist1_ntracks1;

  TH2F* h_bs2ddist1_ntracks0;
  TH2F* h_bs2ddist0_ntracks1;

  TH2F* h_pv2ddist01_ntracks01;
  TH2F* h_pv2ddist0_ntracks01;
  TH2F* h_pv2ddist0_ntracks0;

  TH2F* h_pv3ddist01_ntracks01;
  TH2F* h_pv3ddist0_ntracks01;
  TH2F* h_pv3ddist0_ntracks0;

  TH2F* h_pv3dctau01_ntracks01;
  TH2F* h_pv3dctau0_ntracks01;
  TH2F* h_pv3dctau0_ntracks0;

  TH2F* h_svdist2d_ntracks01;
  TH2F* h_svdist3d_ntracks01;

  TH2F* h_svdist2dcmz_ntracks01;
  TH2F* h_svdist3dcmz_ntracks01;

  TH2F* h_svctau2dcmz_ntracks01;
  TH2F* h_svctau3dcmz_ntracks01;

  //sumht
  TH2F* h_bs2ddist01_sumht;
  TH2F* h_pv2ddist01_sumht;
  TH2F* h_pv3ddist01_sumht;
  TH2F* h_pv3dctau01_sumht;
  TH2F* h_svdist2d_sumht;
  TH2F* h_svdist3d_sumht;
  TH2F* h_svdist2dcmz_sumht;
  TH2F* h_svdist3dcmz_sumht;
  TH2F* h_svctau2dcmz_sumht;
  TH2F* h_svctau3dcmz_sumht;

  //njets
  TH2F* h_bs2ddist01_njets;
  TH2F* h_pv2ddist01_njets;
  TH2F* h_pv3ddist01_njets;
  TH2F* h_pv3dctau01_njets;
  TH2F* h_svdist2d_njets;
  TH2F* h_svdist3d_njets;
  TH2F* h_svdist2dcmz_njets;
  TH2F* h_svdist3dcmz_njets;
  TH2F* h_svctau2dcmz_njets;
  TH2F* h_svctau3dcmz_njets;

  //other variables
  TH2F* h_svctau3dcmz_maxtrackpt01;
  TH2F* h_svctau3dcmz_maxm1trackpt01;
  TH2F* h_svctau3dcmz_ntracksptgt301;
  TH2F* h_svctau3dcmz_msptm01;

  TH2F* h_sumht1_sumht0[2]; // 3d, 2d
  TH1F* h_sumhtdiff[2];
};

ABCDHistos::ABCDHistos(const edm::ParameterSet& cfg)
  : mfv_event_src(cfg.getParameter<edm::InputTag>("mfv_event_src")),
    weight_src(cfg.getParameter<edm::InputTag>("weight_src")),
    vertex_src(cfg.getParameter<edm::InputTag>("vertex_src")),
    which_mom(cfg.getParameter<int>("which_mom"))
{
  die_if_not(which_mom >= 0 && which_mom < mfv::NMomenta, "invalid which_mom");

  edm::Service<TFileService> fs;
  h_nsv = fs->make<TH1F>("h_nsv", ";number of secondary vertices;events", 15, 0, 15);
  h_ntracks01_maxtrackpt01 = fs->make<TH2F>("h_ntracks01_maxtrackpt01", ";sum of maxtrackpt for the two SV's with the highest ntracks;sum of ntracks for the two SV's with the highest ntracks", 300, 0, 300, 80, 0, 80);

  h_bs2derr_ntracks = fs->make<TH2F>("h_bs2derr_ntracks", ";ntracks;bs2derr", 40, 0, 40, 100, 0, 0.05);
  h_bs2derr_drmax = fs->make<TH2F>("h_bs2derr_drmax", ";drmax;bs2derr", 150, 0, 7, 100, 0, 0.05);

  h_ntracks01_sumht = fs->make<TH2F>("h_ntracks01_sumht", ";sumht;ntracks01", 500, 0, 5000, 80, 0, 80);
  h_drmin_sumht = fs->make<TH2F>("h_drmin_sumht", ";sumht;drmin", 500, 0, 5000, 150, 0, 1.5);
  h_drmax_sumht = fs->make<TH2F>("h_drmax_sumht", ";sumht;drmax", 500, 0, 5000, 150, 0, 7);
  h_bs2derr_sumht = fs->make<TH2F>("h_bs2derr_sumht", ";sumht;bs2derr", 500, 0, 5000, 100, 0, 0.05);
  h_njetsntks_sumht = fs->make<TH2F>("h_njetsntks_sumht", ";sumht;njetntks", 500, 0, 5000, 10, 0, 10);
  h_bs2dsig_sumht = fs->make<TH2F>("h_bs2dsig_sumht", ";sumht;bs2dsig", 500, 0, 5000, 100, 0, 100);
  h_ntracksptgt3_sumht = fs->make<TH2F>("h_ntracksptgt3_sumht", ";sumht;ntracksptgt3", 500, 0, 5000, 40, 0, 40);
  h_sumnhitsbehind_sumht = fs->make<TH2F>("h_sumnhitsbehind_sumht", ";sumht;sumnhitsbehind", 500, 0, 5000, 100, 0, 100);

  h_ntracks0_sumht = fs->make<TH2F>("h_ntracks0_sumht", ";sumht;ntracks0", 500, 0, 5000, 40, 0, 40);
  h_drmin0_sumht = fs->make<TH2F>("h_drmin0_sumht", ";sumht;drmin0", 500, 0, 5000, 150, 0, 1.5);
  h_drmax0_sumht = fs->make<TH2F>("h_drmax0_sumht", ";sumht;drmax0", 500, 0, 5000, 150, 0, 7);
  h_bs2derr0_sumht = fs->make<TH2F>("h_bs2derr0_sumht", ";sumht;bs2derr0", 500, 0, 5000, 100, 0, 0.05);
  h_njetsntks0_sumht = fs->make<TH2F>("h_njetsntks0_sumht", ";sumht;njetntks0", 500, 0, 5000, 10, 0, 10);
  h_bs2dsig0_sumht = fs->make<TH2F>("h_bs2dsig0_sumht", ";sumht;bs2dsig0", 500, 0, 5000, 100, 0, 100);
  h_ntracksptgt30_sumht = fs->make<TH2F>("h_ntracksptgt30_sumht", ";sumht;ntracksptgt30", 500, 0, 5000, 40, 0, 40);
  h_sumnhitsbehind0_sumht = fs->make<TH2F>("h_sumnhitsbehind0_sumht", ";sumht;sumnhitsbehind0", 500, 0, 5000, 100, 0, 100);

  h_absdeltaphibs01 = fs->make<TH1F>("h_absdeltaphibs01", ";absdeltaphibs01;events", 315, 0, 3.15);
  h_absdeltaphipv01 = fs->make<TH1F>("h_absdeltaphipv01", ";absdeltaphipv01;events", 315, 0, 3.15);

  h_pz01lab = fs->make<TH1F>("h_pz01lab", ";pz01lab;events", 100, -300, 300);
  h_pz01cmz = fs->make<TH1F>("h_pz01cmz", ";pz01cmz;events", 100, -300, 300);

  h_cosanglemom01lab = fs->make<TH1F>("h_cosanglemom01lab", ";cosanglemom01lab;events", 100, -1, 1);
  h_cosanglemom01cmz = fs->make<TH1F>("h_cosanglemom01cmz", ";cosanglemom01cmz;events", 100, -1, 1);

  h_betagamma0lab_betagamma1lab = fs->make<TH2F>("h_betagamma0lab_betagamma1lab", ";betagamma1lab;betagamma0lab", 100, 0, 10, 100, 0, 10);
  h_betagamma0cmz_betagamma1cmz = fs->make<TH2F>("h_betagamma0cmz_betagamma1cmz", ";betagamma1cmz;betagamma0cmz", 100, 0, 10, 100, 0, 10);

  h_avgbetagammalab = fs->make<TH1F>("h_avgbetagammalab", ";avgbetagammalab;events", 100, 0, 10);
  h_avgbetagammacmz = fs->make<TH1F>("h_avgbetagammacmz", ";avgbetagammacmz;events", 100, 0, 10);

  h_bs2ddist0_bs2ddist1 = fs->make<TH2F>("h_bs2ddist0_bs2ddist1", ";bs2ddist1;bs2ddist0", 50, 0, 0.5, 50, 0, 0.5);

  //mass
  h_mass0_mass1 = fs->make<TH2F>("h_mass0_mass1", ";mass1;mass0", 1000, 0, 1000, 1000, 0, 1000);

  h_bs2ddist01_mass01 = fs->make<TH2F>("h_bs2ddist01_mass01", ";mass01;bs2ddist01", 1000, 0, 1000, 100, 0, 1);
  h_bs2ddist0_mass0 = fs->make<TH2F>("h_bs2ddist0_mass0", ";mass0;bs2ddist0", 500, 0, 500, 50, 0, 0.5);
  h_bs2ddist1_mass1 = fs->make<TH2F>("h_bs2ddist1_mass1", ";mass1;bs2ddist1", 500, 0, 500, 50, 0, 0.5);

  h_bs2ddist1_mass0 = fs->make<TH2F>("h_bs2ddist1_mass0", ";mass0;bs2ddist1", 500, 0, 500, 50, 0, 0.5);
  h_bs2ddist0_mass1 = fs->make<TH2F>("h_bs2ddist0_mass1", ";mass1;bs2ddist0", 500, 0, 500, 50, 0, 0.5);

  h_pv2ddist01_mass01 = fs->make<TH2F>("h_pv2ddist01_mass01", ";mass01;pv2ddist01", 1000, 0, 1000, 100, 0, 1);
  h_pv2ddist0_mass0 = fs->make<TH2F>("h_pv2ddist0_mass0", ";mass0;pv2ddist0", 500, 0, 500, 50, 0, 0.5);

  h_pv3ddist01_mass01 = fs->make<TH2F>("h_pv3ddist01_mass01", ";mass01;pv3ddist01", 1000, 0, 1000, 100, 0, 1);
  h_pv3ddist0_mass0 = fs->make<TH2F>("h_pv3ddist0_mass0", ";mass0;pv3ddist0", 500, 0, 500, 50, 0, 0.5);

  h_pv3dctau01_mass01 = fs->make<TH2F>("h_pv3dctau01_mass01", ";mass01;pv3dctau01", 1000, 0, 1000, 100, 0, 1);
  h_pv3dctau0_mass0 = fs->make<TH2F>("h_pv3dctau0_mass0", ";mass0;pv3dctau0", 500, 0, 500, 50, 0, 0.5);

  h_svdist2d_mass01 = fs->make<TH2F>("h_svdist2d_mass01", ";mass01;svdist2d", 1000, 0, 1000, 100, 0, 1);
  h_svdist3d_mass01 = fs->make<TH2F>("h_svdist3d_mass01", ";mass01;svdist3d", 1000, 0, 1000, 100, 0, 1);

  h_svdist2dcmz_mass01 = fs->make<TH2F>("h_svdist2dcmz_mass01", ";mass01;svdist2dcmz", 1000, 0, 1000, 100, 0, 1);
  h_svdist3dcmz_mass01 = fs->make<TH2F>("h_svdist3dcmz_mass01", ";mass01;svdist3dcmz", 1000, 0, 1000, 100, 0, 1);

  h_svctau2dcmz_mass01 = fs->make<TH2F>("h_svctau2dcmz_mass01", ";mass01;svctau2dcmz", 1000, 0, 1000, 100, 0, 1);
  h_svctau3dcmz_mass01 = fs->make<TH2F>("h_svctau3dcmz_mass01", ";mass01;svctau3dcmz", 1000, 0, 1000, 100, 0, 1);

  //ntracks
  h_ntracks0_ntracks1 = fs->make<TH2F>("h_ntracks0_ntracks1", ";ntracks1;ntracks0", 80, 0, 80, 80, 0, 80);

  h_bs2ddist01_ntracks01 = fs->make<TH2F>("h_bs2ddist01_ntracks01", ";ntracks01;bs2ddist01", 80, 0, 80, 100, 0, 1);
  h_bs2ddist0_ntracks01 = fs->make<TH2F>("h_bs2ddist0_ntracks01", ";ntracks01;bs2ddist0", 80, 0, 80, 50, 0, 0.5);
  h_bs2ddist0_ntracks0 = fs->make<TH2F>("h_bs2ddist0_ntracks0", ";ntracks0;bs2ddist0", 40, 0, 40, 50, 0, 0.5);
  h_bs2ddist1_ntracks1 = fs->make<TH2F>("h_bs2ddist1_ntracks1", ";ntracks1;bs2ddist1", 40, 0, 40, 50, 0, 0.5);

  h_bs2ddist1_ntracks0 = fs->make<TH2F>("h_bs2ddist1_ntracks0", ";ntracks0;bs2ddist1", 40, 0, 40, 50, 0, 0.5);
  h_bs2ddist0_ntracks1 = fs->make<TH2F>("h_bs2ddist0_ntracks1", ";ntracks1;bs2ddist0", 40, 0, 40, 50, 0, 0.5);

  h_pv2ddist01_ntracks01 = fs->make<TH2F>("h_pv2ddist01_ntracks01", ";ntracks01;pv2ddist01", 80, 0, 80, 100, 0, 1);
  h_pv2ddist0_ntracks01 = fs->make<TH2F>("h_pv2ddist0_ntracks01", ";ntracks01;pv2ddist0", 80, 0, 80, 50, 0, 0.5);
  h_pv2ddist0_ntracks0 = fs->make<TH2F>("h_pv2ddist0_ntracks0", ";ntracks0;pv2ddist0", 40, 0, 40, 50, 0, 0.5);

  h_pv3ddist01_ntracks01 = fs->make<TH2F>("h_pv3ddist01_ntracks01", ";ntracks01;pv3ddist01", 80, 0, 80, 100, 0, 1);
  h_pv3ddist0_ntracks01 = fs->make<TH2F>("h_pv3ddist0_ntracks01", ";ntracks01;pv3ddist0", 80, 0, 80, 50, 0, 0.5);
  h_pv3ddist0_ntracks0 = fs->make<TH2F>("h_pv3ddist0_ntracks0", ";ntracks0;pv3ddist0", 40, 0, 40, 50, 0, 0.5);

  h_pv3dctau01_ntracks01 = fs->make<TH2F>("h_pv3dctau01_ntracks01", ";ntracks01;pv3dctau01", 80, 0, 80, 100, 0, 1);
  h_pv3dctau0_ntracks01 = fs->make<TH2F>("h_pv3dctau0_ntracks01", ";ntracks01;pv3dctau0", 80, 0, 80, 50, 0, 0.5);
  h_pv3dctau0_ntracks0 = fs->make<TH2F>("h_pv3dctau0_ntracks0", ";ntracks0;pv3dctau0", 40, 0, 40, 50, 0, 0.5);

  h_svdist2d_ntracks01 = fs->make<TH2F>("h_svdist2d_ntracks01", ";ntracks01;svdist2d", 80, 0, 80, 100, 0, 1);
  h_svdist3d_ntracks01 = fs->make<TH2F>("h_svdist3d_ntracks01", ";ntracks01;svdist3d", 80, 0, 80, 100, 0, 1);

  h_svdist2dcmz_ntracks01 = fs->make<TH2F>("h_svdist2dcmz_ntracks01", ";ntracks01;svdist2dcmz", 80, 0, 80, 100, 0, 1);
  h_svdist3dcmz_ntracks01 = fs->make<TH2F>("h_svdist3dcmz_ntracks01", ";ntracks01;svdist3dcmz", 80, 0, 80, 100, 0, 1);

  h_svctau2dcmz_ntracks01 = fs->make<TH2F>("h_svctau2dcmz_ntracks01", ";ntracks01;svctau2dcmz", 80, 0, 80, 100, 0, 1);
  h_svctau3dcmz_ntracks01 = fs->make<TH2F>("h_svctau3dcmz_ntracks01", ";ntracks01;svctau3dcmz", 80, 0, 80, 100, 0, 1);

  //sumht
  h_bs2ddist01_sumht = fs->make<TH2F>("h_bs2ddist01_sumht", ";sumht;bs2ddist01", 500, 0, 5000, 100, 0, 1);
  h_pv2ddist01_sumht = fs->make<TH2F>("h_pv2ddist01_sumht", ";sumht;pv2ddist01", 500, 0, 5000, 100, 0, 1);
  h_pv3ddist01_sumht = fs->make<TH2F>("h_pv3ddist01_sumht", ";sumht;pv3ddist01", 500, 0, 5000, 100, 0, 1);
  h_pv3dctau01_sumht = fs->make<TH2F>("h_pv3dctau01_sumht", ";sumht;pv3dctau01", 500, 0, 5000, 100, 0, 1);
  h_svdist2d_sumht = fs->make<TH2F>("h_svdist2d_sumht", ";sumht;svdist2d", 500, 0, 5000, 100, 0, 1);
  h_svdist3d_sumht = fs->make<TH2F>("h_svdist3d_sumht", ";sumht;svdist3d", 500, 0, 5000, 100, 0, 1);
  h_svdist2dcmz_sumht = fs->make<TH2F>("h_svdist2dcmz_sumht", ";sumht;svdist2dcmz", 500, 0, 5000, 100, 0, 1);
  h_svdist3dcmz_sumht = fs->make<TH2F>("h_svdist3dcmz_sumht", ";sumht;svdist3dcmz", 500, 0, 5000, 100, 0, 1);
  h_svctau2dcmz_sumht = fs->make<TH2F>("h_svctau2dcmz_sumht", ";sumht;svctau2dcmz", 500, 0, 5000, 100, 0, 1);
  h_svctau3dcmz_sumht = fs->make<TH2F>("h_svctau3dcmz_sumht", ";sumht;svctau3dcmz", 500, 0, 5000, 100, 0, 1);

  //njets
  h_bs2ddist01_njets = fs->make<TH2F>("h_bs2ddist01_njets", ";njets;bs2ddist01", 20, 0, 20, 100, 0, 1);
  h_pv2ddist01_njets = fs->make<TH2F>("h_pv2ddist01_njets", ";njets;pv2ddist01", 20, 0, 20, 100, 0, 1);
  h_pv3ddist01_njets = fs->make<TH2F>("h_pv3ddist01_njets", ";njets;pv3ddist01", 20, 0, 20, 100, 0, 1);
  h_pv3dctau01_njets = fs->make<TH2F>("h_pv3dctau01_njets", ";njets;pv3dctau01", 20, 0, 20, 100, 0, 1);
  h_svdist2d_njets = fs->make<TH2F>("h_svdist2d_njets", ";njets;svdist2d", 20, 0, 20, 100, 0, 1);
  h_svdist3d_njets = fs->make<TH2F>("h_svdist3d_njets", ";njets;svdist3d", 20, 0, 20, 100, 0, 1);
  h_svdist2dcmz_njets = fs->make<TH2F>("h_svdist2dcmz_njets", ";njets;svdist2dcmz", 20, 0, 20, 100, 0, 1);
  h_svdist3dcmz_njets = fs->make<TH2F>("h_svdist3dcmz_njets", ";njets;svdist3dcmz", 20, 0, 20, 100, 0, 1);
  h_svctau2dcmz_njets = fs->make<TH2F>("h_svctau2dcmz_njets", ";njets;svctau2dcmz", 20, 0, 20, 100, 0, 1);
  h_svctau3dcmz_njets = fs->make<TH2F>("h_svctau3dcmz_njets", ";njets;svctau3dcmz", 20, 0, 20, 100, 0, 1);

  //other variables
  h_svctau3dcmz_maxtrackpt01 = fs->make<TH2F>("h_svctau3dcmz_maxtrackpt01", ";maxtrackpt01;svctau3dcmz", 300, 0, 300, 100, 0, 1);
  h_svctau3dcmz_maxm1trackpt01 = fs->make<TH2F>("h_svctau3dcmz_maxm1trackpt01", ";maxm1trackpt01;svctau3dcmz", 300, 0, 300, 100, 0, 1);
  h_svctau3dcmz_ntracksptgt301 = fs->make<TH2F>("h_svctau3dcmz_ntracksptgt301", ";ntracksptgt301;svctau3dcmz", 80, 0, 80, 100, 0, 1);
  h_svctau3dcmz_msptm01 = fs->make<TH2F>("h_svctau3dcmz_msptm01", ";msptm01;svctau3dcmz", 500, 0, 5000, 100, 0, 1);

  h_sumht1_sumht0[0] = fs->make<TH2F>("h_sumht1_sumht0_3d", ";sumht (3D hemisphere 0);sumht (3D hemisphere 1)", 100, 0, 1000, 100, 0, 1000);
  h_sumht1_sumht0[1] = fs->make<TH2F>("h_sumht1_sumht0_2d", ";sumht (2D hemisphere 0);sumht (2D hemisphere 1)", 100, 0, 1000, 100, 0, 1000);
  h_sumhtdiff[0] = fs->make<TH1F>("h_sumhtdiff_3d", ";sumht diff (3D hemisphere 0 - 1);arb. units", 100, -500, 500);
  h_sumhtdiff[1] = fs->make<TH1F>("h_sumhtdiff_2d", ";sumht diff (2D hemisphere 0 - 1);arb. units", 100, -500, 500);

}

void ABCDHistos::analyze(const edm::Event& event, const edm::EventSetup&) {
  edm::Handle<MFVEvent> mevent;
  event.getByLabel(mfv_event_src, mevent);

  edm::Handle<double> weight;
  event.getByLabel(weight_src, weight);
  const double w = *weight;

  const float pvx = mevent->pvx;
  const float pvy = mevent->pvy;
  const float pvz = mevent->pvz;

  edm::Handle<MFVVertexAuxCollection> vertices;
  event.getByLabel(vertex_src, vertices);

  const int nsv = int(vertices->size());
  h_nsv->Fill(nsv, w);

  for (int isv = 0; isv < nsv; ++isv) {
    const MFVVertexAux& vtx = vertices->at(isv);
    h_bs2derr_ntracks->Fill(vtx.ntracks(), vtx.bs2derr(), w);
    h_bs2derr_drmax->Fill(vtx.drmax(), vtx.bs2derr(), w);

    h_drmin_sumht->Fill(mevent->jet_sum_ht(), vtx.drmin(), w);
    h_drmax_sumht->Fill(mevent->jet_sum_ht(), vtx.drmax(), w);
    h_bs2derr_sumht->Fill(mevent->jet_sum_ht(), vtx.bs2derr(), w);
    h_njetsntks_sumht->Fill(mevent->jet_sum_ht(), vtx.njets(mfv::JByNtracks), w);
    h_bs2dsig_sumht->Fill(mevent->jet_sum_ht(), vtx.bs2dsig(), w);
    h_ntracksptgt3_sumht->Fill(mevent->jet_sum_ht(), vtx.ntracksptgt(3), w);
    h_sumnhitsbehind_sumht->Fill(mevent->jet_sum_ht(), vtx.sumnhitsbehind(), w);
  }

  if (nsv >= 1) {
    const MFVVertexAux& vtx = vertices->at(0);
    h_ntracks0_sumht->Fill(mevent->jet_sum_ht(), vtx.ntracks(), w);
    h_drmin0_sumht->Fill(mevent->jet_sum_ht(), vtx.drmin(), w);
    h_drmax0_sumht->Fill(mevent->jet_sum_ht(), vtx.drmax(), w);
    h_bs2derr0_sumht->Fill(mevent->jet_sum_ht(), vtx.bs2derr(), w);
    h_njetsntks0_sumht->Fill(mevent->jet_sum_ht(), vtx.njets(mfv::JByNtracks), w);
    h_bs2dsig0_sumht->Fill(mevent->jet_sum_ht(), vtx.bs2dsig(), w);
    h_ntracksptgt30_sumht->Fill(mevent->jet_sum_ht(), vtx.ntracksptgt(3), w);
    h_sumnhitsbehind0_sumht->Fill(mevent->jet_sum_ht(), vtx.sumnhitsbehind(), w);
  }

  if (nsv >= 2) {
    const MFVVertexAux& v0 = vertices->at(0);
    const MFVVertexAux& v1 = vertices->at(1);
    h_ntracks01_maxtrackpt01->Fill(v0.maxtrackpt() + v1.maxtrackpt(), v0.ntracks() + v1.ntracks(), w);
    h_ntracks01_sumht->Fill(mevent->jet_sum_ht(), v0.ntracks() + v1.ntracks(), w);

    h_bs2ddist0_bs2ddist1->Fill(v1.bs2ddist(), v0.bs2ddist(), w);
    h_mass0_mass1->Fill(v1.mass(which_mom), v0.mass(which_mom), w);

    h_bs2ddist01_mass01->Fill(v0.mass(which_mom) + v1.mass(which_mom), v0.bs2ddist() + v1.bs2ddist(), w);
    h_bs2ddist0_mass0->Fill(v0.mass(which_mom), v0.bs2ddist(), w);
    h_bs2ddist1_mass1->Fill(v1.mass(which_mom), v1.bs2ddist(), w);

    h_bs2ddist1_mass0->Fill(v0.mass(which_mom), v1.bs2ddist(), w);
    h_bs2ddist0_mass1->Fill(v1.mass(which_mom), v0.bs2ddist(), w);

    h_pv2ddist01_mass01->Fill(v0.mass(which_mom) + v1.mass(which_mom), v0.pv2ddist() + v1.pv2ddist(), w);
    h_pv2ddist0_mass0->Fill(v0.mass(which_mom), v0.pv2ddist(), w);

    h_pv3ddist01_mass01->Fill(v0.mass(which_mom) + v1.mass(which_mom), v0.pv3ddist() + v1.pv3ddist(), w);
    h_pv3ddist0_mass0->Fill(v0.mass(which_mom), v0.pv3ddist(), w);

    double pv3dctau0 = v0.pv3ddist() / (v0.p4(which_mom).Beta() * v0.p4(which_mom).Gamma());
    double pv3dctau1 = v1.pv3ddist() / (v1.p4(which_mom).Beta() * v1.p4(which_mom).Gamma());
    h_pv3dctau01_mass01->Fill(v0.mass(which_mom) + v1.mass(which_mom), pv3dctau0 + pv3dctau1, w);
    h_pv3dctau0_mass0->Fill(v0.mass(which_mom), pv3dctau0, w);

    double svdist2d = mag(v0.x - v1.x, v0.y - v1.y);
    double svdist3d = mag(v0.x - v1.x, v0.y - v1.y, v0.z - v1.z);
    h_svdist2d_mass01->Fill(v0.mass(which_mom) + v1.mass(which_mom), svdist2d, w);
    h_svdist3d_mass01->Fill(v0.mass(which_mom) + v1.mass(which_mom), svdist3d, w);

    double phibs0 = atan2(v0.y - mevent->bsy, v0.x - mevent->bsx);
    double phibs1 = atan2(v1.y - mevent->bsy, v1.x - mevent->bsx);
    h_absdeltaphibs01->Fill(fabs(reco::deltaPhi(phibs0, phibs1)), w);
    double phipv0 = atan2(v0.y - mevent->pvy, v0.x - mevent->pvx);
    double phipv1 = atan2(v1.y - mevent->pvy, v1.x - mevent->pvx);
    h_absdeltaphipv01->Fill(fabs(reco::deltaPhi(phipv0, phipv1)), w);

    TLorentzVector x0 = TLorentzVector(v0.x - pvx, v0.y - pvy, v0.z - pvz, v0.pv3ddist() / v0.p4().Beta());
    TLorentzVector x1 = TLorentzVector(v1.x - pvx, v1.y - pvy, v1.z - pvz, v1.pv3ddist() / v1.p4().Beta());
    TLorentzVector p0 = v0.p4(which_mom);
    TLorentzVector p1 = v1.p4(which_mom);
    h_pz01lab->Fill(p0.Pz() + p1.Pz(), w);
    h_cosanglemom01lab->Fill(cos(p0.Angle(p1.Vect())), w);
    h_betagamma0lab_betagamma1lab->Fill(p1.Beta() * p1.Gamma(), p0.Beta() * p0.Gamma(), w);
    h_avgbetagammalab->Fill((p0.Beta() * p0.Gamma() + p1.Beta() * p1.Gamma()) / 2, w);

    TVector3 betacmz = TVector3(0, 0, -(p0.Pz() + p1.Pz()) / (p0.E() + p1.E()));
    x0.Boost(betacmz);
    x1.Boost(betacmz);
    p0.Boost(betacmz);
    p1.Boost(betacmz);
    h_pz01cmz->Fill(p0.Pz() + p1.Pz(), w);
    h_cosanglemom01cmz->Fill(cos(p0.Angle(p1.Vect())), w);
    h_betagamma0cmz_betagamma1cmz->Fill(p1.Beta() * p1.Gamma(), p0.Beta() * p0.Gamma(), w);
    h_avgbetagammacmz->Fill((p0.Beta() * p0.Gamma() + p1.Beta() * p1.Gamma()) / 2, w);

    double svdist2dcmz = mag(x0.X() - x1.X(), x0.Y() - x1.Y());
    double svdist3dcmz = mag(x0.X() - x1.X(), x0.Y() - x1.Y(), x0.Z() - x1.Z());
    h_svdist2dcmz_mass01->Fill(v0.mass(which_mom) + v1.mass(which_mom), svdist2dcmz, w);
    h_svdist3dcmz_mass01->Fill(v0.mass(which_mom) + v1.mass(which_mom), svdist3dcmz, w);

    double svctau2dcmz = 2 * svdist2dcmz / (p0.Beta()*p0.Gamma() + p1.Beta()*p1.Gamma());
    double svctau3dcmz = 2 * svdist3dcmz / (p0.Beta()*p0.Gamma() + p1.Beta()*p1.Gamma());
    h_svctau2dcmz_mass01->Fill(v0.mass(which_mom) + v1.mass(which_mom), svctau2dcmz, w);
    h_svctau3dcmz_mass01->Fill(v0.mass(which_mom) + v1.mass(which_mom), svctau3dcmz, w);

    //ntracks
    h_ntracks0_ntracks1->Fill(v1.ntracks(), v0.ntracks(), w);

    h_bs2ddist01_ntracks01->Fill(v0.ntracks() + v1.ntracks(), v0.bs2ddist() + v1.bs2ddist(), w);
    h_bs2ddist0_ntracks01->Fill(v0.ntracks() + v1.ntracks(), v0.bs2ddist(), w);
    h_bs2ddist0_ntracks0->Fill(v0.ntracks(), v0.bs2ddist(), w);
    h_bs2ddist1_ntracks1->Fill(v1.ntracks(), v1.bs2ddist(), w);

    h_bs2ddist1_ntracks0->Fill(v0.ntracks(), v1.bs2ddist(), w);
    h_bs2ddist0_ntracks1->Fill(v1.ntracks(), v0.bs2ddist(), w);

    h_pv2ddist01_ntracks01->Fill(v0.ntracks() + v1.ntracks(), v0.pv2ddist() + v1.pv2ddist(), w);
    h_pv2ddist0_ntracks01->Fill(v0.ntracks() + v1.ntracks(), v0.pv2ddist(), w);
    h_pv2ddist0_ntracks0->Fill(v0.ntracks(), v0.pv2ddist(), w);

    h_pv3ddist01_ntracks01->Fill(v0.ntracks() + v1.ntracks(), v0.pv3ddist() + v1.pv3ddist(), w);
    h_pv3ddist0_ntracks01->Fill(v0.ntracks() + v1.ntracks(), v0.pv3ddist(), w);
    h_pv3ddist0_ntracks0->Fill(v0.ntracks(), v0.pv3ddist(), w);

    h_pv3dctau01_ntracks01->Fill(v0.ntracks() + v1.ntracks(), pv3dctau0 + pv3dctau1, w);
    h_pv3dctau0_ntracks01->Fill(v0.ntracks() + v1.ntracks(), pv3dctau0, w);
    h_pv3dctau0_ntracks0->Fill(v0.ntracks(), pv3dctau0, w);

    h_svdist2d_ntracks01->Fill(v0.ntracks() + v1.ntracks(), svdist2d, w);
    h_svdist3d_ntracks01->Fill(v0.ntracks() + v1.ntracks(), svdist3d, w);

    h_svdist2dcmz_ntracks01->Fill(v0.ntracks() + v1.ntracks(), svdist2dcmz, w);
    h_svdist3dcmz_ntracks01->Fill(v0.ntracks() + v1.ntracks(), svdist3dcmz, w);

    h_svctau2dcmz_ntracks01->Fill(v0.ntracks() + v1.ntracks(), svctau2dcmz, w);
    h_svctau3dcmz_ntracks01->Fill(v0.ntracks() + v1.ntracks(), svctau3dcmz, w);

    //sumht
    h_bs2ddist01_sumht->Fill(mevent->jet_sum_ht(), v0.bs2ddist() + v1.bs2ddist(), w);
    h_pv2ddist01_sumht->Fill(mevent->jet_sum_ht(), v0.pv2ddist() + v1.pv2ddist(), w);
    h_pv3ddist01_sumht->Fill(mevent->jet_sum_ht(), v0.pv3ddist() + v1.pv3ddist(), w);
    h_pv3dctau01_sumht->Fill(mevent->jet_sum_ht(), pv3dctau0 + pv3dctau1, w);
    h_svdist2d_sumht->Fill(mevent->jet_sum_ht(), svdist2d, w);
    h_svdist3d_sumht->Fill(mevent->jet_sum_ht(), svdist3d, w);
    h_svdist2dcmz_sumht->Fill(mevent->jet_sum_ht(), svdist2dcmz, w);
    h_svdist3dcmz_sumht->Fill(mevent->jet_sum_ht(), svdist3dcmz, w);
    h_svctau2dcmz_sumht->Fill(mevent->jet_sum_ht(), svctau2dcmz, w);
    h_svctau3dcmz_sumht->Fill(mevent->jet_sum_ht(), svctau3dcmz, w);

    //njets
    h_bs2ddist01_njets->Fill(mevent->njets(), v0.bs2ddist() + v1.bs2ddist(), w);
    h_pv2ddist01_njets->Fill(mevent->njets(), v0.pv2ddist() + v1.pv2ddist(), w);
    h_pv3ddist01_njets->Fill(mevent->njets(), v0.pv3ddist() + v1.pv3ddist(), w);
    h_pv3dctau01_njets->Fill(mevent->njets(), pv3dctau0 + pv3dctau1, w);
    h_svdist2d_njets->Fill(mevent->njets(), svdist2d, w);
    h_svdist3d_njets->Fill(mevent->njets(), svdist3d, w);
    h_svdist2dcmz_njets->Fill(mevent->njets(), svdist2dcmz, w);
    h_svdist3dcmz_njets->Fill(mevent->njets(), svdist3dcmz, w);
    h_svctau2dcmz_njets->Fill(mevent->njets(), svctau2dcmz, w);
    h_svctau3dcmz_njets->Fill(mevent->njets(), svctau3dcmz, w);

    //other variables
    h_svctau3dcmz_maxtrackpt01->Fill(v0.maxtrackpt() + v1.maxtrackpt(), svctau3dcmz, w);
    h_svctau3dcmz_maxm1trackpt01->Fill(v0.maxmntrackpt(1) + v1.maxmntrackpt(1), svctau3dcmz, w);
    h_svctau3dcmz_ntracksptgt301->Fill(v0.ntracksptgt(3) + v1.ntracksptgt(3), svctau3dcmz, w);
    double msptm0 = sqrt(v0.mass(which_mom) * v0.mass(which_mom) + v0.pt(which_mom) * v0.pt(which_mom)) + fabs(v0.pt(which_mom));
    double msptm1 = sqrt(v1.mass(which_mom) * v1.mass(which_mom) + v1.pt(which_mom) * v1.pt(which_mom)) + fabs(v1.pt(which_mom));
    h_svctau3dcmz_msptm01->Fill(msptm0 + msptm1, svctau3dcmz, w);


    TVector3 pos0(v0.x, v0.y, v0.z);
    TVector3 pos1(v1.x, v1.y, v1.z);
    TVector3 posavg = 0.5*(pos0 + pos1);
    pos0 = pos0 - posavg;
    pos1 = pos1 - posavg;
    for (int j = 0; j < 2; ++j) {
      if (j == 1) {
        pos0.SetZ(0);
        pos1.SetZ(0);
        posavg.SetZ(0);
      }
      float sumht0 = 0, sumht1 = 0;
      for (int i = 0, ie = mevent->njets(); i < ie; ++i) {
        TVector3 jet_dir = mevent->jet_p4(i).Vect();
        if (j == 1)
          jet_dir.SetZ(0); // not really necessary
        if (pos0.Dot(jet_dir) >= 0)
          sumht0 += mevent->jet_pt[i];
        else
          sumht1 += mevent->jet_pt[i];
      }
      
      h_sumht1_sumht0[j]->Fill(sumht0, sumht1);
      h_sumhtdiff[j]->Fill(sumht0 - sumht1);
    }
  }
}

DEFINE_FWK_MODULE(ABCDHistos);
