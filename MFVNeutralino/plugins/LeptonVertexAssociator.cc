#include "TH2F.h"
#include "TVector3.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/Common/interface/AssociationMap.h"
#include "DataFormats/PatCandidates/interface/PackedCandidate.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "SimDataFormats/GeneratorProducts/interface/GenEventInfoProduct.h"
#include "JMTucker/MFVNeutralinoFormats/interface/LeptonVertexAssociation.h"
#include "TrackingTools/Records/interface/TransientTrackRecord.h"
#include "TrackingTools/TransientTrack/interface/TransientTrack.h"
#include "TrackingTools/TransientTrack/interface/TransientTrackBuilder.h"
#include "JMTucker/Tools/interface/TrackRefGetter.h"
#include "JMTucker/Tools/interface/GenUtilities.h"

#include <algorithm>

class MFVLeptonVertexAssociator : public edm::EDProducer {
public:
  MFVLeptonVertexAssociator(const edm::ParameterSet&);

  virtual void produce(edm::Event&, const edm::EventSetup&);

private:
  typedef mfv::ElectronVertexAssociation ElAssociation;
  typedef mfv::MuonVertexAssociation MuAssociation;

  const bool enable;
  const edm::EDGetTokenT<reco::BeamSpot> beamspot_token;
  const edm::EDGetTokenT<pat::MuonCollection> muons_token;
  const edm::EDGetTokenT<pat::ElectronCollection> electrons_token;
  const edm::EDGetTokenT<reco::VertexRefVector> vertex_ref_token;
  const edm::EDGetTokenT<reco::VertexCollection> vertex_token;
  const edm::EDGetTokenT<GenEventInfoProduct> gen_info_token;
  const edm::EDGetTokenT<std::vector<double>> gen_vertex_token;
  const edm::EDGetTokenT<reco::GenParticleCollection> gen_particles_token;
  const bool input_is_refs;
  const double min_vertex_track_weight;
  const bool histos;
  const bool verbose;

  //how far away the matched leptons are from their respective vertex 
  TH1F* h_ele_vtx_miss_dist;
  TH1F* h_mu_vtx_miss_dist;

  //also get how many leptons/electrons/muons are in vertex + their pt 
  TH1F* h_nlepinSV;
  TH1F* h_nmuinSV;
  TH1F* h_neleinSV;

  TH1F* h_eleinSV_pt;
  TH1F* h_muinSV_pt;
  TH1F* h_eleinSV_dxy;
  TH1F* h_muinSV_dxy;
  TH2F* h_eleinSV_pt_vs_dxy;
  TH2F* h_muinSV_pt_vs_dxy;

  //now also genmatching these leptons -> plot the gen level pt, dxy
  TH1F* h_geneleinSV_pt;
  TH1F* h_genmuinSV_pt;
  TH1F* h_geneleinSV_dxy;
  TH1F* h_genmuinSV_dxy;
  TH2F* h_geneleinSV_pt_vs_dxy;
  TH2F* h_genmuinSV_pt_vs_dxy;

  //by design -- does not include genID of mu to recomu, ele to recoele. 
  TH1F* h_genIDs_recomuinSV;
  TH1F* h_genIDs_recomuinSV50;
  TH1F* h_genIDs_recoeleinSV;
  TH1F* h_genIDs_recoeleinSV50;
  TH1F* h_biggenIDs_recomuinSV;
  TH1F* h_biggenIDs_recomuinSV50;
  TH1F* h_biggenIDs_recoeleinSV;
  TH1F* h_biggenIDs_recoeleinSV50;

  TH2F* h_matchedtkpt_vs_matchedmupt;
  TH2F* h_matchedtkpt_vs_matchedelept;
  TH1F* h_ele_pt;
  TH1F* h_mu_pt;
  TH2F* h_nmu_vs_nmuinSV;
  TH2F* h_nele_vs_neleinSV;

};

