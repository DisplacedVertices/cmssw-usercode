#ifndef JMTucker_MFVNeutralino_One2Two_Templater_h
#define JMTucker_MFVNeutralino_One2Two_Templater_h

#include "SimpleObjects.h"
#include "Templates.h"

class TFile;
class TRandom;

namespace mfv {
  struct Templater {
    const std::string name;
    const std::string uname;

    TFile* fout;
    TDirectory* dout;
    TDirectory* dtoy;
    TRandom* rand;
    const int seed;

    ////////////////////////////////////////////////////////////////////////////

    int toy;
    const VertexSimples* one_vertices;
    const VertexPairs* two_vertices;

    Templates templates;

    virtual std::vector<double> true_pars() const = 0;

    ////////////////////////////////////////////////////////////////////////////

    Templater(const std::string& name_, TFile* f, TRandom* r);
    ~Templater();

    virtual void clear_templates();
    virtual void process(int toy, const VertexSimples*, const VertexPairs*);
    virtual void process_imp() = 0;
  };
}

#endif
