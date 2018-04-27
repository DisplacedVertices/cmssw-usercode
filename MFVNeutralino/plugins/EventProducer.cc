#include "CommonTools/Utils/interface/StringCutObjectSelector.h"
#include "DataFormats/Common/interface/TriggerResults.h"
#include "DataFormats/JetReco/interface/PFJetCollection.h"
#include "DataFormats/BeamSpot/interface/BeamSpot.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/MET.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "FWCore/Common/interface/TriggerNames.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "PhysicsTools/SelectorUtils/interface/JetIDSelectionFunctor.h"
#include "SimDataFormats/GeneratorProducts/interface/GenEventInfoProduct.h"
#include "SimDataFormats/PileupSummaryInfo/interface/PileupSummaryInfo.h"
#include "JMTucker/MFVNeutralinoFormats/interface/Event.h"
#include "JMTucker/MFVNeutralinoFormats/interface/MCInteractions.h"
#include "JMTucker/MFVNeutralinoFormats/interface/TriggerFloats.h"
#include "JMTucker/MFVNeutralino/interface/EventTools.h"
#include "JMTucker/Tools/interface/Bridges.h"
#include "JMTucker/Tools/interface/GenUtilities.h"
#include "JMTucker/Tools/interface/TriggerHelper.h"
#include "JMTucker/Tools/interface/Utilities.h"

class MFVEventProducer : public edm::EDProducer {
public:
  explicit MFVEventProducer(const edm::ParameterSet&);
  void produce(edm::Event&, const edm::EventSetup&);

private:
  const bool input_is_miniaod;
  const edm::EDGetTokenT<mfv::TriggerFloats> triggerfloats_token;
  const edm::EDGetTokenT<reco::BeamSpot> beamspot_token;
  const edm::EDGetTokenT<reco::VertexCollection> primary_vertex_token;
  const edm::EDGetTokenT<pat::PackedCandidateCollection> packed_candidates_token;
  const edm::EDGetTokenT<GenEventInfoProduct> gen_info_token;
  const edm::EDGetTokenT<std::vector<double>> gen_vertex_token;
  const edm::EDGetTokenT<reco::GenJetCollection> gen_jets_token;
  const edm::EDGetTokenT<reco::GenParticleCollection> gen_particles_token;
  const edm::EDGetTokenT<mfv::MCInteraction> mci_token;
  const edm::EDGetTokenT<std::vector<PileupSummaryInfo> > pileup_summary_token;
  const edm::EDGetTokenT<pat::JetCollection> jets_token;
  const bool use_met;
  const edm::EDGetTokenT<pat::METCollection> met_token;
  const edm::EDGetTokenT<pat::MuonCollection> muons_token;
  const edm::EDGetTokenT<pat::ElectronCollection> electrons_token;
  const edm::EDGetTokenT<reco::TrackCollection> vertex_seed_tracks_token;
  const double jet_pt_min;
  const std::string b_discriminator;
  const std::vector<double> b_discriminator_mins;
  const StringCutObjectSelector<pat::Muon> muon_semilep_selector;
  const StringCutObjectSelector<pat::Muon> muon_dilep_selector;
  const StringCutObjectSelector<pat::Electron> electron_semilep_selector;
  const StringCutObjectSelector<pat::Electron> electron_dilep_selector;
  const bool lightweight;
};

