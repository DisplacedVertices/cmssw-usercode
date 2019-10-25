#ifndef JMTucker_Tools_BTagging_h
#define JMTucker_Tools_BTagging_h

namespace pat { class Jet; }

namespace jmt {
  namespace BTagging {
    enum { loose, medium, tight, nwp };

    float discriminator_min(int wp, bool old=false);
    bool is_tagged(double disc, int wp, bool old=false);
    float discriminator(const pat::Jet& jet, bool old=false);
    bool is_tagged(const pat::Jet& jet, int wp, bool old=false);
  }
}

#endif
