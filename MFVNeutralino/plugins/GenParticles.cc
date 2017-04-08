#include "DataFormats/BeamSpot/interface/BeamSpot.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/HepMCCandidate/interface/GenParticleFwd.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "JMTucker/Tools/interface/GenUtilities.h"
#include "JMTucker/Tools/interface/Utilities.h"
#include "JMTucker/MFVNeutralinoFormats/interface/MCInteractions.h"

class MFVGenParticles : public edm::EDProducer {
public:
  explicit MFVGenParticles(const edm::ParameterSet&);

private:
  void produce(edm::Event&, const edm::EventSetup&) override;

  const edm::EDGetTokenT<reco::GenParticleCollection> gen_particles_token;
  const edm::EDGetTokenT<reco::BeamSpot> beamspot_token;
  const bool debug;
  int lsp_id;

  void set_Ttbar_decay(mfv::MCInteractionHolderTtbar&, const edm::Handle<reco::GenParticleCollection>&) const;

  bool try_MFVtbs  (mfv::MCInteraction&, const edm::Handle<reco::GenParticleCollection>&) const;
  bool try_Ttbar   (mfv::MCInteraction&, const edm::Handle<reco::GenParticleCollection>&) const;
  bool try_XX4j    (mfv::MCInteraction&, const edm::Handle<reco::GenParticleCollection>&) const;
  bool try_MFVdijet(mfv::MCInteraction&, const edm::Handle<reco::GenParticleCollection>&) const;
  bool try_MFVlq   (mfv::MCInteraction&, const edm::Handle<reco::GenParticleCollection>&) const;
};

MFVGenParticles::MFVGenParticles(const edm::ParameterSet& cfg) 
  : gen_particles_token(consumes<reco::GenParticleCollection>(cfg.getParameter<edm::InputTag>("gen_particles_src"))),
    beamspot_token(consumes<reco::BeamSpot>(cfg.getParameter<edm::InputTag>("beamspot_src"))),
    debug(cfg.getUntrackedParameter<bool>("debug", false)),
    lsp_id(-1)
{
  produces<mfv::MCInteraction>();
  produces<std::vector<double>>(); // decay positions

  // these for event display
  produces<reco::GenParticleCollection>("primaries");
  produces<reco::GenParticleCollection>("secondaries");
  produces<reco::GenParticleCollection>("visible");
}

