#include "JMTucker/Tools/interface/AnalysisEras.h"
#include "JMTucker/Tools/interface/TrackRescaler.h"
#include <vector>  //Alec added
#include <iostream> //Alec added
using namespace std; //Alec added

//FIXME: need further study to see whether this need to be changed
//JetHT parameter apply to high HT
namespace jmt {
  void TrackRescaler::set_JetHT2017B(double x, double eta) {
    if (fabs(eta) < 1.5) {
      const double p_dxy[8] = {1.003954411196716, 0.04680608038556485, 1.1651640253424076, 0.010686515626581808, 1.2423728669230774, 0.002510211465163767, 1.301491397216935, -0.0005992241020962791};
      const double p_dsz[10] = {1.0245229183638793, 0.06544824469215105, 1.1860096333638355, 0.009315198253046261, 1.2534005803324926, -0.0010188848309496473, 1.2759550243574909, -0.0033600655572815436, 2.0547714269037252e-05, -3.967354320030131e-08};
      const double p_dxydsz[5] = {1.2373808693167834, -0.06306772746156655, 0.9989407561722071, 0.004296811774057659, 1.0281436760070548};

      scales_.set((x<=5)*(p_dxy[0]+p_dxy[1]*x)+(x>5&&x<=10)*(p_dxy[2]+p_dxy[3]*x)+(x>10&&x<=19)*(p_dxy[4]+p_dxy[5]*x)+(x>19&&x<=200)*(p_dxy[6]+p_dxy[7]*x)+(x>200)*(p_dxy[6]+p_dxy[7]*200),
                  (x<=3)*(p_dsz[0]+p_dsz[1]*x)+(x>3&&x<=7)*(p_dsz[2]+p_dsz[3]*x)+(x>7&&x<=11)*(p_dsz[4]+p_dsz[5]*x)+(x>11&&x<=200)*(p_dsz[6]+p_dsz[7]*x+p_dsz[8]*pow(x,2)+p_dsz[9]*pow(x,3))+(x>200)*(p_dsz[6]+p_dsz[7]*200+p_dsz[8]*pow(200,2)+p_dsz[9]*pow(200,3)),
                  (x<=3.5)*(p_dxydsz[0]+p_dxydsz[1]*x)+(x>3.5&&x<=20)*(p_dxydsz[2]+p_dxydsz[3]*x)+(x>20)*p_dxydsz[4]
                  );
    }
    else {
      const double p_dxy[8] = {0.9809194238515303, 0.02988345020861421, 1.0494209346433279, 0.01638247946618149, 1.1747904134913318, 0.004173705981459077, 1.27170013468283, -0.0015234534159011834};
      const double p_dsz[7] = {0.9741157497540216, 0.03454031770932743, 1.1551685052673273, 0.008041427889944022, 1.3366714462830347, -0.0034743381492504328, 1.3448120785319356e-05};
      const double p_dxydsz[5] = {1.1772587629670426, -0.012843798533138594, 1.097301005478153, -0.005013846780833367, 0.952633219303397};

      scales_.set((x<=5)*(p_dxy[0]+p_dxy[1]*x)+(x>5&&x<=10)*(p_dxy[2]+p_dxy[3]*x)+(x>10&&x<=19)*(p_dxy[4]+p_dxy[5]*x)+(x>19&&x<=200)*(p_dxy[6]+p_dxy[7]*x)+(x>200)*(p_dxy[6]+p_dxy[7]*200),
                  (x<=7)*(p_dsz[0]+p_dsz[1]*x)+(x>7&&x<=17)*(p_dsz[2]+p_dsz[3]*x)+(x>17&&x<=200)*(p_dsz[4]+p_dsz[5]*x+p_dsz[6]*pow(x,2))+(x>200)*(p_dsz[4]+p_dsz[5]*200+p_dsz[6]*pow(200,2)),
                  (x<=5)*(p_dxydsz[0]+p_dxydsz[1]*x)+(x>5&&x<=21)*(p_dxydsz[2]+p_dxydsz[3]*x)+(x>21)*p_dxydsz[4]
                  );
    }
  }

