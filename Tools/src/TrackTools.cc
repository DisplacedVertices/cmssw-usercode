#include "DataFormats/TrackReco/interface/Track.h"
#include "JMTucker/Tools/interface/AnalysisEras.h"
#include "JMTucker/Tools/interface/TrackRescaler.h"
#include "JMTucker/Tools/interface/TrackTools.h"

namespace jmt {
  bool pass_track(const reco::Track& tk, const int level, const int use_rescaled, const edm::Event* ev, const reco::BeamSpot* bs) {
    if (level >= 2) {
      if (!bs) throw std::invalid_argument("need beamspot for level 2");
      if (use_rescaled && !ev) throw std::invalid_argument("need event for level 2 with rescaling");
    }

    if (level < 0)
      return true;

    if (tk.pt() < 1 ||
        tk.hitPattern().pixelLayersWithMeasurement() < 2 ||
        tk.hitPattern().stripLayersWithMeasurement() < 6)
      return false;

    if (level >= 1 && !tk.hitPattern().hasValidHitInPixelLayer(PixelSubdetector::PixelBarrel,1))
      return false;

    if (level >= 2) {
      jmt::TrackRescaler track_rescaler;
      if (use_rescaled) {
        const int track_rescaler_which = jmt::TrackRescaler::w_JetHT; // JMTBAD which rescaling if ever a different one
        track_rescaler.setup(!ev->isRealData() && track_rescaler_which != -1,
                             jmt::AnalysisEras::pick(ev->id().event()), // JMTBAD hardcoded use of which == -1 = int.lumi. distributed
                             track_rescaler_which);
      }

      const auto rs = track_rescaler.scale(tk);
      auto pass_nsigmadxy = [&](const reco::Track& tk) { return fabs(tk.dxy(*bs)) / tk.dxyError() > 4; };
      if (use_rescaled == 0) {
        if (!pass_nsigmadxy(tk))
          return false;
      }
      else {
        const auto rs = track_rescaler.scale(tk);
        if (!pass_nsigmadxy(rs.rescaled_tk)) {
          if (use_rescaled > 0 || !pass_nsigmadxy(tk))
            return false;
        }
      }
    }

    return true;
  }
}