void MFVGenParticles::set_Ttbar_decay(mfv::MCInteractionHolderTtbar& mc, const edm::Handle<reco::GenParticleCollection>& gen_particles) const {
  if (debug) printf("MFVGenParticles::set_Ttbar_decay\n");

  if (mc.tops[0].isNull() || mc.tops[1].isNull() ||
      abs(mc.tops[0]->pdgId()) != 6 || abs(mc.tops[1]->pdgId()) != 6 ||
      mc.tops[0]->numberOfDaughters() < 2 || mc.tops[1]->numberOfDaughters() < 2) {
    print_gen_and_daus(0, "header", *gen_particles, true, true);
    print_gen_and_daus(mc.tops[0], "tops 0", *gen_particles, true, true);
    print_gen_and_daus(mc.tops[1], "tops 1", *gen_particles, true, true);
    throw cms::Exception("BadAssumption", "set_decay and a problem with a top?");
  }

  mc.num_leptonic = 0;

  for (int which = 0; which < 2; ++which) {
    // Find the Ws and bs from top decay. Bottom or bottombar might
    // not be there, since |Vtb| isn't exactly 1.
    mc.Ws     [which] = gen_ref(daughter_with_id(mc.tops[which], sgn(mc.tops[which]->pdgId()) * 24), gen_particles);
    mc.bottoms[which] = gen_ref(daughter_with_id(mc.tops[which], sgn(mc.tops[which]->pdgId()) *  5), gen_particles);

    if (mc.Ws[which].isNull())
      throw cms::Exception("BadAssumption") << "W #" << which << " not found";

    // The W may have a lot of copies, but the copies should always
    // have just one daughter until we reach the actual W decay (qq'
    // or lnu). Find the last one. ("2" means only photons allowed
    // besides the W copies.)
    mc.Ws[which] = gen_ref(final_candidate(mc.Ws[which], 2), gen_particles);
    if (mc.Ws[which]->numberOfDaughters() < 2)
      throw cms::Exception("BadAssumption") << "W #" << which << " did not have at least two daughters: id " << mc.Ws[which]->pdgId() << " numDau " << mc.Ws[which]->numberOfDaughters();

    // Bottom or bottombar might not be there, since |Vtb| isn't
    // exactly 1. If the top decayed into some other down-type quark,
    // grab it, trying strange and down in turn. Client code has to
    // check if "bottoms[which]" was actually a bottom if needed.
    if (mc.bottoms[which].isNull()) {
      mc.bottoms[which]   = gen_ref(daughter_with_id(mc.tops[which], sgn(mc.tops[which]->pdgId()) * 3), gen_particles);
      if (mc.bottoms[which].isNull()) {
	mc.bottoms[which] = gen_ref(daughter_with_id(mc.tops[which], sgn(mc.tops[which]->pdgId()) * 1), gen_particles);
	if (mc.bottoms[which].isNull())
          throw cms::Exception("BadAssumption", "could not find down-type quark from top #") << which;
      }
    }

    // Get the final copy for the bottom. -1 means anything goes (seen
    // hadronization products instead of just gluons and photons in
    // one event).
    mc.bottoms[which] = gen_ref(final_candidate(mc.bottoms[which], -1), gen_particles);

    // Find the W daughters, and store them in the order (down-type
    // quark, up-type quark) or (charged lepton, neutrino).
    std::vector<const reco::Candidate*> daus;
    for (int j = 0, je = mc.Ws[which]->numberOfDaughters(); j < je; ++j) {
      const reco::Candidate* d = mc.Ws[which]->daughter(j);
      if (d->pdgId() != mc.Ws[which]->pdgId()) // The W can have a copy of itself as a daughter, in addition to qqbar' or lnu.
	daus.push_back(d);
    }
    if (daus.size() != 2)
      throw cms::Exception("BadAssumption") << "W #" << which << " did not have exactly two non-W daughters";
    const int order = abs(daus[0]->pdgId()) % 2 == 0;
    mc.W_daughters[which][0] = gen_ref(daus[ order], gen_particles);
    mc.W_daughters[which][1] = gen_ref(daus[!order], gen_particles);
    if (mc.W_daughters[which][0].isNull() || mc.W_daughters[which][1].isNull())
      throw cms::Exception("BadAssumption") << "W #" << which << " daughter refs not found";

    // Finalize the W daughters.
    mc.W_daughters[which][0] = gen_ref(final_candidate(mc.W_daughters[which][0], -1), gen_particles);
    mc.W_daughters[which][1] = gen_ref(final_candidate(mc.W_daughters[which][1], -1), gen_particles);

    if (is_quark(mc.W_daughters[which][0])) {
      if (!is_quark(mc.W_daughters[which][1]))
        throw cms::Exception("BadAssumption", "one W daughter is quark but other is not");
    }
    else {
      if (!is_lepton(mc.W_daughters[which][0]) || !is_lepton(mc.W_daughters[which][1]))
        throw cms::Exception("BadAssumption", "one W daughter is lepton and other is not");
      ++mc.num_leptonic;
    }  
    mc.decay_type[which] = lepton_code(mc.W_daughters[which][0]);

    // testing
    assert(mc.tops[which]->statusFlags().isLastCopy());
    assert(mc.Ws[which]->statusFlags().isLastCopy());
    assert(mc.bottoms[which]->statusFlags().isLastCopy());
    assert(mc.W_daughters[which][0]->statusFlags().isLastCopy());
    assert(mc.W_daughters[which][1]->statusFlags().isLastCopy());
  }
}

