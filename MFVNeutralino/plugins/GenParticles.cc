// JMTBAD unify try_XX4j/MFVdijet/MFVlq and try_MFVtbs/uds

#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/BeamSpot/interface/BeamSpot.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/HepMCCandidate/interface/GenParticleFwd.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
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
  const bool last_flag_check;
  const bool debug;
  const bool histos;
  int lsp_id;

  void set_Ttbar_decay(mfv::MCInteractionHolderTtbar&, const edm::Handle<reco::GenParticleCollection>&) const;

  bool try_MFVtbs      (mfv::MCInteraction&, const edm::Handle<reco::GenParticleCollection>&, int t1, int t2) const;
  bool try_Ttbar       (mfv::MCInteraction&, const edm::Handle<reco::GenParticleCollection>&) const;
  bool try_MFVthree    (mfv::MCInteraction&, const edm::Handle<reco::GenParticleCollection>&, int t1, int t2, int t3) const;
  bool try_XX4j        (mfv::MCInteraction&, const edm::Handle<reco::GenParticleCollection>&) const;
  bool try_MFVdijet    (mfv::MCInteraction&, const edm::Handle<reco::GenParticleCollection>&, int quark) const;
  bool try_stopdbardbar(mfv::MCInteraction&, const edm::Handle<reco::GenParticleCollection>&, int quark) const;
  bool try_MFVlq       (mfv::MCInteraction&, const edm::Handle<reco::GenParticleCollection>&) const;
  bool try_splitSUSY   (mfv::MCInteraction&, const edm::Handle<reco::GenParticleCollection>&) const;
  bool try_MFV_stoplq   (mfv::MCInteraction&, const edm::Handle<reco::GenParticleCollection>&) const;

  TH1F* h_valid;
  TH1F* h_pos_check;
};

MFVGenParticles::MFVGenParticles(const edm::ParameterSet& cfg) 
  : gen_particles_token(consumes<reco::GenParticleCollection>(cfg.getParameter<edm::InputTag>("gen_particles_src"))),
    beamspot_token(consumes<reco::BeamSpot>(cfg.getParameter<edm::InputTag>("beamspot_src"))),
    last_flag_check(cfg.getParameter<bool>("last_flag_check")),
    debug(cfg.getUntrackedParameter<bool>("debug", false)),
    histos(cfg.getUntrackedParameter<bool>("histos", true)),
    lsp_id(cfg.getUntrackedParameter<int>("lsp_id", -1))
{
  produces<mfv::MCInteraction>();
  produces<std::vector<double>>("genVertex"); // generated primary vertex
  produces<std::vector<double>>("decays"); // decay positions

  // these for event display
  produces<reco::GenParticleCollection>("primaries");
  produces<reco::GenParticleCollection>("secondaries");
  produces<reco::GenParticleCollection>("visible");

  if (histos) {
    edm::Service<TFileService> fs;
    h_valid = fs->make<TH1F>("h_valid", "", 2, 0, 2);
    h_pos_check = fs->make<TH1F>("h_pos_check", "", 100, 0, 0.01);
  }
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
    // or lnu). Find the last one.
    mc.Ws[which] = gen_ref(final_candidate(mc.Ws[which], -1), gen_particles);
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

    if (last_flag_check) {
      assert(mc.tops[which]->statusFlags().isLastCopy());
      assert(mc.Ws[which]->statusFlags().isLastCopy());
      assert(mc.bottoms[which]->statusFlags().isLastCopy());
      assert(mc.W_daughters[which][0]->statusFlags().isLastCopy());
      assert(mc.W_daughters[which][1]->statusFlags().isLastCopy());
    }
  }
}

