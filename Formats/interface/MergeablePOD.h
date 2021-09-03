#ifndef DVCode_Tools_MergeablePOD_h
#define DVCode_Tools_MergeablePOD_h

namespace jmt {
  template <typename T>
  class MergeablePOD {
  public:
    MergeablePOD() { reset(); }
    MergeablePOD(const T& v) : val_(v) {}
    
    void reset() { val_ = 0; }
    T get() const { return val_; }
    void set(const T& v) { val_ = v; }
    void operator+=(const T& v) { val_ += v; }

    bool mergeProduct(const MergeablePOD<T>& v) {
      val_ += v.get();
      return true;
    }

  private:
    T val_;
  };

  typedef MergeablePOD<int> MergeableInt;
  typedef MergeablePOD<float> MergeableFloat;
}

#endif
