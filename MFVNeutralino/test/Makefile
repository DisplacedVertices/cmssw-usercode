clustertrackstest.exe: clustertrackstest.cc ${CMSSW_BASE}/src/JMTucker/MFVNeutralino/src/MiniNtuple.cc ${CMSSW_BASE}/src/JMTucker/MFVNeutralino/interface/MiniNtuple.h
	g++ -O3 -I${CMSSW_BASE}/src -std=c++14 clustertrackstest.cc -o clustertrackstest.exe $(shell /cvmfs/cms.cern.ch/slc6_amd64_gcc493/external/fastjet/3.1.0/bin/fastjet-config --cxxflags --libs --plugins) $(shell root-config --cflags --libs) ${CMSSW_BASE}/src/JMTucker/MFVNeutralino/src/MiniNtuple.cc

zclustertest.exe: zclustertest.cc ${CMSSW_BASE}/src/JMTucker/MFVNeutralino/src/MiniNtuple.cc ${CMSSW_BASE}/src/JMTucker/MFVNeutralino/interface/MiniNtuple.h
	g++ -O3 -I${CMSSW_BASE}/src -std=c++14 zclustertest.cc -o zclustertest.exe $(shell root-config --cflags --libs) ${CMSSW_BASE}/src/JMTucker/MFVNeutralino/src/MiniNtuple.cc
