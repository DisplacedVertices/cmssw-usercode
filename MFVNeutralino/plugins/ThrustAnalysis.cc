#include "TTree.h"
#include "TSystem.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/HepMCCandidate/interface/GenParticleFwd.h"
#include "DataFormats/JetReco/interface/GenJet.h"
#include "DataFormats/METReco/interface/GenMET.h"
#include "DataFormats/METReco/interface/GenMETCollection.h"
#include "DataFormats/Math/interface/LorentzVector.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "PhysicsTools/CandUtils/interface/Thrust.h"
#include "JMTucker/MFVNeutralino/interface/MCInteractionMFV3j.h"
#include "JMTucker/Tools/interface/GenUtilities.h"
#include "JMTucker/Tools/interface/Thrust2D.h"

class MFVThrustAnalysis : public edm::EDAnalyzer {
public:
  explicit MFVThrustAnalysis(const edm::ParameterSet&);

private:
  virtual void analyze(const edm::Event&, const edm::EventSetup&);

  void fillVecs(const reco::Candidate* genp, // initial candidate
		TLorentzVector* p4,
		TVector3* vtx,
		const reco::Candidate* genpFinal = 0); // final candidate (used for b's)
  
  const reco::GenJet* matchedGenJet(const reco::GenParticle*, const reco::GenJetCollection&);

  template <typename T>
  void fillCandVec(std::vector<T>& vec, const T* cand, bool ptNotP=false) {
    if (!cand) return;
    T tmp = *cand;
    if (ptNotP)
      tmp.setPz(0);
    vec.push_back(tmp);
  }

  template <typename ThrustCalculator, typename Candidate>
  void calcThrust(const std::vector<Candidate>& cands, TVector3& axis, double& thrust) {
    ThrustCalculator calc(cands.begin(), cands.end());
    axis.SetXYZ(calc.axis().x(), calc.axis().y(), calc.axis().z());
    thrust = calc.thrust();
  }

  const edm::InputTag gen_particles_src;
  const edm::InputTag gen_jets_src;
  const edm::InputTag gen_met_src;
  const double pt_cut;
  const double eta_cut;
  const double loose_pt_cut;
  const double loose_eta_cut;
  const bool prints;

  TTree* m_tree;

  TLorentzVector* m_p4GHad;
  TLorentzVector* m_p4BgHad;
  TLorentzVector* m_p4SHad;
  TLorentzVector* m_p4THad;
  TLorentzVector* m_p4BtHad;
  TLorentzVector* m_p4Q0;
  TLorentzVector* m_p4Q1;
  TLorentzVector* m_p4GLep;
  TLorentzVector* m_p4BgLep;
  TLorentzVector* m_p4SLep;
  TLorentzVector* m_p4TLep;
  TLorentzVector* m_p4BtLep;
  TLorentzVector* m_p4Lep;
  TLorentzVector* m_p4Nu;

  TVector3* m_vtxGHad;
  TVector3* m_vtxBgHad;
  TVector3* m_vtxSHad;
  TVector3* m_vtxTHad;
  TVector3* m_vtxBtHad;
  TVector3* m_vtxQ0;
  TVector3* m_vtxQ1;
  TVector3* m_vtxGLep;
  TVector3* m_vtxBgLep;
  TVector3* m_vtxSLep;
  TVector3* m_vtxTLep;
  TVector3* m_vtxBtLep;
  TVector3* m_vtxLep;
  TVector3* m_vtxNu;

  TVector3* m_vthr3;
  Double_t m_thr3;
  TVector3* m_vthr2;
  Double_t m_thr2;

  TLorentzVector* m_p4jBgHad;
  TLorentzVector* m_p4jSHad;
  TLorentzVector* m_p4jBtHad;
  TLorentzVector* m_p4jQ0;
  TLorentzVector* m_p4jQ1;
  TLorentzVector* m_p4jBgLep;
  TLorentzVector* m_p4jSLep;
  TLorentzVector* m_p4jBtLep;
  TLorentzVector* m_p4MET;

  TVector3* m_vthr3j;
  Double_t m_thr3j;
  TVector3* m_vthr2j;
  Double_t m_thr2j;

