#ifndef DVCode_MFVNeutralino_VertexMVA_h
#define DVCode_MFVNeutralino_VertexMVA_h

// Class: ReadMLP
// Automatically generated by MethodBase::MakeClass
//

/* configuration options =====================================================

#GEN -*-*-*-*-*-*-*-*-*-*-*- general info -*-*-*-*-*-*-*-*-*-*-*-

Method         : MLP::MLP
TMVA Release   : 4.1.2         [262402]
ROOT Release   : 5.32/00       [335872]
Creator        : tucker
Date           : Fri Dec 13 11:54:06 2013
Host           : Linux lxbuild168.cern.ch 2.6.18-308.16.1.el5 #1 SMP Thu Oct 4 14:02:28 CEST 2012 x86_64 x86_64 x86_64 GNU/Linux
Dir            : /uscms/home/tucker/private/tmva
Training events: 7783
Analysis type  : [Classification]


#OPT -*-*-*-*-*-*-*-*-*-*-*-*- options -*-*-*-*-*-*-*-*-*-*-*-*-

# Set by User:
NCycles: "600" [Number of training cycles]
HiddenLayers: "N+5" [Specification of hidden layer architecture]
NeuronType: "tanh" [Neuron activation function type]
V: "False" [Verbose output (short form of "VerbosityLevel" below - overrides the latter one)]
VarTransform: "N" [List of variable transformations performed before training, e.g., "D_Background,P_Signal,G,N_AllClasses" for: "Decorrelation, PCA-transformation, Gaussianisation, Normalisation, each for the given class of events ('AllClasses' denotes all events of all classes, if no class indication is given, 'All' is assumed)"]
H: "True" [Print method-specific help message]
TestRate: "5" [Test for overtraining performed at each #th epochs]
UseRegulator: "False" [Use regulator to avoid over-training]
# Default:
RandomSeed: "1" [Random seed for initial synapse weights (0 means unique seed for each run; default value '1')]
EstimatorType: "MSE" [MSE (Mean Square Estimator) for Gaussian Likelihood or CE(Cross-Entropy) for Bernoulli Likelihood]
NeuronInputType: "sum" [Neuron input function type]
VerbosityLevel: "Default" [Verbosity level]
CreateMVAPdfs: "False" [Create PDFs for classifier outputs (signal and background)]
IgnoreNegWeightsInTraining: "False" [Events with negative weights are ignored in the training (but are included for testing and performance evaluation)]
TrainingMethod: "BP" [Train with Back-Propagation (BP), BFGS Algorithm (BFGS), or Genetic Algorithm (GA - slower and worse)]
LearningRate: "2.000000e-02" [ANN learning rate parameter]
DecayRate: "1.000000e-02" [Decay rate for learning parameter]
EpochMonitoring: "False" [Provide epoch-wise monitoring plots according to TestRate (caution: causes big ROOT output file!)]
Sampling: "1.000000e+00" [Only 'Sampling' (randomly selected) events are trained each epoch]
SamplingEpoch: "1.000000e+00" [Sampling is used for the first 'SamplingEpoch' epochs, afterwards, all events are taken for training]
SamplingImportance: "1.000000e+00" [ The sampling weights of events in epochs which successful (worse estimator than before) are multiplied with SamplingImportance, else they are divided.]
SamplingTraining: "True" [The training sample is sampled]
SamplingTesting: "False" [The testing sample is sampled]
ResetStep: "50" [How often BFGS should reset history]
Tau: "3.000000e+00" [LineSearch "size step"]
BPMode: "sequential" [Back-propagation learning mode: sequential or batch]
BatchSize: "-1" [Batch size: number of events/batch, only set if in Batch Mode, -1 for BatchSize=number_of_events]
ConvergenceImprove: "1.000000e-30" [Minimum improvement which counts as improvement (<0 means automatic convergence check is turned off)]
ConvergenceTests: "-1" [Number of steps (without improvement) required for convergence (<0 means automatic convergence check is turned off)]
UpdateLimit: "10000" [Maximum times of regulator update]
CalculateErrors: "False" [Calculates inverse Hessian matrix at the end of the training to be able to calculate the uncertainties of an MVA value]
WeightRange: "1.000000e+00" [Take the events for the estimator calculations from small deviations from the desired value to large deviations only over the weight range]
##


#VAR -*-*-*-*-*-*-*-*-*-*-*-* variables *-*-*-*-*-*-*-*-*-*-*-*-

NVar 15
vtx.ntracks                   vtx.ntracks                   vtx.ntracks                   vtx.ntracks                                                     'c'    [5,34]
vtx.ntracksptgt3              vtx.ntracksptgt3              vtx.ntracksptgt3              vtx.ntracksptgt3                                                'c'    [0,22]
TMath::Prob(vtx.chi2,vtx.ndof) TMath_Prob_vtx.chi2,vtx.ndof_  TMath::Prob(vtx.chi2,vtx.ndof) TMath::Prob(vtx.chi2,vtx.ndof)                                    'F'    [1.10716809773e-17,0.999991416931]
vtx.eta[][0]                  vtx.eta___0_                  vtx.eta[][0]                  vtx.eta[][0]                                                    'F'    [-6.6865940094,5.33746910095]
vtx.costhmompv3d[][2]         vtx.costhmompv3d___2_         vtx.costhmompv3d[][2]         vtx.costhmompv3d[][2]                                           'F'    [-2,0.999999821186]
vtx.trackdxyerrmin            vtx.trackdxyerrmin            vtx.trackdxyerrmin            vtx.trackdxyerrmin                                              'F'    [0.000780336209573,0.36220741272]
vtx.trackdzerrmin             vtx.trackdzerrmin             vtx.trackdzerrmin             vtx.trackdzerrmin                                               'F'    [0.00142211036291,3.00996232033]
vtx.trackquadmassmin          vtx.trackquadmassmin          vtx.trackquadmassmin          vtx.trackquadmassmin                                            'F'    [0.142663016915,92.6201324463]
vtx.costhtkmomvtxdispavg      vtx.costhtkmomvtxdispavg      vtx.costhtkmomvtxdispavg      vtx.costhtkmomvtxdispavg                                        'F'    [-0.979679763317,0.999767661095]
vtx.mass[][2]                 vtx.mass___2_                 vtx.mass[][2]                 vtx.mass[][2]                                                   'F'    [0,3789.05102539]
vtx.maxtrackpt                vtx.maxtrackpt                vtx.maxtrackpt                vtx.maxtrackpt                                                  'F'    [1.0471663475,1040.47387695]
vtx.drmin                     vtx.drmin                     vtx.drmin                     vtx.drmin                                                       'F'    [0.000926514097955,2.26235461235]
vtx.drmax                     vtx.drmax                     vtx.drmax                     vtx.drmax                                                       'F'    [0.0571069195867,5.84594631195]
vtx.njets[0]                  vtx.njets_0_                  vtx.njets[0]                  vtx.njets[0]                                                    'c'    [0,7]
vtx.bs2dsig()                 vtx.bs2dsig__                 vtx.bs2dsig()                 vtx.bs2dsig()                                                   'F'    [0,1079.31750488]
NSpec 0


============================================================================ */

