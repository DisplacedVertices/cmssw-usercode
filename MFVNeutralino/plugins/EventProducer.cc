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

class MFVEventProducer : public edm::EDProducer {
public:
  explicit MFVEventProducer(const edm::ParameterSet&);
  void produce(edm::Event&, const edm::EventSetup&);
  
private:
  const edm::InputTag trigger_results_src;
  const edm::InputTag cleaning_results_src;
  const edm::InputTag pfjets_src;
  const double jet_pt_min;
  const edm::InputTag primary_vertex_src;
  const edm::InputTag gen_particles_src;
  const edm::InputTag jets_src;
  const edm::InputTag met_src;
  const std::string b_discriminator;
  const std::vector<double> b_discriminator_mins;
  const edm::InputTag muons_src;
  const StringCutObjectSelector<pat::Muon> muon_semilep_selector;
  const StringCutObjectSelector<pat::Muon> muon_dilep_selector;
  const edm::InputTag electrons_src;
  const StringCutObjectSelector<pat::Electron> electron_semilep_selector;
  const StringCutObjectSelector<pat::Electron> electron_dilep_selector;
  bool warned_non_mfv;
};

MFVEventProducer::MFVEventProducer(const edm::ParameterSet& cfg)
  : trigger_results_src(cfg.getParameter<edm::InputTag>("trigger_results_src")),
    cleaning_results_src(cfg.getParameter<edm::InputTag>("cleaning_results_src")),
    pfjets_src(cfg.getParameter<edm::InputTag>("pfjets_src")),
    jet_pt_min(cfg.getParameter<double>("jet_pt_min")),
    primary_vertex_src(cfg.getParameter<edm::InputTag>("primary_vertex_src")),
    gen_particles_src(cfg.getParameter<edm::InputTag>("gen_particles_src")),
    jets_src(cfg.getParameter<edm::InputTag>("jets_src")),
    met_src(cfg.getParameter<edm::InputTag>("met_src")),
    b_discriminator(cfg.getParameter<std::string>("b_discriminator")),
    b_discriminator_mins(cfg.getParameter<std::vector<double> >("b_discriminator_mins")),
    muons_src(cfg.getParameter<edm::InputTag>("muons_src")),
    muon_semilep_selector(cfg.getParameter<std::string>("muon_semilep_cut")),
    muon_dilep_selector(cfg.getParameter<std::string>("muon_dilep_cut")),
    electrons_src(cfg.getParameter<edm::InputTag>("electrons_src")),
    electron_semilep_selector(cfg.getParameter<std::string>("electron_semilep_cut")),
    electron_dilep_selector(cfg.getParameter<std::string>("electron_dilep_cut")),
    warned_non_mfv(false)
{
  produces<MFVEvent>();
}

