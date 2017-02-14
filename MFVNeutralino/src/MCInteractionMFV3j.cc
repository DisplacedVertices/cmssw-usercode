#include "DataFormats/Math/interface/deltaR.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "JMTucker/MFVNeutralino/interface/MCInteractionMFV3j.h"
#include "JMTucker/Tools/interface/GenUtilities.h"
#include "JMTucker/Tools/interface/Utilities.h"

void MCInteractionMFV3j::Clear() {
  MCInteraction::Clear();
  for (int i = 0; i < 2; ++i) {
    lsps[i] = stranges[i] = bottoms[i] = tops[i] = Ws[i] = bottoms_from_tops[i] = 0;
    for (int j = 0; j < 2; ++j)
      W_daughters[i][j] = 0;
    decay_type[i] = -1;
  }
  num_leptonic = -1;
  which_is_lepton = -1;
}

bool MCInteractionMFV3j::Valid() {
  return 
    lsps[0] && stranges[0] && bottoms[0] && tops[0] && bottoms_from_tops[0] && Ws[0] && W_daughters[0][0] && W_daughters[0][1] &&
    lsps[1] && stranges[1] && bottoms[1] && tops[1] && bottoms_from_tops[1] && Ws[1] && W_daughters[1][0] && W_daughters[1][1];
}

namespace {
  int sgn(int x) {
    return x >= 0 ? 1 : -1;
  }
}