bool MFVGenParticles::try_MFVtbs(mfv::MCInteraction& mc, const edm::Handle<reco::GenParticleCollection>& gen_particles, int t1, int t2) const {
  if (debug) printf("MFVGenParticles::try_MFVtbs\n");

  assert(t1 == 5 || t1 == 1);
  assert(t2 == 3 || t2 == 5);
  mfv::MCInteractions_t type = mfv::mci_MFVtbs;
  if      (t1 == 1) type = mfv::mci_MFVtds;
  else if (t2 == 5) type = mfv::mci_MFVtbb;

  mfv::MCInteractionHolderMFVtbs h;

  GenParticlePrinter gpp(*gen_particles);
  gpp.print_mothers = gpp.print_vertex = true;
  if (debug) gpp.PrintHeader();

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

    if (type == mfv::mci_MFVtbb) {
      // JMTBAD ugh merge with MFVthree
      const int doubled_id = 5;
      const std::set<int> req_ids = { 5,5,6 };
      const size_t n = 3;
      if (lsp->numberOfDaughters() == n) {
        std::vector<const reco::Candidate*> daus = { lsp->daughter(0), lsp->daughter(1), lsp->daughter(2) };
        const std::vector<int> ids = { abs(daus[0]->pdgId()), abs(daus[1]->pdgId()), abs(daus[2]->pdgId()) };
        const std::set<int> sids(ids.begin(), ids.end());
        if (sids == req_ids)
          for (size_t i = 0; i < n; ++i)
            for (size_t j = i+1; j < n; ++j)
              if (ids[i] == doubled_id && ids[j] == doubled_id) {
                h.stranges       [which] = gen_ref(daus[i], gen_particles);
                h.primary_bottoms[which] = gen_ref(daus[j], gen_particles);
              }
      }

      h.tops           [which] = gen_ref(daughter_with_id(&*lsp, 6,  true), gen_particles);
    }
    else {
      // The last true param of daughter_with_id means take absolute value, so that e.g. strange or antistrange is OK.
      h.stranges       [which] = gen_ref(daughter_with_id(&*lsp, t1, true), gen_particles);
      h.primary_bottoms[which] = gen_ref(daughter_with_id(&*lsp, t2, true), gen_particles);
      h.tops           [which] = gen_ref(daughter_with_id(&*lsp, 6,  true), gen_particles);
    }

    if (debug) {
      char lspname[16];
      snprintf(lspname, 16, "lsp #%lu", which);
      gpp.Print(lsp, lspname);
      gpp.Print(h.stranges[which], "strangetemp");
      gpp.Print(h.primary_bottoms[which], "bottomtemp");
      gpp.Print(h.tops[which], "toptemp");
    }

    // If any are bad, let the mc object be half-formed/invalid.
    if (h.stranges       [which].isNull()) return false;
    if (h.primary_bottoms[which].isNull()) return false;
    if (h.tops           [which].isNull()) return false;

    // The -1 in final_candidate for the tops used to be 3 for
    // allowing radiated gluons or photons but with official sample
    // pythia got a top that had protons and pions and kaons oh my 42/-6 111/21 112/21 113/21 121/2212 122/2212 123/2212 124/2212 157/310 158/310
    h.stranges       [which] = gen_ref(final_candidate(h.stranges       [which], -1), gen_particles);
    h.primary_bottoms[which] = gen_ref(final_candidate(h.primary_bottoms[which], -1), gen_particles);
    h.tops           [which] = gen_ref(final_candidate(h.tops           [which], -1), gen_particles);

    if (debug) {
      gpp.Print(h.stranges[which], "strange");
      gpp.Print(h.primary_bottoms[which], "bottom");
      gpp.Print(h.tops[which], "top");
    }

    if (last_flag_check) {
      assert(lsp                     ->statusFlags().isLastCopy());
      assert(h.stranges       [which]->statusFlags().isLastCopy());
      assert(h.primary_bottoms[which]->statusFlags().isLastCopy());
      assert(h.tops           [which]->statusFlags().isLastCopy());
    }
  }

  if (h.lsps[0].isNull() || h.stranges[0].isNull() || h.primary_bottoms[0].isNull() || h.tops[0].isNull() ||
      h.lsps[1].isNull() || h.stranges[1].isNull() || h.primary_bottoms[1].isNull() || h.tops[1].isNull())
    return false;

  set_Ttbar_decay(h, gen_particles);
  
  if (h.valid()) {
    mc.set(h, type);
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

    if (last_flag_check) {
      assert(h.tops[0]->statusFlags().isLastCopy());
      assert(h.tops[1]->statusFlags().isLastCopy());
    }

    set_Ttbar_decay(h, gen_particles);
  }

  if (h.valid()) {
    mc.set(h);
    return true;
  }
  else
    return false;
}

