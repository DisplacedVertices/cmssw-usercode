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

#define NJETDISTS 4
#define NBJETDISTS 2
#define NBDISC 1
#define NLEPDISTS 2

class ResolutionsHistogrammer : public edm::EDAnalyzer {
public:
  explicit ResolutionsHistogrammer(const edm::ParameterSet&);
  ~ResolutionsHistogrammer();

private:
  const edm::EDGetTokenT<reco::VertexCollection> vertex_token;
  const edm::EDGetTokenT<pat::JetCollection> jets_token;
  const edm::EDGetTokenT<pat::MuonCollection> muons_token;
  const edm::EDGetTokenT<pat::ElectronCollection> electrons_token;
  const edm::EDGetTokenT<pat::METCollection> met_token;
  const StringCutObjectSelector<pat::Jet> jet_selector;
  const StringCutObjectSelector<pat::Muon> muon_selector;
  const StringCutObjectSelector<pat::Electron> electron_selector;
  const std::vector<std::string> b_discriminators;
  const std::vector<double> b_discriminator_mins;
  const double max_muon_dxy;
  const double max_muon_dz;
  const double max_electron_dxy;
  const double max_electron_dz;

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
  TH1F* JetNConstituents;
  TH1F* JetConstituentMaxPt;
  TH1F* JetNConstituent[NJETDISTS];
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
  TH1F* NElectrons;
  TH1F* RecoMuonsIso;
  TH1F* RecoElectronsIso;
  TH1F* RecoSemilepElectronsIso;
  TH1F* RecoDilepElectronsIso;

  BasicKinematicHists* RecoMuons;
  BasicKinematicHists* RecoMuon[NLEPDISTS];
  BasicKinematicHists* RecoElectrons;
  BasicKinematicHists* RecoElectron[NLEPDISTS];
};

namespace {
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

  double mag(double x, double y) {
    return sqrt(x*x + y*y);
  }

  TFileDirectory mkdir(edm::Service<TFileService>& fs, const TString& name) {
    return fs->mkdir(name.Data());
  }
}

