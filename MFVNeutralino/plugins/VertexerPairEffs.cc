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
  const bool allow_duplicate_pairs;
  const bool verbose;

  // 1st index is min_ntracks, 2nd index is max_ntracks, with 0 inclusive, 1 unused
  TH1F* h_n_pairs[6][6];
  TH1F* h_n_merge[6][6];
  TH1F* h_n_erase[6][6];
  TH1D* h_pairs_d2d[6][6];
  TH1D* h_merge_d2d[6][6];
  TH1D* h_erase_d2d[6][6];
};

MFVVertexerPairEffs::MFVVertexerPairEffs(const edm::ParameterSet& cfg)
  : vpeff_token(consumes<VertexerPairEffs>(cfg.getParameter<edm::InputTag>("vpeff_src"))),
    allow_duplicate_pairs(cfg.getParameter<bool>("allow_duplicate_pairs")),
    verbose(cfg.getUntrackedParameter<bool>("verbose", false))
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

  std::vector<float> d2ds;

  if (verbose) printf("\nrun = %u, lumi = %u, event = %llu, npveffs = %d\n", event.id().run(), event.luminosityBlock(), event.id().event(), nvpeffs);

  for (int ivpeff = 0; ivpeff < nvpeffs; ++ivpeff) {
    const VertexerPairEff& vpeff = vpeffs->at(ivpeff);

    const int ntk_min = vpeff.ntkmin();
    const int ntk_max = vpeff.ntkmax();
    assert(ntk_min >= 2 && ntk_max <= 5 && ntk_min <= ntk_max);

    const float d2d = vpeff.d2d();

    if (!allow_duplicate_pairs) {
      bool seen = false;
      for (size_t i = 0, ie = d2ds.size(); i < ie; ++i) {
        if (fabs(d2d - d2ds.at(i)) < 0.000001) {
          seen = true;
          break;
        }
      }
      if (seen) continue;
      d2ds.push_back(d2d);
    }

    if (verbose) {
      printf("\tivpeff = %d, ntk_min = %d, ntk_max = %d, d2d = %f, kind = %d", ivpeff, ntk_min, ntk_max, d2d, vpeff.kind());
      printf("  tks0:"); for (auto tk : vpeff.tracks(0)) printf(" %u", tk);
      printf("  tks1:"); for (auto tk : vpeff.tracks(1)) printf(" %u", tk);
      printf("\n");
    }

    ++n_pairs[0][0];
    ++n_pairs[ntk_min][0];
    ++n_pairs[0][ntk_max];
    ++n_pairs[ntk_min][ntk_max];

    h_pairs_d2d[0][0]->Fill(d2d);
    h_pairs_d2d[ntk_min][0]->Fill(d2d);
    h_pairs_d2d[0][ntk_max]->Fill(d2d);
    h_pairs_d2d[ntk_min][ntk_max]->Fill(d2d);

    if (vpeff.kind() & VertexerPairEff::merge) {
      ++n_merge[0][0];
      ++n_merge[ntk_min][0];
      ++n_merge[0][ntk_max];
      ++n_merge[ntk_min][ntk_max];

      h_merge_d2d[0][0]->Fill(d2d);
      h_merge_d2d[ntk_min][0]->Fill(d2d);
      h_merge_d2d[0][ntk_max]->Fill(d2d);
      h_merge_d2d[ntk_min][ntk_max]->Fill(d2d);
    }

    if (vpeff.kind() & VertexerPairEff::erase) {
      ++n_erase[0][0];
      ++n_erase[ntk_min][0];
      ++n_erase[0][ntk_max];
      ++n_erase[ntk_min][ntk_max];

      h_erase_d2d[0][0]->Fill(d2d);
      h_erase_d2d[ntk_min][0]->Fill(d2d);
      h_erase_d2d[0][ntk_max]->Fill(d2d);
      h_erase_d2d[ntk_min][ntk_max]->Fill(d2d);
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