bool MFVGenParticles::try_MFVthree(mfv::MCInteraction& mc, const edm::Handle<reco::GenParticleCollection>& gen_particles, int t1, int t2, int t3) const {
  if (debug) printf("MFVGenParticles::try_MFVthree %i %i %i\n", t1, t2, t3);

  mfv::MCInteractions_t type = mfv::mci_invalid;
  int doubled_id = 0;
  {
    static const std::vector<std::vector<int>> allowed = {
      {3,2,1},
      {11,2,-1},
      {13,2,-1},
      {15,2,-1},
      {5,2,1},
      {3,1,4},
      {5,1,4},
      {5,5,2}, // if doubled the doubled ids have to be first
    };
    static const std::vector<mfv::MCInteractions_t> allowed_types = {
      mfv::mci_MFVuds,
      mfv::mci_MFVude,
      mfv::mci_MFVudmu,
      mfv::mci_MFVudtu,
      mfv::mci_MFVudb,
      mfv::mci_MFVcds,
      mfv::mci_MFVcdb,
      mfv::mci_MFVubb,
    };
    static const std::vector<int> doubleds = { 0,0,0,0,0,0,0,5 };
    static const size_t n = allowed.size();
    assert(n == allowed_types.size());
    for (size_t i = 0; i < n; ++i) {
      if (t1 == allowed[i][0] &&
          t2 == allowed[i][1] &&
          t3 == allowed[i][2]) {
        type = allowed_types[i];
        doubled_id = doubleds[i];
        break;
      }
    }
    assert(type != mfv::mci_invalid);
  }

  mfv::MCInteractionHolderThruple h;

  GenParticlePrinter gpp(*gen_particles);
  gpp.print_mothers = gpp.print_vertex = true;
  if (debug) gpp.PrintHeader();

  // Find the LSPs (e.g. gluinos or neutralinos). Since this is
  // PYTHIA8 there are lots of copies -- try to get the ones that
  // decay to the three quarks.
  for (int i = 0, ie = int(gen_particles->size()); i < ie; ++i) {
    const reco::GenParticle& gen = gen_particles->at(i);
    if (gen.pdgId() != lsp_id || gen.numberOfDaughters() != 3)
      continue;
    reco::GenParticleRef lsp(gen_particles, i);

    size_t which = 0;
    if (h.p[0].isNull())
      h.p[0] = lsp;
    else {
      if (reco::deltaR(*h.p[0], gen) < 0.001)
	throw cms::Exception("BadAssumption", "may have found same LSP twice based on deltaR < 0.001");
      which = 1;
      h.p[1] = lsp;
    }

   // testing
    if (debug) {
      char lspname[16];
      snprintf(lspname, 16, "lsp #%lu", which);
      gpp.Print(&*lsp, lspname);
    }

    // Get the daughters. 
    if (doubled_id) {
      const std::set<int> req_ids = { abs(t1), abs(t2), abs(t3) };
      const size_t n = 3;
      if (lsp->numberOfDaughters() == n) {
        std::vector<const reco::Candidate*> daus = { lsp->daughter(0), lsp->daughter(1), lsp->daughter(2) };
        const std::vector<int> ids = { abs(daus[0]->pdgId()), abs(daus[1]->pdgId()), abs(daus[2]->pdgId()) };
        const std::set<int> sids(ids.begin(), ids.end());
        if (sids == req_ids) {
          for (size_t i = 0; i < n; ++i) {
            if (ids[i] != doubled_id) {
              h.s[which][n-1] = gen_ref(daus[i], gen_particles);
              daus.erase(daus.begin() + i);
              break;
            }
          }
          assert(daus.size() == n-1);
          for (size_t i = 0; i < n-1; ++i)
            h.s[which][i] = gen_ref(daus[i], gen_particles);
        }
      }
    }
    else {
      // The last true param of daughter_with_id means take absolute value, so that e.g. strange or antistrange is OK.
      h.s[which][0] = gen_ref(daughter_with_id(&*lsp, t1, true), gen_particles);
      h.s[which][1] = gen_ref(daughter_with_id(&*lsp, t2, true), gen_particles);
      h.s[which][2] = gen_ref(daughter_with_id(&*lsp, t3, true), gen_particles);
    }

    if (debug) {
      gpp.Print(h.s[which][0], "s0temp");
      gpp.Print(h.s[which][1], "s1temp");
      gpp.Print(h.s[which][2], "s2temp");
    }

    // If any are bad, let the mc object be half-formed/invalid.
    if (h.s[which][0].isNull()) return false;
    if (h.s[which][1].isNull()) return false;
    if (h.s[which][2].isNull()) return false;

    // The -1 in final_candidate for the tops used to be 3 for
    // allowing radiated gluons or photons but with official sample
    // pythia got a top that had protons and pions and kaons oh my 42/-6 111/21 112/21 113/21 121/2212 122/2212 123/2212 124/2212 157/310 158/310
    for (int j = 0; j < 3; ++j)
      h.s[which][j] = gen_ref(final_candidate(h.s[which][j], -1), gen_particles);

    if (debug) {
      gpp.Print(&*h.s[which][0], "s0");
      gpp.Print(&*h.s[which][1], "s1");
      gpp.Print(&*h.s[which][2], "s2");
    }

    if (last_flag_check) {
      assert(lsp->statusFlags().isLastCopy());
      for (int j = 0; j < 3; ++j)
        assert(h.s[which][j]->statusFlags().isLastCopy());
    }
  }

  if (h.valid()) {
    mc.set(h, type);
    return true;
  }
  else
    return false;
}

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

