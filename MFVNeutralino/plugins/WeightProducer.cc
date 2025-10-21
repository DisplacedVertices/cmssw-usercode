#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/LuminosityBlock.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "JMTucker/Formats/interface/MergeablePOD.h"
#include "JMTucker/MFVNeutralinoFormats/interface/Event.h"
#include "JMTucker/MFVNeutralinoFormats/interface/VertexAux.h" //Abby change
#include "JMTucker/Tools/interface/Year.h"
#include "correction.h"  //Abby change begin
#include "RoccoR/RoccoR.h"
#include "RoccoR/RoccoR.cc"
#include "TRandom3.h"   //Abby change end

class MFVWeightProducer : public edm::EDProducer {
public:
  explicit MFVWeightProducer(const edm::ParameterSet&);
  virtual void endLuminosityBlock(const edm::LuminosityBlock&, const edm::EventSetup&) override;
  virtual void produce(edm::Event&, const edm::EventSetup&) override;

private:
  const edm::EDGetTokenT<jmt::MergeableInt> nevents_token;
  const edm::EDGetTokenT<jmt::MergeableFloat> sumweight_token;
  const bool throw_if_no_mcstat;
  const edm::EDGetTokenT<MFVEvent> mevent_token;
  const edm::EDGetTokenT<MFVVertexAuxCollection> vertex_token; //Abby change
  const bool enable;
  const bool prints;
  const bool histos;

  const double partial_mc_stats_weight;
  const bool weight_gen;
  const bool weight_gen_sign_only;
  const bool weight_pileup;
  const bool weight_pileup_2;
  const std::vector<double> pileup_weights;
  double pileup_weight(int mc_npu) const;
  const bool weight_npv;
  const std::vector<double> npv_weights;
  double npv_weight(int mc_npu) const;
  const std::vector<int> misc_weight_indices;
  const bool apply_lepsf; //Abby changes begin
  const bool apply_roccor;
  const std::string pujson;
  const std::string elejson;
  const std::string mujson;
  // const std::string roccor;
  double run(const std::unique_ptr<correction::CorrectionSet>&, const std::string&, const std::map<std::string, correction::Variable::Type>&) const;
  RoccoR rc;
  std::unique_ptr<correction::CorrectionSet> pu_cset;
  std::unique_ptr<correction::CorrectionSet> mu_cset;
  std::unique_ptr<correction::CorrectionSet> ele_cset; //Abby changes end

  TH1D* h_gensign;
  TH1D* h_npu;
  TH1D* h_npv;
  

  enum { sum_nevents_total, sum_gen_weight_total, sum_gen_weight, sum_pileup_weight, sum_npv_weight, sum_weight, yearcode_x_nfiles, sum_weight_ren_up, sum_weight_ren_dn, sum_weight_fac_up, sum_weight_fac_dn, sum_weight_ren_fac_up, sum_weight_ren_fac_dn, n_sums };
  TH1D* h_sums;

  enum { lsum_nevents_total, sum_leprecoSF, sum_lepidSF, sum_lepisoSF, sum_leptriggerSF, sum_leptotalSF, lsum_weight}; //Abby change
  TH1D* h_lepsums; //Abby change
};

