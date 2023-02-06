#include "CommonTools/Utils/interface/StringCutObjectSelector.h"
#include "DataFormats/Common/interface/TriggerResults.h"
#include "DataFormats/JetReco/interface/PFJetCollection.h"
#include "DataFormats/JetReco/interface/CaloJetCollection.h"
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
#include "RecoEgamma/EgammaTools/interface/EffectiveAreas.h"
#include "SimDataFormats/GeneratorProducts/interface/GenEventInfoProduct.h"
#include "SimDataFormats/PileupSummaryInfo/interface/PileupSummaryInfo.h"
#include "JMTucker/MFVNeutralinoFormats/interface/Event.h"
#include "JMTucker/MFVNeutralinoFormats/interface/MCInteractions.h"
#include "JMTucker/MFVNeutralinoFormats/interface/TriggerFloats.h"
#include "JMTucker/MFVNeutralino/interface/EventTools.h"
#include "JMTucker/Tools/interface/BTagging.h"
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
  const edm::EDGetTokenT<edm::ValueMap<float>> primary_vertex_scores_token;
  const edm::EDGetTokenT<pat::PackedCandidateCollection> packed_candidates_token;
  const edm::EDGetTokenT<GenEventInfoProduct> gen_info_token;
  const edm::EDGetTokenT<std::vector<double>> gen_vertex_token;
  const edm::EDGetTokenT<reco::GenJetCollection> gen_jets_token;
  const edm::EDGetTokenT<reco::GenParticleCollection> gen_particles_token;
  const edm::EDGetTokenT<mfv::MCInteraction> mci_token;
  const edm::EDGetTokenT<std::vector<PileupSummaryInfo> > pileup_summary_token;
  const edm::EDGetTokenT<pat::JetCollection> jets_token;
  const edm::EDGetTokenT<reco::CaloJetCollection> calo_jets_token;
  const edm::EDGetTokenT<double> rho_token;
  const bool use_met;
  const edm::EDGetTokenT<pat::METCollection> met_token;
  const edm::EDGetTokenT<pat::MuonCollection> muons_token;
  const edm::EDGetTokenT<pat::ElectronCollection> electrons_token;
  const bool use_vertex_seed_tracks;
  const edm::EDGetTokenT<reco::TrackCollection> vertex_seed_tracks_token;
  std::vector<StringCutObjectSelector<pat::Muon>> muon_selectors;
  std::vector<StringCutObjectSelector<pat::Electron>> electron_EB_selectors;
  std::vector<StringCutObjectSelector<pat::Electron>> electron_EE_selectors;
  EffectiveAreas electron_effective_areas;
  std::vector<edm::EDGetTokenT<double>> misc_tokens;
  const bool lightweight;
  LHAPDF::PDF* lhapdf;
};

namespace {
  template <typename T>
  std::vector<StringCutObjectSelector<T>> cuts2selectors(const std::vector<std::string>& cuts) {
    std::vector<StringCutObjectSelector<T>> ret;
    for (auto cut : cuts) ret.push_back(StringCutObjectSelector<T>(cut));
    return ret;
  }
}