#include <vector>
#include <cmath>
#include <string>
#include <iostream>

#ifndef IClassifierReader__def
#define IClassifierReader__def

class IClassifierReader {

 public:

   // constructor
   IClassifierReader() : fStatusIsClean( true ) {}
   virtual ~IClassifierReader() {}

   // return classifier response
   virtual double GetMvaValue( const std::vector<double>& inputValues ) const = 0;

   // returns classifier status
   bool IsStatusClean() const { return fStatusIsClean; }

 protected:

   bool fStatusIsClean;
};

#endif

class ReadMLP : public IClassifierReader {

 public:
   // constructor
  ReadMLP()
      : IClassifierReader(),
        fClassName( "ReadMLP" ),
        fNvars( 15 ),
        fIsNormalised( false )
   {      
//      // the training input variables
//      const char* inputVars[] = { "vtx.ntracks", "vtx.ntracksptgt3", "TMath::Prob(vtx.chi2,vtx.ndof)", "vtx.eta[][0]", "vtx.costhmompv3d[][2]", "vtx.trackdxyerrmin", "vtx.trackdzerrmin", "vtx.trackquadmassmin", "vtx.costhtkmomvtxdispavg", "vtx.mass[][2]", "vtx.maxtrackpt", "vtx.drmin", "vtx.drmax", "vtx.njets[0]", "vtx.bs2dsig()" };
//
//      // sanity checks
//      if (theInputVars.size() <= 0) {
//         std::cout << "Problem in class \"" << fClassName << "\": empty input vector" << std::endl;
//         fStatusIsClean = false;
//      }
//
//      if (theInputVars.size() != fNvars) {
//         std::cout << "Problem in class \"" << fClassName << "\": mismatch in number of input values: "
//                   << theInputVars.size() << " != " << fNvars << std::endl;
//         fStatusIsClean = false;
//      }
//
//      // validate input variables
//      for (size_t ivar = 0; ivar < theInputVars.size(); ivar++) {
//         if (theInputVars[ivar] != inputVars[ivar]) {
//            std::cout << "Problem in class \"" << fClassName << "\": mismatch in input variable names" << std::endl
//                      << " for variable [" << ivar << "]: " << theInputVars[ivar].c_str() << " != " << inputVars[ivar] << std::endl;
//            fStatusIsClean = false;
//         }
//      }

      // initialize min and max vectors (for normalisation)
      fVmin[0] = -1;
      fVmax[0] = 1;
      fVmin[1] = -1;
      fVmax[1] = 1;
      fVmin[2] = -1;
      fVmax[2] = 1;
      fVmin[3] = -1;
      fVmax[3] = 1;
      fVmin[4] = -1;
      fVmax[4] = 1;
      fVmin[5] = -1;
      fVmax[5] = 1;
      fVmin[6] = -1;
      fVmax[6] = 1;
      fVmin[7] = -1;
      fVmax[7] = 1;
      fVmin[8] = -1;
      fVmax[8] = 1;
      fVmin[9] = -1;
      fVmax[9] = 1;
      fVmin[10] = -1;
      fVmax[10] = 1;
      fVmin[11] = -1;
      fVmax[11] = 1;
      fVmin[12] = -1;
      fVmax[12] = 1;
      fVmin[13] = -1;
      fVmax[13] = 1;
      fVmin[14] = -1;
      fVmax[14] = 1;

      // initialize input variable types
      fType[0] = 'c';
      fType[1] = 'c';
      fType[2] = 'F';
      fType[3] = 'F';
      fType[4] = 'F';
      fType[5] = 'F';
      fType[6] = 'F';
      fType[7] = 'F';
      fType[8] = 'F';
      fType[9] = 'F';
      fType[10] = 'F';
      fType[11] = 'F';
      fType[12] = 'F';
      fType[13] = 'c';
      fType[14] = 'F';

      // initialize constants
      Initialize();

      // initialize transformation
      InitTransform();
   }

   // destructor
   virtual ~ReadMLP() {
      Clear(); // method-specific
   }

   // the classifier response
   // "inputValues" is a vector of input values in the same order as the 
   // variables given to the constructor
   double GetMvaValue( const std::vector<double>& inputValues ) const;

 private:

   // method-specific destructor
   void Clear();

   // input variable transformation

   double fMin_1[3][15];
   double fMax_1[3][15];
   void InitTransform_1();
   void Transform_1( std::vector<double> & iv, int sigOrBgd ) const;
   void InitTransform();
   void Transform( std::vector<double> & iv, int sigOrBgd ) const;

   // common member variables
   const char* fClassName;

