#include "TFile.h"
#include "TH1.h"
#include "TTree.h"
#include "CLHEP/Random/RandomEngine.h"
#include "CLHEP/Random/RandGauss.h"
#include "DataFormats/GeometryVector/interface/TrackingJacobians.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "FWCore/Utilities/interface/RandomNumberGenerator.h"
#include "TrackingTools/IPTools/interface/IPTools.h"
#include "TrackingTools/Records/interface/TransientTrackRecord.h"
#include "TrackingTools/TransientTrack/interface/TransientTrack.h"
#include "TrackingTools/TransientTrack/interface/TransientTrackBuilder.h"
#include "JMTucker/MFVNeutralino/interface/MiniNtuple.h"
#include "JMTucker/Tools/interface/Utilities.h"

typedef std::tuple<unsigned, unsigned, unsigned long long> RLE;

class MFVOverlayVertexTracks : public edm::EDFilter {
public:
  explicit MFVOverlayVertexTracks(const edm::ParameterSet&);
  ~MFVOverlayVertexTracks();

private:
  virtual bool filter(edm::Event&, const edm::EventSetup&);

  reco::Track copy_track(int i, mfv::MiniNtuple* nt);
  reco::Vertex copy_vertex(mfv::MiniNtuple* nt);
  void update_min_track_vertex_dist(const TransientTrackBuilder& tt_builder, const reco::Track& tk, const reco::Vertex& v,
                                    Measurement1D& min_d, Measurement1D& min_d_sig);

  const std::string minitree_fn;
  const std::string minitree_treepath;
  const std::string sample;
  const int ntracks;
  const int which_event;
  const bool rotate_x;
  const bool rotate_p;
  const std::string z_model_str;
  const int z_model;
  const double z_width;
  const bool rest_of_event;
  const bool only_other_tracks;
  const bool use_prescales;
  const std::string prescales_fn;
  const double prescale_mult;
  const bool verbose;

  enum { z_none, z_deltasv, z_deltapv, z_deltasvgaus };

  std::vector<mfv::MiniNtuple*> minitree_events;
  std::map<RLE, int> event_index;

  TH1D* h_prescales;
};

namespace {
  std::ostream& operator<<(std::ostream& o, const RLE& rle) {
    o << "run " << std::get<0>(rle) << ", lumi " << std::get<1>(rle) << ", event " << std::get<2>(rle);
    return o;
  }
}

