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
  bool useSystFrac() const { return m_useSystFrac; }
  int numa() const { return int(m_systFrac.size()); }
  double systFrac(const int j) const { return m_systFrac[j]; }
  int bitoaj(const int i) const { return m_bitoaj[i]; }

  void systFrac(const std::vector<double>& sf) { m_useSystFrac = true; m_systFrac = sf; }
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

  bool m_useSystFrac;
  std::vector<double> m_systFrac;
  std::vector<int> m_bitoaj;
};

double getSignificance(double mu, double n, double s, const std::vector<double>& m, const std::vector<double>& tau, double systFrac);

#endif
