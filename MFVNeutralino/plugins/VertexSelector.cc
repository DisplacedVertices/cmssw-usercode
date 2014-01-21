#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "JMTucker/MFVNeutralinoFormats/interface/VertexAux.h"
#include "JMTucker/MFVNeutralino/interface/VertexTools.h"
#include "JMTucker/MFVNeutralino/plugins/VertexMVAWrap.h"

class MFVVertexSelector : public edm::EDProducer {
public:
  explicit MFVVertexSelector(const edm::ParameterSet&);
  ~MFVVertexSelector() { delete mva; }

private:
  virtual void produce(edm::Event&, const edm::EventSetup&);

  bool use_vertex(const MFVVertexAux& vtx) const;

  const edm::InputTag vertex_src;
  const edm::InputTag vertex_aux_src;
  const bool produce_vertices;
  const bool produce_refs;
  const MFVVertexAuxSorter sorter;

  const bool use_mva;
  const MFVVertexMVAWrap* mva;
  const double mva_cut;

  const int min_ntracks;
  const int min_ntracksptgt3;
  const int min_ntracksptgt5;
  const int min_ntracksptgt10;
  const int min_njetsntks;
  const int max_njetsntks;
  const double max_chi2dof;
  const double min_tkonlypt;
  const double max_abstkonlyeta;
  const double min_tkonlymass;
  const double min_jetsntkpt;
  const double max_absjetsntketa;
  const double min_jetsntkmass;
  const double min_tksjetsntkpt;
  const double max_abstksjetsntketa;
  const double min_tksjetsntkmass;
  const double min_costhtkonlymombs;
  const double min_costhjetsntkmombs;
  const double min_costhtksjetsntkmombs;
  const double min_missdisttkonlypvsig;
  const double min_missdistjetsntkpvsig;
  const double min_missdisttksjetsntkpvsig;
  const double min_sumpt2;
  const double min_maxtrackpt;
  const double min_maxm1trackpt;
  const double min_maxm2trackpt;
  const double max_trackdxyerrmin;
  const double max_trackdzerrmin;
  const double min_drmin;
  const double max_drmin;
  const double min_drmax;
  const double max_drmax;
  const double max_jetpairdrmin;
  const double max_jetpairdrmax;
  const double max_err2d;
  const double max_err3d;
  const double min_gen3dsig;
  const double max_gen3dsig;
  const double min_bs2ddist;
  const double max_bs2derr;
  const double min_bs2dsig;
  const double min_bs3ddist;
};

