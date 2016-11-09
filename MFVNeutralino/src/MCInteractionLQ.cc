#include "DataFormats/Math/interface/deltaR.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "JMTucker/MFVNeutralino/interface/MCInteractionLQ.h"
#include "JMTucker/Tools/interface/GenUtilities.h"
#include "JMTucker/Tools/interface/Utilities.h"

void MCInteractionLQ::Clear() {
  MCInteraction::Clear();

  lqs[0] = lqs[1] = daus[0][0] = daus[0][1] = daus[1][0] = daus[1][1] = 0;
  decay_id[0] = decay_id[1] = 0;
}

bool MCInteractionLQ::Valid() {
  return lqs[0] && lqs[1] && daus[0][0] && daus[0][1] && daus[1][0] && daus[1][1];
}

void MCInteractionLQ::Fill() {
  // Find the LQ and the LQbar. Start from the end and get the last ones,
  // they should be the ones that go to the pairs of quarks.
  for (int i = int(gen_particles->size()) - 1; i >= 0; --i) {
    const reco::GenParticle& lq = gen_particles->at(i);
    const int id = lq.pdgId();
    if (abs(id) != 42 || lq.numberOfDaughters() != 2)
      continue;

    const int aid[2] = {abs(lq.daughter(0)->pdgId()),
                        abs(lq.daughter(1)->pdgId())};
    bool is_quark [2] = {0};
    bool is_lepton[2] = {0};
    for (int j = 0; j < 2; ++j) {
      is_quark[j]  = aid[j] >= 1 && aid[j] <= 5;
      is_lepton[j] = aid[j] == 11 || aid[j] == 13 || aid[j] == 15; // neutrinos?
    }

    if (!(is_quark[0] && is_lepton[1]) && !(is_quark[1] && is_lepton[0]))
      continue;

    const int which = !(id > 0); // LQ index 0
    die_if_not(lqs[which] == 0, "found duplicate for id %i", id);
    lqs[which] = &lq;

    const int whichq = !is_quark[0];
    decay_id[which] = (aid[!whichq] - 11) / 2 + 1;
    daus[which][0] = dynamic_cast<const reco::GenParticle*>(lq.daughter( whichq));
    daus[which][1] = dynamic_cast<const reco::GenParticle*>(lq.daughter(!whichq));
  }
}

void MCInteractionLQ::SetFourVectors() {
  for (int i = 0; i < 2; ++i) {
    p4_lqs[i] = make_tlv(lqs[i]);
    for (int j = 0; j < 2; ++j)
      p4_daus[i][j] = make_tlv(daus[i][j]);
  }
  MCInteraction::SetFourVectors();
}

void MCInteractionLQ::Print(std::ostream& out) {
  if (!Valid()) {
    out << "not valid\n";
    return;
  }
  print_gen_and_daus(0, "header", *gen_particles, true, true);
  print_gen_and_daus(lqs[0], "lqs[0]", *gen_particles, true, true);
  print_gen_and_daus(daus[0][0], "daus[0][0]", *gen_particles, true, true);
  print_gen_and_daus(daus[0][1], "daus[0][1]", *gen_particles, true, true);
  print_gen_and_daus(lqs[1], "lqs[1]", *gen_particles, true, true);
  print_gen_and_daus(daus[1][0], "daus[1][0]", *gen_particles, true, true);
  print_gen_and_daus(daus[1][1], "daus[1][1]", *gen_particles, true, true);
  MCInteraction::Print(out);
}

std::vector<const reco::GenParticle*> MCInteractionLQ::ElsOrMus() {
  std::vector<const reco::GenParticle*> v;
  for (int i = 0; i < 2; ++i)
    for (int j = 0; j < 2; ++j) {
      int id = abs(daus[i][j]->pdgId());
      if (id == 11 || id == 13)
	v.push_back(daus[i][j]);
    }
  return v;
}
