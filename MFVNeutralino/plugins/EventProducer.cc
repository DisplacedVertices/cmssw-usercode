#include "CommonTools/Utils/interface/StringCutObjectSelector.h"
#include "DataFormats/Common/interface/TriggerResults.h"
#include "DataFormats/JetReco/interface/PFJetCollection.h"
#include "DataFormats/BeamSpot/interface/BeamSpot.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "FWCore/Common/interface/TriggerNames.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "SimDataFormats/PileupSummaryInfo/interface/PileupSummaryInfo.h"
#include "JMTucker/MFVNeutralino/interface/Event.h"
#include "JMTucker/MFVNeutralino/interface/MCInteractionMFV3j.h"
#include "JMTucker/Tools/interface/Utilities.h"

class MFVEventProducer : public edm::EDProducer {
public:
  explicit MFVEventProducer(const edm::ParameterSet&);
  void produce(edm::Event&, const edm::EventSetup&);
  
private:
  const edm::InputTag trigger_results_src;
  const edm::InputTag pfjets_src;
  const double jet_pt_min;
  const edm::InputTag primary_vertex_src;
  const bool is_mc;
  bool warned_non_mfv;
  const edm::InputTag gen_particles_src;
  const edm::InputTag jets_src;
  const std::string b_discriminator;
  const double b_discriminator_min;
  const edm::InputTag muons_src;
  const StringCutObjectSelector<pat::Muon> muon_semilep_selector;
  const StringCutObjectSelector<pat::Muon> muon_dilep_selector;
  const edm::InputTag electrons_src;
  const StringCutObjectSelector<pat::Electron> electron_semilep_selector;
  const StringCutObjectSelector<pat::Electron> electron_dilep_selector;
};

MFVEventProducer::MFVEventProducer(const edm::ParameterSet& cfg)
  : trigger_results_src(cfg.getParameter<edm::InputTag>("trigger_results_src")),
    pfjets_src(cfg.getParameter<edm::InputTag>("pfjets_src")),
    jet_pt_min(cfg.getParameter<double>("jet_pt_min")),
    primary_vertex_src(cfg.getParameter<edm::InputTag>("primary_vertex_src")),
    is_mc(cfg.getParameter<bool>("is_mc")),
    warned_non_mfv(false),
    gen_particles_src(cfg.getParameter<edm::InputTag>("gen_particles_src")),
    jets_src(cfg.getParameter<edm::InputTag>("jets_src")),
    b_discriminator(cfg.getParameter<std::string>("b_discriminator")),
    b_discriminator_min(cfg.getParameter<double>("b_discriminator_min")),
    muons_src(cfg.getParameter<edm::InputTag>("muons_src")),
    muon_semilep_selector(cfg.getParameter<std::string>("muon_semilep_cut")),
    muon_dilep_selector(cfg.getParameter<std::string>("muon_dilep_cut")),
    electrons_src(cfg.getParameter<edm::InputTag>("electrons_src")),
    electron_semilep_selector(cfg.getParameter<std::string>("electron_semilep_cut")),
    electron_dilep_selector(cfg.getParameter<std::string>("electron_dilep_cut"))
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

  if (is_mc) {
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

  edm::Handle<edm::TriggerResults> trigger_results;
  event.getByLabel(trigger_results_src, trigger_results);
  const edm::TriggerNames& trigger_names = event.triggerNames(*trigger_results);
  const size_t npaths = trigger_names.size();

  const bool simple_trigger[MFVEvent::n_trigger_paths] = { true, true, true };
  const std::string try_trigger[MFVEvent::n_trigger_paths] = {
    "HLT_QuadJet50_v", "HLT_IsoMu24_v", "HLT_HT750_v"
  };

  for (int itry = 0; itry < MFVEvent::n_trigger_paths; ++itry) {
    if (simple_trigger[itry]) {
      const std::string& trigger = try_trigger[itry];
    
      for (size_t ipath = 0; ipath < npaths; ++ipath) {
        const std::string path = trigger_names.triggerName(ipath);
        if (path.substr(0, trigger.size()) == trigger) {
          mevent->pass_trigger[itry] = trigger_results->accept(ipath);
          break;
        }
      }
    }
    else {
      assert(0);
    }
  }

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

  if (is_mc) {
    edm::Handle<std::vector<PileupSummaryInfo> > pileup;
    event.getByLabel("addPileupInfo", pileup);

    mevent->npu = -1;

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

  mevent->njets = mevent->nbtags = 0;
  mevent->jetpt4 = mevent->jetpt5 = mevent->jetpt6 = 0;
  mevent->jet_sum_ht = 0;

  edm::Handle<pat::JetCollection> jets;
  event.getByLabel(jets_src, jets);

  for (const pat::Jet& jet : *jets) {
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

    if (jet.bDiscriminator(b_discriminator) > b_discriminator_min)
      inc_uchar(mevent->nbtags);
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