   const size_t fNvars;
   size_t GetNvar()           const { return fNvars; }
   char   GetType( int ivar ) const { return fType[ivar]; }

   // normalisation of input variables
   const bool fIsNormalised;
   bool IsNormalised() const { return fIsNormalised; }
   double fVmin[15];
   double fVmax[15];
   double NormVariable( double x, double xmin, double xmax ) const {
      // normalise to output range: [-1, 1]
      return 2*(x - xmin)/(xmax - xmin) - 1.0;
   }

   // type of input variable: 'F' or 'I'
   char   fType[15];

   // initialize internal variables
   void Initialize();
   double GetMvaValue__( const std::vector<double>& inputValues ) const;

   // private members (method specific)

   double ActivationFnc(double x) const;
   double OutputActivationFnc(double x) const;

   int fLayers;
   int fLayerSize[3];
   double fWeightMatrix0to1[21][16];   // weight matrix from layer 0 to 1
   double fWeightMatrix1to2[1][21];   // weight matrix from layer 1 to 2

   double * fWeights[3];
};

inline void ReadMLP::Initialize()
{
   // build network structure
   fLayers = 3;
   fLayerSize[0] = 16; fWeights[0] = new double[16]; 
   fLayerSize[1] = 21; fWeights[1] = new double[21]; 
   fLayerSize[2] = 1; fWeights[2] = new double[1]; 
   // weight matrix from layer 0 to 1
   fWeightMatrix0to1[0][0] = 0.27148606619138;
   fWeightMatrix0to1[1][0] = 1.9365440980302;
   fWeightMatrix0to1[2][0] = 2.91953574029772;
   fWeightMatrix0to1[3][0] = 0.0695017917785619;
   fWeightMatrix0to1[4][0] = -2.04603047480654;
   fWeightMatrix0to1[5][0] = -1.81223845397514;
   fWeightMatrix0to1[6][0] = -1.34025539718031;
   fWeightMatrix0to1[7][0] = 2.11541730131358;
   fWeightMatrix0to1[8][0] = -1.54981456717586;
   fWeightMatrix0to1[9][0] = -0.89292139724554;
   fWeightMatrix0to1[10][0] = -1.68335847448465;
   fWeightMatrix0to1[11][0] = -0.192313937624825;
   fWeightMatrix0to1[12][0] = -0.546034688762448;
   fWeightMatrix0to1[13][0] = -0.652889916190236;
   fWeightMatrix0to1[14][0] = -0.942523860190525;
   fWeightMatrix0to1[15][0] = 0.855266873993982;
   fWeightMatrix0to1[16][0] = -0.817407383736621;
   fWeightMatrix0to1[17][0] = 1.64219691532841;
   fWeightMatrix0to1[18][0] = 0.10962437723109;
   fWeightMatrix0to1[19][0] = 1.41212475339984;
   fWeightMatrix0to1[0][1] = 0.169473580426327;
   fWeightMatrix0to1[1][1] = -0.747345971746183;
   fWeightMatrix0to1[2][1] = 3.44010710502933;
   fWeightMatrix0to1[3][1] = -0.470162394042265;
   fWeightMatrix0to1[4][1] = -1.28972946047895;
   fWeightMatrix0to1[5][1] = -0.521225271584539;
   fWeightMatrix0to1[6][1] = 0.976812583567276;
   fWeightMatrix0to1[7][1] = -0.988886015032943;
   fWeightMatrix0to1[8][1] = -1.90803668660543;
   fWeightMatrix0to1[9][1] = -0.016862200402349;
   fWeightMatrix0to1[10][1] = 0.617688149351947;
   fWeightMatrix0to1[11][1] = 1.8794169287106;
   fWeightMatrix0to1[12][1] = 0.274379409439249;
   fWeightMatrix0to1[13][1] = -0.339043583973793;
   fWeightMatrix0to1[14][1] = 0.0790545855256225;
   fWeightMatrix0to1[15][1] = -0.0490031906960735;
   fWeightMatrix0to1[16][1] = -1.74649470695902;
   fWeightMatrix0to1[17][1] = 1.67978403016482;
   fWeightMatrix0to1[18][1] = -1.16608107794883;
   fWeightMatrix0to1[19][1] = 1.14412360121586;
   fWeightMatrix0to1[0][2] = 1.10894537574421;
   fWeightMatrix0to1[1][2] = 0.421160022966459;
   fWeightMatrix0to1[2][2] = 0.420725972875958;
   fWeightMatrix0to1[3][2] = -0.252934478467505;
   fWeightMatrix0to1[4][2] = -0.555078007145742;
   fWeightMatrix0to1[5][2] = -1.06067092164527;
   fWeightMatrix0to1[6][2] = 0.243400105629089;
   fWeightMatrix0to1[7][2] = -0.0336913770457693;
   fWeightMatrix0to1[8][2] = 1.07296832337856;
   fWeightMatrix0to1[9][2] = -0.0388675604689954;
   fWeightMatrix0to1[10][2] = 1.529705031547;
   fWeightMatrix0to1[11][2] = 1.26495914619059;
   fWeightMatrix0to1[12][2] = -1.10850837358817;
   fWeightMatrix0to1[13][2] = 1.16407217550769;
   fWeightMatrix0to1[14][2] = -1.72312954340278;
   fWeightMatrix0to1[15][2] = -0.457999685376454;
   fWeightMatrix0to1[16][2] = -1.02798328101941;
   fWeightMatrix0to1[17][2] = -1.83467287998977;
   fWeightMatrix0to1[18][2] = 0.932726846998887;
   fWeightMatrix0to1[19][2] = 0.700145870110931;
   fWeightMatrix0to1[0][3] = -1.5228722181625;
   fWeightMatrix0to1[1][3] = 0.313755707664181;
   fWeightMatrix0to1[2][3] = 0.214540084997672;
   fWeightMatrix0to1[3][3] = 0.547243961915248;
   fWeightMatrix0to1[4][3] = 1.83516541272679;
   fWeightMatrix0to1[5][3] = -0.257925514755132;
   fWeightMatrix0to1[6][3] = 0.12019391769269;
   fWeightMatrix0to1[7][3] = -1.21856001399765;
   fWeightMatrix0to1[8][3] = 0.805018841072048;
   fWeightMatrix0to1[9][3] = -0.377855964053629;
   fWeightMatrix0to1[10][3] = -0.723895531012958;
   fWeightMatrix0to1[11][3] = -0.945148348053517;
   fWeightMatrix0to1[12][3] = 0.716108052915827;
   fWeightMatrix0to1[13][3] = 1.09043906939782;
   fWeightMatrix0to1[14][3] = 1.31043608027274;
   fWeightMatrix0to1[15][3] = -0.446128776322967;
   fWeightMatrix0to1[16][3] = -1.90138414864278;
   fWeightMatrix0to1[17][3] = -1.86290265549601;
   fWeightMatrix0to1[18][3] = 0.747322205846243;
   fWeightMatrix0to1[19][3] = 0.495232899341931;
   fWeightMatrix0to1[0][4] = 1.81587386817795;
   fWeightMatrix0to1[1][4] = 0.221555525761157;
   fWeightMatrix0to1[2][4] = 0.385892428520807;
   fWeightMatrix0to1[3][4] = 0.453250119020239;
   fWeightMatrix0to1[4][4] = -0.694425396684228;
   fWeightMatrix0to1[5][4] = 0.500529639038137;
   fWeightMatrix0to1[6][4] = 0.989316851597553;
   fWeightMatrix0to1[7][4] = -0.922496549636717;
   fWeightMatrix0to1[8][4] = -1.49269314540098;
   fWeightMatrix0to1[9][4] = -1.48053627815366;
   fWeightMatrix0to1[10][4] = -0.301452925250489;
   fWeightMatrix0to1[11][4] = 0.773693302341971;
   fWeightMatrix0to1[12][4] = 1.09643103924244;
   fWeightMatrix0to1[13][4] = -1.60972691897021;
   fWeightMatrix0to1[14][4] = -0.586265815493636;
   fWeightMatrix0to1[15][4] = 1.71101889853153;
   fWeightMatrix0to1[16][4] = -0.779962412639831;
   fWeightMatrix0to1[17][4] = -1.68030849207052;
   fWeightMatrix0to1[18][4] = -1.01928249104302;
   fWeightMatrix0to1[19][4] = 0.133081088350972;
   fWeightMatrix0to1[0][5] = -1.32961365198641;
   fWeightMatrix0to1[1][5] = -1.14691617035825;
   fWeightMatrix0to1[2][5] = -1.02781719771384;
   fWeightMatrix0to1[3][5] = 1.79441819555237;
   fWeightMatrix0to1[4][5] = -1.39628270276767;
   fWeightMatrix0to1[5][5] = 0.618977225115526;
   fWeightMatrix0to1[6][5] = -1.1968575834944;
   fWeightMatrix0to1[7][5] = -0.795238396409704;
   fWeightMatrix0to1[8][5] = -0.0731240628888494;
   fWeightMatrix0to1[9][5] = 0.88871922423475;
   fWeightMatrix0to1[10][5] = -1.70308353076392;
   fWeightMatrix0to1[11][5] = -0.343285259706637;
   fWeightMatrix0to1[12][5] = 1.08448899148956;
   fWeightMatrix0to1[13][5] = 0.35962346703465;
   fWeightMatrix0to1[14][5] = -1.78446936338449;
   fWeightMatrix0to1[15][5] = 1.86878353954946;
   fWeightMatrix0to1[16][5] = 0.0384940918197945;
   fWeightMatrix0to1[17][5] = -1.09654971042113;
   fWeightMatrix0to1[18][5] = 0.955026495154368;
   fWeightMatrix0to1[19][5] = -1.04892608478398;
   fWeightMatrix0to1[0][6] = -1.03312264844823;
   fWeightMatrix0to1[1][6] = 0.653695866665719;
   fWeightMatrix0to1[2][6] = -0.198328442512705;
   fWeightMatrix0to1[3][6] = 1.68808601129277;
   fWeightMatrix0to1[4][6] = 0.533430028055962;
   fWeightMatrix0to1[5][6] = -1.06473724865992;
   fWeightMatrix0to1[6][6] = -0.61391820064339;
   fWeightMatrix0to1[7][6] = 0.172655952729283;
   fWeightMatrix0to1[8][6] = -1.87112420880073;
   fWeightMatrix0to1[9][6] = 1.47669701796439;
   fWeightMatrix0to1[10][6] = 0.199658255839993;
   fWeightMatrix0to1[11][6] = -2.25012218393198;
   fWeightMatrix0to1[12][6] = 1.45615465029739;
   fWeightMatrix0to1[13][6] = -1.57737237210189;
   fWeightMatrix0to1[14][6] = -0.230180920664263;
   fWeightMatrix0to1[15][6] = 1.09488894300307;
   fWeightMatrix0to1[16][6] = 1.46706856394508;
   fWeightMatrix0to1[17][6] = -2.02727910943706;
   fWeightMatrix0to1[18][6] = 0.358151504595966;
   fWeightMatrix0to1[19][6] = 1.56105655844011;
   fWeightMatrix0to1[0][7] = 1.9786790564242;
   fWeightMatrix0to1[1][7] = 0.663965785267336;
   fWeightMatrix0to1[2][7] = 0.666132050260865;
   fWeightMatrix0to1[3][7] = 0.660324873136602;
   fWeightMatrix0to1[4][7] = -1.67780804243054;
   fWeightMatrix0to1[5][7] = 0.625047813603636;
   fWeightMatrix0to1[6][7] = 0.609857335047906;
   fWeightMatrix0to1[7][7] = -0.480628566046972;
   fWeightMatrix0to1[8][7] = -0.437082699230929;
   fWeightMatrix0to1[9][7] = 0.141607924779807;
   fWeightMatrix0to1[10][7] = -1.41043409436452;
   fWeightMatrix0to1[11][7] = 0.561730869076979;
   fWeightMatrix0to1[12][7] = 2.11743581951306;
   fWeightMatrix0to1[13][7] = -0.738197782432483;
   fWeightMatrix0to1[14][7] = -0.694986302219148;
   fWeightMatrix0to1[15][7] = 0.0322844712183477;
   fWeightMatrix0to1[16][7] = 0.781559543200444;
   fWeightMatrix0to1[17][7] = 0.392106891809296;
   fWeightMatrix0to1[18][7] = 0.868236761843426;
   fWeightMatrix0to1[19][7] = -1.45991874130877;
   fWeightMatrix0to1[0][8] = 1.65973687698205;
   fWeightMatrix0to1[1][8] = 0.48427587358396;
   fWeightMatrix0to1[2][8] = 0.592232569592957;
   fWeightMatrix0to1[3][8] = 1.62198333877793;
   fWeightMatrix0to1[4][8] = 1.06019176145176;
   fWeightMatrix0to1[5][8] = -0.304090267420576;
   fWeightMatrix0to1[6][8] = -0.442380779852806;
   fWeightMatrix0to1[7][8] = 1.01149977589588;
   fWeightMatrix0to1[8][8] = -0.818768916840401;
   fWeightMatrix0to1[9][8] = 0.345930387069813;
   fWeightMatrix0to1[10][8] = 1.49367193658951;
   fWeightMatrix0to1[11][8] = 0.275434378175022;
   fWeightMatrix0to1[12][8] = -0.28907944294973;
   fWeightMatrix0to1[13][8] = 1.39579846326557;
   fWeightMatrix0to1[14][8] = 1.58030503947807;
   fWeightMatrix0to1[15][8] = -1.28684209680332;
   fWeightMatrix0to1[16][8] = 0.722562102146745;
   fWeightMatrix0to1[17][8] = -0.00975422782463986;
   fWeightMatrix0to1[18][8] = 0.687635184136829;
   fWeightMatrix0to1[19][8] = -1.71067156558797;
   fWeightMatrix0to1[0][9] = -1.36756567154268;
   fWeightMatrix0to1[1][9] = 1.56071591381997;
   fWeightMatrix0to1[2][9] = -4.60584019351601;
   fWeightMatrix0to1[3][9] = -1.38859132551077;
   fWeightMatrix0to1[4][9] = -0.414558621348803;
   fWeightMatrix0to1[5][9] = -1.25368965715878;
   fWeightMatrix0to1[6][9] = -0.168661936526082;
   fWeightMatrix0to1[7][9] = 1.81365769354702;
   fWeightMatrix0to1[8][9] = -0.323964931108102;
   fWeightMatrix0to1[9][9] = -0.431934356281807;
   fWeightMatrix0to1[10][9] = -1.11476554494525;
   fWeightMatrix0to1[11][9] = 0.402516658738621;
   fWeightMatrix0to1[12][9] = 1.96616259957625;
   fWeightMatrix0to1[13][9] = 0.887835463094915;
   fWeightMatrix0to1[14][9] = -0.163215283298792;
   fWeightMatrix0to1[15][9] = -0.838341169387808;
   fWeightMatrix0to1[16][9] = -2.05953384505544;
   fWeightMatrix0to1[17][9] = 0.702849690925463;
   fWeightMatrix0to1[18][9] = 0.675970122031875;
   fWeightMatrix0to1[19][9] = -1.36186101917803;
   fWeightMatrix0to1[0][10] = -0.186024508989764;
   fWeightMatrix0to1[1][10] = 0.810286206827731;
   fWeightMatrix0to1[2][10] = -0.756966314585439;
   fWeightMatrix0to1[3][10] = -1.31648209144;
   fWeightMatrix0to1[4][10] = 1.31113666395379;
   fWeightMatrix0to1[5][10] = -0.161078692110326;
   fWeightMatrix0to1[6][10] = -1.25287817503345;
   fWeightMatrix0to1[7][10] = -0.101016396045255;
   fWeightMatrix0to1[8][10] = 1.65490857855372;
   fWeightMatrix0to1[9][10] = 1.04896992248519;
   fWeightMatrix0to1[10][10] = 0.438533062021974;
   fWeightMatrix0to1[11][10] = -0.428650385343093;
   fWeightMatrix0to1[12][10] = -1.17413711126897;
   fWeightMatrix0to1[13][10] = -1.10164765916108;
   fWeightMatrix0to1[14][10] = 1.41969125186978;
   fWeightMatrix0to1[15][10] = 1.25930014755223;
   fWeightMatrix0to1[16][10] = 0.477229714962117;
   fWeightMatrix0to1[17][10] = 0.0431537511323964;
   fWeightMatrix0to1[18][10] = 2.06912162109758;
   fWeightMatrix0to1[19][10] = -1.6922896815705;
   fWeightMatrix0to1[0][11] = -0.914477155253948;
   fWeightMatrix0to1[1][11] = 0.395574311505469;
   fWeightMatrix0to1[2][11] = -0.15386378541434;
   fWeightMatrix0to1[3][11] = 1.02360781607512;
   fWeightMatrix0to1[4][11] = 1.49805931411265;
   fWeightMatrix0to1[5][11] = -2.08281154158382;
   fWeightMatrix0to1[6][11] = 0.16195191014684;
   fWeightMatrix0to1[7][11] = -0.161351588576183;
   fWeightMatrix0to1[8][11] = -1.83916317702948;
   fWeightMatrix0to1[9][11] = -1.13760995108088;
   fWeightMatrix0to1[10][11] = 0.969252075948044;
   fWeightMatrix0to1[11][11] = -0.546765346047011;
   fWeightMatrix0to1[12][11] = 1.30074064833582;
   fWeightMatrix0to1[13][11] = -1.26401951353138;
   fWeightMatrix0to1[14][11] = 1.32497313793652;
   fWeightMatrix0to1[15][11] = -2.0830695962097;
   fWeightMatrix0to1[16][11] = 0.578133859490591;
   fWeightMatrix0to1[17][11] = -0.0293560114765276;
   fWeightMatrix0to1[18][11] = -1.22947709089486;
   fWeightMatrix0to1[19][11] = -1.30341491192275;
   fWeightMatrix0to1[0][12] = -1.98926125260753;
   fWeightMatrix0to1[1][12] = -0.469945518617511;
   fWeightMatrix0to1[2][12] = -1.22369743810602;
   fWeightMatrix0to1[3][12] = -3.01790521400975;
   fWeightMatrix0to1[4][12] = -1.77159160528503;
   fWeightMatrix0to1[5][12] = 0.34001839144947;
   fWeightMatrix0to1[6][12] = -0.868878233282707;
   fWeightMatrix0to1[7][12] = -1.58417262666276;
   fWeightMatrix0to1[8][12] = 1.24233431791302;
   fWeightMatrix0to1[9][12] = -0.74447507508005;
   fWeightMatrix0to1[10][12] = 0.0967926204458046;
   fWeightMatrix0to1[11][12] = -0.0458853178997719;
   fWeightMatrix0to1[12][12] = -0.280039470755579;
   fWeightMatrix0to1[13][12] = 1.80571316296251;
   fWeightMatrix0to1[14][12] = 1.4394939060006;
   fWeightMatrix0to1[15][12] = -0.642683448020492;
   fWeightMatrix0to1[16][12] = -1.43348782337605;
   fWeightMatrix0to1[17][12] = -1.02442360012341;
   fWeightMatrix0to1[18][12] = -0.802153185966358;
   fWeightMatrix0to1[19][12] = -1.65016582453438;
   fWeightMatrix0to1[0][13] = 0.609773911208486;
   fWeightMatrix0to1[1][13] = 0.241172626935504;
   fWeightMatrix0to1[2][13] = 1.23506191208338;
   fWeightMatrix0to1[3][13] = -0.504977362138953;
   fWeightMatrix0to1[4][13] = 0.225252788951147;
   fWeightMatrix0to1[5][13] = -0.604297514241195;
   fWeightMatrix0to1[6][13] = -2.14577927059075;
   fWeightMatrix0to1[7][13] = 1.29513485215694;
   fWeightMatrix0to1[8][13] = 1.11731928074316;
   fWeightMatrix0to1[9][13] = -1.22354211887944;
   fWeightMatrix0to1[10][13] = -1.12511019366429;
   fWeightMatrix0to1[11][13] = 1.17432482343243;
   fWeightMatrix0to1[12][13] = 1.4253090900543;
   fWeightMatrix0to1[13][13] = 0.408224764753943;
   fWeightMatrix0to1[14][13] = -0.574657498402982;
   fWeightMatrix0to1[15][13] = -0.169487017870051;
   fWeightMatrix0to1[16][13] = 1.11222315463576;
   fWeightMatrix0to1[17][13] = 0.854855810776535;
   fWeightMatrix0to1[18][13] = 1.22204206022809;
   fWeightMatrix0to1[19][13] = -0.254510302775147;
   fWeightMatrix0to1[0][14] = 0.714189062825104;
   fWeightMatrix0to1[1][14] = 0.207909220702144;
   fWeightMatrix0to1[2][14] = 2.28095395666185;
   fWeightMatrix0to1[3][14] = 0.179105947766422;
   fWeightMatrix0to1[4][14] = -1.96130836963033;
   fWeightMatrix0to1[5][14] = -2.249291086914;
   fWeightMatrix0to1[6][14] = -2.25450507799303;
   fWeightMatrix0to1[7][14] = 1.690919449085;
   fWeightMatrix0to1[8][14] = -2.05246195607804;
   fWeightMatrix0to1[9][14] = 1.76124400336846;
   fWeightMatrix0to1[10][14] = -1.66317416566462;
   fWeightMatrix0to1[11][14] = 1.17482190531367;
   fWeightMatrix0to1[12][14] = -0.312038891558811;
   fWeightMatrix0to1[13][14] = 0.252633828929314;
   fWeightMatrix0to1[14][14] = 0.73878904091497;
   fWeightMatrix0to1[15][14] = -2.10675372946797;
   fWeightMatrix0to1[16][14] = -0.0633536853948249;
   fWeightMatrix0to1[17][14] = 0.47904522824259;
   fWeightMatrix0to1[18][14] = -2.02872187419526;
   fWeightMatrix0to1[19][14] = -1.43493534768424;
   fWeightMatrix0to1[0][15] = -2.25796020354925;
   fWeightMatrix0to1[1][15] = -1.34239949799223;
   fWeightMatrix0to1[2][15] = 2.13211898613353;
   fWeightMatrix0to1[3][15] = -1.35186329932403;
   fWeightMatrix0to1[4][15] = 0.516772055399343;
   fWeightMatrix0to1[5][15] = 0.138358311050748;
   fWeightMatrix0to1[6][15] = -0.485013536248705;
   fWeightMatrix0to1[7][15] = -1.71279576001634;
   fWeightMatrix0to1[8][15] = -0.994872883850832;
   fWeightMatrix0to1[9][15] = -1.4193547667313;
   fWeightMatrix0to1[10][15] = 1.02918726597739;
   fWeightMatrix0to1[11][15] = -0.992126877578349;
   fWeightMatrix0to1[12][15] = -2.02622600157565;
   fWeightMatrix0to1[13][15] = 1.96846493038035;
   fWeightMatrix0to1[14][15] = 0.61627976250828;
   fWeightMatrix0to1[15][15] = -0.456694383908732;
   fWeightMatrix0to1[16][15] = 2.19401676070476;
   fWeightMatrix0to1[17][15] = -1.65613941939662;
   fWeightMatrix0to1[18][15] = 1.32826370477484;
   fWeightMatrix0to1[19][15] = 0.935128963209918;
   // weight matrix from layer 1 to 2
   fWeightMatrix1to2[0][0] = -0.0538943625722131;
   fWeightMatrix1to2[0][1] = -0.569394339799473;
   fWeightMatrix1to2[0][2] = 0.537029949948793;
   fWeightMatrix1to2[0][3] = -0.419095134626258;
   fWeightMatrix1to2[0][4] = -0.00512789590580781;
   fWeightMatrix1to2[0][5] = 1.70818480891102;
   fWeightMatrix1to2[0][6] = 1.22537641158128;
   fWeightMatrix1to2[0][7] = 1.24781794922087;
   fWeightMatrix1to2[0][8] = -0.0587721677655049;
   fWeightMatrix1to2[0][9] = 0.467003711909275;
   fWeightMatrix1to2[0][10] = -1.57415128662269;
   fWeightMatrix1to2[0][11] = 0.110154135670367;
   fWeightMatrix1to2[0][12] = -1.67981062625199;
   fWeightMatrix1to2[0][13] = -1.42685925551487;
   fWeightMatrix1to2[0][14] = 0.0498022292032977;
   fWeightMatrix1to2[0][15] = -0.033239308820492;
   fWeightMatrix1to2[0][16] = 0.0305914150063009;
   fWeightMatrix1to2[0][17] = -0.0594770437090778;
   fWeightMatrix1to2[0][18] = -0.0293253339918902;
   fWeightMatrix1to2[0][19] = 0.00183716061608829;
   fWeightMatrix1to2[0][20] = -0.412325341420558;
}