  void TrackRescaler::set_JetHT2017C(double x, double eta) {
    if (fabs(eta) < 1.5) {
      const double p_dxy[11] = {1.0161768012596906, 0.042041901495531005, 1.1717021770368574, 0.00669013252978249, 1.1971514114269148, 0.0035674496589963335, 1.2470479301245583, -0.0009085954728102639, 1.251603593260837, -0.001172576224929787, 1.9465546830349183e-06};
      const double p_dsz[11] = {1.0492585958417804, 0.08118563766830778, 1.2705697427223215, 0.0032212677086543235, 1.3094832265892142, -0.0037477087686636043, 1.3514702985281841, -0.00876085217779441, 8.598124845502029e-05, -3.842285480601181e-07, 6.029555491156424e-10};
      const double p_dxydsz[5] = {1.291753251455697, -0.11200986158634538, 0.8988572749578425, -0.000993555909164761, 0.8232367847064167};

      scales_.set((x<=5)*(p_dxy[0]+p_dxy[1]*x)+(x>5&&x<=8)*(p_dxy[2]+p_dxy[3]*x)+(x>8&&x<=11)*(p_dxy[4]+p_dxy[5]*x)+(x>11&&x<=19)*(p_dxy[6]+p_dxy[7]*x)+(x>19&&x<=200)*(p_dxy[8]+p_dxy[9]*x+p_dxy[10]*pow(x,2))+(x>200)*(p_dxy[8]+p_dxy[9]*200+p_dxy[10]*pow(200,2)),
                  (x<=3)*(p_dsz[0]+p_dsz[1]*x)+(x>3&&x<=7)*(p_dsz[2]+p_dsz[3]*x)+(x>7&&x<=12)*(p_dsz[4]+p_dsz[5]*x)+(x>12&&x<=200)*(p_dsz[6]+p_dsz[7]*x+p_dsz[8]*pow(x,2)+p_dsz[9]*pow(x,3)+p_dsz[10]*pow(x,4))+(x>200)*(p_dsz[6]+p_dsz[7]*200+p_dsz[8]*pow(200,2)+p_dsz[9]*pow(200,3)+p_dsz[10]*pow(200,4)),
                  (x<=3.5)*(p_dxydsz[0]+p_dxydsz[1]*x)+(x>3.5&&x<=20)*(p_dxydsz[2]+p_dxydsz[3]*x)+(x>20)*p_dxydsz[4]
                  );
    }
    else {
      const double p_dxy[9] = {0.9839923368596756, 0.02430462999210955, 1.0180594006964852, 0.016554773836364164, 1.1079693887355095, 0.005217622826386567, 1.2455318260814945, -0.00301224704167776, 9.488960776721558e-06};
      const double p_dsz[11] = {0.9493659211706715, 0.0822651027868656, 1.291903962581168, 0.01824914776720852, 1.4851588554912978, -0.0005827669494445938, 1.62279301085992, -0.010047580573274734, 5.415895149532794e-05, 1.0757936894853994e-08, -5.818483773901319e-10};
      const double p_dxydsz[5] = {1.1592379138920268, -0.06068316015086136, 0.8522685428672403, -0.006100542684956953, 0.7774233037126433};

      scales_.set((x<=5)*(p_dxy[0]+p_dxy[1]*x)+(x>5&&x<=8)*(p_dxy[2]+p_dxy[3]*x)+(x>8&&x<=19)*(p_dxy[4]+p_dxy[5]*x)+(x>19&&x<=200)*(p_dxy[6]+p_dxy[7]*x+p_dxy[8]*pow(x,2))+(x>200)*(p_dxy[6]+p_dxy[7]*200+p_dxy[8]*pow(200,2)),
                  (x<=5.5)*(p_dsz[0]+p_dsz[1]*x)+(x>5.5&&x<=10)*(p_dsz[2]+p_dsz[3]*x)+(x>10&&x<=19)*(p_dsz[4]+p_dsz[5]*x)+(x>19&&x<=200)*(p_dsz[6]+p_dsz[7]*x+p_dsz[8]*pow(x,2)+p_dsz[9]*pow(x,3)+p_dsz[10]*pow(x,4))+(x>200)*(p_dsz[6]+p_dsz[7]*200+p_dsz[8]*pow(200,2)+p_dsz[9]*pow(200,3)+p_dsz[10]*pow(200,4)),
                  (x<=4.5)*(p_dxydsz[0]+p_dxydsz[1]*x)+(x>4.5&&x<=21)*(p_dxydsz[2]+p_dxydsz[3]*x)+(x>21)*p_dxydsz[4]
                  );
    }
  }

