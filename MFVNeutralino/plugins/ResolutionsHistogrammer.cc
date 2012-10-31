#include "TH1F.h"
#include "TH2F.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "CommonTools/Utils/interface/StringCutObjectSelector.h"
#include "DataFormats/METReco/interface/GenMET.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/MET.h"
#include "DataFormats/PatCandidates/interface/Tau.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "RecoBTag/SecondaryVertex/interface/TrackKinematics.h"
#include "SimDataFormats/PileupSummaryInfo/interface/PileupSummaryInfo.h"
#include "JMTucker/Tools/interface/BasicKinematicHists.h"
#include "JMTucker/Tools/interface/Utilities.h"

#define NJETDISTS 20
#define NBJETDISTS 10
#define NBDISC 13
#define NLEPDISTS 5

class MFVNeutralinoResolutionsHistogrammer : public edm::EDAnalyzer {
public:
  explicit MFVNeutralinoResolutionsHistogrammer(const edm::ParameterSet&);
  ~MFVNeutralinoResolutionsHistogrammer();

private:
  const bool reweight_pileup;
  const double force_weight;
  const edm::InputTag vertex_src;
  const edm::InputTag met_src;
  const edm::InputTag jet_src;
  const std::vector<std::string> b_discriminators;
  const std::vector<double> b_discriminator_mins;
  const edm::InputTag muon_src;
  const double max_muon_dxy;
  const double max_muon_dz;
  const StringCutObjectSelector<pat::Muon> muon_semilep_selector;
  const StringCutObjectSelector<pat::Muon> muon_dilep_selector;
  const edm::InputTag electron_src;
  const double max_semilep_electron_dxy;
  const double max_dilep_electron_dxy;
  const StringCutObjectSelector<pat::Electron> electron_semilep_selector;
  const StringCutObjectSelector<pat::Electron> electron_dilep_selector;
  const bool print_info;

  void Book(edm::Service<TFileService>&);
  double GetWeight(const edm::Event&) const;

  virtual void analyze(const edm::Event&, const edm::EventSetup&);

  // Simplify booking simple histograms.
  BasicKinematicHistsFactory* bkh_factory;

  TH1F* NVertices;

  TH1F* NJets;
  TH1F* NBTags[NBDISC];
  TH1F* RecoJetsHT;
  TH1F* RecoJetsPVSVCosTheta;

  BasicKinematicHists* RecoJets;
  BasicKinematicHists* RecoJet[NJETDISTS];
  TH1F* JetBDiscs[NBDISC];
  TH1F* JetBDisc[NBDISC][NJETDISTS];
  BasicKinematicHists* RecoBJets[NBDISC];
  BasicKinematicHists* RecoBJet[NBDISC][NBJETDISTS];

  TH1F* JetPtRes;
  TH1F* JetPtResPtGt70;
  TH1F* JetPtRelRes;
  TH1F* JetPtRelResPtGt70;
  //TH2F* JetPtResVsPt;
  //TH2F* JetPtRelResVsPt;
  //TH2F* JetPtResVsEta;
  //TH2F* JetPtRelResVsEta;
  //TH2F* JetPtResVsNPV;
  //TH2F* JetPtRelResVsNPV;

  TH1F* RecoMETx;
  TH1F* RecoMETy;
  TH1F* RecoMET;
  TH1F* RecoMETSig;
  TH1F* RecoMETSigProb;

  TH1F* METxRes;
  TH1F* METyRes;
  TH1F* METRes;
  TH2F* METResVsSig;
  TH2F* METResVsJetHT;
  TH2F* METResVsNPV;

  TH1F* NMuons;
  TH1F* NSemilepMuons;
  TH1F* NDilepMuons;
  TH1F* NElectrons;
  TH1F* NSemilepElectrons;
  TH1F* NDilepElectrons;

  TH1F* RecoMuonsIso;
  TH1F* RecoSemilepMuonsIso;
  TH1F* RecoDilepMuonsIso;
  TH1F* RecoElectronsIso;
  TH1F* RecoSemilepElectronsIso;
  TH1F* RecoDilepElectronsIso;