inline double ReadMLP::GetMvaValue__( const std::vector<double>& inputValues ) const
{
   if (inputValues.size() != (unsigned int)fLayerSize[0]-1) {
      std::cout << "Input vector needs to be of size " << fLayerSize[0]-1 << std::endl;
      return 0;
   }

   for (int l=0; l<fLayers; l++)
      for (int i=0; i<fLayerSize[l]; i++) fWeights[l][i]=0;

   for (int l=0; l<fLayers-1; l++)
      fWeights[l][fLayerSize[l]-1]=1;

   for (int i=0; i<fLayerSize[0]-1; i++)
      fWeights[0][i]=inputValues[i];

   // layer 0 to 1
   for (int o=0; o<fLayerSize[1]-1; o++) {
      for (int i=0; i<fLayerSize[0]; i++) {
         double inputVal = fWeightMatrix0to1[o][i] * fWeights[0][i];
         fWeights[1][o] += inputVal;
      }
      fWeights[1][o] = ActivationFnc(fWeights[1][o]);
   }
   // layer 1 to 2
   for (int o=0; o<fLayerSize[2]; o++) {
      for (int i=0; i<fLayerSize[1]; i++) {
         double inputVal = fWeightMatrix1to2[o][i] * fWeights[1][i];
         fWeights[2][o] += inputVal;
      }
      fWeights[2][o] = OutputActivationFnc(fWeights[2][o]);
   }

   return fWeights[2][0];
}

