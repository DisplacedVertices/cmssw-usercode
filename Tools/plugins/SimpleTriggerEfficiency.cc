#include "TH1F.h"
#include "TH2F.h"
#include "CLHEP/Random/RandFlat.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/Common/interface/TriggerResults.h"
#include "FWCore/Common/interface/TriggerNames.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "FWCore/Utilities/interface/RandomNumberGenerator.h"

class SimpleTriggerEfficiency : public edm::EDAnalyzer {
public:
  explicit SimpleTriggerEfficiency(const edm::ParameterSet&);

private:
  virtual void analyze(const edm::Event&, const edm::EventSetup&);

  edm::InputTag trigger_results_src;
  std::map<std::string, unsigned> prescales;
  edm::Service<edm::RandomNumberGenerator> rng;

  bool pass_prescale(std::string) const;

  TH1F* triggers_pass_num;
  TH1F* triggers_pass_den;
  TH2F* triggers2d_pass_num;
  TH2F* triggers2d_pass_den;
};

SimpleTriggerEfficiency::SimpleTriggerEfficiency(const edm::ParameterSet& cfg) 
  : trigger_results_src(cfg.getParameter<edm::InputTag>("trigger_results_src")),
    triggers_pass_num(0),
    triggers_pass_den(0),
    triggers2d_pass_num(0),
    triggers2d_pass_den(0)
{
  if (cfg.existsAs<std::vector<std::string> >("prescale_paths")) {
    const std::vector<std::string>& prescale_paths = cfg.getParameter<std::vector<std::string> >("prescale_paths");
    const std::vector<unsigned>& prescale_values = cfg.getParameter<std::vector<unsigned> >("prescale_values");
    if (prescale_paths.size() != prescale_values.size())
      throw cms::Exception("SimpleTriggerEfficiency") << "size mismatch: prescale_paths: " << prescale_paths.size() << " prescale_values: " << prescale_values.size();
    for (size_t i = 0; i < prescale_paths.size(); ++i)
      prescales[prescale_paths[i]] = prescale_values[i];
    if (prescale_paths.size() > 0 && !rng.isAvailable())
      throw cms::Exception("SimpleTriggerEfficiency") << "RandomNumberGeneratorService not available for prescaling!\n";
  }
}

bool SimpleTriggerEfficiency::pass_prescale(std::string path) const {
  // prescales map is empty => all paths have prescale 1.
  if (prescales.size() == 0)
    return true;
  size_t pos = path.rfind("_v");
  if (pos != std::string::npos)
    path.erase(pos);
  std::map<std::string, unsigned>::const_iterator it = prescales.find(path);
  if (it == prescales.end())
    return false;
  const unsigned prescale = it->second;
  if (prescale == 0)
    return false;
  CLHEP::RandFlat rand(rng->getEngine());
  return rand.fire() < 1./prescale;
}

void SimpleTriggerEfficiency::analyze(const edm::Event& event, const edm::EventSetup&) {
  edm::Handle<edm::TriggerResults> trigger_results;
  event.getByLabel(trigger_results_src, trigger_results);
  const edm::TriggerNames& trigger_names = event.triggerNames(*trigger_results);
  const size_t npaths = trigger_names.size();

  if (triggers_pass_num == 0) {
    // Initialize the histograms now that we have the information on
    // the paths. The bin labels will store the path names. The
    // denominator histogram will just end up being filled nevents
    // times in each bin.
    edm::Service<TFileService> fs;

    triggers_pass_num = fs->make<TH1F>("triggers_pass_num", "", npaths, 0, npaths);
    triggers_pass_den = fs->make<TH1F>("triggers_pass_den", "", npaths, 0, npaths);

    triggers2d_pass_num = fs->make<TH2F>("triggers2d_pass_num", "", npaths, 0, npaths, npaths, 0, npaths);
    triggers2d_pass_den = fs->make<TH2F>("triggers2d_pass_den", "", npaths, 0, npaths, npaths, 0, npaths);
    
    TH1F* hists[2] = { triggers_pass_num, triggers_pass_den };
    TH2F* hists2d[2] = { triggers2d_pass_num, triggers2d_pass_den };
    for (size_t ipath = 0; ipath < npaths; ++ipath) {
      for (int ihist = 0; ihist < 2; ++ihist) {
	const size_t ibin = ipath + 1;
	const char* name = trigger_names.triggerName(ipath).c_str();
	hists  [ihist]->GetXaxis()->SetBinLabel(ibin, name);
	hists2d[ihist]->GetXaxis()->SetBinLabel(ibin, name);
	hists2d[ihist]->GetYaxis()->SetBinLabel(ibin, name);
      }
    }
  }
  else {
    // Throw an exception if  we're not using the exact same paths.
    const TH1F* hist = triggers_pass_num;
    for (size_t ipath = 0; ipath < npaths; ++ipath) {
      std::string bin_label(hist->GetXaxis()->GetBinLabel(ipath + 1));
      const std::string& path_name = trigger_names.triggerName(ipath);
      if (bin_label != path_name)
	throw cms::Exception("SimpleTriggerEfficiency") << "different trigger menu? path " << ipath << " had name " << bin_label << " before, now " << path_name;
    }
  }

  for (size_t ipath = 0; ipath < npaths; ++ipath) {
    triggers_pass_den->Fill(ipath);
    const bool iacc = trigger_results->accept(ipath) && pass_prescale(trigger_names.triggerName(ipath));
    if (iacc)
      triggers_pass_num->Fill(ipath);

    for (size_t jpath = 0; jpath < ipath; ++jpath) {
      triggers2d_pass_den->Fill(ipath, jpath);
      const bool jacc = trigger_results->accept(jpath) && pass_prescale(trigger_names.triggerName(jpath));
      if (iacc || jacc)
	triggers2d_pass_num->Fill(ipath, jpath);
    }
  }
}

DEFINE_FWK_MODULE(SimpleTriggerEfficiency);
