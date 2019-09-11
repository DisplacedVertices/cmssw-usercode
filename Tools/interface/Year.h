#ifndef JMTucker_Tools_interface_Year_h
#define JMTucker_Tools_interface_Year_h

#define MFVNEUTRALINO_2017

#define MFVNEUTRALINO_YEARS {2017, 2018}

#ifdef MFVNEUTRALINO_2017
#define MFVNEUTRALINO_YEAR   2017
#elif defined(MFVNEUTRALINO_2018)
#define MFVNEUTRALINO_YEAR   2018
#else
#error bad year
#endif

// this lets us uniquely determine the year from {MCStat,{JMT,MFV}Weight}Producer h_sums
#define MFVNEUTRALINO_YEARCODE_MULT 2371
#define MFVNEUTRALINO_YEARCODE (MFVNEUTRALINO_YEAR * MFVNEUTRALINO_YEARCODE_MULT)

namespace jmt {
  // for standalone code where we don't want to have to have two environments and we read the year out of the input file
  void set_year(int y);
  void assert_year(int y);
  class yearcode {
  public:
    yearcode() = delete;
    yearcode(const yearcode&) = delete;
    yearcode(double c);
    int year() const { return year_; }
    int nfiles() const { return nfiles_; }
  private:
    int year_;
    int nfiles_;
  };
}

#endif