ResolutionsHistogrammer::ResolutionsHistogrammer(const edm::ParameterSet& cfg)
  : vertex_token(consumes<reco::VertexCollection>(cfg.getParameter<edm::InputTag>("vertex_src"))),
    jets_token(consumes<pat::JetCollection>(cfg.getParameter<edm::InputTag>("jets_src"))),
    muons_token(consumes<pat::MuonCollection>(cfg.getParameter<edm::InputTag>("muons_src"))),
    electrons_token(consumes<pat::ElectronCollection>(cfg.getParameter<edm::InputTag>("electrons_src"))),
    met_token(consumes<pat::METCollection>(cfg.getParameter<edm::InputTag>("met_src"))),
    jet_selector(cfg.getParameter<std::string>("jet_cut")),
    muon_selector(cfg.getParameter<std::string>("muon_cut")),
    electron_selector(cfg.getParameter<std::string>("electron_cut")),
    b_discriminators(copy_N_elements(cfg.getParameter<std::vector<std::string> >("b_discriminators"), NBDISC)),
    b_discriminator_mins(copy_N_elements(cfg.getParameter<std::vector<double> >("b_discriminator_mins"), NBDISC)),
    max_muon_dxy(cfg.getParameter<double>("max_muon_dxy")),
    max_muon_dz(cfg.getParameter<double>("max_muon_dz")),
    max_electron_dxy(cfg.getParameter<double>("max_electron_dxy")),
    max_electron_dz(cfg.getParameter<double>("max_electron_dz"))
{
  TH1::SetDefaultSumw2();

  die_if_not(b_discriminators.size() == b_discriminator_mins.size(), "b_discriminators size %i != b_discriminator_mins size %i", int(b_discriminators.size()), int(b_discriminator_mins.size()));
  if (cfg.getParameter<std::vector<std::string> >("b_discriminators").size() > NBDISC)
    edm::LogWarning("ResolutionsHistogrammer") << "only first " << NBDISC << " b_discriminators will be used";
  edm::Service<TFileService> fs;
  bkh_factory = new BasicKinematicHistsFactory(fs);

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

  JetNConstituents = RecoJets->dir.make<TH1F>("NConstituents", ";number of constituents/jet;events", 60, 0, 60);
  JetConstituentMaxPt = RecoJets->dir.make<TH1F>("ConstituentMaxPt", ";max(constituents' p_{T})/jet;events/4 GeV", 50, 0, 200);
  for (int i = 0; i < NJETDISTS; ++i)
    JetNConstituent[i] = RecoJet[i]->dir.make<TH1F>("NConstituents", TString::Format(";number of constituents for jet #%i;events", i), 60, 0, 60);

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

  RecoMuons = bkh_factory->make("RecoMuons", "all reconstructed muons");
  RecoElectrons = bkh_factory->make("RecoElectrons", "all reconstructed electrons");
  NMuons = RecoMuons ->dir.make<TH1F>("NMuons", ";number of reconstructed muons;events", 10, 0, 10);
  NElectrons = RecoElectrons ->dir.make<TH1F>("NElectrons", ";number of reconstructed electrons;events", 10, 0, 10);
  RecoMuonsIso = RecoMuons ->dir.make<TH1F>("Iso", ";muon isolation;events/0.05", 40, 0, 2);
  RecoElectronsIso = RecoElectrons->dir.make<TH1F>("Iso", ";electron isolation;events/0.05", 40, 0, 2);

  BasicKinematicHists* bkhs[2] = { RecoMuons, RecoElectrons };
  for (int i = 0; i < 2; ++i) {
    bkhs[i]->BookPt(100, 0, 1000, "10");
    bkhs[i]->BookEta(40, -3, 3, "0.15");
    bkhs[i]->BookPhi(40, "0.157");
    bkhs[i]->BookDxy(100, -2, 2, "0.04");
    bkhs[i]->BookDz(100, -20, 20, "0.4");
    bkhs[i]->BookQ();
  }

  for (int i = 0; i < NLEPDISTS; ++i) {
    RecoMuon[i] = bkh_factory->make(TString::Format("RecoMuon/pt#%i", i), TString::Format("reconstructed muon #%i", i));
    RecoMuon[i]->BookPt(100, 0, 1000, "10");
    RecoMuon[i]->BookEta(40, -3, 3, "0.15");
    RecoMuon[i]->BookPhi(40, "0.157");
    RecoMuon[i]->BookDxy(100, -2, 2, "0.04");
    RecoMuon[i]->BookDz(100, -20, 20, "0.4");

    RecoElectron[i] = bkh_factory->make(TString::Format("RecoElectron/pt#%i", i), TString::Format("reconstructed electron #%i", i));
    RecoElectron[i]->BookPt(100, 0, 1000, "10");
    RecoElectron[i]->BookEta(40, -3, 3, "0.15");
    RecoElectron[i]->BookPhi(40, "0.157");
    RecoElectron[i]->BookDxy(100, -2, 2, "0.04");
    RecoElectron[i]->BookDz(100, -20, 20, "0.4");
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

ResolutionsHistogrammer::~ResolutionsHistogrammer() {
  delete bkh_factory;
}

double ResolutionsHistogrammer::GetWeight(const edm::Event& event) const {
  double weight = 1.;
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

void ResolutionsHistogrammer::analyze(const edm::Event& event, const edm::EventSetup&) {
  const bool is_mc = !event.isRealData();
  const double weight = is_mc ? GetWeight(event) : 1.;

  /////////////////////

  edm::Handle<reco::VertexCollection> vertices;
  event.getByToken(vertex_token, vertices);
  NVertices->Fill(vertices->size(), weight);

  /////////////////////

  edm::Handle<pat::JetCollection> jets;
  event.getByToken(jets_token, jets);

  double jet_ht = 0;
  int n_btags[NBDISC] = {0};

  int ijet = 0;
  for (const pat::Jet& jet : *jets) {
    if (jet_selector(jet)) {
      jet_ht += jet.pt();

      RecoJets->Pt ->Fill(jet.pt(),  weight);
      RecoJets->Eta->Fill(jet.eta(), weight);
      RecoJets->Phi->Fill(jet.phi(), weight);
      JetNConstituents->Fill(jet.nConstituents(), weight);
      double max_jet_const_pt = 0;
      for (const reco::PFCandidatePtr& pfcand : jet.getPFConstituents())
        if (pfcand->pt() > max_jet_const_pt)
          max_jet_const_pt = pfcand->pt();
      JetConstituentMaxPt->Fill(max_jet_const_pt);

      if (ijet < NJETDISTS) {
        RecoJet[ijet]->Pt ->Fill(jet.pt(), weight);
        RecoJet[ijet]->Eta->Fill(jet.eta(), weight);
        RecoJet[ijet]->Phi->Fill(jet.phi(), weight);
        JetNConstituent[ijet]->Fill(jet.nConstituents(), weight);
      }

      for (int j = 0; j < int(b_discriminators.size()); ++j) {
        const double b_disc = jet.bDiscriminator(b_discriminators[j]);
        const bool b_tagged = b_disc > b_discriminator_mins[j];
        JetBDiscs[j]->Fill(b_disc, weight);

        if (ijet < NJETDISTS)
          JetBDisc[j][ijet]->Fill(jet.bDiscriminator(b_discriminators[j]), weight);

        if (b_tagged) {
          RecoBJets[j]->Pt ->Fill(jet.pt(), weight);
          RecoBJets[j]->Eta->Fill(jet.eta(), weight);
          RecoBJets[j]->Phi->Fill(jet.phi(), weight);
	
          if (n_btags[j] < NBJETDISTS) {
            RecoBJet[j][n_btags[j]]->Pt ->Fill(jet.pt(), weight);
            RecoBJet[j][n_btags[j]]->Eta->Fill(jet.eta(), weight);
            RecoBJet[j][n_btags[j]]->Phi->Fill(jet.phi(), weight);
          }

          ++n_btags[j];
        }
      }

      double jet_pvsv_costheta = -999;
      const reco::SecondaryVertexTagInfo* svtag = jet.tagInfoSecondaryVertex("secondaryVertex");
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

      ++ijet;
    }
  }

  NJets->Fill(ijet);
  RecoJetsHT->Fill(jet_ht);

  for (int j = 0; j < int(b_discriminators.size()); ++j)
    NBTags[j]->Fill(n_btags[j], weight);

  /////////////////////

  edm::Handle<pat::MuonCollection> orig_muons;
  event.getByToken(muons_token, orig_muons);
  const std::vector<const pat::Muon*> muons = sort_pointers(*orig_muons);

  int imu = 0;
  for (const pat::Muon* muon : muons) {
    if (muon_selector(*muon)) {
      double dxy = -999, dz = -999;
      if (vertices->size() > 0) {
        dxy = muon->innerTrack()->dxy(vertices->at(0).position());
        dz  = muon->innerTrack()->dz (vertices->at(0).position());
      }
      if (fabs(dxy) < max_muon_dxy && fabs(dz) < max_muon_dz) {
        RecoMuons->Fill(muon, weight);
        RecoMuons->FillEx(dxy, dz, muon->charge(), weight);
    
        if (imu < NLEPDISTS) {
          RecoMuon[imu]->Fill(muon, weight);
          RecoMuon[imu]->FillEx(dxy, dz, muon->charge(), weight);
        }

        ++imu;
      }
    }
  }

  NMuons->Fill(imu);

  /////////////////////

  edm::Handle<pat::ElectronCollection> orig_electrons;
  event.getByToken(electrons_token, orig_electrons);
  const std::vector<const pat::Electron*> electrons = sort_pointers(*orig_electrons);

  int iel = 0;
  for (const pat::Electron* electron : electrons) {
    if (electron_selector(*electron)) {
      double dxy = -999, dz = -999;
      if (vertices->size() > 0) {
        dxy = electron->gsfTrack()->dxy(vertices->at(0).position());
        dz  = electron->gsfTrack()->dz (vertices->at(0).position());
      }
      if (fabs(dxy) < max_electron_dxy && fabs(dz) < max_electron_dz) {
        RecoElectrons->Fill(electron, weight);
        RecoElectrons->FillEx(dxy, dz, electron->charge(), weight);
    
        if (iel < NLEPDISTS) {
          RecoElectron[iel]->Fill(electron, weight);
          RecoElectron[iel]->FillEx(dxy, dz, electron->charge(), weight);
        }

        ++iel;
      }
    }
  }

  NElectrons->Fill(iel);

  /////////////////////

  edm::Handle<pat::METCollection> mets;
  event.getByToken(met_token, mets);
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

DEFINE_FWK_MODULE(ResolutionsHistogrammer);