MFVWeightProducer::MFVWeightProducer(const edm::ParameterSet& cfg)
  : nevents_token(consumes<jmt::MergeableInt, edm::InLumi>(edm::InputTag("mcStat", "nEvents"))),
    sumweight_token(consumes<jmt::MergeableFloat, edm::InLumi>(edm::InputTag("mcStat", "sumWeight"))),
    throw_if_no_mcstat(cfg.getParameter<bool>("throw_if_no_mcstat")),
    mevent_token(consumes<MFVEvent>(cfg.getParameter<edm::InputTag>("mevent_src"))),
    vertex_token(consumes<MFVVertexAuxCollection>(cfg.getParameter<edm::InputTag>("vertex_src"))), //Abby change
    enable(cfg.getParameter<bool>("enable")),
    prints(cfg.getUntrackedParameter<bool>("prints", false)),
    histos(cfg.getUntrackedParameter<bool>("histos", true)),
    partial_mc_stats_weight(cfg.getParameter<double>("partial_mc_stats_weight")),
    weight_gen(cfg.getParameter<bool>("weight_gen")),
    weight_gen_sign_only(cfg.getParameter<bool>("weight_gen_sign_only")),
    weight_pileup(cfg.getParameter<bool>("weight_pileup")),
    weight_pileup_2(cfg.getParameter<bool>("weight_pileup_2")), //Abby change
    pileup_weights(cfg.getParameter<std::vector<double> >("pileup_weights")),
    weight_npv(cfg.getParameter<bool>("weight_npv")),
    npv_weights(cfg.getParameter<std::vector<double> >("npv_weights")),
    misc_weight_indices(cfg.getParameter<std::vector<int>>("misc_weight_indices")), //Abby change added comma on the end here
    apply_lepsf(cfg.getParameter<bool>("apply_lepsf")), //Abby change begin
    apply_roccor(cfg.getParameter<bool>("apply_roccor")),
    pujson(cfg.getParameter<std::string>("pujson")),
    elejson(cfg.getParameter<std::string>("elejson")),
    mujson(cfg.getParameter<std::string>("mujson")) //Abby change end
    
{
  if (weight_gen + weight_gen_sign_only > 1)
    throw cms::Exception("Configuration", "can only set one of weight_gen, weight_gen_sign_only");

  produces<double>();

  //FIXME way to turn off?    //Abby change begin
  produces<double>("lepsfup"); //syst up 
  produces<double>("lepsfdown"); //syst down 
  
  std::string year = std::to_string(int(MFVNEUTRALINO_YEAR));

  if (year == "20161") rc.init(edm::FileInPath("RoccoR/RoccoR2016aUL.txt").fullPath()); //FIXME year is hardcoded
  else if (year == "20162") rc.init(edm::FileInPath("RoccoR/RoccoR2016bUL.txt").fullPath()); //FIXME year is hardcoded
  else if (year == "2017")  { 
    rc.init(edm::FileInPath("RoccoR/RoccoR2017UL.txt").fullPath()); //FIXME year is hardcoded

  }
  else if (year == "2018")  {
    rc.init(edm::FileInPath("RoccoR/RoccoR2018UL.txt").fullPath()); //FIXME year is hardcoded
  }


  pu_cset = correction::CorrectionSet::from_file(pujson); 
  mu_cset = correction::CorrectionSet::from_file(mujson); 
  ele_cset = correction::CorrectionSet::from_file(elejson); //Abby change end

  if (histos) {
    edm::Service<TFileService> fs;
    TH1::SetDefaultSumw2();

    h_gensign = fs->make<TH1D>("h_gensign", ";gen weight sign;events", 2, -1.5, 1.5);
    h_npu = fs->make<TH1D>("h_npu", ";number of pileup interactions;events", 100, 0, 100);
    h_npv = fs->make<TH1D>("h_npv", ";number of primary vertices;events", 100, 0, 100);

    h_sums = fs->make<TH1D>("h_sums", TString::Format("partial_mc_stats_weight = %.3f", partial_mc_stats_weight), n_sums+1, 0, n_sums+1);
    int ibin = 1;
    for (const char* x : { "sum_nevents_total", "sum_gen_weight_total", "sum_gen_weight", "sum_pileup_weight", "sum_npv_weight", "sum_weight", "yearcode_x_nfiles", "sum_weight_ren_up", "sum_weight_ren_dn", "sum_weight_fac_up", "sum_weight_fac_dn", "sum_weight_ren_fac_up", "sum_weight_ren_fac_dn", "n_sums" })
      h_sums->GetXaxis()->SetBinLabel(ibin++, x);
    h_sums->Fill(yearcode_x_nfiles, MFVNEUTRALINO_YEARCODE);

    h_lepsums = fs->make<TH1D>("h_lepsums", "partial_mc_stats_weight = 1", 8, 0, 8); //Abby change begin
    int xbin = 1;
    for (const char* b : {"sum_nevents_total", "sum_leprecoSF", "sum_lepidSF", "sum_lepisoSF", "sum_leptriggerSF", "sum_leptotalSF", "sum_weight"})
      h_lepsums->GetXaxis()->SetBinLabel(xbin++, b); //Abby change end
  }
}

