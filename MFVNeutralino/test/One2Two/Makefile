SOURCES       = Utility.cc ToyThrower.cc
INCLUDES      = $(patsubst %.cc, %.h, $(SOURCES))
OBJECTS       = $(patsubst %.cc, bin/%.o, $(SOURCES))
ROOTCFLAGS   := $(shell root-config --cflags)
ROOTLIBS     := $(shell root-config --nonew --glibs)
CFLAGS       += $(ROOTCFLAGS) -I $(CMSSW_BASE)/src -std=c++0x -Wall -Werror -g
LIBS         += $(ROOTLIBS) -lMinuit
LDFLAGS       = -O

all: $(OBJECTS)

%.o : %.cc $(INCLUDES)
	@mkdir -p bin
	g++ $(CFLAGS) -c -o $@ $<

test:
	@echo SOURCES:
	@echo $(SOURCES)
	@echo INCLUDES:
	@echo $(INCLUDES)
	@echo OBJECTS:
	@echo $(OBJECTS)
	@echo CFLAGS:
	@echo $(CFLAGS)

clean:	
	-rm -f $(OBJECTS)