  void TrackRescaler::set_JetHT2017DE(double x, double eta) {
    if (fabs(eta) < 1.5) {
      const double p_dxy[9] = {0.9958341628606665, 0.023815756395143658, 1.071738238640757, 0.006782337094144922, 1.1330981925851835, 0.00015785672276847224, 1.170129041506572, -0.0016917369270458358, 5.3937634669262654e-06};
      const double p_dsz[8] = {1.0145308767949242, 0.06023485905656432, 1.1774762080717533, 0.004158899681702615, 1.251578501191003, -0.005737179860514227, 4.03056359898546e-05, -9.546973869635759e-08};
      const double p_dxydsz[5] = {1.0633535739740558, -0.048896075027159376, 0.8892955287512224, -0.0009422431396516016, 0.8383948468014116};

      scales_.set((x<=5)*(p_dxy[0]+p_dxy[1]*x)+(x>5&&x<=9)*(p_dxy[2]+p_dxy[3]*x)+(x>9&&x<=20)*(p_dxy[4]+p_dxy[5]*x)+(x>20&&x<=200)*(p_dxy[6]+p_dxy[7]*x+p_dxy[8]*pow(x,2))+(x>200)*(p_dxy[6]+p_dxy[7]*200+p_dxy[8]*pow(200,2)),
                  (x<=3)*(p_dsz[0]+p_dsz[1]*x)+(x>3&&x<=8)*(p_dsz[2]+p_dsz[3]*x)+(x>8&&x<=200)*(p_dsz[4]+p_dsz[5]*x+p_dsz[6]*pow(x,2)+p_dsz[7]*pow(x,3))+(x>200)*(p_dsz[4]+p_dsz[5]*200+p_dsz[6]*pow(200,2)+p_dsz[7]*pow(200,3)),
                  (x<=3.5)*(p_dxydsz[0]+p_dxydsz[1]*x)+(x>3.5&&x<=20)*(p_dxydsz[2]+p_dxydsz[3]*x)+(x>20)*p_dxydsz[4]
                  );
    }
    else {
      const double p_dxy[9] = {0.9902445099668238, 0.006934208617877735, 0.9744731512541432, 0.012034983205999293, 1.0629826235864053, 0.0029136479108657146, 1.170459333797536, -0.0018981811098766116, 6.403573224467264e-06};
      const double p_dsz[10] = {0.9655353376051706, 0.03948647373196264, 1.1446808507342674, 0.010962801074448891, 1.2599056250973795, 0.00033785088924465306, 1.3942188620396598, -0.00684412727829742, 4.332240884536905e-05, -8.792941673523394e-08};
      const double p_dxydsz[5] = {0.9283521729147935, -0.003769450899472301, 0.8980042607612827, -0.0022320448484044655, 0.8695603485477653};

      scales_.set((x<=5)*(p_dxy[0]+p_dxy[1]*x)+(x>5&&x<=9)*(p_dxy[2]+p_dxy[3]*x)+(x>9&&x<=20)*(p_dxy[4]+p_dxy[5]*x)+(x>20&&x<=200)*(p_dxy[6]+p_dxy[7]*x+p_dxy[8]*pow(x,2))+(x>200)*(p_dxy[6]+p_dxy[7]*200+p_dxy[8]*pow(200,2)),
                  (x<=7)*(p_dsz[0]+p_dsz[1]*x)+(x>7&&x<=13)*(p_dsz[2]+p_dsz[3]*x)+(x>13&&x<=21)*(p_dsz[4]+p_dsz[5]*x)+(x>21&&x<=200)*(p_dsz[6]+p_dsz[7]*x+p_dsz[8]*pow(x,2)+p_dsz[9]*pow(x,3))+(x>200)*(p_dsz[6]+p_dsz[7]*200+p_dsz[8]*pow(200,2)+p_dsz[9]*pow(200,3)),
                  (x<=5)*(p_dxydsz[0]+p_dxydsz[1]*x)+(x>5&&x<=21)*(p_dxydsz[2]+p_dxydsz[3]*x)+(x>21)*p_dxydsz[4]
                  );
    }
  }

  void TrackRescaler::set_JetHT2017F(double x, double eta) {
    if (fabs(eta) < 1.5) {
      const double p_dxy[9] = {1.02507143855885, 0.035682416838607, 1.1630170173759637, 0.004135059939736778, 1.2157833722885292, -0.0015115779115216182, 1.231899976429208, -0.0026144724219604736, 7.601335880195158e-06};
      const double p_dsz[10] = {1.0531495875855903, 0.05985532137012233, 1.2357977380860046, 0.004052611805848134, 1.2812877188371545, -0.003684138598605247, 1.3203497359522545, -0.00782694386275162, 5.598493204763304e-05, -1.3740304386617287e-07};
      const double p_dxydsz[7] = {1.2055709843570976, -0.06934397474723346, 0.9623420790557042, -0.0029739123523973656, 0.9247086191627053, -0.0027398170929929418, 0.7654225404225834};

      scales_.set((x<=5)*(p_dxy[0]+p_dxy[1]*x)+(x>5&&x<=9)*(p_dxy[2]+p_dxy[3]*x)+(x>9&&x<=17)*(p_dxy[4]+p_dxy[5]*x)+(x>17&&x<=200)*(p_dxy[6]+p_dxy[7]*x+p_dxy[8]*pow(x,2))+(x>200)*(p_dxy[6]+p_dxy[7]*200+p_dxy[8]*pow(200,2)),
                  (x<=3.5)*(p_dsz[0]+p_dsz[1]*x)+(x>3.5&&x<=6)*(p_dsz[2]+p_dsz[3]*x)+(x>6&&x<=13)*(p_dsz[4]+p_dsz[5]*x)+(x>13&&x<=200)*(p_dsz[6]+p_dsz[7]*x+p_dsz[8]*pow(x,2)+p_dsz[9]*pow(x,3))+(x>200)*(p_dsz[6]+p_dsz[7]*200+p_dsz[8]*pow(200,2)+p_dsz[9]*pow(200,3)),
                  (x<=3.5)*(p_dxydsz[0]+p_dxydsz[1]*x)+(x>3.5&&x<=20)*(p_dxydsz[2]+p_dxydsz[3]*x)+(x>20&&x<=60)*(p_dxydsz[4]+p_dxydsz[5]*x)+(x>60)*p_dxydsz[6]
                  );
    }
    else {
      const double p_dxy[9] = {0.9855065768424701, 0.021753810507718217, 1.0549206517648415, 0.009742124539396489, 1.1237284934232026, 0.0034751924685682317, 1.2328186747546215, -0.002983564755841868, 9.62782905533306e-06};
      const double p_dsz[8] = {0.9576484312028871, 0.06012619494580462, 1.2849093402304101, 0.007793339895653828, 1.5233812422690591, -0.009001069977632883, 5.652031220754525e-05, -1.213962343039487e-07};
      const double p_dxydsz[5] = {1.0720609338851717, -0.025840782949423238, 0.9241594442252488, -0.004200723132161754, 0.8428807481959472};

      scales_.set((x<=5)*(p_dxy[0]+p_dxy[1]*x)+(x>5&&x<=9)*(p_dxy[2]+p_dxy[3]*x)+(x>9&&x<=17)*(p_dxy[4]+p_dxy[5]*x)+(x>17&&x<=200)*(p_dxy[6]+p_dxy[7]*x+p_dxy[8]*pow(x,2))+(x>200)*(p_dxy[6]+p_dxy[7]*200+p_dxy[8]*pow(200,2)),
                  (x<=7)*(p_dsz[0]+p_dsz[1]*x)+(x>7&&x<=16)*(p_dsz[2]+p_dsz[3]*x)+(x>16&&x<=200)*(p_dsz[4]+p_dsz[5]*x+p_dsz[6]*pow(x,2)+p_dsz[7]*pow(x,3))+(x>200)*(p_dsz[4]+p_dsz[5]*200+p_dsz[6]*pow(200,2)+p_dsz[7]*pow(200,3)),
                  (x<=5)*(p_dxydsz[0]+p_dxydsz[1]*x)+(x>5&&x<=21)*(p_dxydsz[2]+p_dxydsz[3]*x)+(x>21)*p_dxydsz[4]
                  );
    }
  }

