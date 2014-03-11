#include "CMGTools/External/interface/PileupJetIdentifier.h"
#include "CommonTools/Utils/interface/StringCutObjectSelector.h"
#include "DataFormats/Common/interface/TriggerResults.h"
#include "DataFormats/JetReco/interface/PFJetCollection.h"
#include "DataFormats/BeamSpot/interface/BeamSpot.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/MET.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "DataFormats/Math/interface/LorentzVector.h"
#include "FWCore/Common/interface/TriggerNames.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "SimDataFormats/PileupSummaryInfo/interface/PileupSummaryInfo.h"
#include "JMTucker/MFVNeutralinoFormats/interface/Event.h"
#include "JMTucker/MFVNeutralino/interface/EventTools.h"
#include "JMTucker/MFVNeutralino/interface/MCInteractionMFV3j.h"
#include "JMTucker/Tools/interface/TriggerHelper.h"
#include "JMTucker/Tools/interface/Utilities.h"
#include "CondFormats/JetMETObjects/interface/JetCorrectionUncertainty.h"
#include "CondFormats/JetMETObjects/interface/SimpleJetCorrectionUncertainty.h"

class JECPATProducer : public edm::EDProducer {
public:
  explicit JECPATProducer(const edm::ParameterSet&);
private:
  void produce(edm::Event&, const edm::EventSetup&);
  const edm::InputTag jet_src;
  const bool jes_uncertainty;
  const bool jes_way;
  const bool jer_way;
};

JECPATProducer::JECPATProducer(const edm::ParameterSet& cfg)
  : jet_src(cfg.getParameter<edm::InputTag>("jet_src")),
    jes_uncertainty(cfg.getParameter<bool>("jes_uncertainty")),
    jes_way(cfg.getParameter<bool>("jes_way")),
    jer_way(cfg.getParameter<bool>("jer_way"))
{
  produces<pat::JetCollection>();
}

void JECPATProducer::produce(edm::Event& event, const edm::EventSetup& setup) {
  edm::Handle<pat::JetCollection> jets;
  event.getByLabel(jet_src, jets);
  
  std::auto_ptr<pat::JetCollection> mjets(new pat::JetCollection);
  JetCorrectionUncertainty *jecUnc_ = new JetCorrectionUncertainty("Summer13_V4_MC_Uncertainty_AK5PF.txt");
  //std::cout<<"Making Jets"<<std::endl;

  for(std::vector<pat::Jet>::const_iterator jet = jets->begin(); jet != jets->end(); ++jet) {

    float uncertainty = -1000;
    float scaled_pt = 999;
    pat::Jet mjet = *jet;
    auto mp4 = jet->p4();

    if(jes_uncertainty){
      jecUnc_->setJetEta( jet->eta() );
      jecUnc_->setJetPt( jet->pt() ); // here you must use the CORRECTED jet pt
      uncertainty = jecUnc_->getUncertainty(jes_way);
      if(jes_way)
	scaled_pt = (1+uncertainty)*jet->pt();
      else
	scaled_pt = (1-uncertainty)*jet->pt();
    }
    else{
      float JER_scale_up,JER_scale_down;
      JER_scale_up=JER_scale_down=-999;
      if( fabs(jet->eta()) < 0.5 ){
	JER_scale_up   = 1.115;
	JER_scale_down = 0.990;
      }
      if( fabs(jet->eta()) < 1.1 && fabs(jet->eta()) > 0.5 ){
	JER_scale_up   = 1.114;
	JER_scale_down = 1.001;
	}
      if( fabs(jet->eta()) < 1.7 && fabs(jet->eta()) > 1.1 ){
	JER_scale_up   = 1.161;
	JER_scale_down = 1.032;
      }
      if( fabs(jet->eta()) < 2.3 && fabs(jet->eta()) > 1.7 ){
	JER_scale_up   = 1.228;
	JER_scale_down = 1.042;
      }
      if( fabs(jet->eta()) < 5.0 && fabs(jet->eta()) > 2.3 ){
	JER_scale_up   = 1.488;
	JER_scale_down = 1.089;
      }
      float gen_jet_pt = -999;
      if(jet->genJet())
	gen_jet_pt = jet->genJet()->pt();
      else {
	std::cout<<"no gen jet"<<std::endl;
	continue;
      }
      if(jer_way)
	scaled_pt = gen_jet_pt + JER_scale_up*(jet->pt() - gen_jet_pt);
      else
	scaled_pt = gen_jet_pt + JER_scale_down*(jet->pt() - gen_jet_pt);
    }
    
    mp4.SetPx(scaled_pt*TMath::Cos(jet->phi()));
    mp4.SetPy(scaled_pt*TMath::Sin(jet->phi()));
    mjet.setP4(mp4);
    std::cout<<"Jet Pt "<<jet->pt()<<", Mod jet Pt "<<mjet.pt()<<std::endl; 
    if(jet->pt()==mjet.pt())
      std::cout<<"EQUAL"<<std::endl;
    mjets->push_back(mjet);

    
  }
  event.put(mjets);

}

DEFINE_FWK_MODULE(JECPATProducer);