inline double ReadMLP::ActivationFnc(double x) const {
   // hyperbolic tan
   return tanh(x);
}
inline double ReadMLP::OutputActivationFnc(double x) const {
   // identity
   return x;
}
   
// Clean up
inline void ReadMLP::Clear() 
{
   // nothing to clear
}
   inline double ReadMLP::GetMvaValue( const std::vector<double>& inputValues ) const
   {
      // classifier response value
      double retval = 0;

      // classifier response, sanity check first
      if (!IsStatusClean()) {
         std::cout << "Problem in class \"" << fClassName << "\": cannot return classifier response"
                   << " because status is dirty" << std::endl;
         retval = 0;
      }
      else {
         if (IsNormalised()) {
            // normalise variables
            std::vector<double> iV;
            int ivar = 0;
            for (std::vector<double>::const_iterator varIt = inputValues.begin();
                 varIt != inputValues.end(); varIt++, ivar++) {
               iV.push_back(NormVariable( *varIt, fVmin[ivar], fVmax[ivar] ));
            }
            Transform( iV, -1 );
            retval = GetMvaValue__( iV );
         }
         else {
            std::vector<double> iV;
            int ivar = 0;
            for (std::vector<double>::const_iterator varIt = inputValues.begin();
                 varIt != inputValues.end(); varIt++, ivar++) {
               iV.push_back(*varIt);
            }
            Transform( iV, -1 );
            retval = GetMvaValue__( iV );
         }
      }

      return retval;
   }

