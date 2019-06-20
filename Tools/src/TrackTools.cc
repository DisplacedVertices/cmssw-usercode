#include "DataFormats/TrackReco/interface/Track.h"
#include "JMTucker/Tools/interface/TrackTools.h"

namespace jmt {
  bool pass_track(const reco::Track& tk, const int level, const reco::BeamSpot* bs) {
    if (level < 0)
      return true;

    if (level >= 2 && !bs)
      throw std::invalid_argument("need beamspot for level 2");

    return
      tk.pt() >= 1 &&
      tk.hitPattern().pixelLayersWithMeasurement() >= 2 &&
      tk.hitPattern().stripLayersWithMeasurement() >= 6 &&
      (level < 1 || tk.hitPattern().hasValidHitInPixelLayer(PixelSubdetector::PixelBarrel,1)) &&
      (level < 2 || fabs(tk.dxy(*bs)) / tk.dxyError() > 4)
      ;
  }
}
