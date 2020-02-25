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
        auto secondaries = mci_->secondaries(i);

        for (unsigned int i_secondary = 0; i_secondary < secondaries.size(); ++i_secondary){
          const reco::GenParticleRef& s = secondaries[i_secondary];

          float x=1e9,y=1e9,z=1e9;
          if (s->numberOfDaughters()) {
            x = s->daughter(0)->vx();
            y = s->daughter(0)->vy();
            z = s->daughter(0)->vz();
          }
          nt_.add(s->pdgId(), s->pt(), s->eta(), s->phi(), s->mass(), x,y,z);

          // skip tops and W's to avoid adding duplicates (since they share descendants!)
          if(abs(s->pdgId()) != 5 && abs(s->pdgId()) != 24){

            // look at all accessible daughters of the secondary particles (stable, unstable, etc.)
            for(unsigned int i_dau = 0; i_dau < s->numberOfDaughters(); ++i_dau){
              auto dau = s->daughter(i_dau);
              nt_.add_FS(dau->pdgId(), dau->pt(), dau->eta(), dau->phi(), dau->mass(), dau->vx(), dau->vy(), dau->vz(), i, i_secondary, dau->status());
            }
          }
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

  void NtupleAdd(VerticesSubNtuple& nt, const reco::Vertex& v, const reco::Vertex& rv, const MFVVertexAux& a, bool genmatch) {
    nt.add( v.chi2(),  v.x(),  v.y(),  v.z(),  v.covariance(0,0),  v.covariance(0,1),  v.covariance(0,2),  v.covariance(1,1),  v.covariance(1,2),  v.covariance(2,2),
           rv.chi2(), rv.x(), rv.y(), rv.z(), rv.covariance(0,0), rv.covariance(0,1), rv.covariance(0,2), rv.covariance(1,1), rv.covariance(1,2), rv.covariance(2,2),
           a.ntracks(), a.njets[0], a.bs2derr, a.rescale_bs2derr, genmatch,
           a.pt[mfv::PTracksPlusJetsByNtracks], a.eta[mfv::PTracksPlusJetsByNtracks], a.phi[mfv::PTracksPlusJetsByNtracks], a.mass[mfv::PTracksPlusJetsByNtracks]);
  }
}