  BasicKinematicHists* RecoMuons;
  BasicKinematicHists* RecoMuon[NLEPDISTS];
  BasicKinematicHists* RecoElectrons;
  BasicKinematicHists* RecoElectron[NLEPDISTS];
  BasicKinematicHists* RecoSemilepMuons;
  BasicKinematicHists* RecoSemilepMuon[NLEPDISTS];
  BasicKinematicHists* RecoSemilepElectrons;
  BasicKinematicHists* RecoSemilepElectron[NLEPDISTS];
  BasicKinematicHists* RecoDilepMuons;
  BasicKinematicHists* RecoDilepMuon[NLEPDISTS];
  BasicKinematicHists* RecoDilepElectrons;
  BasicKinematicHists* RecoDilepElectron[NLEPDISTS];
};

template <typename T>
std::vector<T> copy_N_elements(const std::vector<T>& src, const size_t N) {
  std::vector<T> res;
  const size_t ie = N < src.size() ? N : src.size();
  for (size_t i = 0; i < ie; ++i)
    res.push_back(src[i]);
  return res;
}

template <typename T>
bool greater_by_pt(const T* l, const T* r) {
  return l->pt() > r->pt();
}

template <typename T>
std::vector<const T*> sort_pointers(const std::vector<T>& src) {
  std::vector<const T*> res;
  for (size_t i = 0; i < src.size(); ++i)
    res.push_back(&src[i]);
  std::sort(res.begin(), res.end(), greater_by_pt<T>);
  return res;
}

MFVNeutralinoResolutionsHistogrammer::MFVNeutralinoResolutionsHistogrammer(const edm::ParameterSet& cfg)
  : reweight_pileup(cfg.getParameter<bool>("reweight_pileup")),
    force_weight(cfg.existsAs<double>("force_weight") ? cfg.getParameter<double>("force_weight") : -1),
    vertex_src(cfg.getParameter<edm::InputTag>("vertex_src")),
    met_src(cfg.getParameter<edm::InputTag>("met_src")),
    jet_src(cfg.getParameter<edm::InputTag>("jet_src")),
    b_discriminators(copy_N_elements(cfg.getParameter<std::vector<std::string> >("b_discriminators"), NBDISC)),
    b_discriminator_mins(copy_N_elements(cfg.getParameter<std::vector<double> >("b_discriminator_mins"), NBDISC)),
    muon_src(cfg.getParameter<edm::InputTag>("muon_src")),
    max_muon_dxy(cfg.getParameter<double>("max_muon_dxy")),
    max_muon_dz(cfg.getParameter<double>("max_muon_dz")),
    muon_semilep_selector(cfg.getParameter<std::string>("muon_semilep_cut")),
    muon_dilep_selector(cfg.getParameter<std::string>("muon_dilep_cut")),
    electron_src(cfg.getParameter<edm::InputTag>("electron_src")),
    max_semilep_electron_dxy(cfg.getParameter<double>("max_semilep_electron_dxy")),
    max_dilep_electron_dxy(cfg.getParameter<double>("max_dilep_electron_dxy")),
    electron_semilep_selector(cfg.getParameter<std::string>("electron_semilep_cut")),
    electron_dilep_selector(cfg.getParameter<std::string>("electron_dilep_cut")),
    print_info(cfg.getParameter<bool>("print_info"))
{
  die_if_not(b_discriminators.size() == b_discriminator_mins.size(), "b_discriminators size %i != b_discriminator_mins size %i", int(b_discriminators.size()), int(b_discriminator_mins.size()));
  if (cfg.getParameter<std::vector<std::string> >("b_discriminators").size() > NBDISC)
    edm::LogWarning("MFVNeutralinoResolutionsHistogrammer") << "only first " << NBDISC << " b_discriminators will be used";
  edm::Service<TFileService> fs;
  bkh_factory = new BasicKinematicHistsFactory(fs);
  Book(fs);
}

MFVNeutralinoResolutionsHistogrammer::~MFVNeutralinoResolutionsHistogrammer() {
  delete bkh_factory;
}