void MFVEventProducer::produce(edm::Event& event, const edm::EventSetup& setup) {
  std::auto_ptr<MFVEvent> mevent(new MFVEvent);

  edm::Handle<reco::BeamSpot> beamspot;
  event.getByLabel("offlineBeamSpot", beamspot);
  mevent->bsx = beamspot->x0();
  mevent->bsy = beamspot->y0();
  mevent->bsz = beamspot->z0();

  edm::Handle<reco::VertexCollection> primary_vertices;
  event.getByLabel(primary_vertex_src, primary_vertices);
  const reco::Vertex* primary_vertex = 0;
  if (primary_vertices->size())
    primary_vertex = &primary_vertices->at(0);

  //////////////////////////////////////////////////////////////////////

  mevent->gen_valid = false;

  if (!event.isRealData()) {
    edm::Handle<reco::GenParticleCollection> gen_particles;
    event.getByLabel(gen_particles_src, gen_particles);

    MCInteractionMFV3j mci;
    mci.Init(*gen_particles);
    if (!mci.Valid()) {
      if (!warned_non_mfv) {
        edm::LogWarning("MCInteractionMFV3j") << "invalid! hope this is not an MFV signal file";
        warned_non_mfv = true;
      }
    }
    else {
      mevent->gen_valid = true;
      std::vector<const reco::GenParticle*> lsp_partons;
      for (int i = 0; i < 2; ++i) {
        mevent->gen_lsp_pt  [i] = mci.lsps[i]->pt();
        mevent->gen_lsp_eta [i] = mci.lsps[i]->eta();
        mevent->gen_lsp_phi [i] = mci.lsps[i]->phi();
        mevent->gen_lsp_mass[i] = mci.lsps[i]->mass();

        mevent->gen_lsp_decay[i*3+0] = mci.stranges[i]->vx();
        mevent->gen_lsp_decay[i*3+1] = mci.stranges[i]->vy();
        mevent->gen_lsp_decay[i*3+2] = mci.stranges[i]->vz();

        lsp_partons.push_back(mci.stranges[i]);
        lsp_partons.push_back(mci.bottoms[i]);
        lsp_partons.push_back(mci.bottoms_from_tops[i]);

        mevent->gen_decay_type[i] = mci.decay_type[i];
        if (mci.decay_type[i] == 3) {
          lsp_partons.push_back(mci.W_daughters[i][0]);
          lsp_partons.push_back(mci.W_daughters[i][1]);
        }
      } 

      mevent->gen_partons_in_acc = 0;
      for (const reco::GenParticle* p : lsp_partons) 
        if (p->pt() > jet_pt_min && fabs(p->eta()) < 2.5)
          inc_uchar(mevent->gen_partons_in_acc);
    }
  }

  //////////////////////////////////////////////////////////////////////

  TriggerHelper trig_helper(event, trigger_results_src);
  mfv::trigger_decision(trig_helper, mevent->pass_trigger);

  TriggerHelper trig_helper_cleaning(event, cleaning_results_src);
  const std::string cleaning_paths[mfv::n_clean_paths] = { // JMTBAD take from PATTupleSelection_cfg
    "All",
    "hltPhysicsDeclared",
    "FilterOutScraping",
    "goodOfflinePrimaryVertices",
    "HBHENoiseFilter",
    "CSCTightHaloFilter",
    "hcalLaserEventFilter",
    "EcalDeadCellTriggerPrimitiveFilter",
    "trackingFailureFilter",
    "eeBadScFilter",
    "ecalLaserCorrFilter",
    "tobtecfakesfilter",
    "logErrorTooManyClusters",
    "logErrorTooManySeeds",
    "logErrorTooManySeedsDefault",
    "logErrorTooManySeedsMainIterations",
    "logErrorTooManyTripletsPairs",
    "logErrorTooManyTripletsPairsMainIterations",
    "manystripclus53X",
    "toomanystripclus53X"
  };
  for (int i = 0; i < mfv::n_clean_paths; ++i)
    mevent->pass_clean[i] = trig_helper_cleaning.pass("eventCleaning" + cleaning_paths[i]);

  mevent->passoldskim = 
    trig_helper_cleaning.pass("pHadronic") ||
    trig_helper_cleaning.pass("pSemileptonic") ||
    trig_helper_cleaning.pass("pDileptonic");
  
  //////////////////////////////////////////////////////////////////////

  edm::Handle<reco::PFJetCollection> pfjets;
  event.getByLabel(pfjets_src, pfjets);

  mevent->npfjets = 0;

  for (const reco::PFJet& jet : *pfjets) {
    if (jet.pt() > jet_pt_min &&
        fabs(jet.eta()) < 2.5 &&
        jet.numberOfDaughters() > 1 &&
        (fabs(jet.eta()) >= 2.4 || (jet.chargedEmEnergyFraction() < 0.99 && jet.chargedHadronEnergyFraction() > 0. && jet.chargedMultiplicity() > 0)) &&
        jet.neutralHadronEnergyFraction() < 0.90 &&
        jet.neutralEmEnergyFraction() < 0.90) {

      inc_uchar(mevent->npfjets);

      if (mevent->npfjets == 4)
        mevent->pfjetpt4 = jet.pt();
      else if (mevent->npfjets == 5)
        mevent->pfjetpt5 = jet.pt();
      else if (mevent->npfjets == 6)
        mevent->pfjetpt6 = jet.pt();
    }
  }

  //////////////////////////////////////////////////////////////////////

  mevent->npu = -1;

  if (!event.isRealData()) {
    edm::Handle<std::vector<PileupSummaryInfo> > pileup;
    event.getByLabel("addPileupInfo", pileup);

    for (std::vector<PileupSummaryInfo>::const_iterator psi = pileup->begin(), end = pileup->end(); psi != end; ++psi)
      if (psi->getBunchCrossing() == 0)
        mevent->npu = psi->getTrueNumInteractions();
  }

  //////////////////////////////////////////////////////////////////////
  
  mevent->npv = int2uchar(primary_vertices->size());

  if (primary_vertex != 0) {
    mevent->pvx = primary_vertex->x();
    mevent->pvy = primary_vertex->y();
    mevent->pvz = primary_vertex->z();
    mevent->pv_ntracks = int2uchar_clamp(primary_vertex->nTracks());
    mevent->pv_sumpt2 = 0;
    for (auto trki = primary_vertex->tracks_begin(), trke = primary_vertex->tracks_end(); trki != trke; ++trki) {
      double trkpt = (*trki)->pt();
      mevent->pv_sumpt2 += trkpt * trkpt;
    }
  }

  //////////////////////////////////////////////////////////////////////

  mevent->njets = 0;
  mevent->jetpt4 = mevent->jetpt5 = mevent->jetpt6 = 0;
  mevent->jet_sum_ht = 0;
  for (int i = 0; i < 3; ++i) {
    mevent->njetsnopu[i] = 0;
    mevent->nbtags[i] = 0;
  }

  edm::Handle<pat::JetCollection> jets;
  event.getByLabel(jets_src, jets);

  edm::Handle<pat::METCollection> mets;
  event.getByLabel(met_src, mets);
  const pat::MET& met = mets->at(0);

  mevent->metx = met.px();
  mevent->mety = met.py();
  if (met.getSignificanceMatrix()(0,0) < 1e10 && met.getSignificanceMatrix()(1,1) < 1e10)
    mevent->metsig = met.significance();
  else
    mevent->metsig = -999;
  mevent->metdphimin = 1e99;

  for (int jjet = 0, jjete = int(jets->size()); jjet < jjete; ++jjet) {
    const pat::Jet& jet = jets->at(jjet);
    if (jet.pt() < jet_pt_min)
      continue;

    inc_uchar(mevent->njets);

    if (mevent->njets == 4)
      mevent->jetpt4 = jet.pt();
    else if (mevent->njets == 5)
      mevent->jetpt5 = jet.pt();
    else if (mevent->njets == 6)
      mevent->jetpt6 = jet.pt();

    mevent->jet_sum_ht += jet.pt();

    if (jjet < 4) {
      double deltatsum = 0;
      for (int ijet = 0, ijete = int(jets->size()); ijet < ijete; ++ijet) {
        if (ijet == jjet)
          continue;
        const pat::Jet& jeti = jets->at(ijet);
        deltatsum += pow(jet.px() * jeti.py() - jet.py() * jeti.px(), 2);
      }
      const double deltat = 0.1 * sqrt(deltatsum) / jet.pt();
      const double dphi = fabs(reco::deltaPhi(jet, met)/asin(deltat/met.pt()));
      if (dphi < mevent->metdphimin)
        mevent->metdphimin = dphi;
    }
      
    for (int i = 0; i < 3; ++i)
      if (jet.bDiscriminator(b_discriminator) > b_discriminator_mins[i])
        inc_uchar(mevent->nbtags[i]);
  }

  //////////////////////////////////////////////////////////////////////

  for (int i = 0; i < 3; ++i)
    mevent->nmu[i] = mevent->nel[i] = 0;

  edm::Handle<pat::MuonCollection> muons;
  event.getByLabel(muons_src, muons);

  mevent->nmu[0] = int2uchar(muons->size());
  for (const pat::Muon& muon : *muons) {
    if (muon_semilep_selector(muon))
      inc_uchar(mevent->nmu[1]);
    if (muon_dilep_selector(muon))
      inc_uchar(mevent->nmu[2]);
  }
  
  edm::Handle<pat::ElectronCollection> electrons;
  event.getByLabel(electrons_src, electrons);
  
  mevent->nel[0] = int2uchar(electrons->size());
  for (const pat::Electron& electron : *electrons) {
    if (electron_semilep_selector(electron))
      inc_uchar(mevent->nel[1]);
    if (electron_dilep_selector(electron))
      inc_uchar(mevent->nel[2]);
  }
  
  //////////////////////////////////////////////////////////////////////

  event.put(mevent);
}

DEFINE_FWK_MODULE(MFVEventProducer);
