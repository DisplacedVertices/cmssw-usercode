#include "DVCode/MFVNeutralino/interface/EventTools.h"

namespace mfv {

  // See https://hypernews.cern.ch/HyperNews/CMS/get/generators/5090/1/1/1.html and 
  // https://gitlab.cern.ch/cms-desy-top/TopAnalysis/-/blob/Htottbar_2016/ZTopUtils/plugins/EventWeightMCSystematicRecalc.cc
  
  LHAPDF::PDF* setupLHAPDF() {
    // LHAPDF too verbose otherwise!
    LHAPDF::Info& cfg = LHAPDF::getConfig();
    cfg.set_entry("Verbosity", 0);

    // in MakeSamples/gensim.py:
    // 'PDF:pSet = LHAPDF6:NNPDF31_lo_as_0130',
    //
    // which https://lhapdf.hepforge.org/pdfsets tells us is 315200
    int lhapdfnumber = 315200;
    return LHAPDF::mkPDF(lhapdfnumber);
  }

  double alphas(double q2) {
    double mZ = 91.1876; //Z boson mass
    double alphas_mZ = 0.1184; //alpha_s evaluated at Z boson mass
    int nf = 4; //effective number of flavors
    double pi = 3.14159265359;
    double b0 = (33 - 2.*nf) / (12*pi);

    return alphas_mZ / (1 + alphas_mZ * b0 * std::log(q2 / std::pow(mZ,2)));    
  }

  double renormalization_weight(double q, int up_or_dn) {
    double q2 = q*q;
    double k2 = 1;

    if      ( up_or_dn ==  1 ) k2 = 4; // 2*q ==> 4*q2
    else if ( up_or_dn == -1 ) k2 = 0.25; // 0.5*q ==> 0.25*q2
    else {
      throw std::invalid_argument("up_or_dn must be -1 or 1");
    }
    
    double alphas_old = alphas(q2);
    double alphas_new = alphas(k2*q2);

    int nQCD = 2; //number of QCD vertices (i.e. gg/gq/qq -> gluino gluino or stop stop)

    return std::pow(alphas_new / alphas_old, nQCD);
  }

  double factorization_weight(LHAPDF::PDF* pdf, double id1, double id2, double x1, double x2, double q, int up_or_dn) {
    double q2 = q*q;
    double k2 = 1;

    if      ( up_or_dn ==  1 ) k2 = 4; // 2*q ==> 4*q2
    else if ( up_or_dn == -1 ) k2 = 0.25; // 0.5*q ==> 0.25*q2
    else {
      throw std::invalid_argument("up_or_dn must be -1 or 1");
    }

    double pdf1old = pdf->xfxQ2(id1,x1,q2);
    double pdf2old = pdf->xfxQ2(id2,x2,q2);
    double pdf1new = pdf->xfxQ2(id1,x1,k2*q2);
    double pdf2new = pdf->xfxQ2(id2,x2,k2*q2);

    return (pdf1new*pdf2new)/(pdf1old*pdf2old);
  }
}
