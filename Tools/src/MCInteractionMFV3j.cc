#include "DataFormats/Math/interface/deltaR.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "JMTucker/Tools/interface/MCInteractionMFV3j.h"
#include "JMTucker/Tools/interface/GenUtilities.h"
#include "JMTucker/Tools/interface/Utilities.h"

void MCInteractionMFV3j::Clear() {
  MCInteraction::Clear();
  for (int i = 0; i < 2; ++i) {
    lsps[i] = stranges[i] = bottoms[i] = tops[i] = Ws[i] = bottoms_from_tops[i] = 0;
    stranges_init[i] = bottoms_init[i] = tops_init[i] = Ws_init[i] = bottoms_from_tops_init[i] = 0;
    for (int j = 0; j < 2; ++j)
      {
	W_daughters[i][j] = 0;
	W_daughters_init[i][j] = 0;
      }
    decay_type[i] = -1;
  }
  num_leptonic = -1;
}

bool MCInteractionMFV3j::Valid() {
  // bottoms_from_tops can be null if Vtb != 1 in gen, but everything else has to be there
  return 
    lsps[0] && stranges[0] && bottoms[0] && tops[0] && Ws[0] && W_daughters[0][0] && W_daughters[0][1] &&
    lsps[1] && stranges[1] && bottoms[1] && tops[1] && Ws[1] && W_daughters[1][0] && W_daughters[1][1] &&
    stranges_init[0] && bottoms_init[0] && tops_init[0] && Ws_init[0] && W_daughters_init[0][0] && W_daughters_init[0][1] &&
    stranges_init[1] && bottoms_init[1] && tops_init[1] && Ws_init[1] && W_daughters_init[1][0] && W_daughters_init[1][1];
}

int sgn(int x) {
  return x >= 0 ? 1 : -1;
}

