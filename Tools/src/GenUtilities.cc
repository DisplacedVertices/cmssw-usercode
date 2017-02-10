#include "JMTucker/Tools/interface/GenUtilities.h"

double track_qoverp(const reco::Candidate* c) {
  return c->p() > 0 ? c->charge()/c->p() : 1e99;
}

double track_lambda(const reco::Candidate* c) {
  return M_PI_2 - c->theta();
}

double track_phi(const reco::Candidate* c) {
  return c->phi();
}

double track_dxy(const reco::Candidate* c) {
  return -c->vx()*sin(c->phi()) + c->vy()*cos(c->phi());
}

double track_dsz(const reco::Candidate* c) {
  double lambda = track_lambda(c);
  return c->vz()*cos(lambda) - (c->vx()*cos(c->phi())+c->vy()*sin(c->phi()))*sin(lambda);
}

double track_dz(const reco::Candidate* c) {
  return track_dsz(c)/cos(track_lambda(c));
}

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

bool is_chadron(int id) {
  id = abs(id);
  return id % 1000 / 400 == 1 || id % 10000 / 4000 == 1;
}

bool is_chadron(const reco::Candidate* c) {
  return is_chadron(c->pdgId());
}

bool is_bhadron(int id) {
  id = abs(id);
  return id % 1000 / 500 == 1 || id % 10000 / 5000 == 1;
}

bool is_bhadron(const reco::Candidate* c) {
  return is_bhadron(c->pdgId());
}

int original_index(const reco::Candidate* c, const reco::GenParticleCollection& gens) {
  if (c != 0)
    for (int i = 0, ie = int(gens.size()); i < ie; ++i)
      if (&gens[i] == c)
	return i;
  return -1;
}

bool is_ancestor_of(const reco::Candidate* c, const reco::Candidate* possible_ancestor) {
  if (c == 0 || possible_ancestor == 0)
    return false;
  if (c == possible_ancestor)
    return true;
  for (int i = 0, ie = c->numberOfMothers(); i < ie; ++i) {
    const reco::Candidate* mom = c->mother(i);
    if (mom == c)
      continue;
    if (mom == possible_ancestor || is_ancestor_of(mom, possible_ancestor))
      return true;
  }
  return false;
}

bool is_ancestor_of(const reco::Candidate* c, const std::vector<const reco::Candidate*>& possible_ancestors) {
  for (const reco::Candidate* possible_ancestor : possible_ancestors)
    if (is_ancestor_of(c, possible_ancestor))
      return true;
  return false;
}

bool has_any_ancestor_such_that(const reco::Candidate* c, std::function<bool(const reco::Candidate*)> such_that) {
  if (c == 0)
    return false;
  for (int i = 0, ie = c->numberOfMothers(); i < ie; ++i) {
    const reco::Candidate* mom = c->mother(i);
    if (mom == c)
      continue;
    if (such_that(mom) || has_any_ancestor_such_that(mom, such_that))
      return true;
  }
  return false;
}

bool has_any_ancestor_with_id(const reco::Candidate* c, const int id) {
  return has_any_ancestor_such_that(c, [id](const reco::Candidate* c) { return c->pdgId() == id; });
}

void flatten_descendants(const reco::Candidate* c, std::vector<const reco::Candidate*>& descendants) {
  if (c == 0)
    return;
  for (size_t i = 0, ie = c->numberOfDaughters(); i < ie; ++i) {
    const reco::Candidate* dau = c->daughter(i);
    if (dau == c)
      continue;
    descendants.push_back(dau);
    flatten_descendants(dau, descendants);
  }
}

const reco::Candidate* daughter_with_id_and_status(const reco::Candidate* c, int id, int status, bool take_abs) {
  const reco::Candidate* d = 0;
  for (size_t i = 0; i < c->numberOfDaughters(); ++i) {
    int this_id     = c->daughter(i)->pdgId();
    int this_status = c->daughter(i)->status();
    if (take_abs) {
      this_id = abs(this_id);
      this_status = abs(this_status); // meaningful for pythia8
    }
    if ((id == 0     || this_id == id) && 
	(status == 0 || this_status == status)) {
      // If we've found a second one, return 0 and let the caller
      // deal with it.
      if (d != 0)
	return 0;
      d = c->daughter(i);
    }
  }
  return d;
}

const reco::Candidate* daughter_with_id(const reco::Candidate* c, int id, bool take_abs) {
  return daughter_with_id_and_status(c, id, 0, take_abs);
}

const reco::Candidate* daughter_with_status(const reco::Candidate* c, int status, bool take_abs) {
  return daughter_with_id_and_status(c, 0, status, take_abs);
}