void MFVWeightProducer::endLuminosityBlock(const edm::LuminosityBlock& lumi, const edm::EventSetup&) {
  if (lumi.run() == 1) { // no lumi.isRealData()
    edm::Handle<jmt::MergeableInt> nEvents;
    edm::Handle<jmt::MergeableFloat> sumWeight;
    lumi.getByToken(nevents_token, nEvents);
    lumi.getByToken(sumweight_token, sumWeight);

    if (nEvents.isValid() && sumWeight.isValid()) {
      if (prints)
        printf("MFVWeight::beginLuminosityBlock r: %u l: %u nEvents: %i  sumWeight: %f\n", lumi.run(), lumi.luminosityBlock(), nEvents->get(), sumWeight->get());
      
      if (histos) {
        h_sums->Fill(sum_nevents_total,        partial_mc_stats_weight * nEvents->get());
        h_sums->Fill(sum_gen_weight_total,     partial_mc_stats_weight * sumWeight->get());
	h_lepsums->Fill(lsum_nevents_total,     partial_mc_stats_weight * nEvents->get()); //Abby change
      }
    }
    else if (throw_if_no_mcstat)
      throw cms::Exception("ProductNotFound", "MCStatProducer luminosity branch products not found!");
  }
}

double MFVWeightProducer::pileup_weight(int mc_npu) const {
  if (mc_npu < 0 || mc_npu >= int(pileup_weights.size()))
    return 0;
  else
    return pileup_weights[mc_npu];
}

double MFVWeightProducer::npv_weight(int mc_npv) const {
  if (mc_npv < 0 || mc_npv >= int(npv_weights.size()))
    return 0;
  else
    return npv_weights[mc_npv];
}


double MFVWeightProducer::run (const std::unique_ptr<correction::CorrectionSet>& cset, const std::string& key, const std::map<std::string, correction::Variable::Type>& values) const {
  correction::Correction::Ref sf = cset->at(key);
  std::vector<correction::Variable::Type> inputs;
  // std::cout << "run fcn called ... " << std::endl;
  for (const correction::Variable& input: sf->inputs()) { 
    // std::cout << "input name : " << input.name() << std::endl;
    inputs.push_back(values.at(input.name()));
  }
  double result = sf->evaluate(inputs);
  return result;
}