bool MFVGenParticles::try_MFVtbs(mfv::MCInteraction& mc, const edm::Handle<reco::GenParticleCollection>& gen_particles) const {
  if (debug) printf("MFVGenParticles::try_MFVtbs\n");

  mfv::MCInteractionHolderMFVtbs h;

  // Find the LSPs (e.g. gluinos or neutralinos). Since this is
  // PYTHIA8 there are lots of copies -- try to get the ones that
  // decay to the three quarks.
  for (int i = 0, ie = int(gen_particles->size()); i < ie; ++i) {
    const reco::GenParticle& gen = gen_particles->at(i);
    if (gen.pdgId() != lsp_id || gen.numberOfDaughters() != 3)
      continue;
    reco::GenParticleRef lsp(gen_particles, i);

    size_t which = 0;
    if (h.lsps[0].isNull())
      h.lsps[0] = lsp;
    else {
      if (reco::deltaR(*h.lsps[0], gen) < 0.001)
	throw cms::Exception("BadAssumption", "may have found same LSP twice based on deltaR < 0.001");
      which = 1;
      h.lsps[1] = lsp;
    }

    // Get the daughters. 
    // The last true param of daughter_with_id means take absolute value, so that e.g. strange or antistrange is OK.
    // If any are bad, let the mc object be half-formed/invalid.
    if ((h.stranges       [which] = gen_ref(daughter_with_id(&*lsp, 3, true), gen_particles)).isNull()) return false;
    if ((h.primary_bottoms[which] = gen_ref(daughter_with_id(&*lsp, 5, true), gen_particles)).isNull()) return false;
    if ((h.tops           [which] = gen_ref(daughter_with_id(&*lsp, 6, true), gen_particles)).isNull()) return false;

    // The -1 in final_candidate for the tops used to be 3 for
    // allowing radiated gluons or photons but with official sample
    // pythia got a top that had protons and pions and kaons oh my 42/-6 111/21 112/21 113/21 121/2212 122/2212 123/2212 124/2212 157/310 158/310
    h.stranges       [which] = gen_ref(final_candidate(h.stranges       [which], -1), gen_particles);
    h.primary_bottoms[which] = gen_ref(final_candidate(h.primary_bottoms[which], -1), gen_particles);
    h.tops           [which] = gen_ref(final_candidate(h.tops           [which], -1), gen_particles);

    // testing
    assert(lsp                     ->statusFlags().isLastCopy());
    assert(h.stranges       [which]->statusFlags().isLastCopy());
    assert(h.primary_bottoms[which]->statusFlags().isLastCopy());
    assert(h.tops           [which]->statusFlags().isLastCopy());
  }

  if (h.lsps[0].isNull() || h.stranges[0].isNull() || h.primary_bottoms[0].isNull() || h.tops[0].isNull() ||
      h.lsps[1].isNull() || h.stranges[1].isNull() || h.primary_bottoms[1].isNull() || h.tops[1].isNull())
    return false;

  set_Ttbar_decay(h, gen_particles);
  
  if (h.valid()) {
    mc.set(h);
    return true;
  }
  else
    return false;
}

bool MFVGenParticles::try_Ttbar(mfv::MCInteraction& mc, const edm::Handle<reco::GenParticleCollection>& gen_particles) const {
  if (debug) printf("MFVGenParticles::try_Ttbar\n");

  mfv::MCInteractionHolderTtbar h;

  for (size_t i = 0, ie = gen_particles->size(); i < ie; ++i) {    
    reco::GenParticleRef r(gen_particles, i);
    const int id = r->pdgId();
    if      (id ==  6) h.tops[0] = r;
    else if (id == -6) h.tops[1] = r;
  }

  if (h.tops[0].isNonnull() && h.tops[1].isNonnull()) {
    h.tops[0] = gen_ref(final_candidate(h.tops[0], -1), gen_particles);
    h.tops[1] = gen_ref(final_candidate(h.tops[1], -1), gen_particles);

    assert(h.tops[0]->statusFlags().isLastCopy());
    assert(h.tops[1]->statusFlags().isLastCopy());

    set_Ttbar_decay(h, gen_particles);
  }

  if (h.valid()) {
    mc.set(h);
    return true;
  }
  else
    return false;
}

// JMTBAD unify try_XX4j/MFVdijet/MFVlq