//_______________________________________________________________________
inline void ReadMLP::InitTransform_1()
{
   // Normalization transformation, initialisation
   fMin_1[0][0] = 5;
   fMax_1[0][0] = 34;
   fMin_1[1][0] = 5;
   fMax_1[1][0] = 18;
   fMin_1[2][0] = 5;
   fMax_1[2][0] = 34;
   fMin_1[0][1] = 0;
   fMax_1[0][1] = 22;
   fMin_1[1][1] = 0;
   fMax_1[1][1] = 9;
   fMin_1[2][1] = 0;
   fMax_1[2][1] = 22;
   fMin_1[0][2] = 1.10716809773e-17;
   fMax_1[0][2] = 0.999991416931;
   fMin_1[1][2] = 1.04131156822e-12;
   fMax_1[1][2] = 0.999935925007;
   fMin_1[2][2] = 1.10716809773e-17;
   fMax_1[2][2] = 0.999991416931;
   fMin_1[0][3] = -3.59665679932;
   fMax_1[0][3] = 5.05114507675;
   fMin_1[1][3] = -6.6865940094;
   fMax_1[1][3] = 5.33746910095;
   fMin_1[2][3] = -6.6865940094;
   fMax_1[2][3] = 5.33746910095;
   fMin_1[0][4] = -2;
   fMax_1[0][4] = 0.999933362007;
   fMin_1[1][4] = -2;
   fMax_1[1][4] = 0.999999821186;
   fMin_1[2][4] = -2;
   fMax_1[2][4] = 0.999999821186;
   fMin_1[0][5] = 0.000780336209573;
   fMax_1[0][5] = 0.00934400502592;
   fMin_1[1][5] = 0.000928723777179;
   fMax_1[1][5] = 0.36220741272;
   fMin_1[2][5] = 0.000780336209573;
   fMax_1[2][5] = 0.36220741272;
   fMin_1[0][6] = 0.00150164938532;
   fMax_1[0][6] = 0.0170790404081;
   fMin_1[1][6] = 0.00142211036291;
   fMax_1[1][6] = 3.00996232033;
   fMin_1[2][6] = 0.00142211036291;
   fMax_1[2][6] = 3.00996232033;
   fMin_1[0][7] = 0.229534015059;
   fMax_1[0][7] = 36.9986686707;
   fMin_1[1][7] = 0.142663016915;
   fMax_1[1][7] = 92.6201324463;
   fMin_1[2][7] = 0.142663016915;
   fMax_1[2][7] = 92.6201324463;
   fMin_1[0][8] = -0.758881688118;
   fMax_1[0][8] = 0.952944278717;
   fMin_1[1][8] = -0.979679763317;
   fMax_1[1][8] = 0.999767661095;
   fMin_1[2][8] = -0.979679763317;
   fMax_1[2][8] = 0.999767661095;
   fMin_1[0][9] = 0;
   fMax_1[0][9] = 2006.76025391;
   fMin_1[1][9] = 0;
   fMax_1[1][9] = 3789.05102539;
   fMin_1[2][9] = 0;
   fMax_1[2][9] = 3789.05102539;
   fMin_1[0][10] = 1.5146971941;
   fMax_1[0][10] = 232.810134888;
   fMin_1[1][10] = 1.0471663475;
   fMax_1[1][10] = 1040.47387695;
   fMin_1[2][10] = 1.0471663475;
   fMax_1[2][10] = 1040.47387695;
   fMin_1[0][11] = 0.000926514097955;
   fMax_1[0][11] = 1.81163454056;
   fMin_1[1][11] = 0.000956738600507;
   fMax_1[1][11] = 2.26235461235;
   fMin_1[2][11] = 0.000926514097955;
   fMax_1[2][11] = 2.26235461235;
   fMin_1[0][12] = 0.935113430023;
   fMax_1[0][12] = 5.76238298416;
   fMin_1[1][12] = 0.0571069195867;
   fMax_1[1][12] = 5.84594631195;
   fMin_1[2][12] = 0.0571069195867;
   fMax_1[2][12] = 5.84594631195;
   fMin_1[0][13] = 0;
   fMax_1[0][13] = 7;
   fMin_1[1][13] = 0;
   fMax_1[1][13] = 5;
   fMin_1[2][13] = 0;
   fMax_1[2][13] = 7;
   fMin_1[0][14] = 0;
   fMax_1[0][14] = 1079.31750488;
   fMin_1[1][14] = 0;
   fMax_1[1][14] = 152.220748901;
   fMin_1[2][14] = 0;
   fMax_1[2][14] = 1079.31750488;
}