MFVVertexSelector::MFVVertexSelector(const edm::ParameterSet& cfg) 
  : vertex_src(cfg.getParameter<edm::InputTag>("vertex_src")),
    vertex_aux_src(cfg.getParameter<edm::InputTag>("vertex_aux_src")),
    produce_vertices(cfg.getParameter<bool>("produce_vertices")),
    produce_refs(cfg.getParameter<bool>("produce_refs")),
    sorter(cfg.getParameter<std::string>("sort_by")),
    use_mva(cfg.getParameter<bool>("use_mva")),
    mva(use_mva ? new MFVVertexMVAWrap : 0),
    mva_cut(cfg.getParameter<double>("mva_cut")),
    min_ntracks(cfg.getParameter<int>("min_ntracks")),
    min_ntracksptgt3(cfg.getParameter<int>("min_ntracksptgt3")),
    min_ntracksptgt5(cfg.getParameter<int>("min_ntracksptgt5")),
    min_ntracksptgt10(cfg.getParameter<int>("min_ntracksptgt10")),
    min_njetsntks(cfg.getParameter<int>("min_njetsntks")),
    max_njetsntks(cfg.getParameter<int>("max_njetsntks")),
    max_chi2dof(cfg.getParameter<double>("max_chi2dof")),
    min_tkonlypt(cfg.getParameter<double>("min_tkonlypt")),
    max_abstkonlyeta(cfg.getParameter<double>("max_abstkonlyeta")),
    min_tkonlymass(cfg.getParameter<double>("min_tkonlymass")),
    min_jetsntkpt(cfg.getParameter<double>("min_jetsntkpt")),
    max_absjetsntketa(cfg.getParameter<double>("max_absjetsntketa")),
    min_jetsntkmass(cfg.getParameter<double>("min_jetsntkmass")),
    min_tksjetsntkpt(cfg.getParameter<double>("min_tksjetsntkpt")),
    max_abstksjetsntketa(cfg.getParameter<double>("max_abstksjetsntketa")),
    min_tksjetsntkmass(cfg.getParameter<double>("min_tksjetsntkmass")),
    min_costhtkonlymombs(cfg.getParameter<double>("min_costhtkonlymombs")),
    min_costhjetsntkmombs(cfg.getParameter<double>("min_costhjetsntkmombs")),
    min_costhtksjetsntkmombs(cfg.getParameter<double>("min_costhtksjetsntkmombs")),
    min_missdisttkonlypvsig(cfg.getParameter<double>("min_missdisttkonlypvsig")),
    min_missdistjetsntkpvsig(cfg.getParameter<double>("min_missdistjetsntkpvsig")),
    min_missdisttksjetsntkpvsig(cfg.getParameter<double>("min_missdisttksjetsntkpvsig")),
    min_sumpt2(cfg.getParameter<double>("min_sumpt2")),
    min_maxtrackpt(cfg.getParameter<double>("min_maxtrackpt")),
    min_maxm1trackpt(cfg.getParameter<double>("min_maxm1trackpt")),
    min_maxm2trackpt(cfg.getParameter<double>("min_maxm2trackpt")),
    max_trackdxyerrmin(cfg.getParameter<double>("max_trackdxyerrmin")),
    max_trackdzerrmin(cfg.getParameter<double>("max_trackdzerrmin")),
    min_drmin(cfg.getParameter<double>("min_drmin")),
    max_drmin(cfg.getParameter<double>("max_drmin")),
    min_drmax(cfg.getParameter<double>("min_drmax")),
    max_drmax(cfg.getParameter<double>("max_drmax")),
    max_jetpairdrmin(cfg.getParameter<double>("max_jetpairdrmin")),
    max_jetpairdrmax(cfg.getParameter<double>("max_jetpairdrmax")),
    max_err2d(cfg.getParameter<double>("max_err2d")),
    max_err3d(cfg.getParameter<double>("max_err3d")),
    min_gen3dsig(cfg.getParameter<double>("min_gen3dsig")),
    max_gen3dsig(cfg.getParameter<double>("max_gen3dsig")),
    min_bs2ddist(cfg.getParameter<double>("min_bs2ddist")),
    max_bs2derr(cfg.getParameter<double>("max_bs2derr")),
    min_bs2dsig(cfg.getParameter<double>("min_bs2dsig")),
    min_bs3ddist(cfg.getParameter<double>("min_bs3ddist"))
{
  if (produce_refs)
    produces<reco::VertexRefVector>();
  else
    produces<reco::VertexCollection>();
  produces<MFVVertexAuxCollection>();
}

