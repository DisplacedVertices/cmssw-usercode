#include "TH1.h"
#include "TH2.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "JMTucker/Tools/interface/GenUtilities.h"

class MFVEXO12038SampleFilter : public edm::EDFilter {
public:
  explicit MFVEXO12038SampleFilter(const edm::ParameterSet&);

private:
  virtual bool filter(edm::Event&, const edm::EventSetup&);

  const edm::InputTag gen_particles_src;
  const std::string mode;
  const bool doing_h2x;
  const bool doing_chi2muqq;
  const int h2x_num;
  const double min_dbv;
  const double max_dbv;
  const double min_dvv;
  const double max_dvv;
  const bool diag_plots;
  
  TH1F* h_dbv[2][3];
  TH2F* h_dbv_2d[2];
  TH1F* h_dvv[2];
};

MFVEXO12038SampleFilter::MFVEXO12038SampleFilter(const edm::ParameterSet& cfg) 
  : gen_particles_src(cfg.getParameter<edm::InputTag>("gen_particles_src")),
    mode(cfg.getParameter<std::string>("mode")),
    doing_h2x(mode == "h2x"),
    doing_chi2muqq(mode == "chi2muqq"),
    h2x_num(cfg.getParameter<int>("h2x_num")),
    min_dbv(cfg.getParameter<double>("min_dbv")),
    max_dbv(cfg.getParameter<double>("max_dbv")),
    min_dvv(cfg.getParameter<double>("min_dvv")),
    max_dvv(cfg.getParameter<double>("max_dvv")),
    diag_plots(true)
{
  if (doing_h2x) {
    if (h2x_num < 1 || h2x_num > 3)
      throw cms::Exception("Configuration") << "with mode = h2x, h2x_num must be 1-3, got " << h2x_num;
  }
  else if (doing_chi2muqq) {
  }
  else
    throw cms::Exception("Configuration") << "mode must be either h2x or chi2muqq, got " << mode;

  if (diag_plots) {
    edm::Service<TFileService> fs;
    for (int j = 0; j < 2; ++j) {
      for (int i = 0; i < 3; ++i)
        h_dbv[j][i] = fs->make<TH1F>(TString::Format("h_dbv_%i_%i", j, i), "", 1000, 0, 100);
      h_dbv_2d[j] = fs->make<TH2F>(TString::Format("h_dbv_2d_%i", j), "", 50, 0, 100, 50, 0, 100);
      h_dvv[j] = fs->make<TH1F>(TString::Format("h_dvv_%i", j), "", 1000, 0, 100);
    }
  }
}

namespace {
  template <typename T>
  T mag(T x, T y) {
    return sqrt(x*x + y*y);
  }
}

bool MFVEXO12038SampleFilter::filter(edm::Event& event, const edm::EventSetup&) {
  edm::Handle<reco::GenParticleCollection> gen_particles;
  event.getByLabel(gen_particles_src, gen_particles);
  const size_t ngen = gen_particles->size();

  double v[2][3] = {{0}};

  if (doing_h2x) {
    std::vector<const reco::GenParticle*> strings;
    for (size_t igen = 0; igen < ngen; ++igen) {
      const reco::GenParticle& gen = gen_particles->at(igen);
      if (gen.status() == 3 && abs(gen.pdgId()) == 35) {
        assert(gen.numberOfDaughters() == 2);
        for (size_t idau = 0; idau < gen.numberOfDaughters(); ++idau) {
          const reco::Candidate* dau = gen.daughter(idau);
          int dauid = dau->pdgId();
          // https://espace.cern.ch/cms-exotica/long-lived/selection/MC2012.aspx
          // 600N114 = quarks where N is 1 2 or 3 for the lifetime selection
          assert(dauid/6000000 == 1);
          dauid %= 6000000;
          const int h2x = dauid / 1000;
          assert(h2x == 1 || h2x == 2 || h2x == 3);
          dauid %= h2x*1000;
          assert(dauid/100 == 1);
          dauid %= 100;
          assert(dauid/10 == 1);
          dauid %= 10;
          assert(dauid == 3 || dauid == 4);
          
          if (h2x != h2x_num || dauid != 4)
            return false;

          
        }
      }
    }
  }
  else if (doing_chi2muqq) {
    // Find the status-1 mu+ and mu- and use their vertices as the
    // decay positions.  The ones we want should have mother =
    // status-3 mu and grandmother = chi10, possibly with
    // generation(s) of status-2 mu with gammas in between.
    std::vector<const reco::GenParticle*> mus;
    for (size_t igen = 0; igen < ngen; ++igen) {
      const reco::GenParticle& gen = gen_particles->at(igen);
      if (gen.status() == 3 && abs(gen.pdgId()) == 13) {
        //printf("status-3 mu at %i\n", int(igen));
        bool found_chi10 = false;
        for (size_t imom = 0; imom < gen.numberOfMothers(); ++imom) {
          //printf("mother %i is an %i\n", int(imom), gen.mother(imom)->pdgId());
          if (gen.mother(imom)->pdgId() == 1000022)
            found_chi10 = true;
        }

        if (found_chi10) {
          //printf("found chi10\n");
          const reco::Candidate* dau = &gen;
          while (dau->status() != 1) {
            dau = daughter_with_id(dau, 13, true);
            assert(dau);
            //print_gen_and_daus(dau, "dau now", *gen_particles);
          }

          mus.push_back(dynamic_cast<const reco::GenParticle*>(dau));
        }
      }
    }

    if (mus.size() != 2) // || mus[0]->charge() * mus[1]->charge() != -1)
      throw cms::Exception("DumbCode", "didn't find the muons");

    for (int i = 0; i < 2; ++i) {
      v[i][0] = mus[i]->vx();
      v[i][1] = mus[i]->vy();
      v[i][2] = mus[i]->vz();
    }
  }

  const double dbv[2] = {
    mag(v[0][0], v[0][1]),
    mag(v[1][0], v[1][1])
  };
  const double dvv = mag(v[0][0] - v[1][0],
                         v[0][1] - v[1][1]);

  if (diag_plots) {
    h_dbv[0][0]->Fill(dbv[0]);
    h_dbv[0][1]->Fill(dbv[1]);
    h_dbv[0][2]->Fill(dbv[0]);
    h_dbv[0][2]->Fill(dbv[1]);
    h_dbv_2d[0]->Fill(dbv[0], dbv[1]);
    h_dvv[0]->Fill(dvv);
  }

  if (dbv[0] < min_dbv || dbv[0] > max_dbv ||
      dbv[1] < min_dbv || dbv[1] > max_dbv ||
      dvv < min_dbv || dvv > max_dvv)
    return false;

  if (diag_plots) {
    h_dbv[1][0]->Fill(dbv[0]);
    h_dbv[1][1]->Fill(dbv[1]);
    h_dbv[1][2]->Fill(dbv[0]);
    h_dbv[1][2]->Fill(dbv[1]);
    h_dbv_2d[1]->Fill(dbv[0], dbv[1]);
    h_dvv[1]->Fill(dvv);
  }

  return true;
}

DEFINE_FWK_MODULE(MFVEXO12038SampleFilter);
