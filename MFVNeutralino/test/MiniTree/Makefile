looptrees.exe: looptrees.cc ${CMSSW_BASE}/src/JMTucker/MFVNeutralino/src/MiniNtuple.cc ${CMSSW_BASE}/src/JMTucker/MFVNeutralino/interface/MiniNtuple.h
	g++ -O3 -I${CMSSW_BASE}/src -I${CMSSW_RELEASE_BASE}/src -std=c++14 looptrees.cc -o looptrees.exe $(shell root-config --cflags --libs) ${CMSSW_BASE}/src/JMTucker/MFVNeutralino/src/MiniNtuple.cc
