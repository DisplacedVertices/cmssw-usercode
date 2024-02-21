#include "DataFormats/Common/interface/TriggerResults.h"
#include "DataFormats/JetReco/interface/PFJetCollection.h"
#include "DataFormats/BeamSpot/interface/BeamSpot.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "RecoEgamma/EgammaTools/interface/EffectiveAreas.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "FWCore/Common/interface/TriggerNames.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "RecoVertex/KalmanVertexFit/interface/KalmanVertexFitter.h"
#include "RecoVertex/VertexTools/interface/VertexDistance3D.h"
#include "RecoVertex/VertexTools/interface/VertexDistanceXY.h"
#include "TrackingTools/Records/interface/TransientTrackRecord.h"
#include "TrackingTools/TransientTrack/interface/TransientTrack.h"
#include "TrackingTools/TransientTrack/interface/TransientTrackBuilder.h"
#include "JMTucker/MFVNeutralinoFormats/interface/VertexAux.h"
#include "JMTucker/MFVNeutralino/interface/VertexAuxSorter.h"
#include "JMTucker/MFVNeutralino/interface/VertexerParams.h"
#include "JMTucker/Tools/interface/AnalysisEras.h"
#include "JMTucker/Tools/interface/ExtValue.h"
#include "JMTucker/Tools/interface/Math.h"
#include "JMTucker/Tools/interface/TrackRefGetter.h"
#include "JMTucker/Tools/interface/TrackRescaler.h"
#include "JMTucker/Tools/interface/StatCalculator.h"
#include "JMTucker/Tools/interface/Utilities.h"

class MFVVertexAuxProducer : public edm::EDProducer {
 public:
  explicit MFVVertexAuxProducer(const edm::ParameterSet&);
  void produce(edm::Event&, const edm::EventSetup&);

 private:
  jmt::TrackRescaler track_rescaler;
  std::unique_ptr<KalmanVertexFitter> kv_reco;
  const edm::EDGetTokenT<reco::BeamSpot> beamspot_token;
  const edm::EDGetTokenT<reco::VertexCollection> primary_vertex_token;
  const edm::EDGetTokenT<std::vector<double> > gen_vertices_token;
  const edm::EDGetTokenT<reco::VertexCollection> vertex_token;
  const edm::EDGetTokenT<reco::TrackCollection> vertex_seed_tracks_token;
  const std::string sv_to_jets_src;
  edm::EDGetTokenT<mfv::JetVertexAssociation> sv_to_jets_token[mfv::NJetsByUse];
  jmt::TrackRefGetter track_ref_getter;
  const std::string sv_to_muons_src;
  edm::EDGetTokenT<mfv::MuonVertexAssociation> sv_to_muons_token;
  const std::string sv_to_ele_src;
  edm::EDGetTokenT<mfv::ElectronVertexAssociation> sv_to_ele_token;
  const edm::EDGetTokenT<pat::MuonCollection> muons_token;
  const edm::EDGetTokenT<pat::ElectronCollection> electrons_token;
  const edm::EDGetTokenT<double> rho_token;
  EffectiveAreas electron_effective_areas;
  const mfv::VertexAuxSorter sorter;
  const bool verbose;
  const std::string module_label;

  VertexDistanceXY distcalc_2d;
  VertexDistance3D distcalc_3d;
  Measurement1D gen_dist(const reco::Vertex&, const std::vector<double>& gen, const bool use3d);
  Measurement1D miss_dist(const reco::Vertex&, const reco::Vertex&, const math::XYZTLorentzVector& mom);
  std::pair<bool, Measurement1D> track_dist(const reco::TransientTrack & t, const reco::Vertex & v);
};

MFVVertexAuxProducer::MFVVertexAuxProducer(const edm::ParameterSet& cfg)
  : kv_reco(new KalmanVertexFitter(cfg.getParameter<edm::ParameterSet>("kvr_params"), cfg.getParameter<edm::ParameterSet>("kvr_params").getParameter<bool>("doSmoothing"))),
    beamspot_token(consumes<reco::BeamSpot>(cfg.getParameter<edm::InputTag>("beamspot_src"))),
    primary_vertex_token(consumes<reco::VertexCollection>(cfg.getParameter<edm::InputTag>("primary_vertex_src"))),
    gen_vertices_token(consumes<std::vector<double> >(cfg.getParameter<edm::InputTag>("gen_vertices_src"))),
    vertex_token(consumes<reco::VertexCollection>(cfg.getParameter<edm::InputTag>("vertex_src"))),
	vertex_seed_tracks_token(consumes<reco::TrackCollection>(cfg.getParameter<edm::InputTag>("vertex_seed_tracks_src"))),
	sv_to_jets_src(cfg.getParameter<std::string>("sv_to_jets_src")),
    //sv_to_jets_token(consumes<mfv::JetVertexAssociation>(edm::InputTag("sv_to_jets_src"))),
    track_ref_getter(cfg.getParameter<std::string>("@module_label"),
                         cfg.getParameter<edm::ParameterSet>("track_ref_getter"),
                         consumesCollector()),
    sv_to_muons_src(cfg.getParameter<std::string>("sv_to_muons_src")),
    sv_to_ele_src(cfg.getParameter<std::string>("sv_to_ele_src")),
    muons_token(consumes<pat::MuonCollection>(cfg.getParameter<edm::InputTag>("muons_src"))),
    electrons_token(consumes<pat::ElectronCollection>(cfg.getParameter<edm::InputTag>("electrons_src"))),
    rho_token(consumes<double>(cfg.getParameter<edm::InputTag>("rho_src"))),
    electron_effective_areas(cfg.getParameter<edm::FileInPath>("electron_effective_areas").fullPath()),
    sorter(cfg.getParameter<std::string>("sort_by")),
    verbose(cfg.getUntrackedParameter<bool>("verbose", false)),
    module_label(cfg.getParameter<std::string>("@module_label"))
{
  for (int i = 0; i < mfv::NJetsByUse; ++i)
    sv_to_jets_token[i] = consumes<mfv::JetVertexAssociation>(edm::InputTag(sv_to_jets_src, mfv::jetsby_names[i])); // JMTBAD yuck, rethink

  sv_to_muons_token = consumes<mfv::MuonVertexAssociation>(edm::InputTag(sv_to_muons_src, mfv::muonsby_name));
  sv_to_ele_token = consumes<mfv::ElectronVertexAssociation>(edm::InputTag(sv_to_ele_src, mfv::electronsby_name));

  produces<std::vector<MFVVertexAux> >();
}

