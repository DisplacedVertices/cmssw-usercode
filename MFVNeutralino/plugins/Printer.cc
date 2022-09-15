#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "TrackingTools/IPTools/interface/IPTools.h"
#include "TrackingTools/Records/interface/TransientTrackRecord.h"
#include "TrackingTools/TransientTrack/interface/TransientTrack.h"
#include "TrackingTools/TransientTrack/interface/TransientTrackBuilder.h"
#include "JMTucker/MFVNeutralinoFormats/interface/Event.h"
#include "JMTucker/MFVNeutralinoFormats/interface/VertexAux.h"
#include "JMTucker/Tools/interface/Utilities.h"

class MFVPrinter : public edm::EDAnalyzer {
 public:
  explicit MFVPrinter(const edm::ParameterSet&);
  void analyze(const edm::Event&, const edm::EventSetup&);

 private:
  const bool print_vertex;
  const bool print_event;
  const bool print_vertex_aux;
  const edm::EDGetTokenT<reco::VertexCollection> vertex_token;
  const edm::EDGetTokenT<MFVEvent> event_token;
  const edm::EDGetTokenT<MFVVertexAuxCollection> vertex_aux_token;
  const std::string name;
};

MFVPrinter::MFVPrinter(const edm::ParameterSet& cfg)
  : print_vertex(cfg.getParameter<bool>("print_vertex")),
    print_event(cfg.getParameter<bool>("print_event")),
    print_vertex_aux(cfg.getParameter<bool>("print_vertex_aux")),
    vertex_token(consumes<reco::VertexCollection>(cfg.getParameter<edm::InputTag>("vertex_src"))),
    event_token(consumes<MFVEvent>(cfg.getParameter<edm::InputTag>("event_src"))),
    vertex_aux_token(consumes<MFVVertexAuxCollection>(cfg.getParameter<edm::InputTag>("vertex_aux_src"))),
    name(cfg.getParameter<std::string>("@module_label"))
{
}

