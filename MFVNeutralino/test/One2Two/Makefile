SHADOWDEPS = $(wildcard $(CMSSW_BASE)/src/JMTucker/MFVNeutralinoFormats/*/TriggerEnum*) $(CMSSW_BASE)/lib/$(SCRAM_ARCH)/libJMTuckerTools.so 

ROOTFLAGS=$(shell root-config --cflags --libs)
CFLAGS=-I${CMSSW_BASE}/src -I${CMSSW_RELEASE_BASE}/src -std=c++17 -O3

all: 2v_from_jets.exe statmodel.exe

MiniNtuple.o: ${CMSSW_BASE}/src/JMTucker/MFVNeutralino/src/MiniNtuple.cc ${CMSSW_BASE}/src/JMTucker/MFVNeutralino/interface/MiniNtuple.h
	g++ -I${CMSSW_BASE}/src -I${CMSSW_RELEASE_BASE}/src -std=c++17 $(ROOTFLAGS) -c $< -o $@

2v_from_jets.exe: 2v_from_jets.cc MiniNtuple.o $(SHADOWDEPS)
	g++ -g -Wall -I${CMSSW_BASE}/src -I${CMSSW_RELEASE_BASE}/src -std=c++17 $^ -o $@ $(ROOTFLAGS)

statmodel.exe: statmodel.cc
	g++ -O3 -Wall -std=c++17 $^ -o $@ -lstdc++fs $(SMFLAGS) $(ROOTFLAGS) -I${CMSSW_BASE}/src -L${CMSSW_BASE}/lib/${SCRAM_ARCH} -lJMTuckerTools

clean:
	rm -f 2v_from_jets.exe statmodel.exe