//    if (last_flag_check) {
//      assert(h.p[which]   ->statusFlags().isLastCopy());
//      assert(h.s[which][0]->statusFlags().isLastCopy());
//      assert(h.s[which][1]->statusFlags().isLastCopy());
//    }
  }

  if (h.valid()) {
    mc.set(h);
    return true;
  }
  else
    return false;
}

bool MFVGenParticles::try_MFVdijet(mfv::MCInteraction& mc, const edm::Handle<reco::GenParticleCollection>& gen_particles, int quark) const {
  if (debug) printf("MFVGenParticles::try_MFVdijet quark=%i\n", quark);
  assert(quark == 1 || quark == 4 || quark == 5);

  mfv::MCInteractionHolderPair h;

  //GenParticlePrinter gpp(*gen_particles);
  //gpp.PrintHeader();

  // Find the LLPs (e.g. gluinos, neutralinos, LL scalar). Since this is
  // PYTHIA8 there are lots of copies -- try to get the ones that
  // decay to the correct two quarks.
  int found = 0;
  for (int i = int(gen_particles->size()) - 1; i >= 0 && found < 2; --i) {
    const reco::GenParticle& gen = gen_particles->at(i);
    reco::GenParticleRef ref(gen_particles, i);
    if (abs(gen.pdgId()) != lsp_id || gen.numberOfDaughters() != 2)
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

    //char lspname[16];
    //snprintf(lspname, 16, "dijet primary #%lu", which);
    //gpp.Print(&*h.p[which], lspname);

    // Get the immediate daughters. 
    if ((h.s[which][0] = gen_ref(daughter_with_id(&gen,  quark, false), gen_particles)).isNull() ||
        (h.s[which][1] = gen_ref(daughter_with_id(&gen, -quark, false), gen_particles)).isNull()) {
      //printf("WEIRD GLUBALL CRAP??? %i %i\n", h.s[which][0].isNull(), h.s[which][1].isNull()); // or the wrong quark flavor! should handle msg better here
      return false;
    }

    h.decay_id[which] = 1;
    h.s[which][0] = gen_ref(final_candidate(h.s[which][0], 3), gen_particles);
    h.s[which][1] = gen_ref(final_candidate(h.s[which][1], 3), gen_particles);

    if (last_flag_check) {
      assert(h.p[which]   ->statusFlags().isLastCopy());
      assert(h.s[which][0]->statusFlags().isLastCopy());
      assert(h.s[which][1]->statusFlags().isLastCopy());
    }
  }

  if (h.valid()) {
    mfv::MCInteractions_t type = mfv::mci_MFVddbar;
    if      (quark == 4) type = mfv::mci_MFVccbar;
    else if (quark == 5) type = mfv::mci_MFVbbbar;
    mc.set(h, type);
    return true;
  }
  else
    return false;
}

