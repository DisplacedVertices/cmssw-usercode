#ifndef DVCode_Tools_GenUtilities
#define DVCode_Tools_GenUtilities

#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/HepMCCandidate/interface/GenParticleFwd.h"
#include "DataFormats/JetReco/interface/GenJet.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"

double track_qoverp(const reco::Candidate* c);
double track_lambda(const reco::Candidate* c);
double track_phi(const reco::Candidate* c);
double track_dxy(const reco::Candidate* c);
double track_dsz(const reco::Candidate* c);
double track_dz(const reco::Candidate* c);

bool is_quark(const reco::Candidate* c);
bool is_quark(const reco::GenParticleRef& c);
bool is_lepton(const reco::Candidate* c);
bool is_lepton(const reco::GenParticleRef& c);
int lepton_code(const reco::Candidate* c);
int lepton_code(const reco::GenParticleRef& c);
bool is_neutrino(const reco::Candidate* c);
bool is_neutrino(const reco::GenParticleRef& c);
bool is_chadron(const int id);
bool is_chadron(const reco::Candidate* c);
bool is_bhadron(const int id);
bool is_bhadron(const reco::Candidate* c);
int original_index(const reco::Candidate* c, const reco::GenParticleCollection& gens);
reco::GenParticleRef gen_ref(const reco::Candidate* c, const edm::Handle<reco::GenParticleCollection>& gens);
bool is_ancestor_of(const reco::Candidate* c, const reco::Candidate* possible_ancestor);
bool is_ancestor_of(const reco::Candidate* c, const std::vector<const reco::Candidate*>& possible_ancestors);
bool has_any_ancestor_such_that(const reco::Candidate* c, std::function<bool(const reco::Candidate*)> such_that);
bool has_any_ancestor_with_id(const reco::Candidate* c, const int id);
void flatten_descendants(const reco::Candidate* c, std::vector<const reco::Candidate*>& descendants);
const reco::Candidate* daughter_with_id_and_status(const reco::Candidate* c, int id, int status, bool take_abs=false);
const reco::Candidate* daughter_with_id(const reco::Candidate* c, int id, bool take_abs=false);
const reco::Candidate* daughter_with_id(const reco::GenParticleRef& c, int id, bool take_abs=false);
const reco::Candidate* daughter_with_status(const reco::Candidate* c, int status, bool take_abs=false);
void daughters_with_id(const reco::Candidate* c, int id, std::vector<const reco::Candidate*>& d);
std::pair<const reco::Candidate*, std::vector<const reco::Candidate*> > terminal_candidate_with_copies(const reco::Candidate* c,     int allowed_others, int direction);
std::pair<const reco::Candidate*, std::vector<const reco::Candidate*> > terminal_candidate_with_copies(const reco::GenParticleRef c, int allowed_others, int direction);
std::pair<const reco::Candidate*, std::vector<const reco::Candidate*> > first_candidate_with_copies(const reco::Candidate* c);
std::pair<const reco::Candidate*, std::vector<const reco::Candidate*> > first_candidate_with_copies(const reco::GenParticleRef c);
std::pair<const reco::Candidate*, std::vector<const reco::Candidate*> > final_candidate_with_copies(const reco::Candidate* c,     int allowed_others);
std::pair<const reco::Candidate*, std::vector<const reco::Candidate*> > final_candidate_with_copies(const reco::GenParticleRef c, int allowed_others);
const reco::Candidate* first_candidate(const reco::Candidate* c);
const reco::Candidate* first_candidate(const reco::GenParticleRef& c);
const reco::Candidate* final_candidate(const reco::Candidate* c, int allowed_others);
const reco::Candidate* final_candidate(const reco::GenParticleRef& c, int allowed_others);
void print_gen_and_daus(const reco::Candidate* c, const char* name, const reco::GenParticleCollection& gens, const bool print_daus=true, const bool print_vtx=false);
void print_gen_and_daus(const reco::GenParticleRef c, const char* name, const reco::GenParticleCollection& gens, const bool print_daus=true, const bool print_vtx=false);
int gen_jet_id(const reco::GenJet& jet);

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
  void Print(const reco::GenParticleRef r, const char* name) { Print(r.isNull() ? 0 : &*r, name); }
};

#endif
