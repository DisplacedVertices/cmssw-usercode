// Modified version of SigCalc from Glen Cowan, RHUL Physics

#ifndef SigCalc_SigCalc_h
#define SigCalc_SigCalc_h

#include <vector>

class SigCalc {
public: 
  SigCalc(double n, double s, std::vector<double> mVec, std::vector<double> tauVec);

  double n() { return m_n; }
  double s() { return m_s; }
  double m(int i) { return m_m[i]; }
  double tau(int i) { return m_tau[i]; }
  int numBck(){ return m_numBck; }
  double systFrac() { return m_systFrac; }
  void setSystFrac(double x) { m_systFrac = x; }

  double lnL(double mu, std::vector<double> bVec);
  double qmu(double mu, double& muHat, std::vector<double>& bHat, std::vector<double>& bHatHat);
  double qmu(double mu);

private:
  int m_numBck;
  double m_n;
  double m_s;
  std::vector<double> m_m;
  std::vector<double> m_tau;
  double m_systFrac;
};

double getSignificance(double mu, double n, double s, std::vector<double> m, std::vector<double> tau, double systFrac);

#endif