MFVOverlayVertexTracks::MFVOverlayVertexTracks(const edm::ParameterSet& cfg) 
  : minitree_fn(cfg.getParameter<std::string>("minitree_fn")),
    minitree_treepath(cfg.getParameter<std::string>("minitree_treepath")),
    sample(cfg.getParameter<std::string>("sample")),
    ntracks(cfg.getParameter<int>("ntracks")),
    which_event(cfg.getParameter<int>("which_event")),
    rotate_x(cfg.getParameter<bool>("rotate_x")),
    rotate_p(cfg.getParameter<bool>("rotate_p")),
    z_model_str(cfg.getParameter<std::string>("z_model")),
    z_model(z_model_str == "none"    ? z_none    :
            z_model_str == "deltasv" ? z_deltasv :
            z_model_str == "deltapv" ? z_deltapv :
            z_model_str == "deltasvgaus" ? z_deltasvgaus :
            -1),
    z_width(cfg.getParameter<double>("z_width")),
    rest_of_event(cfg.getParameter<bool>("rest_of_event")),
    only_other_tracks(cfg.getParameter<bool>("only_other_tracks")),
    use_prescales(cfg.getParameter<bool>("use_prescales")),
    prescales_fn(cfg.getParameter<std::string>("prescales_fn")),
    prescale_mult(cfg.getParameter<double>("prescale_mult")),
    verbose(cfg.getParameter<bool>("verbose")),

    h_prescales(0)
{
  edm::Service<edm::RandomNumberGenerator> rng;
  if (z_model == z_deltasvgaus && !rng.isAvailable())
    throw cms::Exception("MFVOverlayVertexTracks", "RandomNumberGeneratorService not available");

  if (z_model == -1)
    throw cms::Exception("MFVOverlayVertexTracks", "bad z_model: ") << z_model_str;

  TFile* f = TFile::Open(minitree_fn.c_str());
  if (!f || !f->IsOpen())
    throw cms::Exception("MFVOverlayVertexTracks", "bad minitree file: ") << minitree_fn;

  mfv::MiniNtuple nt;
  TTree* t = (TTree*)f->Get(minitree_treepath.c_str());
  if (!t)
    throw cms::Exception("MFVOverlayVertexTracks", "bad tree");

  mfv::read_from_tree(t, nt);

  if (which_event < 0 || which_event >= t->GetEntries())
    throw cms::Exception("MFVOverlayVertexTracks", "bad event: ") << which_event << " tree has " << t->GetEntries();

  if (t->LoadTree(which_event) < 0 || t->GetEntry(which_event) <= 0)
    throw cms::Exception("MFVOverlayVertexTracks", "bad event: ") << which_event << " ; couldn't load it";

  for (int j = 0, je = t->GetEntries(); j < je; ++j) {
    if (t->LoadTree(j) < 0 || t->GetEntry(j) <= 0)
      throw cms::Exception("MFVOverlayVertexTracks", "problem with tree entry") << j;

    if (nt.nvtx == 1) { // don't include 2-vertex events for now
      mfv::MiniNtuple* clnt = mfv::clone(nt);
      minitree_events.push_back(clnt);
      const RLE rle(nt.run, nt.lumi, nt.event);
      const int index = int(minitree_events.size()) - 1;
      event_index[rle] = index;
      
      if (verbose) {
        std::cout << "original event: " << rle << " its pv at " << nt.pvx << ", " << nt.pvy << ", " << nt.pvz << " and sv at " << nt.x0 << ", " << nt.y0 << ", " << nt.z0 << " with " << +nt.ntk0 << " tracks:\n";
        for (int i = 0; i < nt.ntk0; ++i)
          std::cout << "#" << i << " px " << (*nt.p_tk0_px)[i] << " py " << (*nt.p_tk0_py)[i] << "\n";
        std::cout << "storing from minitree " << rle << " with index " << index << " : its pv at " << clnt->pvx << ", " << clnt->pvy << ", " << clnt->pvz << " and sv at " << clnt->x0 << ", " << clnt->y0 << ", " << clnt->z0 << " with " << +clnt->ntk0 << " tracks:\n";
        for (int i = 0; i < clnt->ntk0; ++i)
          std::cout << "#" << i << " px " << clnt->tk0_px[i] << " py " << clnt->tk0_py[i] << "\n";
      }
    }
  }

  f->Close();
  delete f;

  if (use_prescales) {
    TFile* f_prescales = TFile::Open(prescales_fn.c_str());
    if (!f_prescales || !f_prescales->IsOpen())
      throw cms::Exception("MFVOverlayVertexTracks", "bad prescales file");
    TString prescales_path; prescales_path.Form("ntk%i/%s-%s_prescales", ntracks, sample.c_str(), rest_of_event ? "P" : "C");
    if (verbose) std::cout << "getting prescales from " << prescales_fn << "/" << prescales_path << "\n";
    TObject* temp = f_prescales->Get(prescales_path);
    if (!temp) throw cms::Exception("MFVOverlayVertexTracks") << "no " << prescales_path << " in " << prescales_fn;
    h_prescales = (TH1D*)temp->Clone("h_prescales");
    h_prescales->SetDirectory(0);
    f_prescales->Close();
    delete f_prescales;
  }
    
  produces<reco::TrackCollection>();
  produces<std::vector<double>>();
}

MFVOverlayVertexTracks::~MFVOverlayVertexTracks() {
  for (mfv::MiniNtuple* nt : minitree_events)
    delete nt;
  delete h_prescales;
}

reco::Track MFVOverlayVertexTracks::copy_track(int i, mfv::MiniNtuple* nt) {
  return reco::Track(fabs(nt->tk0_qchi2[i]),
                     nt->tk0_ndof[i],
                     reco::TrackBase::Point(nt->tk0_vx[i],
                                            nt->tk0_vy[i],
                                            nt->tk0_vz[i]),
                     reco::TrackBase::Vector(nt->tk0_px[i],
                                             nt->tk0_py[i],
                                             nt->tk0_pz[i]),
                     sgn(nt->tk0_qchi2[i]),
                     nt->tk0_cov[i],
                     reco::TrackBase::TrackAlgorithm(0));
}

reco::Vertex MFVOverlayVertexTracks::copy_vertex(mfv::MiniNtuple* nt) {
  return reco::Vertex(reco::Vertex::Point(nt->x0, nt->y0, nt->z0), reco::Vertex::Error()); // JMTBAD need cov matrix back in minitree
}

void MFVOverlayVertexTracks::update_min_track_vertex_dist(const TransientTrackBuilder& tt_builder, const reco::Track& tk, const reco::Vertex& v,
                                                          Measurement1D& min_d, Measurement1D& min_d_sig) {
  reco::TransientTrack ttk = tt_builder.build(tk);
  std::pair<bool, Measurement1D> x = IPTools::absoluteImpactParameter3D(ttk, v);
  if (!x.first)
    x.second = Measurement1D(1e9, 1e-9);
  if (x.second.value() < min_d.value())
    min_d = x.second;
  if (x.second.significance() < min_d_sig.significance())
    min_d_sig = x.second;
}

