#include "TH1.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "JMTucker/MFVNeutralinoFormats/interface/VertexerPairEff.h"

class MFVVertexerPairEffs : public edm::EDAnalyzer {
 public:
  explicit MFVVertexerPairEffs(const edm::ParameterSet&);
  void analyze(const edm::Event&, const edm::EventSetup&);

 private:
  const edm::EDGetTokenT<VertexerPairEffs> vpeff_token;

  // 1st index is min_ntracks, 2nd index is max_ntracks, with 0 inclusive, 1 unused
  TH1F* h_n_pairs[6][6];
  TH1F* h_n_merge[6][6];
  TH1F* h_n_erase[6][6];
  TH1D* h_pairs_d2d[6][6];
  TH1D* h_merge_d2d[6][6];
  TH1D* h_erase_d2d[6][6];
  TH1D* h_pairs_d3d[6][6];
  TH1D* h_merge_d3d[6][6];
  TH1D* h_erase_d3d[6][6];
};

MFVVertexerPairEffs::MFVVertexerPairEffs(const edm::ParameterSet& cfg)
  : vpeff_token(consumes<VertexerPairEffs>(cfg.getParameter<edm::InputTag>("vpeff_src")))
{
  edm::Service<TFileService> fs;

  for (int i = 0; i <= 5; ++i) {
    if (i == 1) continue;
    for (int j = 0; j <= 5; ++j) {
      if (j == 1 || (j >= 2 && i > j)) continue;

      h_n_pairs[i][j] = fs->make<TH1F>(TString::Format("h_n_pairs_mintk%i_maxtk%i", i, j), "", 100, 0, 100);
      h_n_merge[i][j] = fs->make<TH1F>(TString::Format("h_n_merge_mintk%i_maxtk%i", i, j), "", 100, 0, 100);
      h_n_erase[i][j] = fs->make<TH1F>(TString::Format("h_n_erase_mintk%i_maxtk%i", i, j), "", 100, 0, 100);

      h_pairs_d2d[i][j] = fs->make<TH1D>(TString::Format("h_pairs_d2d_mintk%i_maxtk%i", i, j), "", 4000, 0, 4);
      h_merge_d2d[i][j] = fs->make<TH1D>(TString::Format("h_merge_d2d_mintk%i_maxtk%i", i, j), "", 4000, 0, 4);
      h_erase_d2d[i][j] = fs->make<TH1D>(TString::Format("h_erase_d2d_mintk%i_maxtk%i", i, j), "", 4000, 0, 4);

      h_pairs_d3d[i][j] = fs->make<TH1D>(TString::Format("h_pairs_d3d_mintk%i_maxtk%i", i, j), "", 4000, 0, 4);
      h_merge_d3d[i][j] = fs->make<TH1D>(TString::Format("h_merge_d3d_mintk%i_maxtk%i", i, j), "", 4000, 0, 4);
      h_erase_d3d[i][j] = fs->make<TH1D>(TString::Format("h_erase_d3d_mintk%i_maxtk%i", i, j), "", 4000, 0, 4);
    }
  }
}

void MFVVertexerPairEffs::analyze(const edm::Event& event, const edm::EventSetup&) {
  edm::Handle<VertexerPairEffs> vpeffs;
  event.getByToken(vpeff_token, vpeffs);

  const int nvpeffs = int(vpeffs->size());

  int n_pairs[6][6] = {{0}};
  int n_merge[6][6] = {{0}};
  int n_erase[6][6] = {{0}};

  for (int ivpeff = 0; ivpeff < nvpeffs; ++ivpeff) {
    const VertexerPairEff& vpeff = vpeffs->at(ivpeff);

    const int ntk_min = vpeff.ntkmin();
    const int ntk_max = vpeff.ntkmax();
    assert(ntk_min >= 2 && ntk_max <= 5 && ntk_min <= ntk_max);

    const float d2d = vpeff.d2d();
    const float d3d = vpeff.d3d();

    ++n_pairs[0][0];
    ++n_pairs[ntk_min][0];
    ++n_pairs[0][ntk_max];
    ++n_pairs[ntk_min][ntk_max];

    h_pairs_d2d[0][0]->Fill(d2d);
    h_pairs_d2d[ntk_min][0]->Fill(d2d);
    h_pairs_d2d[0][ntk_max]->Fill(d2d);
    h_pairs_d2d[ntk_min][ntk_max]->Fill(d2d);

    h_pairs_d3d[0][0]->Fill(d3d);
    h_pairs_d3d[ntk_min][0]->Fill(d3d);
    h_pairs_d3d[0][ntk_max]->Fill(d3d);
    h_pairs_d3d[ntk_min][ntk_max]->Fill(d3d);

    if (vpeff.kind() == VertexerPairEff::merge) {
      ++n_merge[0][0];
      ++n_merge[ntk_min][0];
      ++n_merge[0][ntk_max];
      ++n_merge[ntk_min][ntk_max];

      h_merge_d2d[0][0]->Fill(d2d);
      h_merge_d2d[ntk_min][0]->Fill(d2d);
      h_merge_d2d[0][ntk_max]->Fill(d2d);
      h_merge_d2d[ntk_min][ntk_max]->Fill(d2d);

      h_merge_d3d[0][0]->Fill(d3d);
      h_merge_d3d[ntk_min][0]->Fill(d3d);
      h_merge_d3d[0][ntk_max]->Fill(d3d);
      h_merge_d3d[ntk_min][ntk_max]->Fill(d3d);
    }

    if (vpeff.kind() == VertexerPairEff::erase) {
      ++n_erase[0][0];
      ++n_erase[ntk_min][0];
      ++n_erase[0][ntk_max];
      ++n_erase[ntk_min][ntk_max];

      h_erase_d2d[0][0]->Fill(d2d);
      h_erase_d2d[ntk_min][0]->Fill(d2d);
      h_erase_d2d[0][ntk_max]->Fill(d2d);
      h_erase_d2d[ntk_min][ntk_max]->Fill(d2d);

      h_erase_d3d[0][0]->Fill(d3d);
      h_erase_d3d[ntk_min][0]->Fill(d3d);
      h_erase_d3d[0][ntk_max]->Fill(d3d);
      h_erase_d3d[ntk_min][ntk_max]->Fill(d3d);
    }
  }

  for (int i = 0; i <= 5; ++i) {
    if (i == 1) continue;
    for (int j = 0; j <= 5; ++j) {
      if (j == 1 || (j >= 2 && i > j)) continue;

      h_n_pairs[i][j]->Fill(n_pairs[i][j]);
      h_n_merge[i][j]->Fill(n_merge[i][j]);
      h_n_erase[i][j]->Fill(n_erase[i][j]);
    }
  }
}

DEFINE_FWK_MODULE(MFVVertexerPairEffs);
