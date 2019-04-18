#ifndef TrackMover_BTagSFHelper_h
#define TrackMover_BTagSFHelper_h

#include <cassert>
#include "TFile.h"
#include "TH2.h"
#include "BTagCalibrationStandalone.h"

class BTagSFHelper {
public:
  ~BTagSFHelper() {
    for (auto x : calibs)  delete x;
    for (auto x : readers) delete x;
  }

  enum { BH, BF, GH, ncalibs };
  enum { loose, tight, npoints };

  BTagSFHelper()
    : f_btageff(TFile::Open("btageff_background.root")),
      h_btageff{
        (TH2D*)f_btageff->Get("JMTBTagEfficiency/eff_bottom_3"), // 3 was for the "correct" tight wp
        (TH2D*)f_btageff->Get("JMTBTagEfficiency/eff_charm_3"),
        (TH2D*)f_btageff->Get("JMTBTagEfficiency/eff_light_3")
      }
  {
    const std::string tagger = "csvv2";
    const std::string calib_fns[ncalibs] = { "CSVv2_Moriond17_B_H.csv", "CSVv2_Moriond17_B_F.csv", "CSVv2_Moriond17_G_H.csv" };
    const int wpoints[npoints] = { BTagEntry::OP_LOOSE, BTagEntry::OP_TIGHT };

    for (auto fn : calib_fns) {
      auto calib = new BTagCalibration(tagger, fn);
      calibs.push_back(calib);

      for (auto wp : wpoints) {
        auto reader = new BTagCalibrationReader(BTagEntry::OperatingPoint(wp), "central", {"up", "down"});
        readers.push_back(reader);

        reader->load(*calib, BTagEntry::FLAV_B,    "comb");
        reader->load(*calib, BTagEntry::FLAV_UDSG, "incl");
      }
    }
  }

  const BTagCalibrationReader* reader(int calib, int wpoint) const {
    return readers.at(calib * npoints + wpoint);
  }
    
  struct value_and_error { double v; double e; };
  struct value_and_interval { double v; double d; double u; };

  BTagEntry::JetFlavor hadron2jetflavor(int x) const {
    if      (x == 0) return BTagEntry::FLAV_UDSG;
    else if (x == 4) return BTagEntry::FLAV_C;
    else if (x == 5) return BTagEntry::FLAV_B;
    assert(0);
  }

  value_and_error efficiency(int hadronflavor, double eta, double pt) const {
    const auto jf = hadron2jetflavor(hadronflavor);
    auto h = h_btageff[jf];
    const int bin = h->FindBin(eta, pt);
    return value_and_error{h->GetBinContent(bin), h->GetBinError(bin)};
  }

  value_and_interval scale_factor(int calib, int wpoint, int hadronflavor, double eta, double pt) const {
    const BTagCalibrationReader* read = reader(calib, wpoint);
    const BTagEntry::JetFlavor jf = hadron2jetflavor(hadronflavor);
    return value_and_interval {
      read->eval_auto_bounds("central", jf, eta, pt),
      read->eval_auto_bounds("down",    jf, eta, pt),
      read->eval_auto_bounds("up",      jf, eta, pt),
    };
  }

private:
  TFile* f_btageff;
  TH2D* h_btageff[3];
  std::vector<BTagCalibration*> calibs;
  std::vector<BTagCalibrationReader*> readers;
};

#endif
