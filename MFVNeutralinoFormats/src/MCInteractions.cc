#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "JMTucker/MFVNeutralinoFormats/interface/MCInteractions.h"

namespace mfv {
  bool MCInteractionHolderTtbar::valid() const {
    return
      tops[0].isNonnull() && bottoms[0].isNonnull() && Ws[0].isNonnull() && W_daughters[0][0].isNonnull() && W_daughters[0][1].isNonnull() &&
      tops[1].isNonnull() && bottoms[1].isNonnull() && Ws[1].isNonnull() && W_daughters[1][0].isNonnull() && W_daughters[1][1].isNonnull();
  }

  bool MCInteractionHolderMFVtbs::valid() const {
    return 
      MCInteractionHolderTtbar::valid() && 
      lsps[0].isNonnull() && stranges[0].isNonnull() && primary_bottoms[0].isNonnull() &&
      lsps[1].isNonnull() && stranges[1].isNonnull() && primary_bottoms[1].isNonnull();
  }

  bool MCInteractionHolderMFVuds::valid() const {
    return
      lsps[0].isNonnull() && ups[0].isNonnull() && downs[0].isNonnull() && stranges[0].isNonnull() &&
      lsps[1].isNonnull() && ups[1].isNonnull() && downs[1].isNonnull() && stranges[1].isNonnull();
  }

  bool MCInteractionHolderPair::valid() const {
    return
      p[0].isNonnull() &&
      p[1].isNonnull() &&
      s[0][0].isNonnull() &&
      s[0][1].isNonnull() &&
      s[1][0].isNonnull() &&
      s[1][1].isNonnull();
  }

  ////

  void MCInteraction::check_empty_() const {
    assert(type_ == mci_invalid);
    assert(primaries_.empty());
    assert(secondaries_.empty());
    assert(indices_.empty());
  }

  void MCInteraction::set(const MCInteractionHolderTtbar& h) {
    check_empty_();

    type_ = mci_Ttbar;
    primaries_ = { h.tops[0], h.tops[1] };
    secondaries_ = { h.bottoms[0], h.Ws[0], h.W_daughters[0][0], h.W_daughters[0][1],
                     h.bottoms[1], h.Ws[1], h.W_daughters[1][0], h.W_daughters[1][1] };
    indices_ = { 0, 4, 8 };

    num_leptonic_ = h.num_leptonic;
    decay_type_ = { h.decay_type[0], h.decay_type[1] };
  }

  void MCInteraction::set(const MCInteractionHolderMFVtbs& h) {
    check_empty_();

    type_ = mci_MFVtbs;
    primaries_ = { h.lsps[0], h.lsps[1] };
    secondaries_ = { h.stranges[0], h.primary_bottoms[0], h.tops[0], h.bottoms[0], h.Ws[0], h.W_daughters[0][0], h.W_daughters[0][1],
                     h.stranges[1], h.primary_bottoms[1], h.tops[1], h.bottoms[1], h.Ws[1], h.W_daughters[1][0], h.W_daughters[1][1] };
    indices_ = { 0, 7, 14 };

    num_leptonic_ = h.num_leptonic;
    decay_type_ = { h.decay_type[0], h.decay_type[1] };
  }

  MCInteraction::GenRef MCInteraction::lsp           (size_t i) const { return primaries_  .at(i); }
  MCInteraction::GenRef MCInteraction::strange       (size_t i) const { return secondaries_.at(indices_[i]);   }
  MCInteraction::GenRef MCInteraction::primary_bottom(size_t i) const { return secondaries_.at(indices_[i]+1); }

  MCInteraction::GenRef MCInteraction::top(size_t i) const {
    if (type_ == mci_Ttbar)
      return primaries_.at(i);
    else
      return secondaries_.at(indices_[i]+2);
  }
    