bool MFVGenParticles::try_stopdbardbar(mfv::MCInteraction& mc, const edm::Handle<reco::GenParticleCollection>& gen_particles, int quark) const {
  if (debug) printf("MFVGenParticles::try_stopdbardbar quark=%i\n", quark);
  assert(quark == -1 || quark == -5);

  mfv::MCInteractionHolderPair h;

  GenParticlePrinter gpp(*gen_particles);
  if (debug)
    gpp.PrintHeader();

  int found = 0;
  for (int i = int(gen_particles->size()) - 1; i >= 0 && found < 2; --i) {
    const reco::GenParticle& gen = gen_particles->at(i);
    reco::GenParticleRef ref(gen_particles, i);
    if (abs(gen.pdgId()) == lsp_id && gen.numberOfDaughters() == 2) {
      const int anti = lsp_id * gen.pdgId() > 0 ? -1 : 1;
      if (gen.daughter(0)->pdgId() == anti * quark &&
          gen.daughter(1)->pdgId() == anti * quark) {

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

        if (debug) {
          char lspname[16];
          snprintf(lspname, 16, "primary #%lu", which);
          gpp.Print(&*h.p[which], lspname);
        }

        if ((h.s[which][0] = gen_ref(gen.daughter(0), gen_particles)).isNull() ||
            (h.s[which][1] = gen_ref(gen.daughter(1), gen_particles)).isNull()) {
          printf("HUH??? %i %i\n", h.s[which][0].isNull(), h.s[which][1].isNull());
          return false;
        }

        if (debug) {
          gpp.Print(h.s[which][0], "s0temp");
          gpp.Print(h.s[which][1], "s1temp");
        }

        h.decay_id[which] = 1;
        h.s[which][0] = gen_ref(final_candidate(h.s[which][0], 3), gen_particles);
        h.s[which][1] = gen_ref(final_candidate(h.s[which][1], 3), gen_particles);

        if (debug) {
          gpp.Print(h.s[which][0], "s0");
          gpp.Print(h.s[which][1], "s1");
        }

//        if (last_flag_check) {
//          assert(h.p[which]   ->statusFlags().isLastCopy());
//          assert(h.s[which][0]->statusFlags().isLastCopy());
//          assert(h.s[which][1]->statusFlags().isLastCopy());
//        }
      }
    }
  }

//  printf("h valid?? %i why? %i %i %i %i %i %i\n", h.valid(),
//         h.p[0].isNonnull(), h.p[1].isNonnull(),
//         h.s[0][0].isNonnull(), h.s[0][1].isNonnull(),
//         h.s[1][0].isNonnull(), h.s[1][1].isNonnull());

  if (h.valid()) {
    mfv::MCInteractions_t type = mfv::mci_stopdbardbar;
    if (quark == -5) type = mfv::mci_stopbbarbbar;
    mc.set(h, type);
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

    if (last_flag_check) {
      assert(h.p[which]   ->statusFlags().isLastCopy());
      assert(h.s[which][0]->statusFlags().isLastCopy());
      assert(h.s[which][1]->statusFlags().isLastCopy());
    }
  }

  if (h.valid()) {
    mc.set(h);
    return true;
  }
  else
    return false;
}

