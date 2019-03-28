#include "JMTucker/Tools/interface/NtupleFiller.h"
#include "JMTucker/Tools/interface/TrackerSpaceExtent.h"
#include "JMTucker/Tools/interface/Utilities.h"

namespace jmt {
  void BaseSubNtupleFiller::operator()(const edm::Event& event) {
    nt_.set_event(event.id().run(), event.luminosityBlock(), event.id().event());

    edm::Handle<double> w;
    event.getByToken(weight_token_, w);
    nt_.set_weight(*w);

    if (!event.isRealData()) {
      edm::Handle<std::vector<PileupSummaryInfo>> pileup;
      event.getByToken(pileup_token_, pileup);

      for (const auto& psi : *pileup)
        if (psi.getBunchCrossing() == 0)
          nt_.set_npu(psi.getTrueNumInteractions());
    }

    edm::Handle<double> r;
    event.getByToken(rho_token_, r);
    nt_.set_rho(*r);

    edm::Handle<reco::VertexCollection> pvs;
    event.getByToken(pvs_token_, pvs);
    nt_.set_nallpv(pvs->size());
  }

  void BeamspotSubNtupleFiller::operator()(const edm::Event& event) {
    event.getByToken(token_, bs_);

    for (int i = 0; i < 7; ++i)
      for (int j = i+1; j < 7; ++j)
        if (bs_->covariance(i,j) > 1e-8)
          throw cms::Exception("BadAssumption", "off-diagonal beamspot cov matrix not zero: cov(") << i << "," << j << ") = " << bs_->covariance(i,j);

    nt_.set(bs_->x0(), bs_->y0(), bs_->z0(),
            bs_->sigmaZ(), bs_->dxdz(), bs_->dydz(), bs_->BeamWidthX(),
            bs_->x0Error(), bs_->y0Error(), bs_->z0Error(),
            bs_->sigmaZ0Error(), bs_->dxdzError(), bs_->dydzError(), bs_->BeamWidthXError());
  }

  void PrimaryVerticesSubNtupleFiller::operator()(const edm::Event& event, const reco::BeamSpot* bs) {
    if (miniaod_) {
      event.getByToken(scores_token_, scores_);
      event.getByToken(cands_token_, cands_);
    }

    pv_ = nullptr;
    ipv_ = -1;

    int i = -1;
    for (const reco::Vertex& pv : pvs(event)) {
      ++i;

      if (filter_ && cut(pv))
        continue;

      if (pv_ == nullptr) {
        pv_ = &pv;
        ipv_ = i;
      }

      int ntracks = 0;
      float score = 0;
      if (miniaod_) {
        score = (*scores_)[reco::VertexRef(pvs_, i)];
        for (const pat::PackedCandidate& c : *cands_)
          if (int(c.vertexRef().key()) == i && c.charge() && c.hasTrackDetails())
            ++ntracks;
      }
      else {
        ntracks = pv.nTracks();
        for (auto it = pv.tracks_begin(); it != pv.tracks_end(); ++it)
          score += pow((**it).pt(), 2);
      }

      float x = pv.x();
      float y = pv.y();
      float z = pv.z();
      if (bs) {
        x -= bs->x(z);
        y -= bs->y(z);
      }
      nt_.add(x,y,z, pv.chi2(), pv.ndof(), ntracks, score,
              pv.covariance(0,0), pv.covariance(0,1), pv.covariance(0,2),
                                  pv.covariance(1,1), pv.covariance(1,2),
                                                      pv.covariance(2,2),
              0);

      if (first_only_)
        break;
    }
  }

  void NtupleAdd(TracksSubNtuple& nt, const reco::Track& tk) {
    TrackerSpaceExtents te;
    NumExtents ex    = te.numExtentInRAndZ(tk.hitPattern(), TrackerSpaceExtents::AllowAll);
    NumExtents ex_px = te.numExtentInRAndZ(tk.hitPattern(), TrackerSpaceExtents::PixelOnly);

    const reco::HitPattern& hp = tk.hitPattern();

    nt.add(tk.charge(), tk.pt(), tk.eta(), tk.phi(),
           tk.vx(), tk.vy(), tk.vz(),
           tk.covariance(0,0), tk.covariance(1,1), tk.covariance(1,4), tk.covariance(2,2), tk.covariance(2,3), tk.covariance(3,3), tk.covariance(3,4), tk.covariance(4,4),
           tk.normalizedChi2(),
           hp.numberOfValidPixelHits(),
           hp.numberOfValidStripHits(),
           hp.pixelLayersWithMeasurement(),
           hp.stripLayersWithMeasurement(),
           ex.min_r < 2e9 ? ex.min_r : 0,
           ex.min_z < 2e9 ? ex.min_z : 0,
           ex.max_r > -2e9 ? ex.max_r : 0,
           ex.max_z > -2e9 ? ex.max_z : 0,
           ex_px.max_r > -2e9 ? ex_px.max_r : 0,
           ex_px.max_z > -2e9 ? ex_px.max_z : 0,
           -1,-1,-1,0
           //which_jet, which_pv, which_sv, misc
           );
  }

  void NtupleAdd(JetsSubNtuple& nt, const pat::Jet& jet) {
    int ntracks = 0;
    for (size_t idau = 0, idaue = jet.numberOfDaughters(); idau < idaue; ++idau)
      if (jetDaughterTrack(jet, idau))
        ++ntracks;

    nt.add(jet.pt(), jet.eta(), jet.phi(), jet.energy(),
           jet.jecFactor("Uncorrected"),
           ntracks,
           jet.bDiscriminator("pfCombinedInclusiveSecondaryVertexV2BJetTags"),
           jet.hadronFlavour(),
           0);
  }
}