  void TrackRescaler::set_JetHT2018A(double x, double eta) {
    if (fabs(eta) < 1.5) {
      const double p_dxy[4] = {0.9944651408847637, 0.0003100409123238388, 1.0133318600684997, -0.0002725492604450176};
      const double p_dsz[7] = {0.9545689305290876, -0.005788633682068279, 0.9163531438716942, 0.008255804537721637, -0.0002541675288772417, 0.9906779761637563, -0.000408665473206192};
      const double p_dxydsz[6] = {0.9552901105055515, 0.0553433274762117, 1.2577461745166036, -0.013442809569614248, 0.9387984003983484, -0.0008562833690257464};

      scales_.set((x<=15)*(p_dxy[0]+p_dxy[1]*x)+(x>15&&x<=200)*(p_dxy[2]+p_dxy[3]*x)+(x>200)*(p_dxy[2]+p_dxy[3]*200),
                  (x<=3.5)*(p_dsz[0]+p_dsz[1]*x)+(x>3.5&&x<=20)*(p_dsz[2]+p_dsz[3]*x+p_dsz[4]*pow(x,2))+(x>20&&x<=200)*(p_dsz[5]+p_dsz[6]*x)+(x>200)*(p_dsz[5]+p_dsz[6]*200),
                  (x<=5)*(p_dxydsz[0]+p_dxydsz[1]*x)+(x>5&&x<=10)*(p_dxydsz[2]+p_dxydsz[3]*x)+(x>10&&x<=25)*(p_dxydsz[2]+p_dxydsz[3]*x)+(x>25&&x<=200)*(p_dxydsz[4]+p_dxydsz[5]*x)+(x>200)*(p_dxydsz[4]+p_dxydsz[5]*200)
                  );
    }
    else {
      const double p_dxy[9] = {0.9956638266790775, 0.01311762974898705, 1.0324554787776068, 0.0028794133659762076, 1.0435318764233166, 0.0009594998914445711, 1.0805733205008456, -0.00090961749403609, 2.7865570333431475e-06};
      const double p_dsz[8] = {1.0140154016738616, -0.04030698229824987, 0.8577572602839483, -0.004629518437424471, 0.7862533145771442, 0.002836810498017997, -2.4938561562441677e-05, 6.667933060770695e-08};
      const double p_dxydsz[7] = {1.2031550984529447, 0.017203685604559395, 1.384121127295515, -0.010099538962099513, 1.2839748504629604, -0.0068437725679720215, 0.8675620454856555};

      scales_.set((x<=4)*(p_dxy[0]+p_dxy[1]*x)+(x>4&&x<=10)*(p_dxy[2]+p_dxy[3]*x)+(x>10&&x<=22)*(p_dxy[4]+p_dxy[5]*x)+(x>22&&x<=200)*(p_dxy[6]+p_dxy[7]*x+p_dxy[8]*pow(x,2))+(x>200)*(p_dxy[6]+p_dxy[7]*200+p_dxy[8]*pow(200,2)),
                  (x<=5)*(p_dsz[0]+p_dsz[1]*x)+(x>5&&x<=10)*(p_dsz[2]+p_dsz[3]*x)+(x>10&&x<=200)*(p_dsz[4]+p_dsz[5]*x+p_dsz[6]*pow(x,2)+p_dsz[7]*pow(x,3))+(x>200)*(p_dsz[4]+p_dsz[5]*200+p_dsz[6]*pow(200,2)+p_dsz[7]*pow(200,3)),
                  (x<=7)*(p_dxydsz[0]+p_dxydsz[1]*x)+(x>7&&x<=20)*(p_dxydsz[2]+p_dxydsz[3]*x)+(x>20&&x<=60)*(p_dxydsz[4]+p_dxydsz[5]*x)+(x>60)*p_dxydsz[6]
                  );
    }
  }