  MCInteraction::GenRef MCInteraction::bottom    (size_t i)           const { return secondaries_.at(indices_[i] + (type_ == mci_MFVtbs) * 3); }
  MCInteraction::GenRef MCInteraction::W         (size_t i)           const { return secondaries_.at(indices_[i] + (type_ == mci_MFVtbs) * 3 + 1); }
  MCInteraction::GenRef MCInteraction::W_daughter(size_t i, size_t j) const { return secondaries_.at(indices_[i] + (type_ == mci_MFVtbs) * 3 + 2 + j); }

  void MCInteraction::set(const MCInteractionHolderMFVuds& h) {
    check_empty_();

    type_ = mci_MFVuds;
    primaries_ = { h.lsps[0], h.lsps[1] };
    secondaries_ = { h.stranges[0], h.ups[0], h.downs[0], // keep stranges first so that the strange() method isn't completely stupid
                     h.stranges[1], h.ups[1], h.downs[1]  };
    indices_ = { 0, 3, 6 };

    num_leptonic_ = -1;
    decay_type_ = { 0, 0 };
  }

  MCInteraction::GenRef MCInteraction::up  (size_t i) const { return secondaries_.at(indices_[i] + 1 ); }
  MCInteraction::GenRef MCInteraction::down(size_t i) const { return secondaries_.at(indices_[i] + 2 ); }

  void MCInteraction::set(const MCInteractionHolderPair& h, int type) {
    check_empty_();

    type_ = type;

    primaries_ = { h.p[0], h.p[1] };
    secondaries_ = { h.s[0][0], h.s[0][1],
                     h.s[1][0], h.s[1][1] };
    indices_ = { 0, 2, 4 };

    num_leptonic_ = -1;
    decay_type_ = { h.decay_id[0], h.decay_id[1] };
  }

  void MCInteraction::set(const MCInteractionHolderXX4j& h)     { set(h, mci_XX4j);     }
  void MCInteraction::set(const MCInteractionHolderMFVddbar& h) { set(h, mci_MFVddbar); }
  void MCInteraction::set(const MCInteractionHolderMFVlq& h)    { set(h, mci_MFVlq);    }

  ////

  MCInteraction::GenRefs MCInteraction::secondaries(int which) const {
    if (which == -1 || which >= int(primaries_.size()))
      return secondaries_;

    MCInteraction::GenRefs v;
    for (size_t i = indices_[which]; i < indices_[which+1]; ++i)
      v.push_back(secondaries_[i]);
    return v;
  }

  MCInteraction::GenRefs MCInteraction::visible(int which) const {
    MCInteraction::GenRefs v;
    int b, e;
    if (which == -1 || which >= int(primaries_.size())) {
      b = 0;
      e = int(secondaries_.size());
    }
    else {
      b = indices_[which];
      e = indices_[which+1];
    }

    for (int i = b; i < e; ++i) {
      GenRef x = secondaries_[i];
      const int aid = abs(x->pdgId());
      if ((1 <= aid && aid <= 5) || aid == 11 || aid == 13 || aid == 15)
        v.push_back(x);
    }
    return v;
  }

  MCInteraction::GenRefs MCInteraction::light_leptons(int which) const {
    MCInteraction::GenRefs v;
    int b, e;
    if (which == -1 || which >= int(primaries_.size())) {
      b = 0;
      e = int(secondaries_.size());
    }
    else {
      b = indices_[which];
      e = indices_[which+1];
    }
      
    for (int i = b; i < e; ++i) {
      GenRef x = secondaries_[i];
      const int aid = abs(x->pdgId());
      if (aid == 11 || aid == 13)
        v.push_back(x);
    }
    return v;
  }
  
  MCInteraction::Point MCInteraction::decay_point(size_t i) const {
    MCInteraction::Point p;
    p.x = secondaries_[indices_[i]]->vx();
    p.y = secondaries_[indices_[i]]->vy();
    p.z = secondaries_[indices_[i]]->vz();
    return p;
  }

