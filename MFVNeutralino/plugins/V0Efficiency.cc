#include "TH1.h"
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
#include "RecoVertex/KalmanVertexFit/interface/KalmanVertexFitter.h"
#include "RecoVertex/VertexTools/interface/VertexDistance3D.h"
#include "SimDataFormats/PileupSummaryInfo/interface/PileupSummaryInfo.h"
#include "TrackingTools/IPTools/interface/IPTools.h"
#include "TrackingTools/Records/interface/TransientTrackRecord.h"
#include "TrackingTools/TransientTrack/interface/TransientTrack.h"
#include "TrackingTools/TransientTrack/interface/TransientTrackBuilder.h"

class MFVV0Efficiency : public edm::EDAnalyzer {
public:
  explicit MFVV0Efficiency(const edm::ParameterSet&);

private:
  virtual void analyze(const edm::Event&, const edm::EventSetup&);

  std::auto_ptr<KalmanVertexFitter> kv_reco;

  const edm::EDGetTokenT<std::vector<PileupSummaryInfo>> pileup_token;
  const std::vector<double> pileup_weights;
  const edm::EDGetTokenT<reco::BeamSpot> beamspot_token;
  const edm::EDGetTokenT<reco::VertexCollection> primary_vertices_token;
  const edm::EDGetTokenT<reco::TrackCollection> tracks_token;
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
  TH1D* h_nalltracks;

  enum { self_mfv, nsel };
  static const char* sel_names[nsel];

  TH1D* h_ntracks[nsel];
  TH1D* h_track_charge[nsel];
  TH1D* h_track_pt[nsel];
  TH1D* h_track_eta[nsel];
  TH1D* h_track_phi[nsel];
  TH1D* h_track_npxhits[nsel];
  TH1D* h_track_nsthits[nsel];
  TH1D* h_track_npxlayers[nsel];
  TH1D* h_track_nstlayers[nsel];
  TH1D* h_track_dxybs[nsel];
  TH1D* h_track_dxypv[nsel];
  TH1D* h_track_dzbs[nsel];
  TH1D* h_track_dzpv[nsel];
  TH1D* h_track_sigmadxy[nsel];
  TH1D* h_track_nsigmadxybs[nsel];
  TH1D* h_track_nsigmadxypv[nsel];

  struct particle_hypo {
    const char* name;
    std::vector<double> charges_and_masses;
    double inv_mass;
    double inv_mass_lo;
    double inv_mass_hi;
    size_t ndaughters() const { return charges_and_masses.size(); }
    //    int charge(size_t i) const { return sgn(charges_and_masses[i]); }
    //    double mass(size_t i) const { return fabs(charges_and_masses[i]); }
  };
  enum { K0_pi_pi, Lambda_p_pi, nhyp };
  static const particle_hypo particle_hypos[nhyp];

  TH1D* h_prefit_p[nsel][nhyp];
  TH1D* h_prefit_costh[nsel][nhyp];
  TH1D* h_prefit_mass[nsel][nhyp];
  TH1D* h_vtx_chi2[nsel][nhyp];
  TH1D* h_vtx_x[nsel][nhyp];
  TH1D* h_vtx_y[nsel][nhyp];
  TH1D* h_vtx_z[nsel][nhyp];
  TH1D* h_vtx_r[nsel][nhyp];
  TH1D* h_vtx_rho[nsel][nhyp];
  TH1D* h_vtx_p[nsel][nhyp];
  TH1D* h_vtx_costh[nsel][nhyp];
  TH1D* h_vtx_mass[nsel][nhyp];
};

const char* MFVV0Efficiency::sel_names[] = { "MFVSelection" };
const MFVV0Efficiency::particle_hypo MFVV0Efficiency::particle_hypos[] = {
  { "K0_pi_pi",    { 0.139570, -0.139570 }, 0.497611, 0, 5 },
  { "Lambda_p_pi", { 0.938272, -0.139570 }, 1.115683, 0, 5 }
};

