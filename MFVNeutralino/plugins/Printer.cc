#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "JMTucker/MFVNeutralinoFormats/interface/Event.h"
#include "JMTucker/MFVNeutralinoFormats/interface/VertexAux.h"
#include "JMTucker/Tools/interface/Utilities.h"

class MFVPrinter : public edm::EDAnalyzer {
 public:
  explicit MFVPrinter(const edm::ParameterSet&);
  void analyze(const edm::Event&, const edm::EventSetup&);

 private:
  const edm::InputTag vertex_src;
  const edm::InputTag event_src;
  const edm::InputTag vertex_aux_src;
  const std::string name;
};

MFVPrinter::MFVPrinter(const edm::ParameterSet& cfg)
  : vertex_src(cfg.getParameter<edm::InputTag>("vertex_src")),
    event_src(cfg.getParameter<edm::InputTag>("event_src")),
    vertex_aux_src(cfg.getParameter<edm::InputTag>("vertex_aux_src")),
    name(cfg.getParameter<std::string>("@module_label"))
{
}

void MFVPrinter::analyze(const edm::Event& event, const edm::EventSetup&) {
  printf("================================================================================\n");
  printf(" %s   run, lumi, event: (%u, %u, %u)\n", name.c_str(), event.id().run(), event.luminosityBlock(), event.id().event());
  printf("================================================================================\n");

  if (vertex_src.label() != "") {
    edm::Handle<reco::VertexCollection> vertices;
    event.getByLabel(vertex_src, vertices);

    printf("------- recoVertices: -------\n");

    const int nsv = int(vertices->size());
    printf("# vertices: %i\n", nsv);

    for (int j = 0; j < nsv; ++j) {
      const reco::Vertex& v = vertices->at(j);
      printf("-----\n\n");
      printf("vertex #%i:\n", j);
      printf("x, y, z: (%11.4e, %11.4e, %11.4e)\n", v.x(), v.y(), v.z());
      printf("covariance matrix: %11.4e %11.4e %11.4e\n", v.covariance(0,0), v.covariance(0,1), v.covariance(0,2));
      printf("                   %11s %11.4e %11.4e\n", "", v.covariance(1,1), v.covariance(1,2));
      printf("                   %11s %11s %11.4e\n", "", "", v.covariance(2,2));
      printf("chi2/ndf: %11.4e / %11.4e\n", v.chi2(), v.ndof());
      printf("p4: (%11.4e, %11.4e, %11.4e, %11.4e)\n", v.p4().pt(), v.p4().eta(), v.p4().phi(), v.p4().mass());
      printf("ntracks: %u\n", v.nTracks());
      int itk = 0;
      for (auto it = v.tracks_begin(), ite = v.tracks_end(); it != ite; ++it) {
        const reco::TrackBaseRef& tk = *it;
        printf("   tk #%3i:  q: %2i  chi2/dof: %6.3f/%6.3f  npx: %i  nst: %i\n", itk++, tk->charge(), tk->chi2(), tk->ndof(), tk->hitPattern().numberOfValidPixelHits(), tk->hitPattern().numberOfValidStripHits());
        printf("      pt: %11.4e +/- %11.4e\n", tk->pt(), tk->ptError());
        printf("     eta: %11.4e +/- %11.4e\n", tk->eta(), tk->etaError());
        printf("     phi: %11.4e +/- %11.4e\n", tk->phi(), tk->phiError());
        printf("     dxy: %11.4e +/- %11.4e\n", tk->dxy(), tk->dxyError());
        printf("      dz: %11.4e +/- %11.4e\n", tk->dz(),  tk->dzError());
      }
      printf("\n");
    }
  }
  else
    printf("------- Not printing recoVertices -------\n\n");

  if (event_src.label() != "") {
    edm::Handle<MFVEvent> mevent;
    event.getByLabel(event_src, mevent);

    printf("------- MFVEvent: -------\n");
    const TLorentzVector gen_lsp_p4[2] = { mevent->gen_lsp_p4(0), mevent->gen_lsp_p4(1) };
    const double gen_lsp_d3[2] = { mag(mevent->gen_lsp_decay[0], mevent->gen_lsp_decay[1], mevent->gen_lsp_decay[2]),
                                   mag(mevent->gen_lsp_decay[3], mevent->gen_lsp_decay[4], mevent->gen_lsp_decay[5]) };

    printf("gen_valid? %i\n", mevent->gen_valid);
    printf("gen_lsps: pt, eta, phi, mass: (%11.4e, %11.4e, %11.4e, %11.4e)   (%11.4e, %11.4e, %11.4e, %11.4e)\n", mevent->gen_lsp_pt[0], mevent->gen_lsp_eta[0], mevent->gen_lsp_phi[0], mevent->gen_lsp_mass[0], mevent->gen_lsp_pt[1], mevent->gen_lsp_eta[1], mevent->gen_lsp_phi[1], mevent->gen_lsp_mass[1]);
    printf("          px, py, pz, energy: (%11.4e, %11.4e, %11.4e, %11.4e)   (%11.4e, %11.4e, %11.4e, %11.4e)\n", gen_lsp_p4[0].Px(), gen_lsp_p4[0].Py(), gen_lsp_p4[0].Pz(), gen_lsp_p4[0].E(), gen_lsp_p4[1].Px(), gen_lsp_p4[1].Py(), gen_lsp_p4[1].Pz(), gen_lsp_p4[1].E());
    printf("          vx, vy, vz, vt    : (%11.4e, %11.4e, %11.4e, %11.4e)   (%11.4e, %11.4e, %11.4e, %11.4e)\n", mevent->gen_lsp_decay[0], mevent->gen_lsp_decay[1], mevent->gen_lsp_decay[2], gen_lsp_d3[0]/gen_lsp_p4[0].Beta(), mevent->gen_lsp_decay[3], mevent->gen_lsp_decay[4], mevent->gen_lsp_decay[5], gen_lsp_d3[1]/gen_lsp_p4[1].Beta());
    printf("          minlspdist2d: %11.4e   lspdist2d: %11.4e   lspdist3d: %11.4e\n", mevent->minlspdist2d(), mevent->lspdist2d(), mevent->lspdist3d());
    printf("          decay types:   %u   %u   partons_in_acc: %u\n", mevent->gen_decay_type[0], mevent->gen_decay_type[1], mevent->gen_partons_in_acc);
    printf("pass triggers (n_trigger_paths = %i):\n", mfv::n_trigger_paths);
    for (int i : mevent->pass_trigger)
      printf("%i ", i);
    printf("\n");
    printf("pass clean (n_clean_paths = %i):\n", mfv::n_clean_paths);
    for (int i : mevent->pass_clean)
      printf("%i ", i);
    printf("\n");
    printf("pass old skim? %i\n", mevent->passoldskim);
    printf("npfjets: %u   pt of pf jet #4: %11.4e   pt of pf jet #4: %11.4e   pt of pf jet #4: %11.4e\n", mevent->npfjets, mevent->pfjetpt4, mevent->pfjetpt5, mevent->pfjetpt6);
    printf("npu: %f\n", mevent->npu);
    printf("beamspot: (%11.4e, %11.4e, %11.4e)\n", mevent->bsx, mevent->bsy, mevent->bsz);
    printf("npv: %u\n", mevent->npv);
    printf("pv: ntracks: %u   sumpt2: %11.4e   coords: (%11.4e, %11.4e, %11.4e)   rho: %11.4e\n", mevent->pv_ntracks, mevent->pv_sumpt2, mevent->pvx, mevent->pvy, mevent->pvz, mevent->pv_rho());
    printf("njets: %u  (no pu l: %u  m: %u  t: %u)  jet_sum_ht: %11.4e   pt of jet #4: %11.4e   pt of jet #4: %11.4e   pt of jet #4: %11.4e\n", mevent->njets, mevent->njetsnopu[0], mevent->njetsnopu[1], mevent->njetsnopu[2], mevent->jet_sum_ht, mevent->jetpt4, mevent->jetpt5, mevent->jetpt6);
    printf("met: %11.4e   metx,y: (%11.4e, %11.4e)   phi: %11.4e   sig: %11.4e   dphimin: %11.4e\n", mevent->met(), mevent->metx, mevent->mety, mevent->metphi(), mevent->metsig, mevent->metdphimin);
    printf("nbtags (l,m,t): ");
    for (uchar i : mevent->nbtags)
      printf("%u ", i);
    printf("\n");
    printf("nmu (l,m,t): ");
    for (int i = 0; i < 3; ++i)
      printf("%i ", mevent->nmu(i));
    printf("  nel (l,m,t): ");
    for (int i = 0; i < 3; ++i)
      printf("%i ", mevent->nel(i));
    printf("  nlep (l,m,t): ");
    for (int i = 0; i < 3; ++i)
      printf("%i ", mevent->nlep(i));
//  size_t nl = mevent->lep_id.size();
//  die_if_not(nl == mevent->lep_pt.size() && nl == mevent->lep_eta.size() && nl == mevent->lep_phi.size() && nl == mevent->lep_dxy.size() && nl == mevent->lep_dz.size() && nl == mevent->lep_iso.size() && nl == mevent->lep_mva.size(), "lep vectors not same size");
//  printf("raw lep info (nl: %lu):\n", nl);
//  for (size_t i = 0; i < nl; ++i)
//    printf("id: %u   pt: %11.4e   eta: %11.4e   phi: %11.4e   dxy: %11.4e   dz: %11.4e   iso: %11.4e   mva: %11.4e\n", mevent->lep_id[i], mevent->lep_pt[i], mevent->lep_eta[i], mevent->lep_phi[i], mevent->lep_dxy[i], mevent->lep_dz[i], mevent->lep_iso[i], mevent->lep_mva[i]);

    printf("------- MFVEvent done -------\n\n");
  }
  else
    printf("------- Not printing event -------\n\n");

  if (vertex_aux_src.label() != "") {
    edm::Handle<MFVVertexAuxCollection> vertices;
    event.getByLabel(vertex_aux_src, vertices);

    printf("------- MFVVertexAuxes: -------\n");

    const int nsv = int(vertices->size());
    printf("# vertices: %i\n", nsv);

    for (int j = 0; j < nsv; ++j) {
      const MFVVertexAux& v = vertices->at(j);
      printf("-----\n\n");
      printf("vertex #%i (original %u):\n", j, v.which);
      printf("x, y, z: (%11.4e, %11.4e, %11.4e)\n", v.x, v.y, v.z);
      printf("covariance matrix: %11.4e %11.4e %11.4e\n", v.cxx, v.cxy, v.cxz);
      printf("                   %11s %11.4e %11.4e\n", "", v.cyy, v.cyz);
      printf("                   %11s %11s %11.4e\n", "", "", v.czz);
      printf("chi2/ndf: %11.4e / %11.4e\n", v.chi2, v.ndof);
//    printf("nlep associated: %lu", v.which_lep.size());
//    if (v.which_lep.size()) {
//      printf("which:\n");
//      for (uchar i : v.which_lep)
//        printf("%u ", i);
//      printf("\n");
//    }
      printf("njets (%i types): ", mfv::NJetsByUse);
      for (uchar i : v.njets)
        printf("%u ", i);
      printf("\n");
      printf("momenta (pt, eta, phi, mass) (%i types):\n", mfv::NMomenta);
      for (int i = 0; i < mfv::NMomenta; ++i)
        printf("   (%11.4e, %11.4e, %11.4e, %11.4e)\n", v.pt[i], v.eta[i], v.phi[i], v.mass[i]);
      printf("momenta (px, py, pz, energy) (%i types):\n", mfv::NMomenta);
      for (int i = 0; i < mfv::NMomenta; ++i)
        printf("   (%11.4e, %11.4e, %11.4e, %11.4e)\n", v.p4(i).Px(), v.p4(i).Py(), v.p4(i).Pz(), v.p4(i).E());
      printf("ntracks: %u   nbad: %u   nptgt3: %u   nptgt5: %u   nptgt10: %u\n", v.ntracks, v.nbadtracks, v.ntracksptgt3, v.ntracksptgt5, v.ntracksptgt10);
      printf("trackminnhits: %u   trackmaxnhits: %u   sumnhitsbehind: %u   maxnhitsbehind: %u\n", v.trackminnhits, v.trackmaxnhits, v.sumnhitsbehind, v.maxnhitsbehind);
      printf("sumpt2: %11.4e   mintrackpt: %11.4e   maxtrackpt: %11.4e   maxm1trackpt: %11.4e   maxm2trackpt: %11.4e   trackptavg: %11.4e   trackptrms: %11.4e\n", v.sumpt2, v.mintrackpt, v.maxtrackpt, v.maxm1trackpt, v.maxm2trackpt, v.trackptavg, v.trackptrms);
      printf("trackdxy           min: %11.4e   max: %11.4e   avg: %11.4e   rms: %11.4e\n", v.trackdxymin, v.trackdxymax, v.trackdxyavg, v.trackdxyrms);
      printf("trackdz            min: %11.4e   max: %11.4e   avg: %11.4e   rms: %11.4e\n", v.trackdzmin, v.trackdzmax, v.trackdzavg, v.trackdzrms);
      printf("trackpterr         min: %11.4e   max: %11.4e   avg: %11.4e   rms: %11.4e\n", v.trackpterrmin, v.trackpterrmax, v.trackpterravg, v.trackpterrrms);
      printf("trackdxyerr        min: %11.4e   max: %11.4e   avg: %11.4e   rms: %11.4e\n", v.trackdxyerrmin, v.trackdxyerrmax, v.trackdxyerravg, v.trackdxyerrrms);
      printf("trackdzerr         min: %11.4e   max: %11.4e   avg: %11.4e   rms: %11.4e\n", v.trackdzerrmin, v.trackdzerrmax, v.trackdzerravg, v.trackdzerrrms);
//    printf("trackpairdeta      min: %11.4e   max: %11.4e   avg: %11.4e   rms: %11.4e\n", v.trackpairdetamin, v.trackpairdetamax, v.trackpairdetaavg, v.trackpairdetarms);
      printf("dr                 min: %11.4e   max: %11.4e   avg: %11.4e   rms: %11.4e\n", v.drmin, v.drmax, v.dravg, v.drrms);
      printf("trackpairmass      min: %11.4e   max: %11.4e   avg: %11.4e   rms: %11.4e\n", v.trackpairmassmin, v.trackpairmassmax, v.trackpairmassavg, v.trackpairmassrms);
      printf("tracktripmass      min: %11.4e   max: %11.4e   avg: %11.4e   rms: %11.4e\n", v.tracktripmassmin, v.tracktripmassmax, v.tracktripmassavg, v.tracktripmassrms);
      printf("trackquadmass      min: %11.4e   max: %11.4e   avg: %11.4e   rms: %11.4e\n", v.trackquadmassmin, v.trackquadmassmax, v.trackquadmassavg, v.trackquadmassrms);
      printf("jetpairdr          min: %11.4e   max: %11.4e   avg: %11.4e   rms: %11.4e\n", v.jetpairdrmin, v.jetpairdrmax, v.jetpairdravg, v.jetpairdrrms);
      printf("costhtkmomvtxdisp  min: %11.4e   max: %11.4e   avg: %11.4e   rms: %11.4e\n", v.costhtkmomvtxdispmin, v.costhtkmomvtxdispmax, v.costhtkmomvtxdispavg, v.costhtkmomvtxdisprms);
      printf("costhjetmomvtxdisp min: %11.4e   max: %11.4e   avg: %11.4e   rms: %11.4e\n", v.costhjetmomvtxdispmin, v.costhjetmomvtxdispmax, v.costhjetmomvtxdispavg, v.costhjetmomvtxdisprms);
      printf("gen2d dist: %11.4e +/- %11.4e (%11.4e sig)\n", v.gen2ddist, v.gen2derr, v.gen2dsig());
      printf("gen3d dist: %11.4e +/- %11.4e (%11.4e sig)\n", v.gen3ddist, v.gen3derr, v.gen3dsig());
      printf("bs2d compatscss: %u   compat: %11.4e   dist: %11.4e +/- %11.4e (%11.4e sig)   bs3ddist: %11.4e\n", v.bs2dcompatscss, v.bs2dcompat, v.bs2ddist, v.bs2derr, v.bs2dsig(), v.bs3ddist);
      printf("pv2d compatscss: %u   compat: %11.4e   dist: %11.4e +/- %11.4e (%11.4e sig)\n", v.pv2dcompatscss, v.pv2dcompat, v.pv2ddist, v.pv2derr, v.pv2dsig());
      printf("pv3d compatscss: %u   compat: %11.4e   dist: %11.4e +/- %11.4e (%11.4e sig)\n", v.pv3dcompatscss, v.pv3dcompat, v.pv3ddist, v.pv3derr, v.pv3dsig());
      printf("pvdz: %11.4e +/- %11.4e (%11.4e sig)\n", v.pvdz(), v.pvdzerr(), v.pvdzsig());
      printf("costh, missdists for %i momenta:\n", mfv::NMomenta);
      for (int i = 0; i < mfv::NMomenta; ++i)
        printf("mom %i: costhmombs: %11.4f   costhmompv2d: %11.4f   costhmompv3d: %11.4f   missdistpv: %11.4e +/- %11.4e (%11.4e sig)\n", i, v.costhmombs[i], v.costhmompv2d[i], v.costhmompv3d[i], v.missdistpv[i], v.missdistpverr[i], v.missdistpvsig(i));

      printf("\n");
    }
  }
  else
    printf("------- Not printing vertices -------\n");

  printf("\n");
}

DEFINE_FWK_MODULE(MFVPrinter);