TFileDirectory mkdir(edm::Service<TFileService>& fs, const TString& name) {
  return fs->mkdir(name.Data());
}

void MFVNeutralinoResolutionsHistogrammer::Book(edm::Service<TFileService>& fs) {
  TH1::SetDefaultSumw2();

  NVertices = fs->make<TH1F>("NVertices", ";number of primary vertices;events", 75, 0, 75);

  RecoJets = bkh_factory->make("RecoJets", "all reconstructed jets");
  RecoJets->BookPt(100, 0, 1000, "10");
  RecoJets->BookEta(40, -3, 3, "0.15");
  RecoJets->BookPhi(40, "0.157");
  for (int i = 0; i < NJETDISTS; ++i) {
    RecoJet[i] = bkh_factory->make(TString::Format("RecoJet/pt#%i", i), TString::Format("reconstructed jet #%i", i));
    RecoJet[i]->BookPt(100, 0, 1000, "10");
    RecoJet[i]->BookEta(40, -3, 3, "0.15");
    RecoJet[i]->BookPhi(40, "0.157");
  }

  TFileDirectory RecoJets_dir = fs->mkdir("RecoJets");
  NJets                = RecoJets->dir.make<TH1F>("NJets", ";number of jets;events", 20, 0, 20);
  RecoJetsHT           = RecoJets->dir.make<TH1F>("SumHT", ";reconstructed jet H_{T} (GeV);events/50 GeV", 100, 0, 5000);
  RecoJetsPVSVCosTheta = RecoJets->dir.make<TH1F>("PVSVCosTheta", ";cos(angle between flight direction and jet);events/0.1", 20, -1, 1);

  JetPtRes          = RecoJets->dir.make<TH1F>("PtRes", ";reconstructed jet p_{T} resolution;events/5 GeV", 40, -100, 100);
  JetPtResPtGt70    = RecoJets->dir.make<TH1F>("PtResPtGt70", "gen p_{T} > 70 GeV;reconstructed jet p_{T} resolution;events/5 GeV", 40, -100, 100);
  JetPtRelRes       = RecoJets->dir.make<TH1F>("PtRelRes", ";reconstructed jet p_{T} relative resolution;events/0.1", 40, -2, 2);
  JetPtRelResPtGt70 = RecoJets->dir.make<TH1F>("PtRelResPtGt70", " gen p_{T} > 70 GeV;reconstructed jet p_{T} relative resolution;events/0.1", 40, -2, 2);

  for (int j = 0, je = int(b_discriminators.size()); j < je; ++j) {
    const char* bdisc_name = b_discriminators[j].c_str();
    TFileDirectory bdisc_dir = mkdir(fs, TString::Format("bdisc_%s", bdisc_name));
    NBTags[j]    = bdisc_dir.make<TH1F>("NBTags", TString::Format(";number of b-tagged (%s) jets;events",    bdisc_name), 20, 0, 20);
    JetBDiscs[j] = bdisc_dir.make<TH1F>("BDiscs", TString::Format(";b-discriminator (%s) value;events/0.1", bdisc_name), 200, -10, 10);
    
    RecoBJets[j] = bkh_factory->make(TString::Format("bdisc_%s/RecoBJets", bdisc_name), TString::Format("b-tagged (%s) jets", bdisc_name));
    RecoBJets[j]->BookPt(100, 0, 1000, "10");
    RecoBJets[j]->BookEta(40, -3, 3, "0.15");
    RecoBJets[j]->BookPhi(40, "0.157");
  
    for (int i = 0; i < NJETDISTS; ++i)
      JetBDisc[j][i] = mkdir(fs, TString::Format("RecoJet/pt#%i/bdisc_%s", i, bdisc_name)).make<TH1F>("BDisc", TString::Format(";jet #%i b-discriminator (%s) value;events/0.1", i, bdisc_name), 200, -10, 10);

    for (int i = 0; i < NBJETDISTS; ++i) {
      RecoBJet[j][i] = bkh_factory->make(TString::Format("bdisc_%s/RecoBJet/pt#%i", bdisc_name, i), TString::Format("b-tagged (%s) jet #%i", bdisc_name, i));
      RecoBJet[j][i]->BookPt(100, 0, 1000, "10");
      RecoBJet[j][i]->BookEta(40, -3, 3, "0.15");
      RecoBJet[j][i]->BookPhi(40, "0.157");
    }
  }

  RecoMuons        = bkh_factory->make("RecoMuons",        "all reconstructed muons");
  RecoSemilepMuons = bkh_factory->make("RecoSemilepMuons", "all reconstructed muons passing semilep cuts");
  RecoDilepMuons   = bkh_factory->make("RecoDilepMuons",   "all reconstructed muons passing dilep cuts");

  RecoElectrons        = bkh_factory->make("RecoElectrons",        "all reconstructed electrons");
  RecoSemilepElectrons = bkh_factory->make("RecoSemilepElectrons", "all reconstructed electrons passing semilep cuts");
  RecoDilepElectrons   = bkh_factory->make("RecoDilepElectrons",   "all reconstructed electrons passing dilep cuts");

  NMuons        = RecoMuons       ->dir.make<TH1F>("NMuons",        ";number of reconstructed muons;events",         10, 0, 10);
  NSemilepMuons = RecoSemilepMuons->dir.make<TH1F>("NSemilepMuons", ";number of reconstructed semilep muons;events", 10, 0, 10);
  NDilepMuons   = RecoDilepMuons  ->dir.make<TH1F>("NDilepMuons",   ";number of reconstructed dilep muons;events",   10, 0, 10);

  NElectrons        = RecoElectrons       ->dir.make<TH1F>("NElectrons",        ";number of reconstructed electrons;events",         10, 0, 10);
  NSemilepElectrons = RecoSemilepElectrons->dir.make<TH1F>("NSemilepElectrons", ";number of reconstructed semilep electrons;events", 10, 0, 10);
  NDilepElectrons   = RecoDilepElectrons  ->dir.make<TH1F>("NDilepElectrons",   ";number of reconstructed dilep electrons;events",   10, 0, 10);

  RecoMuonsIso        = RecoMuons       ->dir.make<TH1F>("Iso", ";muon isolation;events/0.05",         40, 0, 2);
  RecoSemilepMuonsIso = RecoSemilepMuons->dir.make<TH1F>("Iso", ";semilep muon isolation;events/0.05", 40, 0, 2);
  RecoDilepMuonsIso   = RecoDilepMuons  ->dir.make<TH1F>("Iso", ";dilep muon isolation;events/0.05",   40, 0, 2);

  RecoElectronsIso        = RecoElectrons       ->dir.make<TH1F>("Iso", ";electron isolation;events/0.05",         40, 0, 2);
  RecoSemilepElectronsIso = RecoSemilepElectrons->dir.make<TH1F>("Iso", ";semilep electron isolation;events/0.05", 40, 0, 2);
  RecoDilepElectronsIso   = RecoDilepElectrons  ->dir.make<TH1F>("Iso", ";dilep electron isolation;events/0.05",   40, 0, 2);

  BasicKinematicHists* bkhs[6] = { RecoMuons, RecoSemilepMuons, RecoDilepMuons, RecoElectrons, RecoSemilepElectrons, RecoDilepElectrons };
  for (int i = 0; i < 6; ++i) {
    bkhs[i]->BookPt(100, 0, 1000, "10");
    bkhs[i]->BookEta(40, -3, 3, "0.15");
    bkhs[i]->BookPhi(40, "0.157");
    bkhs[i]->BookDxy(40, -4, 4, "0.2");
    bkhs[i]->BookDz(40, -20, 20, "1");
    bkhs[i]->BookQ();
  }

  for (int i = 0; i < NLEPDISTS; ++i) {
    RecoMuon[i] = bkh_factory->make(TString::Format("RecoMuon/pt#%i", i), TString::Format("reconstructed muon #%i", i));
    RecoMuon[i]->BookPt(100, 0, 1000, "10");
    RecoMuon[i]->BookEta(40, -3, 3, "0.15");
    RecoMuon[i]->BookPhi(40, "0.157");
    RecoMuon[i]->BookDxy(40, -4, 4, "0.2");
    RecoMuon[i]->BookDz(40, -20, 20, "1");

    RecoSemilepMuon[i] = bkh_factory->make(TString::Format("RecoSemilepMuon/pt#%i", i), TString::Format("reconstructed semilep muon #%i", i));
    RecoSemilepMuon[i]->BookPt(100, 0, 1000, "10");
    RecoSemilepMuon[i]->BookEta(40, -3, 3, "0.15");
    RecoSemilepMuon[i]->BookPhi(40, "0.157");
    RecoSemilepMuon[i]->BookDxy(40, -4, 4, "0.2");
    RecoSemilepMuon[i]->BookDz(40, -20, 20, "1");

    RecoDilepMuon[i] = bkh_factory->make(TString::Format("RecoDilepMuon/pt#%i", i), TString::Format("reconstructed dilep muon #%i", i));
    RecoDilepMuon[i]->BookPt(100, 0, 1000, "10");
    RecoDilepMuon[i]->BookEta(40, -3, 3, "0.15");
    RecoDilepMuon[i]->BookPhi(40, "0.157");
    RecoDilepMuon[i]->BookDxy(40, -4, 4, "0.2");
    RecoDilepMuon[i]->BookDz(40, -20, 20, "1");

    RecoElectron[i] = bkh_factory->make(TString::Format("RecoElectron/pt#%i", i), TString::Format("reconstructed electron #%i", i));
    RecoElectron[i]->BookPt(100, 0, 1000, "10");
    RecoElectron[i]->BookEta(40, -3, 3, "0.15");
    RecoElectron[i]->BookPhi(40, "0.157");
    RecoElectron[i]->BookDxy(40, -4, 4, "0.2");
    RecoElectron[i]->BookDz(40, -20, 20, "1");

    RecoSemilepElectron[i] = bkh_factory->make(TString::Format("RecoSemilepElectron/pt#%i", i), TString::Format("reconstructed semilep electron #%i", i));
    RecoSemilepElectron[i]->BookPt(100, 0, 1000, "10");
    RecoSemilepElectron[i]->BookEta(40, -3, 3, "0.15");
    RecoSemilepElectron[i]->BookPhi(40, "0.157");
    RecoSemilepElectron[i]->BookDxy(40, -4, 4, "0.2");
    RecoSemilepElectron[i]->BookDz(40, -20, 20, "1");

    RecoDilepElectron[i] = bkh_factory->make(TString::Format("RecoDilepElectron/pt#%i", i), TString::Format("reconstructed dilep electron #%i", i));
    RecoDilepElectron[i]->BookPt(100, 0, 1000, "10");
    RecoDilepElectron[i]->BookEta(40, -3, 3, "0.15");
    RecoDilepElectron[i]->BookPhi(40, "0.157");
    RecoDilepElectron[i]->BookDxy(40, -4, 4, "0.2");
    RecoDilepElectron[i]->BookDz(40, -20, 20, "1");
  }

  TFileDirectory met_dir = fs->mkdir("RecoMET");
  RecoMETx = met_dir.make<TH1F>("RecoMETx", ";reconstructed METx (GeV);events/10 GeV", 40, -200, 200);
  RecoMETy = met_dir.make<TH1F>("RecoMETy", ";reconstructed METy (GeV);events/10 GeV", 40, -200, 200);
  RecoMET = met_dir.make<TH1F>("RecoMET", ";reconstructed MET (GeV);events/10 GeV", 30, 0, 300);
  RecoMETSig = met_dir.make<TH1F>("RecoMETSig", ";MET significance;events/0.2", 100, 0, 20);
  RecoMETSigProb = met_dir.make<TH1F>("RecoMETSigProb", ";P(MET significance);events/0.05", 20, 0, 1);

  METxRes = met_dir.make<TH1F>("METxRes", ";METx resolution (GeV);events/10 GeV", 20, -100, 100);
  METyRes = met_dir.make<TH1F>("METyRes", ";METy resolution (GeV);events/10 GeV", 20, -100, 100);
  METRes = met_dir.make<TH1F>("METRes", ";MET resolution (GeV);events/10 GeV", 20, 0, 200);
  METResVsSig = met_dir.make<TH2F>("METResVsSig", ";MET significance;MET resolution (GeV)", 40, 0, 20, 20, 0, 200);
  METResVsJetHT = met_dir.make<TH2F>("METResVsJetHT", ";reconstructed jet H_{T};MET resolution (GeV)", 40, 0, 2000, 20, 0, 200);
  METResVsNPV = met_dir.make<TH2F>("METResVsNPV", ";number of primary vertices;MET resolution (GeV)", 25, 0, 75, 20, 0, 200);
}

