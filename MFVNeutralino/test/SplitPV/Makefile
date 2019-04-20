include $(CMSSW_BASE)/src/JMTucker/Tools/NtupleMakefile.in

SHADOWDEPS += $(CMSSW_BASE)/lib/$(SCRAM_ARCH)/libJMTuckerMFVNeutralino.so
FLAGS += -lJMTuckerMFVNeutralino

copier.cc: $(SHADOWDEPS)
	generate_ntuple_copier.sh mfv::SplitPVNtuple mfvSplitPVs
