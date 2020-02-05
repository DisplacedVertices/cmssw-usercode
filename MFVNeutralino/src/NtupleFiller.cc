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

          // look at all final state daughters of the secondary particles
          for(unsigned int i_dau = 0; i_dau < s->numberOfDaughters(); ++i_dau){
            auto dau = s->daughter(i_dau);
            if(dau->status() == 1){
              // FIXME we're probably double counting daughters of tops and Ws........ Could be bad if we then blindly add them to 4-vectors! One could imagine skipping tops and W's in this loop (maybe Z's and others too for futureproofing?) 
              // FIXME do we want to keep the pdgId of the secondaries as well? Could be useful.
              // Alternatively could change the existing gen_id, etc. to only keep FS particles, and keep track of their pdgId()
              nt_.add_FS(dau->pdgId(), dau->pt(), dau->eta(), dau->phi(), dau->mass(), dau->vx(), dau->vy(), dau->vz(), mci_->primaries()[i]->pdgId());
              
              //std::cout << "parent pdgID " << s->pdgId() << ", i_dau " << i_dau << ", pdgID " << daughter->pdgId() << ", pt " << daughter->pt() << ", eta " << daughter->eta() << ", phi " << daughter->phi() << ", parent eta " << s->eta() << ", parent phi " << s->phi() << ", separated by dR = " << sqrt( (daughter->eta() - s->eta())*(daughter->eta() - s->eta()) + (daughter->phi() - s->phi())*(daughter->phi() - s->phi()) )  << std::endl;
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