bool MFVOverlayVertexTracks::filter(edm::Event& event, const edm::EventSetup& setup) {
  assert(!event.isRealData()); // JMTBAD lots of reasons this dosen't work on data yet, beamspot being the best one

  RLE rle(event.id().run(), event.luminosityBlock(), event.id().event());
  if (event_index.find(rle) == event_index.end()) {
    if (verbose) std::cout << "OverlayTracks rle " << rle << " not found, returning" << std::endl;
    return false;
  }

  const int index = event_index[rle];

  if (verbose) std::cout << "OverlayTracks " << rle << " : index = " << index << " which_event " << which_event << "\n";

  if (index == which_event || (!rest_of_event && index > which_event)) { // don't double count e.g. (3,2) and (2,3) when not using the rest of e0
    if (verbose) std::cout << "  don't double count, returning" << std::endl;
    return false;
  }
    
  mfv::MiniNtuple* nt0 = minitree_events[index];
  mfv::MiniNtuple* nt1 = minitree_events[which_event];
  std::auto_ptr<mfv::MiniNtuple> nt1_0(mfv::clone(*nt1)); // nt1 transformed into the "frame" of nt0

  double deltaz = 0;
  if (z_model == z_deltapv)
    deltaz = nt0->pvz - nt1->pvz;
  else if (z_model == z_deltasv)
    deltaz = nt0->z0 - nt1->z0;
  else if (z_model == z_deltasvgaus) {
    edm::Service<edm::RandomNumberGenerator> rng;
    deltaz = nt0->z0 - nt1->z0 + CLHEP::RandGauss(rng->getEngine(event.streamID())).fire(0., z_width);
  }

  nt1_0->z0 += deltaz;
  for (int i = 0; i < nt1_0->ntk0; ++i)
    nt1_0->tk0_vz[i] += deltaz;

  if (rotate_x || rotate_p) {
    edm::Service<edm::RandomNumberGenerator> rng;
    const double rot_angle = rng->getEngine(event.streamID()).flat() * 2 * M_PI;

    AlgebraicMatrix33 rot3;
    rot3(0,0) = rot3(1,1) = cos(rot_angle);
    rot3(0,1) = -sin(rot_angle);
    rot3(1,0) = sin(rot_angle);
    rot3(2,2) = 1;

    if (rotate_x) {
      AlgebraicVector3 v1_0(nt1_0->x0, nt1_0->y0, nt1_0->z0);
      AlgebraicVector3 rot_v1_0 = rot3 * v1_0;
      assert(0); // vertex covariance for the track-vertex sig stuff
      nt1_0->x0 = rot_v1_0(0);
      nt1_0->y0 = rot_v1_0(1);
      nt1_0->z0 = rot_v1_0(2);
    }

    AlgebraicMatrix66 rot = ROOT::Math::SMatrixIdentity(); // x y z px py pz
    if (rotate_x) rot.Place_at(rot3, 0,0);
    if (rotate_p) rot.Place_at(rot3, 3,3);

    for (int i = 0; i < nt1_0->ntk0; ++i) {
      AlgebraicVector3 pos(nt1_0->tk0_vx[i], nt1_0->tk0_vy[i], nt1_0->tk0_vz[i]);
      AlgebraicVector3 rot_pos = rotate_x ? rot3 * pos : pos;

      AlgebraicVector3 mom(nt1_0->tk0_px[i], nt1_0->tk0_py[i], nt1_0->tk0_pz[i]);
      AlgebraicVector3 rot_mom = rotate_p ? rot3 * mom : mom;

      GlobalVector mom_v(mom(0), mom(1), mom(2));
      AlgebraicMatrix65 jac_curv2cart = jacobianCurvilinearToCartesian(mom_v, sgn(nt1_0->tk0_qchi2[i]));
      AlgebraicSymMatrix66 cart_cov = ROOT::Math::Similarity(jac_curv2cart, nt1_0->tk0_cov[i]);
      AlgebraicSymMatrix66 rot_cart_cov = ROOT::Math::Similarity(rot, cart_cov);

      GlobalVector rot_mom_v(rot_mom(0), rot_mom(1), rot_mom(2));
      AlgebraicMatrix56 jac_cart2curv = jacobianCartesianToCurvilinear(rot_mom_v, sgn(nt1_0->tk0_qchi2[i]));
      AlgebraicSymMatrix55 rot_cov = ROOT::Math::Similarity(jac_cart2curv, rot_cart_cov);

      nt1_0->tk0_vx[i] = rot_pos(0);
      nt1_0->tk0_vy[i] = rot_pos(1);
      nt1_0->tk0_vz[i] = rot_pos(2);
      nt1_0->tk0_px[i] = rot_mom(0);
      nt1_0->tk0_py[i] = rot_mom(1);
      nt1_0->tk0_pz[i] = rot_mom(2);
      nt1_0->tk0_cov[i] = rot_cov;
    }
  }

  if (verbose) std::cout << "ntk0 " << std::setw(2) << +nt0->ntk0 << " v0 " << nt0->x0 << ", " << nt0->y0 << ", " << nt0->z0 << "\n"
                         << "ntk1 " << std::setw(2) << +nt1->ntk0 << " v1 " << nt1->x0 << ", " << nt1->y0 << ", " << nt1->z0 << "\n"
                         << "       " << " v1_0 " << nt1_0->x0 << ", " << nt1_0->y0 << ", " << nt1_0->z0 << "\n";

  if (use_prescales) {
    const double dvv_true = mag(nt0->x0 - nt1_0->x0, nt0->y0 - nt1_0->y0);
    const double prescale = h_prescales->GetBinContent(h_prescales->FindBin(dvv_true));
    const double final_prescale = prescale_mult * prescale;
    if (verbose) std::cout << "using prescales: dvv true = " << dvv_true << ", prescale " << prescale << " mult " << prescale_mult << " final prescale " << final_prescale << "\n";
    if (prescale > 1) {
      edm::Service<edm::RandomNumberGenerator> rng;
      const double u = rng->getEngine(event.streamID()).flat();
      const bool killed = u > 1/final_prescale;
      if (verbose) std::cout << "  draw " << u << " killed? " << killed << "\n";
      if (killed)
        return false;
    }
  }

  std::auto_ptr<std::vector<double>> truth(new std::vector<double>(13)); // ntk0, x0, y0, z0, ntk1, x1, y1, z1, x1_0, y1_0, z1_0, min_track_vertex_dist, min_track_vertex_sig
  // rest of truth is (ntk0 + ntk1) * 3 : px, py, pz, ... tracks for v1_0

  (*truth)[0]  = nt0->ntk0;
  (*truth)[1]  = nt0->x0;
  (*truth)[2]  = nt0->y0;
  (*truth)[3]  = nt0->z0;
  (*truth)[4]  = nt1->ntk0;
  (*truth)[5]  = nt1->x0;
  (*truth)[6]  = nt1->y0;
  (*truth)[7]  = nt1->z0;
  (*truth)[8]  = nt1_0->x0;
  (*truth)[9]  = nt1_0->y0;
  (*truth)[10] = nt1_0->z0;

  for (int i = 0; i < nt0->ntk0; ++i) {
    if (verbose) std::cout << "v0 tk" << i << ": " << nt0->tk0_px[i] << ", " << nt0->tk0_py[i] << ", " << nt0->tk0_pz[i] << "\n";
    truth->push_back(nt0->tk0_px[i]);
    truth->push_back(nt0->tk0_py[i]);
    truth->push_back(nt0->tk0_pz[i]);
  }

  for (int i = 0; i < nt1->ntk0; ++i) {
    if (verbose) std::cout << "v1 tk" << i << ": " << nt1_0->tk0_px[i] << ", " << nt1_0->tk0_py[i] << ", " << nt1_0->tk0_pz[i] << "\n";
    truth->push_back(nt1_0->tk0_px[i]);
    truth->push_back(nt1_0->tk0_py[i]);
    truth->push_back(nt1_0->tk0_pz[i]);
  }

  reco::Vertex v0 = copy_vertex(nt0);
  //reco::Vertex v1 = copy_vertex(nt1);
  reco::Vertex v1_0 = copy_vertex(nt1_0.get());

  edm::ESHandle<TransientTrackBuilder> tt_builder;
  setup.get<TransientTrackRecord>().get("TransientTrackBuilder", tt_builder);

  Measurement1D min_d(1e9, 1e-9), min_d_sig(1e9, 1e-9);

  std::auto_ptr<reco::TrackCollection> output_tracks(new reco::TrackCollection);

  if (!only_other_tracks)
    for (int i = 0; i < nt0->ntk0; ++i) {
      output_tracks->push_back(copy_track(i, nt0));
      update_min_track_vertex_dist(*tt_builder, output_tracks->back(), v1_0, min_d, min_d_sig);
    }

  for (int i = 0; i < nt1_0->ntk0; ++i) {
    output_tracks->push_back(copy_track(i, nt1_0.get()));
    update_min_track_vertex_dist(*tt_builder, output_tracks->back(), v0, min_d, min_d_sig);
  }

  (*truth)[11] = min_d.value();
  (*truth)[12] = min_d_sig.significance();

  event.put(output_tracks);
  event.put(truth);

  return true;
}

DEFINE_FWK_MODULE(MFVOverlayVertexTracks);
