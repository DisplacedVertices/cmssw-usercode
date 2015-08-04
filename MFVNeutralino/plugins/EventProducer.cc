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
#include "HLTrigger/HLTcore/interface/HLTConfigProvider.h"
#include "PhysicsTools/SelectorUtils/interface/JetIDSelectionFunctor.h"
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
  virtual void beginRun(edm::Run&, const edm::EventSetup&);

private:
  const edm::InputTag trigger_results_src;
  const edm::InputTag cleaning_results_src;
  const std::string skip_event_filter;
  const edm::InputTag pfjets_src;
  const double jet_pt_min;
  const edm::InputTag beamspot_src;
  const edm::InputTag primary_vertex_src;
  const edm::InputTag gen_particles_src;
  const edm::InputTag calojets_src;
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

  L1GtUtils l1_cfg;
  HLTConfigProvider hlt_cfg;

  std::vector<JetIDSelectionFunctor> calojet_selectors;
};

MFVEventProducer::MFVEventProducer(const edm::ParameterSet& cfg)
  : trigger_results_src(cfg.getParameter<edm::InputTag>("trigger_results_src")),
    cleaning_results_src(cfg.getParameter<edm::InputTag>("cleaning_results_src")),
    skip_event_filter(cfg.getParameter<std::string>("skip_event_filter")),
    pfjets_src(cfg.getParameter<edm::InputTag>("pfjets_src")),
    jet_pt_min(cfg.getParameter<double>("jet_pt_min")),
    beamspot_src(cfg.getParameter<edm::InputTag>("beamspot_src")),
    primary_vertex_src(cfg.getParameter<edm::InputTag>("primary_vertex_src")),
    gen_particles_src(cfg.getParameter<edm::InputTag>("gen_particles_src")),
    calojets_src(cfg.getParameter<edm::InputTag>("calojets_src")),
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
  for (int i = 0; i < 4; ++i)
    calojet_selectors.push_back(JetIDSelectionFunctor(JetIDSelectionFunctor::PURE09, JetIDSelectionFunctor::Quality_t(i)));

  produces<MFVEvent>();
}

void MFVEventProducer::beginRun(edm::Run& run, const edm::EventSetup& setup) {
  bool changed = true;
  if (!hlt_cfg.init(run, setup, trigger_results_src.process(), changed))
    throw cms::Exception("MFVEventProducer") << "HLTConfigProvider::init failed with process name " << trigger_results_src;
  //if (changed)
  //  hlt_cfg.dump("PrescaleTable");
}

