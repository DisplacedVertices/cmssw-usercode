#ifndef JMTucker_Tools_interface_PileupWeights_h
#define JMTucker_Tools_interface_PileupWeights_h

#include <stdexcept>

namespace jmt {
  class PileupWeights {
  public:
    PileupWeights() : v_(nullptr) { setup_(); };
    PileupWeights(const std::string& k) : v_(nullptr) { setup_(); set_key(k); }

    bool valid() const { return v_ != nullptr; }

    void set_key(const std::string& k) {
      if (!k.size())
        v_ = nullptr;
      else {
        map_t::const_iterator it = w_.find(k);
        if (it == w_.end())
          throw std::invalid_argument("jmt::PileupWeights: bad key");
        v_ = &it->second;
      }
    }

    double w(int i) const {
      if (!valid() || i < 0 || i >= int(v_->size()))
        return 0;
      return (*v_)[i];
    }

    double w(const std::string& k, int i) {
      set_key(k);
      return w(i);
    }

  private:
    typedef std::map<std::string, std::vector<double>> map_t;
    map_t w_;
    const std::vector<double>* v_;

    void setup_() { // these lines will be parsed in PileupWeights.py, don't break it
      //FIXME: check whether those values need to ba changed for UL
      w_["20162"] = std::vector<double>({0.184739, 3.87862, 3.43873, 2.55711, 1.66222, 1.50921, 1.28595, 1.25693, 0.615431, 1.45522, 1.4954, 1.48321, 1.33156, 1.16429, 1.07819, 1.05333, 1.08185, 1.1281, 1.16611, 1.18882, 1.2123, 1.23819, 1.26049, 1.27054, 1.27151, 1.27133, 1.27212, 1.26675, 1.27518, 1.25199, 1.22257, 1.16871, 1.10992, 1.03781, 0.968667, 0.911656, 0.867131, 0.834894, 0.787916, 0.750576, 0.758612, 0.79302, 0.859323, 0.959067, 1.09514, 1.25685, 1.41972, 1.49691, 1.52938, 1.46324, 1.33617, 1.15483, 0.950685, 0.749146, 0.569927, 0.411027, 0.28984, 0.198626, 0.13758, 0.0964932, 0.0693175, 0.0508504, 0.038385, 0.0299888, 0.0240799, 0.0170695, 0.0124844, 0.0107651, 0.00962124, 0.00879133, 0.00826726, 0.00803058, 0.00783523, 0.00781574, 0.00631688, 0.00535918, 0.00553274, 0.00551791, 0.00589565, 0.00594138, 0.00625883, 0.00628165, 0.00635429, 0.00491238, 0.00435898, 0.00445464, 0.00438023, 0.00456194, 0.00393917, 0.00424369, 0.00310455, 0.00284123, 0.00176242, 0.00148484, 0.00316881, 0.00199287});
      w_["2017"] = std::vector<double>({0.184739, 3.87862, 3.43873, 2.55711, 1.66222, 1.50921, 1.28595, 1.25693, 0.615431, 1.45522, 1.4954, 1.48321, 1.33156, 1.16429, 1.07819, 1.05333, 1.08185, 1.1281, 1.16611, 1.18882, 1.2123, 1.23819, 1.26049, 1.27054, 1.27151, 1.27133, 1.27212, 1.26675, 1.27518, 1.25199, 1.22257, 1.16871, 1.10992, 1.03781, 0.968667, 0.911656, 0.867131, 0.834894, 0.787916, 0.750576, 0.758612, 0.79302, 0.859323, 0.959067, 1.09514, 1.25685, 1.41972, 1.49691, 1.52938, 1.46324, 1.33617, 1.15483, 0.950685, 0.749146, 0.569927, 0.411027, 0.28984, 0.198626, 0.13758, 0.0964932, 0.0693175, 0.0508504, 0.038385, 0.0299888, 0.0240799, 0.0170695, 0.0124844, 0.0107651, 0.00962124, 0.00879133, 0.00826726, 0.00803058, 0.00783523, 0.00781574, 0.00631688, 0.00535918, 0.00553274, 0.00551791, 0.00589565, 0.00594138, 0.00625883, 0.00628165, 0.00635429, 0.00491238, 0.00435898, 0.00445464, 0.00438023, 0.00456194, 0.00393917, 0.00424369, 0.00310455, 0.00284123, 0.00176242, 0.00148484, 0.00316881, 0.00199287});
      w_["2018"] = std::vector<double>({0, 11.5, 54.0978, 19.7888, 11.885, 9.25087, 6.26469, 4.80745, 3.49009, 2.64713, 2.15361, 1.82647, 1.63217, 1.50981, 1.44394, 1.40782, 1.39506, 1.40397, 1.42026, 1.42592, 1.43044, 1.41223, 1.38412, 1.3443, 1.29754, 1.24851, 1.20549, 1.16808, 1.13849, 1.11615, 1.09923, 1.09091, 1.08221, 1.07757, 1.07385, 1.06817, 1.0623, 1.05207, 1.03581, 1.01343, 0.982392, 0.940151, 0.892928, 0.837689, 0.773924, 0.707478, 0.639465, 0.570935, 0.504203, 0.442841, 0.385688, 0.333489, 0.288532, 0.249292, 0.215335, 0.187414, 0.162552, 0.142601, 0.1254, 0.110664, 0.0981898, 0.0867282, 0.0774977, 0.0687965, 0.060932, 0.05364, 0.0470512, 0.0413551, 0.0361235, 0.0315523, 0.027532, 0.0240214, 0.0210999, 0.0181469, 0.0153926, 0.013164, 0.0108045, 0.00947701, 0.0078069, 0.00700868, 0.00572437, 0.00443263, 0.0044066, 0.00291622, 0.0024858, 0.00209414, 0.00224626, 0.000990174, 0.000590135, 0.000335204, 0.000293124, 0.0004019, 0.00013152, 0.000127091, 9.06419e-05, 1.41345e-05, 1.95143e-05, 8.83322e-06, 1.96614e-06, 1.72141e-06});
      w_["mfv_signals"] = std::vector<double>({0.172534, 3.13262, 2.68262, 2.33918, 1.49582, 1.75664, 1.45234, 1.27364, 0.585358, 1.49517, 1.45961, 1.44424, 1.30702, 1.18514, 1.07074, 1.03629, 1.09412, 1.10414, 1.16949, 1.20394, 1.21806, 1.23341, 1.25095, 1.27037, 1.29025, 1.25948, 1.27016, 1.25865, 1.27388, 1.24479, 1.23516, 1.16681, 1.09766, 1.04073, 0.973876, 0.917616, 0.869108, 0.840266, 0.782769, 0.745708, 0.755959, 0.788542, 0.849645, 0.941173, 1.08525, 1.24145, 1.44664, 1.4887, 1.51809, 1.48096, 1.33463, 1.17911, 0.96439, 0.752935, 0.578032, 0.4134, 0.289109, 0.200918, 0.137729, 0.0965137, 0.0699985, 0.0523641, 0.0376583, 0.0297392, 0.0241064, 0.0175732, 0.0125353, 0.0112112, 0.00906686, 0.00889159, 0.0083708, 0.00838739, 0.00782759, 0.00836096, 0.00607675, 0.00541676, 0.005148, 0.00664222, 0.00790963, 0.010092, 0.00668878, 0.00330788, 0.00693948, 0.00565068, 0, 0, 0.000997499, 0.00378327});

      w_["2017B"] = std::vector<double>({1.61353e-06, 0.000769866, 0.930231, 1.03107, 1.21038, 1.40051, 1.48383, 1.80102, 0.922482, 1.71824, 2.05294, 2.14752, 1.97101, 1.71201, 1.48589, 1.32433, 1.26675, 1.31208, 1.42441, 1.54234, 1.64321, 1.7186, 1.76387, 1.78005, 1.78809, 1.80725, 1.83937, 1.86422, 1.89897, 1.8685, 1.80759, 1.68982, 1.54775, 1.37476, 1.19695, 1.02702, 0.86664, 0.718257, 0.564594, 0.431458, 0.334365, 0.253934, 0.188225, 0.135228, 0.0941599, 0.0632052, 0.0406745, 0.0241699, 0.0139582, 0.00765884, 0.00410829, 0.00215115, 0.00111213, 0.000572224, 0.000295689, 0.000150375, 7.72943e-05, 3.96646e-05, 2.09785e-05, 1.13665e-05, 6.33296e-06, 3.5919e-06, 2.07634e-06, 1.2233e-06, 7.25628e-07, 3.70448e-07, 1.89412e-07, 1.10431e-07, 6.43637e-08, 3.69301e-08, 2.09881e-08, 1.18652e-08, 6.49745e-09, 3.51481e-09, 1.4916e-09, 6.44649e-10, 3.29517e-10, 1.58392e-10, 7.95016e-11, 3.67237e-11, 1.73162e-11, 7.60424e-12, 3.28965e-12, 1.06372e-12, 3.87322e-13, 1.61439e-13, 6.36211e-14, 2.47097e-14});
      w_["2017C"] = std::vector<double>({0.151588, 1.98709, 0.72531, 1.55845, 1.78199, 1.17016, 1.1638, 1.36538, 0.623399, 0.881218, 0.813739, 1.02878, 1.41585, 1.81856, 2.10372, 2.20994, 2.18912, 2.11072, 2.0205, 1.92204, 1.84265, 1.7868, 1.74435, 1.7052, 1.67595, 1.66372, 1.66629, 1.66728, 1.685, 1.65368, 1.60254, 1.50538, 1.38899, 1.24647, 1.10047, 0.961545, 0.829886, 0.70653, 0.573046, 0.454111, 0.36718, 0.293212, 0.230755, 0.178108, 0.135092, 0.100314, 0.0725909, 0.0493016, 0.0330336, 0.0212923, 0.0135332, 0.00842972, 0.00517883, 0.00314796, 0.00190318, 0.00111885, 0.000656461, 0.000380114, 0.00022478, 0.00013536, 8.36125e-05, 5.26237e-05, 3.389e-05, 2.23917e-05, 1.50265e-05, 8.77077e-06, 5.18881e-06, 3.54613e-06, 2.45646e-06, 1.69942e-06, 1.18178e-06, 8.2973e-07, 5.72725e-07, 3.96286e-07, 2.18221e-07, 1.24096e-07, 8.45978e-08, 5.49412e-08, 3.77258e-08, 2.41267e-08, 1.59332e-08, 9.90637e-09, 6.13586e-09, 2.87145e-09, 1.52516e-09, 9.22723e-10, 5.31343e-10, 3.20641e-10, 1.58753e-10, 9.70531e-11, 3.98916e-11, 2.02805e-11, 6.94009e-12, 3.172e-12, 3.68221e-12, 1.2234e-12});
      w_["2017D"] = std::vector<double>({3.02569e-10, 0.000886267, 0.419327, 1.40478, 2.42475, 2.23266, 1.79821, 1.62234, 0.541593, 0.527066, 0.312378, 0.200611, 0.169879, 0.186718, 0.291196, 0.588878, 1.11329, 1.60826, 1.86223, 1.96124, 2.00487, 1.98492, 1.95414, 1.98884, 2.09014, 2.19971, 2.26605, 2.26293, 2.22735, 2.07913, 1.87307, 1.60793, 1.34302, 1.08631, 0.863067, 0.67936, 0.530577, 0.411623, 0.306338, 0.223571, 0.166262, 0.121289, 0.0862165, 0.0592343, 0.0393289, 0.0251092, 0.0153294, 0.00861014, 0.00467052, 0.002382, 0.0011688, 0.000547481, 0.000246042, 0.000106304, 4.43498e-05, 1.7455e-05, 6.64771e-06, 2.42123e-06, 8.72251e-07, 3.09739e-07, 1.09146e-07, 3.7888e-08, 1.30036e-08, 4.42164e-09, 1.47377e-09, 4.12113e-10, 1.12605e-10, 3.42505e-11, 1.01718e-11, 2.90531e-12, 8.03155e-13, 2.15818e-13, 5.49324e-14, 1.34662e-14, 2.52627e-15, 4.54011e-16, 2.1282e-17});
      w_["2017E"] = std::vector<double>({5.74635e-06, 0.374683, 1.09213, 0.760874, 0.979535, 1.17353, 1.00205, 1.11486, 0.420548, 0.434077, 0.26539, 0.264014, 0.334949, 0.4043, 0.458524, 0.509743, 0.576712, 0.668112, 0.778863, 0.882359, 0.961481, 1.01199, 1.03742, 1.03724, 1.018, 0.992797, 0.973888, 0.965091, 0.987759, 1.0094, 1.04626, 1.07375, 1.09835, 1.10483, 1.10661, 1.11517, 1.13412, 1.16618, 1.17209, 1.18004, 1.24109, 1.31792, 1.40796, 1.50315, 1.60248, 1.69298, 1.7557, 1.71201, 1.64141, 1.50199, 1.33993, 1.15599, 0.969787, 0.793697, 0.637592, 0.492238, 0.375549, 0.280583, 0.212913, 0.163999, 0.129462, 0.104278, 0.0862654, 0.0736547, 0.0643946, 0.0494653, 0.038971, 0.0359391, 0.0340709, 0.0327307, 0.0320713, 0.0321858, 0.0321995, 0.0327258, 0.0268132, 0.022972, 0.0238823, 0.0239382, 0.0256712, 0.0259428, 0.0273898, 0.0275409, 0.0279048, 0.0216043, 0.0191964, 0.0196423, 0.0193367, 0.0201608, 0.017426, 0.0187905, 0.0137581, 0.0126009, 0.0078217, 0.00659386, 0.0140797, 0.00885909});
      w_["2017F"] = std::vector<double>({0.458771, 10.2242, 8.8188, 5.40502, 1.9673, 1.79277, 1.33736, 0.970245, 0.658312, 2.76422, 3.00038, 2.81257, 2.09542, 1.33457, 0.877572, 0.654287, 0.566326, 0.529701, 0.514816, 0.510507, 0.535172, 0.59914, 0.673867, 0.716066, 0.718442, 0.702735, 0.684163, 0.665212, 0.661736, 0.655311, 0.662319, 0.672243, 0.691209, 0.70878, 0.732347, 0.768225, 0.815751, 0.872431, 0.906668, 0.944384, 1.04123, 1.18911, 1.40923, 1.71435, 2.11474, 2.58865, 3.07579, 3.36713, 3.53171, 3.43605, 3.16495, 2.73982, 2.24456, 1.74924, 1.30794, 0.921187, 0.630124, 0.415903, 0.275338, 0.183036, 0.123483, 0.0841899, 0.058362, 0.0412938, 0.0295461, 0.0183194, 0.0114781, 0.00829172, 0.00606944, 0.00444651, 0.0032932, 0.00248872, 0.00188032, 0.00145862, 0.000929013, 0.000634156, 0.000540279, 0.000456396, 0.000422767, 0.000376202, 0.000354398, 0.000320451, 0.000292971, 0.000204712, 0.000163841, 0.000150502, 0.000132457, 0.0001229, 9.40867e-05, 8.94288e-05, 5.74462e-05, 4.5948e-05, 2.47965e-05, 1.80954e-05, 3.33073e-05, 1.7992e-05});

      // https://hypernews.cern.ch/HyperNews/CMS/get/physics-validation/3007.html
      // Bug in npu distribution for official MC samples, one is
      // advised to check per-sample. Few % difference especially wrt
      // peak at 0 and extra at 75-100, so should apply per-sample
      // weights. This is fixed for some samples with PU2017 in
      // dataset name, list of liars is in Samples.py. Each unfixed
      // sample should have a separate entry here.
      w_["dyjetstollM10_2017"] = std::vector<double>({0.000229715, 0.0300705, 0.0319789, 0.0513375, 0.0645684, 0.0908925, 0.111439, 0.152398, 0.113217, 0.293476, 0.422177, 0.582436, 0.640371, 0.690106, 0.727615, 0.794766, 0.89434, 1.02119, 1.09519, 1.15135, 1.21878, 1.26489, 1.30698, 1.34089, 1.35737, 1.36461, 1.37045, 1.37881, 1.38058, 1.36934, 1.33137, 1.27088, 1.20882, 1.14316, 1.06399, 1.00359, 0.9567, 0.913202, 0.865897, 0.824827, 0.829919, 0.870158, 0.949461, 1.05575, 1.18556, 1.36366, 1.54705, 1.58819, 1.63285, 1.58153, 1.41758, 1.22361, 1.01485, 0.789125, 0.602011, 0.429304, 0.309488, 0.211026, 0.146795, 0.102502, 0.0742253, 0.0544275, 0.0400743, 0.0313479, 0.0239129, 0.01804, 0.0123402, 0.0108551, 0.00965488, 0.00880901, 0.0073491, 0.00610756, 0.00605802, 0.00574327, 0.00327484, 0.00321835, 0.00227254, 0.00145935, 0.00157055, 0.000437929, 0.000252333, 0.00028131, 0.000244326, 7.39277e-05, 0.00031638, 7.16363e-05, 6.65681e-05, 1.94714e-05, 2.32228e-05, 1.26017e-05, 5.71133e-05, 1.03919e-05, 8.81662e-06, 2.44195e-06, 2.40042e-06, 5.7742e-07, 1.75046e-05, 4.00919e-06, 2.20699e-05, 3.29462e-07, 5.72512e-05, 0, 2.30248e-05, 0, 1.99777e-05, 0, 0, 2.86971e-06, 0, 7.46115e-07, 0, 0, 0, 0, 0, 0, 0, 0, 1.0162e-09, 0, 2.07865e-10, 0, 2.0365e-11, 8.83521e-12, 7.60851e-12});
      w_["dyjetstollM50_2017"] = std::vector<double>({0.000343766, 0.0454942, 0.0638485, 0.0724603, 0.0808402, 0.11692, 0.120572, 0.159041, 0.116146, 0.37076, 0.494838, 0.657513, 0.700729, 0.708831, 0.744099, 0.804827, 0.910911, 1.00248, 1.08458, 1.13475, 1.19334, 1.24291, 1.29376, 1.32784, 1.33288, 1.34342, 1.3393, 1.34805, 1.3628, 1.34461, 1.30984, 1.25493, 1.18706, 1.12607, 1.04982, 0.990498, 0.944446, 0.897164, 0.852112, 0.816464, 0.816095, 0.854148, 0.92026, 1.03886, 1.19119, 1.35243, 1.51488, 1.59998, 1.61957, 1.54753, 1.39156, 1.20325, 0.994411, 0.788659, 0.596926, 0.421187, 0.301209, 0.209862, 0.145994, 0.102151, 0.0732009, 0.0534267, 0.0402743, 0.0302724, 0.0243304, 0.0174366, 0.0126443, 0.0107361, 0.00966023, 0.00909761, 0.00781418, 0.00715103, 0.00514489, 0.00508311, 0.00287266, 0.0036989, 0.00243739, 0.0018937, 0.000968539, 0.000656432, 0.000186763, 0.000336561, 0.000303331, 0.000105614, 7.70877e-05, 4.73415e-05, 8.20535e-05, 1.33613e-05, 1.17325e-05, 7.87561e-06, 2.4555e-05, 1.0153e-05, 1.24211e-05, 1.34593e-05, 1.33355e-06, 8.47843e-07, 1.60305e-06, 7.96342e-07, 1.06406e-06, 2.8214e-07, 9.40161e-05, 0, 4.25369e-05, 0, 2.4605e-05, 1.3024e-05, 0, 3.53441e-06, 0, 9.18935e-07, 4.61057e-07, 2.28839e-07, 0, 0, 0, 0, 5.85534e-09, 0, 0, 5.69144e-10, 0, 0, 0, 7.25444e-12, 0, 0, 0, 0, 0, 7.89499e-14});
      w_["dyjetstollM50ext_2017"] = std::vector<double>({0.000284296, 0.0441341, 0.048311, 0.0643351, 0.0658194, 0.114021, 0.133082, 0.175306, 0.115663, 0.369264, 0.490677, 0.634555, 0.695788, 0.717745, 0.737257, 0.818224, 0.890208, 1.00881, 1.08936, 1.14807, 1.21153, 1.25518, 1.29829, 1.33017, 1.33314, 1.35532, 1.35278, 1.3581, 1.36822, 1.35198, 1.32441, 1.26484, 1.19439, 1.12787, 1.05852, 0.993088, 0.947668, 0.914562, 0.861042, 0.818735, 0.816466, 0.858118, 0.933036, 1.04665, 1.19173, 1.35124, 1.53126, 1.5808, 1.63146, 1.56586, 1.36686, 1.22517, 1.00695, 0.777073, 0.597204, 0.430277, 0.301055, 0.210501, 0.145842, 0.10178, 0.0713765, 0.0530337, 0.0405464, 0.0307925, 0.0238372, 0.017541, 0.012578, 0.0103144, 0.0100839, 0.00841939, 0.00778395, 0.00525509, 0.00630739, 0.00574322, 0.00276802, 0.00253772, 0.00181574, 0.00153395, 0.000686367, 0.000380877, 0.000309436, 0.000246003, 0.000278578, 8.14963e-05, 0.000106196, 6.26607e-05, 6.54404e-05, 3.04216e-05, 1.34751e-05, 1.00754e-05, 2.08366e-05, 4.27263e-05, 6.05518e-05, 4.57646e-06, 8.65481e-06, 4.64904e-07, 1.64386e-06, 2.78901e-05, 3.0782e-07, 3.29845e-07, 4.68957e-07, 0, 4.29303e-05, 0, 2.48326e-05, 0, 0, 0, 0, 0, 0, 2.30956e-07, 1.13396e-07, 0, 2.64583e-08, 0, 0, 0, 0, 0, 2.5838e-10, 0, 5.06281e-11, 2.19646e-11, 0, 3.98899e-12, 0, 7.05927e-13});
      w_["qcdht0700_2017"] = std::vector<double>({0.000296976, 0.0467324, 0.0515802, 0.0786023, 0.0767765, 0.116231, 0.138737, 0.160398, 0.130265, 0.410072, 0.512657, 0.678021, 0.713518, 0.708992, 0.759389, 0.824747, 0.905276, 0.998377, 1.08614, 1.14625, 1.19965, 1.24653, 1.29428, 1.32301, 1.33964, 1.33752, 1.35273, 1.35557, 1.35342, 1.34281, 1.31616, 1.25714, 1.19093, 1.12915, 1.04937, 0.9833, 0.943394, 0.9101, 0.854044, 0.817876, 0.819624, 0.8649, 0.929556, 1.04286, 1.18773, 1.35497, 1.53263, 1.60641, 1.65089, 1.56006, 1.39906, 1.20585, 1.01227, 0.785997, 0.592608, 0.427797, 0.301509, 0.208699, 0.144675, 0.101881, 0.0739957, 0.0529192, 0.0404076, 0.0295275, 0.0235286, 0.0173968, 0.0130823, 0.0109204, 0.00925239, 0.00839855, 0.00722617, 0.00497941, 0.00522982, 0.00483333, 0.00260868, 0.00363783, 0.00249555, 0.00237076, 0.000663494, 0.000644129, 0.000206572, 0.000206542, 0.000152026, 0.000100963, 0.000106128, 0.000102858, 2.58322e-05, 1.73662e-05, 1.88672e-05, 7.53359e-06, 2.95241e-05, 6.11551e-05, 6.30032e-05, 2.52389e-05, 4.77254e-06, 1.45403e-06, 1.8017e-05, 2.80801e-06, 1.98979e-06, 2.42407e-07, 0, 0, 8.34125e-05, 0, 0, 0, 0, 3.46539e-06, 0, 0, 4.52054e-07, 0, 1.10162e-07, 0, 1.28519e-08, 0, 5.741e-09, 0, 0, 2.79015e-10, 0, 1.11582e-10, 4.91845e-11, 2.13383e-11, 0, 3.87525e-12, 0, 6.85799e-13, 1.29359e-13, 7.74082e-14});

      // cross_* keys can be used for reweighting already produced
      // weights or for zipping with above sets at initial weight
      // time, e.g. run 2017 MC samples but weight toward 2018 PU
      // distribution.
      w_["cross_2017to2018"] = std::vector<double>({0.7797702792139376, 0.6532833569108556, 1.0743562101707458, 1.2497001442762443, 2.050573240365452, 2.195715150467067, 2.948674058448776, 4.050136845705993, 4.228824305563249, 2.483542373408909, 1.7275296644894649, 1.2783549286418805, 1.1170937089500774, 1.0654531852347395, 1.009966386251899, 0.9407319151227456, 0.8659483561845328, 0.8157308961210773, 0.8004512381722789, 0.8062985938953166, 0.8220469674384511, 0.8432201845053094, 0.8647575031243864, 0.8816837717725626, 0.8907101948594957, 0.8921509446490142, 0.8926763346640493, 0.9002790072228023, 0.9199214447806917, 0.9538191105153281, 1.001993314603332, 1.0634929977660772, 1.1384251361768587, 1.2278708503409848, 1.331090453106927, 1.4434402438893936, 1.557030670968403, 1.6623806542404302, 1.7479219522959395, 1.7977040443841021, 1.7919913525555198, 1.7144630987937093, 1.5634350838426936, 1.3576785912585037, 1.1298443348497929, 0.9119752257758621, 0.7246264454913182, 0.5750556617110043, 0.4614293628662269, 0.37796989835064265, 0.31827823562126323, 0.27663918388281883, 0.24875501280633144, 0.23155241873552543, 0.22290710205798295, 0.22142503682807355, 0.22623734289954245, 0.2368211761478704, 0.25285432350682585, 0.2740842314020289, 0.30019890929035775, 0.330691474344418, 0.36471346866837057, 0.40093086447266746, 0.43742215804434315, 0.471684677429645, 0.5008218511009552, 0.521943774424575, 0.5327172103193301, 0.5318900136342424, 0.519574464511983, 0.497163251868251, 0.46692640088100357, 0.43147416023304036, 0.39328491307046193, 0.3544110971373518, 0.3163721660381078, 0.28018114725610477, 0.24643837403056862, 0.21544159489059078, 0.18728409407982882, 0.16193020064121524, 0.13926796453948637, 0.11914330703179914, 0.101380948634925, 0.08579674342259706, 0.07220484298263677, 0.06042194911611612, 0.050270008290214364, 0.0415780840363558, 0.034183765999931316, 0.027934266910575843, 0.02268725831501726, 0.01831145572579861, 0.014686955843226192, 0.011705332581890146, 0.009269506836141644, 0.007293415982895853, 0.005701510041868437, 0.004428114227537249, 0.0034166896397035524, 0.002619023512292484, 0.0019944018517865933, 0.001508749003577175, 0.001133834910582227, 0.0008464656929325453, 0.0006277407346863325, 0.00046244885883637486, 0.0003384476819456606, 0.00024604244297492646, 0.00017775159809773751, 0.0001274389523568934, 9.06371967768704e-05, 6.406993884495793e-05, 4.461456436310904e-05, 3.24153941419403e-05, 2.0587758227728614e-05, 1.267222669159895e-05});
      w_["cross_2017to2017p8"] = std::vector<double>({0.8698982955631639, 0.7951755736623053, 1.0439262677360213, 1.1475114905132253, 1.6206308972259567, 1.7063741376116712, 2.151188020813575, 2.8018821482202965, 2.907442573970012, 1.8764093724310078, 1.4297914425019316, 1.1644394340847508, 1.0691736385936523, 1.0386667654550223, 1.0058876877917293, 0.9649871105783748, 0.9208083846235542, 0.8911421927788529, 0.8821156656813517, 0.8855700175431275, 0.894873440499651, 0.9073816143236796, 0.920104882787808, 0.9301041526094447, 0.9354365529066724, 0.9362876823664672, 0.9365980588960571, 0.9410893721240741, 0.9526932310240182, 0.972718430496484, 1.0011775596247716, 1.037508775835009, 1.081775275785803, 1.1346157363094191, 1.195593183872855, 1.261964331335373, 1.3290683903058849, 1.3913043697965803, 1.4418382788304676, 1.4712472750730463, 1.4678724765164841, 1.4220723096706045, 1.3328518262013145, 1.2113002468386322, 1.0767061285603492, 0.9479989661778988, 0.8373218261797986, 0.7489622086208413, 0.6818369582423264, 0.6325329017956889, 0.597269781840571, 0.5726713235445278, 0.556198623261792, 0.5460361129459341, 0.5409288529851538, 0.5400533162419314, 0.5428962078368313, 0.5491486552366097, 0.5586203096138742, 0.5711619738013619, 0.5865893379734805, 0.6046029588055122, 0.624701605954897, 0.6460971964664061, 0.6676545933238082, 0.6878953317419356, 0.7051082489793509, 0.7175861207923773, 0.7239505768137798, 0.7234619066277109, 0.7161864402366963, 0.7029469149217714, 0.6850843583322136, 0.6641407866928275, 0.6415803160657153, 0.6186154333386716, 0.5961437626063887, 0.5747637544401968, 0.5548300584186119, 0.5365185708329703, 0.5198843997724691, 0.5049064724577546, 0.4915186538987458, 0.4796299213806624, 0.4691367277553743, 0.4599302879833924, 0.4519008112739684, 0.44494001338637607, 0.4389427083901318, 0.43380791479267095, 0.4294396879418482, 0.4257477680660951, 0.4226480739873834, 0.42006304880048095, 0.4179218590883446, 0.4161604516502215, 0.4147214765650155, 0.4135540919485719, 0.4126136663080564, 0.411861401966641, 0.4112638983131068, 0.4107926734376572, 0.41042367536432756, 0.41013677374591234, 0.4099152915484054, 0.4097455268822856, 0.40961631412313065, 0.409518667199269, 0.4094454129427224, 0.4093908241295229, 0.40935048100378923, 0.40932075858057476, 0.40929901777688055, 0.4092833230489991, 0.4092718296984581, 0.40926462298342964, 0.4092576357539749, 0.40925295961788977, 0.40924547344261014, 0.40924547344261014, 0.40924547344261014, 0.4092454734426102, 0.4092454734426102, 0.4092454734426102, 0.40924547344261014, 0.4092454734426102, 0.40924547344261025, 0.40924547344261014, 0.4092454734426102, 0.4092454734426102, 0.40924547344261014});
      w_["cross_2017to2017B"] = std::vector<double>({8.734106e-06, 0.00019848967, 0.27051586, 0.40321691, 0.72817076, 0.92797556, 1.1538785, 1.4328722, 1.4989203, 1.1807424, 1.3728367, 1.4478867, 1.4802262, 1.4704326, 1.3781337, 1.2572793, 1.1709109, 1.1630884, 1.2215057, 1.2973705, 1.3554483, 1.3879938, 1.3993526, 1.4010185, 1.4062729, 1.4215428, 1.4459092, 1.4716558, 1.489178, 1.4924241, 1.4785166, 1.4458848, 1.3944699, 1.3246741, 1.2356672, 1.1265433, 0.99943376, 0.86029724, 0.71656623, 0.57483586, 0.44075891, 0.32021134, 0.21903871, 0.14099953, 0.085979783, 0.050288579, 0.028649663, 0.016146529, 0.0091267049, 0.0052341653, 0.0030746761, 0.0018627417, 0.0011698197, 0.00076383509, 0.00051881908, 0.00036585188, 0.0002666792, 0.0001996949, 0.00015248219, 0.00011779587, 9.1361633e-05, 7.0636612e-05, 5.4092484e-05, 4.0791896e-05, 3.0134178e-05, 2.1702335e-05, 1.5171895e-05, 1.0258242e-05, 6.689751e-06, 4.200741e-06, 2.5387009e-06, 1.4775022e-06, 8.2926092e-07, 4.4970918e-07, 2.3612923e-07, 1.2028874e-07, 5.9557651e-08, 2.8705071e-08, 1.348479e-08, 6.1810051e-09, 2.7666832e-09, 1.2105482e-09, 5.1770536e-10, 2.1653862e-10, 8.8856109e-11, 3.6240639e-11, 1.4524603e-11, 5.4164895e-12});
      w_["cross_2017to2017C"] = std::vector<double>({0.82055224, 0.51231881, 0.2109238, 0.60945755, 1.0720542, 0.77534604, 0.90501186, 1.0862817, 1.012947, 0.60555655, 0.54416143, 0.69361722, 1.0633017, 1.5619476, 1.9511589, 2.0980509, 2.0234968, 1.8710398, 1.7326839, 1.6167628, 1.5199621, 1.4430742, 1.3838666, 1.3421065, 1.3180785, 1.3086453, 1.3098528, 1.3161871, 1.3213821, 1.3208412, 1.3107961, 1.2880698, 1.2514325, 1.201058, 1.1360664, 1.0547235, 0.95704801, 0.84625114, 0.72729326, 0.60501668, 0.48401554, 0.36974099, 0.26853116, 0.18570965, 0.12335592, 0.07981382, 0.051130434, 0.032935581, 0.021599341, 0.014551475, 0.010128352, 0.0072995333, 0.0054474721, 0.0042020648, 0.00333934, 0.002722084, 0.0022649082, 0.0019137172, 0.0016338131, 0.0014027932, 0.001206225, 0.0010348729, 0.00088289696, 0.00074666876, 0.00062402668, 0.000513827, 0.0004156235, 0.00032940985, 0.00025531636, 0.00019330636, 0.000142947, 0.0001033213, 7.3096131e-05, 5.070358e-05, 3.4545693e-05, 2.3155781e-05, 1.5290399e-05, 9.9568858e-06, 6.3989212e-06, 4.0607906e-06, 2.5457154e-06, 1.5770331e-06, 9.656248e-07, 5.8453336e-07, 3.4988919e-07, 2.071375e-07, 1.2130482e-07, 7.0286106e-08, 4.0301129e-08, 2.2869979e-08, 1.2849398e-08, 7.1379297e-09, 3.9378185e-09, 2.1362571e-09, 1.1620167e-09, 6.1388851e-10});
      w_["cross_2017to2017D"] = std::vector<double>({1.6378188e-09, 0.0002285006, 0.1219424, 0.54936237, 1.4587419, 1.4793567, 1.3983514, 1.2907163, 0.88002229, 0.36218991, 0.2088926, 0.13525462, 0.12757893, 0.1603707, 0.27007856, 0.55906316, 1.0290613, 1.425636, 1.5969591, 1.6497367, 1.6537738, 1.6030819, 1.5503019, 1.5653502, 1.6438251, 1.7302431, 1.7813178, 1.7864062, 1.7466946, 1.6606602, 1.5320759, 1.3758161, 1.2100151, 1.046733, 0.89098421, 0.74519336, 0.61187641, 0.49302426, 0.38879525, 0.29786591, 0.21916606, 0.1529457, 0.10033073, 0.061762421, 0.035912212, 0.019977881, 0.010797481, 0.0057519423, 0.003053865, 0.0016278943, 0.00087473899, 0.0004740793, 0.00025880497, 0.00014190024, 7.7816633e-05, 4.2466797e-05, 2.2935792e-05, 1.2189895e-05, 6.3399549e-06, 3.2099568e-06, 1.5745807e-06, 7.4508755e-07, 3.3876775e-07, 1.4744305e-07, 6.1203327e-08, 2.4143238e-08, 9.0196565e-09, 3.181624e-09, 1.0572234e-09, 3.3047446e-10, 9.7148874e-11, 2.6874522e-11, 7.0109493e-12, 1.7229591e-12, 3.999237e-13, 8.4716505e-14, 3.846557e-15});
      w_["cross_2017to2017E"] = std::vector<double>({3.1105235e-05, 0.096602142, 0.3175969, 0.29755231, 0.58929323, 0.777579, 0.77922936, 0.88697063, 0.68333899, 0.29828961, 0.17747091, 0.17800177, 0.25154631, 0.34725026, 0.42527198, 0.48393476, 0.53307945, 0.59224537, 0.66791555, 0.74221413, 0.79310484, 0.81731398, 0.82302914, 0.81637729, 0.80062288, 0.78091212, 0.765563, 0.76186382, 0.77460359, 0.80623647, 0.8557874, 0.91874802, 0.98957583, 1.0645783, 1.142405, 1.2232355, 1.3078993, 1.3968001, 1.4875824, 1.5721792, 1.636001, 1.6619001, 1.6384526, 1.5673045, 1.463265, 1.3470024, 1.2366523, 1.143696, 1.0732519, 1.0264823, 1.002814, 1.0010045, 1.0200929, 1.059469, 1.1187257, 1.1975807, 1.2957114, 1.4126197, 1.5475578, 1.6995913, 1.8676669, 2.050682, 2.2473727, 2.4560736, 2.6742055, 2.8978763, 3.1215757, 3.3384827, 3.5412171, 3.7230658, 3.8793143, 4.0079048, 4.1095794, 4.1871659, 4.2446904, 4.2864767, 4.3165412, 4.338273, 4.3542612, 4.3664603, 4.3761853, 4.3843417, 4.3914898, 4.3979293, 4.4038743, 4.4094023, 4.4145399, 4.4193479, 4.4237746, 4.4278682, 4.4315923, 4.4350158, 4.4380454, 4.4407882, 4.4432137, 4.4453928});
      w_["cross_2017to2017F"] = std::vector<double>({2.4833468, 2.6360407, 2.5645514, 2.1137221, 1.1835377, 1.1878864, 1.0399782, 0.77191649, 1.0696764, 1.8995203, 2.0064063, 1.8962723, 1.573658, 1.1462522, 0.81393075, 0.62116051, 0.52347923, 0.46955146, 0.44148151, 0.42942329, 0.44145179, 0.48388373, 0.53460718, 0.56359186, 0.56503055, 0.55275578, 0.53781326, 0.52513282, 0.51893537, 0.52341552, 0.54174321, 0.57520086, 0.62275569, 0.68295738, 0.75603587, 0.84266982, 0.94074713, 1.0449602, 1.1507166, 1.2582124, 1.3725462, 1.4994704, 1.6399305, 1.7875185, 1.9310225, 2.0596332, 2.1664765, 2.2493871, 2.309243, 2.3482477, 2.3686731, 2.3724877, 2.3609923, 2.3349788, 2.2949255, 2.2411837, 2.1740409, 2.0939001, 2.0012938, 1.8968798, 1.7814116, 1.6556389, 1.5204377, 1.3769741, 1.2270026, 1.0732242, 0.91939541, 0.77024087, 0.63083761, 0.50578354, 0.39834238, 0.30990539, 0.23998274, 0.18662596, 0.14706833, 0.11833079, 0.097651254, 0.082711751, 0.071708293, 0.06331896, 0.056623682, 0.051013826, 0.046106017, 0.041672672, 0.037587004, 0.033785446, 0.030239736, 0.026940293, 0.023884905, 0.021073358, 0.018503873, 0.016171869, 0.014069575, 0.012186768, 0.01051098, 0.0090281855});
    }
  };
}

#endif