void MFVWeightProducer::produce(edm::Event& event, const edm::EventSetup&) {
  if (event.isRealData() != (event.id().run() != 1))
    throw cms::Exception("BadAssumption") << "isRealData = " << event.isRealData() << " and run = " << event.id().run();

  if (histos)
    h_sums->Fill(n_sums);

  if (prints)
    printf("MFVWeight: r,l,e: %u, %u, %llu  ", event.id().run(), event.luminosityBlock(), event.id().event());

  std::unique_ptr<double> weight(new double(1.));
  std::unique_ptr<double> weight_up(new double(1.)); //Abby change
  std::unique_ptr<double> weight_down(new double(1.)); //Abby change

  if (enable) {
    edm::Handle<MFVEvent> mevent;
    event.getByToken(mevent_token, mevent);

    if (!event.isRealData()) {
      if (weight_gen || weight_gen_sign_only) {
        if (prints)
          printf("gen_weight: %g  ", mevent->gen_weight);
        if (histos) {
          h_gensign->Fill(mevent->gen_weight > 0 ? 1 : -1);
          h_sums->Fill(sum_gen_weight, mevent->gen_weight);
        }
        if (weight_gen_sign_only) {
          if (mevent->gen_weight < 0) { //Abby change added curly bracket here
            *weight *= -1;
	    *weight_up *= -1; //Abby change begin
            *weight_down *= -1;
	  } //Abby change end
        }
        else { //Abby change added curly bracket here
          *weight *= mevent->gen_weight;
	  *weight_up *= mevent->gen_weight; //Abby change begin
          *weight_down *= mevent->gen_weight;
	} //Abby change end
      }

      if (weight_pileup) {
        const double pu_w = pileup_weight(mevent->npu);
        if (prints)
          printf("mc_npu: %g  pu weight: %g  ", mevent->npu, pu_w);
        if (histos) {
          h_npu->Fill(mevent->npu);
          h_sums->Fill(sum_pileup_weight, pu_w);
        }
        *weight *= pu_w;
	*weight_up *= pu_w; //Abby change
        *weight_down *= pu_w; //Abby change
      }

      //pulling from json //Abby change begin
      if (weight_pileup_2) {

        double PUsf = 1.0;
        double PUsf_up = 1.0; 
        double PUsf_down = 1.0;
        std::map<std::string, correction::Variable::Type> values {
          {"NumTrueInteractions", mevent->npu}, 
          {"weights", "nominal"}, 
        };

        std::map<std::string, correction::Variable::Type> values_up {
          {"NumTrueInteractions", mevent->npu}, 
          {"weights", "up"}, // variation
        };

        std::map<std::string, correction::Variable::Type> values_down {
          {"NumTrueInteractions", mevent->npu}, 
          {"weights", "down"}, // variation
        };
        // //PU UL SF from Central 
        int year = int(MFVNEUTRALINO_YEAR);

        if (year == 20161 || year == 20162) { 
          PUsf = run(pu_cset, "Collisions16_UltraLegacy_goldenJSON", values);
          PUsf_up = run(pu_cset, "Collisions16_UltraLegacy_goldenJSON", values_up);
          PUsf_down = run(pu_cset, "Collisions16_UltraLegacy_goldenJSON", values_down);
        }
        else if (year == 2017) { 
          PUsf = run(pu_cset, "Collisions17_UltraLegacy_goldenJSON", values);
          PUsf_up = run(pu_cset, "Collisions17_UltraLegacy_goldenJSON", values_up);
          PUsf_down = run(pu_cset, "Collisions17_UltraLegacy_goldenJSON", values_down);

        }
        else if (year == 2018) { 
          PUsf = run(pu_cset, "Collisions18_UltraLegacy_goldenJSON", values);
          PUsf_up = run(pu_cset, "Collisions18_UltraLegacy_goldenJSON", values_up);
          PUsf_down = run(pu_cset, "Collisions18_UltraLegacy_goldenJSON", values_down);

        }

        if (histos) {
          h_npu->Fill(mevent->npu);
          h_sums->Fill(sum_pileup_weight, PUsf);
        }
        *weight *= PUsf;
        *weight_up *= PUsf_up;
        *weight_down *= PUsf_down;
      } //Abby change end

      if (weight_npv) {
        const double npv_w = npv_weight(mevent->npv);
        if (prints)
          printf("mc_npv: %i  npv weight: %g  ", mevent->npv, npv_w);
        if (histos) {
          h_npv->Fill(mevent->npv);
          h_sums->Fill(sum_npv_weight, npv_w);
        }
        *weight *= npv_w;
	*weight_up *= npv_w; //Abby change
        *weight_down *= npv_w; //Abby change
	
      }

      for (int mwi : misc_weight_indices) {
        const double w = mevent->misc[mwi];
        if (prints)
          printf("misc weight %i: %g  ", mwi, w);
        *weight *= w;
	*weight_up *= w; //Abby change
        *weight_down *= w; //Abby change
      }

      //Lepton SF workspace //Abby changes begin 
      if (apply_lepsf) {
        double total_lepsf = 1; 
        double total_lepIDsf = 1; //for histos; in case there are > 1 SV with a leading lepton 
        double lepIDsf = 1;
        double lepRECOsf = 1;
        double total_lepRECOsf = 1; //for histos; in case there are > 1 SV with a leading lepton 
        double lepISOsf = 1;
        double total_lepISOsf = 1; //for histos; in case there are > 1 SV with a leading lepton 
        double lepTRsf = 1;
        double total_lepTRsf = 1; //for histos; in case there are > 1 SV with a leading lepton

        double total_lepsf_down = 1;
        double lepIDsf_down = 1;
        double lepRECOsf_down = 1;
        double lepISOsf_down = 1;
        double lepTRsf_down = 1;

        double total_lepsf_up = 1;
        double lepIDsf_up = 1;
        double lepRECOsf_up = 1;
        double lepISOsf_up = 1;
        double lepTRsf_up = 1;

        //step 1 : get the leading selected lepton (the one that passes all selections; hltmatched, ID, iso, pT, eta)
        std::vector<float> lepinSV_pt;
        std::vector<float> lepinSV_eta;
        std::vector<float> lepinSV_type; //0 == mu, 1 == ele
        std::vector<int> lepinSV_hlt; // index corresponds to {30.0, 35.0, 38.0, 120.0, 55.0, 27.0, 30.0, 53.0, 180.0, 205.0}

        edm::Handle<MFVVertexAuxCollection> auxes;
        event.getByToken(vertex_token, auxes);

        const int nsv = int(auxes->size());
        for (int isv = 0; isv < nsv; ++isv) {
          const MFVVertexAux& aux = auxes->at(isv);

          // std::cout << " nsv : " << isv << "leading mu : " << aux.leading_selmu_pt.size() << " leading ele : " << aux.leading_selele_pt.size() << std::endl;
          //could either be size 0 or size 1
          for (size_t imu = 0; imu < aux.leading_selmu_pt.size(); ++imu) {
            lepinSV_pt.push_back(aux.leading_selmu_pt[imu]);
            lepinSV_eta.push_back(aux.leading_selmu_eta[imu]);
            lepinSV_type.push_back(0);
            lepinSV_hlt.push_back(aux.leading_selmu_hlt[imu]);
          }
          for (size_t iel = 0; iel < aux.leading_selele_pt.size(); ++iel) {
            lepinSV_pt.push_back(aux.leading_selele_pt[iel]);
            lepinSV_eta.push_back(aux.leading_selele_eta[iel]);
            lepinSV_type.push_back(1);
            lepinSV_hlt.push_back(aux.leading_selele_hlt[iel]);

          }
        }
        

        //step 2 : depending on the lepton, get the SFs 
        //need to loop through all the possible SV that has a leading lepton that passes selections and apply SF to those leptons 
        for (size_t ilep=0; ilep < lepinSV_type.size(); ilep++) { 
          if (lepinSV_type[ilep] == 0) { //lepinSV is mu;

            std::map<std::string, correction::Variable::Type> values {
              {"pt", lepinSV_pt[ilep]}, // muon transverse momentum
              {"eta", lepinSV_eta[ilep]}, // muon absolute pseudorapidity
              {"scale_factors", "nominal"}, // variation
            };
  
            std::map<std::string, correction::Variable::Type> values_up {
              {"pt", lepinSV_pt[ilep]}, // muon transverse momentum
              {"eta", lepinSV_eta[ilep]}, // muon absolute pseudorapidity
              {"scale_factors", "systup"}, // variation
            };

            std::map<std::string, correction::Variable::Type> values_down {
              {"pt", lepinSV_pt[ilep]}, // muon transverse momentum
              {"eta", lepinSV_eta[ilep]}, // muon absolute pseudorapidity
              {"scale_factors", "systdown"}, // variation
            };

            // TrackerMuon Reconstruction UL scale factor
            if ( lepinSV_pt[ilep] > 40.0) {  //lower limit is 40 for RECO SF? 
              lepRECOsf = run(mu_cset, "NUM_TrackerMuons_DEN_genTracks", values);
              lepRECOsf_up = run(mu_cset, "NUM_TrackerMuons_DEN_genTracks", values_up);
              lepRECOsf_down = run(mu_cset, "NUM_TrackerMuons_DEN_genTracks", values_down);
  
            }
            // Medium ID UL scale factor, down/up variations
            if (lepinSV_pt[ilep] > 15.0) {  //lower limit is 15 GeV for ID SF, ISO SF
              lepIDsf = run(mu_cset, "NUM_MediumID_DEN_TrackerMuons", values);
              lepIDsf_up = run(mu_cset, "NUM_MediumID_DEN_TrackerMuons", values_up);
              lepIDsf_down = run(mu_cset, "NUM_MediumID_DEN_TrackerMuons", values_down);

              //ISO UL scale factor 
              lepISOsf = run(mu_cset, "NUM_TightRelIso_DEN_MediumID", values);
              lepISOsf_up = run(mu_cset, "NUM_TightRelIso_DEN_MediumID", values_up);
              lepISOsf_down = run(mu_cset, "NUM_TightRelIso_DEN_MediumID", values_down);

            }
            // // Trigger UL systematic uncertainty only
            // if (lepinSV_pt[ilep] > 26.0) { //lower limit is 26GeV for Trigger SF 
            //   lepTRsf = run(mu_cset, "NUM_IsoMu24_DEN_CutBasedIdTight_and_PFIsoTight", values);
            //   lepTRsf_up = run(mu_cset, "NUM_IsoMu24_DEN_CutBasedIdTight_and_PFIsoTight", values_up);
            //   lepTRsf_down = run(mu_cset, "NUM_IsoMu24_DEN_CutBasedIdTight_and_PFIsoTight", values_down);
            // } 
            
            //placeholder trigger SF : 0.99 +- 0.05 (for leptons passing the minimum pT requirements); 
            // also, just apply it to one lepton per event; not per SV 
            if (ilep < 1) { 
              lepTRsf = 0.99;
              lepTRsf_up = 0.995;
              lepTRsf_down = 0.985;
            }
          }
          else { //lepinSV is an electron 
            // int year = 2017;
            std::string year = std::to_string(int(MFVNEUTRALINO_YEAR));

            std::map<std::string, correction::Variable::Type> values {
              {"year", year}, //year
              {"ValType", "sf"}, // variation
              {"WorkingPoint",  "Tight"}, //working point
              {"pt", lepinSV_pt[ilep]}, // electron transverse momentum
              {"eta", lepinSV_eta[ilep]}, // electron absolute pseudorapidity
            };
            std::map<std::string, correction::Variable::Type> values_up {
              {"year", year}, //year
              {"ValType", "sfup"}, // variation
              {"WorkingPoint",  "Tight"}, //working point
              {"pt", lepinSV_pt[ilep]}, // electron transverse momentum
              {"eta", lepinSV_eta[ilep]}, // electron absolute pseudorapidity
            };

            std::map<std::string, correction::Variable::Type> values_down {
              {"year", year}, //year
              {"ValType", "sfdown"}, // variation
              {"WorkingPoint",  "Tight"}, //working point
              {"pt", lepinSV_pt[ilep]}, // electron transverse momentum
              {"eta", lepinSV_eta[ilep]}, // electron absolute pseudorapidity
            };

            if (lepinSV_pt[ilep] > 10.0) { 
              lepRECOsf = run(ele_cset, "UL-Electron-ID-SF", values);
              lepRECOsf_up = run(ele_cset, "UL-Electron-ID-SF", values_up);
              lepRECOsf_down = run(ele_cset, "UL-Electron-ID-SF", values_down);
  
            }
            //placeholder trigger SF : 0.99 +- 0.05 (for leptons passing the minimum pT requirements)
            // also, just apply it to one lepton per event; not per SV 
            if (ilep < 1) { 
              lepTRsf = 0.99;
              lepTRsf_up = 0.995;
              lepTRsf_down = 0.985;
            }
          }

          total_lepsf *= lepRECOsf*lepISOsf*lepIDsf*lepTRsf;
          total_lepsf_up *= lepRECOsf_up*lepISOsf_up*lepIDsf_up*lepTRsf_up;
          total_lepsf_down *= lepRECOsf_down*lepISOsf_down*lepIDsf_down*lepTRsf_down;

          //to be used in histos primarily 
          total_lepRECOsf *= lepRECOsf;
          total_lepISOsf *= lepISOsf;
          total_lepIDsf *= lepIDsf;
          total_lepTRsf *= lepTRsf;
          // std::cout << " total lepsf : " << total_lepsf << std::endl;
        }

        if (histos) {
          h_lepsums->Fill(sum_leprecoSF, total_lepRECOsf);  
          h_lepsums->Fill(sum_lepidSF, total_lepIDsf); 
          h_lepsums->Fill(sum_lepisoSF, total_lepISOsf); 
          h_lepsums->Fill(sum_leptriggerSF, total_lepTRsf);
          h_lepsums->Fill(sum_leptotalSF, total_lepsf);
        }

        *weight *= total_lepsf;
        *weight_up *= total_lepsf_up;
        *weight_down *= total_lepsf_down;
        // std::cout << "total lep sf : " << total_lepsf << std::endl;
      } //Abby changes end
      
      // Fill in sumw entries for renormalization / factorization scale uncertainty
      if (histos) {

        double weight_ren_up = mevent->ren_weight_up;
        double weight_ren_dn = mevent->ren_weight_dn;
        double weight_fac_up = mevent->fac_weight_up;
        double weight_fac_dn = mevent->fac_weight_dn;

        h_sums->Fill(sum_weight_ren_up, *weight*weight_ren_up);
        h_sums->Fill(sum_weight_ren_dn, *weight*weight_ren_dn);
        h_sums->Fill(sum_weight_fac_up, *weight*weight_fac_up);
        h_sums->Fill(sum_weight_fac_dn, *weight*weight_fac_dn);
        h_sums->Fill(sum_weight_ren_fac_up, *weight*weight_ren_up*weight_fac_up);
        h_sums->Fill(sum_weight_ren_fac_dn, *weight*weight_ren_dn*weight_fac_dn);
      }

    }

    //rochester corrections have a correction to apply to data/mc so putting it here //Abby changes begin
    if (apply_roccor) {
      double roccor_sf = 1.0; //total for the event
      //these sf are applied to every muon
      if (event.isRealData()) { 
        for (int imu = 0; imu < mevent->nmuons(); ++imu) {
          if (mevent->muon_pt[imu] < 10.) continue;
          double dtSF = rc.kScaleDT(mevent->muon_q[imu], mevent->muon_pt[imu], mevent->muon_eta[imu], mevent->muon_phi[imu], 0, 0); //data
          roccor_sf *= dtSF;
        }
      }
      else if (!event.isRealData()) { 
        // nl is trackerlayersWithMeasurement 
        // u is random number distributed uniformly between 0 and 1 ( gRandom->Rndm() ); 
        double u = gRandom->Rndm();

        for (int imu = 0; imu < mevent->nmuons(); ++imu) {
          if (mevent->muon_pt[imu] < 10.) continue;

          // get gen muon if available
          bool genmatch = false;
          float genmatch_pt = -1.0; 
          double best_dR = 9.0;
          std::vector<double> mindR;
          std::vector<double> genpT;
          for (auto genmu : mevent->gen_muons) {
            double dR = reco::deltaR(mevent->muon_eta[imu], mevent->muon_phi[imu], genmu.Eta(), genmu.Phi());
            mindR.push_back(dR);
            genpT.push_back(genmu.Pt());
          }
          if (mindR.size() !=0) { 
            best_dR = *min_element(mindR.begin(), mindR.end());
            int best_idx = std::min_element(mindR.begin(), mindR.end()) - mindR.begin();
            genmatch_pt = genpT[best_idx];
          }
          if (best_dR < 0.1) genmatch = true;

          if (genmatch) {
            double mcSF = rc.kSpreadMC(mevent->muon_q[imu], mevent->muon_pt[imu], mevent->muon_eta[imu], mevent->muon_phi[imu], genmatch_pt, 0, 0); //(recommended), MC scale and resolution correction when matched gen muon is available
            roccor_sf *= mcSF;
          }
          else if (!genmatch){ 
            double mcSF = rc.kSmearMC(mevent->muon_q[imu], mevent->muon_pt[imu], mevent->muon_eta[imu], mevent->muon_phi[imu], mevent->muon_nlayers(imu), u, 0, 0); //MC scale and extra smearing when matched gen muon is not available
            roccor_sf *= mcSF; 
          }
        }
      }
      *weight *= roccor_sf; 
      // std::cout << "roccor sf : " << roccor_sf << std::endl;

    } //Abby changes end
    
  }

  if (histos) { //Abby change added curley bracket
    h_sums->Fill(sum_weight, *weight);
    h_lepsums->Fill(lsum_weight, *weight); //Abby change
  } //Abby change

  if (prints)
    printf("total weight: %g\n", *weight);

  
  event.put(std::move(weight));
  event.put(std::move(weight_up), "lepsfup"); //specific for leptoninSV  //Abby change
  event.put(std::move(weight_down), "lepsfdown"); //specific for leptoninSV //Abby change

  
}

DEFINE_FWK_MODULE(MFVWeightProducer);