bool MFVGenParticles::try_MFV_stoplq(mfv::MCInteraction& mc, const edm::Handle<reco::GenParticleCollection>& gen_particles) const {
  if (debug) printf("MFVGenParticles::try_MFV_stoplq");

  mfv::MCInteractionHolderPair h;

  GenParticlePrinter gpp(*gen_particles);
  if (debug)
    gpp.PrintHeader();

  int found = 0;
  for (size_t i = 0; i < gen_particles->size() && found < 2; ++i) {
    const reco::GenParticle& gen = gen_particles->at(i);
    reco::GenParticleRef ref(gen_particles, i);
    if (abs(gen.pdgId()) == lsp_id && gen.numberOfDaughters() == 2) {
      if (debug) printf("found a stop");
      const int aid[2] = {abs(gen.daughter(0)->pdgId()),
			  abs(gen.daughter(1)->pdgId())};
      bool is_q[2] = {0};
      bool is_l[2] = {0};
      for (int j = 0; j < 2; ++j) {
	is_q[j] = aid[j] >= 1 && aid[j] <= 5;
	is_l[j] = aid[j] == 11 || aid[j] == 13 || aid[j] == 15; // neutrinos?
      }

      if ( (is_q[0] && is_l[1]) || (is_q[1] && is_l[0]) ) { 

	if (debug) printf("found one");
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

	if (debug) {
	  char lspname[16];
	  snprintf(lspname, 16, "primary #%lu", which);
	  gpp.Print(&*h.p[which], lspname);
	}

	if ((h.s[which][0] = gen_ref(gen.daughter(0), gen_particles)).isNull() ||
	    (h.s[which][1] = gen_ref(gen.daughter(1), gen_particles)).isNull()) {
	  printf("HUH??? %i %i\n", h.s[which][0].isNull(), h.s[which][1].isNull());
	  return false;
	}

	if (debug) {
	  gpp.Print(h.s[which][0], "s0temp");
	  gpp.Print(h.s[which][1], "s1temp");
	}

	h.decay_id[which] = 1;
	h.s[which][0] = gen_ref(final_candidate(h.s[which][0], 3), gen_particles);
	h.s[which][1] = gen_ref(final_candidate(h.s[which][1], 3), gen_particles);

	if (debug) {
	  gpp.Print(h.s[which][0], "s0");
	  gpp.Print(h.s[which][1], "s1");
	}
      }
    }
  }
  if (h.valid()) {
    mfv::MCInteractions_t type = mfv::mci_stoplq;
    mc.set(h, type);
    return true;
  }
  else
    return false;
}


