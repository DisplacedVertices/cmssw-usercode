#include "TH2F.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "JMTucker/MFVNeutralinoFormats/interface/VertexAux.h"

class ABCDHistos : public edm::EDAnalyzer {
 public:
  explicit ABCDHistos(const edm::ParameterSet&);
  void analyze(const edm::Event&, const edm::EventSetup&);

 private:
  const edm::InputTag vertex_src;

  TH1F* h_nsv;
  TH2F* h_ntracks01_maxtrackpt01;
  TH2F* h_tracks_mass1_mass0;
  TH1F* h_tracks_mass01;
  TH2F* h_tracks_costhmombs1_costhmombs0;
  TH2F* h_njets1_njets0;
  TH1F* h_njets01;
  TH2F* h_jets_mass1_mass0;
  TH1F* h_jets_mass01;
  TH2F* h_jets_costhmombs1_costhmombs0;

};

ABCDHistos::ABCDHistos(const edm::ParameterSet& cfg)
  : vertex_src(cfg.getParameter<edm::InputTag>("vertex_src"))
{
  edm::Service<TFileService> fs;
  h_nsv = fs->make<TH1F>("h_nsv", ";number of secondary vertices;events", 15, 0, 15);
  h_ntracks01_maxtrackpt01 = fs->make<TH2F>("h_ntracks01_maxtrackpt01", ";sum of maxtrackpt for the two SV's with the highest ntracks;sum of ntracks for the two SV's with the highest ntracks", 200, 0, 300, 80, 0, 80);
  h_tracks_mass1_mass0 = fs->make<TH2F>("h_tracks_mass1_mass0", ";tracks mass of the SV with the highest ntracks;tracks mass of the SV with the second highest ntracks", 100, 0, 250, 100, 0, 250);
  h_tracks_mass01 = fs->make<TH1F>("h_tracks_mass01", ";sum of tracks mass for the two SV's with the highest ntracks;events", 200, 0, 500);
  h_tracks_costhmombs1_costhmombs0 = fs->make<TH2F>("h_tracks_costhmombs1_costhmombs0", ";tracks cos theta between momentum and beamspot for the SV with the highest ntracks;tracks cos theta between momentum and beamspot for the SV with the second highest ntracks", 100, -1, 1, 100, -1, 1);
  h_njets1_njets0 = fs->make<TH2F>("h_njets1_njets0", ";number of jets that share tracks with the SV with the highest ntracks;number of jets that share tracks with the SV with the second highest ntracks", 10, 0, 10, 10, 0, 10);
  h_njets01 = fs->make<TH1F>("h_njets01", ";sum of number of jets that share tracks with the two SV's with the highest ntracks;events", 20, 0, 20);
  h_jets_mass1_mass0 = fs->make<TH2F>("h_jets_mass1_mass0", ";jets mass of the SV with the highest ntracks;jets mass of the SV with the second highest ntracks", 200, 0, 2000, 200, 0, 2000);
  h_jets_mass01 = fs->make<TH1F>("h_jets_mass01", ";sum of jets mass for the two SV's with the highest ntracks;events", 400, 0, 4000);
  h_jets_costhmombs1_costhmombs0 = fs->make<TH2F>("h_jets_costhmombs1_costhmombs0", ";jets cos theta between momentum and beamspot for the SV with the highest ntracks;jets cos theta between momentum and beamspot for the SV with the second highest ntracks", 100, -1, 1, 100, -1, 1);
}

void ABCDHistos::analyze(const edm::Event& event, const edm::EventSetup&) {

  edm::Handle<MFVVertexAuxCollection> vertices;
  event.getByLabel(vertex_src, vertices);

  const int nsv = int(vertices->size());
  h_nsv->Fill(nsv);

  if (nsv >= 2) {
    const MFVVertexAux& v0 = vertices->at(0);
    const MFVVertexAux& v1 = vertices->at(1);
    h_ntracks01_maxtrackpt01->Fill(v0.maxtrackpt + v1.maxtrackpt, v0.ntracks + v1.ntracks);
    h_tracks_mass1_mass0->Fill(v0.mass[mfv::PTracksOnly], v1.mass[mfv::PTracksOnly]);
    h_tracks_mass01->Fill(v0.mass[mfv::PTracksOnly] + v1.mass[mfv::PTracksOnly]);
    h_tracks_costhmombs1_costhmombs0->Fill(v0.costhmombs[mfv::PTracksOnly], v1.costhmombs[mfv::PTracksOnly]);
    h_njets1_njets0->Fill(v0.njets[mfv::JByNtracks], v1.njets[mfv::JByNtracks]);
    h_njets01->Fill(v0.njets[mfv::JByNtracks] + v1.njets[mfv::JByNtracks]);
    h_jets_mass1_mass0->Fill(v0.mass[mfv::PJetsByNtracks], v1.mass[mfv::PJetsByNtracks]);
    h_jets_mass01->Fill(v0.mass[mfv::PJetsByNtracks] + v1.mass[mfv::PJetsByNtracks]);
    h_jets_costhmombs1_costhmombs0->Fill(v0.costhmombs[mfv::PJetsByNtracks], v1.costhmombs[mfv::PJetsByNtracks]);
  }

}

DEFINE_FWK_MODULE(ABCDHistos);