Measurement1D MFVVertexAuxProducer::gen_dist(const reco::Vertex& sv, const std::vector<double>& gen, const bool use3d) {
  jmt::MinValue d;
  for (int i = 0; i < 2; ++i)
    d(jmt::mag(        sv.x() - gen[i*3],
                       sv.y() - gen[i*3+1],
               use3d ? sv.z() - gen[i*3+2] : 0));
  AlgebraicVector3 v(sv.x(), sv.y(), use3d ? sv.z() : 0);
  const double dist2 = ROOT::Math::Mag2(v);
  const double sim  = ROOT::Math::Similarity(v, sv.covariance());
  const double ed = dist2 != 0 ? sqrt(sim/dist2) : 0;
  return Measurement1D(d, ed);
}

Measurement1D MFVVertexAuxProducer::miss_dist(const reco::Vertex& v0, const reco::Vertex& v1, const math::XYZTLorentzVector& mom) {
  // miss distance is magnitude of (jet direction (= n) cross (tv - sv) ( = d))
  // to calculate uncertainty, use |n X d|^2 = (|n||d|)^2 - (n . d)^2
  AlgebraicVector3 n = ROOT::Math::Unit(AlgebraicVector3(mom.x(), mom.y(), mom.z()));
  AlgebraicVector3 d(v1.x() - v0.x(),
                     v1.y() - v0.y(),
                     v1.z() - v0.z());
  AlgebraicVector3 n_cross_d = ROOT::Math::Cross(n,d);
  double n_dot_d = ROOT::Math::Dot(n,d);
  double val = ROOT::Math::Mag(n_cross_d);

  AlgebraicVector3 jac(2*d(0) - 2*n_dot_d*n(0),
                       2*d(1) - 2*n_dot_d*n(1),
                       2*d(2) - 2*n_dot_d*n(2));
  return Measurement1D(val, sqrt(ROOT::Math::Similarity(jac, v0.covariance() + v1.covariance())) / 2 / val);
}