  std::vector<TLorentzVector>* m_vp4jQOther;
  std::vector<TLorentzVector>* m_vp4jBOther;
  std::vector<TVector3>* m_vvtxQOther;
  std::vector<TVector3>* m_vvtxBOther;

  TVector3* m_vthr3jAll;
  Double_t m_thr3jAll;
  TVector3* m_vthr2jAll;
  Double_t m_thr2jAll;

  TVector3* m_beamspot;
};

MFVThrustAnalysis::MFVThrustAnalysis(const edm::ParameterSet& cfg)
  : gen_particles_src(cfg.getParameter<edm::InputTag>("gen_particles_src")),
    gen_jets_src(cfg.getParameter<edm::InputTag>("gen_jets_src")),
    gen_met_src(cfg.getParameter<edm::InputTag>("gen_met_src")),
    pt_cut(cfg.getParameter<double>("pt_cut")),
    eta_cut(cfg.getParameter<double>("eta_cut")),
    loose_pt_cut(cfg.getParameter<double>("loose_pt_cut")),
    loose_eta_cut(cfg.getParameter<double>("loose_eta_cut")),
    prints(cfg.getUntrackedParameter<bool>("prints", false))
{
  gSystem->Load("./dict_C.so");

  edm::Service<TFileService> fs;
  m_tree = fs->make<TTree>("tree", "");

  m_p4GHad = new TLorentzVector;
  m_p4BgHad = new TLorentzVector;
  m_p4SHad = new TLorentzVector;
  m_p4THad = new TLorentzVector;
  m_p4BtHad = new TLorentzVector;
  m_p4Q0 = new TLorentzVector;
  m_p4Q1 = new TLorentzVector;
  m_p4GLep = new TLorentzVector;
  m_p4BgLep = new TLorentzVector;
  m_p4SLep = new TLorentzVector;
  m_p4TLep = new TLorentzVector;
  m_p4BtLep = new TLorentzVector;
  m_p4Lep = new TLorentzVector;
  m_p4Nu = new TLorentzVector;

  m_vtxGHad = new TVector3;
  m_vtxBgHad = new TVector3;
  m_vtxSHad = new TVector3;
  m_vtxTHad = new TVector3;
  m_vtxBtHad = new TVector3;
  m_vtxQ0 = new TVector3;
  m_vtxQ1 = new TVector3;
  m_vtxGLep = new TVector3;
  m_vtxBgLep = new TVector3;
  m_vtxSLep = new TVector3;
  m_vtxTLep = new TVector3;
  m_vtxBtLep = new TVector3;
  m_vtxLep = new TVector3;
  m_vtxNu = new TVector3;

  m_vthr3 = new TVector3;
  m_vthr2 = new TVector3;

  m_p4jBgHad = new TLorentzVector;
  m_p4jSHad = new TLorentzVector;
  m_p4jBtHad = new TLorentzVector;
  m_p4jQ0 = new TLorentzVector;
  m_p4jQ1 = new TLorentzVector;
  m_p4jBgLep = new TLorentzVector;
  m_p4jSLep = new TLorentzVector;
  m_p4jBtLep = new TLorentzVector;
  m_p4MET = new TLorentzVector;

  m_vthr3j = new TVector3;
  m_vthr2j = new TVector3;

  m_vp4jQOther = new std::vector<TLorentzVector>;
  m_vp4jBOther = new std::vector<TLorentzVector>;
  m_vvtxQOther = new std::vector<TVector3>;
  m_vvtxBOther = new std::vector<TVector3>;

  m_vthr3jAll = new TVector3;
  m_vthr2jAll = new TVector3;

  m_beamspot = new TVector3;

  m_tree->Branch("p4GHad", &m_p4GHad);
  m_tree->Branch("p4BgHad", &m_p4BgHad);
  m_tree->Branch("p4SHad", &m_p4SHad);
  m_tree->Branch("p4THad", &m_p4THad);
  m_tree->Branch("p4BtHad", &m_p4BtHad);
  m_tree->Branch("p4Q0", &m_p4Q0);
  m_tree->Branch("p4Q1", &m_p4Q1);
  m_tree->Branch("p4GLep", &m_p4GLep);
  m_tree->Branch("p4BgLep", &m_p4BgLep);
  m_tree->Branch("p4SLep", &m_p4SLep);
  m_tree->Branch("p4TLep", &m_p4TLep);
  m_tree->Branch("p4BtLep", &m_p4BtLep);
  m_tree->Branch("p4Lep", &m_p4Lep);
  m_tree->Branch("p4Nu", &m_p4Nu);

  m_tree->Branch("vtxGHad", &m_vtxGHad);
  m_tree->Branch("vtxBgHad", &m_vtxBgHad);
  m_tree->Branch("vtxSHad", &m_vtxSHad);
  m_tree->Branch("vtxTHad", &m_vtxTHad);
  m_tree->Branch("vtxBtHad", &m_vtxBtHad);
  m_tree->Branch("vtxQ0", &m_vtxQ0);
  m_tree->Branch("vtxQ1", &m_vtxQ1);
  m_tree->Branch("vtxGLep", &m_vtxGLep);
  m_tree->Branch("vtxBgLep", &m_vtxBgLep);
  m_tree->Branch("vtxSLep", &m_vtxSLep);
  m_tree->Branch("vtxTLep", &m_vtxTLep);
  m_tree->Branch("vtxBtLep", &m_vtxBtLep);
  m_tree->Branch("vtxLep", &m_vtxLep);
  m_tree->Branch("vtxNu", &m_vtxNu);

  m_tree->Branch("vthr3", &m_vthr3);
  m_tree->Branch("thr3", &m_thr3, "thr3/D");
  m_tree->Branch("vthr2", &m_vthr2);
  m_tree->Branch("thr2", &m_thr2, "thr2/D");

  m_tree->Branch("p4jBgHad", &m_p4jBgHad);
  m_tree->Branch("p4jSHad", &m_p4jSHad);
  m_tree->Branch("p4jBtHad", &m_p4jBtHad);
  m_tree->Branch("p4jQ0", &m_p4jQ0);
  m_tree->Branch("p4jQ1", &m_p4jQ1);
  m_tree->Branch("p4jBgLep", &m_p4jBgLep);
  m_tree->Branch("p4jSLep", &m_p4jSLep);
  m_tree->Branch("p4jBtLep", &m_p4jBtLep);
  m_tree->Branch("p4MET", &m_p4MET);

  m_tree->Branch("vthr3j", &m_vthr3j);
  m_tree->Branch("thr3j", &m_thr3j, "thr3j/D");
  m_tree->Branch("vthr2j", &m_vthr2j);
  m_tree->Branch("thr2j", &m_thr2j, "thr2j/D");

  m_tree->Branch("vp4jQOther", &m_vp4jQOther, 32000, 0);
  m_tree->Branch("vp4jBOther", &m_vp4jBOther, 32000, 0);
  m_tree->Branch("vvtxQOther", &m_vvtxQOther, 32000, 0);
  m_tree->Branch("vvtxBOther", &m_vvtxBOther, 32000, 0);

  m_tree->Branch("vthr3jAll", &m_vthr3jAll);
  m_tree->Branch("thr3jAll", &m_thr3jAll, "thr3jAll/D");
  m_tree->Branch("vthr2jAll", &m_vthr2jAll);
  m_tree->Branch("thr2jAll", &m_thr2jAll, "thr2jAll/D");

  m_tree->Branch("beamspot", &m_beamspot);
}

