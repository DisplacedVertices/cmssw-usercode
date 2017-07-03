#include "TH2.h"
#include "TLorentzVector.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/BeamSpot/interface/BeamSpot.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "RecoVertex/VertexTools/interface/VertexDistanceXY.h"
#include "RecoVertex/VertexTools/interface/VertexDistance3D.h"
#include "SimDataFormats/PileupSummaryInfo/interface/PileupSummaryInfo.h"
#include "JMTucker/MFVNeutralino/interface/V0Hypotheses.h"

class MFVV0Efficiency : public edm::EDAnalyzer {
public:
  explicit MFVV0Efficiency(const edm::ParameterSet&);

private:
  virtual void analyze(const edm::Event&, const edm::EventSetup&);

  const edm::EDGetTokenT<reco::VertexCollection> vertices_token;
  const edm::EDGetTokenT<std::vector<PileupSummaryInfo>> pileup_token;
  const std::vector<double> pileup_weights;
  const edm::EDGetTokenT<reco::BeamSpot> beamspot_token;
  const edm::EDGetTokenT<reco::VertexCollection> primary_vertex_token;
  const edm::EDGetTokenT<int> n_good_primary_vertices_token;
  const edm::EDGetTokenT<reco::TrackCollection> tracks_token;
  const double min_track_pt;
  const double min_track_nsigmadxybs;
  const double max_chi2ndf;
  const double min_p;
  const double max_p;
  const double mass_window_lo;
  const double mass_window_hi;
  const double min_costh2;
  const double min_costh3;
  const double max_geo2ddist;
  const bool debug;

  TH1D* h_npu;
  TH1D* h_bsx;
  TH1D* h_bsy;
  TH1D* h_bsz;
  TH1D* h_npv;
  TH1D* h_pvx;
  TH1D* h_pvy;
  TH1D* h_pvz;
  TH1D* h_pvbsx;
  TH1D* h_pvbsy;
  TH1D* h_pvbsz;
  TH1D* h_pvntracks;

  enum { nhyp = 1 }; //mfv::n_V0_hyp };

  TH1D* h_ntracks[nhyp+1];
  TH1D* h_max_track_multiplicity[nhyp+1];
  TH1D* h_track_charge[nhyp+1];
  TH1D* h_track_pt[nhyp+1];
  TH1D* h_track_eta[nhyp+1];
  TH1D* h_track_phi[nhyp+1];
  TH1D* h_track_npxhits[nhyp+1];
  TH1D* h_track_nsthits[nhyp+1];
  TH1D* h_track_npxlayers[nhyp+1];
  TH1D* h_track_nstlayers[nhyp+1];
  TH1D* h_track_dxybs[nhyp+1];
  TH1D* h_track_dxypv[nhyp+1];
  TH1D* h_track_dzbs[nhyp+1];
  TH1D* h_track_dzpv[nhyp+1];
  TH1D* h_track_sigmadxy[nhyp+1];
  TH1D* h_track_nsigmadxybs[nhyp+1];
  TH1D* h_track_nsigmadxypv[nhyp+1];

  TH1D* h_nvtx;

  TH1D* h_prefit_p[nhyp];
  TH1D* h_prefit_mass[nhyp];
  TH1D* h_vtx_chi2ndf[nhyp];
  TH2D* h_vtx_2d[nhyp];
  TH1D* h_vtx_x[nhyp];
  TH1D* h_vtx_y[nhyp];
  TH1D* h_vtx_z[nhyp];
  TH1D* h_vtx_r[nhyp];
  TH1D* h_vtx_rho[nhyp];
  TH1D* h_vtx_nsigrho[nhyp];
  TH2D* h_vtx_rho_vs_p[nhyp];
  TH2D* h_vtx_rho_vs_mass[nhyp];
  TH1D* h_vtx_angle[nhyp];
  TH2D* h_vtx_angle_vs_p[nhyp];
  TH2D* h_vtx_angle_vs_mass[nhyp];
  TH1D* h_vtx_p[nhyp];
  TH1D* h_vtx_costh3[nhyp];
  TH1D* h_vtx_costh2[nhyp];
  TH1D* h_vtx_mass[nhyp];
};

