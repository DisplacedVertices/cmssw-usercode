#ifndef JMTucker_MFVNeutralinoFormats_MCInteractions_h
#define JMTucker_MFVNeutralinoFormats_MCInteractions_h

#include "DataFormats/HepMCCandidate/interface/GenParticleFwd.h"

namespace mfv {
  enum MCInteractions_t { mci_invalid, mci_Ttbar, mci_MFVtbs, mci_XX4j, mci_MFVdijet, mci_MFVlq };

  struct MCInteractionHolderTtbar {
    virtual bool valid() const;

    reco::GenParticleRef tops[2];  // top, topbar
    reco::GenParticleRef Ws[2]; // plus, minus
    reco::GenParticleRef bottoms[2]; // b, bbar
    reco::GenParticleRef W_daughters[2][2]; // first index is Wplus, Wminus, second is W daughters in order (d-type, u-type quark) or (charged lepton, neutrino)

    int num_leptonic; // for Ttbar, MFVtbs: 0, 1, or 2 for hadronic, semileptonic, dileptonic ttbar decay
    int decay_type[2]; // for Ttbar, MFVtbs:  Wplus and Wminus decays (the array index) into e, mu, tau, hadronic (values 0-3)
                       // for XX4j: the pdgId of the dijet
  };

  struct MCInteractionHolderMFVtbs : public MCInteractionHolderTtbar {
    bool valid() const override;

    reco::GenParticleRef lsps[2];
    reco::GenParticleRef stranges[2];
    reco::GenParticleRef primary_bottoms[2]; // bottoms are those from ttbar decay: rest of particles in MCInteractionTtbar
  };

  struct MCInteractionHolderPair {
    bool valid() const;

    reco::GenParticleRef p[2]; // primaries: LSPs, LQs, Hs, etc.
    reco::GenParticleRef s[2][2]; // secondaries: dijets, lepton + quark, etc.
    int decay_id[2];
  };

  struct MCInteractionHolderXX4j     : public MCInteractionHolderPair {};
  struct MCInteractionHolderMFVdijet : public MCInteractionHolderPair {};
  struct MCInteractionHolderMFVlq    : public MCInteractionHolderPair {};

  class MCInteraction {
  public:
    MCInteraction() : type_(mci_invalid) {}

    struct Point { double x; double y; double z; };

    typedef reco::GenParticleRef GenRef;
    typedef std::vector<GenRef> GenRefs;

    void set(const MCInteractionHolderTtbar&);
    void set(const MCInteractionHolderMFVtbs&);
    void set(const MCInteractionHolderXX4j&);
    void set(const MCInteractionHolderMFVdijet&);
    void set(const MCInteractionHolderMFVlq&);

    int type() const { return type_; }
    bool valid() const { return type_ != mci_invalid; }

    Point decay_point(size_t) const;
    double dvv() const;
    double d3d() const;

    GenRefs primaries() const { return primaries_; }
    GenRefs secondaries() const { return secondaries_; }
    GenRefs visible(int=-1) const;
    GenRefs light_leptons(int=-1) const;

    int num_leptonic() const { return num_leptonic_; }
    std::vector<int> decay_type() const { return decay_type_; }

    // MFVtbs + Ttbar
    GenRef lsp           (size_t i) const;
    GenRef strange       (size_t i) const;
    GenRef primary_bottom(size_t i) const;
    GenRef top           (size_t i) const;
    GenRef bottom        (size_t i) const;
    GenRef W             (size_t i) const;
    GenRef W_daughter    (size_t i, size_t j) const;

  private:
    void check_empty_() const;

    int type_;
    GenRefs primaries_;
    GenRefs secondaries_; // primaries_[0] -> secondaries_[indices_[0]:indices_[1]], primaries_[1] -> secondaries_[indices_[1]:indices_[2]], ...
    std::vector<size_t> indices_; // has length primaries_.size()

    int num_leptonic_;
    std::vector<int> decay_type_; // one for each of the primaries: 0,1,2 = e, mu, tau, 3 = hadronic
  };
}

std::ostream& operator<<(std::ostream& o, const mfv::MCInteraction& x);

#endif
