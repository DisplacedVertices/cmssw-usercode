#ifndef JMTucker_MFVNeutralino_One2Two_SimpleObjects_h
#define JMTucker_MFVNeutralino_One2Two_SimpleObjects_h

#include <cmath>
#include "TVector2.h"
#include "JMTucker/MFVNeutralino/interface/MiniNtuple.h"
#include "Utility.h"
#include "VAException.h"

namespace mfv {
  struct VertexSimple {
    bool is_sig;
    bool is_fake;
    int ntracks;
    double x, y, z;
    double cxx, cxy, cyy;

    VertexSimple() : is_sig(false), is_fake(false), ntracks(-1), x(0), y(0), z(0), cxx(0), cxy(0), cyy(0) {}

    VertexSimple(const MiniNtuple& nt, int which, bool is_sig_)
      : is_sig(is_sig_),
        ntracks(which == 0 ? nt.ntk0 : nt.ntk1),
        x(which == 0 ? nt.x0 : nt.x1),
        y(which == 0 ? nt.y0 : nt.y1),
        z(which == 0 ? nt.z0 : nt.z1),
        cxx(0),
        cxy(0),
        cyy(0)
    {
      if (which != 0 && which != 1)
        jmt::vthrow("can't make a VertexSimple out of MiniNtuple for which = %i", which);
    }

    VertexSimple(double d2d_, double phi_)
      : is_sig(false),
        is_fake(true),
        ntracks(999),
        x(d2d_ * cos(phi_)),
        y(d2d_ * sin(phi_)),
        z(0),
        cxx(0),
        cxy(0),
        cyy(0)
    {}

    double d2d() const { return jmt::mag(x, y); }
    double d3d() const { return jmt::mag(x, y, z); }
    double dz () const { return fabs(z); }
    double phi() const { return atan2(y, x); }

    double d2d(const VertexSimple& o) const { return jmt::mag(x - o.x, y - o.y);          }
    double d3d(const VertexSimple& o) const { return jmt::mag(x - o.x, y - o.y, z - o.z); }
    double dz (const VertexSimple& o) const { return z - o.z; }
    double phi(const VertexSimple& o) const { return TVector2::Phi_mpi_pi(phi() - o.phi()); }

    double dxd(const VertexSimple& o) const { return (x - o.x) / d2d(o); }
    double dyd(const VertexSimple& o) const { return (y - o.y) / d2d(o); }
    double sig(const VertexSimple& o) const { return sqrt((cxx + o.cxx)*dxd(o)*dxd(o) + (cyy + o.cyy)*dyd(o)*dyd(o) + 2*(cxy + o.cxy)*dxd(o)*dyd(o)); }
 };

  //////////////////////////////////////////////////////////////////////////////

  struct VertexPair {
    VertexSimple first;
    VertexSimple second;
    double weight;

    VertexPair(const VertexSimple& f, const VertexSimple& s) : first(f), second(s), weight(0.) {}
    VertexPair(const MiniNtuple& nt, bool is_sig) : first(nt, 0, is_sig), second(nt, 1, is_sig), weight(0.) {}
    
    double d2d() const { return first.d2d(second); }
    double d3d() const { return first.d3d(second); }
    double dz () const { return first.dz (second); }
    double phi() const { return first.phi(second); }

    double sig() const { return first.sig(second); }
  };

  //////////////////////////////////////////////////////////////////////////////

  struct EventSimple : public MiniNtuple {
    EventSimple() : MiniNtuple(), sample(0), nvtx_sel(0) {}
    EventSimple(const MiniNtuple& nt) : MiniNtuple(nt), sample(0), nvtx_sel(0) {}
    int sample;
    int nvtx_sel;
    void invalidate_vertices() {
      nvtx = ntk0 = ntk1 = 0;
      x0 = y0 = z0 = x1 = y1 = z1 = 0;
    }
  };

  //////////////////////////////////////////////////////////////////////////////

  typedef std::vector<VertexSimple> VertexSimples;
  typedef std::vector<VertexPair> VertexPairs;
  typedef std::vector<EventSimple> EventSimples;

  //////////////////////////////////////////////////////////////////////////////

  struct Dataset {
    int toy; // negative for real data
    const EventSimples* events_1v;
    const EventSimples* events_2v;
    const VertexSimples* one_vertices;
    const VertexPairs* two_vertices;
    bool ok() { return events_1v && events_2v && one_vertices && two_vertices; }
    Dataset() : toy(0), events_1v(0), events_2v(0), one_vertices(0), two_vertices(0) {}
  };
}

#endif
