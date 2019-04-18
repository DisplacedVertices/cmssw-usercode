#ifndef JMTucker_MFVNeutralino_NtupleFiller_h
#define JMTucker_MFVNeutralino_NtupleFiller_h

#include "JMTucker/MFVNeutralinoFormats/interface/MCInteractions.h"
#include "JMTucker/MFVNeutralino/interface/Ntuple.h"
#include "JMTucker/Tools/interface/NtupleFiller.h"

namespace mfv {
  class GenTruthSubNtupleFiller {
    GenTruthSubNtuple& nt_;
    const edm::EDGetTokenT<reco::GenParticleCollection> particles_token_;
    const edm::EDGetTokenT<std::vector<double>> vertex_token_;
    const edm::EDGetTokenT<mfv::MCInteraction> mci_token_;
    edm::Handle<reco::GenParticleCollection> particles_;
    edm::Handle<std::vector<double>> vertex_;
    edm::Handle<mfv::MCInteraction> mci_;
  public:
    GenTruthSubNtupleFiller(GenTruthSubNtuple& nt, const edm::ParameterSet& cfg, edm::ConsumesCollector&& cc)
      : nt_(nt),
        particles_token_(cc.consumes<reco::GenParticleCollection>(cfg.getParameter<edm::InputTag>("gen_particles_src"))),
        vertex_token_(cc.consumes<std::vector<double>>(cfg.getParameter<edm::InputTag>("gen_vertex_src"))),
        mci_token_(cc.consumes<mfv::MCInteraction>(cfg.getParameter<edm::InputTag>("mci_src")))
    {}
    void operator()(const edm::Event&);
    const reco::GenParticleCollection& particles() const { return *particles_; }
    const std::vector<double>& vertex() const { return *vertex_; }
    const mfv::MCInteraction& mci() const { return *mci_; }
  };
}

#endif