bool MFVGenParticles::try_XX4j(mfv::MCInteraction& mc, const edm::Handle<reco::GenParticleCollection>& gen_particles) const {
  if (debug) printf("MFVGenParticles::try_XX4j\n");

  mfv::MCInteractionHolderXX4j h;

  // Find the H and the A. Start from the end and get the last ones,
  // they should be the ones that go to the pairs of quarks.
  for (int i = int(gen_particles->size()) - 1; i >= 0; --i) {
    const reco::GenParticle& gen = gen_particles->at(i);
    const int id = gen.pdgId();
    if ((id != 35 && id != 36) || gen.numberOfDaughters() != 2)
      continue;
    const int aid0 = abs(gen.daughter(0)->pdgId());
    const int aid1 = abs(gen.daughter(1)->pdgId());
    if (aid0 != aid1 || aid0 < 1 || aid0 > 5)
      continue;
    const int which(id == 35); // put A in index 0

    if (h.p[which].isNonnull())
      throw cms::Exception("BadAssumption", "found duplicate for id") << " " << id;

    h.p[which] = reco::GenParticleRef(gen_particles, i);
    h.decay_id[which] = aid0;

    const int which2(h.p[which]->daughter(0)->pdgId() > 0);
    h.s[which][0] = gen_ref(final_candidate(h.p[which]->daughter(!which2), 3), gen_particles);
    h.s[which][1] = gen_ref(final_candidate(h.p[which]->daughter( which2), 3), gen_particles);

    // testing
    assert(h.p[which]   ->statusFlags().isLastCopy());
    assert(h.s[which][0]->statusFlags().isLastCopy());
    assert(h.s[which][1]->statusFlags().isLastCopy());
  }

  if (h.valid()) {
    mc.set(h);
    return true;
  }
  else
    return false;
}

bool MFVGenParticles::try_MFVdijet(mfv::MCInteraction& mc, const edm::Handle<reco::GenParticleCollection>& gen_particles) const {
  if (debug) printf("MFVGenParticles::try_MFVdijet\n");

  mfv::MCInteractionHolderMFVdijet h;

  // Find the LSPs (e.g. gluinos or neutralinos). Since this is
  // PYTHIA8 there are lots of copies -- try to get the ones that
  // decay to the three quarks.
  int found = 0;
  for (int i = int(gen_particles->size()) - 1; i >= 0 && found < 2; --i) {
    const reco::GenParticle& gen = gen_particles->at(i);
    reco::GenParticleRef ref(gen_particles, i);
    if (gen.pdgId() != lsp_id || gen.numberOfDaughters() != 2)
      continue;
    ++found;

    size_t which = 0;
    if (h.p[0].isNull())
      h.p[0] = ref;
    else {
      if (reco::deltaR(*h.p[0], gen) < 0.001)
	throw cms::Exception("BadAssumption", "may have found same LSP twice based on deltaR < 0.001");
      which = 1;
      h.p[1] = ref;
    }

    // Get the immediate daughters. 
    if ((h.s[which][0] = gen_ref(daughter_with_id(&gen,  1, false), gen_particles)).isNull() ||
        (h.s[which][1] = gen_ref(daughter_with_id(&gen, -1, false), gen_particles)).isNull()) {
      printf("WEIRD GLUBALL CRAP???\n");
      return false;
    }

    h.decay_id[which] = 1;
    h.s[which][0] = gen_ref(final_candidate(h.s[which][0], 3), gen_particles);
    h.s[which][1] = gen_ref(final_candidate(h.s[which][1], 3), gen_particles);

    assert(h.p[which]   ->statusFlags().isLastCopy());
    assert(h.s[which][0]->statusFlags().isLastCopy());
    assert(h.s[which][1]->statusFlags().isLastCopy());
  }

  if (h.valid()) {
    mc.set(h);
    return true;
  }
  else
    return false;
}

