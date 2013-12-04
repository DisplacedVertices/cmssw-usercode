SIGCALC_PATH  = ../../../Tools/test/SigCalc
SIGCALC_OBJS  = $(SIGCALC_PATH)/*.o
PROGNAME      = ssb
SOURCES       = ssb.cc
OBJECTS       = $(patsubst %.cc, %.o, $(SOURCES))
ROOTCFLAGS   := $(shell root-config --cflags)
ROOTLIBS     := $(shell root-config --libs)
ROOTGLIBS    := $(shell root-config --glibs)
ROOTLIBS     := $(shell root-config --nonew --libs)
CFLAGS       += $(ROOTCFLAGS) -I$(SIGCALC_PATH) -std=c++0x -Wall -Werror
LIBS         += $(ROOTLIBS)
LIBS         += -lMinuit
LDFLAGS       = -O

all: $(PROGNAME)

$(PROGNAME): $(OBJECTS) SigCalc
	g++ -o $@ $(OBJECTS) $(SIGCALC_OBJS) $(LDFLAGS) $(LIBS)

%.o : %.cc $(INCLUDES)
	g++ ${CFLAGS} -c -o $@ $<

test:
	@echo $(CFLAGS)

SigCalc:
	$(MAKE) -C $(SIGCALC_PATH)

clean:	
	-rm -f ${PROGNAME} ${OBJECTS}
	$(MAKE) -C $(SIGCALC_PATH) clean
