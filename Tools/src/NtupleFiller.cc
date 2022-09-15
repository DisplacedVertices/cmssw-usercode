#include "JMTucker/Tools/interface/BTagging.h"
#include "JMTucker/Tools/interface/NtupleFiller.h"
#include "JMTucker/Tools/interface/TrackerSpaceExtent.h"
#include "JMTucker/Tools/interface/TrackTools.h"
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

    auto ps = pvs(event);

    i2nti_.assign(ps.size(), -1);
    pv_ = nullptr;
    ipv_ = -1;

    for (size_t i = 0, ie = ps.size(); i < ie; ++i) {
      const reco::Vertex& pv = ps[i];

      if (filter_ && cut(pv))
        continue;

      i2nti_[i] = nt_.n();

      if (pv_ == nullptr) {
        pv_ = &pv;
        ipv_ = int(i);
      }

      int ntracks = 0;
      int ntracksloose = 0;
      float score = 0;
      if (miniaod_) {
        score = (*scores_)[reco::VertexRef(pvs_, i)];
        for (const pat::PackedCandidate& c : *cands_)
          if (c.charge() && c.hasTrackDetails() && c.vertexRef().key() == i) {
            const int q = c.pvAssociationQuality();
            if (q == pat::PackedCandidate::UsedInFitTight)
              ++ntracks;
            if (q == pat::PackedCandidate::UsedInFitTight || q == pat::PackedCandidate::UsedInFitLoose)
              ++ntracksloose;
          }
      }
      else {
        ntracks = pv.nTracks();
        ntracksloose = pv.nTracks(0);
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

      if (ntracks > 255) ntracks = 255;
      if (ntracksloose > 255) ntracksloose = 255;

      nt_.add(x,y,z, pv.chi2(), pv.ndof(), ntracks, score,
              pv.covariance(0,0), pv.covariance(0,1), pv.covariance(0,2),
                                  pv.covariance(1,1), pv.covariance(1,2),
                                                      pv.covariance(2,2),
              ntracksloose);

      if (first_only_)
        break;
    }
  }

  void NtupleAdd(JetsSubNtuple& nt, const pat::Jet& jet) {
    int ntracks = 0;
    for (size_t idau = 0, idaue = jet.numberOfDaughters(); idau < idaue; ++idau)
      if (jetDaughterTrack(jet, idau))
        ++ntracks;

    nt.add(jet.pt(), jet.eta(), jet.phi(), jet.energy(),
           jet.jecFactor("Uncorrected"),
           ntracks,
           jmt::BTagging::discriminator(jet),
           jet.hadronFlavour(),
           0);
  }

   void NtupleAdd(MuonsSubNtuple& nt, const pat::Muon& mu) {

     reco::TrackRef mtk = mu.globalTrack();
     
     bool isLooseMuon = mu.passed(reco::Muon::CutBasedIdLoose);
     bool isMedMuon = mu.passed(reco::Muon::CutBasedIdMedium);
     bool isTightMuon = mu.passed(reco::Muon::CutBasedIdTight);

     const float iso = (mu.pfIsolationR04().sumChargedHadronPt + std::max(0., mu.pfIsolationR04().sumNeutralHadronEt + mu.pfIsolationR04().sumPhotonEt -0.5*mu.pfIsolationR04().sumPUPt))/mu.pt();
     
     if(!mtk.isNull()) {

       const reco::HitPattern& hp = mtk->hitPattern();

       TrackerSpaceExtents te;
       NumExtents ex    = te.numExtentInRAndZ(hp, TrackerSpaceExtents::AllowAll);
       NumExtents ex_px = te.numExtentInRAndZ(hp, TrackerSpaceExtents::PixelOnly);
       
       nt.add(mu.charge(), mu.pt(), mu.eta(), mu.phi(), isLooseMuon, isMedMuon, isTightMuon, iso,
	      mtk->vx(), mtk->vy(), mtk->vz(),
	      mtk->covariance(0,0), mtk->covariance(1,1), mtk->covariance(1,4), mtk->covariance(2,2), mtk->covariance(2,3),
	      mtk->covariance(3,3), mtk->covariance(3,4), mtk->covariance(4,4), mtk->normalizedChi2(),
	      hp.numberOfValidPixelHits(),
	      hp.numberOfValidStripHits(),
	      hp.pixelLayersWithMeasurement(),
	      hp.stripLayersWithMeasurement(),
	      ex.min_r < 2e9 ? ex.min_r : 0,
	      ex.min_z < 2e9 ? ex.min_z : 0,
	      ex.max_r > -2e9 ? ex.max_r : 0,
	      ex.max_z > -2e9 ? ex.max_z : 0,
	      ex_px.max_r > -2e9 ? ex_px.max_r : 0,
	      ex_px.max_z > -2e9 ? ex_px.max_z : 0
	      );
     }
  }

  void NtupleAdd(ElectronsSubNtuple& nt, const pat::Electron& el, double rho, float eA) {
  //void NtupleAdd(ElectronsSubNtuple& nt, const pat::Electron& el, double rho) {
    
    reco::GsfTrackRef etk = el.gsfTrack();

    const bool passveto = el.passConversionVeto();
    
    bool isVetoEl = el.electronID("cutBasedElectronID-Fall17-94X-V2-veto");
    bool isLooseEl = el.electronID("cutBasedElectronID-Fall17-94X-V2-loose");
    bool isMedEl = el.electronID("cutBasedElectronID-Fall17-94X-V2-medium");
    bool isTightEl = el.electronID("cutBasedElectronID-Fall17-94X-V2-tight");

    const auto pfIso = el.pfIsolationVariables();
    //const float eA = electron_effective_areas.getEffectiveArea(fabs(el.superCluster()->eta()));
    const float iso = (pfIso.sumChargedHadronPt + std::max(0., pfIso.sumNeutralHadronEt + pfIso.sumPhotonEt - rho*eA)) / el.pt();
    //const float iso = (pfIso.sumChargedHadronPt + std::max(0., pfIso.sumNeutralHadronEt + pfIso.sumPhotonEt - rho)) / el.pt();

    if (!etk.isNull()) {
      
      const reco::HitPattern& hp = etk->hitPattern();

      TrackerSpaceExtents te;
      NumExtents ex    = te.numExtentInRAndZ(hp, TrackerSpaceExtents::AllowAll);
      NumExtents ex_px = te.numExtentInRAndZ(hp, TrackerSpaceExtents::PixelOnly);

      nt.add(el.charge(), el.pt(), el.eta(), el.phi(), isVetoEl, isLooseEl, isMedEl, isTightEl, iso, passveto,
	     etk->vx(), etk->vy(), etk->vz(),
	     etk->covariance(0,0), etk->covariance(1,1), etk->covariance(1,4), etk->covariance(2,2), etk->covariance(2,3),
	     etk->covariance(3,3), etk->covariance(3,4), etk->covariance(4,4), etk->normalizedChi2(),
	     hp.numberOfValidPixelHits(),
	     hp.numberOfValidStripHits(),
	     hp.pixelLayersWithMeasurement(),
	     hp.stripLayersWithMeasurement(),
	     ex.min_r < 2e9 ? ex.min_r : 0,
	     ex.min_z < 2e9 ? ex.min_z : 0,
	     ex.max_r > -2e9 ? ex.max_r : 0,
	     ex.max_z > -2e9 ? ex.max_z : 0,
	     ex_px.max_r > -2e9 ? ex_px.max_r : 0,
	     ex_px.max_z > -2e9 ? ex_px.max_z : 0
	     );
    }
  }
  

  void JetsSubNtupleFiller::operator()(const edm::Event& e) {
    auto js = jets(e);
    i2nti_.assign(js.size(), -1);
    for (size_t i = 0, ie = js.size(); i < ie; ++i)
      if (!cut(js[i])) {
        i2nti_[i] = nt_.n();
        NtupleAdd(nt_, js[i]);
      }
  }

  void PFSubNtupleFiller::operator()(const edm::Event& event) {
    event.getByToken(token_, mets_);
    nt_.set(mets_->at(0).px(), mets_->at(0).py());
  }

  void MuonsSubNtupleFiller::operator()(const edm::Event& e) {
    auto ms = muons(e);
    i2nti_.assign(ms.size(), -1);
    for (size_t i = 0, ie = ms.size(); i < ie; ++i) {
      i2nti_[i] = nt_.n();
      NtupleAdd(nt_, ms[i]);
    }
  }

  void ElectronsSubNtupleFiller::operator()(const edm::Event& e) {
    auto es = electrons(e);
    auto r = *rho(e);
    i2nti_.assign(es.size(), -1);
    for (size_t i = 0, ie = es.size(); i < ie; ++i) {
      const float eA = electron_effective_areas.getEffectiveArea(fabs(es[i].superCluster()->eta()));
      //float eta = fabs(es[i].superCluster()->eta());
      //float eA = effArea(eta);
      i2nti_[i] = nt_.n();
      NtupleAdd(nt_, es[i], r, eA);
      // NtupleAdd(nt_, es[i], r);
    }
  }

  // void NtupleAdd(TracksSubNtuple& nt, const reco::Track& tk, int which_jet, int which_pv, int which_sv, bool ismu, bool isel, unsigned misc) {
  void NtupleAdd(TracksSubNtuple& nt, const reco::Track& tk, int which_jet, int which_pv, bool ismu, bool isel, int which_sv, unsigned misc) {
    const reco::HitPattern& hp = tk.hitPattern();

    TrackerSpaceExtents te;
    NumExtents ex    = te.numExtentInRAndZ(hp, TrackerSpaceExtents::AllowAll);
    NumExtents ex_px = te.numExtentInRAndZ(hp, TrackerSpaceExtents::PixelOnly);

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
           which_jet, which_pv, ismu, isel,
	   which_sv,
	   misc
           );
  }

  bool TracksSubNtupleFiller::cut(const reco::Track& tk, const edm::Event& e, BeamspotSubNtupleFiller* bf) const {
    if (cut_level_ < 0)
      return cut_ ? cut_(tk) : false;

    return !pass_track(tk, cut_level_, -1, &e, bf ? &bf->bs() : 0); // JMTBAD hardcoded using either plain or rescaled track
  }

  int TracksSubNtupleFiller::which_jet(const edm::Event& e, JetsSubNtupleFiller* jf, reco::TrackRef& tk) {
    int which_jet = -1;
    if (jf) {
      auto js = jf->jets(e);
      for (size_t i = 0, ie = js.size(); i < ie; ++i) {
        int nti = jf->i2nti(i);
        if (nti != -1 && trg_.has_track(e, js[i], tk))
          which_jet = nti;
      }
    }
    return which_jet;
  }
  
  int TracksSubNtupleFiller::which_pv(const edm::Event& e, PrimaryVerticesSubNtupleFiller* vf, reco::TrackRef& tk) {
    int which_pv = -1;
    if (vf) {
      auto vh = vf->hpvs(e);
      for (size_t i = 0, ie = vh->size(); i < ie; ++i) {
        int nti = vf->i2nti(i);
        if (nti != -1 && nti < 128) {
          const int q = trg_.has_track(e, reco::VertexRef(vh,i), tk);
          const int loosebit = int(q == pat::PackedCandidate::UsedInFitLoose) << 7;
          if (q == pat::PackedCandidate::UsedInFitTight || loosebit)
            which_pv = nti | loosebit;
        }
      }
    }
    return which_pv;
  }

  
  bool TracksSubNtupleFiller::ismu(const edm::Event& e, MuonsSubNtupleFiller* mf, reco::TrackRef& tk) {
    bool ismu = false;
    
    auto ms = mf->muons(e);
    // std::cout << "we have " << ms.size() << " muons in our event" << std::endl;
    std::vector<reco::TrackRef> r;
    for (size_t m = 0, me = ms.size(); m < me; ++m) {
      
      // switching from muonBestTrack to globalTrack
      //reco::TrackRef mtk = ms[m].muonBestTrack();

      reco::TrackRef mtk = ms[m].globalTrack();

      
      // if (!ms[m].muonBestTrack().isNull()) {
      if (!ms[m].globalTrack().isNull()) {

	if (mtk->pt() > 1) {
	  // std::cout << " tkmu " << mtk->pt() << "," << mtk->eta() << "," << mtk->phi() << " ";
	  // std::cout << "\n";
	  r.push_back(mtk);
	}
      }
    }
    
    for (size_t j = 0, je = r.size(); j < je; ++j) {
      double dr = reco::deltaR(tk->eta(), tk->phi(), r[j]->eta(), r[j]->phi());
      if (dr < 0.001 ) {
	ismu = true;
	//	std::cout << "delataR = " << dr << std::endl;
	//	std::cout << " tk " << tk->pt() << "," << tk->eta() << "," << tk->phi() << " ";
	//	std::cout << "\n";
      }
    }
    return ismu;
  }


  
  bool TracksSubNtupleFiller::isel(const edm::Event& e, ElectronsSubNtupleFiller* ef, reco::TrackRef& tk) {
    bool isel = false;

    auto es = ef->electrons(e);
    //std::cout << "we have " << es.size() << " electrons in our event" << std::endl;

    std::vector<reco::GsfTrackRef> r;
    for (size_t e = 0, ee = es.size(); e < ee; ++e) {
      
    //  reco::TrackRef etk = es[e].closestCtfTrackRef();
      reco::GsfTrackRef etk = es[e].gsfTrack();
      
      //if (!es[e].closestCtfTrackRef().isNull()) {
      if (!es[e].gsfTrack().isNull()) {
	if (etk->pt() > 1) {
	  //std::cout << " tkel " << etk->pt() << "," << etk->eta() << "," << etk->phi() << " ";
	  // std::cout << "\n";
	  r.push_back(etk);
	}
      }
    }
      
       
    
    for (size_t j = 0, je = r.size(); j < je; ++j) {
      double dr = reco::deltaR(tk->eta(), tk->phi(), r[j]->eta(), r[j]->phi());
      if (dr < 0.0001 ) {
	//	std::cout << "delataR = " << dr << std::endl;
	//std::cout << " tk " << tk->pt() << "," << tk->eta() << "," << tk->phi() << " ";
	//	std::cout << "\n";
	isel = true;
      }
    }
    
    return isel;
  }

  

  void TracksSubNtupleFiller::operator()(const edm::Event& e, JetsSubNtupleFiller* jf, PrimaryVerticesSubNtupleFiller* vf, BeamspotSubNtupleFiller* bf, MuonsSubNtupleFiller* mf, ElectronsSubNtupleFiller* ef) {
    auto h = htracks(e);


    // //double check (printouts from the boolean is a mess)
    //  auto ms = mf->muons(e);
    // std::cout << "we have " << ms.size() << " muons in our event" << std::endl;
    // std::vector<reco::TrackRef> r;
    // for (size_t m = 0, me = ms.size(); m < me; ++m) {
      
    //   reco::TrackRef mtk = ms[m].globalTrack();

      
    //   if (!ms[m].globalTrack().isNull()) {

    // 	if (mtk->pt() > 1) {
    // 	  std::cout << " tkmu " << mtk->pt() << "," << mtk->eta() << "," << mtk->phi() << " ";
    // 	  std::cout << "\n";
    // 	  r.push_back(mtk);
    // 	}
    //   }
    // }


    // auto es = ef->electrons(e);
    // std::cout << "we have " << es.size() << " electrons in our event" << std::endl;

    // std::vector<reco::GsfTrackRef> rr;
    // for (size_t e = 0, ee = es.size(); e < ee; ++e) {
      
    //   reco::GsfTrackRef etk = es[e].gsfTrack();
      
    //   if (!es[e].gsfTrack().isNull()) {
    // 	if (etk->pt() > 1) {
    // 	  std::cout << " tkel " << etk->pt() << "," << etk->eta() << "," << etk->phi() << " ";
    // 	  std::cout << "\n";
    // 	  rr.push_back(etk);
    // 	}
    //   }
    // }
    
  

    
    
    for (size_t i = 0, ie = h->size(); i < ie; ++i) {
      reco::TrackRef tk(h, i);
      if (!cut(*tk, e, bf)) {

	// // testing muons 
	// for (size_t j = 0, je = r.size(); j < je; ++j) {
	//   double dr = reco::deltaR(tk->eta(), tk->phi(), r[j]->eta(), r[j]->phi());
	//   if (dr < 0.001 ) {
	//     std::cout << "delataR = " << dr << std::endl;
	//     std::cout << " tk " << tk->pt() << "," << tk->eta() << "," << tk->phi() << " ";
	//     std::cout << "\n";
	//   }
	// }
	// //
	// // testing electrons 
	// for (size_t j = 0, je = rr.size(); j < je; ++j) {
	//   double dr = reco::deltaR(tk->eta(), tk->phi(), rr[j]->eta(), rr[j]->phi());
	//   if (dr < 0.001 ) {
	//     std::cout << "delataR = " << dr << std::endl;
	//     std::cout << " tk " << tk->pt() << "," << tk->eta() << "," << tk->phi() << " ";
	//     std::cout << "\n";
	//   }
	// }
	// //
	
	if (ismu(e,mf,tk) && isel(e,ef,tk)) {
	  //std::cout << "Uh oh.... found a track that matched to both an electron and muon." << std::endl;
	  //in the case that track matches to both a muon & electron, resort to matching to the muon. 
	  NtupleAdd(nt_, *tk, which_jet(e,jf,tk), which_pv(e,vf,tk), ismu(e,mf,tk), false);
	}
	else {
	  NtupleAdd(nt_, *tk, which_jet(e,jf,tk), which_pv(e,vf,tk), ismu(e,mf,tk), isel(e,ef,tk));
	  
	}
      }  
    }
    // std::cout << " ---------------------------------------- " << std::endl;
  }

  void TrackingAndJetsNtupleFiller::operator()(const edm::Event& e) {
    base_filler_(e);
    bs_filler_(e);
    pvs_filler_(e, p_.pvs_subtract_bs() ? &bs() : 0);
    jets_filler_(e);
    pf_filler_(e);
    muons_filler_(e);
    electrons_filler_(e);
    if (p_.fill_tracks())
      tracks_filler_(e, &jets_filler_, &pvs_filler_, &bs_filler_, &muons_filler_, &electrons_filler_);
  }
}