std::pair<bool, Measurement1D> MFVVertexAuxProducer::track_dist(const reco::TransientTrack & t, const reco::Vertex & v) { //use 3d by default
  return IPTools::absoluteImpactParameter3D(t, v);
}
void MFVVertexAuxProducer::produce(edm::Event& event, const edm::EventSetup& setup) {
  if (verbose) std::cout << "MFVVertexAuxProducer " << module_label << " run " << event.id().run() << " lumi " << event.luminosityBlock() << " event " << event.id().event() << "\n";

  const int track_rescaler_which = 0; // JMTBAD which rescaling if ever a different one
  track_rescaler.setup(!event.isRealData() && track_rescaler_which != -1,
                       jmt::AnalysisEras::pick(event, this),
                       track_rescaler_which);

  edm::ESHandle<TransientTrackBuilder> tt_builder;
  setup.get<TransientTrackRecord>().get("TransientTrackBuilder", tt_builder);

  //////////////////////////////////////////////////////////////////////

  edm::Handle<reco::BeamSpot> beamspot;
  event.getByToken(beamspot_token, beamspot);
  const float bsx = beamspot->x0();
  const float bsy = beamspot->y0();
  const float bsz = beamspot->z0();
  const GlobalPoint origin(bsx, bsy, bsz);
  const reco::Vertex fake_bs_vtx(beamspot->position(), beamspot->covariance3D());

  //////////////////////////////////////////////////////////////////////

  edm::Handle<reco::VertexCollection> primary_vertices;
  event.getByToken(primary_vertex_token, primary_vertices);
  const reco::Vertex* primary_vertex = 0;
  if (primary_vertices->size())
    primary_vertex = &primary_vertices->at(0);

  std::map<reco::TrackRef, size_t> tracks_in_pvs;
  for (size_t i = 0, ie = primary_vertices->size(); i < ie; ++i) {
    for (const auto& p : track_ref_getter.tracks(event, reco::VertexRef(primary_vertices, i)))
      tracks_in_pvs[p.first] = i;
  }

  //////////////////////////////////////////////////////////////////////
 const bool use_sv_to_muons = sv_to_muons_src != "dummy";
  edm::Handle<mfv::MuonVertexAssociation> sv_to_muons;
  if (use_sv_to_muons)
    event.getByToken(sv_to_muons_token, sv_to_muons);

  const bool use_sv_to_ele = sv_to_ele_src != "dummy";
  edm::Handle<mfv::ElectronVertexAssociation> sv_to_ele;
  if (use_sv_to_ele)
    event.getByToken(sv_to_ele_token, sv_to_ele);

  edm::Handle<pat::MuonCollection> muons;
  event.getByToken(muons_token, muons);
  
  edm::Handle<pat::ElectronCollection> electrons;
  event.getByToken(electrons_token, electrons);

  edm::Handle<double> rho;
  event.getByToken(rho_token, rho);

  //////////////////////////////////////////////////////////////////////

  edm::Handle<std::vector<double> > gen_vertices;
  event.getByToken(gen_vertices_token, gen_vertices);
  assert(gen_vertices->size() == 6);

  //////////////////////////////////////////////////////////////////////

  edm::Handle<reco::VertexCollection> secondary_vertices;
  event.getByToken(vertex_token, secondary_vertices);
  const int nsv = int(secondary_vertices->size());

  const bool use_sv_to_jets = sv_to_jets_src != "dummy";
  edm::Handle<mfv::JetVertexAssociation> sv_to_jets[mfv::NJetsByUse];
  if (use_sv_to_jets)
    for (int i = 0; i < mfv::NJetsByUse; ++i)
      event.getByToken(sv_to_jets_token[i], sv_to_jets[i]);

  //////////////////////////////////////////////////////////////////////

  std::unique_ptr<std::vector<MFVVertexAux> > auxes(new std::vector<MFVVertexAux>(nsv));
  //std::set<int> trackicity;
  std::vector<size_t> sort_ntrack = {};
  std::vector<size_t> sort_irawsv = {};
  for (int isv = 0; isv < nsv; ++isv){
      const reco::Vertex& sv = secondary_vertices->at(isv);
      size_t ntracks = sv.nTracks();
      if (isv == 0) { 
        sort_ntrack.push_back(ntracks);
        sort_irawsv.push_back(isv);
      }
      else { 
        std::vector<size_t>::iterator it_ntracks = sort_ntrack.end();
        std::vector<size_t>::iterator it_vtx = sort_irawsv.end();
        while (it_ntracks != sort_ntrack.begin() && ntracks <= sort_ntrack[std::distance(sort_ntrack.begin(), it_ntracks)-1])
        {
          --it_ntracks;
          --it_vtx;
        }
        if (it_ntracks == sort_ntrack.end() && ntracks > sort_ntrack[std::distance(sort_ntrack.begin(), it_ntracks)]) {
          sort_ntrack.push_back(ntracks);
          sort_irawsv.push_back(isv);
        }
        else {
          sort_ntrack.insert(it_ntracks, ntracks);
          sort_irawsv.insert(it_vtx, isv);
        }
      }
  }
  edm::Handle<reco::TrackCollection> vertex_seed_tracks;
  event.getByToken(vertex_seed_tracks_token, vertex_seed_tracks);
  std::vector<size_t> vec_outsedtki;
  for (int irawsv = 0; irawsv < nsv; ++irawsv) {
    int isv = sort_irawsv[nsv-irawsv-1];
    const reco::Vertex& sv = secondary_vertices->at(isv);
    const reco::Vertex& sv0 = secondary_vertices->at(sort_irawsv[nsv-1]); 
    const reco::VertexRef svref(secondary_vertices, isv);
    MFVVertexAux& aux = auxes->at(irawsv);
    aux.which = int2uchar(isv);
    
    aux.x = sv.x();
    aux.y = sv.y();
    aux.z = sv.z();

    aux.cxx = sv.covariance(0,0);
    aux.cxy = sv.covariance(0,1);
    aux.cxz = sv.covariance(0,2);
    aux.cyy = sv.covariance(1,1);
    aux.cyz = sv.covariance(1,2);
    aux.czz = sv.covariance(2,2);

    aux.chi2 = sv.chi2();
    aux.ndof_ = int2uchar_clamp(int(sv.ndof()));

    std::vector<reco::TransientTrack> ttks, rs_ttks;
    for (auto it = sv.tracks_begin(), ite = sv.tracks_end(); it != ite; ++it){
      reco::TrackRef tk = it->castTo<reco::TrackRef>();
      if (sv.trackWeight(*it) >= mfv::track_vertex_weight_min) {
        ttks.push_back(tt_builder->build(**it));
        rs_ttks.push_back(tt_builder->build(track_rescaler.scale(**it).rescaled_tk));
      }
      //get seed tracks outside all vertices
      size_t sedtki = 0;
      for (const reco::Track& sedtk : *vertex_seed_tracks) {
	      assert(abs(sedtk.charge()) == 1);
	      if ((fabs(sedtk.pt() - fabs(tk->charge() * tk->pt())) < 0.0001 &&
		    fabs(sedtk.eta() - tk->eta()) < 0.0001 &&
		    fabs(sedtk.phi() - tk->phi()) < 0.0001) || std::count(vec_outsedtki.begin(), vec_outsedtki.end(), sedtki) > 0) {
		    continue;
	      }
	      vec_outsedtki.push_back(sedtki);
	      sedtki++;
      }
    }
    if (rs_ttks.size() > 1) {
      reco::Vertex rs_sv(TransientVertex(kv_reco->vertex(rs_ttks)));
      if (rs_sv.isValid()) {
        const auto d = distcalc_2d.distance(rs_sv, fake_bs_vtx);
        aux.rescale_chi2 = rs_sv.chi2();
        aux.rescale_x = rs_sv.x();
        aux.rescale_y = rs_sv.y();
        aux.rescale_z = rs_sv.z();
        aux.rescale_cxx = rs_sv.covariance(0,0);
        aux.rescale_cxy = rs_sv.covariance(0,1);
        aux.rescale_cxz = rs_sv.covariance(0,2);
        aux.rescale_cyy = rs_sv.covariance(1,1);
        aux.rescale_cyz = rs_sv.covariance(1,2);
        aux.rescale_czz = rs_sv.covariance(2,2);
        aux.rescale_bs2ddist = d.value();
        aux.rescale_bs2derr = d.error();
      }
      else
        aux.rescale_chi2 = -1;
    }

    if (ttks.size() > 2) {
      const size_t nttks = ttks.size();
      if (verbose) {
        printf("x %f y %f z %f nttks %lu, pts:", aux.x,aux.y,aux.z, nttks);
        for (size_t i = 0; i < nttks; ++i)
          printf(" %f", ttks[i].track().pt());
        printf("\n");
      }
      aux.nm1_chi2.assign(nttks, -1);
      aux.nm1_x.assign(nttks, -1);
      aux.nm1_y.assign(nttks, -1);
      aux.nm1_z.assign(nttks, -1);
      aux.nm1_cxx.assign(nttks, -1);
      aux.nm1_cxy.assign(nttks, -1);
      aux.nm1_cxz.assign(nttks, -1);
      aux.nm1_cyy.assign(nttks, -1);
      aux.nm1_cyz.assign(nttks, -1);
      aux.nm1_czz.assign(nttks, -1);
      aux.nm1_bs2ddist.assign(nttks, -1);
      aux.nm1_bs2derr.assign(nttks, -1);

      std::vector<reco::TransientTrack> ttks_nm1(nttks-1);
      for (size_t i = 0; i < nttks; ++i) {
        for (size_t j = 0; j < nttks; ++j)
          if (j != i)
            ttks_nm1[j-(j>=i)] = ttks[j];

        if (verbose) {
          printf("refit %lu, pts:", i);
          for (size_t j = 0; j < nttks-1; ++j)
            printf(" %f", ttks_nm1[j].track().pt());
        }

        reco::Vertex rf_sv(TransientVertex(kv_reco->vertex(ttks_nm1)));
        if (rf_sv.isValid()) {
          const auto d = distcalc_2d.distance(rf_sv, fake_bs_vtx);
          aux.nm1_chi2[i] = rf_sv.chi2();
          aux.nm1_x[i] = rf_sv.x();
          aux.nm1_y[i] = rf_sv.y();
          aux.nm1_z[i] = rf_sv.z();
          aux.nm1_cxx[i] = rf_sv.covariance(0,0);
          aux.nm1_cxy[i] = rf_sv.covariance(0,1);
          aux.nm1_cxz[i] = rf_sv.covariance(0,2);
          aux.nm1_cyy[i] = rf_sv.covariance(1,1);
          aux.nm1_cyz[i] = rf_sv.covariance(1,2);
          aux.nm1_czz[i] = rf_sv.covariance(2,2);
          aux.nm1_bs2ddist[i] = d.value();
          aux.nm1_bs2derr[i] = d.error();
        }

        if (verbose) printf(" -> chi2 %f x %f y %f z %f\n", aux.nm1_chi2[i], aux.nm1_x[i], aux.nm1_y[i], aux.nm1_z[i]);
      }
    }

    if (verbose) printf("v#%i at %f,%f,%f ndof %.1f\n", isv, aux.x, aux.y, aux.z, sv.ndof());

    math::XYZVector bs2sv = sv.position() - beamspot->position();
    math::XYZVector pv2sv;
    if (primary_vertex != 0)
      pv2sv = sv.position() - primary_vertex->position();

    std::vector<math::XYZTLorentzVector> p4s(mfv::NMomenta);
    p4s[mfv::PTracksOnly] = p4s[mfv::PJetsByNtracks] = p4s[mfv::PTracksPlusJetsByNtracks] = sv.p4();

 
    for (int i = 0; i < mfv::NJetsByUse; ++i)
      aux.njets[i] = 0;

    std::vector<double> jetpairdetas[mfv::NJetsByUse];
    std::vector<double> jetpairdrs[mfv::NJetsByUse];
    std::vector<double> costhjetmomvtxdisps[mfv::NJetsByUse];
    std::set<reco::TrackRef> jets_tracks[mfv::NJetsByUse];
    auto track_in_a_jet = [&](const int i_jet_assoc, const reco::TrackRef& r) {
      return jets_tracks[i_jet_assoc].count(r) > 0;
    };

    if (use_sv_to_jets) {
      for (int i_jet_assoc = 0; i_jet_assoc < mfv::NJetsByUse; ++i_jet_assoc) {
        const int njets = sv_to_jets[i_jet_assoc]->numberOfAssociations(svref);
        if (verbose) printf("    njets %i:\n", njets);
        aux.njets[i_jet_assoc] = int2uchar(njets);

        if (njets > 0) {
          p4s[mfv::PJetsByNtracks] = p4s[mfv::PTracksPlusJetsByNtracks] = math::XYZTLorentzVector();

          const edm::RefVector<pat::JetCollection>& jets = (*sv_to_jets[i_jet_assoc])[svref];

          for (int ijet = 0; ijet < njets; ++ijet) {
            if (verbose) printf("        %i <%f,%f,%f,%f>\n", ijet, jets[ijet]->pt(), jets[ijet]->eta(), jets[ijet]->phi(), jets[ijet]->energy());
            p4s[1+i_jet_assoc] += jets[ijet]->p4();

            for (auto r : track_ref_getter.tracks(event, *jets[ijet])) {
              jets_tracks[i_jet_assoc].insert(r);
              if (verbose) printf("            tk key %i <%f,%f,%f,%f,%f>\n", r.key(), r->charge()*r->pt(), r->eta(), r->phi(), r->dxy(), r->dz());
            }

            if (primary_vertex)
              costhjetmomvtxdisps[i_jet_assoc].push_back(jmt::costh3(jets[ijet]->p4(), pv2sv));
            else
              costhjetmomvtxdisps[i_jet_assoc].push_back(-2);

            for (int jjet = ijet+1; jjet < njets; ++jjet) {
              jetpairdetas[i_jet_assoc].push_back(fabs(jets[ijet]->eta() - jets[jjet]->eta()));
              jetpairdrs[i_jet_assoc].push_back(reco::deltaR(*jets[ijet], *jets[jjet]));
            }
          }
        
          math::XYZTLorentzVector jpt_p4 = p4s[1+i_jet_assoc];
          if (verbose) printf("    jpt accounting:\n");
          for (auto it = sv.tracks_begin(), ite = sv.tracks_end(); it != ite; ++it) {
            if (sv.trackWeight(*it) >= mfv::track_vertex_weight_min) {
              reco::TrackRef tk = it->castTo<reco::TrackRef>();
              if (!track_in_a_jet(i_jet_assoc, tk)) {
                jpt_p4 += math::XYZTLorentzVector(tk->px(), tk->py(), tk->pz(), tk->p());
                if (verbose) printf("        add tk key %i <%f,%f,%f,%f,%f>\n", tk.key(), tk->charge()*tk->pt(), tk->eta(), tk->phi(), tk->dxy(), tk->dz());
              }
            }
          }

          p4s[1 + i_jet_assoc + mfv::NJetsByUse] = jpt_p4;
        }
      }

      jmt::StatCalculator jetpairdeta(jetpairdetas[mfv::JByNtracks]);
      aux.jetpairdetamin(jetpairdeta.min.back());
      aux.jetpairdetamax(jetpairdeta.max.back());
      aux.jetpairdetaavg(jetpairdeta.avg.back());
      aux.jetpairdetarms(jetpairdeta.rms.back());

      jmt::StatCalculator jetpairdr(jetpairdrs[mfv::JByNtracks]);
      aux.jetpairdrmin(jetpairdr.min.back());
      aux.jetpairdrmax(jetpairdr.max.back());
      aux.jetpairdravg(jetpairdr.avg.back());
      aux.jetpairdrrms(jetpairdr.rms.back());

      if (aux.njets[mfv::JByNtracks] > 0) {
        jmt::StatCalculator costhjetmomvtxdisp(costhjetmomvtxdisps[mfv::JByNtracks]);
        aux.costhjetmomvtxdispmin(costhjetmomvtxdisp.min.back());
        aux.costhjetmomvtxdispmax(costhjetmomvtxdisp.max.back());
        aux.costhjetmomvtxdispavg(costhjetmomvtxdisp.avg.back());
        aux.costhjetmomvtxdisprms(costhjetmomvtxdisp.rms.back());
      }
      else {
        aux.costhjetmomvtxdispmin(-2);
        aux.costhjetmomvtxdispmax(-2);
        aux.costhjetmomvtxdispavg(-2);
        aux.costhjetmomvtxdisprms(-2);
      }
    }
    aux.nelectrons = 0;
    aux.nmuons = 0;
    aux.nleptons = 0;

    //setting up everything for calculating transverse impact parameter between lepton and sv 
    std::pair<bool, Measurement1D> mu_vtx_dist;
    std::pair<bool, Measurement1D> ele_vtx_dist;
    std::vector<reco::TransientTrack> mu_ttracks;
    std::vector<reco::TransientTrack> ele_ttracks;
    std::pair<bool, Measurement1D> matchedmu_vtx_dist;
    std::pair<bool, Measurement1D> matchedele_vtx_dist;
    std::vector<reco::TransientTrack> matchedmu_ttracks;
    std::vector<reco::TransientTrack> matchedele_ttracks;
    
    if (use_sv_to_ele) {
      const int nele = sv_to_ele->numberOfAssociations(svref);
      aux.nelectrons = nele;
      aux.nleptons = nele;
      if (verbose) printf("    nele %i:\n", nele);
      //getting all info from matched electron; including transverse IP 
      if (nele > 0) {
        const edm::RefVector<pat::ElectronCollection>& electronref = (*sv_to_ele)[svref];
        for (int iel = 0; iel < nele; ++iel) {
          reco::GsfTrackRef etk = electronref[iel]->gsfTrack();
          if (!etk.isNull()) {
            matchedele_ttracks.push_back(tt_builder->build(etk));    
          
            const auto pfIso = electronref[iel]->pfIsolationVariables();
            const float eA = electron_effective_areas.getEffectiveArea(fabs(electronref[iel]->superCluster()->eta()));
            const float iso = (pfIso.sumChargedHadronPt + std::max(0., pfIso.sumNeutralHadronEt + pfIso.sumPhotonEt - *rho*eA)) / electronref[iel]->pt();


            bool isVetoEl = electronref[iel]->electronID("cutBasedElectronID-Fall17-94X-V2-veto");
            bool isLooseEl = electronref[iel]->electronID("cutBasedElectronID-Fall17-94X-V2-loose");
            bool isMedEl = electronref[iel]->electronID("cutBasedElectronID-Fall17-94X-V2-medium");
            bool isTightEl = electronref[iel]->electronID("cutBasedElectronID-Fall17-94X-V2-tight");

            aux.electron_iso.push_back(iso);
            std::vector<int> eleID;
            eleID.push_back(isVetoEl);
            eleID.push_back(isLooseEl);
            eleID.push_back(isMedEl);
            eleID.push_back(isTightEl);
            
            aux.electron_ID.push_back(eleID);

            aux.electron_pt.push_back(electronref[iel]->pt());
            aux.electron_eta.push_back(electronref[iel]->eta());
            aux.electron_phi.push_back(electronref[iel]->phi());
            aux.electron_x.push_back(etk->vx());
            aux.electron_y.push_back(etk->vy());
            aux.electron_z.push_back(etk->vz());
            if (primary_vertex != 0) {
              aux.electron_dxy.push_back(etk->dxy(primary_vertex->position()));
              aux.electron_dz.push_back(etk->dz(primary_vertex->position()));
            }
            aux.electron_dxybs.push_back(etk->dxy(beamspot->position()));
            aux.electron_dxyerr.push_back(etk->dxyError());
            aux.electron_dzerr.push_back(etk->dzError());
          }
        }
      }
      //now also getting transverse IP from all electrons (not just matched)
      for (const pat::Electron& electron : *electrons) {
        reco::GsfTrackRef etk = electron.gsfTrack();
        if (!etk.isNull()) {
          ele_ttracks.push_back(tt_builder->build(etk));
        }
      }
    }

    if (use_sv_to_muons) {
      const int nmu = sv_to_muons->numberOfAssociations(svref);
      aux.nmuons = nmu;
      aux.nleptons += nmu;
      if (verbose) printf("    nmu %i:\n", nmu);
      if (nmu > 0) {
        const edm::RefVector<pat::MuonCollection>& muonref = (*sv_to_muons)[svref];
        for (int imu = 0; imu < nmu; ++imu) {
          reco::TrackRef mtk = muonref[imu]->innerTrack();
          if (!mtk.isNull()) {
            matchedmu_ttracks.push_back(tt_builder->build(mtk));    
          
            const float iso = (muonref[imu]->pfIsolationR04().sumChargedHadronPt + std::max(0., muonref[imu]->pfIsolationR04().sumNeutralHadronEt + muonref[imu]->pfIsolationR04().sumPhotonEt -0.5*muonref[imu]->pfIsolationR04().sumPUPt))/muonref[imu]->pt();
            aux.muon_iso.push_back(iso);

            bool isLooseMuon = muonref[imu]->passed(reco::Muon::CutBasedIdLoose);
            bool isMedMuon = muonref[imu]->passed(reco::Muon::CutBasedIdMedium);
            bool isTightMuon = muonref[imu]->passed(reco::Muon::CutBasedIdTight);

            std::vector<int> muID;
            muID.push_back(isLooseMuon);
            muID.push_back(isMedMuon);
            muID.push_back(isTightMuon);

            aux.muon_ID.push_back(muID);

            aux.muon_pt.push_back(muonref[imu]->pt());
            aux.muon_eta.push_back(muonref[imu]->eta());
            aux.muon_phi.push_back(muonref[imu]->phi());
            aux.muon_x.push_back(mtk->vx());
            aux.muon_y.push_back(mtk->vy());
            aux.muon_z.push_back(mtk->vz());
            if (primary_vertex != 0) {
              aux.muon_dxy.push_back(mtk->dxy(primary_vertex->position()));
              aux.muon_dz.push_back(mtk->dz(primary_vertex->position()));
            }
            aux.muon_dxybs.push_back(mtk->dxy(beamspot->position()));
            aux.muon_dxyerr.push_back(mtk->dxyError());
            aux.muon_dzerr.push_back(mtk->dzError());
          }
        }
      }
      for (const pat::Muon& muon : *muons) {
        reco::TrackRef mtk = muon.innerTrack();
        if (!mtk.isNull()) {
          mu_ttracks.push_back(tt_builder->build(mtk));
        }
      }
    }
    for (auto ettk : ele_ttracks) {
      ele_vtx_dist = IPTools::absoluteTransverseImpactParameter(ettk, sv);
      aux.elevtxtip.push_back(ele_vtx_dist.second.value());
      aux.elevtxtiperr.push_back(ele_vtx_dist.second.error());
      aux.elevtxtipsig.push_back(ele_vtx_dist.second.significance());
    }
    for (auto mettk : matchedele_ttracks ) {
      matchedele_vtx_dist = IPTools::absoluteTransverseImpactParameter(mettk, sv);
      aux.matchedelevtxtip.push_back(matchedele_vtx_dist.second.value());
      aux.matchedelevtxtiperr.push_back(matchedele_vtx_dist.second.error());
      aux.matchedelevtxtipsig.push_back(matchedele_vtx_dist.second.significance());
    }
    for (auto mttk : mu_ttracks ) {
      mu_vtx_dist = IPTools::absoluteTransverseImpactParameter(mttk, sv);
      aux.muvtxtip.push_back(mu_vtx_dist.second.value());
      aux.muvtxtiperr.push_back(mu_vtx_dist.second.error());
      aux.muvtxtipsig.push_back(mu_vtx_dist.second.significance());
    }
    for (auto mmttk : matchedmu_ttracks ) {
      matchedmu_vtx_dist = IPTools::absoluteTransverseImpactParameter(mmttk, sv);
      aux.matchedmuvtxtip.push_back(matchedmu_vtx_dist.second.value());
      aux.matchedmuvtxtiperr.push_back(matchedmu_vtx_dist.second.error());
      aux.matchedmuvtxtipsig.push_back(matchedmu_vtx_dist.second.significance());
    }

    if (verbose) printf("    momenta:\n");
    for (int i = 0; i < mfv::NMomenta; ++i) {
      aux.pt[i]   = p4s[i].pt();
      aux.eta[i]  = p4s[i].eta();
      aux.phi[i]  = p4s[i].phi();
      aux.mass[i] = p4s[i].mass();
      if (verbose) printf("    %i <%f,%f,%f,%f>\n", i, aux.pt[i], aux.eta[i], aux.phi[i], aux.mass[i]);
    }
      
    //const double sv_r = mag(sv.position().x() - bsx, sv.position().y() - bsy);
    //const double sv_z = fabs(sv.position().z() - bsz);

    auto trkb = sv.tracks_begin();
    auto trke = sv.tracks_end();

    std::vector<double> costhtkmomvtxdisps;

    if (verbose) printf("    tracks %i:\n", int(trke-trkb));
    for (auto trki = trkb; trki != trke; ++trki) {
      const reco::TrackBaseRef& tri = *trki;
      const reco::TransientTrack sedtri = tt_builder->build(**trki); 
      const reco::TrackRef& trref = tri.castTo<reco::TrackRef>();
      const math::XYZTLorentzVector tri_p4(tri->px(), tri->py(), tri->pz(), tri->p());

      //if (trackicity.count(tri.key()) > 0)
        //throw cms::Exception("VertexAuxProducer") << "trackicity > 1";
      //else
        //trackicity.insert(tri.key());

      if (sv.trackWeight(tri) < mfv::track_vertex_weight_min)
        continue;

      costhtkmomvtxdisps.push_back(jmt::costh3(tri->momentum(), pv2sv));

      const uchar nhitsbehind = 0; //int2uchar(tracker_extents.numHitsBehind(tri->hitPattern(), sv_r, sv_z));

      const auto pv_for_track = tracks_in_pvs.find(trref);

      if (verbose) printf("        %i <%f,%f,%f,%f,%f>\n", int(trki-trkb), tri->charge()*tri->pt(), tri->eta(), tri->phi(), tri->dxy(), tri->dz());

      aux.track_weight(-1, sv.trackWeight(tri));
      aux.track_q(-1, tri->charge());
      aux.track_hitpattern(-1,
                           tri->hitPattern().numberOfValidPixelHits(), 
                           tri->hitPattern().pixelLayersWithMeasurement(), 
                           tri->hitPattern().numberOfValidStripHits(),
                           tri->hitPattern().stripLayersWithMeasurement(), 
                           nhitsbehind,
                           tri->hitPattern().numberOfLostHits(reco::HitPattern::TRACK_HITS)); // JMTBAD could add missing inner, outer

      aux.track_injet.push_back(track_in_a_jet(mfv::JByNtracks, trref)); // JMTBAD multiple jet assoc types
      aux.track_inpv.push_back(pv_for_track == tracks_in_pvs.end() ? -1 : pv_for_track->second);
      aux.track_dxy.push_back(fabs(tri->dxy(beamspot->position())));
      aux.track_dz.push_back(primary_vertex ? fabs(tri->dz(primary_vertex->position())) : 0); // JMTBAD not the previous behavior when no PV
      aux.track_vx.push_back(tri->vx());
      aux.track_vy.push_back(tri->vy());
      aux.track_vz.push_back(tri->vz());
      aux.track_px.push_back(tri->px());
      aux.track_py.push_back(tri->py());
      aux.track_pz.push_back(tri->pz());
      aux.track_chi2.push_back(tri->chi2());
      aux.track_ndof.push_back(tri->ndof());
      aux.track_cov.push_back(tri->covariance());
      aux.track_pt_err.push_back(tri->ptError());
      aux.track_eta.push_back(tri->eta());
      aux.track_phi.push_back(tri->phi());
      std::pair<bool, Measurement1D> tkdist = track_dist(sedtri, sv);
      aux.track_tkdist_val.push_back(tkdist.second.value());
      aux.track_tkdist_sig.push_back(tkdist.second.significance());
      if (nsv >= 2 && irawsv == 0){
         const reco::Vertex& sv1 = secondary_vertices->at(sort_irawsv[nsv-2]);
         std::pair<bool, Measurement1D> tkdist_tosv1 = track_dist(sedtri, sv1);
         aux.track_tkdisttosv1_val.push_back(tkdist_tosv1.second.value());
         aux.track_tkdisttosv1_sig.push_back(tkdist_tosv1.second.significance());
      }
    }

    jmt::StatCalculator costhtkmomvtxdisp(costhtkmomvtxdisps);
    aux.costhtkmomvtxdispmin(costhtkmomvtxdisp.min.back());
    aux.costhtkmomvtxdispmax(costhtkmomvtxdisp.max.back());
    aux.costhtkmomvtxdispavg(costhtkmomvtxdisp.avg.back());
    aux.costhtkmomvtxdisprms(costhtkmomvtxdisp.rms.back());

    auto g2d = gen_dist(sv, *gen_vertices, false);
    auto g3d = gen_dist(sv, *gen_vertices, true);
    aux.gen2ddist = g2d.value();
    aux.gen2derr  = g2d.error();
    aux.gen3ddist = g3d.value();
    aux.gen3derr  = g3d.error();

    auto bs2d = distcalc_2d.distance(sv, fake_bs_vtx);
    aux.bs2ddist = bs2d.value();
    aux.bs2derr  = bs2d.error();

    if (primary_vertex != 0) {
      auto pv2d = distcalc_2d.distance(sv, *primary_vertex);
      auto pv3d = distcalc_3d.distance(sv, *primary_vertex);
      aux.pv2ddist = pv2d.value();
      aux.pv2derr  = pv2d.error();
      aux.pv3ddist = pv3d.value();
      aux.pv3derr  = pv3d.error();
    }
    else
      aux.pv2ddist = aux.pv3ddist = aux.pv2derr = aux.pv3derr = -1;

    for (int i = 0; i < mfv::NMomenta; ++i) {
      const math::XYZTLorentzVector& mom = p4s[i];
      aux.costhmombs(i, -2);
      aux.costhmompv2d(i, -2);
      aux.costhmompv3d(i, -2);
      aux.missdistpv[i] = 1e9;
      aux.missdistpverr[i] = -1;

      if (mom.pt() > 0) {
        aux.costhmombs(i, jmt::costh2(mom, bs2sv));
        if (primary_vertex != 0) {
          aux.costhmompv2d(i, jmt::costh2(mom, pv2sv));
          aux.costhmompv3d(i, jmt::costh3(mom, pv2sv));
          auto mdpv = miss_dist(*primary_vertex, sv, mom);
          aux.missdistpv[i] = mdpv.value();
          aux.missdistpverr[i] = mdpv.error();
          auto mdsv0 = miss_dist(sv0, sv, mom);
          aux.missdistsv0[i] = mdsv0.value();
          aux.missdistsv0err[i] = mdsv0.error();
        }
      }
    }

    if (verbose) printf("aux finish isv %i at %f %f %f ntracks %i bs2ddist %f bs2derr %f\n", isv, aux.x, aux.y, aux.z, aux.ntracks(), aux.bs2ddist, aux.bs2derr);
  }
  //investigate outside seed tracks from vertices 
  for (int irawsv = 0; irawsv < nsv; ++irawsv) {
	  int isv = sort_irawsv[nsv - irawsv - 1];
	  const reco::Vertex& sv = secondary_vertices->at(isv);
	  const reco::VertexRef svref(secondary_vertices, isv);
	  MFVVertexAux & aux = auxes->at(irawsv);

	  size_t sedtki = 0;
	  for (const reco::Track& sedtk : *vertex_seed_tracks) {
		  assert(abs(sedtk.charge()) == 1);
		  if (std::count(vec_outsedtki.begin(), vec_outsedtki.end(), sedtki) > 0) {
			  const reco::TransientTrack outsedtri = tt_builder->build(sedtk);
			  std::pair<bool, Measurement1D> tkdist = track_dist(outsedtri, sv);
			  aux.outsed_track_tkdist_val.push_back(tkdist.second.value());
			  aux.outsed_track_tkdist_sig.push_back(tkdist.second.significance());
			  if (irawsv == 0) {
				  const double dxybs = sedtk.dxy(*beamspot);
				  const auto rs = track_rescaler.scale(sedtk);
				  const double rescaled_dxyerr = rs.rescaled_tk.dxyError();
				  const double rescaled_sigmadxybs = dxybs / rescaled_dxyerr;
				  aux.outsed_track_dxy.push_back(fabs(sedtk.dxy(beamspot->position())));
				  aux.outsed_track_nsigmadxy.push_back(rescaled_sigmadxybs);

			  }
		  }
	  }
	  
  }
  sorter.sort(*auxes);

  event.put(std::move(auxes));
}

DEFINE_FWK_MODULE(MFVVertexAuxProducer);
