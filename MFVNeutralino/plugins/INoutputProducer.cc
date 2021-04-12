#include <memory>

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DNN/TensorFlow/interface/TensorFlow.h"
#include "JMTucker/MFVNeutralinoFormats/interface/Event.h"

class INoutputProducer : public edm::EDProducer
{
public:
    explicit INoutputProducer(const edm::ParameterSet&);
    ~INoutputProducer();

private:
    void beginJob();
    void produce(edm::Event&, const edm::EventSetup&);
    void endJob();
    std::vector<tensorflow::Tensor> getRmatrix(int njets);

    std::string graphPath_;
    tensorflow::GraphDef* graphDef_;
    //tensorflow::MetaGraphDef* metaGraph_;
    tensorflow::Session* session_;

    const edm::EDGetTokenT<MFVEvent> mevent_token;
    const int njets;
};

INoutputProducer::INoutputProducer(const edm::ParameterSet& config)
    : graphPath_(config.getParameter<std::string>("graphPath")),
      graphDef_(nullptr),
      //metaGraph_(nullptr),
      session_(nullptr),
      mevent_token(consumes<MFVEvent>(config.getParameter<edm::InputTag>("mevent_src"))),
      njets(config.getParameter<int>("njets"))
{
    // show tf debug logs
    tensorflow::setLogging("0");
    produces<double>();
}

INoutputProducer::~INoutputProducer()
{
}

std::vector<tensorflow::Tensor> INoutputProducer::getRmatrix(int njets)
{
  int Dr = njets*(njets-1);
  tensorflow::Tensor Rr(tensorflow::DT_FLOAT, { 1, 4, Dr });
  tensorflow::Tensor Rs(tensorflow::DT_FLOAT, { 1, 4, Dr });
  tensorflow::Tensor Ra(tensorflow::DT_FLOAT, { 1, 1, Dr });
  int count = 0;
  std::vector<float> Rr_vec(4*Dr, 0);
  std::vector<float> Rs_vec(4*Dr, 0);
  std::vector<float> Ra_vec(4*Dr, 1);
  for (int i=0; i<njets; ++i){
    for (int j=0; j<njets; ++j){
      if (i!=j){
        Rr_vec[i*Dr+count] = 1;
        Rs_vec[j*Dr+count] = 1;
        ++count;
      }
    }
  }

  float* d_Rr = Rr.flat<float>().data();
  for (float i = 0; i < Rr_vec.size(); i++, d_Rr++)
  {
    *d_Rr = Rr_vec[i];
  }

  float* d_Rs = Rs.flat<float>().data();
  for (float i = 0; i < Rs_vec.size(); i++, d_Rs++)
  {
    *d_Rs = Rs_vec[i];
  }

  float* d_Ra = Ra.flat<float>().data();
  for (float i = 0; i < Ra_vec.size(); i++, d_Ra++)
  {
    *d_Ra = Ra_vec[i];
  }

  return std::vector<tensorflow::Tensor>{Rr, Rs, Ra};
}

void INoutputProducer::beginJob()
{
    // load the graph
    std::cout << "loading graph from " << graphPath_ << std::endl;
    graphDef_ = tensorflow::loadGraphDef(graphPath_);
    //metaGraph_ = tensorflow::loadMetaGraph(graphPath_);

    // create a new session and add the graphDef
    session_ = tensorflow::createSession(graphDef_);
}

void INoutputProducer::endJob()
{
    // close the session
    tensorflow::closeSession(session_);
    session_ = nullptr;

    // delete the graph
    delete graphDef_;
    graphDef_ = nullptr;
    //delete metaGraph_;
    //metaGraph_ = nullptr;
}

void INoutputProducer::produce(edm::Event& event, const edm::EventSetup& setup)
{
    // normalize factors [median, min, max]
    // normalization: x = (x-median)*(2.0/(max-min))
    //pt_n = [80.74742126464844, 25.610614776611328, 402.87548828125]
    //eta_n = [0.0019912796560674906, -1.7208560705184937, 1.7145205736160278]
    //phi_n = [-0.02133125066757202, -2.826939582824707, 2.815577507019043]
    //energy_n = [117.2960205078125, 34.48314666748047, 679.9258422851562]

    std::vector<double> pt_n ({80.74742126464844, 25.610614776611328, 402.87548828125});
    std::vector<double> eta_n ({0.0019912796560674906, -1.7208560705184937, 1.7145205736160278});
    std::vector<double> phi_n ({-0.02133125066757202, -2.826939582824707, 2.815577507019043});
    std::vector<double> energy_n ({117.2960205078125, 34.48314666748047, 679.9258422851562});
    std::unique_ptr<double> INscore(new double(-255.0));

    edm::Handle<MFVEvent> mevent;
    event.getByToken(mevent_token, mevent);
    std::vector<float> jet_info(4*njets, 0);
    for (int i=0; i<njets; ++i){
      if (i<mevent->njets()){
        jet_info[i*4+0] = (mevent->jet_pt[i]-pt_n[0])*(2.0/(pt_n[2]-pt_n[1]));
        jet_info[i*4+1] = (mevent->jet_eta[i]-eta_n[0])*(2.0/(eta_n[2]-eta_n[1]));
        jet_info[i*4+2] = (mevent->jet_phi[i]-phi_n[0])*(2.0/(phi_n[2]-phi_n[1]));
        jet_info[i*4+3] = (mevent->jet_energy[i]-energy_n[0])*(2.0/(energy_n[2]-energy_n[1]));
      }
      else{
        break;
      }
    }

    // define a tensor and fill it with range(10)
    tensorflow::Tensor jet_input(tensorflow::DT_FLOAT, { 1, 4, njets });
    float* d = jet_input.flat<float>().data();
    for (float i = 0; i < jet_info.size(); i++, d++)
    {
        *d = jet_info[i];
    }
    std::vector<tensorflow::Tensor> R_matrix = getRmatrix(njets);

    // define the output and run
    std::cout << "session.run" << std::endl;
    std::vector<tensorflow::Tensor> outputs;
    tensorflow::run(session_, { { "O", jet_input }, { "Rr", R_matrix[0]}, { "Rs", R_matrix[1]}, { "Ra", R_matrix[2]} }, { "out_sigmoid" }, &outputs);

    // check and print the output
    std::cout << " -> " << outputs[0].matrix<float>()(0, 0) << std::endl << std::endl;
    //INscore = outputs[0].matrix<float>()(0, 0);
    event.put(std::move(INscore));
}

DEFINE_FWK_MODULE(INoutputProducer);

