#include "JMTucker/Tools/interface/MCInteractionTops.h"
#include "JMTucker/Tools/interface/GenUtilities.h"
#include "JMTucker/Tools/interface/Utilities.h"

void MCInteractionTops::Clear() {
  MCInteraction::Clear();
  for (int i = 0; i < 2; ++i) {
    tops[i] = Ws[i] = bottoms[i] = 0;
    for (int j = 0; j < 2; ++j)
      W_daughters[i][j] = 0;
    gluons_from_tops[i].clear();
    decay_type[i] = -1;
  }
  num_leptonic = -1;
}

bool MCInteractionTops::Valid() {
  return tops[0] && tops[1];
}

void MCInteractionTops::Fill() {
  // Find the top and topbar.
  for (int i = 0, ie = int(gen_particles->size()); i < ie; ++i) {    
    const reco::GenParticle& gen = gen_particles->at(i);
    if (gen.pdgId() ==  6) {
      tops[0] = &gen;
    }
    else if (gen.pdgId() == -6) {
      tops[1] = &gen;
    }
  }

  if (!Valid())
    return;

    // Find the Ws and bs from top decay, and any gluons off the
    // tops. Bottom or bottombar might not be there, since |Vtb| isn't
    // exactly 1.
    die_if_not(tops[0]->numberOfDaughters() >= 2 &&
	       tops[1]->numberOfDaughters() >= 2,
	       "at least one top doesn't have at least two daughters: top %i topbar %i",
	       tops[0]->numberOfDaughters(), tops[1]->numberOfDaughters());

    const reco::Candidate* last_top0 = final_candidate(tops[0], 3); // the 3 means allow gluons or photons
    last_tops[0] = dynamic_cast<const reco::GenParticle*>(last_top0);
    const reco::Candidate* last_top1 = final_candidate(tops[1], 3); // the 3 means allow gluons or photons
    last_tops[1] = dynamic_cast<const reco::GenParticle*>(last_top1);

    Ws[0] = dynamic_cast<const reco::GenParticle*>(daughter_with_id(top,     24));
    Ws[1] = dynamic_cast<const reco::GenParticle*>(daughter_with_id(topbar, -24));
    bottoms[0] = dynamic_cast<const reco::GenParticle*>(daughter_with_id(top,     5));
    bottoms[1] = dynamic_cast<const reco::GenParticle*>(daughter_with_id(topbar, -5));
    die_if_not(Ws[0] && Ws[1], "at least one W not found: W+ %p W- %p", Ws[0], Ws[1]);

    daughters_with_id(tops[0], 21, gluons_from_tops[0]);
    daughters_with_id(tops[1], 21, gluons_from_tops[1]);
    
    // The W may have a lot of copies, but the copies should always
    // have just one daughter until we reach the actual W decay (qq'
    // or lnu). Find the last one.
    const reco::Candidate* last_W0 = final_candidate(Ws[0], 2); // 2 means allow photons only in the decay chain.
    const reco::Candidate* last_W1 = final_candidate(Ws[1], 2); // 2 means allow photons only in the decay chain.
    last_Ws[0] = dynamic_cast<const reco::GenParticle*>(last_W0);
    last_Ws[1] = dynamic_cast<const reco::GenParticle*>(last_W1);

    die_if_not(Ws[0], "W[0] from top decay not found");
    die_if_not(Ws[1], "W[1] from top decay not found");
    die_if_not(last_W0, "last_W[0] not found");
    die_if_not(last_W1, "last_W[1] not found");
    die_if_not(last_W0->numberOfDaughters() >= 2, "W[0] did not have at least two daughters: id %i numDau %i", Ws[0]->pdgId(), Ws[0]->numberOfDaughters());
    die_if_not(last_W1->numberOfDaughters() >= 2, "W[1] did not have at least two daughters: id %i numDau %i", Ws[1]->pdgId(), Ws[1]->numberOfDaughters());
    
    // Find the W daughters, and store them in the order (down-type
    // quark, up-type quark) or (charged lepton, neutrino).
    std::vector<const reco::GenParticle*> daus0;
    std::vector<const reco::GenParticle*> daus1;
    for (int j = 0, je = last_W0->numberOfDaughters(); j < je; ++j) {
      const reco::Candidate* d = last_W0->daughter(j);
      if (d->pdgId() != last_W0->pdgId()) // The W can have a copy of itself as a daughter, in addition to qqbar' or lnu.
      daus0.push_back(dynamic_cast<const reco::GenParticle*>(d));
    }
    for (int j = 0, je = last_W1->numberOfDaughters(); j < je; ++j) {
      const reco::Candidate* d = last_W1->daughter(j);
      if (d->pdgId() != last_W1->pdgId()) // The W can have a copy of itself as a daughter, in addition to qqbar' or lnu.
      daus1.push_back(dynamic_cast<const reco::GenParticle*>(d));
    }
    die_if_not(daus0.size() == 2, "W[0] did not have exactly two non-W daughters");
    die_if_not(daus1.size() == 2, "W[1] did not have exactly two non-W daughters");
    const int order0 = abs(daus0[0]->pdgId()) % 2 == 0;
    const int order1 = abs(daus1[0]->pdgId()) % 2 == 0;
    W_daughters[0][0] = daus0[ order0];
    W_daughters[0][1] = daus0[!order0];
    W_daughters[1][0] = daus1[ order1];
    W_daughters[1][1] = daus1[!order1];
    
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
}

