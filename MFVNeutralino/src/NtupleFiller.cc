#include "JMTucker/MFVNeutralino/interface/NtupleFiller.h"
#include "JMTucker/Tools/interface/GenUtilities.h"

namespace mfv {
  void GenTruthSubNtupleFiller::operator()(const edm::Event& event) {
    if (event.isRealData()) return;

    event.getByToken(particles_token_, particles_);
    event.getByToken(vertex_token_, vertex_);
    event.getByToken(mci_token_, mci_);
 
    if (mci_->valid()) {
      assert(mci_->primaries().size() == 2);
      for (int i = 0; i < 2; ++i) {
        auto p = mci_->primaries()[i];
        auto v = mci_->decay_point(i);
        nt_.add(p->pdgId(), p->pt(), p->eta(), p->phi(), p->mass(), v.x, v.y, v.z);
      }

      for (int i = 0; i < 2; ++i) {
        for (const reco::GenParticleRef& s : mci_->secondaries(i)) {
          float x=1e9,y=1e9,z=1e9;
          if (s->numberOfDaughters()) {
            x = s->daughter(0)->vx();
            y = s->daughter(0)->vy();
            z = s->daughter(0)->vz();
          }
          nt_.add(s->pdgId(), s->pt(), s->eta(), s->phi(), s->mass(), x,y,z);
        }
      }
    }

    bool saw_c = false;
    bool saw_b = false;

    for (const reco::GenParticle& gen : particles()) {
      if (is_bhadron(&gen))
        saw_b = true;
      if (is_chadron(&gen))
        saw_c = true;

      if (gen.pt() < 1)
        continue;

      const int id = abs(gen.pdgId());

      if (id == 5) {
        bool has_b_dau = false;
        for (size_t i = 0, ie = gen.numberOfDaughters(); i < ie; ++i) {
          if (abs(gen.daughter(i)->pdgId()) == 5) {
            has_b_dau = true;
            break;
          }
        }
        if (!has_b_dau)
          nt_.add_bquark(gen.pt(), gen.eta(), gen.phi());
      }
      else if ((id == 11 || id == 13) && (gen.status() == 1 || (gen.status() >= 21 && gen.status() <= 29)))
        nt_.add_lepton(id == 13, gen.charge(), gen.pt(), gen.eta(), gen.phi());
    }

    nt_.set(mci_->valid(),
            (*vertex_)[0], (*vertex_)[1], (*vertex_)[2],
            saw_c, saw_b);
  }

  void NtupleAdd(VerticesSubNtuple& nt, const MFVVertexAux& v, bool genmatch) {
    nt.add(v.x, v.y, v.z,
           v.cxx, v.cxy, v.cxz, v.cyy, v.cyz, v.czz,
           v.ntracks(), v.bs2derr, v.rescale_bs2derr, v.geo2ddist(), genmatch,
           v.pt[mfv::PTracksPlusJetsByNtracks], v.eta[mfv::PTracksPlusJetsByNtracks], v.phi[mfv::PTracksPlusJetsByNtracks], v.mass[mfv::PTracksPlusJetsByNtracks],
           v.mass[mfv::PTracksOnly]);
  }
}
