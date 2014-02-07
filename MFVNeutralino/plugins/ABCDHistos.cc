#include "TH2F.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "JMTucker/MFVNeutralinoFormats/interface/VertexAux.h"
#include "JMTucker/Tools/interface/Utilities.h"

class ABCDHistos : public edm::EDAnalyzer {
 public:
  explicit ABCDHistos(const edm::ParameterSet&);
  void analyze(const edm::Event&, const edm::EventSetup&);

 private:
  const edm::InputTag vertex_src;

  TH1F* h_nsv;
  TH2F* h_ntracks01_maxtrackpt01;

  TH2F* h_bs2ddist0_bs2ddist1;
  TH2F* h_tkonlymass0_tkonlymass1;

  TH2F* h_bs2ddist01_tkonlymass01;
  TH2F* h_bs2ddist0_tkonlymass0;
  TH2F* h_bs2ddist1_tkonlymass1;

  TH2F* h_bs2ddist1_tkonlymass0;
  TH2F* h_bs2ddist0_tkonlymass1;

  TH2F* h_pv2ddist01_tkonlymass01;
  TH2F* h_pv2ddist0_tkonlymass0;

  TH2F* h_pv3ddist01_tkonlymass01;
  TH2F* h_pv3ddist0_tkonlymass0;

  TH2F* h_pv3dtkonlyctau01_tkonlymass01;
  TH2F* h_pv3dtkonlyctau0_tkonlymass0;

  TH2F* h_pv3djetsntkctau01_tkonlymass01;
  TH2F* h_pv3djetsntkctau0_tkonlymass0;

  TH2F* h_pv3dtksjetsntkctau01_tkonlymass01;
  TH2F* h_pv3dtksjetsntkctau0_tkonlymass0;

  TH2F* h_svdist2d_tkonlymass01;
  TH2F* h_svdist3d_tkonlymass01;

  TH2F* h_ntracks01_tkonlymass01;
  TH2F* h_maxtrackpt01_tkonlymass01;

  TH2F* h_bs2ddist_ntracks;
  TH2F* h_bs2derr_ntracks;
  TH2F* h_bs2dsig_ntracks;
};

