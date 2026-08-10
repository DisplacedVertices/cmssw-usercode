prescales.exe: prescales.cc ${CMSSW_BASE}/src/JMTucker/MFVNeutralino/src/MiniNtuple.cc ${CMSSW_BASE}/src/JMTucker/MFVNeutralino/interface/MiniNtuple.h
	g++ -O3 -I${CMSSW_BASE}/src -std=c++14 prescales.cc -o prescales.exe $(shell root-config --cflags --libs) ${CMSSW_BASE}/src/JMTucker/MFVNeutralino/src/MiniNtuple.cc
