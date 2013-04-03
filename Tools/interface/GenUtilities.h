#ifndef JMTucker_Tools_GenUtilities
#define JMTucker_Tools_GenUtilities

#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/JetReco/interface/GenJet.h"

bool is_quark(const reco::Candidate* c);
bool is_lepton(const reco::Candidate* c);
int lepton_code(const reco::Candidate* c);
bool is_neutrino(const reco::Candidate* c);
int original_index(const reco::Candidate* c, const reco::GenParticleCollection& gens);
bool is_ancestor_of(const reco::Candidate* c, const reco::Candidate* possible_ancestor);
bool is_ancestor_of(const reco::Candidate* c, const std::vector<const reco::Candidate*>& possible_ancestors);
bool has_any_ancestor_with_id(const reco::Candidate* c, const int id);
const reco::Candidate* daughter_with_id_and_status(const reco::Candidate* c, int id, int status, bool take_abs=false);
const reco::Candidate* daughter_with_id(const reco::Candidate* c, int id, bool take_abs=false);
const reco::Candidate* daughter_with_status(const reco::Candidate* c, int status, bool take_abs=false);
void daughters_with_id(const reco::Candidate* c, int id, std::vector<const reco::Candidate*>& d);
std::pair<const reco::Candidate*, std::vector<const reco::Candidate*> > final_candidate_with_copies(const reco::Candidate* c, int allowed_others);
const reco::Candidate* final_candidate(const reco::Candidate* c, int allowed_others);
void print_gen_and_daus(const reco::Candidate* c, const char* name, const reco::GenParticleCollection& gens, const bool print_daus=true, const bool print_vtx=false);

template <typename T>
std::vector<const reco::GenParticle*> constituents_from_ancestors(const reco::GenJet& gen_jet, const T& ancestors) {
  std::vector<const reco::GenParticle*> result;
  for (const reco::GenParticle* g : gen_jet.getGenConstituents())
    if (is_ancestor_of(g, ancestors))
      result.push_back(g);
  return result;
}

struct GenParticlePrinter {
  const reco::GenParticleCollection& gen_particles;
  bool print_mothers;
  bool print_daughters;
  bool print_vertex;

  GenParticlePrinter(const reco::GenParticleCollection& gens)
    : gen_particles(gens),
      print_mothers(false),
      print_daughters(true),
      print_vertex(false)
  {}

  void PrintHeader();
  void Print(const reco::Candidate* c, const char* name);
};

#endif