void MFVEventProducer::produce(edm::Event& event, const edm::EventSetup& setup) {
  if (cleaning_results_src.label() != "" && skip_event_filter != "" && !TriggerHelper(event, cleaning_results_src).pass(skip_event_filter))
    return;

  std::auto_ptr<MFVEvent> mevent(new MFVEvent);

  edm::Handle<reco::BeamSpot> beamspot;
  event.getByLabel(beamspot_src, beamspot);
  mevent->bsx = beamspot->x0();
  mevent->bsy = beamspot->y0();
  mevent->bsz = beamspot->z0();
  mevent->bsdxdz = beamspot->dxdz();
  mevent->bsdydz = beamspot->dydz();
  mevent->bswidthx = beamspot->BeamWidthX();
  mevent->bswidthy = beamspot->BeamWidthY();

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

#if 0  
  TriggerHelper trig_helper(event, trigger_results_src);
  mfv::trigger_decision(trig_helper, mevent->pass_trigger);

  l1_cfg.getL1GtRunCache(event, setup, true, false);

  const std::vector<std::string> all_l1_seeds = { "L1_QuadJetC32", "L1_QuadJetC36", "L1_QuadJetC40", "L1_HTT125", "L1_HTT150", "L1_HTT175", "L1_DoubleJetC52", "L1_DoubleJetC56", "L1_DoubleJetC64" };
  //const size_t nl1 = all_l1_seeds.size();
  const std::vector<int> hlt_versions = {1,2,3,5};
  const size_t nhlt = hlt_versions.size();

  int l1_found = 0;
  int hlt_found = 0;
  for (size_t ihlt = 0; ihlt < nhlt; ++ihlt) {
    const int hlt_version = hlt_versions[ihlt];
    char path[1024];
    snprintf(path, 1024, "HLT_QuadJet50_v%i", hlt_version);
    if (hlt_cfg.triggerIndex(path) == hlt_cfg.size())
      continue;

    const int hlt_prescale = hlt_cfg.prescaleValue(event, setup, path);
    mevent->hlt_prescale = hlt_prescale > 65535 ? 65535 : hlt_prescale;

    if (++hlt_found > 1)
      throw cms::Exception("BadAssumption") << "more than one QuadJet50";

    const auto& v = hlt_cfg.hltL1GTSeeds(path);
    if (v.size() != 1)
      throw cms::Exception("BadAssumption") << "more than one seed returned: " << v.size();

    std::string s = v[0].second;
    const std::string delim = " OR ";
    while (s.size()) {
      const size_t pos = s.find(delim);
      const std::string l1_path = s.substr(0, pos);
      const auto& itl1 = std::find(all_l1_seeds.begin(), all_l1_seeds.end(), l1_path);
      if (itl1 == all_l1_seeds.end())
        throw cms::Exception("BadAssumption") << "L1 seed " << l1_path << " not expected";
      const size_t il1 = itl1 - all_l1_seeds.begin();

      ++l1_found;

      int l1_err;

      const int l1_prescale = l1_cfg.prescaleFactor(event, l1_path, l1_err);
      if (l1_err != 0)
        throw cms::Exception("L1Error") << "error code " << l1_err << " for path " << l1_path << " when getting prescale";
      mevent->l1_prescale[il1] = l1_prescale > 65535 ? 65535 : l1_prescale;

      mevent->l1_pass[il1] = l1_cfg.decision(event, l1_path, l1_err);
      if (l1_err != 0)
        throw cms::Exception("L1Error") << "error code " << l1_err << " for path " << l1_path << " when getting decision";

      if (pos == std::string::npos)
        break;
      else
        s.erase(0, pos + delim.length());
    }
  }

  if (l1_found != 3 && l1_found != 9)
    throw cms::Exception("BadAssumption") << "not the right L1 paths found: l1_found = " << l1_found;

  if (cleaning_results_src.label() != "") {
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

    TriggerHelper trig_helper_cleaning(event, cleaning_results_src);
    for (int i = 0; i < mfv::n_clean_paths; ++i)
      mevent->pass_clean[i] = trig_helper_cleaning.pass("eventCleaning" + cleaning_paths[i]);
  }
#endif

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
    mevent->pvcxx = primary_vertex->covariance(0,0);
    mevent->pvcxy = primary_vertex->covariance(0,1);
    mevent->pvcxz = primary_vertex->covariance(0,2);
    mevent->pvcyy = primary_vertex->covariance(1,1);
    mevent->pvcyz = primary_vertex->covariance(1,2);
    mevent->pvczz = primary_vertex->covariance(2,2);

    mevent->pv_ntracks = int2uchar_clamp(primary_vertex->nTracks());
    mevent->pv_sumpt2 = 0;
    for (auto trki = primary_vertex->tracks_begin(), trke = primary_vertex->tracks_end(); trki != trke; ++trki) {
      double trkpt = (*trki)->pt();
      mevent->pv_sumpt2 += trkpt * trkpt;
    }
  }

  //////////////////////////////////////////////////////////////////////
#if 0
  edm::Handle<pat::JetCollection> calojets;
  event.getByLabel(calojets_src, calojets);

  for (const pat::Jet& jet : *calojets) {
    if (jet.pt() < jet_pt_min) // JMTBAD should also require |eta| < 2.5
      continue;

    uchar id = 0;
    for (int i = 0; i < 4; ++i) {
      pat::strbitset ret = calojet_selectors[i].getBitTemplate();
      id = id | (calojet_selectors[i](jet, ret) << i);
    }

    mevent->calojet_id.push_back(id);
    mevent->calojet_pt.push_back(jet.pt());
    mevent->calojet_eta.push_back(jet.eta());
    mevent->calojet_phi.push_back(jet.phi());
    mevent->calojet_energy.push_back(jet.energy());
  }