void MCInteractionMFV3j::Fill() {
  // JMTBAD split class into TopsPythia8 and the rest

  static int lsp_id = -1;
  if (lsp_id == -1) {
    // If there is a neutralino in the first event (lsp_id is
    // static, so what we set here will stay for future events),
    // assume that's the LSP id wanted. Otherwise, default to looking
    // for gluino.
    lsp_id = 1000021;
    for (int i = 0, ie = int(gen_particles->size()); i < ie; ++i)
      if (gen_particles->at(i).pdgId() == 1000022) {
        lsp_id = 1000022;
        break;
      }
  }
  
  // Find the LSPs (e.g. gluinos or neutralinos). Since this is
  // PYTHIA8 there are lots of copies -- try to get the ones that
  // decay to the three quarks.
  for (int i = 0, ie = int(gen_particles->size()); i < ie; ++i) {
    const reco::GenParticle& gen = gen_particles->at(i);
    if (gen.pdgId() != lsp_id || gen.numberOfDaughters() != 3)
      continue;

    const reco::GenParticle& lsp = gen;

    size_t which = 0;
    if (lsps[0] == 0)
      lsps[0] = &lsp;
    else {
      if (reco::deltaR(*lsps[0], gen) < 0.001)
	edm::LogWarning("MCInteractionMFV3j") << "warning: may have found same LSP twice based on deltaR < 0.001";
      which = 1;
      lsps[1] = &lsp;
    }

    // Get the immediate daughters. 
    stranges[which] = dynamic_cast<const reco::GenParticle*>(daughter_with_id(&lsp, 3, true)); // true means take absolute value, so that e.g. strange or antistrange is OK.
    bottoms [which] = dynamic_cast<const reco::GenParticle*>(daughter_with_id(&lsp, 5, true));
    tops    [which] = dynamic_cast<const reco::GenParticle*>(daughter_with_id(&lsp, 6, true));

    // Make sure we found all three daughters, and then get the
    // "final" top (PYTHIA8 likes to copy things a lot while it messes
    // with e.g. gluon radiation) to get its decay products.
    die_if_not(stranges[which] && bottoms[which] && tops[which],
	       "LSP[%i] did not have strange+bottom+top daughters:  strange: %p bottom: %p top: %p", which, stranges[which], bottoms[which], tops[which]);

    const reco::Candidate* last_top = final_candidate(tops[which], -1); // used to be 3 for allowing radiated gluons or photons but with official sample pythia got a top that had protons and pions 42/-6 111/21 112/21 113/21 121/2212 122/2212 123/2212 124/2212 157/310 158/310
    last_tops[which] = dynamic_cast<const reco::GenParticle*>(last_top);

    die_if_not(last_top, "can't find final candidate for top[%i]", which);
    die_if_not(last_top->numberOfDaughters() >= 2, "top[%i] doesn't have at least two daughters: %i", which, last_top->numberOfDaughters());

    // Find the Ws and bs from top decay.
    Ws[which]                = dynamic_cast<const reco::GenParticle*>(daughter_with_id(last_top, sgn(last_top->pdgId()) * 24));
    bottoms_from_tops[which] = dynamic_cast<const reco::GenParticle*>(daughter_with_id(last_top, sgn(last_top->pdgId()) *  5));

    // Bottom or bottombar might not be there, since |Vtb| isn't
    // exactly 1. If the top decayed into some other down-type quark,
    // grab it, trying strange and down in turn.. Client code has to
    // check if "bottoms_from_tops[which]" was actually a bottom, if
    // needed. (See is_bottom_from_top(which) below.)
    if (bottoms_from_tops[which] == 0) {
      bottoms_from_tops[which]   = dynamic_cast<const reco::GenParticle*>(daughter_with_id(last_top, sgn(last_top->pdgId()) * 3));
      if (bottoms_from_tops[which] == 0) {
	bottoms_from_tops[which] = dynamic_cast<const reco::GenParticle*>(daughter_with_id(last_top, sgn(last_top->pdgId()) * 1));
	die_if_not(bottoms_from_tops[which] != 0, "could not find down-type quark from top[%i]", which);
      }
    }

    // The W may have a lot of copies, but the copies should always
    // have just one daughter until we reach the actual W decay (qq'
    // or lnu). Find the last one.
    const reco::Candidate* last_W = final_candidate(Ws[which], 2); // 2 means allow photons only in the decay chain.
    last_Ws[which] = dynamic_cast<const reco::GenParticle*>(last_W);

    die_if_not(Ws[which], "W[%i] from top decay not found", which);
    die_if_not(last_W, "last_W[%i] not found", which);
    die_if_not(last_W->numberOfDaughters() >= 2, "W[%i] did not have at least two daughters: id %i numDau %i", which, Ws[which]->pdgId(), Ws[which]->numberOfDaughters());

    // Find the W daughters, and store them in the order (down-type
    // quark, up-type quark) or (charged lepton, neutrino).
    std::vector<const reco::GenParticle*> daus;
    for (int j = 0, je = last_W->numberOfDaughters(); j < je; ++j) {
      const reco::Candidate* d = last_W->daughter(j);
      if (d->pdgId() != last_W->pdgId()) // The W can have a copy of itself as a daughter, in addition to qqbar' or lnu.
	daus.push_back(dynamic_cast<const reco::GenParticle*>(d));
    }
    die_if_not(daus.size() == 2, "W[%i] did not have exactly two non-W daughters", which);
    const int order = abs(daus[0]->pdgId()) % 2 == 0;
    W_daughters[which][0] = daus[ order];
    W_daughters[which][1] = daus[!order];
  }

  // If we didn't find the LSPs or one of the decay products, stop now
  // before trying to set up the convenience stuff.
  if (!Valid())
    return;

  // Count and store decay types: e, mu, tau, hadronic (0-3).
  num_leptonic = 0;
  for (int i = 0; i < 2; ++i) {
    if (is_quark(W_daughters[i][0]))
      die_if_not(is_quark(W_daughters[i][1]), "one W daughter is quark but other is not");
    else {
      die_if_not(is_lepton(W_daughters[i][0]) && is_lepton(W_daughters[i][1]), "one W daughter is lepton and other is not");
      which_is_lepton = i;
      ++num_leptonic;
    }

    decay_type[i] = lepton_code(W_daughters[i][0]);
  }
}

void MCInteractionMFV3j::SetFourVectors() {
  for (int i = 0; i < 2; ++i) {
    p4_lsps[i] = make_tlv(lsps[i]);
    p4_stranges[i] = make_tlv(stranges[i]);
    p4_bottoms[i] = make_tlv(bottoms[i]);
    p4_tops[i] = make_tlv(tops[i]);
    p4_Ws  [i] = make_tlv(Ws[i]);
    p4_bottoms_from_tops[i] = make_tlv(bottoms_from_tops[i]);
    for (int j = 0; j < 2; ++j)
      p4_W_daughters[i][j] = make_tlv(W_daughters[i][j]);
  }

  p4_W_neutrinosum.SetXYZT(0,0,0,0);
  for (int j = 0; j < 2; ++j)
    if (decay_type[j] < 3)
      p4_W_neutrinosum += p4_W_daughters[j][1];

  MCInteraction::SetFourVectors();
}