  void TrackRescaler::set_JetHT2018B(double x, double eta) {
    if (fabs(eta) < 1.5) {
      const double p_dxy[6] = {1.0256264904575256, 0.009715735968613925, 1.068844323041154, 0.00033895695306054006, 1.0848778079691845, -0.0006977308728749745};
      const double p_dsz[9] = {0.9833226242346282, 0.0071660524462303895, 0.9986713490547589, 0.0049036996534738775, 1.0388229095240424, 0.0005066627844654905, 1.0783250345578144, -0.0015397166527444765, 4.242917947464464e-06};
      const double p_dxydsz[7] = {1.124793037516908, 0.01914449930639376, 1.2810760942113992, -0.015293440249163699, 1.0148982357550616, -0.0025529706682178525, 8.59087101168877e-06};

      scales_.set((x<=5)*(p_dxy[0]+p_dxy[1]*x)+(x>5&&x<=20)*(p_dxy[2]+p_dxy[3]*x)+(x>20&&x<=200)*(p_dxy[4]+p_dxy[5]*x)+(x>200)*(p_dxy[4]+p_dxy[5]*200),
                  (x<=4)*(p_dsz[0]+p_dsz[1]*x)+(x>4&&x<=10)*(p_dsz[2]+p_dsz[3]*x)+(x>10&&x<=20)*(p_dsz[4]+p_dsz[5]*x)+(x>20&&x<=200)*(p_dsz[6]+p_dsz[7]*x+p_dsz[8]*pow(x,2))+(x>200)*(p_dsz[6]+p_dsz[7]*200+p_dsz[8]*pow(200,2)),
                  (x<=5)*(p_dxydsz[0]+p_dxydsz[1]*x)+(x>5&&x<=20)*(p_dxydsz[2]+p_dxydsz[3]*x)+(x>20&&x<=200)*(p_dxydsz[4]+p_dxydsz[5]*x+p_dxydsz[6]*pow(x,2))+(x>200)*(p_dxydsz[4]+p_dxydsz[5]*200+p_dxydsz[6]*pow(200,2))
                  );
    }
    else {
      const double p_dxy[7] = {0.9942554971947344, 0.029208330046791322, 1.1235485672857737, 0.00027768700364697133, 1.187023460774488, -0.002575725575608303, 8.245747692776023e-06};
      const double p_dsz[7] = {1.0167140774242465, -0.032708194933232064, 0.9324407187709378, -0.011435288449341503, 0.0005377023719642616, 0.8940958127845231, 0.0001301033835020374};
      const double p_dxydsz[7] = {1.4789398005907999, 0.013491081544295418, 1.6937002770041638, -0.02092983741448696, 1.4393828519124914, -0.00969425131501225, 3.8016115943619035e-05};

      scales_.set((x<=5)*(p_dxy[0]+p_dxy[1]*x)+(x>5&&x<=25)*(p_dxy[2]+p_dxy[3]*x)+(x>25&&x<=200)*(p_dxy[4]+p_dxy[5]*x+p_dxy[6]*pow(x,2))+(x>200)*(p_dxy[4]+p_dxy[5]*200+p_dxy[6]*pow(200,2)),
                  (x<=4)*(p_dsz[0]+p_dsz[1]*x)+(x>4&&x<=17)*(p_dsz[2]+p_dsz[3]*x+p_dsz[4]*pow(x,2))+(x>17&&x<=200)*(p_dsz[5]+p_dsz[6]*x)+(x>200)*(p_dsz[5]+p_dsz[6]*200),
                  (x<=6)*(p_dxydsz[0]+p_dxydsz[1]*x)+(x>6&&x<=20)*(p_dxydsz[2]+p_dxydsz[3]*x)+(x>20&&x<=200)*(p_dxydsz[4]+p_dxydsz[5]*x+p_dxydsz[6]*pow(x,2))+(x>200)*(p_dxydsz[4]+p_dxydsz[5]*200+p_dxydsz[6]*pow(200,2))
                  );
    }
  }

