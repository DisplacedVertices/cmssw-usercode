#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/Electron.h"

class MFVAnalysisCuts : public edm::EDFilter {
public:
  explicit MFVAnalysisCuts(const edm::ParameterSet&);

private:
  virtual bool filter(edm::Event&, const edm::EventSetup&);

  const edm::InputTag jet_src;
  const double min_jet_pt;
  const double min_4th_jet_pt;
  const double min_5th_jet_pt;
  const double min_6th_jet_pt;
  const int min_njets;
  const int max_njets;
  const int min_nbtags;
  const double min_sum_ht;

  const std::string b_discriminator_name;
  const double bdisc_min;
  const edm::InputTag muon_src;
  const edm::InputTag electron_src;
  const int min_nleptons;

  const edm::InputTag vertex_src;
  const int min_nvertex;
  const int min_ntracks01;
  const double min_maxtrackpt01;
};

MFVAnalysisCuts::MFVAnalysisCuts(const edm::ParameterSet& cfg) 
  : jet_src(cfg.getParameter<edm::InputTag>("jet_src")),
    min_jet_pt(cfg.getParameter<double>("min_jet_pt")),
    min_4th_jet_pt(cfg.getParameter<double>("min_4th_jet_pt")),
    min_5th_jet_pt(cfg.getParameter<double>("min_5th_jet_pt")),
    min_6th_jet_pt(cfg.getParameter<double>("min_6th_jet_pt")),
    min_njets(cfg.getParameter<int>("min_njets")),
    max_njets(cfg.getParameter<int>("max_njets")),
    min_nbtags(cfg.getParameter<int>("min_nbtags")),
    min_sum_ht(cfg.getParameter<double>("min_sum_ht")),

    b_discriminator_name(cfg.getParameter<std::string>("b_discriminator_name")),
    bdisc_min(cfg.getParameter<double>("bdisc_min")),
    muon_src(cfg.getParameter<edm::InputTag>("muon_src")),
    electron_src(cfg.getParameter<edm::InputTag>("electron_src")),
    min_nleptons(cfg.getParameter<int>("min_nleptons")),

    vertex_src(cfg.getParameter<edm::InputTag>("vertex_src")),
    min_nvertex(cfg.getParameter<int>("min_nvertex")),
    min_ntracks01(cfg.getParameter<int>("min_ntracks01")),
    min_maxtrackpt01(cfg.getParameter<int>("min_maxtrackpt01"))
{
}

bool MFVAnalysisCuts::filter(edm::Event& event, const edm::EventSetup&) {
  edm::Handle<pat::MuonCollection> muons;
  event.getByLabel(muon_src, muons);
  edm::Handle<pat::ElectronCollection> electrons;
  event.getByLabel(electron_src, electrons);
  
  if (int(muons->size() + electrons->size()) < min_nleptons)
    return false;

  edm::Handle<pat::JetCollection> jets;
  event.getByLabel(jet_src, jets);

  int njets = 0;
  int nbtags = 0;
  
  double sum_ht = 0;
  for (int i = 0, ie = jets->size(); i < ie; ++i) {
    const pat::Jet& jet = jets->at(i);
    const double bdisc = jet.bDiscriminator(b_discriminator_name);

    if (jet.pt() > min_jet_pt) {
      sum_ht += jet.pt();
      ++njets;
      if (bdisc > bdisc_min)
        ++nbtags;
    }

    if (i+1==4 && jet.pt() < min_4th_jet_pt) return false; //cut on the pt of the 4th jet
    if (i+1==5 && jet.pt() < min_5th_jet_pt) return false; //cut on the pt of the 5th jet
    if (i+1==6 && jet.pt() < min_6th_jet_pt) return false; //cut on the pt of the 6th jet
  }

  //if (njets == 0) printf("njets = %d, run = %u, luminosity block = %u, event = %u\n", njets, event.id().run(), event.luminosityBlock(), event.id().event());
  if (njets < min_njets) return false; //cut on the minimum number of jets
  if (njets > max_njets) return false; //cut on the maximum number of jets
  if (nbtags < min_nbtags) return false; //cut on the number of btags
  if (sum_ht < min_sum_ht) return false; //cut on the sum of the pt's of all the jets

  edm::Handle<reco::VertexCollection> secondary_vertices;
  event.getByLabel(vertex_src, secondary_vertices);

  const int nsv = int(secondary_vertices->size());
  if (nsv < min_nvertex) return false; //cut on the number of secondary vertices
  int ntracks0 = 0;
  int ntracks1 = 0;
  double maxtrackpt0 = 0;
  double maxtrackpt1 = 0;
  for (int isv = 0; isv < nsv; ++isv) {
    const reco::Vertex& sv = secondary_vertices->at(isv);
    const reco::VertexRef svref(secondary_vertices, isv);
    auto trkb = sv.tracks_begin();
    auto trke = sv.tracks_end();
    int ntracks = trke - trkb;

    std::vector<double> trackpts;
    for (auto trki = trkb; trki != trke; ++trki) {
      const reco::TrackBaseRef& tri = *trki;
      double pti = tri->pt();
      trackpts.push_back(pti);
    }
    std::sort(trackpts.begin(), trackpts.end());
    const double maxtrackpt = trackpts[trackpts.size()-1];

    if (ntracks > ntracks0) {
      ntracks1 = ntracks0;
      ntracks0 = ntracks;
      maxtrackpt1 = maxtrackpt0;
      maxtrackpt0 = maxtrackpt;
    } else if (ntracks > ntracks1) {
      ntracks1 = ntracks;
      maxtrackpt1 = maxtrackpt;
    }
  }
  if (ntracks0 + ntracks1 < min_ntracks01) return false; //cut on the sum of ntracks for the two SV's with the highest ntracks
  if (maxtrackpt0 + maxtrackpt1 < min_maxtrackpt01) return false; //cut on the sum of maxtrackpt for the two SV's with the highest ntracks

  return true;
}

DEFINE_FWK_MODULE(MFVAnalysisCuts);