MFVEventProducer::MFVEventProducer(const edm::ParameterSet& cfg)
  : input_is_miniaod(cfg.getParameter<bool>("input_is_miniaod")),
    triggerfloats_token(consumes<mfv::TriggerFloats>(cfg.getParameter<edm::InputTag>("triggerfloats_src"))),
    beamspot_token(consumes<reco::BeamSpot>(cfg.getParameter<edm::InputTag>("beamspot_src"))),
    primary_vertex_token(consumes<reco::VertexCollection>(cfg.getParameter<edm::InputTag>("primary_vertex_src"))),
    packed_candidates_token(consumes<pat::PackedCandidateCollection>(cfg.getParameter<edm::InputTag>("packed_candidates_src"))),
    gen_info_token(consumes<GenEventInfoProduct>(cfg.getParameter<edm::InputTag>("gen_info_src"))),
    gen_vertex_token(consumes<std::vector<double>>(cfg.getParameter<edm::InputTag>("gen_vertex_src"))),
    gen_jets_token(consumes<reco::GenJetCollection>(cfg.getParameter<edm::InputTag>("gen_jets_src"))),
    gen_particles_token(consumes<reco::GenParticleCollection>(cfg.getParameter<edm::InputTag>("gen_particles_src"))),
    mci_token(consumes<mfv::MCInteraction>(cfg.getParameter<edm::InputTag>("mci_src"))),
    pileup_summary_token(consumes<std::vector<PileupSummaryInfo> >(cfg.getParameter<edm::InputTag>("pileup_info_src"))),
    jets_token(consumes<pat::JetCollection>(cfg.getParameter<edm::InputTag>("jets_src"))),
    use_met(cfg.getParameter<edm::InputTag>("met_src").label() != ""),
    met_token(consumes<pat::METCollection>(cfg.getParameter<edm::InputTag>("met_src"))),
    muons_token(consumes<pat::MuonCollection>(cfg.getParameter<edm::InputTag>("muons_src"))),
    electrons_token(consumes<pat::ElectronCollection>(cfg.getParameter<edm::InputTag>("electrons_src"))),
    vertex_seed_tracks_token(consumes<reco::TrackCollection>(cfg.getParameter<edm::InputTag>("vertex_seed_tracks_src"))),
    jet_pt_min(cfg.getParameter<double>("jet_pt_min")),
    b_discriminator(cfg.getParameter<std::string>("b_discriminator")),
    b_discriminator_mins(cfg.getParameter<std::vector<double> >("b_discriminator_mins")),
    muon_semilep_selector(cfg.getParameter<std::string>("muon_semilep_cut")),
    muon_dilep_selector(cfg.getParameter<std::string>("muon_dilep_cut")),
    electron_semilep_selector(cfg.getParameter<std::string>("electron_semilep_cut")),
    electron_dilep_selector(cfg.getParameter<std::string>("electron_dilep_cut")),
    lightweight(cfg.getParameter<bool>("lightweight"))
{
  produces<MFVEvent>();
}

