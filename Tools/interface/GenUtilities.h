#ifndef JMTucker_Tools_GenUtilities
#define JMTucker_Tools_GenUtilities

#include "DataFormats/HepMCCandidate/interface/GenParticle.h"

bool is_quark(const reco::Candidate* c);
bool is_lepton(const reco::Candidate* c);
int lepton_code(const reco::Candidate* c);
bool is_neutrino(const reco::Candidate* c);
int original_index(const reco::Candidate* c, const reco::GenParticleCollection& gens);
bool is_ancestor_of(const reco::Candidate* c, const reco::Candidate* possible_ancestor);
bool has_any_ancestor_with_id(const reco::Candidate* c, const int id);
const reco::Candidate* daughter_with_id_and_status(const reco::Candidate* c, int id, int status);
const reco::Candidate* daughter_with_id(const reco::Candidate* c, int id);
const reco::Candidate* daughter_with_status(const reco::Candidate* c, int status);
void daughters_with_id(const reco::Candidate* c, int id, std::vector<const reco::Candidate*>& d);
const reco::Candidate* final_candidate(const reco::Candidate* c, int allowed_others);
void print_gen_and_daus(const reco::Candidate* c, const char* name, const reco::GenParticleCollection& gens, const bool print_daus=true, const bool print_vtx=false);

#endif