  void TrackRescaler::set_JetHT2018C(double x, double eta) {
    if (fabs(eta) < 1.5) {
      const double p_dxy[7] = {1.0302540567003182, 0.013197495129669386, -0.019689839265792486, 0.0011915978744290266, 1.1015931462176, -0.0017612236034551046, 4.940039349770814e-06};
      const double p_dsz[9] = {0.9912887712662574, 0.00859718807110327, 1.0167899738314499, 0.004188850233047356, 1.063093537733667, -0.00035888586676950413, 1.0828841838238998, -0.0015723297743335614, 3.91610610491999e-06};
      const double p_dxydsz[7] = {1.180729792563169, 0.009006964511076306, 1.2731621239981623, -0.014484683652236648, 0.9761251034739371, -0.002575876654600912, 1.0393275942124709e-05};

      scales_.set((x<=4)*(p_dxy[0]+p_dxy[1]*x)+(x>4&&x<=20)*(p_dxy[2]+p_dxy[3]*x)+(x>4&&x<=200)*(p_dxy[4]+p_dxy[5]*x+p_dxy[6]*pow(x,2))+(x>200)*(p_dxy[4]+p_dxy[5]*200+p_dxy[6]*pow(200,2)),
                  (x<=5)*(p_dsz[0]+p_dsz[1]*x)+(x>5&&x<=9)*(p_dsz[2]+p_dsz[3]*x)+(x>9&&x<=17)*(p_dsz[4]+p_dsz[5]*x)+(x>17&&x<=200)*(p_dsz[6]+p_dsz[7]*x+p_dsz[8]*pow(x,2))+(x>200)*(p_dsz[6]+p_dsz[7]*200+p_dsz[8]*pow(200,2)),
                  (x<=4)*(p_dxydsz[0]+p_dxydsz[1]*x)+(x>4&&x<=25)*(p_dxydsz[2]+p_dxydsz[3]*x)+(x>25&&x<=200)*(p_dxydsz[4]+p_dxydsz[5]*x+p_dxydsz[6]*pow(x,2))+(x>200)*(p_dxydsz[4]+p_dxydsz[5]*200+p_dxydsz[6]*pow(200,2))
                  );
    }
    else {
      const double p_dxy[9] = {0.9930850416130731, 0.034917683150413985, 1.0937098590923977, 0.007629689779291711, 1.159171907659493, -0.00021289424286392985, 1.1988856358148134, -0.0024894191562249246, 9.85583519235196e-06};
      const double p_dsz[8] = {1.008840672713832, -0.02714063566702515, 0.9046206654979322, -0.0030406210476378818, 0.8772810420132723, 0.0004512486169276639, 0.8973183732699721, 7.82644843746967e-05};
      const double p_dxydsz[8] = {1.5841905135970438, 0.008588585620311284, 1.585498321932181, -0.0017576002355790517, 1.6922017618757823, -0.016221930264984336, 1.0946507830770524, -0.0013293929099910803};

      scales_.set((x<=5)*(p_dxy[0]+p_dxy[1]*x)+(x>5&&x<=9)*(p_dxy[2]+p_dxy[3]*x)+(x>9&&x<=20)*(p_dxy[4]+p_dxy[5]*x)+(x>20&&x<=200)*(p_dxy[6]+p_dxy[7]*x+p_dxy[8]*pow(x,2))+(x>200)*(p_dxy[6]+p_dxy[7]*200+p_dxy[8]*pow(200,2)),
                  (x<=5)*(p_dsz[0]+p_dsz[1]*x)+(x>5&&x<=9)*(p_dsz[2]+p_dsz[3]*x)+(x>9&&x<=17)*(p_dsz[4]+p_dsz[5]*x)+(x>17&&x<=200)*(p_dsz[6]+p_dsz[7]*x)+(x>200)*(p_dsz[6]+p_dsz[7]*200),
                  (x<=5)*(p_dxydsz[0]+p_dxydsz[1]*x)+(x>5&&x<=10)*(p_dxydsz[2]+p_dxydsz[3]*x)+(x>10&&x<=40)*(p_dxydsz[4]+p_dxydsz[5]*x)+(x>40&&x<=200)*(p_dxydsz[6]+p_dxydsz[7]*x)+(x>200)*(p_dxydsz[6]+p_dxydsz[7]*200)
                  );
    }
  }

  void TrackRescaler::set_JetHT2018D(double x, double eta) {
    if (fabs(eta) < 1.5) {
      const double p_dxy[9] = {1.0149539511516237, 0.026557574255677584, 1.0775759322350924, 0.005199456392796661, 1.1172567499833552, 0.00029550032896444485, 1.144144230550563, -0.0015803270993739878, 3.7139899854107313e-06};
      const double p_dsz[9] = {1.0016164882163539, 0.014316358907761777, 1.0372583625077623, 0.00691907940640445, 1.0951155778742487, 0.0004128671983521199, 1.1392404223219428, -0.002156753822489316, 6.403416833996928e-06};
      const double p_dxydsz[7] = {1.152256405398597, 0.02069954776458397, 1.3494744427024379, -0.0166970053084306, 1.0872513823821675, -0.004525737159592511, 0.8255652889052753};

      scales_.set((x<=3)*(p_dxy[0]+p_dxy[1]*x)+(x>3&&x<=10)*(p_dxy[2]+p_dxy[3]*x)+(x>10&&x<=15)*(p_dxy[4]+p_dxy[5]*x)+(x>15&&x<=200)*(p_dxy[6]+p_dxy[7]*x+p_dxy[8]*pow(x,2))+(x>200)*(p_dxy[6]+p_dxy[7]*200+p_dxy[8]*pow(200,2)),
                  (x<=5)*(p_dsz[0]+p_dsz[1]*x)+(x>5&&x<=9)*(p_dsz[2]+p_dsz[3]*x)+(x>9&&x<=17)*(p_dsz[4]+p_dsz[5]*x)+(x>17&&x<=200)*(p_dsz[6]+p_dsz[7]*x+p_dsz[8]*pow(x,2))+(x>200)*(p_dsz[6]+p_dsz[7]*200+p_dsz[8]*pow(200,2)),
                  (x<=5)*(p_dxydsz[0]+p_dxydsz[1]*x)+(x>5&&x<=20)*(p_dxydsz[2]+p_dxydsz[3]*x)+(x>20&&x<=60)*(p_dxydsz[4]+p_dxydsz[5]*x)+(x>60)*p_dxydsz[6]
                  );
    }
    else {
      const double p_dxy[9] = {0.994381147495573, 0.03648365798779281, 1.1122747895474503, 0.007517290214880828, 1.1685396038118878, 0.0016399776215087246, 1.2358122699505796, -0.002481691850650871, 9.008389210669608e-06};
      const double p_dsz[9] = {1.0208298538168237, -0.015906515857588968, 0.9513989682071168, -0.00016704431123983966, 0.9432501513463789, 0.0011105386766240154, 0.9711559352781072, -1.6347157758553316e-05, -1.0233711920211618e-07};
      const double p_dxydsz[9] = {1.5916557054593765, -0.013311726870981673, 1.5389935556589058, -0.005360374120004968, 2.1087651673683094, -0.04134596978138514, 1.4804181459721781, -0.009180041573825893, 0.9340573014121997};

      scales_.set((x<=5)*(p_dxy[0]+p_dxy[1]*x)+(x>5&&x<=9)*(p_dxy[2]+p_dxy[3]*x)+(x>9&&x<=17)*(p_dxy[4]+p_dxy[5]*x)+(x>17&&x<=200)*(p_dxy[6]+p_dxy[7]*x+p_dxy[8]*pow(x,2))+(x>200)*(p_dxy[6]+p_dxy[7]*200+p_dxy[8]*pow(200,2)),
                  (x<=5)*(p_dsz[0]+p_dsz[1]*x)+(x>5&&x<=9)*(p_dsz[2]+p_dsz[3]*x)+(x>9&&x<=17)*(p_dsz[4]+p_dsz[5]*x)+(x>17&&x<=200)*(p_dsz[6]+p_dsz[7]*x+p_dsz[8]*pow(x,2))+(x>200)*(p_dsz[6]+p_dsz[7]*200+p_dsz[8]*pow(200,2)),
                  (x<=3.5)*(p_dxydsz[0]+p_dxydsz[1]*x)+(x>3.5&&x<=15)*(p_dxydsz[2]+p_dxydsz[3]*x)+(x>15&&x<=20)*(p_dxydsz[4]+p_dxydsz[5]*x)+(x>20&&x<=60)*(p_dxydsz[6]+p_dxydsz[7]*x)+(x>60)*p_dxydsz[8]
                  );
    }
  }