void MFVEventProducer::produce(edm::Event& event, const edm::EventSetup& setup) {
  std::unique_ptr<MFVEvent> mevent(new MFVEvent);

  edm::Handle<reco::BeamSpot> beamspot;
  event.getByToken(beamspot_token, beamspot);
  mevent->bsx = beamspot->x0();
  mevent->bsy = beamspot->y0();
  mevent->bsz = beamspot->z0();
  mevent->bsdxdz = beamspot->dxdz();
  mevent->bsdydz = beamspot->dydz();
  mevent->bswidthx = beamspot->BeamWidthX();
  mevent->bswidthy = beamspot->BeamWidthY();

  edm::Handle<reco::VertexCollection> primary_vertices;
  event.getByToken(primary_vertex_token, primary_vertices);
  const reco::Vertex* primary_vertex = 0;
  if (primary_vertices->size())
    primary_vertex = &primary_vertices->at(0);

  edm::Handle<pat::PackedCandidateCollection> packed_candidates;
  if (input_is_miniaod)
    event.getByToken(packed_candidates_token, packed_candidates);

  //////////////////////////////////////////////////////////////////////

  mevent->gen_valid = false;

  if (!event.isRealData()) {
    edm::Handle<GenEventInfoProduct> gen_info;
    event.getByToken(gen_info_token, gen_info);

    mevent->gen_weight = gen_info->weight();
    mevent->gen_weightprod = gen_info->weightProduct();

    edm::Handle<reco::GenJetCollection> gen_jets;
    event.getByToken(gen_jets_token, gen_jets);

    for (const reco::GenJet& jet : *gen_jets) {
      if (jet.pt() > 20 && fabs(jet.eta()) < 2.5) {
        double mue = 0;
        for (auto c : jet.getJetConstituents())
          if (abs(c->pdgId()) == 13)
            mue += c->energy();
        if (mue / jet.energy() < 0.8)
          mevent->gen_jets.push_back(TLorentzVector(jet.px(), jet.py(), jet.pz(), jet.energy()));
      }
    }

    edm::Handle<std::vector<double>> gen_vertex;
    event.getByToken(gen_vertex_token, gen_vertex);

    mevent->gen_pv[0] = (*gen_vertex)[0];
    mevent->gen_pv[1] = (*gen_vertex)[1];
    mevent->gen_pv[2] = (*gen_vertex)[2];

    edm::Handle<reco::GenParticleCollection> gen_particles;
    event.getByToken(gen_particles_token, gen_particles);
    
    mevent->gen_flavor_code = 0;
    bool saw_c = false;
    for (const reco::GenParticle& gen : *gen_particles) {
      if (is_bhadron(&gen)) {
	mevent->gen_flavor_code = 2;
	break;
      }
      if (is_chadron(&gen))
	saw_c = true;
    }
    if (saw_c && mevent->gen_flavor_code == 0)
      mevent->gen_flavor_code = 1;

    edm::Handle<mfv::MCInteraction> mci;
    event.getByToken(mci_token, mci);

    std::vector<reco::GenParticleRef> mci_lep;

    if (mci->valid()) {
      mevent->gen_valid = true;

      assert(mci->primaries().size() == 2);
      for (int i = 0; i < 2; ++i) {
        mevent->gen_lsp_pt  [i] = mci->primaries()[i]->pt();
        mevent->gen_lsp_eta [i] = mci->primaries()[i]->eta();
        mevent->gen_lsp_phi [i] = mci->primaries()[i]->phi();
        mevent->gen_lsp_mass[i] = mci->primaries()[i]->mass();

        auto p = mci->decay_point(i);
        mevent->gen_lsp_decay[i*3+0] = p.x;
        mevent->gen_lsp_decay[i*3+1] = p.y;
        mevent->gen_lsp_decay[i*3+2] = p.z;

        mevent->gen_decay_type[i] = mci->decay_type()[i];

        for (const reco::GenParticleRef& s : mci->secondaries(i)) {
          mevent->gen_daughters.push_back(MFVEvent::p4(s->pt(), s->eta(), s->phi(), s->mass()));
          mevent->gen_daughter_id.push_back(s->pdgId());
        }
      }

      mci_lep = mci->light_leptons();
    }

    for (const reco::GenParticle& gen : *gen_particles) {
      if (gen.pt() < 1)
        continue;

      const int id = abs(gen.pdgId());

      if (id == 5) {
        bool has_b_dau = false;
        for (size_t i = 0, ie = gen.numberOfDaughters(); i < ie; ++i) {
          if (abs(gen.daughter(i)->pdgId()) == 5) {
            has_b_dau = true;
            break;
          }
        }
        if (!has_b_dau)
          mevent->gen_bquarks.push_back(TLorentzVector(gen.px(), gen.py(), gen.pz(), gen.energy()));
      }
      else if ((id == 11 || id == 13) && (gen.status() == 1 || (gen.status() >= 21 && gen.status() <= 29)))
        mevent->gen_leptons.push_back(MFVEvent::p4(gen.pt(), gen.eta(), gen.phi(), gen.mass()));
    }
  }

  //////////////////////////////////////////////////////////////////////

  edm::Handle<mfv::TriggerFloats> triggerfloats;
  event.getByToken(triggerfloats_token, triggerfloats);

  mevent->l1_htt = triggerfloats->l1htt;
  mevent->l1_myhtt = triggerfloats->myhtt;
  mevent->l1_myhttwbug = triggerfloats->myhttwbug;
  mevent->hlt_ht = triggerfloats->hltht;
  mevent->hlt_ht4mc = triggerfloats->hltht4mc;

  assert(triggerfloats->L1decisions.size() == mfv::n_l1_paths);
  for (size_t i = 0; i < mfv::n_l1_paths; ++i) {
    const bool found = triggerfloats->L1decisions[i] != -1;
    mevent->found_l1(i, found);
    mevent-> pass_l1(i, found && triggerfloats->L1decisions[i]);
  }

  assert(triggerfloats->HLTdecisions.size() == mfv::n_hlt_paths);
  for (size_t i = 0; i < mfv::n_hlt_paths; ++i) {
    const bool found = triggerfloats->HLTdecisions[i] != -1;
    mevent->found_hlt(i, found);
    mevent-> pass_hlt(i, found && triggerfloats->HLTdecisions[i]);
  }

  //////////////////////////////////////////////////////////////////////

  mevent->npu = -1;

  if (!event.isRealData()) {
    edm::Handle<std::vector<PileupSummaryInfo> > pileup;
    event.getByToken(pileup_summary_token, pileup);

    for (std::vector<PileupSummaryInfo>::const_iterator psi = pileup->begin(), end = pileup->end(); psi != end; ++psi)
      if (psi->getBunchCrossing() == 0)
        mevent->npu = psi->getTrueNumInteractions();
  }

  //////////////////////////////////////////////////////////////////////

  mevent->npv = int2uchar_clamp(primary_vertices->size());

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

    mevent->pv_ntracks = 0;
    mevent->pv_sumpt2 = 0;
    if (input_is_miniaod) {
      for (const pat::PackedCandidate& cand : *packed_candidates)
        if (cand.vertexRef().key() == 0 && jmt::packedCandidateHasTrackDetails(cand)) {
          inc_uchar_clamp(mevent->pv_ntracks);
          mevent->pv_sumpt2 += cand.pt() * cand.pt(); // JMTBAD just use the stored score
        }
    }
    else {
      mevent->pv_ntracks = int2uchar_clamp(primary_vertex->nTracks());
      for (auto trki = primary_vertex->tracks_begin(), trke = primary_vertex->tracks_end(); trki != trke; ++trki) {
        double trkpt = (*trki)->pt();
        mevent->pv_sumpt2 += trkpt * trkpt;
      }
    }
  }

  //////////////////////////////////////////////////////////////////////

  if (use_met) {
    edm::Handle<pat::METCollection> mets;
    event.getByToken(met_token, mets);
    const pat::MET& met = mets->at(0);
    mevent->metx = met.px();
    mevent->mety = met.py();
  }

  //////////////////////////////////////////////////////////////////////

  edm::Handle<pat::JetCollection> jets;
  event.getByToken(jets_token, jets);

  for (int jjet = 0, jjete = int(jets->size()); jjet < jjete; ++jjet) {
    const pat::Jet& jet = jets->at(jjet);
    if (jet.pt() < jet_pt_min)
      continue;

    mevent->jet_pudisc.push_back(jet.userFloat("pileupJetId:fullDiscriminant")); // to be removed and put into _id when working points defined
    mevent->jet_pt.push_back(jet.pt());
    mevent->jet_raw_pt.push_back(jet.pt()*jet.jecFactor("Uncorrected"));
    mevent->jet_bdisc.push_back(jet.bDiscriminator(b_discriminator));
    mevent->jet_eta.push_back(jet.eta());
    mevent->jet_phi.push_back(jet.phi());
    mevent->jet_energy.push_back(jet.energy());

    int bdisc_level = 0;
    for (int i = 0; i < 3; ++i)
      if (jet.bDiscriminator(b_discriminator) > b_discriminator_mins[i])
        bdisc_level = i+1;

    mevent->jet_id.push_back(MFVEvent::encode_jet_id(0, bdisc_level, jet.hadronFlavour()));
    const size_t ijet = mevent->njets() - 1; // will stay in track with jjet as long as jets are pt ordered...

    assert(ijet <= 255);
    for (size_t idau = 0, idaue = jet.numberOfDaughters(); idau < idaue; ++idau) {
      // handle both regular aod and miniaod: in the latter
      // getPFConstituents() doesn't work because the daughters are
      // pat::PackedCandidates. Since we don't care about track
      // identities e.g. to compare with vertices we don't use
      // JetTrackRefGetter here, but could
      const reco::Candidate* dau = jet.daughter(idau);
      if (dau->charge() == 0)
        continue;
        
      const reco::Track* tk = 0;
      const reco::PFCandidate* pf = dynamic_cast<const reco::PFCandidate*>(dau);
      if (pf) {
        const reco::TrackRef& r = pf->trackRef();
        if (r.isNonnull())
          tk = &*r;
      }
      else {
        const pat::PackedCandidate* pk = dynamic_cast<const pat::PackedCandidate*>(dau);
        if (pk && jmt::packedCandidateHasTrackDetails(*pk))
          tk = &pk->pseudoTrack();
      }

      if (tk) {
        assert(abs(tk->charge()) == 1);
        mevent->jet_track_which_jet.push_back(ijet);
        mevent->jet_track_chi2dof.push_back(tk->normalizedChi2());
        mevent->jet_track_qpt.push_back(tk->charge() * tk->pt());
        mevent->jet_track_eta.push_back(tk->eta());
        mevent->jet_track_phi.push_back(tk->phi());
        mevent->jet_track_dxy.push_back(tk->dxy(beamspot->position()));
        mevent->jet_track_dz.push_back(primary_vertex ? tk->dz(primary_vertex->position()) : 0);
        mevent->jet_track_pt_err.push_back(tk->ptError());
        mevent->jet_track_eta_err.push_back(tk->etaError());
        mevent->jet_track_phi_err.push_back(tk->phiError());
        mevent->jet_track_dxy_err.push_back(tk->dxyError());
        mevent->jet_track_dz_err.push_back(tk->dzError());
        mevent->jet_track_hp_.push_back(MFVEvent::make_track_hitpattern(tk->hitPattern().numberOfValidPixelHits(), tk->hitPattern().numberOfValidStripHits(), tk->hitPattern().pixelLayersWithMeasurement(), tk->hitPattern().stripLayersWithMeasurement()));
      }
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

  edm::Handle<pat::MuonCollection> muons;
  event.getByToken(muons_token, muons);

  for (const pat::Muon& muon : *muons) {
    uchar sel = 0;
    if (1)                           sel |= MFVEvent::mu_veto;
    if (muon_semilep_selector(muon)) sel |= MFVEvent::mu_semilep;
    if (muon_dilep_selector  (muon)) sel |= MFVEvent::mu_dilep;

    const float iso = (muon.chargedHadronIso() + std::max(0.f,muon.neutralHadronIso()) + muon.photonIso() - 0.5*muon.puChargedHadronIso())/muon.pt(); // JMTBAD keep in sync with .py

    mevent->lep_id.push_back(MFVEvent::encode_mu_id(sel));
    mevent->lep_pt.push_back(muon.pt());
    mevent->lep_eta.push_back(muon.eta());
    mevent->lep_phi.push_back(muon.phi());
    if (primary_vertex != 0) {
      const auto& pvpos = primary_vertex->position();
      mevent->lep_dxy.push_back(muon.track()->dxy(pvpos));
      mevent->lep_dz.push_back(muon.track()->dz(pvpos));
    }
    else {
      mevent->lep_dxy.push_back(muon.track()->dxy());
      mevent->lep_dz.push_back(muon.track()->dz());
    }
    mevent->lep_dxybs.push_back(muon.track()->dxy(beamspot->position()));
    mevent->lep_iso.push_back(iso);
  }

  edm::Handle<pat::ElectronCollection> electrons;
  event.getByToken(electrons_token, electrons);
  
  for (const pat::Electron& electron : *electrons) {
    uchar sel = 0;
    if (1)                                         sel |= MFVEvent::el_veto;
    if (electron_semilep_selector(electron))       sel |= MFVEvent::el_semilep;
    if (electron_dilep_selector  (electron))       sel |= MFVEvent::el_dilep;
    if (electron.closestCtfTrackRef().isNonnull()) sel |= MFVEvent::el_ctf;

    const float iso = (electron.chargedHadronIso() + std::max(0.f,electron.neutralHadronIso()) + electron.photonIso() - 0.5*electron.puChargedHadronIso())/electron.et();

    mevent->lep_id.push_back(MFVEvent::encode_el_id(sel));
    mevent->lep_pt.push_back(electron.pt());
    mevent->lep_eta.push_back(electron.eta());
    mevent->lep_phi.push_back(electron.phi());
    if (primary_vertex != 0) {
      const auto& pvpos = primary_vertex->position();
      mevent->lep_dxy.push_back(electron.gsfTrack()->dxy(pvpos));
      mevent->lep_dz.push_back(electron.gsfTrack()->dz(pvpos));
    }
    else {
      mevent->lep_dxy.push_back(electron.gsfTrack()->dxy());
      mevent->lep_dz.push_back(electron.gsfTrack()->dz());
    }
    mevent->lep_dxybs.push_back(electron.gsfTrack()->dxy(beamspot->position()));
    mevent->lep_iso.push_back(iso);
  }

  //////////////////////////////////////////////////////////////////////

  edm::Handle<reco::TrackCollection> vertex_seed_tracks;
  event.getByToken(vertex_seed_tracks_token, vertex_seed_tracks);
  for (const reco::Track& tk : *vertex_seed_tracks) {
    assert(abs(tk.charge()) == 1);
    mevent->vertex_seed_track_chi2dof.push_back(tk.normalizedChi2());
    mevent->vertex_seed_track_qpt.push_back(tk.charge() * tk.pt());
    mevent->vertex_seed_track_eta.push_back(tk.eta());
    mevent->vertex_seed_track_phi.push_back(tk.phi());
    mevent->vertex_seed_track_dxy.push_back(tk.dxy(beamspot->position()));
    mevent->vertex_seed_track_dz.push_back(primary_vertex ? tk.dz(primary_vertex->position()) : 0);
    mevent->vertex_seed_track_hp_.push_back(MFVEvent::make_track_hitpattern(tk.hitPattern().numberOfValidPixelHits(), tk.hitPattern().numberOfValidStripHits(), tk.hitPattern().pixelLayersWithMeasurement(), tk.hitPattern().stripLayersWithMeasurement()));
  }

  //////////////////////////////////////////////////////////////////////

  if (lightweight) {
    // keep
    // for weight: gen_weight, npv, , npu
    // for trigger: pass_
    // for njets and ht40: jet_pt vector
    // jet_id vector
    // beamspot and slopes, pvx,y,z

    mevent->gen_valid = 0;
    mevent->gen_weightprod = 0;
    mevent->gen_flavor_code = 0;
    for (int i = 0; i < 2; ++i) {
      mevent->gen_lsp_pt[i] = mevent->gen_lsp_eta[i] = mevent->gen_lsp_phi[i] = mevent->gen_lsp_mass[i] = 0;
      mevent->gen_decay_type[i] = 0;
      for (int j = 0; j < 3; ++j)
        mevent->gen_lsp_decay[i*3+j] = 0;
    }
    for (int i = 0; i < 3; ++i) {
      mevent->gen_pv[i] = 0;
    }
    mevent->gen_bquarks.clear();
    mevent->gen_leptons.clear();
    mevent->gen_jets.clear();
    mevent->gen_daughters.clear();
    mevent->gen_daughter_id.clear();
    mevent->l1_htt = 0;
    mevent->l1_myhtt = 0;
    mevent->l1_myhttwbug = 0;
    mevent->hlt_ht = 0;
    mevent->hlt_ht4mc = 0;
    mevent->bswidthx = 0;
    mevent->bswidthy = 0;
    mevent->pvcxx = 0;
    mevent->pvcxy = 0;
    mevent->pvcxz = 0;
    mevent->pvcyy = 0;
    mevent->pvcyz = 0;
    mevent->pvczz = 0;
    mevent->pv_ntracks = 0;
    mevent->pv_sumpt2 = 0; 
    mevent->jet_pudisc.clear();
    mevent->jet_raw_pt.clear();
    mevent->jet_bdisc.clear();
    mevent->jet_eta.clear();
    mevent->jet_phi.clear();
    mevent->jet_energy.clear();
    mevent->metx = 0;
    mevent->mety = 0;
    mevent->lep_id.clear();
    mevent->lep_pt.clear();
    mevent->lep_eta.clear();
    mevent->lep_phi.clear();
    mevent->lep_dxy.clear();
    mevent->lep_dxybs.clear();
    mevent->lep_dz.clear();
    mevent->lep_iso.clear();
    mevent->vertex_seed_track_chi2dof.clear();
    mevent->vertex_seed_track_qpt.clear();
    mevent->vertex_seed_track_eta.clear();
    mevent->vertex_seed_track_phi.clear();
    mevent->vertex_seed_track_dxy.clear();
    mevent->vertex_seed_track_dz.clear();
    mevent->vertex_seed_track_hp_.clear();
    mevent->jet_track_which_jet.clear();
    mevent->jet_track_chi2dof.clear();
    mevent->jet_track_qpt.clear();
    mevent->jet_track_eta.clear();
    mevent->jet_track_phi.clear();
    mevent->jet_track_dxy.clear();
    mevent->jet_track_dz.clear();
    mevent->jet_track_pt_err.clear();
    mevent->jet_track_eta_err.clear();
    mevent->jet_track_phi_err.clear();
    mevent->jet_track_dxy_err.clear();
    mevent->jet_track_dz_err.clear();
    mevent->jet_track_hp_.clear();
  }

  event.put(std::move(mevent));
}

DEFINE_FWK_MODULE(MFVEventProducer);
