#include <memory>
#include <TH1F.h>

#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "TrackingTools/TransientTrack/interface/TransientTrack.h"
#include "TrackingTools/TransientTrack/interface/TransientTrackBuilder.h"
#include "TrackingTools/Records/interface/TransientTrackRecord.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "DataFormats/BeamSpot/interface/BeamSpot.h"

#include "TrackingTools/PatternTools/interface/TwoTrackMinimumDistance.h"
#include "TrackingTools/IPTools/interface/IPTools.h"

//#define VTXDEBUG

class MFVTracksClusteringFromDisplacedSeed {
    public:
    struct Cluster 
    { 
      GlobalPoint seedPoint;  
      reco::TransientTrack seedingTrack;
      std::vector<reco::TransientTrack> tracks;
    };
	MFVTracksClusteringFromDisplacedSeed(const edm::ParameterSet &params);
	
	
        std::vector<Cluster> clusters(
	  const reco::Vertex    &pv,
	  const std::vector<reco::TransientTrack> & selectedTracks
	 );
	 
  double npv_weight;

    private:
	bool trackFilter(const reco::TrackRef &track) const;
        std::pair<std::vector<reco::TransientTrack>,GlobalPoint> nearTracks(const reco::TransientTrack &seed, const std::vector<reco::TransientTrack> & tracks, const reco::Vertex & primaryVertex) const;

//	unsigned int				maxNTracks;
        double 					min3DIPSignificance;
        double 					min3DIPValue;
        double 					clusterMaxDistance;
        double 					clusterMaxSignificance;
        double 					clusterScale;
        double 					clusterMinAngleCosine;

  TH1F* h_tcfds_trackip3dsuccess;
  TH1F* h_tcfds_trackip3d;
  TH1F* h_tcfds_trackip3dsig;
  TH1F* h_tcfds_seedtrackip3d;
  TH1F* h_tcfds_seedtrackip3dsig;
  TH1F* h_tcfds_mval;
  TH1F* h_tcfds_msig;
  TH1F* h_tcfds_distfrompv;
  TH1F* h_tcfds_dist;
  TH1F* h_tcfds_dotprodTrack;
  TH1F* h_tcfds_dotprodSeed;
  TH1F* h_tcfds_w;
  TH1F* h_tcfds_sel;
  TH1F* h_tcfds_disttimesscale;
  TH1F* h_tcfds_densitytimesdist;
  TH1F* h_tcfds_sumw;
};

