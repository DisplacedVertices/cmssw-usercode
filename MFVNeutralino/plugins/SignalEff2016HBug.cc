#include "TH2.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "JMTucker/MFVNeutralino/interface/MCInteractionMFV3j.h"
#include "JMTucker/MFVNeutralinoFormats/interface/Event.h"
#include "JMTucker/MFVNeutralinoFormats/interface/TriggerFloats.h"

class MFVSignalEff2016HBug : public edm::EDAnalyzer {
public:
  explicit MFVSignalEff2016HBug(const edm::ParameterSet&);

private:
  virtual void analyze(const edm::Event&, const edm::EventSetup&);

  const edm::EDGetTokenT<mfv::TriggerFloats> triggerfloats_token;
  const int l1htt_threshold;
  const int l1htt_bit;

  const std::string which_l1htt_s;
  const enum use_which { use_event_l1htt, use_my_l1htt, use_my_l1htt_wbug, use_none } which_l1htt;

  const edm::EDGetTokenT<reco::GenParticleCollection> gen_particles_token;

  TH2F* h_l1_check;
  TH1F* h_gendvv_den;
  TH1F* h_gendvv_num;
  TH1F* h_gendvv_fail; // = den - num but for a check
  TH1F* h_gendvv_faill1htt_l1single;
  TH1F* h_gendvv_faill1htt_l1single450;
  TH1F* h_gendvv_faill1htt_l1single450ak;
};

MFVSignalEff2016HBug::MFVSignalEff2016HBug(const edm::ParameterSet& cfg)
  : triggerfloats_token(consumes<mfv::TriggerFloats>(edm::InputTag("mfvTriggerFloats"))),
    l1htt_threshold(cfg.getParameter<int>("l1htt_threshold")),
    l1htt_bit(l1htt_threshold == 160 ? mfv::b_L1_HTT160 :
              l1htt_threshold == 200 ? mfv::b_L1_HTT200 :
              l1htt_threshold == 220 ? mfv::b_L1_HTT220 :
              l1htt_threshold == 240 ? mfv::b_L1_HTT240 :
              l1htt_threshold == 255 ? mfv::b_L1_HTT255 :
              l1htt_threshold == 270 ? mfv::b_L1_HTT270 :
              l1htt_threshold == 280 ? mfv::b_L1_HTT280 :
              l1htt_threshold == 300 ? mfv::b_L1_HTT300 :
              l1htt_threshold == 320 ? mfv::b_L1_HTT320 :
              999),
    which_l1htt_s(cfg.getParameter<std::string>("which_l1htt")),
    which_l1htt(which_l1htt_s == "event"  ? use_event_l1htt   : 
                which_l1htt_s == "my"     ? use_my_l1htt      :
                which_l1htt_s == "mywbug" ? use_my_l1htt_wbug :
                use_none),
    gen_particles_token(consumes<reco::GenParticleCollection>(edm::InputTag("genParticles")))
{
  if (which_l1htt == use_none)
    throw cms::Exception("Configuration", "bad setting for which_l1htt: ") << which_l1htt_s;
  if (l1htt_bit == 999)
    throw cms::Exception("Configuration", "bad setting for l1htt_threshold: ") << l1htt_threshold;

  edm::Service<TFileService> fs;
  TH1::SetDefaultSumw2();

  h_l1_check = fs->make<TH2F>("h_l1_check", "", 1000, 0, 1000, 2, 0, 2);
  h_gendvv_den = fs->make<TH1F>("h_gendvv_den", "", 1000, 0, 4);
  h_gendvv_num = fs->make<TH1F>("h_gendvv_num", "", 1000, 0, 4);
  h_gendvv_fail = fs->make<TH1F>("h_gendvv_fail", "", 1000, 0, 4);
  h_gendvv_faill1htt_l1single = fs->make<TH1F>("h_gendvv_faill1htt_l1single", "", 1000, 0, 4);
  h_gendvv_faill1htt_l1single450 = fs->make<TH1F>("h_gendvv_faill1htt_l1single450", "", 1000, 0, 4);
  h_gendvv_faill1htt_l1single450ak = fs->make<TH1F>("h_gendvv_faill1htt_l1single450ak", "", 1000, 0, 4);
}

void MFVSignalEff2016HBug::analyze(const edm::Event& event, const edm::EventSetup&) {
  edm::Handle<mfv::TriggerFloats> triggerfloats;
  event.getByToken(triggerfloats_token, triggerfloats);

  if (triggerfloats->HLTdecisions[mfv::b_HLT_PFHT900] == -1 ||
      triggerfloats->HLTdecisions[mfv::b_HLT_PFJet450] == -1 ||
      triggerfloats->HLTdecisions[mfv::b_HLT_AK8PFJet450] == -1 ||
      triggerfloats->L1decisions[mfv::b_L1_SingleJet170] == -1 ||
      triggerfloats->L1decisions[mfv::b_L1_SingleJet180] == -1 || 
      triggerfloats->L1decisions[mfv::b_L1_SingleJet200] == -1)
    throw cms::Exception("Trigger", "one of the trigger bits was not found:")
      << " " << triggerfloats->HLTdecisions[mfv::b_HLT_PFHT900]
      << " " << triggerfloats->HLTdecisions[mfv::b_HLT_PFJet450]
      << " " << triggerfloats->HLTdecisions[mfv::b_HLT_AK8PFJet450]
      << " " << triggerfloats->L1decisions[mfv::b_L1_SingleJet170]
      << " " << triggerfloats->L1decisions[mfv::b_L1_SingleJet180] 
      << " " << triggerfloats->L1decisions[mfv::b_L1_SingleJet200];

  const float l1htts[3] = {triggerfloats->l1htt, triggerfloats->myhtt, triggerfloats->myhttwbug};
  const float use_l1htt = l1htts[which_l1htt];

  h_l1_check->Fill(use_l1htt, triggerfloats->L1decisions[l1htt_bit]);

  edm::Handle<reco::GenParticleCollection> gen_particles;
  event.getByToken(gen_particles_token, gen_particles);
  MCInteractionMFV3j mci;
  mci.Init(*gen_particles);
  if (!mci.Valid())
    throw cms::Exception("MCInteraction", "not a signal file?");

  const double gendvv = mci.dvv();
  h_gendvv_den->Fill(gendvv);

  if (use_l1htt >= l1htt_threshold)
    h_gendvv_num->Fill(gendvv);
  else {
    h_gendvv_fail->Fill(gendvv);
    const bool l1single = 
      triggerfloats->L1decisions[mfv::b_L1_SingleJet170] ||
      triggerfloats->L1decisions[mfv::b_L1_SingleJet180] ||
      triggerfloats->L1decisions[mfv::b_L1_SingleJet200];
    if (l1single) {
      h_gendvv_faill1htt_l1single->Fill(gendvv);
      if (triggerfloats->HLTdecisions[mfv::b_HLT_PFJet450])
        h_gendvv_faill1htt_l1single450->Fill(gendvv);
      if (triggerfloats->HLTdecisions[mfv::b_HLT_PFJet450] || triggerfloats->HLTdecisions[mfv::b_HLT_AK8PFJet450])
        h_gendvv_faill1htt_l1single450ak->Fill(gendvv);
    }      
  }
}

DEFINE_FWK_MODULE(MFVSignalEff2016HBug);