MFVLeptonVertexAssociator::MFVLeptonVertexAssociator(const edm::ParameterSet& cfg)
  : enable(cfg.getParameter<bool>("enable")),
    beamspot_token(consumes<reco::BeamSpot>(cfg.getParameter<edm::InputTag>("beamspot_src"))),
    muons_token(consumes<pat::MuonCollection>(cfg.getParameter<edm::InputTag>("muons_src"))),
    electrons_token(consumes<pat::ElectronCollection>(cfg.getParameter<edm::InputTag>("electrons_src"))),
    vertex_ref_token(consumes<reco::VertexRefVector>(cfg.getParameter<edm::InputTag>("vertex_src"))),
    vertex_token(consumes<reco::VertexCollection>(cfg.getParameter<edm::InputTag>("vertex_src"))),
    gen_info_token(consumes<GenEventInfoProduct>(cfg.getParameter<edm::InputTag>("gen_info_src"))),
    gen_vertex_token(consumes<std::vector<double>>(cfg.getParameter<edm::InputTag>("gen_vertex_src"))),
    gen_particles_token(consumes<reco::GenParticleCollection>(cfg.getParameter<edm::InputTag>("gen_particles_src"))),
    input_is_refs(cfg.getParameter<bool>("input_is_refs")),
    min_vertex_track_weight(cfg.getParameter<double>("min_vertex_track_weight")),
    histos(cfg.getUntrackedParameter<bool>("histos", true)),
    verbose(cfg.getUntrackedParameter<bool>("verbose"))
{
  produces<MuAssociation>(mfv::muonsby_name);
  produces<ElAssociation>(mfv::electronsby_name);

  if(histos) {
    edm::Service<TFileService> fs;

    h_ele_vtx_miss_dist = fs->make<TH1F>("h_ele_vtx_miss_dist", ";miss dist between electron and vertex;arb. units", 100, 0, 0.5);
    h_mu_vtx_miss_dist = fs->make<TH1F>("h_mu_vtx_miss_dist", ";miss dist between muon and vertex;arb. units", 100, 0, 0.5);
    h_nlepinSV = fs->make<TH1F>("h_nlepinSV", ";# of leptons associated to SV;arb. units", 5, 0, 5);
    h_nmuinSV = fs->make<TH1F>("h_nmuinSV", ";# of muons associated to SV;arb. units", 5, 0, 5);
    h_neleinSV = fs->make<TH1F>("h_neleinSV", ";# of electrons associated to SV;arb. units", 5, 0, 5);
    h_muinSV_pt = fs->make<TH1F>("h_muinSV_pt", ";pt of muons associated to SV (GeV);arb. units", 200, 0, 400);
    h_eleinSV_pt = fs->make<TH1F>("h_eleinSV_pt", ";pt of electrons associated to SV (GeV);arb. units", 200, 0, 400);
    h_muinSV_dxy = fs->make<TH1F>("h_muinSV_dxy", ";dxy of muons associated to SV (cm);arb. units", 200, 0, 0.2);
    h_eleinSV_dxy = fs->make<TH1F>("h_eleinSV_dxy", ";dxy of electrons associated to SV (cm);arb. units", 200, 0, 0.2);
    h_muinSV_pt_vs_dxy = fs->make<TH2F>("h_muinSV_pt_vs_dxy", ";pt of muons associated to SV (GeV);dxy of muons associated to SV (cm)", 200, 0, 400, 200, 0, 0.2);
    h_eleinSV_pt_vs_dxy = fs->make<TH2F>("h_eleinSV_pt_vs_dxy", ";pt of electrons associated to SV (GeV);dxy of electrons associated to SV (cm)", 200, 0, 400, 200, 0, 0.2);
    

    h_genmuinSV_pt = fs->make<TH1F>("h_gennmuinSV_pt", ";pt of gen muons associated to SV (GeV);arb. units", 200, 0, 400);
    h_geneleinSV_pt = fs->make<TH1F>("h_geneleinSV_pt", ";pt of gen electrons associated to SV (GeV);arb. units", 200, 0, 400);
    h_genmuinSV_dxy = fs->make<TH1F>("h_genmuinSV_dxy", ";dxy of gen muons associated to SV (cm);arb. units", 200, 0, 0.2);
    h_geneleinSV_dxy = fs->make<TH1F>("h_geneleinSV_dxy", ";dxy of gen electrons associated to SV (cm);arb. units", 200, 0, 0.2);
    h_genmuinSV_pt_vs_dxy = fs->make<TH2F>("h_genmuinSV_pt_vs_dxy", ";pt of gen muons associated to SV (GeV);dxy of gen muons associated to SV (cm)", 200, 0, 400, 200, 0, 0.2);
    h_geneleinSV_pt_vs_dxy = fs->make<TH2F>("h_geneleinSV_pt_vs_dxy", ";pt of gen electrons associated to SV (GeV);dxy of gen electrons associated to SV (cm)", 200, 0, 400, 200, 0, 0.2);
    
    h_genIDs_recomuinSV = fs->make<TH1F>("h_genIDs_recomuinSV", ";abs(pdgID) of the gen particle matched to the reco mu in SV;arb. units", 212, 0, 212);
    h_genIDs_recoeleinSV = fs->make<TH1F>("h_genIDs_recoeleinSV", ";abs(pdgID) of the gen particle matched to the reco ele in SV;arb. units", 212, 0, 212);
    h_genIDs_recomuinSV50 = fs->make<TH1F>("h_genIDs_recomuinSV50", ";abs(pdgID) of the gen particle matched to the reco mu w/ pt > 50 in SV;arb. units", 212, 0, 212);
    h_genIDs_recoeleinSV50 = fs->make<TH1F>("h_genIDs_recoeleinSV50", ";abs(pdgID) of the gen particle matched to the reco ele w/ pt > 50 in SV;arb. units", 212, 0, 212);

    h_biggenIDs_recomuinSV = fs->make<TH1F>("h_biggenIDs_recomuinSV", ";abs(pdgID) of the gen particle matched to the reco mu in SV;arb. units", 200, 213, 1213);
    h_biggenIDs_recoeleinSV = fs->make<TH1F>("h_biggenIDs_recoeleinSV", ";abs(pdgID) of the gen particle matched to the reco ele in SV;arb. units", 200, 213, 1213);
    h_biggenIDs_recomuinSV50 = fs->make<TH1F>("h_biggenIDs_recomuinSV50", ";abs(pdgID) of the gen particle matched to the reco mu w/ pt > 50 in SV;arb. units", 200, 213, 1213);
    h_biggenIDs_recoeleinSV50 = fs->make<TH1F>("h_biggenIDs_recoeleinSV50", ";abs(pdgID) of the gen particle matched to the reco ele w/ pt > 50 in SV;arb. units", 200, 213, 1213);

    h_matchedtkpt_vs_matchedmupt = fs->make<TH2F>("h_matchedtkpt_vs_matchedmupt", ";pt of matched tk (GeV); pt of matched mu (GeV))", 200, 0, 400, 200, 0, 400);
    h_matchedtkpt_vs_matchedelept = fs->make<TH2F>("h_matchedtkpt_vs_matchedelept", ";pt of matched tk (GeV); pt of matched ele (GeV))", 200, 0, 400, 200, 0, 400);

    h_mu_pt = fs->make<TH1F>("h_nmu_pt", ";pt of muons not associated to SV (GeV);arb. units", 400, 0, 2000);
    h_ele_pt = fs->make<TH1F>("h_nele_pt", ";pt of electrons not associated to SV (GeV);arb. units", 400, 0, 2000);
    h_nmu_vs_nmuinSV = fs->make<TH2F>("h_nmu_vs_nmuinSV", ";# of mu in SV;# of mu", 5, 0, 5, 5, 0, 5);
    h_nele_vs_neleinSV = fs->make<TH2F>("h_nele_vs_neleinSV", ";# of ele in SV;# of ele", 5, 0, 5, 5, 0, 5);
  }
}