void MFVThrustAnalysis::fillVecs(const reco::Candidate* genp, TLorentzVector* p4, TVector3* vtx, const reco::Candidate* genpFinal) {
  if (!genp) {
    *p4 = TLorentzVector();
    *vtx = TVector3();
  }

  p4->SetXYZT(genp->px(), genp->py(), genp->pz(), genp->energy());

  const reco::Candidate* for_vtx = genp;
  if (genpFinal) {
    // get position of first non-b daughter
    int ndau = genpFinal->numberOfDaughters();
    for (int i = 0; i < ndau; ++i) {
      const reco::Candidate* dau = genpFinal->daughter(i);
      int dauId = abs(dau->pdgId());

      if (dauId != 5) {
	// If dau is a B hadron, get its first daughter
	if (dauId > 10000)
	  dauId = dauId % 10000;
	  
	while ((dauId < 1000 && dauId / 100  == 5) ||
	       (dauId > 1000 && dauId / 1000 == 5))
	{
	  dau = final_candidate(dau, 3);
	  int ndau2 = dau->numberOfDaughters();
	  for (int j = 0; j < ndau2; ++j) {
	    const reco::Candidate* dau2 = dau->daughter(i);
	    if (abs(dau2->pdgId()) != dauId) {
	      dau = dau2;
	      dauId = abs(dau->pdgId());
	      if (dauId > 10000)
		dauId = dauId % 10000;
	      break;
	    }
	  }
	}

	for_vtx = dau;
	break;
      }
    }
  }

  vtx->SetXYZ(for_vtx->vx(), for_vtx->vy(), for_vtx->vz());
}

