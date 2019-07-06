#ifndef JMTucker_Tools_ExtValue
#define JMTucker_Tools_ExtValue

#include <limits>

namespace jmt {
  class ExtValue {
  private:
    bool lt_;
    double v_;
    int i_;
  public:
    ExtValue(bool lt) : lt_(lt), v_(lt ? std::numeric_limits<double>::max() : -std::numeric_limits<double>::max()), i_(-1) {}
    void operator()(const int i, const double v) { if ((lt_ && v < v_) || (!lt_ && v > v_)) { v_ = v; i_ = i; } }
    void operator()(             const double v) { (*this)(-1, v); }
    operator double() const { return v_; }
    int i() const { return i_; }
  };

  class MinValue : public ExtValue { public: MinValue() : ExtValue(true)  {} };
  class MaxValue : public ExtValue { public: MaxValue() : ExtValue(false) {} };
}

#endif