  void TrackRescaler::set_BTagDispJet20161(double x, double eta) {  //Alec tried using 1/scale_factor since scale_ seems to divide
    if (fabs(eta) < 1.5) {
      const double p_dxy[3] = {.90391, .896, -.1585};
      const double p_dsz[3] = {.90834, .7094, -.1133};
      const double p_dxydsz[3] = {.7946, .294, .0963};
    
      scales_.set(p_dxy[0]-p_dxy[2]*exp(-p_dxy[1]*x),
                  p_dsz[0]-p_dsz[2]*exp(-p_dsz[1]*x),
	          p_dxydsz[0]-p_dxydsz[2]*exp(-p_dxydsz[1]*x)
		  );
    }
    else {
      const double p_dxy[3] = {.89441, .3372, -.13827};
      const double p_dsz[3] = {.89631, .1800, -.11508};
      const double p_dxydsz[4] = {.73781, 3.41, -6.0, .002034};
      
      scales_.set(p_dxy[0]-p_dxy[2]*exp(-p_dxy[1]*x),
	          p_dsz[0]-p_dsz[2]*exp(-p_dsz[1]*x),
		  p_dxydsz[0]-p_dxydsz[2]*exp(-p_dxydsz[1]*x)+p_dxydsz[3]*x
		  );
    }
  }

  void TrackRescaler::set_BTagDispJet20162(double x, double eta) {
    if (fabs(eta) < 1.5) {
      const double p_dxy[1] = {0.981341};
      const double p_dsz[3] = {1.8725, -.0005732, -.1141};
      const double p_dxydsz[3] = {.93580, 2.026, .350};

      scales_.set(p_dxy[0],
		  p_dsz[0]-exp(-p_dsz[1]*x+p_dsz[2]),
		  p_dxydsz[0]-p_dxydsz[2]*exp(-p_dxydsz[1]*x)
                  );
    }
    else {
      const double p_dxy[1] = {0.998868};
      const double p_dsz[3] = {1.2526, -.001625, -1.3885};
      const double p_dxydsz[3] = {.9649, .080, -.0512};

      scales_.set(p_dxy[0],
                  p_dsz[0]-exp(-p_dsz[1]*x+p_dsz[2]),
                  p_dxydsz[0]-p_dxydsz[2]*exp(-p_dxydsz[1]*x)
                  );
    }
  }

  void TrackRescaler::set_BTagDispJet2017(double x, double eta) {
    if (fabs(eta) < 1.5) {
      const double p_dxy[3] = {1.17509, .771, -1.263};
      const double p_dsz[3] = {1.15733, 1.274, -1.257};
      const double p_dxydsz[3] = {1.2828, 3.05, -6.1};

      scales_.set(p_dxy[0]-exp(-p_dxy[1]*x+p_dxy[2]),
                  p_dsz[0]-exp(-p_dsz[1]*x+p_dsz[2]),
                  p_dxydsz[0]-p_dxydsz[2]*exp(-p_dxydsz[1]*x)
                  );
    }
    else {
      const double p_dxy[3] = {1.3108, .2508, -.9690};
      const double p_dsz[3] = {1.2758, .1959, -1.1719};
      const double p_dxydsz[3] = {1.526, .285, -.375};

      scales_.set(p_dxy[0]-exp(-p_dxy[1]*x+p_dxy[2]),
                  p_dsz[0]-exp(-p_dsz[1]*x+p_dsz[2]),
                  p_dxydsz[0]-p_dxydsz[2]*exp(-p_dxydsz[1]*x)
                  );
    }
  }