void MFVPrinter::analyze(const edm::Event& event, const edm::EventSetup& setup) {
  edm::Handle<MFVEvent> mevent;
  event.getByToken(event_token, mevent);

  const math::XYZPoint bs(mevent->bsx, mevent->bsy, mevent->bsz);
  const math::XYZPoint pv(mevent->pvx, mevent->pvy, mevent->pvz);

  edm::ESHandle<TransientTrackBuilder> tt_builder;
  setup.get<TransientTrackRecord>().get("TransientTrackBuilder", tt_builder);

  printf("================================================================================\n");
  printf(" %s   run, lumi, event: (%u, %u, ", name.c_str(), event.id().run(), event.luminosityBlock());
  std::cout << event.id().event() << ")\n";
  printf("================================================================================\n");

  if (print_vertex) {
    edm::Handle<reco::VertexCollection> primary_vertices;
    event.getByLabel("offlinePrimaryVertices", primary_vertices);
    const reco::Vertex& thepv = primary_vertices->at(0);
    
    edm::Handle<reco::VertexCollection> vertices;
    event.getByToken(vertex_token, vertices);

    printf("------- recoVertices: -------\n");

    const int nsv = int(vertices->size());
    printf("# vertices: %i\n", nsv);

    for (int j = 0; j < nsv; ++j) {
      const reco::Vertex& v = vertices->at(j);
      printf("-----\n\n");
      printf("vertex #%i:\n", j);
      printf("x, y, z: (%11.3g, %11.3g, %11.3g)\n", v.x(), v.y(), v.z());
      printf("covariance matrix: %11.3g %11.3g %11.3g\n", v.covariance(0,0), v.covariance(0,1), v.covariance(0,2));
      printf("                   %11s %11.3g %11.3g\n", "", v.covariance(1,1), v.covariance(1,2));
      printf("                   %11s %11s %11.3g\n", "", "", v.covariance(2,2));
      printf("chi2/ndf: %11.3g = %11.3g / %11.3g\n", v.normalizedChi2(), v.chi2(), v.ndof());
      printf("p4: (%11.3g, %11.3g, %11.3g, %11.3g)\n", v.p4().pt(), v.p4().eta(), v.p4().phi(), v.p4().mass());
      printf("ntracks: %u\n", v.nTracks());
      int itk = 0;
      for (auto it = v.tracks_begin(), ite = v.tracks_end(); it != ite; ++it) {
        const reco::TrackBaseRef& tk = *it;
        const reco::TransientTrack& ttk = tt_builder->build(tk.castTo<reco::TrackRef>());
        printf("   tk #%3i:  q: %2i  chi2/dof: %6.3f/%6.3f  npx: %i  nst: %i\n", itk++, tk->charge(), tk->chi2(), tk->ndof(), tk->hitPattern().numberOfValidPixelHits(), tk->hitPattern().numberOfValidStripHits());
        printf("      pt: %11.3g +/- %11.3g\n", tk->pt(), tk->ptError());
        printf("     eta: %11.3g +/- %11.3g\n", tk->eta(), tk->etaError());
        printf("     phi: %11.3g +/- %11.3g\n", tk->phi(), tk->phiError());
        printf("  dxy_bs: %11.3g +/- %11.3g\n", tk->dxy(bs), tk->dxyError());
        printf("  dxy_pv: %11.3g +/- %11.3g\n", tk->dxy(pv), tk->dxyError());
        printf("   dz_pv: %11.3g +/- %11.3g\n", tk->dz(pv),  tk->dzError());

        auto dxy_ipv = IPTools::absoluteTransverseImpactParameter(ttk, thepv);
        if (dxy_ipv.first)
          printf(" dxy_ipv: %11.3g +/- %11.3g\n", dxy_ipv.second.value(), dxy_ipv.second.error());
        else
          printf(" dxy_ipv: n/a\n");
        auto dxy_isv = IPTools::absoluteTransverseImpactParameter(ttk, v);
        if (dxy_isv.first)
          printf(" dxy_isv: %11.3g +/- %11.3g\n", dxy_isv.second.value(), dxy_isv.second.error());
        else
          printf(" dxy_isv: n/a\n");

        auto d3d_ipv = IPTools::absoluteImpactParameter3D(ttk, thepv);
        if (d3d_ipv.first)
          printf(" d3d_ipv: %11.3g +/- %11.3g\n", d3d_ipv.second.value(), d3d_ipv.second.error());
        else
          printf(" d3d_ipv: n/a\n");
        auto d3d_isv = IPTools::absoluteImpactParameter3D(ttk, v);
        if (d3d_isv.first)
          printf(" d3d_isv: %11.3g +/- %11.3g\n", d3d_isv.second.value(), d3d_isv.second.error());
        else
          printf(" d3d_isv: n/a\n");
        
      }
      printf("\n");
    }
  }
  else
    printf("------- Not printing recoVertices -------\n\n");

  if (print_event) {
    edm::Handle<MFVEvent> mevent;
    event.getByToken(event_token, mevent);

    printf("------- MFVEvent: -------\n");
    const TLorentzVector gen_lsp_p4[2] = { mevent->gen_lsp_p4(0), mevent->gen_lsp_p4(1) };
    const double gen_lsp_d3[2] = { mag(mevent->gen_lsp_decay[0], mevent->gen_lsp_decay[1], mevent->gen_lsp_decay[2]),
                                   mag(mevent->gen_lsp_decay[3], mevent->gen_lsp_decay[4], mevent->gen_lsp_decay[5]) };

    printf("gen_valid? %i\n", mevent->gen_valid);
    printf("gen_lsps: pt, eta, phi, mass: (%11.3g, %11.3g, %11.3g, %11.3g)   (%11.3g, %11.3g, %11.3g, %11.3g)\n", mevent->gen_lsp_pt[0], mevent->gen_lsp_eta[0], mevent->gen_lsp_phi[0], mevent->gen_lsp_mass[0], mevent->gen_lsp_pt[1], mevent->gen_lsp_eta[1], mevent->gen_lsp_phi[1], mevent->gen_lsp_mass[1]);
    printf("          px, py, pz, energy: (%11.3g, %11.3g, %11.3g, %11.3g)   (%11.3g, %11.3g, %11.3g, %11.3g)\n", gen_lsp_p4[0].Px(), gen_lsp_p4[0].Py(), gen_lsp_p4[0].Pz(), gen_lsp_p4[0].E(), gen_lsp_p4[1].Px(), gen_lsp_p4[1].Py(), gen_lsp_p4[1].Pz(), gen_lsp_p4[1].E());
    printf("          vx, vy, vz, vt    : (%11.3g, %11.3g, %11.3g, %11.3g)   (%11.3g, %11.3g, %11.3g, %11.3g)\n", mevent->gen_lsp_decay[0], mevent->gen_lsp_decay[1], mevent->gen_lsp_decay[2], gen_lsp_d3[0]/gen_lsp_p4[0].Beta(), mevent->gen_lsp_decay[3], mevent->gen_lsp_decay[4], mevent->gen_lsp_decay[5], gen_lsp_d3[1]/gen_lsp_p4[1].Beta());
    printf("          minlspdist2d: %11.3g   lspdist2d: %11.3g   lspdist3d: %11.3g\n", mevent->minlspdist2d(), mevent->lspdist2d(), mevent->lspdist3d());
    printf("          decay types:   %u   %u\n", mevent->gen_decay_type[0], mevent->gen_decay_type[1]);
    printf("found hlt (n_hlt_paths = %i):\n", mfv::n_hlt_paths);
    for (int i = 0; i < mfv::n_hlt_paths; ++i)
      printf("%i ", mevent->found_hlt(i));
    printf("\n");
    printf("pass hlt (n_hlt_paths = %i):\n", mfv::n_hlt_paths);
    for (int i = 0; i < mfv::n_hlt_paths; ++i)
      printf("%i ", mevent->pass_hlt(i));
    printf("\n");
    printf("npu: %f\n", mevent->npu);
    printf("beamspot: (%11.3g, %11.3g, %11.3g)  dxdz: %11.3g  dydz: %11.3g  widthx: %11.3g  widthy: %11.3g\n", mevent->bsx, mevent->bsy, mevent->bsz, mevent->bsdxdz, mevent->bsdydz, mevent->bswidthx, mevent->bswidthy);
    printf("npv: %u\n", mevent->npv);
    printf("pv: ntracks: %u   score: %11.3g   coords: (%11.3g, %11.3g, %11.3g)   rho: %11.3g\n", mevent->pv_ntracks, mevent->pv_score, mevent->pvx, mevent->pvy, mevent->pvz, mevent->pv_rho());
    printf("njets: %i (>20GeV: %i)  (no pu l: %u  m: %u  t: %u)  jet_ht: %11.3g   pt of jet #3: %11.3g   pt of jet #4: %11.3g   pt of jet #5: %11.3g\n", mevent->njets(), mevent->njets(20), mevent->njetsnopu(0), mevent->njetsnopu(1), mevent->njetsnopu(2), mevent->jet_ht(), mevent->nth_jet_pt(3), mevent->nth_jet_pt(4), mevent->nth_jet_pt(5));
    printf("jet tracks (n all = %lu)\n", mevent->n_jet_tracks_all());
    for (size_t i = 0, ie = mevent->n_jet_tracks_all(); i < ie; ++i)
      printf("  jet %2i npxhits: %i npxlayers: %i nsthits: %i nstlayers: %i chi2/dof: %.4f qpt %11.3g +- %11.3g eta %11.3g +- %11.3g phi %11.3g +- %11.3g dxy %11.3g +- %11.3g dz %11.3g +- %11.3g\n",
             mevent->jet_track_which_jet[i],
             mevent->jet_track_npxhits(i), mevent->jet_track_npxlayers(i),
             mevent->jet_track_nsthits(i), mevent->jet_track_nstlayers(i),
             mevent->jet_track_chi2dof[i],
             mevent->jet_track_qpt[i], mevent->jet_track_pt_err[i], 
             mevent->jet_track_eta[i], mevent->jet_track_eta_err[i], 
             mevent->jet_track_phi[i], mevent->jet_track_phi_err[i], 
             mevent->jet_track_dxy[i], mevent->jet_track_dxy_err[i], 
             mevent->jet_track_dz[i], mevent->jet_track_dz_err[i]);
    printf("met: %11.3g   phi: %11.3g\n", mevent->met(), mevent->metphi());
    printf("nbtags (l,m,t): ");
    for (int i = 0; i < 3; ++i)
      printf("%u ", mevent->nbtags(i));
    printf("\n");
    // printf("nmu (any,sel): ");
    // for (int i = 0; i < 2; ++i)
    //   printf("%i ", mevent->nmu(i));
    // printf("  nel (any,sel): ");
    // for (int i = 0; i < 2; ++i)
    //   printf("%i ", mevent->nel(i));
    // printf("  nlep (any,sel): ");
    // for (int i = 0; i < 2; ++i)
    //   printf("%i ", mevent->nlep(i));
    // size_t nl = mevent->nlep();
    // die_if_not(nl == mevent->lep_qpt.size() && nl == mevent->lep_eta.size() && nl == mevent->lep_phi.size() && nl == mevent->lep_dxy.size() && nl == mevent->lep_dz.size() && nl == mevent->lep_iso.size(), "lep vectors not same size");
    // printf("raw lep info (nl: %lu):\n", nl);
    // for (size_t i = 0; i < nl; ++i)
    //   printf("id: 0x%08x   pt: %11.3g   eta: %11.3g   phi: %11.3g   dxypv: %11.3g   dxybs: %11.3g   dz: %11.3g   iso: %11.3g\n", mevent->lep_id_[i], mevent->lep_qpt[i], mevent->lep_eta[i], mevent->lep_phi[i], mevent->lep_dxy[i], mevent->lep_dxybs[i], mevent->lep_dz[i], mevent->lep_iso[i]);

    printf("------- MFVEvent done -------\n\n");
  }
  else
    printf("------- Not printing event -------\n\n");

  if (print_vertex_aux) {
    edm::Handle<MFVVertexAuxCollection> vertices;
    event.getByToken(vertex_aux_token, vertices);

    printf("------- MFVVertexAuxes: -------\n");

    const int nsv = int(vertices->size());
    printf("# vertices: %i\n", nsv);

    for (int j = 0; j < nsv; ++j) {
      const MFVVertexAux& v = vertices->at(j);
      printf("-----\n\n");
      printf("vertex #%i (original %u):\n", j, v.which);
      printf("x, y, z: (%11.3g, %11.3g, %11.3g)\n", v.x, v.y, v.z);
      printf("covariance matrix: %11.3g %11.3g %11.3g\n", v.cxx, v.cxy, v.cxz);
      printf("                   %11s %11.3g %11.3g\n", "", v.cyy, v.cyz);
      printf("                   %11s %11s %11.3g\n", "", "", v.czz);
      printf("chi2/ndf: %11.3g = %11.3g / %11.3g\n", v.chi2dof(), v.chi2, v.ndof());
      printf("nlep associated: %lu\n", v.which_lep.size());
      if (v.which_lep.size()) {
        printf("which:\n");
        for (uchar i : v.which_lep)
          printf("%u ", i);
        printf("\n");
      }
      printf("njets (%i types): ", mfv::NJetsByUse);
      for (uchar i : v.njets)
        printf("%u ", i);
      printf("\n");
      printf("momenta (pt, eta, phi, mass) (%i types):\n", mfv::NMomenta);
      for (int i = 0; i < mfv::NMomenta; ++i)
        printf("   (%11.3g, %11.3g, %11.3g, %11.3g)\n", v.pt[i], v.eta[i], v.phi[i], v.mass[i]);
      printf("momenta (px, py, pz, energy) (%i types):\n", mfv::NMomenta);
      for (int i = 0; i < mfv::NMomenta; ++i)
        printf("   (%11.3g, %11.3g, %11.3g, %11.3g)\n", v.p4(i).Px(), v.p4(i).Py(), v.p4(i).Pz(), v.p4(i).E());
      printf("ntracks: %u   nbad: %u   nptgt3: %u   nptgt5: %u   nptgt10: %u\n", v.ntracks(), v.nbadtracks(), v.ntracksptgt(3), v.ntracksptgt(5), v.ntracksptgt(10));
      printf("trackminnhits: %u   trackmaxnhits: %u   sumnhitsbehind: %u   maxnhitsbehind: %u\n", v.trackminnhits(), v.trackmaxnhits(), v.sumnhitsbehind(), v.maxnhitsbehind());
      printf("ntracksshared wpv: %u  wpvs: %u  npvs: %u  pvmost: %i\n", v.ntrackssharedwpv(), v.ntrackssharedwpvs(), v.npvswtracksshared(), v.pvmosttracksshared());
      printf("sumpt2: %11.3g   mintrackpt: %11.3g   maxtrackpt: %11.3g   maxm1trackpt: %11.3g   maxm2trackpt: %11.3g   trackptavg: %11.3g   trackptrms: %11.3g\n", v.sumpt2(), v.mintrackpt(), v.maxtrackpt(), v.maxmntrackpt(1), v.maxmntrackpt(2), v.trackptavg(), v.trackptrms());
      printf("trackdxy           min: %11.3g   max: %11.3g   avg: %11.3g   rms: %11.3g\n", v.trackdxymin(), v.trackdxymax(), v.trackdxyavg(), v.trackdxyrms());
      printf("trackdz            min: %11.3g   max: %11.3g   avg: %11.3g   rms: %11.3g\n", v.trackdzmin(), v.trackdzmax(), v.trackdzavg(), v.trackdzrms());
      printf("trackpterr         min: %11.3g   max: %11.3g   avg: %11.3g   rms: %11.3g\n", v.trackpterrmin(), v.trackpterrmax(), v.trackpterravg(), v.trackpterrrms());
      printf("trackdxyerr        min: %11.3g   max: %11.3g   avg: %11.3g   rms: %11.3g\n", v.trackdxyerrmin(), v.trackdxyerrmax(), v.trackdxyerravg(), v.trackdxyerrrms());
      printf("trackdzerr         min: %11.3g   max: %11.3g   avg: %11.3g   rms: %11.3g\n", v.trackdzerrmin(), v.trackdzerrmax(), v.trackdzerravg(), v.trackdzerrrms());
      printf("trackpairdeta      min: %11.3g   max: %11.3g   avg: %11.3g   rms: %11.3g\n", v.trackpairdetamin(), v.trackpairdetamax(), v.trackpairdetaavg(), v.trackpairdetarms());
      printf("dr                 min: %11.3g   max: %11.3g   avg: %11.3g   rms: %11.3g\n", v.drmin(), v.drmax(), v.dravg(), v.drrms());
      printf("trackpairmass      min: %11.3g   max: %11.3g   avg: %11.3g   rms: %11.3g\n", v.trackpairmassmin(), v.trackpairmassmax(), v.trackpairmassavg(), v.trackpairmassrms());
      printf("tracktripmass      min: %11.3g   max: %11.3g   avg: %11.3g   rms: %11.3g\n", v.tracktripmassmin(), v.tracktripmassmax(), v.tracktripmassavg(), v.tracktripmassrms());
      printf("trackquadmass      min: %11.3g   max: %11.3g   avg: %11.3g   rms: %11.3g\n", v.trackquadmassmin(), v.trackquadmassmax(), v.trackquadmassavg(), v.trackquadmassrms());
      printf("jetpairdeta        min: %11.3g   max: %11.3g   avg: %11.3g   rms: %11.3g\n", v.jetpairdetamin(), v.jetpairdetamax(), v.jetpairdetaavg(), v.jetpairdetarms());
      printf("jetpairdr          min: %11.3g   max: %11.3g   avg: %11.3g   rms: %11.3g\n", v.jetpairdrmin(), v.jetpairdrmax(), v.jetpairdravg(), v.jetpairdrrms());
      printf("costhtkmomvtxdisp  min: %11.3g   max: %11.3g   avg: %11.3g   rms: %11.3g\n", v.costhtkmomvtxdispmin(), v.costhtkmomvtxdispmax(), v.costhtkmomvtxdispavg(), v.costhtkmomvtxdisprms());
      printf("costhjetmomvtxdisp min: %11.3g   max: %11.3g   avg: %11.3g   rms: %11.3g\n", v.costhjetmomvtxdispmin(), v.costhjetmomvtxdispmax(), v.costhjetmomvtxdispavg(), v.costhjetmomvtxdisprms());
      printf("gen2d dist: %11.3g +/- %11.3g (%11.3g sig)\n", v.gen2ddist, v.gen2derr, v.gen2dsig());
      printf("gen3d dist: %11.3g +/- %11.3g (%11.3g sig)\n", v.gen3ddist, v.gen3derr, v.gen3dsig());
      printf("bs2d dist: %11.3g +/- %11.3g (%11.3g sig)\n", v.bs2ddist, v.bs2derr, v.bs2dsig());
      printf("pv2d dist: %11.3g +/- %11.3g (%11.3g sig)\n", v.pv2ddist, v.pv2derr, v.pv2dsig());
      printf("pv3d dist: %11.3g +/- %11.3g (%11.3g sig)\n", v.pv3ddist, v.pv3derr, v.pv3dsig());
      printf("pvdz: %11.3g +/- %11.3g (%11.3g sig)\n", v.pvdz(), v.pvdzerr(), v.pvdzsig());
      printf("costh, missdists for %i momenta:\n", mfv::NMomenta);
      for (int i = 0; i < mfv::NMomenta; ++i)
        printf("mom %i: costhmombs: %11.4f   costhmompv2d: %11.4f   costhmompv3d: %11.4f   missdistpv: %11.3g +/- %11.3g (%11.3g sig)\n", i, v.costhmombs(i), v.costhmompv2d(i), v.costhmompv3d(i), v.missdistpv[i], v.missdistpverr[i], v.missdistpvsig(i));
      printf("tracks:\n");
      for (int i = 0; i < v.ntracks(); ++i) {
        printf("#%i:  chi2: %11.3g ndof: %11.3g  q*pt: %11.3g +- %11.3g eta: %11.3g +- %11.3g phi: %11.3g +- %11.3g dxy: %11.3g +- %11.3g dz: %11.3g +- %11.3g\n", i, v.track_chi2[i], v.track_ndof[i], v.track_q(i) * v.track_pt(i), v.track_pt_err[i], v.track_eta[i], v.track_eta_err(i), v.track_phi[i], v.track_phi_err(i), v.track_dxy[i], v.track_dxy_err(i), v.track_dz[i], v.track_dz_err(i));
        printf("vx: %11.3g vy: %11.3g vz: %11.3g  px: %11.3g py: %11.3g pz: %11.3g\n", v.track_vx[i], v.track_vy[i], v.track_vz[i], v.track_px[i], v.track_py[i], v.track_pz[i]);
        printf("cov:\n");
        for (int j = 0; j < 5; ++j) {
          for (int k = 0; k < j; ++k)
            printf("%11s", "");
          for (int k = j; k < 5; ++k)
            printf("%11.3g", v.track_cov[i](j,k));
          printf("\n");
        }
      }

      printf("\n");
    }
  }
  else
    printf("------- Not printing vertices -------\n");

  printf("\n");
}

DEFINE_FWK_MODULE(MFVPrinter);
