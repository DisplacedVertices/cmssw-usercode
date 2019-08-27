#include "TTree.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "JMTucker/MFVNeutralino/interface/Ntuple.h"
#include "JMTucker/MFVNeutralino/interface/NtupleFiller.h"
#include "JMTucker/MFVNeutralinoFormats/interface/VertexAux.h"
#include "JMTucker/Tools/interface/ExtValue.h"
#include "JMTucker/Tools/interface/Utilities.h"

class MFVMiniTreer2 : public edm::EDAnalyzer {
public:
  explicit MFVMiniTreer2(const edm::ParameterSet&);
  void analyze(const edm::Event&, const edm::EventSetup&);

  jmt::BaseSubNtupleFiller base_filler;
  jmt::BeamspotSubNtupleFiller bs_filler;
  jmt::PrimaryVerticesSubNtupleFiller pvs_filler;
  jmt::JetsSubNtupleFiller jets_filler;
  jmt::TracksSubNtupleFiller tracks_filler;
  mfv::GenTruthSubNtupleFiller gentruth_filler;
  const edm::EDGetTokenT<MFVVertexAuxCollection> vertices_token;

  mfv::MiniNtuple2 nt;
  TTree* tree;
};

MFVMiniTreer2::MFVMiniTreer2(const edm::ParameterSet& cfg)
  : base_filler(nt.base(), cfg, consumesCollector()),
    bs_filler(nt.bs(), cfg, consumesCollector()),
    pvs_filler(nt.pvs(), cfg, consumesCollector(), true, false),
    jets_filler(nt.jets(), cfg, consumesCollector()),
    tracks_filler(nt.tracks(), cfg, consumesCollector(), 2),
    gentruth_filler(nt.gentruth(), cfg, consumesCollector()),
    vertices_token(consumes<MFVVertexAuxCollection>(cfg.getParameter<edm::InputTag>("vertices_src")))
{
  edm::Service<TFileService> fs;
  tree = fs->make<TTree>("t", "");
  nt.write_to_tree(tree);
}

namespace { double mag2(double x, double y, double z) { return x*x + y*y + z*z; } }

void MFVMiniTreer2::analyze(const edm::Event& event, const edm::EventSetup&) {
  edm::Handle<MFVVertexAuxCollection> vertices;
  event.getByToken(vertices_token, vertices);

  if (vertices->empty())
    return;

  nt.clear();

  base_filler(event);
  bs_filler(event);
  pvs_filler(event, &bs_filler.bs());
  jets_filler(event);
  tracks_filler(event, &jets_filler, &pvs_filler, &bs_filler);
  gentruth_filler(event);

  int n3 = 0, n7 = 0, n4 = 0, n5 = 0;

  for (const auto& v : *vertices) {
    mfv::NtupleAdd(nt.vertices(), v, nt.gentruth().lspmatch(v));

    if      (v.ntracks() == 3) ++n3, ++n7;
    else if (v.ntracks() == 4) ++n4, ++n7;
    else if (v.ntracks() >= 5) ++n5;

    for (size_t i = 0, ie = v.ntracks(); i < ie; ++i) {
      jmt::MinValue mindist2(0.1);
      for (size_t j = 0, je = nt.tracks().n(); j < je; ++j)
        mindist2(j, mag2(v.track_qpt(i) - nt.tracks().qpt(j),
                         v.track_eta[i] - nt.tracks().eta(j),
                         v.track_phi[i] - nt.tracks().phi(j)));

      if (mindist2.i() == -1) {
        cms::Exception ce("BadAssumption");
        ce << "vertex w " << v.ntracks() << " tracks @ <" << v.x << ", " << v.y << ", " << v.z << ">: track " << i << " <" << v.track_qpt(i) << ", " << v.track_eta[i] << ", " << v.track_phi[i] << "> not found in " << nt.tracks().n() << " tracks in general collection:\n";
        for (size_t j = 0, je = nt.tracks().n(); j < je; ++j)
          ce << j << ": <" << nt.tracks().qpt(j) << ", " << nt.tracks().eta(j) << ", " << nt.tracks().phi(j) << ">\n";
        //std::cout << ce <<"\n";
        throw ce;
      }

      assert(nt.tracks().which_sv(mindist2.i()) == 255);
      const size_t iv = nt.vertices().n() - 1;
      assert(iv < 255);
      nt.tracks().set_which_sv(mindist2.i(), iv);
    }
  }

  nt.event().set(mfv::MiniNtuple2SubNtuple::vcode(n3, n7, n4, n5));
  // trim tracks/jets?

  tree->Fill();
}

DEFINE_FWK_MODULE(MFVMiniTreer2);
