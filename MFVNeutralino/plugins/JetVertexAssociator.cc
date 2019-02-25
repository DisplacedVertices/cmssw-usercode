#include "TH2F.h"
#include "TVector3.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/Common/interface/AssociationMap.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "JMTucker/MFVNeutralinoFormats/interface/JetVertexAssociation.h"
#include "JMTucker/MFVNeutralino/interface/JetTrackRefGetter.h"

class MFVJetVertexAssociator : public edm::EDProducer {
public:
  MFVJetVertexAssociator(const edm::ParameterSet&);

  virtual void produce(edm::Event&, const edm::EventSetup&);

private:
  typedef mfv::JetVertexAssociation Association;

  const bool enable;
  const edm::EDGetTokenT<pat::JetCollection> jet_token;
  const edm::EDGetTokenT<reco::VertexRefVector> vertex_ref_token;
  const edm::EDGetTokenT<reco::VertexCollection> vertex_token;

  mfv::JetTrackRefGetter jet_track_ref_getter;

  const bool input_is_refs;
  const std::string tag_info_name;
  const double min_vertex_track_weight;
  const int min_tracks_shared;
  const double min_track_pt;
  const int min_hits_shared;
  const double max_cos_angle_diff;
  const double max_miss_dist;
  const double max_miss_sig;
  const bool histos;
  const bool verbose;

  TH2F* h_n_jets_v_vertices;
  TH1F* h_n_vertex_tracks;
  TH1F* h_n_jet_tracks;

  TH1F* h_ntracks;
  TH1F* h_ntracks_ptmin;
  TH1F* h_sum_nhits;
  TH1F* h_cos_angle;
  TH1F* h_miss_dist;
  TH1F* h_miss_dist_err;
  TH1F* h_miss_dist_sig;
  TH2F* h_miss_dist_err_v;

  TH1F* h_best_ntracks;
  TH1F* h_best_ntracks_ptmin;
  TH1F* h_best_sum_nhits;
  TH1F* h_best_cos_angle;
  TH1F* h_best_miss_dist;
  TH1F* h_best_miss_dist_err;
  TH1F* h_best_miss_dist_sig;
  TH2F* h_best_miss_dist_err_v;

  TH2F* h_best_ntracks_v_second;
  TH2F* h_best_ntracks_ptmin_v_second;
  TH2F* h_best_sum_nhits_v_second;
  TH2F* h_best_cos_angle_v_second;
  TH2F* h_best_miss_dist_v_second;
  TH2F* h_best_miss_dist_err_v_second;
  TH2F* h_best_miss_dist_sig_v_second;

  TH2F* h_n_matchedjets_v_jets[mfv::NJetsBy];
  TH2F* h_n_matchedjets_v_vertices[mfv::NJetsBy];
  TH2F* h_n_matchedvertices_v_jets[mfv::NJetsBy];
  TH2F* h_n_matchedvertices_v_vertices[mfv::NJetsBy];
};