void MCInteractionTops::SetFourVectors() {
  for (int i = 0; i < 2; ++i) {
    p4_tops[i] = make_tlv(tops[i]);
    p4_Ws  [i] = make_tlv(Ws[i]);
    p4_bottoms[i] = make_tlv(bottoms[i]);
    for (int j = 0; j < 2; ++j)
      p4_W_daughters[i][j] = make_tlv(W_daughters[i][j]);
  }

  p4_toptopbar = p4_top + p4_topbar;
    
  if (decay_plus < 3 && decay_minus < 3)
    p4_W_neutrinosum = p4_Wplus_neutrino + p4_Wminus_neutrino;
  else if (decay_plus < 3)
    p4_W_neutrinosum = p4_Wplus_neutrino;
  else if (decay_minus < 3)
    p4_W_neutrinosum = p4_Wminus_neutrino;
  else
    p4_W_neutrinosum = TLorentzVector();

  MCInteraction::SetFourVectors();
}

void MCInteractionTops::Print(std::ostream& out) {
  if (!Valid()) {
    out << "not valid\n";
    return;
  }
  printf("num_leptons: %i\n", num_leptonic);
  const char* decay_types[4] = {"e", "mu", "tau", "h"};
  printf("decay type: W+ -> %s,  W- -> %s\n", decay_types[decay_plus], decay_types[decay_minus]);
  print_gen_and_daus(0,                       "header",                  *gen_particles);
  print_gen_and_daus(top,                     "top",                     *gen_particles);
  print_gen_and_daus(topbar,                  "topbar",                  *gen_particles);
  print_gen_and_daus(Wplus,                   "Wplus",                   *gen_particles);
  print_gen_and_daus(Wminus,                  "Wminus",                  *gen_particles);
  print_gen_and_daus(bottom,                  "bottom",                  *gen_particles);
  print_gen_and_daus(bottombar,               "bottombar",               *gen_particles);
  print_gen_and_daus(W_daughters[0][0],       "Wplus daughter 0",        *gen_particles);
  print_gen_and_daus(W_daughters[0][1],       "Wplus daughter 1",        *gen_particles);
  print_gen_and_daus(W_daughters[1][0],       "Wminus daughter 0",       *gen_particles);
  print_gen_and_daus(W_daughters[1][1],       "Wminus daughter 1",       *gen_particles);
  MCInteraction::Print(out);
}

std::vector<const reco::GenParticle*> MCInteractionTops::ElsOrMus() {
  std::vector<const reco::GenParticle*> v;
  for (int i = 0; i < 2; ++i)
    for (int j = 0; j < 2; ++j) {
      int id = abs(W_daughters[i][j]->pdgId());
      if (id == 11 || id == 13)
        v.push_back(W_daughters[i][j]);
    }
  return v;
}
