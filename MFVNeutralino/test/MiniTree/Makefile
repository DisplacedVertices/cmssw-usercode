SHADOWDEPS = $(wildcard $(CMSSW_BASE)/src/JMTucker/MFVNeutralinoFormats/*/TriggerEnum*) $(CMSSW_BASE)/lib/$(SCRAM_ARCH)/libJMTuckerTools.so

ROOTFLAGS=$(shell root-config --cflags --libs)
CFLAGS=-I${CMSSW_BASE}/src -I${CMSSW_RELEASE_BASE}/src -std=c++17 -O3
EXES=looptrees.exe 

all: $(EXES)

MiniNtuple.o: ${CMSSW_BASE}/src/JMTucker/MFVNeutralino/src/MiniNtuple.cc ${CMSSW_BASE}/src/JMTucker/MFVNeutralino/interface/MiniNtuple.h
	g++ $(CFLAGS) $(ROOTFLAGS) -c $< -o $@

%.exe: %.cc MiniNtuple.o $(SHADOWDEPS)
	g++ $(CFLAGS) $(ROOTFLAGS) $^ -o $@

clean:
	rm -f MiniNtuple.o $(EXES)