void MFVLeptonVertexAssociator::produce(edm::Event& event, const edm::EventSetup& setup) {
  edm::ESHandle<TransientTrackBuilder> tt_builder;
  setup.get<TransientTrackRecord>().get("TransientTrackBuilder", tt_builder);

  edm::Handle<reco::BeamSpot> beamspot;
  event.getByToken(beamspot_token, beamspot);

  edm::Handle<pat::MuonCollection> muons;
  event.getByToken(muons_token, muons);

  edm::Handle<pat::ElectronCollection> electrons;
  event.getByToken(electrons_token, electrons);

  std::vector<reco::VertexRef> vertices;

  //cant be real data 
  edm::Handle<GenEventInfoProduct> gen_info;
  event.getByToken(gen_info_token, gen_info);

  edm::Handle<std::vector<double>> gen_vertex;
  event.getByToken(gen_vertex_token, gen_vertex);

  edm::Handle<reco::GenParticleCollection> gen_particles;
  event.getByToken(gen_particles_token, gen_particles);

  if (input_is_refs) {
    edm::Handle<reco::VertexRefVector> h;
    event.getByToken(vertex_ref_token, h);
    for (const reco::VertexRef& ref : *h)
      vertices.push_back(ref);
  }
  else {
    edm::Handle<reco::VertexCollection> h;
    event.getByToken(vertex_token, h);
    for (size_t i = 0; i < h->size(); ++i)
      vertices.push_back(reco::VertexRef(h, i));
  }
  const size_t n_muons = muons->size();
  const size_t n_electrons = electrons->size();
  const size_t n_vertices = vertices.size();


  // Associate leptons (muons and electrons) to vertices. For each 
  // lepton, determine if it matches to a track in a vertex. 

  // have the index == muon, but the value is which vertex the muon is
  // associated to (which starts at 0) 
  std::vector<int> mu_index_in_vertex(n_muons, -1);
  std::vector<int> el_index_in_vertex(n_electrons, -1);

  if (enable) {
    //which vertex it is associated to and the transient track 
    std::vector<std::pair<size_t, reco::TransientTrack>> matchedmu_ttracks;
    std::vector<std::pair<size_t, reco::TransientTrack>> matchedele_ttracks;

    for (size_t ivtx = 0; ivtx < n_vertices; ++ivtx) {
      const reco::Vertex& vtx = *vertices.at(ivtx);
      for (auto itk = vtx.tracks_begin(), itke = vtx.tracks_end(); itk != itke; ++itk) {
        if (vtx.trackWeight(*itk) >= min_vertex_track_weight) {
          reco::TrackRef tk = itk->castTo<reco::TrackRef>();

          std::tuple<double, size_t, reco::TransientTrack> matchedmuons; 
          std::tuple<double, size_t, reco::TransientTrack> matchedelectrons;

          for (size_t imuon = 0; imuon < n_muons; ++imuon) {
            const pat::Muon& muon = muons->at(imuon);
            //reco::TrackRef mtk = muon.globalTrack();
            reco::TrackRef mtk = muon.innerTrack();

            if (!mtk.isNull()) {

              //make the same requirements on the muon track that I do for all tracks 
              const double dxybs = mtk->dxy(*beamspot);
              const double dxyerr = mtk->dxyError();
              const double sigmadxybs = dxybs / dxyerr;
              const int npxlayers = mtk->hitPattern().pixelLayersWithMeasurement();
              const int nstlayers = mtk->hitPattern().stripLayersWithMeasurement();
              int min_r = 2000000000;
              for (int i = 1; i <= 4; ++i)
                if (mtk->hitPattern().hasValidHitInPixelLayer(PixelSubdetector::PixelBarrel,i)) {
                  min_r = i;
                  break;
                }
              int losthits = mtk->hitPattern().numberOfLostHits(reco::HitPattern::MISSING_INNER_HITS);
              const double pt = mtk->pt();

              const bool use_mtk =
                        pt > 1 &&
                        fabs(sigmadxybs) > 3 &&
                        npxlayers >= 2 &&
                        nstlayers >= 6 &&
                        ((min_r <= 2 && losthits == 0) || min_r <= 1);
                  
              if (use_mtk) {
                double dr = reco::deltaR(tk->eta(), tk->phi(), mtk->eta(), mtk->phi());
                if (dr < 0.001 ) {
                  matchedmuons = std::make_tuple(dr, imuon, tt_builder->build(mtk));
                  h_matchedtkpt_vs_matchedmupt->Fill(tk->pt(), muon.pt());
                }
              }
            }
          }
          for (size_t iel = 0; iel < n_electrons; ++iel) {
            const pat::Electron& electron = electrons->at(iel);
      
            reco::GsfTrackRef etk = electron.gsfTrack();
            if (!etk.isNull()) {
              //make the same requirements on the muon track that I do for all tracks 
              const double dxybs = etk->dxy(*beamspot);
              const double dxyerr = etk->dxyError();
              const double sigmadxybs = dxybs / dxyerr;
              const int npxlayers = etk->hitPattern().pixelLayersWithMeasurement();
              const int nstlayers = etk->hitPattern().stripLayersWithMeasurement();
              int min_r = 2000000000;
              for (int i = 1; i <= 4; ++i)
                if (etk->hitPattern().hasValidHitInPixelLayer(PixelSubdetector::PixelBarrel,i)) {
                  min_r = i;
                  break;
                }
              int losthits = etk->hitPattern().numberOfLostHits(reco::HitPattern::MISSING_INNER_HITS);
              const double pt = etk->pt();

              const bool use_etk =
                        pt > 1 &&
                        fabs(sigmadxybs) > 3 &&
                        npxlayers >= 2 &&
                        nstlayers >= 6 &&
                        ((min_r <= 2 && losthits == 0) || min_r <= 1);

              if (use_etk) {
                double dr = reco::deltaR(tk->eta(), tk->phi(), etk->eta(), etk->phi());
                if (dr < 0.001 ) {
                  matchedelectrons = std::make_tuple(dr, iel, tt_builder->build(etk));
                  h_matchedtkpt_vs_matchedelept->Fill(tk->pt(), electron.pt());
                }
              }
            }
          }
          // case 1 : have a matched ele 
          if (std::get<0>(matchedelectrons) !=0) {
            if (std::get<0>(matchedmuons) == 0) {
              matchedele_ttracks.push_back(std::make_pair(ivtx, std::get<2>(matchedelectrons)));
              el_index_in_vertex[std::get<1>(matchedelectrons)] = ivtx;
            }
          }
          // case 2 : have a matched mu 
          if (std::get<0>(matchedelectrons) == 0) {
            if (std::get<0>(matchedmuons) != 0) {
              matchedmu_ttracks.push_back(std::make_pair(ivtx, std::get<2>(matchedmuons)));
              mu_index_in_vertex[std::get<1>(matchedmuons)] = ivtx;
            }
          }
          // case 3 : have both matched ele and matched mu --> chose the muon over the electron 
          if (std::get<0>(matchedelectrons) != 0) {
            if (std::get<0>(matchedmuons) != 0) {
              matchedmu_ttracks.push_back(std::make_pair(ivtx, std::get<2>(matchedmuons)));
              mu_index_in_vertex[std::get<1>(matchedmuons)] = ivtx;
            }
          }
        }
      }
    }
    
    if (histos) {
      int nmuinSV = 0;
      int neleinSV = 0;
      for (size_t imuon = 0; imuon < n_muons; ++imuon) {
        // bool gen_matched = false; 
        const pat::Muon& muon = muons->at(imuon);
        if (mu_index_in_vertex[imuon] > 0) {
          nmuinSV += 1;
          h_muinSV_pt->Fill(muon.pt());
          float muinSV_dxy = - (muon.vx() - beamspot->x0() *sin(muon.phi()) + (muon.vy() - beamspot->y0()) * cos(muon.phi()));
          h_muinSV_dxy->Fill(muinSV_dxy);
          h_muinSV_pt_vs_dxy->Fill(muon.pt(), muinSV_dxy);

          //now do the genmatching 
          std::vector<double> mindR;
          for (const reco::GenParticle& gen : *gen_particles) {
            double dR = reco::deltaR(muon.eta(), muon.phi(), gen.eta(), gen.phi());
            mindR.push_back(dR);
          }
          if (*min_element(mindR.begin(), mindR.end()) < 0.01) {
            int idx = std::min_element(mindR.begin(), mindR.end()) - mindR.begin();
            const reco::GenParticle& gen = gen_particles->at(idx);
            const int id = abs(gen.pdgId());
            float geninSV_dxy = - (gen.vx() - beamspot->x0() *sin(gen.phi()) + (gen.vy() - beamspot->y0()) * cos(gen.phi()));
            if (id == 13) {
              h_genmuinSV_pt->Fill(gen.pt());
              h_genmuinSV_dxy->Fill(geninSV_dxy);
              h_genmuinSV_pt_vs_dxy->Fill(gen.pt(), geninSV_dxy);
            }
            else {
              if (id < 213) {
                h_genIDs_recomuinSV->Fill(abs(gen.pdgId()));
                if (muon.pt() > 50) {
                  h_genIDs_recomuinSV50->Fill(abs(gen.pdgId()));
                }
              }
              else if (id > 212) {
                h_biggenIDs_recomuinSV->Fill(abs(gen.pdgId()));
                if (muon.pt() > 50) {
                  h_biggenIDs_recomuinSV50->Fill(abs(gen.pdgId()));
                }
              }
            }
          }
        }
        else {
          h_mu_pt->Fill(muon.pt());
        }
      }
      for (size_t iel = 0; iel < n_electrons; ++iel) {
        const pat::Electron& electron = electrons->at(iel);
        if (el_index_in_vertex[iel] > 0) {
          neleinSV += 1;
          h_eleinSV_pt->Fill(electron.pt());
          float eleinSV_dxy = - (electron.vx() - beamspot->x0() *sin(electron.phi()) + (electron.vy() - beamspot->y0()) * cos(electron.phi()));
          h_eleinSV_dxy->Fill(eleinSV_dxy);
          h_eleinSV_pt_vs_dxy->Fill(electron.pt(), eleinSV_dxy);

          //now do the genmatching 
          std::vector<double> mindR; //now for all 
          for (const reco::GenParticle& gen : *gen_particles) {
            double dR = reco::deltaR(electron.eta(), electron.phi(), gen.eta(), gen.phi());
            mindR.push_back(dR);
          }

          if (*min_element(mindR.begin(), mindR.end()) < 0.01) {
            int idx = std::min_element(mindR.begin(), mindR.end()) - mindR.begin();
            const reco::GenParticle& gen = gen_particles->at(idx);
            const int id = abs(gen.pdgId());
            float geninSV_dxy = - (gen.vx() - beamspot->x0() *sin(gen.phi()) + (gen.vy() - beamspot->y0()) * cos(gen.phi()));
            if (id == 11) {
              h_geneleinSV_pt->Fill(gen.pt());
              h_geneleinSV_dxy->Fill(geninSV_dxy);
              h_geneleinSV_pt_vs_dxy->Fill(gen.pt(), geninSV_dxy);
            }
            else {
              if (id < 213) {
                h_genIDs_recoeleinSV->Fill(abs(gen.pdgId()));
                if (electron.pt() > 50) {
                  h_genIDs_recoeleinSV50->Fill(abs(gen.pdgId()));
                }
              }
              else if (id > 212) {
                h_biggenIDs_recoeleinSV->Fill(abs(gen.pdgId()));
                if (electron.pt() > 50) {
                  h_biggenIDs_recoeleinSV50->Fill(abs(gen.pdgId()));
                }
              }
            }
          }
        }
        else {
          h_ele_pt->Fill(electron.pt());
        }
      }
      h_nmuinSV->Fill(nmuinSV);
      h_neleinSV->Fill(neleinSV);
      h_nlepinSV->Fill(nmuinSV + neleinSV);

      h_nmu_vs_nmuinSV->Fill(nmuinSV, n_muons);
      h_nele_vs_neleinSV->Fill(neleinSV, n_electrons);

      for (size_t ivtx = 0; ivtx < n_vertices; ++ivtx) {
        const reco::Vertex& vtx = *vertices.at(ivtx);
        for (unsigned int j = 0; j < matchedele_ttracks.size(); j++ ) {
          if (matchedele_ttracks[j].first == ivtx) h_ele_vtx_miss_dist->Fill(IPTools::absoluteTransverseImpactParameter(matchedele_ttracks[j].second, vtx).second.value());
        }
        for (unsigned int j = 0; j < matchedmu_ttracks.size(); j++ ) {
          if (matchedmu_ttracks[j].first == ivtx) h_mu_vtx_miss_dist->Fill(IPTools::absoluteTransverseImpactParameter(matchedmu_ttracks[j].second, vtx).second.value());
        }
      }
    }
  }
  
  std::unique_ptr<MuAssociation> mu_assoc;
  mu_assoc.reset(new MuAssociation(&event.productGetter()));

  std::unique_ptr<ElAssociation> el_assoc;
  el_assoc.reset(new ElAssociation(&event.productGetter()));

  if (enable) {
    for (size_t ivtx = 0; ivtx < n_vertices; ++ivtx) {
      reco::VertexRef vtxref = vertices.at(ivtx);
      for (size_t imuon = 0; imuon < n_muons; ++imuon) {
        pat::MuonRef muonref(muons, imuon);
        if (mu_index_in_vertex[imuon] == int(ivtx)) {
          mu_assoc->insert(vtxref, muonref);
        }
      }
      for (size_t iel = 0; iel < n_electrons; ++iel) {
        pat::ElectronRef eleref(electrons, iel);
        if (el_index_in_vertex[iel] == int(ivtx)) {
          el_assoc->insert(vtxref, eleref);
        }
      }
    }
  }

  event.put(std::move(mu_assoc), mfv::muonsby_name);
  event.put(std::move(el_assoc), mfv::electronsby_name);
  
}

DEFINE_FWK_MODULE(MFVLeptonVertexAssociator);