MFVJetVertexAssociator::MFVJetVertexAssociator(const edm::ParameterSet& cfg)
  : enable(cfg.getParameter<bool>("enable")),
    jet_token(consumes<pat::JetCollection>(cfg.getParameter<edm::InputTag>("jet_src"))),
    vertex_ref_token(consumes<reco::VertexRefVector>(cfg.getParameter<edm::InputTag>("vertex_src"))),
    vertex_token(consumes<reco::VertexCollection>(cfg.getParameter<edm::InputTag>("vertex_src"))),
    jet_track_ref_getter(cfg.getParameter<std::string>("@module_label"),
                         cfg.getParameter<edm::ParameterSet>("jet_track_ref_getter"),
                         consumesCollector()),
    input_is_refs(cfg.getParameter<bool>("input_is_refs")),
    tag_info_name(cfg.getParameter<std::string>("tag_info_name")),
    min_vertex_track_weight(cfg.getParameter<double>("min_vertex_track_weight")),
    min_tracks_shared(cfg.getParameter<int>("min_tracks_shared")),
    min_track_pt(cfg.getParameter<double>("min_track_pt")),
    min_hits_shared(cfg.getParameter<int>("min_hits_shared")),
    max_cos_angle_diff(cfg.getParameter<double>("max_cos_angle_diff")),
    max_miss_dist(cfg.getParameter<double>("max_miss_dist")),
    max_miss_sig(cfg.getParameter<double>("max_miss_sig")),
    histos(cfg.getUntrackedParameter<bool>("histos", false)),
    verbose(cfg.getUntrackedParameter<bool>("verbose", false))
{
  for (int i = 0; i < mfv::NJetsBy; ++i)
    produces<Association>(mfv::jetsby_names[i]);

  if (histos) {
    edm::Service<TFileService> fs;
    
    h_n_jets_v_vertices = fs->make<TH2F>("h_n_jets_v_vertices", ";# of vertices;# of jets", 20, 0, 20, 20, 0, 20);
    h_n_vertex_tracks = fs->make<TH1F>("h_n_vertex_tracks", ";# tracks per vertex;arb. units", 50, 0, 50);
    h_n_jet_tracks = fs->make<TH1F>("h_n_jet_tracks", ";# tracks per jet;arb. units", 50, 0, 50);

    h_ntracks = fs->make<TH1F>("h_ntracks", ";# tracks shared w. a vertex;arb. units", 20, 0, 20);
    h_ntracks_ptmin = fs->make<TH1F>("h_ntracks_ptmin", ";# tracks (p_{T} cut) shared w. a vertex;arb. units", 20, 0, 20);
    h_sum_nhits = fs->make<TH1F>("h_sum_nhits", ";# tracks' hits shared w. a vertex;arb. units", 100, 0, 100);
    h_cos_angle = fs->make<TH1F>("h_cos_angle", ";cos(angle between jet mom. and TV-SV);arb. units", 101, -1, 1.02);
    h_miss_dist = fs->make<TH1F>("h_miss_dist", ";jet miss distance (cm);arb. units", 100, 0, 0.5);
    h_miss_dist_err = fs->make<TH1F>("h_miss_dist_err", ";#sigma(jet miss distance) (cm);arb. units", 100, 0, 0.5);
    h_miss_dist_sig = fs->make<TH1F>("h_miss_dist_sig", ";N#sigma(jet miss distance);arb. units", 100, 0, 50);
    h_miss_dist_err_v = fs->make<TH2F>("h_miss_dist_err_v", ";jet miss distance to a vertex (cm);#sigma(jet miss distance to a vertex) (cm)", 100, 0, 0.5, 100, 0, 0.5);

    h_best_ntracks = fs->make<TH1F>("h_best_ntracks", ";# tracks shared w. best vertex;arb. units", 20, 0, 20);
    h_best_ntracks_ptmin = fs->make<TH1F>("h_best_ntracks_ptmin", ";# tracks (p_{T} cut) shared w. best vertex;arb. units", 20, 0, 20);
    h_best_sum_nhits = fs->make<TH1F>("h_best_sum_nhits", ";# tracks' hits shared w. best vertex;arb. units", 100, 0, 100);
    h_best_cos_angle = fs->make<TH1F>("h_best_cos_angle", ";cos(angle between jet mom. and TV-best SV);arb. units", 101, -1, 1.02);
    h_best_miss_dist = fs->make<TH1F>("h_best_miss_dist", ";jet miss distance to best SV (cm);arb. units", 100, 0, 0.5);
    h_best_miss_dist_err = fs->make<TH1F>("h_best_miss_dist_err", ";#sigma(jet miss distance to best SV) (cm);arb. units", 100, 0, 0.5);
    h_best_miss_dist_sig = fs->make<TH1F>("h_best_miss_dist_sig", ";N#sigma(jet miss distance to best SV);arb. units", 100, 0, 50);
    h_best_miss_dist_err_v = fs->make<TH2F>("h_best_miss_dist_err_v", ";jet miss distance to best vertex (cm);#sigma(jet miss distance to best vertex) (cm)", 100, 0, 0.5, 100, 0, 0.5);

    h_best_ntracks_v_second = fs->make<TH2F>("h_best_ntracks_v_second", ";# tracks shared w. 2nd-best vertex;# tracks shared w. best vertex", 20, 0, 20, 20, 0, 20);
    h_best_ntracks_ptmin_v_second = fs->make<TH2F>("h_best_ntracks_ptmin_v_second", ";# tracks (p_{T} cut) shared w. 2nd-best vertex;# tracks (p_{T} cut) shared w. best vertex", 20, 0, 20, 20, 0, 20);
    h_best_sum_nhits_v_second = fs->make<TH2F>("h_best_sum_nhits_v_second", ";# tracks' hits shared w. 2nd-best vertex;# tracks' hits shared w. best vertex", 100, 0, 100, 100, 0, 100);
    h_best_cos_angle_v_second = fs->make<TH2F>("h_best_cos_angle_v_second", ";cos(angle between jet mom. and TV-SV) for 2nd-best vertex;cos(angle between jet mom. and TV-SV) for best vertex", 101, -1, 1.02, 101, -1, 1.02);
    h_best_miss_dist_v_second = fs->make<TH2F>("h_best_miss_dist_v_second", ";jet miss distance to 2nd-best vertex (cm);jet miss distance to best vertex", 100, 0, 0.5, 100, 0, 0.5);
    h_best_miss_dist_err_v_second = fs->make<TH2F>("h_best_miss_dist_err_v_second", ";#sigma(jet miss distance to 2nd-best vertex) (cm);#sigma(jet miss distance to best vertex) (cm)", 100, 0, 0.5, 100, 0, 0.5);
    h_best_miss_dist_sig_v_second = fs->make<TH2F>("h_best_miss_dist_sig_v_second", ";N#sigma(jet miss distance to 2nd-best vertex);N#sigma(jet miss distance to best vertex)", 100, 0, 50, 100, 0, 50);

    for (int i = 0; i < 5; ++i) {
      h_n_matchedjets_v_jets        [i] = fs->make<TH2F>(TString::Format("h_n_matched%sjets_v_jets",         mfv::jetsby_names[i]), TString::Format(";# of jets;# of matched jets (%s)",         mfv::jetsby_names[i]), 20, 0, 20, 20, 0, 20);
      h_n_matchedjets_v_vertices    [i] = fs->make<TH2F>(TString::Format("h_n_matched%sjets_v_vertices",     mfv::jetsby_names[i]), TString::Format(";# of vertices;# of matched jets (%s)",     mfv::jetsby_names[i]), 20, 0, 20, 20, 0, 20);
      h_n_matchedvertices_v_jets    [i] = fs->make<TH2F>(TString::Format("h_n_matched%svertices_v_jets",     mfv::jetsby_names[i]), TString::Format(";# of jets;# of matched vertices (%s)",     mfv::jetsby_names[i]), 20, 0, 20, 20, 0, 20);
      h_n_matchedvertices_v_vertices[i] = fs->make<TH2F>(TString::Format("h_n_matched%svertices_v_vertices", mfv::jetsby_names[i]), TString::Format(";# of vertices;# of matched vertices (%s)", mfv::jetsby_names[i]), 20, 0, 20, 20, 0, 20);
    }
  }
}