MFVV0Efficiency::MFVV0Efficiency(const edm::ParameterSet& cfg)
  : vertices_token(consumes<reco::VertexCollection>(cfg.getParameter<edm::InputTag>("vertices_src"))),
    pileup_token(consumes<std::vector<PileupSummaryInfo>>(edm::InputTag("slimmedAddPileupInfo"))),
    pileup_weights(cfg.getParameter<std::vector<double>>("pileup_weights")),
    beamspot_token(consumes<reco::BeamSpot>(cfg.getParameter<edm::InputTag>("beamspot_src"))),
    primary_vertex_token(consumes<reco::VertexCollection>(cfg.getParameter<edm::InputTag>("primary_vertex_src"))),
    n_good_primary_vertices_token(consumes<int>(edm::InputTag(cfg.getParameter<edm::InputTag>("primary_vertex_src").label(), "nGood"))),
    tracks_token(consumes<reco::TrackCollection>(cfg.getParameter<edm::InputTag>("tracks_src"))),
    min_track_pt(cfg.getParameter<double>("min_track_pt")),
    min_track_nsigmadxybs(cfg.getParameter<double>("min_track_nsigmadxybs")),
    max_chi2ndf(cfg.getParameter<double>("max_chi2ndf")),
    min_p(cfg.getParameter<double>("min_p")),
    max_p(cfg.getParameter<double>("max_p")),
    mass_window_lo(cfg.getParameter<double>("mass_window_lo")),
    mass_window_hi(cfg.getParameter<double>("mass_window_hi")),
    min_costh2(cfg.getParameter<double>("min_costh2")),
    min_costh3(cfg.getParameter<double>("min_costh3")),
    max_geo2ddist(cfg.getParameter<double>("max_geo2ddist")),
    debug(cfg.getUntrackedParameter<bool>("debug", false))
{
  edm::Service<TFileService> fs;
  TH1::SetDefaultSumw2();

  h_npu = fs->make<TH1D>("h_npu", ";true npu", 100, 0, 100);
  h_bsx = fs->make<TH1D>("h_bsx", ";beamspot x", 4000, -2, 2);
  h_bsy = fs->make<TH1D>("h_bsy", ";beamspot y", 4000, -2, 2);
  h_bsz = fs->make<TH1D>("h_bsz", ";beamspot z", 4000, -20, 20);
  h_npv = fs->make<TH1D>("h_npv", ";number of primary vertices", 100, 0, 100);
  h_pvx = fs->make<TH1D>("h_pvx", ";primary vertex x (cm)", 4000, -2, 2);
  h_pvy = fs->make<TH1D>("h_pvy", ";primary vertex y (cm)", 4000, -2, 2);
  h_pvz = fs->make<TH1D>("h_pvz", ";primary vertex z (cm)", 4000, -20, 20);
  h_pvbsx = fs->make<TH1D>("h_pvbsx", ";primary vertex x - beam spot x (cm)", 4000, -2, 2);
  h_pvbsy = fs->make<TH1D>("h_pvbsy", ";primary vertex y - beam spot y (cm)", 4000, -2, 2);
  h_pvbsz = fs->make<TH1D>("h_pvbsz", ";primary vertex z - beam spot z (cm)", 4000, -20, 20);
  h_pvntracks = fs->make<TH1D>("h_pvntracks", ";# tracks in primary vertex;events/5", 100, 0, 500);

  auto booktracks = [&](int i) {
    h_ntracks[i] = fs->make<TH1D>("h_ntracks", ";# of selected tracks;events/1", 500, 0, 500);
    h_max_track_multiplicity[i] = fs->make<TH1D>("h_max_track_multiplicity", ";max multiplicity of any track in vertices;events/1", 10, 0, 10);
    h_track_charge[i] = fs->make<TH1D>("h_track_charge", ";track charge;tracks/1", 3, -1, 2);
    h_track_pt[i] = fs->make<TH1D>("h_track_pt", ";track p_{T} (GeV);tracks/100 MeV", 1000, 0, 100);
    h_track_eta[i] = fs->make<TH1D>("h_track_eta", ";track #eta;tracks/0.01", 540, -2.7, 2.7);
    h_track_phi[i] = fs->make<TH1D>("h_track_phi", ";track #eta;tracks/0.01", 628, -M_PI, M_PI);
    h_track_npxhits[i] = fs->make<TH1D>("h_track_npxhits", ";track # pixel hits;tracks/1", 15, 0, 15);
    h_track_nsthits[i] = fs->make<TH1D>("h_track_nsthits", ";track # strip hits;tracks/1", 40, 0, 40);
    h_track_npxlayers[i] = fs->make<TH1D>("h_track_npxlayers", ";track # pixel layers;tracks/1", 7, 0, 7);
    h_track_nstlayers[i] = fs->make<TH1D>("h_track_nstlayers", ";track # strip layers;tracks/1", 20, 0, 20);
    h_track_dxybs[i] = fs->make<TH1D>("h_track_dxybs", ";track dxy to BS (cm);tracks/10 #mum", 4000, -2, 2);
    h_track_dxypv[i] = fs->make<TH1D>("h_track_dxypv", ";track dxy to PV (cm);tracks/10 #mum", 4000, -2, 2);
    h_track_dzbs[i] = fs->make<TH1D>("h_track_dzbs", ";track dz to BS (cm);tracks/100 #mum", 4000, -20, 20);
    h_track_dzpv[i] = fs->make<TH1D>("h_track_dzpv", ";track dz to PV (cm);tracks/100 #mum", 4000, -20, 20);
    h_track_sigmadxy[i] = fs->make<TH1D>("h_track_sigmadxy", ";track #sigma(dxy) (cm);tracks/5 #mum", 200, 0, 0.1);
    h_track_nsigmadxybs[i] = fs->make<TH1D>("h_track_nsigmadxybs", ";track N#sigma(dxy) to BS (cm);tracks/0.1", 1000, 0, 100);
    h_track_nsigmadxypv[i] = fs->make<TH1D>("h_track_nsigmadxypv", ";track N#sigma(dxy) to PV (cm);tracks/0.1", 1000, 0, 100);
  };

  booktracks(nhyp);

  h_nvtx = fs->make<TH1D>("h_nvtx", ";# of vertices;events/1", 50, 0, 50);

  for (int ihyp = 0; ihyp < nhyp; ++ihyp) {
    TFileDirectory d = fs->mkdir(mfv::V0_hypotheses[ihyp].name);

    booktracks(ihyp);

    h_prefit_p[ihyp] = d.make<TH1D>("h_prefit_p", ";pre-fit candidate momentum (GeV);candidates/100 MeV", 5000, 0, 500);
    h_prefit_mass[ihyp] = d.make<TH1D>("h_prefit_mass", ";pre-fit candidate invariant mass (GeV);candidates/1 MeV", 5000, 0, 5);

    h_vtx_chi2ndf[ihyp] = d.make<TH1D>("h_vtx_chi2ndf", ";candidate vertex #chi^{2}/ndf;candidates/0.05", 200, 0, 10);
    h_vtx_2d[ihyp] = d.make<TH2D>("h_vtx_2d", ";candidate vertex x (cm);candidate veretx y (cm)", 800, -4,4, 800, -4, 4);
    h_vtx_x[ihyp] = d.make<TH1D>("h_vtx_x", ";candidate vertex x - pv x (cm);candidates/40 #mum", 2000, -4,4);
    h_vtx_y[ihyp] = d.make<TH1D>("h_vtx_y", ";candidate vertex y - pv y (cm);candidates/40 #mum", 2000, -4,4);
    h_vtx_z[ihyp] = d.make<TH1D>("h_vtx_z", ";candidate vertex z - pv z (cm);candidates/40 #mum", 2000, -4,4);
    h_vtx_r[ihyp] = d.make<TH1D>("h_vtx_r", ";candidate vertex - pv (cm);candidates/40 #mum", 2000, 0, 8);

    h_vtx_rho[ihyp] = d.make<TH1D>("h_vtx_rho", ";candidate vertex - pv (2D) (cm);candidates/10 #mum", 2000, 0, 8);
    h_vtx_nsigrho[ihyp] = d.make<TH1D>("h_vtx_nsigrho", ";N#sigma(candidate vertex - pv (2D));candidates/0.01", 10000, 0, 100);
    h_vtx_rho_vs_p[ihyp] = d.make<TH2D>("h_vtx_rho_vs_p", ";candidate p (GeV);candidate vertex - pv (2D) (cm)", 400,0,100, 400, 0, 4);
    h_vtx_rho_vs_mass[ihyp] = d.make<TH2D>("h_vtx_rho_vs_mass", ";candidate mass (GeV);candidate vertex - pv (2D) (cm)", 220, 0.380,0.600, 400, 0, 4);

    h_vtx_angle[ihyp] = d.make<TH1D>("h_vtx_angle", ";candidate vertex opening angle (rad);candidates/0.0315", 100, 0, M_PI);
    h_vtx_angle_vs_p[ihyp] = d.make<TH2D>("h_vtx_angle_vs_p", ";candidate vertex momentum (GeV);candidate vertex opening angle (rad)", 400,0,100, 100, 0, M_PI);
    h_vtx_angle_vs_mass[ihyp] = d.make<TH2D>("h_vtx_angle_vs_mass", ";candidate vertex mass (GeV);candidate vertex opening angle (rad)", 220, 0.380,0.600, 100, 0, M_PI);

    h_vtx_p[ihyp] = d.make<TH1D>("h_vtx_p", ";post-fit candidate momentum (GeV);candidates/1 GeV", 400, 0, 100);
    h_vtx_costh3[ihyp] = d.make<TH1D>("h_vtx_costh3", ";post-fit candidate cos(angle between displacement and flight dir);candidates/0.001", 2001, -1, 1.01);
    h_vtx_costh2[ihyp] = d.make<TH1D>("h_vtx_costh2", ";post-fit candidate cos(angle between displacement and flight dir (2D));candidates/0.001", 2001, -1, 1.01);
    h_vtx_mass[ihyp] = d.make<TH1D>("h_vtx_mass", ";post-fit candidate invariant mass (GeV);candidates/1 MeV", 5000, 0, 5);
  }
}

