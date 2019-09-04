#ifndef JMTucker_Tools_interface_Year_h
#define JMTucker_Tools_interface_Year_h

#define MFVNEUTRALINO_2017

#ifdef MFVNEUTRALINO_2017
#define MFVNEUTRALINO_YEAR   2017
#elif defined(MFVNEUTRALINO_2018)
#define MFVNEUTRALINO_YEAR   2018
#else
#error bad year
#endif

// this lets us uniquely determine the year from {MCStat,{JMT,MFV}Weight}Producer h_sums
#define MFVNEUTRALINO_YEAR_P (MFVNEUTRALINO_YEAR*2371)

#endif