  double MCInteraction::dvv() const {
    auto p0 = decay_point(0);
    auto p1 = decay_point(1);
    return sqrt(pow(p0.x - p1.x, 2) + 
                pow(p0.y - p1.y, 2));
  }

  double MCInteraction::d3d() const {
    auto p0 = decay_point(0);
    auto p1 = decay_point(1);
    return sqrt(pow(p0.x - p1.x, 2) + 
                pow(p0.y - p1.y, 2) +
                pow(p0.z - p1.z, 2));
  }
}

////

std::ostream& operator<<(std::ostream& o, const mfv::MCInteraction& x) {
  using std::setw;
  using std::setprecision;
  auto printit = [&o](const reco::GenParticleRef& p) {
    std::streamsize prec = o.precision();
    o << "key " << setw(5) << p.key() << " id " << setw(10) << p->pdgId() << " pt " << setw(7) << setprecision(1) << p->pt() << " eta " << setw(6) << setprecision(2) << p->eta() << " phi " << setw(6) << setprecision(2) << p->phi() << " mass " << setw(7) << setprecision(1) << p->mass();
    o.precision(prec);
    o << " mother ids: ";
    if (p->numberOfMothers() == 0) o << " none ";
    else for (size_t i = 0, ie = p->numberOfMothers(); i < ie; ++i)
           o << " " << p->mother(i)->pdgId();
    o << " daughter ids: ";
    if (p->numberOfDaughters() == 0) o << " none ";
    else for (size_t i = 0, ie = p->numberOfDaughters(); i < ie; ++i)
           o << " " << p->daughter(i)->pdgId();
    o << "\n";
  };

  o << "MCInteraction: type " << x.type() << " valid? " << x.valid() << "\n";

  if (x.valid()) {
    o << "# primaries: " << x.primaries().size() << "\n";
    for (auto p : x.primaries())   { o << "  "; printit(p); }
    o << "# secondaries: " << x.secondaries().size() << "\n";
    for (auto p : x.secondaries()) { o << "  "; printit(p); }

    if (x.type() == mfv::mci_MFVtbs || x.type() == mfv::mci_Ttbar) {
      for (int i = 0; i < 2; ++i) {
        if (x.type() == mfv::mci_MFVtbs) {
          o << "lsp #" << i << "        : ";
          printit(x.lsp(i));
          o << "      strange: ";
          printit(x.strange(i));
          o << "  pri. bottom: ";
          printit(x.primary_bottom(i));
          o << "          ";
        }
        o << "top";
        if (x.type() == mfv::mci_Ttbar)
          o << " #" << i;
        o << ": ";
        printit(x.top(i));
        o << "       bottom: ";
        printit(x.bottom(i));
        o << "            W: ";
        printit(x.W(i));
        for (int j = 0; j < 2; ++j) {
          o << "W daughter #" << j << ": ";
          printit(x.W_daughter(i, j));
        }
      } 
    }
  }

  return o;
}

#if 0

std::ostream& operator<<(std::ostream& o, const MCInteractionTtbar& x) {
  if (!x.valid())
    o << "not valid\n";
  else {
#if 0
    printf("num_leptons: %i\n", num_leptonic);
    const char* decay_types[4] = {"e", "mu", "tau", "h"};
    printf("decay type: W+ -> %s,  W- -> %s\n", decay_types[decay_plus], decay_types[decay_minus]);
    print_gen_and_daus(0,                       "header",                  *gen_particles);
    print_gen_and_daus(tops[0],                     "top",                     *gen_particles);
    print_gen_and_daus(tops[1],                  "topbar",                  *gen_particles);
    print_gen_and_daus(Ws[0],                   "Wplus",                   *gen_particles);
    print_gen_and_daus(Ws[1],                  "Wminus",                  *gen_particles);
    print_gen_and_daus(bottoms[0],                  "bottom",                  *gen_particles);
    print_gen_and_daus(bottoms[1],               "bottombar",               *gen_particles);
    print_gen_and_daus(W_daughters[0][0],       "Wplus daughter 0",        *gen_particles);
    print_gen_and_daus(W_daughters[0][1],       "Wplus daughter 1",        *gen_particles);
    print_gen_and_daus(W_daughters[1][0],       "Wminus daughter 0",       *gen_particles);
    print_gen_and_daus(W_daughters[1][1],       "Wminus daughter 1",       *gen_particles);
#endif
  }
  return o;
}