void MCInteractionMFV3j::Print(std::ostream& out) {
  if (!Valid()) {
    out << "not valid\n";
    return;
  }
  printf("num_leptons: %i\n", num_leptonic);
  const char* decay_types[4] = {"e", "mu", "tau", "h"};
  printf("decay type: Ws[0] -> %s,  Ws[1] -> %s\n", decay_types[decay_type[0]], decay_types[decay_type[1]]);
  print_gen_and_daus(0,                      "header",                  *gen_particles, true, true);
  print_gen_and_daus(lsps[0],                "lsps[0]",                 *gen_particles, true, true);
  print_gen_and_daus(lsps[1],                "lsps[1]",                 *gen_particles, true, true);
  print_gen_and_daus(stranges[0],            "stranges[0]",             *gen_particles, true, true);
  print_gen_and_daus(stranges[1],            "stranges[1]",             *gen_particles, true, true);
  print_gen_and_daus(bottoms[0],             "bottoms[0]",              *gen_particles, true, true);
  print_gen_and_daus(bottoms[1],             "bottoms[1]",              *gen_particles, true, true);
  print_gen_and_daus(tops[0],                "tops[0]",                 *gen_particles, true, true);
  print_gen_and_daus(tops[1],                "tops[1]",                 *gen_particles, true, true);
  print_gen_and_daus(Ws[0],                  "Ws[0]",                   *gen_particles, true, true);
  print_gen_and_daus(Ws[1],                  "Ws[1]",                   *gen_particles, true, true);
  print_gen_and_daus(bottoms_from_tops[0],   "bottoms_from_tops[0]",    *gen_particles, true, true);
  if (abs(bottoms_from_tops[0]->pdgId()) != 5)
    printf("NB: this was not a bottom quark!\n");
  print_gen_and_daus(bottoms_from_tops[1],   "bottoms_from_tops[1]",    *gen_particles, true, true);
  if (abs(bottoms_from_tops[1]->pdgId()) != 5)
    printf("NB: this was not a bottom quark!\n");
  print_gen_and_daus(W_daughters[0][0],      "Wplus daughter 0",        *gen_particles, true, true);
  print_gen_and_daus(W_daughters[0][1],      "Wplus daughter 1",        *gen_particles, true, true);
  print_gen_and_daus(W_daughters[1][0],      "Wminus daughter 0",       *gen_particles, true, true);
  print_gen_and_daus(W_daughters[1][1],      "Wminus daughter 1",       *gen_particles, true, true);
  MCInteraction::Print(out);
}

bool MCInteractionMFV3j::is_bottom_from_top(int which) {
  // Since the top could have decayed into Ws, check if the quark from
  // top is really a bottom.
  return abs(bottoms_from_tops[which]->pdgId()) == 5;
}

const reco::Candidate* MCInteractionMFV3j::Ancestor(const reco::Candidate* c, const std::string& type) {
  if (type == "lsp") {
    if (is_ancestor_of(c, lsps[0]))
      return lsps[0];
    else if (is_ancestor_of(c, lsps[1]))
      return lsps[1];
  }
  else if (type == "top") {
    if (is_ancestor_of(c, tops[0]))
      return tops[0];
    else if (is_ancestor_of(c, tops[1]))
      return tops[1];
  }
  else if (type == "strange") {
    if (is_ancestor_of(c, stranges[0]))
      return stranges[0];
    else if (is_ancestor_of(c, stranges[1]))
      return stranges[1];
  }
  else if (type == "bottom") {
    if (is_ancestor_of(c, bottoms[0]))
      return bottoms[0];
    else if (is_ancestor_of(c, bottoms[1]))
      return bottoms[1];
  }
  else if (type == "bottom_from_top") {
    if (is_ancestor_of(c, bottoms_from_tops[0]))
      return bottoms_from_tops[0];
    else if (is_ancestor_of(c, bottoms_from_tops[1]))
      return bottoms_from_tops[1];
  }
  else if (type == "quark") {
    const reco::Candidate* result = Ancestor(c, "top");
    if (result == 0) {
      result = Ancestor(c, "bottom");
      if (result == 0)
	result = Ancestor(c, "strange");
    }
    return result;
  }
  else
    throw cms::Exception("MCInteractionMFV3j") << "Ancestor: type " << type << " not recognized";

  return 0;
}

std::vector<const reco::GenParticle*> MCInteractionMFV3j::ElsOrMus() {
  std::vector<const reco::GenParticle*> v;
  for (int i = 0; i < 2; ++i)
    for (int j = 0; j < 2; ++j) {
      int id = abs(W_daughters[i][j]->pdgId());
      if (id == 11 || id == 13)
        v.push_back(W_daughters[i][j]);
    }
  return v;
}