#endif
  //////////////////////////////////////////////////////////////////////

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

    mevent->jet_pt.push_back(jet.pt());
    mevent->jet_eta.push_back(jet.eta());
    mevent->jet_phi.push_back(jet.phi());
    mevent->jet_energy.push_back(jet.energy());

    int bdisc_level = 0;
    for (int i = 0; i < 3; ++i)
      if (jet.bDiscriminator(b_discriminator) > b_discriminator_mins[i])
        bdisc_level = i+1;

    mevent->jet_id.push_back(MFVEvent::encode_jet_id(0, bdisc_level));

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

    const reco::SecondaryVertexTagInfo* svtag = jet.tagInfoSecondaryVertex("secondaryVertex");
    mevent->jet_svnvertices.push_back(svtag ? svtag->nVertices() : -1);

    if (svtag && svtag->nVertices() > 0) {
      const reco::Vertex &sv = svtag->secondaryVertex(0);
      mevent->jet_svntracks.push_back(sv.nTracks());
      double svsumpt2 = 0;
      for (auto trki = sv.tracks_begin(), trke = sv.tracks_end(); trki != trke; ++trki) {
        double trkpt = (*trki)->pt();
        svsumpt2 += trkpt * trkpt;
      }
      mevent->jet_svsumpt2.push_back(svsumpt2);
      mevent->jet_svx.push_back(sv.x());
      mevent->jet_svy.push_back(sv.y());
      mevent->jet_svz.push_back(sv.z());
      mevent->jet_svcxx.push_back(sv.covariance(0,0));
      mevent->jet_svcxy.push_back(sv.covariance(0,1));
      mevent->jet_svcxz.push_back(sv.covariance(0,2));
      mevent->jet_svcyy.push_back(sv.covariance(1,1));
      mevent->jet_svcyz.push_back(sv.covariance(1,2));
      mevent->jet_svczz.push_back(sv.covariance(2,2));
    }
    else {
      mevent->jet_svntracks.push_back(0);
      mevent->jet_svsumpt2.push_back(0);
      mevent->jet_svx.push_back(0);
      mevent->jet_svy.push_back(0);
      mevent->jet_svz.push_back(0);
      mevent->jet_svcxx.push_back(0);
      mevent->jet_svcxy.push_back(0);
      mevent->jet_svcxz.push_back(0);
      mevent->jet_svcyy.push_back(0);
      mevent->jet_svcyz.push_back(0);
      mevent->jet_svczz.push_back(0);
    }
  }

  //////////////////////////////////////////////////////////////////////

  mevent->lep_id.clear();
  mevent->lep_pt.clear();
  mevent->lep_eta.clear();
  mevent->lep_phi.clear();
  mevent->lep_dxy.clear();
  mevent->lep_dz.clear();
  mevent->lep_iso.clear();
  mevent->lep_mva.clear();

#if 0
  edm::Handle<pat::MuonCollection> muons;
  event.getByLabel(muons_src, muons);

  for (const pat::Muon& muon : *muons) {
    uchar id =
      0
      | 1 << 1  // if it's in the collection it passes veto selection
      | muon_semilep_selector(muon) << 2
      | muon_dilep_selector(muon) << 3;

    float iso = (muon.chargedHadronIso() + muon.neutralHadronIso() + muon.photonIso() - 0.5*muon.puChargedHadronIso())/muon.pt(); // JMTBAD keep in sync with .py
    float mva = 1e99;

    mevent->lep_id.push_back(id);
    mevent->lep_pt.push_back(muon.pt());
    mevent->lep_eta.push_back(muon.eta());
    mevent->lep_phi.push_back(muon.phi());
    mevent->lep_dxy.push_back(muon.track()->dxy(beamspot->position()));
    mevent->lep_dz.push_back(muon.track()->dz(primary_vertex->position()));
    mevent->lep_iso.push_back(iso);
    mevent->lep_mva.push_back(mva);
  }

  edm::Handle<pat::ElectronCollection> electrons;
  event.getByLabel(electrons_src, electrons);
  
  for (const pat::Electron& electron : *electrons) {
    uchar id =
      1
      | 1 << 1  // if it's in the collection it passes veto selection
      | electron_semilep_selector(electron) << 2
      | electron_dilep_selector(electron) << 3
      | electron.closestCtfTrackRef().isNonnull() << 4;

    float iso = (electron.chargedHadronIso() + std::max(0.f,electron.neutralHadronIso()) + electron.photonIso() - 0.5*electron.puChargedHadronIso())/electron.et();
    float mva = electron.electronID("mvaNonTrigV0");

    mevent->lep_id.push_back(id);
    mevent->lep_pt.push_back(electron.pt());
    mevent->lep_eta.push_back(electron.eta());
    mevent->lep_phi.push_back(electron.phi());
    mevent->lep_dxy.push_back(electron.gsfTrack()->dxy(beamspot->position()));
    mevent->lep_dz.push_back(electron.gsfTrack()->dz(primary_vertex->position()));
    mevent->lep_iso.push_back(iso);
    mevent->lep_mva.push_back(mva);
  }
  #endif
  //////////////////////////////////////////////////////////////////////

  event.put(mevent);
}

DEFINE_FWK_MODULE(MFVEventProducer);
