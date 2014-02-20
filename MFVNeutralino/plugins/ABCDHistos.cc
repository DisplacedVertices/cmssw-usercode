#include "TH2F.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/Math/interface/deltaPhi.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "JMTucker/MFVNeutralinoFormats/interface/Event.h"
#include "JMTucker/MFVNeutralinoFormats/interface/VertexAux.h"
#include "JMTucker/Tools/interface/Utilities.h"

class ABCDHistos : public edm::EDAnalyzer {
 public:
  explicit ABCDHistos(const edm::ParameterSet&);
  void analyze(const edm::Event&, const edm::EventSetup&);

 private:
  const edm::InputTag mfv_event_src;
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

  TH1F* h_absdeltaphibs01;
  TH1F* h_absdeltaphipv01;

  TH1F* h_pz01lab;
  TH1F* h_pz01cmz;

  TH1F* h_cosanglemom01lab;
  TH1F* h_cosanglemom01cmz;

  TH2F* h_betagamma0lab_betagamma1lab;
  TH2F* h_betagamma0cmz_betagamma1cmz;

  TH2F* h_svdist3dcmz_tkonlymass01;
  TH2F* h_svctau3dcmz_tkonlymass01;
};

ABCDHistos::ABCDHistos(const edm::ParameterSet& cfg)
  : mfv_event_src(cfg.getParameter<edm::InputTag>("mfv_event_src")),
    vertex_src(cfg.getParameter<edm::InputTag>("vertex_src"))
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

  h_absdeltaphibs01 = fs->make<TH1F>("h_absdeltaphibs01", ";absdeltaphibs01;events", 315, 0, 3.15);
  h_absdeltaphipv01 = fs->make<TH1F>("h_absdeltaphipv01", ";absdeltaphipv01;events", 315, 0, 3.15);

  h_pz01lab = fs->make<TH1F>("h_pz01lab", ";pz01lab;events", 100, -300, 300);
  h_pz01cmz = fs->make<TH1F>("h_pz01cmz", ";pz01cmz;events", 100, -300, 300);

  h_cosanglemom01lab = fs->make<TH1F>("h_cosanglemom01lab", ";cosanglemom01lab;events", 100, -1, 1);
  h_cosanglemom01cmz = fs->make<TH1F>("h_cosanglemom01cmz", ";cosanglemom01cmz;events", 100, -1, 1);

  h_betagamma0lab_betagamma1lab = fs->make<TH2F>("h_betagamma0lab_betagamma1lab", ";betagamma1lab;betagamma0lab", 100, 0, 10, 100, 0, 10);
  h_betagamma0cmz_betagamma1cmz = fs->make<TH2F>("h_betagamma0cmz_betagamma1cmz", ";betagamma1cmz;betagamma0cmz", 100, 0, 10, 100, 0, 10);

  h_svdist3dcmz_tkonlymass01 = fs->make<TH2F>("h_svdist3dcmz_tkonlymass01", ";tkonlymass01;svdist3dcmz", 500, 0, 500, 100, 0, 1);
  h_svctau3dcmz_tkonlymass01 = fs->make<TH2F>("h_svctau3dcmz_tkonlymass01", ";tkonlymass01;svtkonlyctau3dcmz", 500, 0, 500, 100, 0, 1);
}

void ABCDHistos::analyze(const edm::Event& event, const edm::EventSetup&) {
  edm::Handle<MFVEvent> mevent;
  event.getByLabel(mfv_event_src, mevent);

  const float pvx = mevent->pvx;
  const float pvy = mevent->pvy;
  const float pvz = mevent->pvz;

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

    double phibs0 = atan2(v0.y - mevent->bsy, v0.x - mevent->bsx);
    double phibs1 = atan2(v1.y - mevent->bsy, v1.x - mevent->bsx);
    h_absdeltaphibs01->Fill(fabs(reco::deltaPhi(phibs0, phibs1)));
    double phipv0 = atan2(v0.y - mevent->pvy, v0.x - mevent->pvx);
    double phipv1 = atan2(v1.y - mevent->pvy, v1.x - mevent->pvx);
    h_absdeltaphipv01->Fill(fabs(reco::deltaPhi(phipv0, phipv1)));

    TLorentzVector x0 = TLorentzVector(v0.x - pvx, v0.y - pvy, v0.z - pvz, v0.pv3ddist / v0.p4().Beta());
    TLorentzVector x1 = TLorentzVector(v1.x - pvx, v1.y - pvy, v1.z - pvz, v1.pv3ddist / v1.p4().Beta());
    TLorentzVector p0 = v0.p4();
    TLorentzVector p1 = v1.p4();
    h_pz01lab->Fill(p0.Pz() + p1.Pz());
    h_cosanglemom01lab->Fill(cos(p0.Angle(p1.Vect())));
    h_betagamma0lab_betagamma1lab->Fill(p1.Beta() * p1.Gamma(), p0.Beta() * p0.Gamma());

    TVector3 betacmz = TVector3(0, 0, -(p0.Pz() + p1.Pz()) / (p0.E() + p1.E()));
    x0.Boost(betacmz);
    x1.Boost(betacmz);
    p0.Boost(betacmz);
    p1.Boost(betacmz);
    h_pz01cmz->Fill(p0.Pz() + p1.Pz());
    h_cosanglemom01cmz->Fill(cos(p0.Angle(p1.Vect())));
    h_betagamma0cmz_betagamma1cmz->Fill(p1.Beta() * p1.Gamma(), p0.Beta() * p0.Gamma());

    double svdist3dcmz = mag(x0.X() - x1.X(), x0.Y() - x1.Y(), x0.Z() - x1.Z());
    double svctau3dcmz = 2 * svdist3dcmz / (p0.Beta()*p0.Gamma() + p1.Beta()*p1.Gamma());
    h_svdist3dcmz_tkonlymass01->Fill(v0.mass[mfv::PTracksOnly] + v1.mass[mfv::PTracksOnly], svdist3dcmz);
    h_svctau3dcmz_tkonlymass01->Fill(v0.mass[mfv::PTracksOnly] + v1.mass[mfv::PTracksOnly], svctau3dcmz);
  }
}

DEFINE_FWK_MODULE(ABCDHistos);
