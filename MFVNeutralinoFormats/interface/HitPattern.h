#ifndef DVCode_MFVNeutralinoFormats_interface_HitPattern_h
#define DVCode_MFVNeutralinoFormats_interface_HitPattern_h

#include <cassert>

namespace mfv {
  struct HitPattern {
    typedef unsigned short value_t;
    value_t value;
    int npxhits() const { return value & 0x7; }
    int nsthits() const { return (value >> 3) & 0x1f; }
    int npxlayers() const { return (value >> 8) & 0x7; }
    int nstlayers() const { return (value >> 11) & 0x1f; }
    int nhits() const { return npxhits() + nsthits(); }
    int nlayers() const { return npxlayers() + nstlayers(); }
    HitPattern(value_t v) : value(v) {}
    HitPattern(int npxh, int nsth, int npxl, int nstl) : value(_encode(npxh, nsth, npxl, nstl)) {}
    static value_t _encode(int npxh, int nsth, int npxl, int nstl) {
      assert(npxh >= 0 && nsth >= 0 && npxl >= 0 && nstl >= 0);
      if (npxh > 7) npxh = 7;
      if (nsth > 31) nsth = 31;
      if (npxl > 7) npxl = 7;
      if (nstl > 31) nstl = 31;
      return (nstl << 11) | (npxl << 8) | (nsth << 3) | npxh;
    }
  };
}

#endif
