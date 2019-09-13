#include "TH2.h"
#include "JMTucker/MFVNeutralino/interface/Ntuple.h"
#include "JMTucker/Tools/interface/NtupleReader.h"

int main(int argc, char** argv) {
  jmt::NtupleReader<mfv::MiniNtuple2> nr;
  nr.init_options("mfvMiniTree2/t", "CountV27mm", "nr_ntuplev27mm");
  if (!nr.parse_options(argc, argv) || !nr.init()) return 1;
  auto& nt = nr.nt();
  auto& vs = nt.vertices();

  auto h_n = new TH1D("h_n", "", 8, 0, 8);
  auto h_w = new TH1D("h_w", "", 8, 0, 8);
  auto h_b_n = new TH1D("h_b_n", "", 8, 0, 8);
  auto h_b_w = new TH1D("h_b_w", "", 8, 0, 8);
  for (auto h : {h_n, h_w, h_b_n, h_b_w}) {
    h->GetXaxis()->SetBinLabel(1, "1v, 3-or-4 track");
    h->GetXaxis()->SetBinLabel(2, "1v, 3 track");
    h->GetXaxis()->SetBinLabel(3, "1v, 4 track");
    h->GetXaxis()->SetBinLabel(4, "1v, >=5 track");
    h->GetXaxis()->SetBinLabel(5, ">=2v, 3-or-4 track");
    h->GetXaxis()->SetBinLabel(6, ">=2v, 3 track");
    h->GetXaxis()->SetBinLabel(7, ">=2v, 4 track");
    h->GetXaxis()->SetBinLabel(8, ">=2v, >=5 track");
  }

  nr.loop([&]() {
      int c[8] = {0};
      for (int i : vs.pass(nt.bs())) {
        const int ntk = vs.ntracks(i);
        if      (ntk == 3) ++c[3], ++c[7];
        else if (ntk == 4) ++c[4], ++c[7];
        else if (ntk >= 5) ++c[5];
      }

      const double w = nr.weight();
      for (int ntk : {7,3,4,5}) {
        if (c[ntk] == 0) continue;
        const int i = 4*(c[ntk] >= 2) + (ntk == 7 ? 0 : ntk-2); // see axis labels above
        h_n->Fill(i);
        h_w->Fill(i, w);
        if (nt.gentruth().saw_b()) {
          h_b_n->Fill(i);
          h_b_w->Fill(i, w);
        }
      }

      return std::make_pair(true, w);
    });
}