//_______________________________________________________________________
inline void ReadMLP::Transform_1( std::vector<double>& iv, int cls) const
{
   // Normalization transformation
   if (cls < 0 || cls > 2) {
   if (2 > 1 ) cls = 2;
      else cls = 2;
   }
   const int nVar = 15;

   // get indices of used variables

   // define the indices of the variables which are transformed by this transformation
   std::vector<int> indicesGet;
   std::vector<int> indicesPut;

   indicesGet.push_back( 0);
   indicesGet.push_back( 1);
   indicesGet.push_back( 2);
   indicesGet.push_back( 3);
   indicesGet.push_back( 4);
   indicesGet.push_back( 5);
   indicesGet.push_back( 6);
   indicesGet.push_back( 7);
   indicesGet.push_back( 8);
   indicesGet.push_back( 9);
   indicesGet.push_back( 10);
   indicesGet.push_back( 11);
   indicesGet.push_back( 12);
   indicesGet.push_back( 13);
   indicesGet.push_back( 14);
   indicesPut.push_back( 0);
   indicesPut.push_back( 1);
   indicesPut.push_back( 2);
   indicesPut.push_back( 3);
   indicesPut.push_back( 4);
   indicesPut.push_back( 5);
   indicesPut.push_back( 6);
   indicesPut.push_back( 7);
   indicesPut.push_back( 8);
   indicesPut.push_back( 9);
   indicesPut.push_back( 10);
   indicesPut.push_back( 11);
   indicesPut.push_back( 12);
   indicesPut.push_back( 13);
   indicesPut.push_back( 14);

   std::vector<double> dv(nVar);
   for (int ivar=0; ivar<nVar; ivar++) dv[ivar] = iv[indicesGet.at(ivar)];
   for (int ivar=0;ivar<15;ivar++) {
      double offset = fMin_1[cls][ivar];
      double scale  = 1.0/(fMax_1[cls][ivar]-fMin_1[cls][ivar]);
      iv[indicesPut.at(ivar)] = (dv[ivar]-offset)*scale * 2 - 1;
   }
}

//_______________________________________________________________________
inline void ReadMLP::InitTransform()
{
   InitTransform_1();
}

//_______________________________________________________________________
inline void ReadMLP::Transform( std::vector<double>& iv, int sigOrBgd ) const
{
   Transform_1( iv, sigOrBgd );
}

#endif
