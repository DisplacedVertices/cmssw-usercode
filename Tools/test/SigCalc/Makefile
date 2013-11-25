SOURCES       = SigCalc.cc fitPar.cc
INCLUDES      = SigCalc.h fitPar.h
OBJECTS       = $(patsubst %.cc, %.o, $(SOURCES))
ROOTCFLAGS   := $(shell root-config --cflags)
ROOTLIBS     := $(shell root-config --libs)
ROOTGLIBS    := $(shell root-config --glibs)
ROOTLIBS     := $(shell root-config --nonew --libs)
CFLAGS       += $(ROOTCFLAGS)
LIBS         += $(ROOTLIBS)
LIBS         += -lMinuit
LDFLAGS       = -O

all: $(OBJECTS)

%.o : %.cc $(INCLUDES)
	g++ $(CFLAGS) -c -o $@ $<

test:
	@echo $(CFLAGS)

clean:	
	-rm -f $(OBJECTS)