bool MFVGenParticles::try_MFVlq(mfv::MCInteraction& mc, const edm::Handle<reco::GenParticleCollection>& gen_particles) const {
  if (debug) printf("MFVGenParticles::try_MFVlq\n");

  mfv::MCInteractionHolderMFVlq h;

  // Find the LQ and the LQbar. Start from the end and get the last ones,
  // they should be the ones that go to the pairs of quarks.
  for (int i = int(gen_particles->size()) - 1; i >= 0; --i) {
    const reco::GenParticle& lq = gen_particles->at(i);
    reco::GenParticleRef ref(gen_particles, i);
    const int id = lq.pdgId();
    if (abs(id) != 42 || lq.numberOfDaughters() != 2)
      continue;

    const int aid[2] = {abs(lq.daughter(0)->pdgId()),
                        abs(lq.daughter(1)->pdgId())};
    bool is_q [2] = {0};
    bool is_l[2] = {0};
    for (int j = 0; j < 2; ++j) {
      is_q[j] = aid[j] >= 1 && aid[j] <= 5;
      is_l[j] = aid[j] == 11 || aid[j] == 13 || aid[j] == 15; // neutrinos?
    }

    if (!(is_q[0] && is_l[1]) && !(is_q[1] && is_l[0]))
      continue;

    const int which = !(id > 0); // LQ index 0
    if (h.p[which].isNonnull())
      throw cms::Exception("BadAssumption", "found duplicate for id") << " " << id;
    h.p[which] = ref;

    const int whichq = !is_q[0];
    h.decay_id[which] = (aid[!whichq] - 11) / 2 + 1;
    h.s[which][0] = gen_ref(final_candidate(lq.daughter( whichq), 3), gen_particles);
    h.s[which][1] = gen_ref(final_candidate(lq.daughter(!whichq), 3), gen_particles);

    assert(h.p[which]   ->statusFlags().isLastCopy());
    assert(h.s[which][0]->statusFlags().isLastCopy());
    assert(h.s[which][1]->statusFlags().isLastCopy());
  }

  if (h.valid()) {
    mc.set(h);
    return true;
  }
  else
    return false;
}

void MFVGenParticles::produce(edm::Event& event, const edm::EventSetup&) {
  std::auto_ptr<mfv::MCInteraction> mc(new mfv::MCInteraction);
  std::auto_ptr<std::vector<double> > decay_vertices(new std::vector<double>);
  std::auto_ptr<reco::GenParticleCollection> primaries  (new reco::GenParticleCollection);
  std::auto_ptr<reco::GenParticleCollection> secondaries(new reco::GenParticleCollection);
  std::auto_ptr<reco::GenParticleCollection> visible    (new reco::GenParticleCollection);

  if (!event.isRealData()) {
    edm::Handle<reco::GenParticleCollection> gen_particles;
    event.getByToken(gen_particles_token, gen_particles);

    if (lsp_id == -1) {
      // If there is a neutralino in the first event, assume that's the
      // LSP id wanted. Otherwise, default to looking for gluino. This
      // isn't relevant for some signals.
      lsp_id = 1000021;
      for (int i = 0, ie = int(gen_particles->size()); i < ie; ++i)
        if (gen_particles->at(i).pdgId() == 1000022) {
          lsp_id = 1000022;
          break;
        }
    }

    if (debug) printf("MFVGenParticles::analyze: lsp_id %i\n", lsp_id);

    // the order of these tries is important, at least that MFVtbs comes before Ttbar
    try_MFVtbs  (*mc, gen_particles) ||
    try_Ttbar   (*mc, gen_particles) || 
    try_XX4j    (*mc, gen_particles) ||
    try_MFVdijet(*mc, gen_particles) ||
    try_MFVlq   (*mc, gen_particles);

    if (mc->valid()) {
      for (auto r : mc->primaries())   primaries  ->push_back(*r);
      for (auto r : mc->secondaries()) secondaries->push_back(*r);
      for (auto r : mc->visible())     visible    ->push_back(*r);

      for (int i = 0; i < 2; ++i) {
        auto p = mc->decay_point(i);
        decay_vertices->push_back(p.x);
        decay_vertices->push_back(p.y);
        decay_vertices->push_back(p.z);
      }
    }
  }
  else {
    if (debug) printf("MFVGenParticles: running on data, not MC\n");
  }

  if (decay_vertices->empty()) {
    if (debug) printf("MFVGenParticles: using beamspot for decay position\n");

    edm::Handle<reco::BeamSpot> beamspot;
    event.getByToken(beamspot_token, beamspot);

    for (int i = 0; i < 2; ++i) {
      decay_vertices->push_back(beamspot->x0());
      decay_vertices->push_back(beamspot->y0());
      decay_vertices->push_back(beamspot->z0());
    }
  }

  if (debug) {
    std::cout << "MFVGenParticles " << *mc << "MFVGenParticles decay_vertices:";
    for (double d : *decay_vertices)
      printf(" %6.3f", d);
    printf("\n");
  }

  event.put(mc);
  event.put(decay_vertices);
  event.put(primaries,   "primaries");
  event.put(secondaries, "secondaries");
  event.put(visible,     "visible");
}

DEFINE_FWK_MODULE(MFVGenParticles);
