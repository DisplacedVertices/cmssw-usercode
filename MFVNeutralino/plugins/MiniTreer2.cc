#include "RecoVertex/KalmanVertexFit/interface/KalmanVertexFitter.h"
#include "TrackingTools/Records/interface/TransientTrackRecord.h"
#include "TrackingTools/TransientTrack/interface/TransientTrack.h"
#include "TrackingTools/TransientTrack/interface/TransientTrackBuilder.h"
#include "JMTucker/MFVNeutralino/interface/NtupleFiller.h"
#include "JMTucker/MFVNeutralino/interface/VertexerParams.h"
#include "JMTucker/MFVNeutralinoFormats/interface/VertexAux.h"
#include "JMTucker/Tools/interface/AnalysisEras.h"
#include "JMTucker/Tools/interface/ExtValue.h"
#include "JMTucker/Tools/interface/Math.h"
#include "JMTucker/Tools/interface/TrackRescaler.h"

class MFVMiniTreer2 : public edm::EDAnalyzer {
public:
  explicit MFVMiniTreer2(const edm::ParameterSet&);
  void analyze(const edm::Event&, const edm::EventSetup&);

  mfv::MiniNtuple2 nt;
  jmt::TrackingAndJetsNtupleFiller nt_filler; // JMTBAD MiniNtuple2Filler
  mfv::GenTruthSubNtupleFiller gentruth_filler;

  const edm::EDGetTokenT<reco::VertexCollection> vertices_token;
  const edm::EDGetTokenT<MFVVertexAuxCollection> auxes_token;
  jmt::TrackRescaler track_rescaler;
  std::unique_ptr<KalmanVertexFitter> kv_reco;
  enum { vertex_sel_none, vertex_sel_loose, vertex_sel_tight };
  const std::string vertex_sel_s;
  const int vertex_sel;
};

MFVMiniTreer2::MFVMiniTreer2(const edm::ParameterSet& cfg)
  : nt_filler(nt, cfg, NF_CC_TrackingAndJets_v,
              jmt::TrackingAndJetsNtupleFillerParams()
                .pvs_subtract_bs(true) // JMTBAD get rid of this everywhere
                .tracks_cut_level(2)),
    gentruth_filler(nt.gentruth(), cfg, consumesCollector()),
    vertices_token(consumes<reco::VertexCollection>(cfg.getParameter<edm::InputTag>("vertices_src"))),
    auxes_token(consumes<MFVVertexAuxCollection>(cfg.getParameter<edm::InputTag>("auxes_src"))),
    kv_reco(new KalmanVertexFitter(cfg.getParameter<edm::ParameterSet>("kvr_params"), cfg.getParameter<edm::ParameterSet>("kvr_params").getParameter<bool>("doSmoothing"))),
    vertex_sel_s(cfg.getParameter<std::string>("vertex_sel")),
    vertex_sel(vertex_sel_s == "loose" ? vertex_sel_loose :
            vertex_sel_s == "tight" ? vertex_sel_tight : vertex_sel_none)
{}

