#ifndef JMTucker_Tools_BTagging_h
#define JMTucker_Tools_BTagging_h

namespace pat { class Jet; }

namespace jmt {
  namespace BTagging {
    enum { loose, medium, tight, nwp };

    float discriminator_min(int wp, int tagger=2);
    bool is_tagged(double disc, int wp, int tagger=2);
    float discriminator(const pat::Jet& jet, int tagger=2);
    bool is_tagged(const pat::Jet& jet, int wp, int tagger=2);
  }
}

#endif
