#include "DataFormats/Math/interface/deltaR.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "JMTucker/MFVNeutralino/interface/MCInteractionXX4j.h"
#include "JMTucker/Tools/interface/GenUtilities.h"
#include "JMTucker/Tools/interface/Utilities.h"

void MCInteractionXX4j::Clear() {
  MCInteraction::Clear();

  hs[0] = hs[1] = qs[0][0] = qs[0][1] = qs[1][0] = qs[1][1] = 0;
  decay_id[0] = decay_id[1] = 0;
}

bool MCInteractionXX4j::Valid() {
  return hs[0] && hs[1] && qs[0][0] && qs[0][1] && qs[1][0] && qs[1][1];
}

void MCInteractionXX4j::Fill() {
  // Find the H and the A. Start from the end and get the last ones,
  // they should be the ones that go to the pairs of quarks.
  for (int i = int(gen_particles->size()) - 1; i >= 0; --i) {
    const reco::GenParticle& h = gen_particles->at(i);
    const int id = h.pdgId();
    if ((id != 35 && id != 36) || h.numberOfDaughters() != 2)
      continue;
    const int aid0 = abs(h.daughter(0)->pdgId());
    const int aid1 = abs(h.daughter(1)->pdgId());
    if (aid0 != aid1 || aid0 < 1 || aid0 > 5)
      continue;
    const int which(id == 35); // put A in index 0

    die_if_not(hs[which] == 0, "found duplicate for id %i", id);

    hs[which] = &h;
    decay_id[which] = aid0;

    if (h.daughter(0)->pdgId() > 0) {
      qs[which][0] = dynamic_cast<const reco::GenParticle*>(h.daughter(0));
      qs[which][1] = dynamic_cast<const reco::GenParticle*>(h.daughter(1));
    }
    else {
      qs[which][0] = dynamic_cast<const reco::GenParticle*>(h.daughter(1));
      qs[which][1] = dynamic_cast<const reco::GenParticle*>(h.daughter(0));
    }
  }

  // If we didn't find the LSPs or one of the decay products, stop now
  // before trying to set up the convenience stuff.
  if (!Valid())
    return;
}

void MCInteractionXX4j::SetFourVectors() {
  for (int i = 0; i < 2; ++i) {
    p4_hs[i] = make_tlv(hs[i]);
    for (int j = 0; j < 2; ++j)
      p4_qs[i][j] = make_tlv(qs[i][j]);
  }
  MCInteraction::SetFourVectors();
}

void MCInteractionXX4j::Print(std::ostream& out) {
  if (!Valid()) {
    out << "not valid\n";
    return;
  }
  print_gen_and_daus(0, "header", *gen_particles, true, true);
  print_gen_and_daus(hs[0], "hs[0]", *gen_particles, true, true);
  print_gen_and_daus(qs[0][0], "qs[0][0]", *gen_particles, true, true);
  print_gen_and_daus(qs[0][1], "qs[0][1]", *gen_particles, true, true);
  print_gen_and_daus(hs[1], "hs[1]", *gen_particles, true, true);
  print_gen_and_daus(qs[1][0], "qs[1][0]", *gen_particles, true, true);
  print_gen_and_daus(qs[1][1], "qs[1][1]", *gen_particles, true, true);
  MCInteraction::Print(out);
}
