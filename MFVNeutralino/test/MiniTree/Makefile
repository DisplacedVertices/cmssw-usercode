all: looptrees.exe btags_vs_bquarks.exe

looptrees.exe: looptrees.cc ${CMSSW_BASE}/src/JMTucker/MFVNeutralino/src/MiniNtuple.cc ${CMSSW_BASE}/src/JMTucker/MFVNeutralino/interface/MiniNtuple.h
	g++ -O3 -I${CMSSW_BASE}/src -I${CMSSW_RELEASE_BASE}/src -std=c++14 looptrees.cc -o looptrees.exe $(shell root-config --cflags --libs) ${CMSSW_BASE}/src/JMTucker/MFVNeutralino/src/MiniNtuple.cc

btags_vs_bquarks.exe: btags_vs_bquarks.cc ${CMSSW_BASE}/src/JMTucker/MFVNeutralino/src/MiniNtuple.cc ${CMSSW_BASE}/src/JMTucker/MFVNeutralino/interface/MiniNtuple.h
	g++ -O3 -I${CMSSW_BASE}/src -I${CMSSW_RELEASE_BASE}/src -std=c++14 btags_vs_bquarks.cc -o btags_vs_bquarks.exe $(shell root-config --cflags --libs) ${CMSSW_BASE}/src/JMTucker/MFVNeutralino/src/MiniNtuple.cc

clean:
	rm -f looptrees.exe btags_vs_bquarks.exe
