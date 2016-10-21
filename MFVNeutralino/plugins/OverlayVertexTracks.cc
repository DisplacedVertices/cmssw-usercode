#include "TFile.h"
#include "TTree.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "JMTucker/MFVNeutralino/interface/MiniNtuple.h"

typedef std::tuple<unsigned, unsigned, unsigned long long> RLE;

class MFVOverlayVertexTracks : public edm::EDProducer {
public:
  explicit MFVOverlayVertexTracks(const edm::ParameterSet&);
  ~MFVOverlayVertexTracks();

private:
  virtual void produce(edm::Event&, const edm::EventSetup&);

  reco::Track copy_track(int i, mfv::MiniNtuple* nt);

  const std::string minitree_fn;
  const int which_event;
  const bool only_other_tracks;
  const bool verbose;

  std::vector<mfv::MiniNtuple*> minitree_events;
  std::map<RLE, int> event_index;
};

namespace {
  std::ostream& operator<<(std::ostream& o, const RLE& rle) {
    o << "run " << std::get<0>(rle) << ", lumi " << std::get<1>(rle) << ", event " << std::get<2>(rle);
    return o;
  }
}

MFVOverlayVertexTracks::MFVOverlayVertexTracks(const edm::ParameterSet& cfg) 
  : minitree_fn(cfg.getParameter<std::string>("minitree_fn")),
    which_event(cfg.getParameter<int>("which_event")),
    only_other_tracks(cfg.getParameter<bool>("only_other_tracks")),
    verbose(cfg.getParameter<bool>("verbose"))
{
  TFile* f = TFile::Open(minitree_fn.c_str());
  if (!f || !f->IsOpen())
    throw cms::Exception("MFVOverlayVertexTracks", "bad minitree file: ") << minitree_fn;

  mfv::MiniNtuple nt;
  TTree* t = (TTree*)f->Get("mfvMiniTree/t");
  if (!t)
    throw cms::Exception("MFVOverlayVertexTracks", "bad tree");

  mfv::read_from_tree(t, nt);

  if (which_event < 0 || which_event >= t->GetEntries() - 1) // -1 because we skip the event corresponding to the current event
    throw cms::Exception("MFVOverlayVertexTracks", "bad event: ") << which_event << " tree has " << t->GetEntries();

  if (t->LoadTree(which_event) < 0 || t->GetEntry(which_event) <= 0)
    throw cms::Exception("MFVOverlayVertexTracks", "bad event: ") << which_event << " ; couldn't load it";

  for (int j = 0, je = t->GetEntries(); j < je; ++j) {
    if (t->LoadTree(j) < 0 || t->GetEntry(j) <= 0)
      throw cms::Exception("MFVOverlayVertexTracks", "problem with tree");

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

  produces<reco::TrackCollection>();
  produces<std::vector<double>>();
}

MFVOverlayVertexTracks::~MFVOverlayVertexTracks() {
  for (mfv::MiniNtuple* nt : minitree_events)
    delete nt;
}

namespace {
  template <typename T>
  int sgn(T val) {
    return (T(0) < val) - (val < T(0));
  }
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

void MFVOverlayVertexTracks::produce(edm::Event& event, const edm::EventSetup&) {
  assert(!event.isRealData()); // JMTBAD lots of reasons this dosen't work on data yet

  std::auto_ptr<reco::TrackCollection> output_tracks(new reco::TrackCollection);
  std::auto_ptr<std::vector<double>> truth(new std::vector<double>(11)); // ntk0, x0, y0, z0, ntk1, x1, y1, z1, x1_0, y1_0, z1_0

  RLE rle(event.id().run(), event.luminosityBlock(), event.id().event());
  const int index = event_index[rle];
  const int which_event_offset = index <= which_event ? which_event+1 : which_event;
  if (verbose) std::cout << "OverlayTracks " << rle << " : index = " << index << " which_event " << which_event << " which_event_offset " << which_event_offset << "\n";
    
  mfv::MiniNtuple* nt0 = minitree_events[index];
  mfv::MiniNtuple* nt1 = minitree_events[which_event_offset];
  mfv::MiniNtuple* nt1_0 = mfv::clone(*nt1); // nt1 transformed into the "frame" of nt0

  const double deltaz = nt0->pvz - nt1->pvz;
  nt1_0->z0 += deltaz;
  for (int i = 0; i < nt1_0->ntk0; ++i)
    nt1_0->tk0_vz[i] += deltaz;

  if (verbose) std::cout << "ntk0 " << std::setw(2) << +nt0->ntk0 << " v0 " << nt0->x0 << ", " << nt0->y0 << ", " << nt0->z0 << "\n"
                         << "ntk1 " << std::setw(2) << +nt1->ntk0 << " v1 " << nt1->x0 << ", " << nt1->y0 << ", " << nt1->z0 << "\n"
                         << "       " << " v1_0 " << nt1_0->x0 << ", " << nt1_0->y0 << ", " << nt1_0->z0 << std::endl;

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

  if (!only_other_tracks)
    for (int i = 0; i < nt0->ntk0; ++i)
      output_tracks->push_back(copy_track(i, nt0));

  for (int i = 0; i < nt1_0->ntk0; ++i)
    output_tracks->push_back(copy_track(i, nt1_0));

  delete nt1_0;

  event.put(output_tracks);
  event.put(truth);
}

DEFINE_FWK_MODULE(MFVOverlayVertexTracks);
