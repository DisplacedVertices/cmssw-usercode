#ifndef DVCode_MFVNeutralino_VertexMVAWrap_h
#define DVCode_MFVNeutralino_VertexMVAWrap_h

#include "DVCode/MFVNeutralino/plugins/VertexMVA.h"
#include "DVCode/MFVNeutralinoFormats/interface/VertexAux.h"

class MFVVertexMVAWrap {
private:
  const ReadMLP* mva;

public:
  MFVVertexMVAWrap() : mva(new ReadMLP) {}

  double value(const MFVVertexAux& vtx) const {
    std::vector<double> input = {
      double(vtx.ntracks()),
      double(vtx.ntracksptgt(3)),
      TMath::Prob(vtx.chi2,vtx.ndof()),
      vtx.eta[0],
      vtx.costhmompv3d(2),
      vtx.trackdxyerrmin(),
      vtx.trackdzerrmin(),
      vtx.trackquadmassmin(),
      vtx.costhtkmomvtxdispavg(),
      vtx.mass[2],
      vtx.maxtrackpt(),
      vtx.drmin(),
      vtx.drmax(),
      double(vtx.njets[0]),
      vtx.bs2dsig()
    };

    return mva->GetMvaValue(input);
  }
};

#endif