void MFVJetVertexAssociator::produce(edm::Event& event, const edm::EventSetup&) {
  edm::Handle<pat::JetCollection> jets;
  event.getByToken(jet_token, jets);

  std::vector<reco::VertexRef> vertices;

  if (input_is_refs) {
    edm::Handle<reco::VertexRefVector> h;
    event.getByToken(vertex_ref_token, h);
    for (const reco::VertexRef& ref : *h)
      vertices.push_back(ref);
  }
  else {
    edm::Handle<reco::VertexCollection> h;
    event.getByToken(vertex_token, h);
    for (size_t i = 0; i < h->size(); ++i)
      vertices.push_back(reco::VertexRef(h, i));
  }

  const size_t n_jets = jets->size();
  const size_t n_vertices = vertices.size();

  if (histos) {
    h_n_jets_v_vertices->Fill(n_vertices, n_jets);
    for (const reco::VertexRef& vtx : vertices)
      h_n_vertex_tracks->Fill(vtx->nTracks(min_vertex_track_weight));
  }

  if (verbose) {
    for (size_t ivtx = 0; ivtx < n_vertices; ++ivtx) {
      const reco::Vertex& vtx = *vertices.at(ivtx);
      printf("ivtx %lu ntracks %i mass %f\n", ivtx, vtx.nTracks(min_vertex_track_weight), vtx.p4().mass());
    }
  }

  // Associate jets to vertices. For each jet, find the vertex that
  // shares the most tracks, or the most tracks with given ptmin, or
  // the most tracks' hits.
  //
  // When considering #tracks, do not use fractions of tracks so that
  // low-ntrack vertices are not preferentially picked.
  //
  // Also, especially for the case when a jet does not share tracks
  // with any vertex, try to find a vertex (SV) that it points back to
  // in a straight line. The two points that form the line are the SV
  // position and the jet's vertex. The jet's vertex is taken from the
  // b-tag software "SV" (= "TV" here) tag for now. (JMTBAD try
  // fitting jet's tracks for vertices using our fitter, and taking
  // the one with e.g. the largest number of tracks, or pT.)
  //
  // Try taking closest in cos(angle between jet momentum and
  // (TV-SV)), as well as the distance of closest approach ("miss
  // distance").

  std::vector<int> index_by_ntracks(n_jets, -1);
  std::vector<int> best_ntracks(n_jets, 0);
  std::vector<int> second_best_ntracks(n_jets, 0);

  std::vector<int> index_by_ntracks_ptmin(n_jets, -1);
  std::vector<int> best_ntracks_ptmin(n_jets, 0);
  std::vector<int> second_best_ntracks_ptmin(n_jets, 0);

  std::vector<int> index_by_sum_nhits(n_jets, -1);
  std::vector<int> best_sum_nhits(n_jets, 0);
  std::vector<int> second_best_sum_nhits(n_jets, 0);

  std::vector<int> index_by_cos_angle(n_jets, -1);
  std::vector<double> best_cos_angle(n_jets, 1e9);
  std::vector<double> second_best_cos_angle(n_jets, 1e9);

  std::vector<int> index_by_miss_dist(n_jets, -1);
  std::vector<Measurement1D> best_miss_dist(n_jets, Measurement1D(1e9, 1));
  std::vector<Measurement1D> second_best_miss_dist(n_jets, Measurement1D(1e9, 1));

  if (enable) {
    for (size_t ijet = 0; ijet < n_jets; ++ijet) {
      const pat::Jet& jet = jets->at(ijet);
      std::set<reco::TrackRef> jet_tracks;

      for (auto r : jet_track_ref_getter.tracks(event, jet))
        jet_tracks.insert(r);

      const size_t n_jet_tracks = jet_tracks.size();
      if (histos)
        h_n_jet_tracks->Fill(n_jet_tracks);

      const reco::SecondaryVertexTagInfo* jet_tag = jet.tagInfoSecondaryVertex(tag_info_name);
      const reco::Vertex* jet_tag_vtx = 0;
      TVector3 jet_tag_vtx_pos;
      if (jet_tag && jet_tag->nVertices() > 0) {
        jet_tag_vtx = &jet_tag->secondaryVertex(0);
        jet_tag_vtx_pos.SetXYZ(jet_tag_vtx->x(), jet_tag_vtx->y(), jet_tag_vtx->z());
      }
      const TVector3 jet_mom_dir = TVector3(jet.px(), jet.py(), jet.pz()).Unit();

      for (size_t ivtx = 0; ivtx < n_vertices; ++ivtx) {
        const reco::Vertex& vtx = *vertices.at(ivtx);
        int ntracks = 0;
        int ntracks_ptmin = 0;
        int sum_nhits = 0;
        double cos_angle = 1e9;
        Measurement1D miss_dist(1e9, 1);

        for (auto itk = vtx.tracks_begin(), itke = vtx.tracks_end(); itk != itke; ++itk) {
          if (vtx.trackWeight(*itk) >= min_vertex_track_weight) {
            reco::TrackRef tk = itk->castTo<reco::TrackRef>();
            if (jet_tracks.count(tk) > 0) {
              ++ntracks;
              if (tk->pt() > min_track_pt)
                ++ntracks_ptmin;
              sum_nhits += tk->hitPattern().numberOfValidHits();
            }
          }
        }

        if (jet_tag_vtx) {
          const TVector3 sv_to_tv = jet_tag_vtx_pos - TVector3(vtx.x(), vtx.y(), vtx.z());
          cos_angle = sv_to_tv.Dot(jet_mom_dir) / sv_to_tv.Mag();

          // JMTBAD use mfv::miss_dist()
          // miss distance is magnitude of (jet direction cross (tv - sv))
          // to calculate uncertainty, use |n X d|^2 = (|n||d|)^2 - (n . d)^2
          const TVector3& n = jet_mom_dir;
          const TVector3& d = sv_to_tv;
          const double n_dot_d = n.Dot(d);
          const TVector3 n_cross_d = n.Cross(d);
          typedef math::VectorD<3>::type vec_t;
          typedef math::ErrorD<3>::type mat_t;
          vec_t jacobian(2*d.x() - 2*n_dot_d*n.x(),
                         2*d.y() - 2*n_dot_d*n.y(),
                         2*d.z() - 2*n_dot_d*n.z());
          mat_t sv_to_tv_cov_matrix = vtx.covariance() + jet_tag_vtx->covariance();
          double sigma_f2 = sqrt(ROOT::Math::Similarity(jacobian, sv_to_tv_cov_matrix));
          double miss_dist_value = n_cross_d.Mag();
          double miss_dist_err = sigma_f2 / 2 / miss_dist_value;
          miss_dist = Measurement1D(miss_dist_value, miss_dist_err);
        }

        if (ntracks >= min_tracks_shared && ntracks > best_ntracks[ijet]) {
          second_best_ntracks[ijet] = best_ntracks[ijet];
          best_ntracks[ijet] = ntracks;
          index_by_ntracks[ijet] = ivtx;
        }

        if (ntracks_ptmin >= min_tracks_shared && ntracks_ptmin > best_ntracks_ptmin[ijet]) {
          second_best_ntracks_ptmin[ijet] = best_ntracks_ptmin[ijet];
          best_ntracks_ptmin[ijet] = ntracks_ptmin;
          index_by_ntracks_ptmin[ijet] = ivtx;
        }

        if (sum_nhits >= min_hits_shared && sum_nhits > best_sum_nhits[ijet]) {
          second_best_sum_nhits[ijet] = best_sum_nhits[ijet];
          best_sum_nhits[ijet] = sum_nhits;
          index_by_sum_nhits[ijet] = ivtx;
        }
      
      
        if (fabs(cos_angle - 1) <= max_cos_angle_diff && fabs(cos_angle - 1) < fabs(best_cos_angle[ijet] - 1)) {
          second_best_cos_angle[ijet] = best_cos_angle[ijet];
          best_cos_angle[ijet] = cos_angle;
          index_by_cos_angle[ijet] = ivtx;
        }

        if (miss_dist.value() <= max_miss_dist && miss_dist.significance() <= max_miss_sig && miss_dist.value() < best_miss_dist[ijet].value()) {
          second_best_miss_dist[ijet] = best_miss_dist[ijet];
          best_miss_dist[ijet] = miss_dist;
          index_by_miss_dist[ijet] = ivtx;
        }

        if (histos) {
          h_ntracks->Fill(ntracks);
          h_ntracks_ptmin->Fill(ntracks_ptmin);
          h_sum_nhits->Fill(sum_nhits);
          h_cos_angle->Fill(cos_angle);
          h_miss_dist->Fill(miss_dist.value());
          h_miss_dist_err->Fill(miss_dist.error());
          h_miss_dist_sig->Fill(miss_dist.significance());
          h_miss_dist_err_v->Fill(miss_dist.value(), miss_dist.error());
        }        
      }        

      if (histos) {
        h_best_ntracks->Fill(best_ntracks[ijet]);
        h_best_ntracks_ptmin->Fill(best_ntracks_ptmin[ijet]);
        h_best_sum_nhits->Fill(best_sum_nhits[ijet]);
        h_best_cos_angle->Fill(best_cos_angle[ijet]);
        h_best_miss_dist->Fill(best_miss_dist[ijet].value());
        h_best_miss_dist_err->Fill(best_miss_dist[ijet].error());
        h_best_miss_dist_sig->Fill(best_miss_dist[ijet].significance());
        h_best_miss_dist_err_v->Fill(best_miss_dist[ijet].value(), best_miss_dist[ijet].error());

        h_best_ntracks_v_second->Fill(second_best_ntracks[ijet], best_ntracks[ijet]);
        h_best_ntracks_ptmin_v_second->Fill(second_best_ntracks_ptmin[ijet], best_ntracks_ptmin[ijet]);
        h_best_sum_nhits_v_second->Fill(second_best_sum_nhits[ijet], best_sum_nhits[ijet]);
        h_best_cos_angle_v_second->Fill(second_best_cos_angle[ijet], best_cos_angle[ijet]);
        h_best_miss_dist_v_second->Fill(second_best_miss_dist[ijet].value(), best_miss_dist[ijet].value());
        h_best_miss_dist_err_v_second->Fill(second_best_miss_dist[ijet].error(), best_miss_dist[ijet].error());
        h_best_miss_dist_sig_v_second->Fill(second_best_miss_dist[ijet].significance(), best_miss_dist[ijet].significance());
      }        

      //if (verbose)
      //  printf("ijet %lu pt %f eta %f phi %f  assoc ivtx %i\n", ijet, jet.pt(), jet.eta(), jet.phi(), indices[ijet]);
    }
  }

  std::unique_ptr<Association> assoc[mfv::NJetsBy];
  for (int i = 0; i < mfv::NJetsBy; ++i)
    assoc[i].reset(new Association(&event.productGetter()));

  int n_matchedvertices[mfv::NJetsBy] = {0};
  int n_matchedjets[mfv::NJetsBy] = {0};

  if (enable) {
    for (size_t ivtx = 0; ivtx < n_vertices; ++ivtx) {
      reco::VertexRef vtxref = vertices.at(ivtx);
      int these_n_matchedjets[mfv::NJetsBy] = {0};

      for (size_t ijet = 0; ijet < n_jets; ++ijet) {
        pat::JetRef jetref(jets, ijet);
      
        if (index_by_ntracks[ijet] == int(ivtx)) {
          assoc[mfv::JByNtracks]->insert(vtxref, jetref);
          ++these_n_matchedjets[mfv::JByNtracks];
        }

        if (index_by_ntracks_ptmin[ijet] == int(ivtx)) {
          assoc[mfv::JByNtracksPtmin]->insert(vtxref, jetref);
          ++these_n_matchedjets[mfv::JByNtracksPtmin];
        }

        if (index_by_miss_dist[ijet] == int(ivtx)) {
          assoc[mfv::JByMissDist]->insert(vtxref, jetref);
          ++these_n_matchedjets[mfv::JByMissDist];
        }

        if (index_by_ntracks[ijet] == int(ivtx) || index_by_miss_dist[ijet] == int(ivtx)) {
          assoc[mfv::JByCombination]->insert(vtxref, jetref);
          ++these_n_matchedjets[mfv::JByCombination];
        }

        if (index_by_ntracks_ptmin[ijet] == int(ivtx) || index_by_miss_dist[ijet] == int(ivtx)) {
          assoc[mfv::JByCombinationPtmin]->insert(vtxref, jetref);
          ++these_n_matchedjets[mfv::JByCombinationPtmin];
        }
      }

      for (int i = 0; i < mfv::NJetsBy; ++i) {
        n_matchedjets[i] += these_n_matchedjets[i];
        if (these_n_matchedjets[i] > 0)
          ++n_matchedvertices[i];
      }
    }
  }

  if (histos) {
    for (int i = 0; i < mfv::NJetsBy; ++i) {
      h_n_matchedjets_v_jets        [i]->Fill(n_jets,     n_matchedjets[i]);
      h_n_matchedjets_v_vertices    [i]->Fill(n_vertices, n_matchedjets[i]);
      h_n_matchedvertices_v_jets    [i]->Fill(n_jets,     n_matchedvertices[i]);
      h_n_matchedvertices_v_vertices[i]->Fill(n_vertices, n_matchedvertices[i]);
    }
  }

  for (int i = 0; i < mfv::NJetsBy; ++i)
    event.put(std::move(assoc[i]), mfv::jetsby_names[i]);
}

DEFINE_FWK_MODULE(MFVJetVertexAssociator);