void MCInteractionMFV3j::Fill() {

  // JMTBAD split class into TopsPythia8 and the rest

  const int lsp_id = 1000021;
  const int ndau = 3;
  const int dau_id_order[ndau] = { 3, 5, 6 };

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

    // Get the immediate daughters, in order by the ids specified in
    // dau_id_order.
    const reco::Candidate* daughters[ndau] = {0};
    for (int i = 0; i < ndau; ++i) {
      int id = lsp.daughter(i)->pdgId();
      for (int j = 0; j < ndau; ++j) {
	if (abs(id) == dau_id_order[j])
	  daughters[j] = lsp.daughter(i);
      }
    }

    stranges_init[which] = dynamic_cast<const reco::GenParticle*>(daughters[0]);
    bottoms_init [which] = dynamic_cast<const reco::GenParticle*>(daughters[1]);
    tops_init    [which] = dynamic_cast<const reco::GenParticle*>(daughters[2]);

    // Make sure we found all three daughters, and then get the
    // "final" daughters (PYTHIA8 likes to copy things a lot while it
    // messes with e.g. gluon radiation).
    for (int i = 0; i < ndau; ++i)
      daughters[i] = final_candidate(daughters[i], 3); // the 3 means allow gluons or photons

    // The asserts protect against dau_id_order changing above.
    assert(abs(daughters[0]->pdgId()) == 3); stranges[which] = dynamic_cast<const reco::GenParticle*>(daughters[0]);
    assert(abs(daughters[1]->pdgId()) == 5); bottoms [which] = dynamic_cast<const reco::GenParticle*>(daughters[1]);
    assert(abs(daughters[2]->pdgId()) == 6); tops    [which] = dynamic_cast<const reco::GenParticle*>(daughters[2]);

    die_if_not(tops[which]->numberOfDaughters() >= 2,
	       "at least one top doesn't have at least two daughters: tops[%i] %i", which, tops[which]->numberOfDaughters());

    // Find the Ws and bs from top decay. Bottom or bottombar might
    // not be there, since |Vtb| isn't exactly 1. The W may have a
    // lot of copies, but the copies should always have just one
    // daughter until we reach the actual W decay (qq' or lnu). The
    // bottom also can have a lot of copies, with the daughter being
    // just a new bottom, or along with some gluons.
    Ws_init[which]                = dynamic_cast<const reco::GenParticle*>(daughter_with_id(tops[which], sgn(tops[which]->pdgId()) * 24));
    Ws[which]                     = dynamic_cast<const reco::GenParticle*>(final_candidate(Ws_init[which], 2)); // 2 means allow photons only. sheesh.
    bottoms_from_tops_init[which] = dynamic_cast<const reco::GenParticle*>(daughter_with_id(tops[which], sgn(tops[which]->pdgId()) *  5));
    bottoms_from_tops[which]      = dynamic_cast<const reco::GenParticle*>(final_candidate(bottoms_from_tops_init[which], 3));

    if (bottoms_from_tops[which] == 0) {
      // JMTBAD ok letting it be strange or down... if it cares, client code now has to check, ugh
      bottoms_from_tops_init[which] = dynamic_cast<const reco::GenParticle*>(daughter_with_id(tops[which], sgn(tops[which]->pdgId()) *  3));
      bottoms_from_tops[which] = dynamic_cast<const reco::GenParticle*>(final_candidate(bottoms_from_tops_init[which], 3));
      if (bottoms_from_tops[which] == 0) {
	bottoms_from_tops_init[which] = dynamic_cast<const reco::GenParticle*>(daughter_with_id(tops[which], sgn(tops[which]->pdgId()) *  1));
	bottoms_from_tops[which] = dynamic_cast<const reco::GenParticle*>(final_candidate(bottoms_from_tops_init[which], 3));
      }
    }

    die_if_not(Ws[which],
	       "at least one W not found: Ws[%i] == %p",
	       which, Ws[which]);
    die_if_not(Ws[which]->numberOfDaughters() >= 2,
	       "one W did not have at least two daughters: Ws[%i] id %i numDau %i",
	       which, Ws[which]->pdgId(), Ws[which]->numberOfDaughters());

    // Find the W daughters, and store them in the order (down-type
    // quark, up-type quark) or (charged lepton, neutrino).
    std::vector<const reco::GenParticle*> daus;
    for (int j = 0, je = Ws[which]->numberOfDaughters(); j < je; ++j) {
      const reco::Candidate* d = Ws[which]->daughter(j);
      if (d->pdgId() != Ws[which]->pdgId()) {
	int allowed_other = is_quark(d) ? 3 : 2;
	daus.push_back(dynamic_cast<const reco::GenParticle*>(final_candidate(d, allowed_other)));
      }
    }
    die_if_not(daus.size() == 2, "a W did not have exactly two non-W daughters: which=%i", which);
    const int order = abs(daus[0]->pdgId()) % 2 == 0;
    W_daughters_init[which][0] = dynamic_cast<const reco::GenParticle*>(Ws[which]->daughter(order));
    W_daughters[which][0] = daus[ order];
    W_daughters_init[which][1] = dynamic_cast<const reco::GenParticle*>(Ws[which]->daughter(!order));
    W_daughters[which][1] = daus[!order];
  }

  if (!Valid())
    return;

  // Count and store decay types: e, mu, tau, hadronic (0-3).
  num_leptonic = 0;
  for (int i = 0; i < 2; ++i) {
    if (is_quark(W_daughters[i][0]))
      die_if_not(is_quark(W_daughters[i][1]), "one W daughter is quark but other is not");
    else {
      die_if_not(is_lepton(W_daughters[i][0]) && is_lepton(W_daughters[i][1]), "one W daughter is lepton and other is not");
      ++num_leptonic;
    }

    decay_type[i] = lepton_code(W_daughters[i][0]);
  }

  for (int j = 0; j < 2; ++j)
    for (int k = 0; k < 2; ++k)
      immediate_nus.push_back(dynamic_cast<const reco::Candidate*>(W_daughters[j][k]));
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

  MCInteraction::SetFourVectors(); // sets p4_dif_neutrinosum

  p4_neutrinosum += p4_W_neutrinosum;
  p4_missingsum += p4_W_neutrinosum;
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

    
    
