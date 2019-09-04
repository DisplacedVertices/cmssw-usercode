#ifndef JMTucker_Tools_interface_Year_h
#define JMTucker_Tools_interface_Year_h

#define MFVNEUTRALINO_2017

#ifdef MFVNEUTRALINO_2017
#define MFVNEUTRALINO_YEAR 2017
#elif defined(MFVNEUTRALINO_2018)
#define MFVNEUTRALINO_YEAR 2018
#else
#error bad year
#endif

#endif
