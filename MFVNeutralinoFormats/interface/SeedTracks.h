#ifndef JMTucker_MFVNeutralinoFormats_interface_SeedTracks_h
#define JMTucker_MFVNeutralinoFormats_interface_SeedTracks_h

#include <vector>
#include "TLorentzVector.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "DataFormats/TrackReco/interface/TrackBase.h"
#include "DataFormats/TrackReco/interface/HitPattern.h"
#include "DataFormats/BeamSpot/interface/BeamSpot.h"
// #include "JMTucker/MFVNeutralinoFormats/interface/HitPattern.h"

struct MFVSeedTracks { 
    typedef unsigned char uchar;
    typedef unsigned short ushort;
    typedef unsigned int uint;

    float bsx;
    float bsy;
    float bsz;
    
    MFVSeedTracks() {
        nseedtracks = neleseed = nmuseed = 0;
        for (int i = 0; i < 2; ++i) {
            for (int j = 0; j < 3; ++j)
              gen_lsp_decay[i*3+j] = 0;
        }   

    }
    int nseedtracks;
    int neleseed;
    int nmuseed;
    float gen_lsp_decay[2*3];

    std::vector<float> id;
    std::vector<float> key;
    std::vector<float> tk_idx;
    std::vector<double> p;
    std::vector<double> pt;
    std::vector<float> pterr;
    std::vector<float> eta;
    std::vector<float> etaerr;
    std::vector<float> phi;
    std::vector<float> phierr;
    std::vector<int> minr;
    std::vector<int> nhits;
    std::vector<int> npxhits;
    std::vector<int> nsthits;
    std::vector<int> npxlayers;
    std::vector<int> nstlayers;
    std::vector<float> absdxybs;
    std::vector<float> dxybs;
    std::vector<float> dxyerr;
    std::vector<float> nsigmadxybs;
    std::vector<float> absnsigmadxybs;
    std::vector<float> absdz;
    std::vector<float> dz;
    std::vector<float> dzerr;
    std::vector<float> nsigmadz;
    std::vector<float> absnsigmadz;
    std::vector<double> chi2;
    std::vector<double> ndof;
    std::vector<double> chi2ndof;
    std::vector<double> vx;
    std::vector<double> vy;
    std::vector<double> vz;
    std::vector<reco::TrackBase::CovarianceMatrix> cov;

};

typedef std::vector<MFVSeedTracks> MFVSeedTracksCollection;

namespace mfv {
  typedef std::vector<MFVSeedTracks> SeedTracksCollection;
}

#endif