  void TrackRescaler::set_BTagDispJet2018(double x, double eta) {
    if (fabs(eta) < 1.5) {
      const double p_dxy[3] = {1.09967, 1.582, -.842};
      const double p_dsz[3] = {1.11861, 3.14, .91};
      const double p_dxydsz[3] = {1.0866, .595, -.2691};

      scales_.set(p_dxy[0]-exp(-p_dxy[1]*x+p_dxy[2]),
                  p_dsz[0]-exp(-p_dsz[1]*x+p_dsz[2]),
                  p_dxydsz[0]-p_dxydsz[2]*exp(-p_dxydsz[1]*x)
                  );
    }
    else {
      const double p_dxy[3] = {1.1875, .3201, -1.4224};
      const double p_dsz[3] = {1.06183, .402, -2.5405};
      const double p_dxydsz[3] = {1.259, .097, -.197};

      scales_.set(p_dxy[0]-exp(-p_dxy[1]*x+p_dxy[2]),
                  p_dsz[0]-exp(-p_dsz[1]*x+p_dsz[2]),
                  p_dxydsz[0]-p_dxydsz[2]*exp(-p_dxydsz[1]*x)
                  );
    }
  }

  void TrackRescaler::set(double era, int /*which*/, double pt, double eta) {
    if (enable()) {
      //if      (era == jmt::AnalysisEras::e_2017B) set_JetHT2017B(pt, eta);
      //else if (era == jmt::AnalysisEras::e_2017C) set_JetHT2017C(pt, eta);
      //else if (era == jmt::AnalysisEras::e_2017D || era == jmt::AnalysisEras::e_2017E) set_JetHT2017DE(pt, eta);     Alec changed
      //else if (era == jmt::AnalysisEras::e_2017F) set_JetHT2017F(pt, eta);
      //else if (era == jmt::AnalysisEras::e_2018A) set_JetHT2018A(pt, eta);
      //else if (era == jmt::AnalysisEras::e_2018B) set_JetHT2018B(pt, eta);
      //else if (era == jmt::AnalysisEras::e_2018C) set_JetHT2018C(pt, eta);
      //else if (era == jmt::AnalysisEras::e_2018D) set_JetHT2018D(pt, eta);
      if      (era == jmt::AnalysisEras::e_2017B || era == jmt::AnalysisEras::e_2017C || era == jmt::AnalysisEras::e_2017D || era == jmt::AnalysisEras::e_2017E || era == jmt::AnalysisEras::e_2017F) set_BTagDispJet2017(pt, eta);
      else if (era == jmt::AnalysisEras::e_2018A || era == jmt::AnalysisEras::e_2018B || era == jmt::AnalysisEras::e_2018C || era == jmt::AnalysisEras::e_2018D) set_BTagDispJet2018(pt, eta);
      else if (era == jmt::AnalysisEras::e_20161B1 || era == jmt::AnalysisEras::e_20161B2 || era == jmt::AnalysisEras::e_20161C || era == jmt::AnalysisEras::e_20161D || era == jmt::AnalysisEras::e_20161E || era == jmt::AnalysisEras::e_20161F) set_BTagDispJet20161(pt, eta);
      else if (era == jmt::AnalysisEras::e_20162F || era == jmt::AnalysisEras::e_20162G || era == jmt::AnalysisEras::e_20162H) set_BTagDispJet20162(pt, eta);
      else throw std::out_of_range("bad era");
    }
    else
      scales_.reset();
  }

  int counter = 0;
  TrackRescaler::ret_t TrackRescaler::scale(const reco::Track& tk) {
    ret_t r;
    r.tk = tk;

    if (enable()) {
      //std::cout << "Alec prints pt" << tk.pt() << ", Alec prints dxyerr" << scales_.dxyerr() << std::endl; //Alec added
      set(era_, which_, tk.pt(), tk.eta());
      //if ((fabs(tk.eta()) < 1.5) && (counter % 100 == 0)) {
      //  std::cout << "[" << tk.pt() << ", " << scales_.dxyerr() << "], "; //Alec added
      //  counter += 1;
      //}
      //else counter += 1;

      reco::TrackBase::CovarianceMatrix cov = tk.covariance();

      const int i_dxy = reco::TrackBase::i_dxy;
      const int i_dsz = reco::TrackBase::i_dsz;

      for (int idim = 0; idim < reco::TrackBase::dimension; ++idim) {
        if (idim == i_dxy) cov(idim, i_dxy) *= scales_.dxycov();
        else               cov(idim, i_dxy) *= scales_.dxyerr();
      }

      for (int idim = 0; idim < reco::TrackBase::dimension; ++idim) {
        if (idim == i_dsz) cov(idim, i_dsz) *= scales_.dszcov();
        else               cov(idim, i_dsz) *= scales_.dszerr();
      }

      cov(i_dxy, i_dsz) *= scales_.dxydszcov();

      r.rescaled_tk = reco::Track(tk.chi2(), tk.ndof(), tk.referencePoint(), tk.momentum(), tk.charge(), cov, tk.algo());
      r.rescaled_tk.setQualityMask(tk.qualityMask());
      r.rescaled_tk.setNLoops(tk.nLoops());
      (*const_cast<reco::HitPattern*>(&r.rescaled_tk.hitPattern())) = tk.hitPattern(); // lmao
    }
    else
      r.rescaled_tk = tk;

    return r;
  }

}