const reco::GenJet* MFVThrustAnalysis::matchedGenJet(const reco::GenParticle* genp, const reco::GenJetCollection& genJets) {
  // Find closest GenJet with dR < 0.4.
  const reco::GenJet* matchedGenJet = 0;

  if (genp) {
    double bestDR = 999.;
    for (unsigned i = 0, n = genJets.size(); i < n; ++i) {
      double dR = deltaR(genp->p4(), genJets[i].p4());
      if (dR < 0.4 && dR < bestDR) {
	matchedGenJet = &genJets[i];
	bestDR = dR;
      }
    }
  }

  return matchedGenJet;
}

void MFVThrustAnalysis::analyze(const edm::Event& event, const edm::EventSetup&) {
  *m_p4GHad = TLorentzVector();
  *m_p4BgHad = TLorentzVector();
  *m_p4SHad = TLorentzVector();
  *m_p4THad = TLorentzVector();
  *m_p4BtHad = TLorentzVector();
  *m_p4Q0 = TLorentzVector();
  *m_p4Q1 = TLorentzVector();
  *m_p4GLep = TLorentzVector();
  *m_p4BgLep = TLorentzVector();
  *m_p4SLep = TLorentzVector();
  *m_p4TLep = TLorentzVector();
  *m_p4BtLep = TLorentzVector();
  *m_p4Lep = TLorentzVector();
  *m_p4Nu = TLorentzVector();

  *m_vtxGHad = TVector3();
  *m_vtxBgHad = TVector3();
  *m_vtxSHad = TVector3();
  *m_vtxTHad = TVector3();
  *m_vtxBtHad = TVector3();
  *m_vtxQ0 = TVector3();
  *m_vtxQ1 = TVector3();
  *m_vtxGLep = TVector3();
  *m_vtxBgLep = TVector3();
  *m_vtxSLep = TVector3();
  *m_vtxTLep = TVector3();
  *m_vtxBtLep = TVector3();
  *m_vtxLep = TVector3();
  *m_vtxNu = TVector3();

  *m_vthr3 = TVector3();
  m_thr3 = 0.;
  *m_vthr2 = TVector3();
  m_thr2 = 0.;

  *m_p4jBgHad = TLorentzVector();
  *m_p4jSHad = TLorentzVector();
  *m_p4jBtHad = TLorentzVector();
  *m_p4jQ0 = TLorentzVector();
  *m_p4jQ1 = TLorentzVector();
  *m_p4jBgLep = TLorentzVector();
  *m_p4jSLep = TLorentzVector();
  *m_p4jBtLep = TLorentzVector();
  *m_p4MET = TLorentzVector();

  *m_vthr3j = TVector3();
  m_thr3j = 0.;
  *m_vthr2j = TVector3();
  m_thr2j = 0.;

  m_vp4jQOther->clear();
  m_vp4jBOther->clear();
  m_vvtxQOther->clear();
  m_vvtxBOther->clear();

  *m_vthr3jAll = TVector3();
  m_thr3jAll = 0.;
  *m_vthr2jAll = TVector3();
  m_thr2jAll = 0.;

  edm::Handle<reco::GenParticleCollection> gen_particles;
  event.getByLabel(gen_particles_src, gen_particles); 
  edm::Handle<reco::GenJetCollection> gen_jets;
  event.getByLabel(gen_jets_src, gen_jets);
  edm::Handle<reco::GenMETCollection> gen_mets;
  event.getByLabel(gen_met_src, gen_mets);
  const reco::GenMET& gen_met = gen_mets->at(0);

  std::vector<reco::GenParticle> thr3Cands;
  std::vector<reco::GenJet> thr3jCands;
  const reco::GenJet* jBgHad = 0;
  const reco::GenJet* jSHad  = 0;
  const reco::GenJet* jBtHad = 0;
  const reco::GenJet* jQ0    = 0;
  const reco::GenJet* jQ1    = 0;
  const reco::GenJet* jBgLep = 0;
  const reco::GenJet* jSLep  = 0;
  const reco::GenJet* jBtLep = 0;

  *m_beamspot = TVector3();

  // ~~~~~~~~~~ GenParticle ~~~~~~~~~~

  MCInteractionMFV3j mci;
  mci.Init(*gen_particles, *gen_jets, gen_met);
  if (mci.Valid()) {
    int ihad = mci.decay_type[0] == 3 ? 0 : 1;
    int ilep = 1 - ihad;

    fillVecs(mci.lsps             [ihad],     m_p4GHad,  m_vtxGHad);
    fillVecs(mci.bottoms          [ihad],     m_p4BgHad, m_vtxBgHad, final_candidate(mci.bottoms[ihad], 3));
    fillVecs(mci.stranges         [ihad],     m_p4SHad,  m_vtxSHad);
    fillVecs(mci.tops             [ihad],     m_p4THad,  m_vtxTHad);
    fillVecs(mci.bottoms_from_tops[ihad],     m_p4BtHad, m_vtxBtHad, final_candidate(mci.bottoms_from_tops[ihad], 3));
    fillVecs(mci.W_daughters      [ihad][0],  m_p4Q0,    m_vtxQ0);
    fillVecs(mci.W_daughters      [ihad][1],  m_p4Q1,    m_vtxQ1);
    fillVecs(mci.lsps             [ilep],     m_p4GLep,  m_vtxGLep);
    fillVecs(mci.bottoms          [ilep],     m_p4BgLep, m_vtxBgLep, final_candidate(mci.bottoms[ilep], 3));
    fillVecs(mci.stranges         [ilep],     m_p4SLep,  m_vtxSLep);
    fillVecs(mci.tops             [ilep],     m_p4TLep,  m_vtxTLep);
    fillVecs(mci.bottoms_from_tops[ilep],     m_p4BtLep, m_vtxBtLep, final_candidate(mci.bottoms_from_tops[ilep], 3));
    fillVecs(mci.W_daughters      [ilep][0],  m_p4Lep,   m_vtxLep);
    fillVecs(mci.W_daughters      [ilep][1],  m_p4Nu,    m_vtxNu);

    if (prints)
      std::cout << "GHad  " << mci.lsps             [ihad]   ->vertex() << "\n"
		<< "BgHad " << mci.bottoms          [ihad]   ->vertex() << "\n"
		<< "SHad  " << mci.stranges         [ihad]   ->vertex() << "\n"
		<< "THad  " << mci.tops             [ihad]   ->vertex() << "\n"
		<< "BtHad " << mci.bottoms_from_tops[ihad]   ->vertex() << "\n"
		<< "Q0    " << mci.W_daughters      [ihad][0]->vertex() << "\n"
		<< "Q1    " << mci.W_daughters      [ihad][1]->vertex() << "\n"
		<< "GLep  " << mci.lsps             [ilep]   ->vertex() << "\n"
		<< "BgLep " << mci.bottoms          [ilep]   ->vertex() << "\n"
		<< "SLep  " << mci.stranges         [ilep]   ->vertex() << "\n"
		<< "TLep  " << mci.tops             [ilep]   ->vertex() << "\n"
		<< "BtLep " << mci.bottoms_from_tops[ilep]   ->vertex() << "\n"
		<< "Lep   " << mci.W_daughters      [ilep][0]->vertex() << "\n"
		<< "Nu    " << mci.W_daughters      [ilep][1]->vertex() << "\n";

    *m_beamspot = *m_vtxGHad;

    fillCandVec(thr3Cands, mci.bottoms          [ihad]);
    fillCandVec(thr3Cands, mci.stranges         [ihad]);
    fillCandVec(thr3Cands, mci.bottoms_from_tops[ihad]);
    fillCandVec(thr3Cands, mci.W_daughters      [ihad][0]);
    fillCandVec(thr3Cands, mci.W_daughters      [ihad][1]);
    fillCandVec(thr3Cands, mci.bottoms          [ilep]);
    fillCandVec(thr3Cands, mci.stranges         [ilep]);
    fillCandVec(thr3Cands, mci.bottoms_from_tops[ilep]);
    fillCandVec(thr3Cands, mci.W_daughters      [ilep][0]); // omit neutrino

    calcThrust<Thrust>  (thr3Cands, *m_vthr3, m_thr3);
    calcThrust<Thrust2D>(thr3Cands, *m_vthr2, m_thr2);

    // ~~~~~~~~~~ Matched GenJets ~~~~~~~~~~

    // Find matching GenJets
    jBgHad = matchedGenJet(mci.bottoms          [ihad],    *gen_jets);
    jSHad  = matchedGenJet(mci.stranges         [ihad],    *gen_jets);
    jBtHad = matchedGenJet(mci.bottoms_from_tops[ihad],    *gen_jets);
    jQ0    = matchedGenJet(mci.W_daughters      [ihad][0], *gen_jets);
    jQ1    = matchedGenJet(mci.W_daughters      [ihad][1], *gen_jets);
    jBgLep = matchedGenJet(mci.bottoms          [ilep],    *gen_jets);
    jSLep  = matchedGenJet(mci.stranges         [ilep],    *gen_jets);
    jBtLep = matchedGenJet(mci.bottoms_from_tops[ilep],    *gen_jets);

    TVector3 vtxTmp;
    fillVecs(jBgHad, m_p4jBgHad, &vtxTmp);
    fillVecs(jSHad,  m_p4jSHad,  &vtxTmp);
    fillVecs(jBtHad, m_p4jBtHad, &vtxTmp);
    fillVecs(jQ0,    m_p4jQ0,    &vtxTmp);
    fillVecs(jQ1,    m_p4jQ1,    &vtxTmp);
    fillVecs(jBgLep, m_p4jBgLep, &vtxTmp);
    fillVecs(jSLep,  m_p4jSLep,  &vtxTmp);
    fillVecs(jBtLep, m_p4jBtLep, &vtxTmp);

    // the met object has pz = px ?
    m_p4MET->SetXYZT(gen_met.px(), gen_met.py(), 0, gen_met.energy());

    fillCandVec(thr3jCands, jBgHad);
    fillCandVec(thr3jCands, jSHad);
    fillCandVec(thr3jCands, jBtHad);
    fillCandVec(thr3jCands, jQ0);
    fillCandVec(thr3jCands, jQ1);
    fillCandVec(thr3jCands, jBgLep);
    fillCandVec(thr3jCands, jSLep);
    fillCandVec(thr3jCands, jBtLep);

    // don't forget the lepton
    if (mci.W_daughters[ilep][0])
      thr3jCands.push_back(reco::GenJet(mci.W_daughters[ilep][0]->p4(),
					mci.W_daughters[ilep][0]->vertex(),
					reco::GenJet::Specific(),
					reco::Jet::Constituents()));

    calcThrust<Thrust>  (thr3jCands, *m_vthr3j, m_thr3j);
    calcThrust<Thrust2D>(thr3jCands, *m_vthr2j, m_thr2j);
  }
  else {
    // Require one and only one lepton passing pt and eta cuts
    for (int i = 0, n = gen_particles->size(); i < n; ++i) {
      const reco::GenParticle* gen = &gen_particles->at(i);

      if (abs(gen->pdgId()) == 6) // if not mfv signal sample, assume ttbar
	m_beamspot->SetXYZ(gen->vx(), gen->vy(), gen->vz());
      else if (is_lepton(gen) &&
	       !is_neutrino(gen) &&
	       gen->mother() &&
	       fabs(gen->mother()->pdgId()) == 24 && // to get first copy of lepton
	       gen->pt() > pt_cut &&
	       fabs(gen->eta()) < eta_cut)
      {
	if (thr3jCands.size())
	  // > 1 lepton, so discard event
	  return;
	else {
	  fillVecs(gen, m_p4Lep, m_vtxLep);
	  thr3jCands.push_back(reco::GenJet(gen->p4(),
					    gen->vertex(),
					    reco::GenJet::Specific(),
					    reco::Jet::Constituents()));
	}
      }
    }

    if (!thr3jCands.size())
      return;
  }

  // ~~~~~~~~~~ All GenJets ~~~~~~~~~~

  // Find GenJets (passing pt and eta cuts) matched to generated
  // b quarks not from gluino decay.
  std::vector<const reco::GenJet*> vbjOther;
  std::vector<reco::GenJet> thr3jAllCands;

  for (unsigned i = 0, n = gen_particles->size(); i < n; ++i) {
    const reco::GenParticle& gen = gen_particles->at(i);
    if (abs(gen.pdgId()) == 5 &&
	gen.mother() &&
	abs(gen.mother()->pdgId()) != 5 &&
	&gen != mci.bottoms[0] &&
	&gen != mci.bottoms[1] &&
	&gen != mci.bottoms_from_tops[0] &&
	&gen != mci.bottoms_from_tops[1])
    {
      const reco::GenJet* match = matchedGenJet(&gen, *gen_jets);
      if (match &&
	  match != jBgHad &&
	  match != jSHad &&
	  match != jBtHad &&
	  match != jQ0 &&
	  match != jQ1 &&
	  match != jBgLep &&
	  match != jSLep &&
	  match != jBtLep &&
	  match->pt() > loose_pt_cut &&
	  fabs(match->eta()) < loose_eta_cut)
      {	   
	vbjOther.push_back(match);
	fillCandVec(thr3jAllCands, match);

	TLorentzVector p4tmp;
	TVector3 vtxtmp;
	fillVecs(match, &p4tmp, &vtxtmp, final_candidate(match, 3));
	m_vp4jBOther->push_back(p4tmp);
	m_vvtxBOther->push_back(vtxtmp);
      }
    }
  }

  // get the unmatched GenJets passing pt and eta cuts
  for (unsigned i = 0, n = gen_jets->size(); i < n; ++i) {
    const reco::GenJet* gen_jet = &gen_jets->at(i);

    if (gen_jet != jBgHad &&
	gen_jet != jSHad &&
	gen_jet != jBtHad &&
	gen_jet != jQ0 &&
	gen_jet != jQ1 &&
	gen_jet != jBgLep &&
	gen_jet != jSLep &&
	gen_jet != jBtLep &&
	gen_jet->pt() > loose_pt_cut &&
	fabs(gen_jet->eta()) < loose_eta_cut &&
	find(vbjOther.begin(), vbjOther.end(), gen_jet) == vbjOther.end())
    {
      fillCandVec(thr3jAllCands, gen_jet);

      TLorentzVector p4tmp;
      TVector3 vtxtmp;
      fillVecs(gen_jet, &p4tmp, &vtxtmp);
      m_vp4jQOther->push_back(p4tmp);
      //m_vvtxQOther->push_back(vtxtmp); // always at origin
      m_vvtxQOther->push_back(*m_beamspot);
    }
  }

  // Calculate thrusts with all jets + lepton with pt and eta cuts
  for (int i = 0, n = thr3jCands.size(); i < n; ++i)
    if (thr3jCands[i].pt() > pt_cut && fabs(thr3jCands[i].eta()) < eta_cut)
      thr3jAllCands.push_back(thr3jCands[i]);

  calcThrust<Thrust>  (thr3jAllCands, *m_vthr3jAll, m_thr3jAll);
  calcThrust<Thrust2D>(thr3jAllCands, *m_vthr2jAll, m_thr2jAll);

  if (prints) {
    m_beamspot->Print();
    m_vtxSHad->Print();
  }

  if (mci.Valid() ||
      (m_vp4jQOther->size() > 2 && m_vp4jBOther->size() > 2))
    m_tree->Fill();
}

DEFINE_FWK_MODULE(MFVThrustAnalysis);