void MFVV0Efficiency::analyze(const edm::Event& event, const edm::EventSetup& setup) {
  const bool is_mc = !event.isRealData();
  int npu = -1;
  double w = 1;

  if (is_mc) {
    edm::Handle<std::vector<PileupSummaryInfo> > pileup;
    event.getByToken(pileup_token, pileup);

    for (std::vector<PileupSummaryInfo>::const_iterator psi = pileup->begin(), end = pileup->end(); psi != end; ++psi)
      if (psi->getBunchCrossing() == 0)
        npu = psi->getTrueNumInteractions();

    assert(npu >= 0);
    h_npu->Fill(npu);
    if (npu >= int(pileup_weights.size()))
      w *= pileup_weights.back();
    else
      w *= pileup_weights[npu];
  }

  h_npu->Fill(npu);

  edm::Handle<reco::BeamSpot> beamspot;
  event.getByToken(beamspot_token, beamspot);

  const double bsx = beamspot->x0();
  const double bsy = beamspot->y0();
  const double bsz = beamspot->z0();

  h_bsx->Fill(bsx, w);
  h_bsy->Fill(bsy, w);
  h_bsz->Fill(bsz, w);

  edm::Handle<reco::VertexCollection> primary_vertex;
  event.getByToken(primary_vertex_token, primary_vertex);
  edm::Handle<int> n_good_primary_vertices;
  event.getByToken(n_good_primary_vertices_token, n_good_primary_vertices);

  const reco::Vertex& pv = (*primary_vertex)[0];
  const int npv = *n_good_primary_vertices;
  h_npv->Fill(npv);

  const double pvx = pv.x();
  const double pvy = pv.y();
  const double pvz = pv.z();
  const int pvntracks = pv.nTracks();

  h_pvx->Fill(pvx, w);
  h_pvy->Fill(pvy, w);
  h_pvz->Fill(pvz, w);
  h_pvbsx->Fill(pvx - bsx, w);
  h_pvbsy->Fill(pvy - bsy, w);
  h_pvbsz->Fill(pvz - bsz, w);
  h_pvntracks->Fill(pvntracks, w);
  
  if (debug) printf("\nEVENT (%u, %u, %llu) npu %i npv %i weight %f\n", event.id().run(), event.luminosityBlock(), event.id().event(), npu, npv, w);

  edm::Handle<reco::TrackCollection> tracks;
  event.getByToken(tracks_token, tracks);
  const size_t ntracks = tracks->size();
  h_ntracks[nhyp]->Fill(ntracks);

  auto filltrack = [&](const int i, const reco::Track& tk) {
    h_track_charge[i]->Fill(tk.charge(), w);
    h_track_pt[i]->Fill(tk.pt(), w);
    h_track_eta[i]->Fill(tk.eta(), w);
    h_track_phi[i]->Fill(tk.phi(), w);
    h_track_npxhits[i]->Fill(tk.hitPattern().numberOfValidPixelHits(), w);
    h_track_nsthits[i]->Fill(tk.hitPattern().numberOfValidStripHits(), w);
    h_track_npxlayers[i]->Fill(tk.hitPattern().pixelLayersWithMeasurement(), w);
    h_track_nstlayers[i]->Fill(tk.hitPattern().stripLayersWithMeasurement(), w);
    h_track_dxybs[i]->Fill(tk.dxy(*beamspot), w);
    h_track_dxypv[i]->Fill(tk.dxy(pv.position()), w);
    h_track_dzbs[i]->Fill(tk.dz(beamspot->position()), w);
    h_track_dzpv[i]->Fill(tk.dz(pv.position()), w);
    h_track_sigmadxy[i]->Fill(tk.dxyError(), w);
    h_track_nsigmadxybs[i]->Fill(tk.dxy(*beamspot) / tk.dxyError(), w);
    h_track_nsigmadxypv[i]->Fill(tk.dxy(pv.position()) / tk.dxyError(), w);
  };

  for (size_t itk = 0; itk < ntracks; ++itk)
    filltrack(nhyp, (*tracks)[itk]);

  edm::Handle<reco::VertexCollection> vertices;
  event.getByToken(vertices_token, vertices);
  const size_t nvtx = vertices->size();
  h_nvtx->Fill(nvtx, w);

  std::vector<std::multiset<reco::TrackRef>> tracks_used(nhyp);

  for (size_t ivtx = 0; ivtx < nvtx; ++ivtx) {
    const reco::Vertex& v = (*vertices)[ivtx];
    const double chi2ndf = v.normalizedChi2();
    if (chi2ndf > max_chi2ndf)
      continue;

    const size_t ndaughters = v.nTracks();
    if (debug) std::cout << "ivtx " << ivtx << " chi2 " << chi2ndf << " ntracks " << v.nTracks() << " has refits? " << v.hasRefittedTracks() << std::endl;
    std::vector<int> charges(ndaughters, 0);
    std::vector<TVector3> v3s(ndaughters);
    std::vector<reco::TrackRef> refs(ndaughters);
    bool tracks_ok = true;

    int itk = 0;
    for (auto it = v.tracks_begin(), ite = v.tracks_end(); it != ite; ++it, ++itk) {
      const reco::Track& tk = **it;
      if (tk.pt() < min_track_pt ||
          fabs(tk.dxy(*beamspot) / tk.dxyError()) < min_track_nsigmadxybs) {
        tracks_ok = false;
        break;
      }

      charges[itk] = tk.charge();
      v3s[itk].SetPtEtaPhi(tk.pt(), tk.eta(), tk.phi());
      refs[itk] = it->castTo<reco::TrackRef>();
    }

    if (!tracks_ok)
      continue;
        
    for (size_t ihyp = 0; ihyp < nhyp; ++ihyp) {
      const auto& hyp = mfv::V0_hypotheses[ihyp];
      if (debug) printf("hypothesis %s:\n", hyp.name);
      if (ndaughters != hyp.ndaughters())
        continue;

      std::vector<double> test(hyp.charges_and_masses);

      do {
        if (debug) {
          printf("permutation:");
          for (size_t idau = 0; idau < ndaughters; ++idau)
            printf(" %10.4f", test[idau]);
          printf("\n");
        }

        bool all_same = true, all_opp = true;
        for (size_t idau = 0; idau < ndaughters; ++idau) {
          const int x = charges[idau] * (test[idau] > 0 ? 1 : -1);
          if (x > 0) all_opp = false;
          if (x < 0) all_same = false;
        }
        if (debug) printf("all same? %i opp? %i\n", all_same, all_opp);

        if (!all_same && !all_opp)
          continue;

        TLorentzVector sum_prefit, p4;
        for (size_t idau = 0; idau < ndaughters; ++idau) {
          const double mass = fabs(test[idau]);
          p4.SetVectM(v3s[idau], mass);
          sum_prefit += p4;
        }

        if (debug) printf(" pre-fit 4-vector: p = %10.4f y = %10.4f eta = %10.4f phi = %10.4f M = %10.4f>\n", sum_prefit.P(), sum_prefit.Rapidity(), sum_prefit.Eta(), sum_prefit.Phi(), sum_prefit.M());

        const double x = v.x();
        const double y = v.y();
        const double z = v.z();
        const double nsigrho = VertexDistanceXY().distance(v, pv).significance();

        const TVector3 flight(x - pv.x(), y - pv.y(), z - pv.z());
        const TVector3 flight_dir(flight.Unit());
        const TVector2 flight_dir_2(flight_dir.X(), flight_dir.Y());

        TLorentzVector sum;
        for (size_t idau = 0; idau < ndaughters; ++idau) {
          const reco::Track refit_tk = v.refittedTrack(refs[idau]);
          const double mass = fabs(test[idau]); 
          p4.SetXYZM(refit_tk.px(), refit_tk.py(), refit_tk.pz(), mass);
          sum += p4;
        }

        auto get_angle = [&](const reco::Track& tk0, const reco::Track& tk1) { return acos((tk0.px() * tk1.px() + tk0.py() * tk1.py() + tk0.pz() * tk1.pz()) / tk0.p() / tk1.p()); };
        const double angle = ndaughters == 2 ? get_angle(v.refittedTrack(refs[0]), v.refittedTrack(refs[1])) : -1;
        const double mass = sum.M();
        const double p = sum.P();
        const double costh3 = sum.Vect().Unit().Dot(flight_dir);
        const double costh2 = cos(sum.Vect().Unit().XYvector().DeltaPhi(flight_dir_2)); // wtf
        const double geo2ddist = hypot(x, y);
        const double mass_lo = mass_window_lo < 0 ? -mass_window_lo : hyp.mass - mass_window_lo;
        const double mass_hi = mass_window_hi < 0 ? -mass_window_hi : hyp.mass + mass_window_hi;
        const bool use =
          p >= min_p &&
          p < max_p && // < and not <= for disjoint bins
          mass >= mass_lo &&
          mass <= mass_hi &&
          costh2 >= min_costh2 &&
          costh3 >= min_costh3 &&
          geo2ddist < max_geo2ddist;

        if (debug) {
          printf("vertex chi2: %10.4f (%.1f dof)  position: <%10.4f %10.4f %10.4f>  err: <%10.4f %10.4f %10.4f / %10.4f %10.4f / %10.4f>\n",
                 chi2ndf, v.ndof(), x, y, z, v.covariance(0,0), v.covariance(0,1), v.covariance(0,2), v.covariance(1,1), v.covariance(1,2), v.covariance(2,2));
          printf("post-fit 4-vector: p = %10.4f y = %10.4f eta = %10.4f phi = %10.4f M = %10.4f>\n", p, sum.Rapidity(), sum.Eta(), sum.Phi(), mass);
          printf("use? %i\n", use);
        }

        if (!use)
          continue;

        tracks_used[ihyp].insert(refs.begin(), refs.end());

        h_vtx_chi2ndf[ihyp]->Fill(chi2ndf, w);
        h_vtx_2d[ihyp]->Fill(x, y, w);
        h_vtx_x[ihyp]->Fill(flight.X(), w);
        h_vtx_y[ihyp]->Fill(flight.Y(), w);
        h_vtx_z[ihyp]->Fill(flight.Z(), w);
        h_vtx_r[ihyp]->Fill(flight.Mag(), w);
        h_vtx_rho[ihyp]->Fill(flight.Perp(), w);
        h_vtx_rho_vs_p[ihyp]->Fill(sum.P(), flight.Perp(), w);
        h_vtx_rho_vs_mass[ihyp]->Fill(mass, flight.Perp(), w);
        h_vtx_nsigrho[ihyp]->Fill(nsigrho, w);

        h_vtx_angle[ihyp]->Fill(angle, w);
        h_vtx_angle_vs_p[ihyp]->Fill(p, angle, w);
        h_vtx_angle_vs_mass[ihyp]->Fill(mass, angle, w);

        h_vtx_p[ihyp]->Fill(p, w);
        h_vtx_costh3[ihyp]->Fill(costh3, w);
        h_vtx_costh2[ihyp]->Fill(costh2, w);
        h_vtx_mass[ihyp]->Fill(mass, w);

        h_prefit_p[ihyp]->Fill(sum_prefit.P(), w);
        h_prefit_mass[ihyp]->Fill(sum_prefit.M(), w);
      }
      while (std::next_permutation(test.begin(), test.end()));
    }
  }

  for (size_t ihyp = 0; ihyp < nhyp; ++ihyp) {
    int max_mult = 0;
    for (auto r : tracks_used[ihyp]) {
      const int mult = tracks_used[ihyp].count(r);
      if (mult > max_mult)
        max_mult = mult;
    }
    h_max_track_multiplicity[ihyp]->Fill(max_mult);

    for (auto tkref : tracks_used[ihyp])
      filltrack(ihyp, *tkref);
  }
}

DEFINE_FWK_MODULE(MFVV0Efficiency);
