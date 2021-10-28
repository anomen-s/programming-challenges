COMPILER=gcc
LINKER=gcc
OBJECTS=main.o plist.o
HEADERS=plist.h main.h
EXECUTABLE=mbrview

LDFLAGS=-lstdc++ 
CFLAGS=-g -c -Wall #-DNDEBUG

all: $(EXECUTABLE)

clean: 
	rm -f $(EXECUTABLE) *.o 
	if [ "`ls *~* 2> /dev/null`" ] ; then mv *~* /tmp ; fi

$(EXECUTABLE): $(OBJECTS)
	$(LINKER) $(LDFLAGS) -o $(EXECUTABLE)  $(OBJECTS)

main.o: main.cpp $(HEADERS)
	$(COMPILER) $(CFLAGS) -o main.o main.cpp

plist.o: plist.cpp $(HEADERS)
	$(COMPILER) $(CFLAGS) -o plist.o plist.cpp