MFVEventProducer::MFVEventProducer(const edm::ParameterSet& cfg)
  : input_is_miniaod(cfg.getParameter<bool>("input_is_miniaod")),
    triggerfloats_token(consumes<mfv::TriggerFloats>(cfg.getParameter<edm::InputTag>("triggerfloats_src"))),
    beamspot_token(consumes<reco::BeamSpot>(cfg.getParameter<edm::InputTag>("beamspot_src"))),
    primary_vertex_token(consumes<reco::VertexCollection>(cfg.getParameter<edm::InputTag>("primary_vertex_src"))),
    primary_vertex_scores_token(consumes<edm::ValueMap<float>>(cfg.getParameter<edm::InputTag>("primary_vertex_src"))),
    packed_candidates_token(consumes<pat::PackedCandidateCollection>(cfg.getParameter<edm::InputTag>("packed_candidates_src"))),
    gen_info_token(consumes<GenEventInfoProduct>(cfg.getParameter<edm::InputTag>("gen_info_src"))),
    gen_vertex_token(consumes<std::vector<double>>(cfg.getParameter<edm::InputTag>("gen_vertex_src"))),
    gen_jets_token(consumes<reco::GenJetCollection>(cfg.getParameter<edm::InputTag>("gen_jets_src"))),
    gen_particles_token(consumes<reco::GenParticleCollection>(cfg.getParameter<edm::InputTag>("gen_particles_src"))),
    mci_token(consumes<mfv::MCInteraction>(cfg.getParameter<edm::InputTag>("mci_src"))),
    pileup_summary_token(consumes<std::vector<PileupSummaryInfo> >(cfg.getParameter<edm::InputTag>("pileup_info_src"))),
    jets_token(consumes<pat::JetCollection>(cfg.getParameter<edm::InputTag>("jets_src"))),
    calo_jets_token(consumes<reco::CaloJetCollection>(cfg.getParameter<edm::InputTag>("calo_jets_src"))),
    rho_token(consumes<double>(cfg.getParameter<edm::InputTag>("rho_src"))),
    use_met(cfg.getParameter<edm::InputTag>("met_src").label() != ""),
    met_token(consumes<pat::METCollection>(cfg.getParameter<edm::InputTag>("met_src"))),
    muons_token(consumes<pat::MuonCollection>(cfg.getParameter<edm::InputTag>("muons_src"))),
    electrons_token(consumes<pat::ElectronCollection>(cfg.getParameter<edm::InputTag>("electrons_src"))),
    use_vertex_seed_tracks(cfg.getParameter<edm::InputTag>("vertex_seed_tracks_src").label() != ""),
    vertex_seed_tracks_token(consumes<reco::TrackCollection>(cfg.getParameter<edm::InputTag>("vertex_seed_tracks_src"))),
    muon_selectors(cuts2selectors<pat::Muon>(cfg.getParameter<std::vector<std::string>>("muon_cuts"))),
    electron_EB_selectors(cuts2selectors<pat::Electron>(cfg.getParameter<std::vector<std::string>>("electron_EB_cuts"))),
    electron_EE_selectors(cuts2selectors<pat::Electron>(cfg.getParameter<std::vector<std::string>>("electron_EE_cuts"))),
    electron_effective_areas(cfg.getParameter<edm::FileInPath>("electron_effective_areas").fullPath()),
    lightweight(cfg.getParameter<bool>("lightweight"))
{
  for (const edm::InputTag& src : cfg.getParameter<std::vector<edm::InputTag> >("misc_srcs"))
    misc_tokens.push_back(consumes<double>(src));

  produces<MFVEvent>();
  assert(muon_selectors.size() == MFVEvent::n_lep_mu_idrequired);
  assert(MFVEvent::n_lep_mu_idrequired == MFVEvent::n_lep_mu_idbits);
  assert(electron_EB_selectors.size() == electron_EE_selectors.size());
  assert(electron_EB_selectors.size() == MFVEvent::n_lep_el_idrequired);

  // setup LHAPDF for scale uncertainties
  lhapdf = mfv::setupLHAPDF();
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
  const math::XYZPoint primary_vertex_position = primary_vertex ? primary_vertex->position() : math::XYZPoint(0,0,0);
  edm::Handle<edm::ValueMap<float>> primary_vertex_scores;
  event.getByToken(primary_vertex_scores_token, primary_vertex_scores);

  edm::Handle<pat::PackedCandidateCollection> packed_candidates;
  if (input_is_miniaod)
    event.getByToken(packed_candidates_token, packed_candidates);

  //////////////////////////////////////////////////////////////////////

  mevent->gen_valid = false;

  if (!event.isRealData()) {
    edm::Handle<GenEventInfoProduct> gen_info;
    event.getByToken(gen_info_token, gen_info);

    mevent->gen_weight = gen_info->weight();

    for (double x : gen_info->weights())
      mevent->misc.push_back(x);

    if (gen_info->hasPDF()) {

      int id1 = gen_info->pdf()->id.first;
      int id2 = gen_info->pdf()->id.second;
      double x1 = gen_info->pdf()->x.first;
      double x2 = gen_info->pdf()->x.second;
      double xpdf1 = gen_info->pdf()->xPDF.first;
      double xpdf2 = gen_info->pdf()->xPDF.second;
      double qscale = gen_info->pdf()->scalePDF;

      // TODO move these to their own branches? but would need to propagate to MiniTree too
      mevent->misc.push_back(id1);
      mevent->misc.push_back(id2);
      mevent->misc.push_back(x1);
      mevent->misc.push_back(x2);
      mevent->misc.push_back(xpdf1);
      mevent->misc.push_back(xpdf2);
      mevent->misc.push_back(qscale);

      mevent->ren_weight_up = mfv::renormalization_weight(qscale,  1);
      mevent->ren_weight_dn = mfv::renormalization_weight(qscale, -1);
      mevent->fac_weight_up = mfv::factorization_weight(lhapdf, id1, id2, x1, x2, qscale,  1);
      mevent->fac_weight_dn = mfv::factorization_weight(lhapdf, id1, id2, x1, x2, qscale, -1);
    }

    edm::Handle<reco::GenJetCollection> gen_jets;
    event.getByToken(gen_jets_token, gen_jets);

    for (const reco::GenJet& jet : *gen_jets) {
      if (jet.pt() > 20 && fabs(jet.eta()) < 2.5) {
        double mue = 0, ele = 0;
        for (auto c : jet.getJetConstituents())
          if (abs(c->pdgId()) == 13)
            mue += c->energy();
          else if (abs(c->pdgId()) == 11)
            ele += c->energy();
        if (mue / jet.energy() < 0.8 && ele / jet.energy() < 0.9)
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

        for (const reco::GenParticleRef& s_temp : mci->secondaries(i)) {
          reco::GenParticle* s = (reco::GenParticle*)first_candidate(&*s_temp);
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
  mevent->hlt_caloht = triggerfloats->hltcaloht;

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

  assert(triggerfloats->FLTdecisions.size() == mfv::n_filter_paths);
  for (size_t i = 0; i < mfv::n_filter_paths; ++i) {
    const bool found = triggerfloats->FLTdecisions[i] != -1;
    mevent->pass_filter(i, found && triggerfloats->FLTdecisions[i]);
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

  const size_t npv = mevent->npv = int2uchar_clamp(primary_vertices->size());

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
    mevent->pv_score = (*primary_vertex_scores)[reco::VertexRef(primary_vertices, 0)];

    if (input_is_miniaod) {
      mevent->pv_ntracks = 0;
      mevent->pv_ntracksloose = 0;

      for (const pat::PackedCandidate& cand : *packed_candidates)
        if (cand.vertexRef().key() == 0 && cand.charge() && cand.hasTrackDetails()) {
          if (cand.pvAssociationQuality() == pat::PackedCandidate::UsedInFitTight) {
            inc_uchar_clamp(mevent->pv_ntracks);
            inc_uchar_clamp(mevent->pv_ntracksloose);
          }
          else if (cand.pvAssociationQuality() == pat::PackedCandidate::UsedInFitLoose)
            inc_uchar_clamp(mevent->pv_ntracksloose);
        }
    }
    else {
      mevent->pv_ntracks = int2uchar_clamp(primary_vertex->nTracks());
      mevent->pv_ntracksloose = int2uchar_clamp(primary_vertex->nTracks(0.));
    }

    for (size_t i = 1; i < npv; ++i) {
      mevent->pvsx.push_back((*primary_vertices)[i].x());
      mevent->pvsy.push_back((*primary_vertices)[i].y());
      mevent->pvsz.push_back((*primary_vertices)[i].z());
      mevent->pvsscores.push_back((*primary_vertex_scores)[reco::VertexRef(primary_vertices, i)]);
    }
  }

  //////////////////////////////////////////////////////////////////////

  if (use_met) {
    // getting MET using original source
    //edm::Handle<pat::METCollection> mets;
    //event.getByToken(met_token, mets);
    //const pat::MET& met = mets->at(0);
    //mevent->metx = met.px();
    //mevent->mety = met.py();

    // getting corrected MET from TriggerFloats
    mevent->pass_metfilters = triggerfloats->pass_metfilters;

    double met_pt = triggerfloats->met_pt;
    double met_phi = triggerfloats->met_phi;
    mevent->metx = met_pt*std::cos(met_phi);
    mevent->mety = met_pt*std::sin(met_phi);
    mevent->met_calo = triggerfloats->met_pt_calo;

    double metNoMu_pt = triggerfloats->met_pt_nomu;
    double metNoMu_phi = triggerfloats->met_phi_nomu;
    mevent->metNoMux = metNoMu_pt*std::cos(metNoMu_phi);
    mevent->metNoMuy = metNoMu_pt*std::sin(metNoMu_phi);
  }

  //////////////////////////////////////////////////////////////////////

  edm::Handle<pat::JetCollection> jets;
  event.getByToken(jets_token, jets);

  edm::Handle<double> rho;
  event.getByToken(rho_token, rho);


  for (int jjet = 0, jjete = int(jets->size()); jjet < jjete; ++jjet) {
    const pat::Jet& jet = jets->at(jjet);

    mevent->jet_pudisc.push_back(jet.userFloat("pileupJetId:fullDiscriminant")); // to be removed and put into _id when working points defined
    mevent->jet_pt.push_back(jet.pt());
    mevent->jet_raw_pt.push_back(jet.pt()*jet.jecFactor("Uncorrected"));
    mevent->jet_bdisc_csv.push_back(jmt::BTagging::discriminator(jet, 0));
    mevent->jet_bdisc_deepcsv.push_back(jmt::BTagging::discriminator(jet, 1));
    mevent->jet_bdisc_deepflav.push_back(jmt::BTagging::discriminator(jet, 2));
    mevent->jet_eta.push_back(jet.eta());
    mevent->jet_phi.push_back(jet.phi());
    mevent->jet_energy.push_back(jet.energy());
    mevent->jet_gen_energy.push_back(jet.genJet() ? jet.genJet()->energy() : -1);

    // match trigger and offline jets
    mevent->jet_hlt_push_back(jet, triggerfloats->hltpfjets, false);
    mevent->jet_hlt_push_back(jet, triggerfloats->hltcalojets, true);

    int bdisc_level = 0;
    for (int i = 0; i < 3; ++i)
      if (jmt::BTagging::is_tagged(jet, i))
        bdisc_level = i+1;

    mevent->jet_id.push_back(MFVEvent::encode_jet_id(0, bdisc_level, jet.hadronFlavour()));
    const size_t ijet = mevent->njets() - 1; // will stay in track with jjet as long as jets are pt ordered...

    assert(ijet <= 255);
    for (size_t idau = 0, idaue = jet.numberOfDaughters(); idau < idaue; ++idau) {
      // handle both regular aod and miniaod: in the latter
      // getPFConstituents() doesn't work because the daughters are
      // pat::PackedCandidates. Since we don't care about track
      // identities e.g. to compare with vertices we don't use
      // TrackRefGetter here, but could
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
        if (pk && pk->charge() && pk->hasTrackDetails())
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
        mevent->jet_track_hp_push_back(tk->hitPattern().numberOfValidPixelHits(), tk->hitPattern().numberOfValidStripHits(), tk->hitPattern().pixelLayersWithMeasurement(), tk->hitPattern().stripLayersWithMeasurement());
      }
    }
  }

  edm::Handle<reco::CaloJetCollection> calo_jets;
  event.getByToken(calo_jets_token, calo_jets);

  for (const reco::CaloJet& cjet : *calo_jets) {
    mevent->calo_jet_pt.push_back(cjet.pt());
    mevent->calo_jet_eta.push_back(cjet.eta());
    mevent->calo_jet_phi.push_back(cjet.phi());
    mevent->calo_jet_energy.push_back(cjet.energy());
  }

  for (const TLorentzVector& jp4 : triggerfloats->hltpfjets) {
    mevent->hlt_pf_jet_pt.push_back(jp4.Pt());
    mevent->hlt_pf_jet_eta.push_back(jp4.Eta());
    mevent->hlt_pf_jet_phi.push_back(jp4.Phi());
    mevent->hlt_pf_jet_energy.push_back(jp4.E());

  }

  for (const TLorentzVector& cp4 : triggerfloats->hltcalojets) {
    mevent->hlt_calo_jet_pt.push_back(cp4.Pt());
    mevent->hlt_calo_jet_eta.push_back(cp4.Eta());
    mevent->hlt_calo_jet_phi.push_back(cp4.Phi());
    mevent->hlt_calo_jet_energy.push_back(cp4.E());

  } 

  for (const TLorentzVector& pp4 : triggerfloats->hltidpassedcalojets) {
     mevent->hlt_idp_calo_jet_pt.push_back(pp4.Pt());
     mevent->hlt_idp_calo_jet_eta.push_back(pp4.Eta());
     mevent->hlt_idp_calo_jet_phi.push_back(pp4.Phi());
     mevent->hlt_idp_calo_jet_energy.push_back(pp4.E());
  }

  for (const TLorentzVector& bp4 : triggerfloats->hltpfjetsforbtag) {
     mevent->hlt_pfforbtag_jet_pt.push_back(bp4.Pt());
     mevent->hlt_pfforbtag_jet_eta.push_back(bp4.Eta());
     mevent->hlt_pfforbtag_jet_phi.push_back(bp4.Phi());
     mevent->hlt_pfforbtag_jet_energy.push_back(bp4.E());
  }


  for (const TLorentzVector& ap4 : triggerfloats->hltcalojets_lowpt_fewprompt) {
     mevent->hlt_calo_jet_lowpt_fewprompt_pt.push_back(ap4.Pt());
     mevent->hlt_calo_jet_lowpt_fewprompt_eta.push_back(ap4.Eta());
     mevent->hlt_calo_jet_lowpt_fewprompt_phi.push_back(ap4.Phi());
     mevent->hlt_calo_jet_lowpt_fewprompt_energy.push_back(ap4.E());
  }


  for (const TLorentzVector& dp4 : triggerfloats->hltcalojets_lowpt_wdisptks) {
     mevent->hlt_calo_jet_lowpt_wdisptks_pt.push_back(dp4.Pt());
     mevent->hlt_calo_jet_lowpt_wdisptks_eta.push_back(dp4.Eta());
     mevent->hlt_calo_jet_lowpt_wdisptks_phi.push_back(dp4.Phi());
     mevent->hlt_calo_jet_lowpt_wdisptks_energy.push_back(dp4.E());
  }


  for (const TLorentzVector& mp4 : triggerfloats->hltcalojets_midpt_fewprompt) {
     mevent->hlt_calo_jet_midpt_fewprompt_pt.push_back(mp4.Pt());
     mevent->hlt_calo_jet_midpt_fewprompt_eta.push_back(mp4.Eta());
     mevent->hlt_calo_jet_midpt_fewprompt_phi.push_back(mp4.Phi());
     mevent->hlt_calo_jet_midpt_fewprompt_energy.push_back(mp4.E());
  }

  //////////////////////////////////////////////////////////////////////

  edm::Handle<pat::MuonCollection> muons;
  event.getByToken(muons_token, muons);

  for (const pat::Muon& muon : *muons) {
    MFVEvent::lep_id_t id = 0;
    for (int i = 0, ie = muon_selectors.size(); i < ie; ++i)
      if (muon_selectors[i](muon))
        id |= 1 << i;

    const float iso = (muon.pfIsolationR04().sumChargedHadronPt + std::max(0., muon.pfIsolationR04().sumNeutralHadronEt + muon.pfIsolationR04().sumPhotonEt - 0.5*muon.pfIsolationR04().sumPUPt))/muon.pt();

    mevent->lep_push_back(MFVEvent::encode_mu_id(id), muon, *muon.bestTrack(), iso, triggerfloats->hltmuons, beamspot->position(muon.bestTrack()->vz()), primary_vertex_position);
  }

  edm::Handle<pat::ElectronCollection> electrons;
  event.getByToken(electrons_token, electrons);
  
  for (const pat::Electron& electron : *electrons) {
    if (!electron.isEB() && !electron.isEE()) continue;
    auto electron_selectors = electron.isEB() ? electron_EB_selectors : electron_EE_selectors;

    MFVEvent::lep_id_t id = 0;
    for (int i = 0, ie = electron_selectors.size(); i < ie; ++i) {
      if (i == MFVEvent::lep_el_hovere) continue; // skip for below code
      if (electron_selectors[i](electron))
        id |= 1 << i;
    }

    if (electron.hadronicOverEm() < 0.05 + (electron.isEB() ? 1.12 + 0.0368 * *rho : 0.5 + 0.201 * *rho) / electron.superCluster()->energy())
      id |= 1 << MFVEvent::lep_el_hovere;
    if (electron.passConversionVeto())
      id |= 1 << MFVEvent::lep_el_conversionveto;
    if (electron.closestCtfTrackRef().isNonnull())
      id |= 1 << MFVEvent::lep_el_ctftrack;

    const auto pfIso = electron.pfIsolationVariables();
    const float eA = electron_effective_areas.getEffectiveArea(fabs(electron.superCluster()->eta()));
    const float iso = pfIso.sumChargedHadronPt + std::max(0., pfIso.sumNeutralHadronEt + pfIso.sumPhotonEt - *rho*eA) / electron.pt();

    mevent->lep_push_back(MFVEvent::encode_el_id(id), electron, *electron.gsfTrack(), iso, triggerfloats->hltelectrons, beamspot->position(electron.gsfTrack()->vz()), primary_vertex_position);
  }

  //////////////////////////////////////////////////////////////////////

  if (use_vertex_seed_tracks) {
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
      mevent->vertex_seed_track_err_pt.push_back(tk.ptError());
      mevent->vertex_seed_track_err_eta.push_back(tk.etaError());
      mevent->vertex_seed_track_err_phi.push_back(tk.phiError());
      mevent->vertex_seed_track_err_dxy.push_back(tk.dxyError());
      mevent->vertex_seed_track_err_dz.push_back(tk.dzError());
      mevent->vertex_seed_track_hp_push_back(tk.hitPattern().numberOfValidPixelHits(), tk.hitPattern().numberOfValidStripHits(), tk.hitPattern().pixelLayersWithMeasurement(), tk.hitPattern().stripLayersWithMeasurement());
    }
  }

  //////////////////////////////////////////////////////////////////////

  for (auto t : misc_tokens) {
    edm::Handle<double> m;
    event.getByToken(t, m);
    mevent->misc.push_back(*m);
  }

  //////////////////////////////////////////////////////////////////////

  if (lightweight) {
    // keep
    // for weight: gen_weight, npv, , npu
    // for trigger: pass_
    // for njets and ht40: jet_pt vector
    // jet_id vector
    // beamspot and slopes, pvx,y,z
    // HLT jet pt, offline bdisc, and offline jet eta information for trigger matching

    mevent->gen_valid = 0;
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
    mevent->bswidthx = 0;
    mevent->bswidthy = 0;
    mevent->pvcxx = 0;
    mevent->pvcxy = 0;
    mevent->pvcxz = 0;
    mevent->pvcyy = 0;
    mevent->pvcyz = 0;
    mevent->pvczz = 0;
    mevent->pv_ntracks = 0;
    mevent->pv_score = 0;
    mevent->pvsx.clear();
    mevent->pvsy.clear();
    mevent->pvsz.clear();
    mevent->pvsscores.clear();
    mevent->jet_pudisc.clear();
    mevent->jet_raw_pt.clear();
    mevent->jet_phi.clear();
    mevent->jet_energy.clear();
    mevent->jet_hlt_eta.clear();
    mevent->jet_hlt_phi.clear();
    mevent->jet_hlt_energy.clear();
    mevent->displaced_jet_hlt_eta.clear();
    mevent->displaced_jet_hlt_phi.clear();
    mevent->displaced_jet_hlt_energy.clear();
    mevent->metx = 0;
    mevent->mety = 0;
    mevent->lep_id_.clear();
    mevent->lep_qpt.clear();
    mevent->lep_eta.clear();
    mevent->lep_phi.clear();
    mevent->lep_dxy.clear();
    mevent->lep_dxybs.clear();
    mevent->lep_dz.clear();
    mevent->lep_pt_err.clear();
    mevent->lep_eta_err.clear();
    mevent->lep_phi_err.clear();
    mevent->lep_dxy_err.clear();
    mevent->lep_dz_err.clear();
    mevent->lep_iso.clear();
    mevent->lep_hlt_pt.clear();
    mevent->lep_hlt_eta.clear();
    mevent->lep_hlt_phi.clear();
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