void MFVMiniTreer2::analyze(const edm::Event& event, const edm::EventSetup& setup) {
  nt_filler.fill(event);
  gentruth_filler(event);

  const int track_rescaler_which = 0; // JMTBAD which rescaling if ever a different one
  track_rescaler.setup(!event.isRealData() && track_rescaler_which != -1,
                       jmt::AnalysisEras::pick(event, this),
                       track_rescaler_which);

  edm::ESHandle<TransientTrackBuilder> tt_builder;
  setup.get<TransientTrackRecord>().get("TransientTrackBuilder", tt_builder);

  //////////////////////////////////////////////////////////////////////

  edm::Handle<reco::VertexCollection> vertices;
  event.getByToken(vertices_token, vertices);

  std::vector<size_t> indices(vertices->size());
  std::iota(indices.begin(), indices.end(), 0);
  auto vertices_sorter = [&vertices](size_t i1, size_t i2) {
    auto w = mfv::track_vertex_weight_min;
    auto mtk = 0.13957018f;
    auto v1 = (*vertices)[i1]; int n1 = v1.nTracks(w); double m1 = v1.p4(mtk, w).mass();
    auto v2 = (*vertices)[i2]; int n2 = v2.nTracks(w); double m2 = v2.p4(mtk, w).mass();
    if (n1 == n2) return m1 > m2;
    return n1 > n2;
  };
  std::sort(indices.begin(), indices.end(), vertices_sorter);

  edm::Handle<MFVVertexAuxCollection> auxes;
  event.getByToken(auxes_token, auxes);

  //////////////////////////////////////////////////////////////////////

  int ngt3loose = 0, n3 = 0, n7 = 0, n4 = 0, n5 = 0;

  for (size_t i : indices) { // JMTBAD SubFiller for this?
    const reco::Vertex& v = (*vertices)[i];
    const int ntracks = v.nTracks(mfv::track_vertex_weight_min);

    // rescaled track fit
    std::vector<reco::TransientTrack> /*ttks,*/ rs_ttks;
    for (auto it = v.tracks_begin(), ite = v.tracks_end(); it != ite; ++it)
      if (v.trackWeight(*it) >= mfv::track_vertex_weight_min)
        rs_ttks.push_back(tt_builder->build(track_rescaler.scale(**it).rescaled_tk));
    assert(rs_ttks.size() > 1);
    const reco::Vertex rescale_v(TransientVertex(kv_reco->vertex(rs_ttks)));

    // temporary
    jmt::MinValue m(0.1);
    for (size_t j = 0, je = auxes->size(); j < je; ++j)
      m(j, jmt::mag2(v.x() - (*auxes)[j].x, v.y() - (*auxes)[j].y, v.z() - (*auxes)[j].z));
    assert(m.i() != -1);
    const MFVVertexAux& a = (*auxes)[m.i()];

    ////

    mfv::NtupleAdd(nt.vertices(), v, rescale_v, a, nt.gentruth().lspmatch(a)); // JMTBAD lspmatch method
    const size_t iv = nt.vertices().n() - 1;
    assert(a.ntracks() == ntracks);
    assert(iv < 255); // JMTBAD not really needed, just the max the current jet/track assoc uchars can handle

    ////

    for (auto it = v.tracks_begin(), ite = v.tracks_end(); it != ite; ++it)
      if (v.trackWeight(*it) >= mfv::track_vertex_weight_min) {
        const reco::Track& tk = **it;
        jmt::MinValue m(0.1);
        for (size_t j = 0, je = nt.tracks().n(); j < je; ++j)
          m(j, jmt::mag2(tk.charge() * tk.pt() - nt.tracks().qpt(j),
                         tk.eta() - nt.tracks().eta(j),
                         tk.phi() - nt.tracks().phi(j)));

        if (m.i() == -1) {
          cms::Exception ce("BadAssumption");
          ce << "vertex w " << v.nTracks(mfv::track_vertex_weight_min) << " tracks @ <" << v.x() << ", " << v.y() << ", " << v.z() << ">: track <" << tk.charge()*tk.pt() << ", " << tk.eta() << ", " << tk.phi() << "> not found in " << nt.tracks().n() << " tracks in general collection:\n";
          for (size_t j = 0, je = nt.tracks().n(); j < je; ++j)
            ce << j << ": <" << nt.tracks().qpt(j) << ", " << nt.tracks().eta(j) << ", " << nt.tracks().phi(j) << ">\n";
          //std::cout << ce <<"\n";
          throw ce;
        }

        assert(nt.tracks().which_sv(m.i()) == 255);
        nt.tracks().set_which_sv(m.i(), iv);
      }

    if (nt.vertices().pass(iv, nt.bs())) {
      if      (ntracks == 3) ++n3, ++n7;
      else if (ntracks == 4) ++n4, ++n7;
      else if (ntracks >= 5) ++n5;
    }

    if (nt.vertices().pass(iv, nt.bs(),
                           3, -1, // ntracks >= 3
                           mfv::VertexNm1s::nm1_beampipe, // keep ones outside beampipe
                           0.005, 0.05)) // dbv> and edbv<
      ++ngt3loose;
  }

  nt.event().set(mfv::MiniNtuple2SubNtuple::vcode(n3, n7, n4, n5));

  if (vertex_sel == vertex_sel_none ||
      (vertex_sel == vertex_sel_loose && ngt3loose > 0) ||
      (vertex_sel == vertex_sel_tight && n5 > 0))
    nt_filler.finalize();
}

DEFINE_FWK_MODULE(MFVMiniTreer2);