bool MFVGenParticles::try_splitSUSY(mfv::MCInteraction& mc, const edm::Handle<reco::GenParticleCollection>& gen_particles) const {
  if (debug) printf("MFVGenParticles::try_splitSUSY");

  mfv::MCInteractionHolderThruple h;

  GenParticlePrinter gpp(*gen_particles);
  if (debug)
    gpp.PrintHeader();

  for (size_t i = 0; i < gen_particles->size(); ++i) {
    const reco::GenParticle& gen = gen_particles->at(i);
    reco::GenParticleRef ref(gen_particles, i);
    if (gen.pdgId() == lsp_id && gen.numberOfDaughters() == 3) {
      if (!gen.isLastCopy()) continue;
      bool found = false;

      for (size_t j = 0; j<gen.numberOfDaughters(); ++j){
        if (gen.daughter(j)->pdgId()==1000022) found = true;
      }
      if (!found) continue;

      size_t which = 0;
      if (h.p[0].isNull())
        h.p[0] = ref;
      else {
        if (reco::deltaR(*h.p[0], gen) < 0.001)
          throw cms::Exception("BadAssumption", "may have found same LSP twice based on deltaR < 0.001");
        which = 1;
        h.p[1] = ref;
      }

      if (debug) {
        char lspname[16];
        snprintf(lspname, 16, "primary #%lu", which);
        gpp.Print(&*h.p[which], lspname);
      }

      if ((h.s[which][0] = gen_ref(gen.daughter(0), gen_particles)).isNull() ||
          (h.s[which][1] = gen_ref(gen.daughter(1), gen_particles)).isNull() ||
          (h.s[which][2] = gen_ref(gen.daughter(2), gen_particles)).isNull()) {
        printf("HUH??? %i %i %i\n", h.s[which][0].isNull(), h.s[which][1].isNull(), h.s[which][2].isNull());
        return false;
      }

      if (debug) {
        gpp.Print(h.s[which][0], "s0temp");
        gpp.Print(h.s[which][1], "s1temp");
        gpp.Print(h.s[which][2], "s2temp");
      }

      h.s[which][0] = gen_ref(final_candidate(h.s[which][0], 3), gen_particles);
      h.s[which][1] = gen_ref(final_candidate(h.s[which][1], 3), gen_particles);
      h.s[which][2] = gen_ref(final_candidate(h.s[which][2], 3), gen_particles);

      if (debug) {
        gpp.Print(h.s[which][0], "s0");
        gpp.Print(h.s[which][1], "s1");
        gpp.Print(h.s[which][2], "s2");
      }

//        if (last_flag_check) {
//          assert(h.p[which]   ->statusFlags().isLastCopy());
//          assert(h.s[which][0]->statusFlags().isLastCopy());
//          assert(h.s[which][1]->statusFlags().isLastCopy());
//        }
    }
  }

//  printf("h valid?? %i why? %i %i %i %i %i %i\n", h.valid(),
//         h.p[0].isNonnull(), h.p[1].isNonnull(),
//         h.s[0][0].isNonnull(), h.s[0][1].isNonnull(),
//         h.s[1][0].isNonnull(), h.s[1][1].isNonnull());

  if (h.valid()) {
    mfv::MCInteractions_t type = mfv::mci_MFVsplitsusy;
    mc.set(h, type);
    return true;
  }
  else
    return false;
}
void MFVGenParticles::produce(edm::Event& event, const edm::EventSetup&) {
  std::unique_ptr<mfv::MCInteraction> mc(new mfv::MCInteraction);
  std::unique_ptr<std::vector<double> > primary_vertex(new std::vector<double>(3,0.));
  std::unique_ptr<std::vector<double> > decay_vertices(new std::vector<double>);
  std::unique_ptr<reco::GenParticleCollection> primaries  (new reco::GenParticleCollection);
  std::unique_ptr<reco::GenParticleCollection> secondaries(new reco::GenParticleCollection);
  std::unique_ptr<reco::GenParticleCollection> visible    (new reco::GenParticleCollection);

  if (!event.isRealData()) {
    edm::Handle<reco::GenParticleCollection> gen_particles;
    event.getByToken(gen_particles_token, gen_particles);

    const reco::GenParticle& for_vtx = gen_particles->at(2);
    const int for_vtx_id = abs(for_vtx.pdgId());
    if (for_vtx_id != 21 && !(for_vtx_id >= 1 && for_vtx_id <= 5))
      throw cms::Exception("BadAssumption", "gen_particles[2] is not a gluon or udscb: id=") << for_vtx_id;

    (*primary_vertex)[0] = for_vtx.vx();
    (*primary_vertex)[1] = for_vtx.vy();
    (*primary_vertex)[2] = for_vtx.vz();

    if (lsp_id == -1) {
      // If there is a neutralino or stop in the first event, assume that's the
      // LSP id wanted. Otherwise, default to looking for gluino. This
      // isn't relevant for some signals.
      //lsp_id = 1000021;
      lsp_id = 1000006;
      for (int i = 0, ie = int(gen_particles->size()); i < ie; ++i)
	if      (gen_particles->at(i).pdgId() == 1000022) { lsp_id = 1000022; break; }
        else if (gen_particles->at(i).pdgId() == 1000006) { lsp_id = 1000006; break; }
        else if (gen_particles->at(i).pdgId() == 9000006) { lsp_id = 9000006; break; }

      for (int i = 0, ie = int(gen_particles->size()); i < ie; ++i)
	if (debug) std::cout<< gen_particles->at(i).pdgId()<<std::endl;

    }

    if (debug) printf("MFVGenParticles::analyze: lsp_id %i\n", lsp_id);
    
    // the order of these tries is important, at least that MFVtbses come before Ttbar
    try_MFV_stoplq   (*mc, gen_particles);
    // try_splitSUSY(*mc,gen_particles) || //splitSUSY gluino  -> qqbar neu
    // try_MFVtbs  (*mc, gen_particles, 5, 3) || // tbs
    // try_MFVtbs  (*mc, gen_particles, 1, 3) || // tds
    // try_MFVtbs  (*mc, gen_particles, 5, 5) || // tbb
    // try_Ttbar   (*mc, gen_particles) || 
    // try_MFVthree(*mc, gen_particles,  3, 2,  1) ||
    // try_MFVthree(*mc, gen_particles, 11, 2, -1) ||
    // try_MFVthree(*mc, gen_particles, 13, 2, -1) ||
    // try_MFVthree(*mc, gen_particles, 15, 2, -1) ||
    // try_MFVthree(*mc, gen_particles,  5, 2,  1) || // udb
    // try_MFVthree(*mc, gen_particles,  3, 1,  4) || // cds
    // try_MFVthree(*mc, gen_particles,  5, 1,  4) || // cdb
    // try_MFVthree(*mc, gen_particles,  5, 5,  2) || // ubb
    // try_XX4j    (*mc, gen_particles) ||
    // try_stopdbardbar(*mc, gen_particles, -1) || // stop -> dbar dbar + c.c.
    // try_stopdbardbar(*mc, gen_particles, -5) || // stop -> bbar bbar + c.c.
    // try_MFVdijet(*mc, gen_particles, 1) || //ddbar
    // try_MFVdijet(*mc, gen_particles, 4) || //ccbar
    // try_MFVdijet(*mc, gen_particles, 5) || //bbbar
    // try_MFVlq   (*mc, gen_particles);

    if (mc->valid()) {
      for (auto r : mc->primaries())   primaries  ->push_back(*r);
      for (auto r : mc->secondaries()) secondaries->push_back(*r);
      for (auto r : mc->visible())     visible    ->push_back(*r);

      GenParticlePrinter gpp(*gen_particles);
      gpp.print_mothers = gpp.print_vertex = true;
      if (debug) {
        printf("print primaries, secondaries, visible last and first copies:\n");
        gpp.PrintHeader();
        for (auto r : mc->primaries())   { gpp.Print(r, "pri last"); gpp.Print(first_candidate(r), "pri first"); }
        for (auto r : mc->secondaries()) { gpp.Print(r, "sec last"); gpp.Print(first_candidate(r), "sec first"); }
        for (auto r : mc->visible())     { gpp.Print(r, "vis last"); gpp.Print(first_candidate(r), "vis first"); }
      }

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
    if (debug) printf("MFVGenParticles: trying to use beamspot for decay position\n");

    edm::Handle<reco::BeamSpot> beamspot;
    event.getByToken(beamspot_token, beamspot);

    if (beamspot.isValid()) {
      for (int i = 0; i < 2; ++i) {
        decay_vertices->push_back(beamspot->x0());
        decay_vertices->push_back(beamspot->y0());
        decay_vertices->push_back(beamspot->z0());
      }
    }
    else {
      if (debug) printf("MFVGenParticles: no beamspot in Event, falling back to 0,0,0\n");
      decay_vertices->resize(6,0.);
    }
  }

  if (debug) {
    std::cout << "MFVGenParticles " << *mc << "MFVGenParticles decay_vertices:";
    for (double d : *decay_vertices)
      printf(" %6.3f", d);
    printf("\n");
  }


  if (histos) {
    h_valid->Fill(mc->valid());
    if (mc->valid()) {
      double pos_check = 0;
      for (int i = 0; i < 2; ++i) {
        const auto& refs = mc->secondaries(i);
        for (size_t j = 0; j < refs.size(); ++j)
          for (size_t k = j+1; k < refs.size(); ++k)
            pos_check +=
              fabs(refs[j]->vx() - refs[k]->vx()) +
              fabs(refs[j]->vy() - refs[k]->vy()) +
              fabs(refs[j]->vz() - refs[k]->vz());
      }
      h_pos_check->Fill(pos_check);
    }
  }

  event.put(std::move(mc));
  event.put(std::move(primary_vertex), "genVertex");
  event.put(std::move(decay_vertices), "decays");
  event.put(std::move(primaries),   "primaries");
  event.put(std::move(secondaries), "secondaries");
  event.put(std::move(visible),     "visible");
}

DEFINE_FWK_MODULE(MFVGenParticles);