float mag(double x, double y) {
  return sqrt(x*x + y*y);
}

double MFVNeutralinoResolutionsHistogrammer::GetWeight(const edm::Event& event) const {
  double weight = 1.;
  if (force_weight > 0)
    weight *= force_weight;
  // JMTBAD PU reweighting
  //  edm::Handle<std::vector<PileupSummaryInfo> > pileup;
  //  event.getByLabel("addPileupInfo", pileup);
  //  for (std::vector<PileupSummaryInfo>::const_iterator psi = pileup->begin(), end = pileup->end(); psi != end; ++psi) {
  //    const int bx = psi->getBunchCrossing();
  //    die_if_not(bx >= -1 && bx <= 1, "pileup BX not -1, 0, or 1: %i", bx);
  //    nt->sim_pileup_num_int     [bx+1] = psi->getPU_NumInteractions();
  //    nt->sim_pileup_true_num_int[bx+1] = psi->getTrueNumInteractions();
  //  }
  return weight;
}

void MFVNeutralinoResolutionsHistogrammer::analyze(const edm::Event& event, const edm::EventSetup&) {
  const bool is_mc = !event.isRealData();
  const double weight = is_mc ? GetWeight(event) : 1.;

  /////////////////////

  edm::Handle<reco::VertexCollection> vertices;
  event.getByLabel(vertex_src, vertices);
  NVertices->Fill(vertices->size(), weight);

  /////////////////////

  edm::Handle<pat::JetCollection> jets;
  event.getByLabel(jet_src, jets);

  const int n_jets = int(jets->size());
  NJets->Fill(n_jets, weight);

  double jet_ht = 0;
  int n_btags[NBDISC] = {0};

  for (int i = 0; i < n_jets; ++i) {
    if (i > 0)
      die_if_not(jets->at(i).pt() <= jets->at(i-1).pt(), "input jets not sorted by decreasing pT");
    const pat::Jet& jet = jets->at(i);
    jet_ht += jet.pt();

    RecoJets->Pt ->Fill(jet.pt(),  weight);
    RecoJets->Eta->Fill(jet.eta(), weight);
    RecoJets->Phi->Fill(jet.phi(), weight);

    if (i < NJETDISTS) {
      RecoJet[i]->Pt ->Fill(jet.pt(), weight);
      RecoJet[i]->Eta->Fill(jet.eta(), weight);
      RecoJet[i]->Phi->Fill(jet.phi(), weight);
    }

    for (int j = 0; j < int(b_discriminators.size()); ++j) {
      const double b_disc = jet.bDiscriminator(b_discriminators[j]);
      const bool b_tagged = b_disc > b_discriminator_mins[j];
      JetBDiscs[j]->Fill(b_disc, weight);

      if (i < NJETDISTS)
      	JetBDisc[j][i]->Fill(jet.bDiscriminator(b_discriminators[j]), weight);

      if (b_tagged) {
	RecoBJets[j]->Pt ->Fill(jet.pt(), weight);
	RecoBJets[j]->Eta->Fill(jet.eta(), weight);
	RecoBJets[j]->Phi->Fill(jet.phi(), weight);
	
	if (n_btags[j] < NJETDISTS) {
	  RecoBJet[j][n_btags[j]]->Pt ->Fill(jet.pt(), weight);
	  RecoBJet[j][n_btags[j]]->Eta->Fill(jet.eta(), weight);
	  RecoBJet[j][n_btags[j]]->Phi->Fill(jet.phi(), weight);
	}

	n_btags[j] += 1;
      }
    }

    double jet_pvsv_costheta = -999;
    const reco::SecondaryVertexTagInfo* svtag = jet.tagInfoSecondaryVertex("secondaryVertexMaxDR2p5");
    if (vertices->size() > 0 && svtag && svtag->nVertices() > 0) {
      const GlobalVector& flight_dir = svtag->flightDirection(0);
      const GlobalVector jet_mom(jet.momentum().x(), jet.momentum().y(), jet.momentum().z());
      jet_pvsv_costheta = jet_mom.dot(flight_dir)/jet_mom.mag()/flight_dir.mag();
    }
    RecoJetsPVSVCosTheta->Fill(jet_pvsv_costheta, weight);

    if (is_mc) {
      if (jet.genJet() != 0) {
	JetPtRes->Fill(jet.pt() - jet.genJet()->pt(), weight);
	JetPtRelRes->Fill(jet.pt()/jet.genJet()->pt() - 1, weight);
	if (jet.genJet()->pt() > 70) {
	  JetPtResPtGt70->Fill(jet.pt() - jet.genJet()->pt(), weight);
	  JetPtRelResPtGt70->Fill(jet.pt()/jet.genJet()->pt() - 1, weight);
	}
      }

      //const int gen_jet_parton_flavor = jet.partonFlavour();
      //if (jet.genParton() != 0) {
      //  const int gen_parton_id = jet.genParton()->pdgId();
      //}
    }
  }

  RecoJetsHT->Fill(jet_ht);

  for (int j = 0; j < int(b_discriminators.size()); ++j)
    NBTags[j]->Fill(n_btags[j], weight);

  /////////////////////

  edm::Handle<pat::MuonCollection> orig_muons;
  event.getByLabel(muon_src, orig_muons);
  const std::vector<const pat::Muon*> muons = sort_pointers(*orig_muons);
  NMuons->Fill(muons.size(), weight);

  int n_semilep_muons = 0;
  int n_dilep_muons = 0;

  for (int i = 0; i < int(muons.size()); ++i) {
    const pat::Muon& muon = *muons.at(i);
    RecoMuons->Fill(&muon, weight);
    double dxy = -999, dz = -999;
    if (vertices->size() > 0) {
      dxy = muon.innerTrack()->dxy(vertices->at(0).position());
      dz  = muon.innerTrack()->dz (vertices->at(0).position());
    }
    RecoMuons->FillEx(dxy, dz, muon.charge(), weight);
    
    if (i < NLEPDISTS) {
      RecoMuon[i]->Fill(&muon, weight);
      RecoMuon[i]->FillEx(dxy, dz, muon.charge(), weight);
    }
      
    const bool muon_pass_semilep = muon_semilep_selector(muon) && fabs(dxy) < max_muon_dxy && fabs(dz) < max_muon_dz; // impact parameter cuts wrt PV not doable in StringCutSelector
    const bool muon_pass_dilep   = muon_dilep_selector  (muon);

    if (muon_pass_semilep) {
      RecoSemilepMuons->Fill(&muon, weight);
      RecoSemilepMuons->FillEx(dxy, dz, muon.charge(), weight);

      if (n_semilep_muons < NLEPDISTS) {
	RecoSemilepMuon[n_semilep_muons]->Fill(&muon, weight);
	RecoSemilepMuon[n_semilep_muons]->FillEx(dxy, dz, muon.charge(), weight);
      }

      n_semilep_muons += 1;
    }
	
    if (muon_pass_dilep) {
      RecoDilepMuons->Fill(&muon, weight);
      RecoDilepMuons->FillEx(dxy, dz, muon.charge(), weight);

      if (n_dilep_muons < NLEPDISTS) {
	RecoDilepMuon[n_dilep_muons]->Fill(&muon, weight);
	RecoDilepMuon[n_dilep_muons]->FillEx(dxy, dz, muon.charge(), weight);
      }

      n_dilep_muons += 1;
    }

    //if (muon.genParticle()) {
    //}
  }

  NSemilepMuons->Fill(n_semilep_muons);
  NDilepMuons  ->Fill(n_dilep_muons);

  /////////////////////

  edm::Handle<pat::ElectronCollection> orig_electrons;
  event.getByLabel(electron_src, orig_electrons);
  const std::vector<const pat::Electron*> electrons = sort_pointers(*orig_electrons);
  NElectrons->Fill(electrons.size(), weight);

  int n_semilep_electrons = 0;
  int n_dilep_electrons = 0;

  for (int i = 0; i < int(electrons.size()); ++i) {
    const pat::Electron& electron = *electrons.at(i);
    RecoElectrons->Fill(&electron, weight);
    double dxy = -999, dz = -999;
    if (vertices->size() > 0) {
      dxy = electron.gsfTrack()->dxy(vertices->at(0).position());
      dz  = electron.gsfTrack()->dz (vertices->at(0).position());
    }
    RecoElectrons->FillEx(dxy, dz, electron.charge(), weight);
    
    if (i < NLEPDISTS) {
      RecoElectron[i]->Fill(&electron, weight);
      RecoElectron[i]->FillEx(dxy, dz, electron.charge(), weight);
    }

    const bool electron_pass_semilep = electron_semilep_selector(electron) && fabs(dxy) < max_semilep_electron_dxy;
    const bool electron_pass_dilep   = electron_dilep_selector  (electron) && fabs(dxy) < max_dilep_electron_dxy;

    if (electron_pass_semilep) {
      RecoSemilepElectrons->Fill(&electron, weight);
      RecoSemilepElectrons->FillEx(dxy, dz, electron.charge(), weight);

      if (n_semilep_electrons < NLEPDISTS) {
	RecoSemilepElectron[n_semilep_electrons]->Fill(&electron, weight);
	RecoSemilepElectron[n_semilep_electrons]->FillEx(dxy, dz, electron.charge(), weight);
      }

      n_semilep_electrons += 1;
    }
	
    if (electron_pass_dilep) {
      RecoDilepElectrons->Fill(&electron, weight);
      RecoDilepElectrons->FillEx(dxy, dz, electron.charge(), weight);

      if (n_dilep_electrons < NLEPDISTS) {
	RecoDilepElectron[n_dilep_electrons]->Fill(&electron, weight);
	RecoDilepElectron[n_dilep_electrons]->FillEx(dxy, dz, electron.charge(), weight);
      }

      n_dilep_electrons += 1;
    }

    //if (electron.genParticle()) {
    //}
  }

  NSemilepElectrons->Fill(n_semilep_electrons);
  NDilepElectrons  ->Fill(n_dilep_electrons);

  /////////////////////

  edm::Handle<pat::METCollection> mets;
  event.getByLabel(met_src, mets);
  const pat::MET& met = mets->at(0);

  RecoMETx->Fill(met.px(), weight);
  RecoMETy->Fill(met.py(), weight);
  RecoMET->Fill(met.pt(), weight);
  const bool met_sig_ok = met.getSignificanceMatrix()(0,0) < 1e10 && met.getSignificanceMatrix()(1,1) < 1e10;
  const double met_sig = met_sig_ok ? met.significance() : -999;
  if (met_sig_ok) {
    RecoMETSig->Fill(met_sig, weight);
    RecoMETSigProb->Fill(TMath::Prob(met_sig, 2));
  }

  if (is_mc) {
    die_if_not(met.genMET(), "MET does not have gen MET pointer");
    const float met_res = mag(met.px() - met.genMET()->px(), met.py() - met.genMET()->py());
    METxRes->Fill(met.px() - met.genMET()->px(), weight);
    METyRes->Fill(met.py() - met.genMET()->py(), weight);
    METRes->Fill(met_res, weight);
    if (met_sig_ok)
      METResVsSig->Fill(met_sig, met_res, weight);
    METResVsJetHT->Fill(jet_ht, met_res, weight);
    METResVsNPV->Fill(vertices->size(), met_res, weight);
  }
}

DEFINE_FWK_MODULE(MFVNeutralinoResolutionsHistogrammer);