std::ostream& operator<<(std::ostream& o, const MCInteractionTtbar& x) {
  if (!x.valid())
    o << "not valid\n";
  else {
#if 0
    printf("num_leptons: %i\n", num_leptonic);
    const char* decay_types[4] = {"e", "mu", "tau", "h"};
    printf("decay type: Ws[0] -> %s,  Ws[1] -> %s\n", decay_types[decay_type[0]], decay_types[decay_type[1]]);
    print_gen_and_daus(0,                      "header",                  *gen_particles, true, true);
    print_gen_and_daus(lsps[0],                "lsps[0]",                 *gen_particles, true, true);
    print_gen_and_daus(lsps[1],                "lsps[1]",                 *gen_particles, true, true);
    print_gen_and_daus(stranges[0],            "stranges[0]",             *gen_particles, true, true);
    print_gen_and_daus(stranges[1],            "stranges[1]",             *gen_particles, true, true);
    print_gen_and_daus(bottoms[0],             "bottoms[0]",              *gen_particles, true, true);
    print_gen_and_daus(bottoms[1],             "bottoms[1]",              *gen_particles, true, true);
    print_gen_and_daus(tops[0],                "tops[0]",                 *gen_particles, true, true);
    print_gen_and_daus(tops[1],                "tops[1]",                 *gen_particles, true, true);
    print_gen_and_daus(Ws[0],                  "Ws[0]",                   *gen_particles, true, true);
    print_gen_and_daus(Ws[1],                  "Ws[1]",                   *gen_particles, true, true);
    print_gen_and_daus(bottoms_from_tops[0],   "bottoms_from_tops[0]",    *gen_particles, true, true);
    if (abs(bottoms_from_tops[0]->pdgId()) != 5)
      printf("NB: this was not a bottom quark!\n");
    print_gen_and_daus(bottoms_from_tops[1],   "bottoms_from_tops[1]",    *gen_particles, true, true);
    if (abs(bottoms_from_tops[1]->pdgId()) != 5)
      printf("NB: this was not a bottom quark!\n");
    print_gen_and_daus(W_daughters[0][0],      "Wplus daughter 0",        *gen_particles, true, true);
    print_gen_and_daus(W_daughters[0][1],      "Wplus daughter 1",        *gen_particles, true, true);
    print_gen_and_daus(W_daughters[1][0],      "Wminus daughter 0",       *gen_particles, true, true);
    print_gen_and_daus(W_daughters[1][1],      "Wminus daughter 1",       *gen_particles, true, true);
    MCInteraction::Print(out);
#endif
  }
  return o;
}

std::ostream& operator<<(std::ostream& o, const MCInteractionPair& x) {
  if (!x.valid())
    o << "not valid\n";
  else {
#if 0
    print_gen_and_daus(0, "header", *gen_particles, true, true);
    print_gen_and_daus(hs[0], "hs[0]", *gen_particles, true, true);
    print_gen_and_daus(qs[0][0], "qs[0][0]", *gen_particles, true, true);
    print_gen_and_daus(qs[0][1], "qs[0][1]", *gen_particles, true, true);
    print_gen_and_daus(hs[1], "hs[1]", *gen_particles, true, true);
    print_gen_and_daus(qs[1][0], "qs[1][0]", *gen_particles, true, true);
    print_gen_and_daus(qs[1][1], "qs[1][1]", *gen_particles, true, true);
#endif
  }
  return o;
}
#endif
