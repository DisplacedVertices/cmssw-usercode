#include "JMTucker/Tools/interface/GenUtilities.h"

bool is_quark(const reco::Candidate* c) {
  int apid = abs(c->pdgId());
  return apid >= 1 && apid <= 6;
}

bool is_lepton(const reco::Candidate* c) {
  int apid = abs(c->pdgId());
  return apid >= 11 && apid <= 18;
}

int lepton_code(const reco::Candidate* c) {
  // 0 for e/nu_e (bar), 1 for mu/nu_mu (bar), 2 for tau/nu_tau (bar), 3 for anything else (e.g. quarks)
  switch (abs(c->pdgId())) {
  case 11: case 12: return 0;
  case 13: case 14: return 1;
  case 15: case 16: return 2;
  }
  return 3;
}

bool is_neutrino(const reco::Candidate* c) {
  int apid = abs(c->pdgId());
  return apid == 12 || apid == 14 || apid == 16;
}

int original_index(const reco::Candidate* c, const reco::GenParticleCollection& gens) {
  for (int i = 0; i < int(gens.size()); ++i)
    if (&gens[i] == c)
      return i;
  return -1;
}

const reco::Candidate* daughter_with_id_and_status(const reco::Candidate* c, int id, int status) {
  const reco::Candidate* d = 0;
  for (size_t i = 0; i < c->numberOfDaughters(); ++i) {
    if ((id == 0     || c->daughter(i)->pdgId()  == id) && 
	(status == 0 || c->daughter(i)->status() == status)) {
      // If we've found a second one, return 0 and let the caller
      // deal with it.
      if (d != 0)
	return 0;
      d = c->daughter(i);
    }
  }
  return d;
}

const reco::Candidate* daughter_with_id(const reco::Candidate* c, int id) {
  return daughter_with_id_and_status(c, id, 0);
}

const reco::Candidate* daughter_with_status(const reco::Candidate* c, int status) {
  return daughter_with_id_and_status(c, 0, status);
}

void daughters_with_id(const reco::Candidate* c, int id, std::vector<const reco::Candidate*>& d) {
  for (size_t i = 0; i < c->numberOfDaughters(); ++i)
    if (c->daughter(i)->pdgId() == id)
      d.push_back(c->daughter(i));
}

const reco::Candidate* final_candidate(const reco::Candidate* c) {
  // Handle PYTHIA8 particle record copying.
  while (c != 0 && c->numberOfDaughters() == 1 && c->daughter(0)->pdgId() == c->pdgId())
    c = c->daughter(0);
  return c;
}

void print_gen_and_daus(const reco::Candidate* c, const char* name, const reco::GenParticleCollection& gens, const bool print_daus) {
  if (strcmp(name, "header") == 0) 
    printf("%25s %4s %8s %7s %7s %7s %7s %7s %7s   daughters' index/id\n", "particle", "ndx", "pdgId", "energy", "mass", "pT", "rap", "eta", "phi");
  else if (c == 0)
    printf("%25s    not in event\n", name);
  else {
    printf("%25s %4i %8i %7.2f %7.2f %7.2f %7.3f %7.3f %7.3f  ", name, original_index(c, gens), c->pdgId(), c->energy(), c->mass(), c->pt(), c->rapidity(), c->eta(), c->phi());
    if (print_daus)
      for (int i = 0; i < int(c->numberOfDaughters()); ++i)
	printf(" %i/%i,", original_index(c->daughter(i), gens), c->daughter(i)->pdgId());
    printf("\n");
  }
}
