#include "DataFormats/JetReco/interface/PFJetCollection.h"
#include "DataFormats/BeamSpot/interface/BeamSpot.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "RecoEgamma/EgammaTools/interface/EffectiveAreas.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "DataFormats/TrackReco/interface/HitPattern.h"

#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "JMTucker/MFVNeutralinoFormats/interface/MCInteractions.h"
#include "JMTucker/MFVNeutralinoFormats/interface/SeedTracks.h"
#include "JMTucker/Tools/interface/AnalysisEras.h"
#include "JMTucker/Tools/interface/ExtValue.h"
#include "JMTucker/Tools/interface/Math.h"
#include "JMTucker/Tools/interface/TrackRefGetter.h"
#include "JMTucker/Tools/interface/StatCalculator.h"
#include "JMTucker/Tools/interface/Utilities.h"


#include <string>

class MFVSeedTracksProducer : public edm::EDProducer {
public:
    explicit MFVSeedTracksProducer(const edm::ParameterSet&);
    void produce(edm::Event&, const edm::EventSetup&);

private:
    const edm::EDGetTokenT<reco::BeamSpot> beamspot_token;
    const edm::EDGetTokenT<mfv::MCInteraction> mci_token;
    const edm::EDGetTokenT<std::vector<reco::TrackRef>> seed_tracks_token;
    const edm::EDGetTokenT<std::vector<reco::TrackRef>> museed_tracks_token;
    const edm::EDGetTokenT<std::vector<reco::TrackRef>> eleseed_tracks_token;
};

MFVSeedTracksProducer::MFVSeedTracksProducer(const edm::ParameterSet& cfg) 
    : beamspot_token(consumes<reco::BeamSpot>(cfg.getParameter<edm::InputTag>("beamspot_src"))),
      mci_token(consumes<mfv::MCInteraction>(cfg.getParameter<edm::InputTag>("mci_src"))),
      seed_tracks_token(consumes<std::vector<reco::TrackRef>>(cfg.getParameter<edm::InputTag>("seed_tracks_src"))),
      museed_tracks_token(consumes<std::vector<reco::TrackRef>>(cfg.getParameter<edm::InputTag>("muon_seed_tracks_src"))),
      eleseed_tracks_token(consumes<std::vector<reco::TrackRef>>(cfg.getParameter<edm::InputTag>("electron_seed_tracks_src")))
{
    produces<MFVSeedTracks>();
}

void MFVSeedTracksProducer::produce(edm::Event& event, const edm::EventSetup& setup) {
    std::unique_ptr<MFVSeedTracks> seedtks(new MFVSeedTracks);
    
    edm::Handle<reco::BeamSpot> beamspot;
    event.getByToken(beamspot_token, beamspot);
    const float bsx = beamspot->x0();
    const float bsy = beamspot->y0();
    const float bsz = beamspot->z0();
    const GlobalPoint origin(bsx, bsy, bsz);
    const reco::Vertex fake_bs_vtx(beamspot->position(), beamspot->covariance3D());

    edm::Handle<mfv::MCInteraction> mci;
    event.getByToken(mci_token, mci);

    if (mci->valid()) {
        assert(mci->primaries().size() == 2);
        for (int i = 0; i < 2; ++i) {
            auto p = mci->decay_point(i);
            seedtks->gen_lsp_decay[i*3+0] = p.x;
            seedtks->gen_lsp_decay[i*3+1] = p.y;
            seedtks->gen_lsp_decay[i*3+2] = p.z;
        }
    }

    edm::Handle<std::vector<reco::TrackRef>> seed_tracks;
    event.getByToken(seed_tracks_token, seed_tracks);

    edm::Handle<std::vector<reco::TrackRef>> muon_seed_tracks;
    event.getByToken(museed_tracks_token, muon_seed_tracks);

    edm::Handle<std::vector<reco::TrackRef>> electron_seed_tracks;
    event.getByToken(eleseed_tracks_token, electron_seed_tracks);

    //seed tracks is the main collection with all seed tracks included 
    // neleseed and nmuseed are : of the seed tracks, how many are electrons? how many are muons? 
    seedtks->nseedtracks = (seed_tracks->size());
    seedtks->neleseed = (electron_seed_tracks->size());
    seedtks->nmuseed = (muon_seed_tracks->size());

    for (size_t i = 0, it = seed_tracks->size(); i < it; ++i){

        const reco::TrackRef& tk = (*seed_tracks)[i];

        seedtks->id.push_back(float(tk.id().id()));
        seedtks->key.push_back(float(tk.key()));
        seedtks->tk_idx.push_back(float(i));

        int min_r = 2000000000;
        for (int i = 1; i <= 4; ++i)
        if (tk->hitPattern().hasValidHitInPixelLayer(PixelSubdetector::PixelBarrel,i)) {
            min_r = i;
            break;
        }

        double nsigmadxybs = (tk->dxy(*beamspot)) / (tk->dxyError());
        double nsigmadz = (tk->dz(beamspot->position())) / (tk->dzError());

        seedtks->p.push_back(tk->p());
        seedtks->pt.push_back(tk->pt());
        seedtks->pterr.push_back(tk->ptError());
        seedtks->eta.push_back(tk->eta());
        seedtks->etaerr.push_back(tk->etaError());
        seedtks->phi.push_back(tk->phi());
        seedtks->phierr.push_back(tk->phiError());
        seedtks->minr.push_back(min_r);
        seedtks->nhits.push_back(tk->hitPattern().numberOfValidHits());
        seedtks->npxhits.push_back(tk->hitPattern().numberOfValidPixelHits());
        seedtks->nsthits.push_back(tk->hitPattern().numberOfValidStripHits());
        seedtks->npxlayers.push_back(tk->hitPattern().pixelLayersWithMeasurement());
        seedtks->nstlayers.push_back(tk->hitPattern().stripLayersWithMeasurement());
        seedtks->absdxybs.push_back(fabs(tk->dxy(*beamspot)));
        seedtks->dxybs.push_back(tk->dxy(*beamspot));
        seedtks->dxyerr.push_back(tk->dxyError());
        seedtks->nsigmadxybs.push_back(nsigmadxybs);
        seedtks->absnsigmadxybs.push_back(fabs(nsigmadxybs));
        seedtks->absdz.push_back(fabs(tk->dz(beamspot->position())));
        seedtks->dz.push_back(tk->dz(beamspot->position()));
        seedtks->dzerr.push_back(tk->dzError());
        seedtks->nsigmadz.push_back(nsigmadz);
        seedtks->absnsigmadz.push_back(fabs(nsigmadz));
        seedtks->chi2.push_back(tk->chi2());
        seedtks->ndof.push_back(tk->ndof());
        seedtks->chi2ndof.push_back((tk->chi2()/tk->ndof()));
        seedtks->vx.push_back(tk->vx());
        seedtks->vy.push_back(tk->vy());
        seedtks->vz.push_back(tk->vz());
        seedtks->cov.push_back(tk->covariance());
    }
    event.put(std::move(seedtks));

}

DEFINE_FWK_MODULE(MFVSeedTracksProducer);