ABCDHistos::ABCDHistos(const edm::ParameterSet& cfg)
  : vertex_src(cfg.getParameter<edm::InputTag>("vertex_src"))
{
  edm::Service<TFileService> fs;
  h_nsv = fs->make<TH1F>("h_nsv", ";number of secondary vertices;events", 15, 0, 15);
  h_ntracks01_maxtrackpt01 = fs->make<TH2F>("h_ntracks01_maxtrackpt01", ";sum of maxtrackpt for the two SV's with the highest ntracks;sum of ntracks for the two SV's with the highest ntracks", 300, 0, 300, 80, 0, 80);

  h_bs2ddist0_bs2ddist1 = fs->make<TH2F>("h_bs2ddist0_bs2ddist1", ";bs2ddist1;bs2ddist0", 50, 0, 0.5, 50, 0, 0.5);
  h_tkonlymass0_tkonlymass1 = fs->make<TH2F>("h_tkonlymass0_tkonlymass1", ";tkonlymass1;tkonlymass0", 250, 0, 250, 250, 0, 250);

  h_bs2ddist01_tkonlymass01 = fs->make<TH2F>("h_bs2ddist01_tkonlymass01", ";tkonlymass01;bs2ddist01", 500, 0, 500, 100, 0, 1);
  h_bs2ddist0_tkonlymass0 = fs->make<TH2F>("h_bs2ddist0_tkonlymass0", ";tkonlymass0;bs2ddist0", 250, 0, 250, 50, 0, 0.5);
  h_bs2ddist1_tkonlymass1 = fs->make<TH2F>("h_bs2ddist1_tkonlymass1", ";tkonlymass1;bs2ddist1", 250, 0, 250, 50, 0, 0.5);

  h_bs2ddist1_tkonlymass0 = fs->make<TH2F>("h_bs2ddist1_tkonlymass0", ";tkonlymass0;bs2ddist1", 250, 0, 250, 50, 0, 0.5);
  h_bs2ddist0_tkonlymass1 = fs->make<TH2F>("h_bs2ddist0_tkonlymass1", ";tkonlymass1;bs2ddist0", 250, 0, 250, 50, 0, 0.5);

  h_pv2ddist01_tkonlymass01 = fs->make<TH2F>("h_pv2ddist01_tkonlymass01", ";tkonlymass01;pv2ddist01", 500, 0, 500, 100, 0, 1);
  h_pv2ddist0_tkonlymass0 = fs->make<TH2F>("h_pv2ddist0_tkonlymass0", ";tkonlymass0;pv2ddist0", 250, 0, 250, 50, 0, 0.5);

  h_pv3ddist01_tkonlymass01 = fs->make<TH2F>("h_pv3ddist01_tkonlymass01", ";tkonlymass01;pv3ddist01", 500, 0, 500, 100, 0, 1);
  h_pv3ddist0_tkonlymass0 = fs->make<TH2F>("h_pv3ddist0_tkonlymass0", ";tkonlymass0;pv3ddist0", 250, 0, 250, 50, 0, 0.5);

  h_pv3dtkonlyctau01_tkonlymass01 = fs->make<TH2F>("h_pv3dtkonlyctau01_tkonlymass01", ";tkonlymass01;pv3dtkonlyctau01", 500, 0, 500, 100, 0, 1);
  h_pv3dtkonlyctau0_tkonlymass0 = fs->make<TH2F>("h_pv3dtkonlyctau0_tkonlymass0", ";tkonlymass0;pv3dtkonlyctau0", 250, 0, 250, 50, 0, 0.5);

  h_pv3djetsntkctau01_tkonlymass01 = fs->make<TH2F>("h_pv3djetsntkctau01_tkonlymass01", ";tkonlymass01;pv3djetsntkctau01", 500, 0, 500, 100, 0, 1);
  h_pv3djetsntkctau0_tkonlymass0 = fs->make<TH2F>("h_pv3djetsntkctau0_tkonlymass0", ";tkonlymass0;pv3djetsntkctau0", 250, 0, 250, 50, 0, 0.5);

  h_pv3dtksjetsntkctau01_tkonlymass01 = fs->make<TH2F>("h_pv3dtksjetsntkctau01_tkonlymass01", ";tkonlymass01;pv3dtksjetsntkctau01", 500, 0, 500, 100, 0, 1);
  h_pv3dtksjetsntkctau0_tkonlymass0 = fs->make<TH2F>("h_pv3dtksjetsntkctau0_tkonlymass0", ";tkonlymass0;pv3dtksjetsntkctau0", 250, 0, 250, 50, 0, 0.5);

  h_svdist2d_tkonlymass01 = fs->make<TH2F>("h_svdist2d_tkonlymass01", ";tkonlymass01;svdist2d", 500, 0, 500, 100, 0, 1);
  h_svdist3d_tkonlymass01 = fs->make<TH2F>("h_svdist3d_tkonlymass01", ";tkonlymass01;svdist3d", 500, 0, 500, 100, 0, 1);

  h_ntracks01_tkonlymass01 = fs->make<TH2F>("h_ntracks01_tkonlymass01", ";tkonlymass01;ntracks01", 500, 0, 500, 80, 0, 80);
  h_maxtrackpt01_tkonlymass01 = fs->make<TH2F>("h_maxtrackpt01_tkonlymass01", ";tkonlymass01;maxtrackpt01", 500, 0, 500, 300, 0, 300);

  h_bs2ddist_ntracks = fs->make<TH2F>("h_bs2ddist_ntracks", ";ntracks;bs2ddist", 40, 0, 40, 100, 0, 0.5);
  h_bs2derr_ntracks = fs->make<TH2F>("h_bs2derr_ntracks", ";ntracks;bs2derr", 40, 0, 40, 100, 0, 0.05);
  h_bs2dsig_ntracks = fs->make<TH2F>("h_bs2dsig_ntracks", ";ntracks;bs2dsig", 40, 0, 40, 100, 0, 100);
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

    h_bs2ddist0_bs2ddist1->Fill(v1.bs2ddist, v0.bs2ddist);
    h_tkonlymass0_tkonlymass1->Fill(v1.mass[mfv::PTracksOnly], v0.mass[mfv::PTracksOnly]);

    h_bs2ddist01_tkonlymass01->Fill(v0.mass[mfv::PTracksOnly] + v1.mass[mfv::PTracksOnly], v0.bs2ddist + v1.bs2ddist);
    h_bs2ddist0_tkonlymass0->Fill(v0.mass[mfv::PTracksOnly], v0.bs2ddist);
    h_bs2ddist1_tkonlymass1->Fill(v1.mass[mfv::PTracksOnly], v1.bs2ddist);

    h_bs2ddist1_tkonlymass0->Fill(v0.mass[mfv::PTracksOnly], v1.bs2ddist);
    h_bs2ddist0_tkonlymass1->Fill(v1.mass[mfv::PTracksOnly], v0.bs2ddist);

    h_pv2ddist01_tkonlymass01->Fill(v0.mass[mfv::PTracksOnly] + v1.mass[mfv::PTracksOnly], v0.pv2ddist + v1.pv2ddist);
    h_pv2ddist0_tkonlymass0->Fill(v0.mass[mfv::PTracksOnly], v0.pv2ddist);

    h_pv3ddist01_tkonlymass01->Fill(v0.mass[mfv::PTracksOnly] + v1.mass[mfv::PTracksOnly], v0.pv3ddist + v1.pv3ddist);
    h_pv3ddist0_tkonlymass0->Fill(v0.mass[mfv::PTracksOnly], v0.pv3ddist);

    double pv3dtkonlyctau0 = v0.pv3ddist / (v0.p4(mfv::PTracksOnly).Beta() * v0.p4(mfv::PTracksOnly).Gamma());
    double pv3dtkonlyctau1 = v1.pv3ddist / (v1.p4(mfv::PTracksOnly).Beta() * v1.p4(mfv::PTracksOnly).Gamma());
    h_pv3dtkonlyctau01_tkonlymass01->Fill(v0.mass[mfv::PTracksOnly] + v1.mass[mfv::PTracksOnly], pv3dtkonlyctau0 + pv3dtkonlyctau1);
    h_pv3dtkonlyctau0_tkonlymass0->Fill(v0.mass[mfv::PTracksOnly], pv3dtkonlyctau0);

    double pv3djetsntkctau0 = v0.pv3ddist / (v0.p4(mfv::PJetsByNtracks).Beta() * v0.p4(mfv::PJetsByNtracks).Gamma());
    double pv3djetsntkctau1 = v1.pv3ddist / (v1.p4(mfv::PJetsByNtracks).Beta() * v1.p4(mfv::PJetsByNtracks).Gamma());
    h_pv3djetsntkctau01_tkonlymass01->Fill(v0.mass[mfv::PTracksOnly] + v1.mass[mfv::PTracksOnly], pv3djetsntkctau0 + pv3djetsntkctau1);
    h_pv3djetsntkctau0_tkonlymass0->Fill(v0.mass[mfv::PTracksOnly], pv3djetsntkctau0);

    double pv3dtksjetsntkctau0 = v0.pv3ddist / (v0.p4(mfv::PTracksPlusJetsByNtracks).Beta() * v0.p4(mfv::PTracksPlusJetsByNtracks).Gamma());
    double pv3dtksjetsntkctau1 = v1.pv3ddist / (v1.p4(mfv::PTracksPlusJetsByNtracks).Beta() * v1.p4(mfv::PTracksPlusJetsByNtracks).Gamma());
    h_pv3dtksjetsntkctau01_tkonlymass01->Fill(v0.mass[mfv::PTracksOnly] + v1.mass[mfv::PTracksOnly], pv3dtksjetsntkctau0 + pv3dtksjetsntkctau1);
    h_pv3dtksjetsntkctau0_tkonlymass0->Fill(v0.mass[mfv::PTracksOnly], pv3dtksjetsntkctau0);

    double svdist2d = mag(v0.x - v1.x, v0.y - v1.y);
    double svdist3d = mag(v0.x - v1.x, v0.y - v1.y, v0.z - v1.z);
    h_svdist2d_tkonlymass01->Fill(v0.mass[mfv::PTracksOnly] + v1.mass[mfv::PTracksOnly], svdist2d);
    h_svdist3d_tkonlymass01->Fill(v0.mass[mfv::PTracksOnly] + v1.mass[mfv::PTracksOnly], svdist3d);

    h_ntracks01_tkonlymass01->Fill(v0.mass[mfv::PTracksOnly] + v1.mass[mfv::PTracksOnly], v0.ntracks + v1.ntracks);
    h_maxtrackpt01_tkonlymass01->Fill(v0.mass[mfv::PTracksOnly] + v1.mass[mfv::PTracksOnly], v0.maxtrackpt + v1.maxtrackpt);
  }

  for (int isv = 0; isv < nsv; ++isv) {
    const MFVVertexAux& vtx = vertices->at(isv);
    h_bs2ddist_ntracks->Fill(vtx.ntracks, vtx.bs2ddist);
    h_bs2derr_ntracks->Fill(vtx.ntracks, vtx.bs2derr);
    h_bs2dsig_ntracks->Fill(vtx.ntracks, vtx.bs2dsig());
  }

}

DEFINE_FWK_MODULE(ABCDHistos);