MFVV0Efficiency::MFVV0Efficiency(const edm::ParameterSet& cfg)
  : kv_reco(new KalmanVertexFitter(cfg.getParameter<edm::ParameterSet>("kvr_params"), cfg.getParameter<edm::ParameterSet>("kvr_params").getParameter<bool>("doSmoothing"))),
    pileup_token(consumes<std::vector<PileupSummaryInfo>>(edm::InputTag("addPileupInfo"))),
    pileup_weights(cfg.getParameter<std::vector<double>>("pileup_weights")),
    beamspot_token(consumes<reco::BeamSpot>(cfg.getParameter<edm::InputTag>("beamspot_src"))),
    primary_vertices_token(consumes<reco::VertexCollection>(cfg.getParameter<edm::InputTag>("primary_vertices_src"))),
    tracks_token(consumes<reco::TrackCollection>(cfg.getParameter<edm::InputTag>("tracks_src"))),
    debug(cfg.getUntrackedParameter<bool>("debug", false))
{
  edm::Service<TFileService> fs;

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
  h_nalltracks = fs->make<TH1D>("h_nalltracks", ";# of tracks, generalTracks selection;events/50", 50, 0, 2500);

  for (int isel = 0; isel < nsel; ++isel) {
    TFileDirectory d = fs->mkdir(sel_names[isel]);

    h_ntracks[isel] = d.make<TH1D>("h_ntracks", ";# of selected tracks;events/1", 500, 0, 500);
    h_track_charge[isel] = d.make<TH1D>("h_track_charge", ";track charge;tracks/1", 3, -1, 2);
    h_track_pt[isel] = d.make<TH1D>("h_track_pt", ";track p_{T} (GeV);tracks/100 MeV", 1000, 0, 100);
    h_track_eta[isel] = d.make<TH1D>("h_track_eta", ";track #eta;tracks/0.01", 540, -2.7, 2.7);
    h_track_phi[isel] = d.make<TH1D>("h_track_phi", ";track #eta;tracks/0.01", 628, -M_PI, M_PI);
    h_track_npxhits[isel] = d.make<TH1D>("h_track_npxhits", ";track # pixel hits;tracks/1", 15, 0, 15);
    h_track_nsthits[isel] = d.make<TH1D>("h_track_nsthits", ";track # strip hits;tracks/1", 40, 0, 40);
    h_track_npxlayers[isel] = d.make<TH1D>("h_track_npxlayers", ";track # pixel layers;tracks/1", 7, 0, 7);
    h_track_nstlayers[isel] = d.make<TH1D>("h_track_nstlayers", ";track # strip layers;tracks/1", 20, 0, 20);
    h_track_dxybs[isel] = d.make<TH1D>("h_track_dxybs", ";track dxy to BS (cm);tracks/10 #mum", 4000, -2, 2);
    h_track_dxypv[isel] = d.make<TH1D>("h_track_dxypv", ";track dxy to PV (cm);tracks/10 #mum", 4000, -2, 2);
    h_track_dzbs[isel] = d.make<TH1D>("h_track_dzbs", ";track dz to BS (cm);tracks/100 #mum", 4000, -20, 20);
    h_track_dzpv[isel] = d.make<TH1D>("h_track_dzpv", ";track dz to PV (cm);tracks/100 #mum", 4000, -20, 20);
    h_track_sigmadxy[isel] = d.make<TH1D>("h_track_sigmadxy", ";track #sigma(dxy) (cm);tracks/5 #mum", 200, 0, 0.1);
    h_track_nsigmadxybs[isel] = d.make<TH1D>("h_track_nsigmadxybs", ";track N#sigma(dxy) to BS (cm);tracks/0.1", 1000, 0, 100);
    h_track_nsigmadxypv[isel] = d.make<TH1D>("h_track_nsigmadxypv", ";track N#sigma(dxy) to PV (cm);tracks/0.1", 1000, 0, 100);

    for (int ihyp = 0; ihyp < nhyp; ++ihyp) {
      TFileDirectory dd = d.mkdir(particle_hypos[ihyp].name);

      h_prefit_p[isel][ihyp] = dd.make<TH1D>("h_prefit_p", ";pre-fit candidate momentum (GeV);candidates/1 GeV", 500, 0, 500);
      h_prefit_costh[isel][ihyp] = dd.make<TH1D>("h_prefit_costh", ";pre-fit candidate cos(angle between displacement and flight dir);candidates/0.01", 201, -1, 1.01);
      h_prefit_mass[isel][ihyp] = dd.make<TH1D>("h_prefit_mass", ";pre-fit candidate invariant mass (GeV);candidates/10 MeV", 500, 0, 5);

      h_vtx_chi2[isel][ihyp] = dd.make<TH1D>("h_vtx_chi2", ";candidate vertex #chi^{2}/ndf;candidates/0.05", 200, 0, 10);
      h_vtx_x[isel][ihyp] = dd.make<TH1D>("h_vtx_x", ";candidate vertex x - pv x (cm);candidates/10 #mum", 4000, -2,2);
      h_vtx_y[isel][ihyp] = dd.make<TH1D>("h_vtx_y", ";candidate vertex y - pv y (cm);candidates/10 #mum", 4000, -2,2);
      h_vtx_z[isel][ihyp] = dd.make<TH1D>("h_vtx_y", ";candidate vertex z - pv z (cm);candidates/10 #mum", 4000, -2,2);
      h_vtx_r[isel][ihyp] = dd.make<TH1D>("h_vtx_y", ";candidate vertex - pv (cm);candidates/10 #mum", 4000, -2,2);
      h_vtx_rho[isel][ihyp] = dd.make<TH1D>("h_vtx_y", ";candidate vertex - pv (2D) (cm);candidates/10 #mum", 4000, -2,2);

      h_vtx_p[isel][ihyp] = dd.make<TH1D>("h_vtx_p", ";post-fit candidate momentum (GeV);candidates/1 GeV", 500, 0, 500);
      h_vtx_costh[isel][ihyp] = dd.make<TH1D>("h_vtx_costh", ";post-fit candidate cos(angle between displacement and flight dir);candidates/0.01", 201, -1, 1.01);
      h_vtx_mass[isel][ihyp] = dd.make<TH1D>("h_vtx_mass", ";post-fit candidate invariant mass (GeV);candidates/10 MeV", 500, 0, 5);
    }
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


  edm::Handle<reco::BeamSpot> beamspot;
  event.getByToken(beamspot_token, beamspot);

  const double bsx = beamspot->x0();
  const double bsy = beamspot->y0();
  const double bsz = beamspot->z0();

  h_bsx->Fill(bsx, w);
  h_bsy->Fill(bsy, w);
  h_bsz->Fill(bsz, w);


  edm::Handle<reco::VertexCollection> primary_vertices;
  event.getByToken(primary_vertices_token, primary_vertices);

  const int npv = int(primary_vertices->size());
  h_npv->Fill(npv);
  if (npv == 0) return;
  const reco::Vertex& pv = (*primary_vertices)[0];

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

  const int nalltracks = int(tracks->size());
  h_nalltracks->Fill(nalltracks);

  std::vector<std::vector<size_t>> seltracks(nsel);

  for (int itk = 0; itk < nalltracks; ++itk) {
    const reco::Track& tk = (*tracks)[itk];
    const int charge = tk.charge();
    const double pt = tk.pt();
    const double eta = tk.eta();
    const double aeta = fabs(eta);
    const double phi = tk.phi();
    const double dzbs = tk.dz(beamspot->position());
    const double dzpv = tk.dz(pv.position());
    const double sigmadxy = tk.dxyError();
    const double dxybs = tk.dxy(*beamspot);
    const double dxypv = tk.dxy(pv.position());
    const double nsigmadxybs = dxybs / sigmadxy;
    const double nsigmadxypv = dxypv / sigmadxy;
    const int npxhits = tk.hitPattern().numberOfValidPixelHits();
    const int nsthits = tk.hitPattern().numberOfValidStripHits();
    const int npxlayers = tk.hitPattern().pixelLayersWithMeasurement();
    const int nstlayers = tk.hitPattern().stripLayersWithMeasurement();
    const int min_r = tk.hitPattern().hasValidHitInFirstPixelBarrel() ? 1 : 2000000000;

    const bool use[nsel] = {
      pt > 1 && npxlayers >= 2 && ((aeta < 2 && nstlayers >= 6) || (aeta >= 2 && nstlayers >= 7)) && fabs(nsigmadxybs) > 4 && min_r == 1
    };

    for (int isel = 0; isel < nsel; ++isel) { 
      if (use[isel]) {
        seltracks[isel].push_back(itk);

        h_track_charge[isel]->Fill(charge);
        h_track_pt[isel]->Fill(pt);
        h_track_eta[isel]->Fill(eta);
        h_track_phi[isel]->Fill(phi);
        h_track_npxhits[isel]->Fill(npxhits);
        h_track_nsthits[isel]->Fill(nsthits);
        h_track_npxlayers[isel]->Fill(npxlayers);
        h_track_nstlayers[isel]->Fill(nstlayers);
        h_track_dxybs[isel]->Fill(dxybs);
        h_track_dxypv[isel]->Fill(dxypv);
        h_track_dzbs[isel]->Fill(dzbs);
        h_track_dzpv[isel]->Fill(dzpv);
        h_track_sigmadxy[isel]->Fill(sigmadxy);
        h_track_nsigmadxybs[isel]->Fill(nsigmadxybs);
        h_track_nsigmadxypv[isel]->Fill(nsigmadxypv);
      }
    }
  }

  auto v3 = [](const reco::Track& tk) { TVector3 v; v.SetPtEtaPhi(tk.pt(), tk.eta(), tk.phi()); return v; };
  auto sgn = [](double x) { return std::signbit(x) ? -1 : 1; };
  edm::ESHandle<TransientTrackBuilder> tt_builder;
  setup.get<TransientTrackRecord>().get("TransientTrackBuilder", tt_builder);

  for (int isel = 0; isel < nsel; ++isel) { 
    const size_t nseltracks = seltracks[isel].size();
    h_ntracks[isel]->Fill(nseltracks);
    if (debug) printf("%s # selected tracks: %lu\n", sel_names[isel], nseltracks);

    for (size_t iseltk = 0; iseltk < nseltracks; ++iseltk) {
      const size_t itk = seltracks[isel][iseltk];
      const reco::Track& tki = (*tracks)[itk];
      const int icharge = tki.charge();
      const TVector3 iv3 = v3(tki);

      for (size_t jseltk = iseltk+1; jseltk < nseltracks; ++jseltk) {
        const size_t jtk = seltracks[isel][jseltk];
        const reco::Track& tkj = (*tracks)[jtk];
        const int jcharge = tkj.charge();
        const TVector3 jv3 = v3(tkj);

        const std::vector<size_t> indices = { itk, jtk };
        const std::vector<int> charges = { icharge, jcharge };
        const std::vector<TVector3> v3s = { iv3, jv3 };
        const size_t ndaughters = charges.size();

        if (debug) {
          printf("track set:\n");
          for (size_t idau = 0; idau < ndaughters; ++idau)
            printf("  %4lu: %s <%10.4f %10.4f %10.4f>\n", indices[idau], charges[idau] > 0 ? "+" : "-", v3s[idau].Pt(), v3s[idau].Eta(), v3s[idau].Phi());
        }

        for (size_t ihyp = 0; ihyp < nhyp; ++ihyp) {
          const particle_hypo& hyp = particle_hypos[ihyp];
          if (hyp.ndaughters() != ndaughters)
            continue;
          if (debug) printf("hypothesis %s:\n", hyp.name);

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
              const int x = charges[idau] * sgn(test[idau]);
              if (x > 0) all_opp = false;
              if (x < 0) all_same = false;
            }
            if (debug) printf("all same? %i opp? %i\n", all_same, all_opp);

            if (!(all_same || all_opp))
              continue;
            
            std::vector<reco::TransientTrack> ttks(ndaughters);
            for (size_t idau = 0; idau < ndaughters; ++idau)
              ttks[idau] = tt_builder->build((*tracks)[indices[idau]]);

            const std::vector<TransientVertex> vv(1, kv_reco->vertex(ttks));
            const TransientVertex& v(vv[0]);
            const double chi2ndof = v.normalisedChiSquared();
            const double ndof = v.degreesOfFreedom();
            const double x = v.position().x();
            const double y = v.position().y();
            const double z = v.position().z();
            const GlobalError cov = v.positionError();

            const TVector3 flight(x - pvx, y - pvy, z - pvz);
            const TVector3 flight_dir(flight.Unit());

            TLorentzVector sum_prefit, sum, p4;
            for (size_t idau = 0; idau < ndaughters; ++idau) {
              const double mass = fabs(test[idau]);

              p4.SetVectM(v3s[idau], mass);
              sum_prefit += p4;

              reco::TransientTrack refit_tk(ttks[idau]);
              p4.SetXYZM(refit_tk.track().px(), refit_tk.track().py(), refit_tk.track().pz(), mass);
              sum += p4;
            }

            if (debug) {
              printf("vertex valid? %i chi2: %10.4f (%.1f dof)  position: <%10.4f %10.4f %10.4f>  err: <%10.4f %10.4f %10.4f / %10.4f %10.4f / %10.4f>\n",
                     v.isValid(), chi2ndof, ndof, x, y, z,
                     cov.cxx(), cov.cyx(), cov.czx(), cov.cyy(), cov.czy(), cov.czz());
              printf(" pre-fit 4-vector: p = %10.4f y = %10.4f eta = %10.4f phi = %10.4f M = %10.4f>\n", sum_prefit.P(), sum_prefit.Rapidity(), sum_prefit.Eta(), sum_prefit.Phi(), sum_prefit.M());
              printf("post-fit 4-vector: p = %10.4f y = %10.4f eta = %10.4f phi = %10.4f M = %10.4f>\n", sum.P(), sum.Rapidity(), sum.Eta(), sum.Phi(), sum.M());
            }
              
            h_prefit_p[isel][ihyp]->Fill(sum_prefit.P());
            h_prefit_costh[isel][ihyp]->Fill(sum_prefit.Vect().Unit().Dot(flight_dir));
            h_prefit_mass[isel][ihyp]->Fill(sum_prefit.M());

            h_vtx_chi2[isel][ihyp]->Fill(chi2ndof);
            h_vtx_x[isel][ihyp]->Fill(flight.X());
            h_vtx_y[isel][ihyp]->Fill(flight.Y());
            h_vtx_z[isel][ihyp]->Fill(flight.Z());
            h_vtx_r[isel][ihyp]->Fill(flight.Mag());
            h_vtx_rho[isel][ihyp]->Fill(flight.Perp());

            h_vtx_p[isel][ihyp]->Fill(sum.P());
            h_vtx_costh[isel][ihyp]->Fill(sum.Vect().Unit().Dot(flight_dir));
            h_vtx_mass[isel][ihyp]->Fill(sum.M());
          }
          while (std::next_permutation(test.begin(), test.end()));
        }
      }
    }
  }
}

DEFINE_FWK_MODULE(MFVV0Efficiency);