bool MFVVertexSelector::use_vertex(const MFVVertexAux& vtx) const {
  if (use_mva) {
    if (vtx.ntracks < 5)
      return false;

    return mva->value(vtx) > mva_cut;
  }

  return 
    vtx.ntracks >= min_ntracks &&
    vtx.ntracksptgt3 >= min_ntracksptgt3 &&
    vtx.ntracksptgt5 >= min_ntracksptgt5 &&
    vtx.ntracksptgt10 >= min_ntracksptgt10 &&
    vtx.njets[mfv::JByNtracks] >= min_njetsntks &&
    vtx.njets[mfv::JByNtracks] <= max_njetsntks &&
    vtx.chi2/vtx.ndof < max_chi2dof &&
    vtx.pt[mfv::PTracksOnly] >= min_tkonlypt &&
    fabs(vtx.eta[mfv::PTracksOnly]) < max_abstkonlyeta &&
    vtx.mass[mfv::PTracksOnly] >= min_tkonlymass &&
    vtx.pt[mfv::PJetsByNtracks] >= min_jetsntkpt &&
    fabs(vtx.eta[mfv::PJetsByNtracks]) < max_absjetsntketa &&
    vtx.mass[mfv::PJetsByNtracks] >= min_jetsntkmass &&
    vtx.pt[mfv::PTracksPlusJetsByNtracks] >= min_tksjetsntkpt &&
    fabs(vtx.eta[mfv::PTracksPlusJetsByNtracks]) < max_abstksjetsntketa &&
    vtx.mass[mfv::PTracksPlusJetsByNtracks] >= min_tksjetsntkmass &&
    vtx.costhmombs[mfv::PTracksOnly] >= min_costhtkonlymombs &&
    vtx.costhmombs[mfv::PJetsByNtracks] >= min_costhjetsntkmombs &&
    vtx.costhmombs[mfv::PTracksPlusJetsByNtracks] >= min_costhtksjetsntkmombs &&
    vtx.missdistpvsig(mfv::PTracksOnly) >= min_missdisttkonlypvsig &&
    vtx.missdistpvsig(mfv::PJetsByNtracks) >= min_missdistjetsntkpvsig &&
    vtx.missdistpvsig(mfv::PTracksPlusJetsByNtracks) >= min_missdisttksjetsntkpvsig &&
    vtx.sumpt2 >= min_sumpt2 &&
    vtx.maxtrackpt >= min_maxtrackpt &&
    vtx.maxm1trackpt >= min_maxm1trackpt &&
    vtx.maxm2trackpt >= min_maxm2trackpt &&
    vtx.trackdxyerrmin < max_trackdxyerrmin &&
    vtx.trackdzerrmin < max_trackdzerrmin &&
    vtx.drmin >= min_drmin &&
    vtx.drmin <  max_drmin &&
    vtx.drmax >= min_drmax &&
    vtx.drmax <  max_drmax &&
    (max_jetpairdrmin > 1e6 || vtx.jetpairdrmin < max_jetpairdrmin) &&
    vtx.jetpairdrmax < max_jetpairdrmax &&
    vtx.gen2derr < max_err2d &&
    vtx.gen3derr < max_err3d &&
    vtx.gen3dsig() >= min_gen3dsig &&
    vtx.gen3dsig() <  max_gen3dsig &&
    vtx.bs2ddist >= min_bs2ddist &&
    vtx.bs2derr < max_bs2derr &&
    vtx.bs2dsig() >= min_bs2dsig &&
    vtx.bs3ddist >= min_bs3ddist;
}

void MFVVertexSelector::produce(edm::Event& event, const edm::EventSetup&) {
  edm::Handle<reco::VertexCollection> vertices;
  event.getByLabel(vertex_src, vertices);

  edm::Handle<MFVVertexAuxCollection> auxes;
  event.getByLabel(vertex_aux_src, auxes);

  std::auto_ptr<MFVVertexAuxCollection> selected(new MFVVertexAuxCollection);

  for (const MFVVertexAux& aux : *auxes)
    if (use_vertex(aux))
      selected->push_back(aux);

  sorter.sort(*selected);


  if (produce_vertices || produce_refs) {
    std::auto_ptr<reco::VertexRefVector> selected_vertex_refs(new reco::VertexRefVector);
    for (const MFVVertexAux& aux : *selected)
      selected_vertex_refs->push_back(reco::VertexRef(vertices, aux.which));

    if (produce_vertices) {
      std::auto_ptr<reco::VertexCollection> selected_vertices(new reco::VertexCollection);
      for (const reco::VertexRef& v : *selected_vertex_refs)
        selected_vertices->push_back(*v);
      event.put(selected_vertices);
    }
    else
      event.put(selected_vertex_refs);
  }

  event.put(selected);
}

DEFINE_FWK_MODULE(MFVVertexSelector);