void daughters_with_id(const reco::Candidate* c, int id, std::vector<const reco::Candidate*>& d) {
  for (size_t i = 0; i < c->numberOfDaughters(); ++i)
    if (c->daughter(i)->pdgId() == id)
      d.push_back(c->daughter(i));
}

std::pair<const reco::Candidate*, std::vector<const reco::Candidate*> > final_candidate_with_copies(const reco::Candidate* c, int allowed_others) {
  // Handle PYTHIA8 particle record copying. allowed_others can be -1
  // for don't care if there are other daughters as long as the same
  // particle is there, 1 means allow gluons, 2 means allow photons, 3
  // for allow both photons and gluons, or 0 to be strict and allow no
  // other particles. JMTBAD magic numbers

  std::pair<const reco::Candidate*, std::vector<const reco::Candidate*> > result;
  result.first = 0;
  if (c == 0)
    return result;

  while (1) {
    result.second.push_back(c);

    if (c == 0 || c->numberOfDaughters() == 0)
      break;
    if (c->numberOfDaughters() == 1) {
      if (c->daughter(0)->pdgId() == c->pdgId())
	c = c->daughter(0);
      else
	break;
    }
    else if (allowed_others != 0) {
      int the = -1;
      bool wrong_others = false;
      for (int i = 0, ie = int(c->numberOfDaughters()); i < ie; ++i) {
	int id = c->daughter(i)->pdgId();
	if (id == c->pdgId())
	  the = i;
	else if (allowed_others != -1 && ((id != 21 && id != 22) || (id == 21 && !(allowed_others & 1)) || (id == 22 && !(allowed_others & 2)))) {
	  wrong_others = true;
	  break;
	}
      }
      if (wrong_others || the < 0)
	break;
      else
	c = c->daughter(the);
    }
    else
      break;
  }

  result.first = c;
  return result;
}

const reco::Candidate* final_candidate(const reco::Candidate* c, int allowed_others) {
  return final_candidate_with_copies(c, allowed_others).first;
}

void GenParticlePrinter::PrintHeader() {
  printf("%25s %4s %8s %4s %7s %7s %7s %7s %7s %7s", "particle", "ndx", "pdgId", "stat", "energy", "mass", "pT", "rap", "eta", "phi");
  if (print_vertex)
    printf(" %7s %7s %7s", "vx", "vy", "vz");
  if (print_mothers)
    printf(" | %20s |", "moms' ndx/id");
  if (print_daughters)
    printf(" | daus' ndx/id");
  printf("\n");
}

void GenParticlePrinter::Print(const reco::Candidate* c, const char* name) {
  if (strcmp(name, "header") == 0)
    PrintHeader();
  else if (c == 0)
    printf("%25s    pointer nil (not in event?)\n", name);
  else {
    printf("%25s %4i %8i %4i %7.2f %7.2f %7.2f %7.3f %7.3f %7.3f", name, original_index(c, gen_particles), c->pdgId(), c->status(), c->energy(), c->mass(), c->pt(), c->rapidity(), c->eta(), c->phi());
    if (print_vertex)
      printf(" %7.3f %7.3f %7.3f", c->vx(), c->vy(), c->vz());

    if (print_mothers) {
      printf(" | ");
      if (c->numberOfMothers() > 2)
	printf("%20s", "(more than 2)");
      else {
	std::string z;
	for (int i = 0, ie = int(c->numberOfMothers()); i < ie; ++i) {
	  char buf[64];
	  snprintf(buf, 64, "%i/%i", original_index(c->mother(i), gen_particles), c->mother(i)->pdgId());
	  z += buf;
	  if (i < ie - 1)
	    z += ", ";
	}
	printf("%20s", z.c_str());
      }
    }
    if (print_daughters) {
      printf(" | ");
      for (int i = 0, ie = int(c->numberOfDaughters()); i < ie; ++i) {
	printf("%i/%i", original_index(c->daughter(i), gen_particles), c->daughter(i)->pdgId());
	if (i < ie - 1)
	  printf(" ");
      }
    }
    printf("\n");
  }
}

void print_gen_and_daus(const reco::Candidate* c, const char* name, const reco::GenParticleCollection& gens, const bool print_daus, const bool print_vtx) {
  GenParticlePrinter p(gens);
  p.print_daughters = print_daus;
  p.print_vertex = print_vtx;
  p.Print(c, name);
}

int gen_jet_id(const reco::GenJet& jet) {
  int id = 0;
  for (const reco::GenParticle* g : jet.getGenConstituents()) {
    if (id == 0) {
      if (has_any_ancestor_such_that(g, [](const reco::Candidate* c) { return is_bhadron(c); }))
        id = 5;
      else if (has_any_ancestor_such_that(g, [](const reco::Candidate* c) { return is_chadron(c); }))
        id = 4;
    }
  }
  return id;
}
