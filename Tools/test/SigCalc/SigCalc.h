// Modified version of SigCalc from Glen Cowan, RHUL Physics

#ifndef SigCalc_SigCalc_h
#define SigCalc_SigCalc_h

#include <vector>

class SigCalc {
public: 
  SigCalc(double n, double s, const std::vector<double>& m, const std::vector<double>& tau);

  double n() const { return m_n; }
  double s() const { return m_s; }
  double m(int i) const { return m_m[i]; }
  double tau(int i) const { return m_tau[i]; }
  int numBck() const { return m_numBck; }
  double systFrac() const { return m_systFrac; }
  int numa() const { return m_numa; }
  int bitoaj(const int i) const { return m_bitoaj[i]; }

  void systFrac(const double x) { m_systFrac = x > 0 ? x : 0; }
  void numa(int na) { m_numa = na; }
  void bitoaj(const std::vector<int>& x) { m_bitoaj = x; }

  double lnL(double mu, const std::vector<double>& b, const std::vector<double>& a) const;
  double qmu(double mu, double& muHat, std::vector<double>& bHat, std::vector<double>& bHatHat) const;
  double qmu(double mu) const {
    double muHat;
    std::vector<double> bHat, bHatHat;
    return qmu(mu, muHat, bHat, bHatHat);
  }

  static int debugLevel;

private:
  int m_numBck;
  double m_n;
  double m_s;
  std::vector<double> m_m;
  std::vector<double> m_tau;
  double m_systFrac;
  int m_numa;
  std::vector<int> m_bitoaj;
};

double getSignificance(double mu, double n, double s, const std::vector<double>& m, const std::vector<double>& tau, double systFrac);

#endif
