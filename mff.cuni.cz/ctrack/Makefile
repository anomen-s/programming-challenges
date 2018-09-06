#DAEMON=-DDAEMON_SUPPORT 
CFLAGS=-g -c -Wall # -v -g

LINK_LINUX=-lstdc++ -lpthread -Wall # -v
LINK_SOLARIS=-lstdc++ -lpthread -lsocket -lnsl -Wall 
LINK_FREEBSD=-pthread -lstdc++ -Wall 
LINK_IRIX=-shared # doesn't work
LDFLAGS=$(LINK_LINUX)

COMPILER=gcc
LINKER=gcc
OBJECTS=benc.o config.o ctrack.o db.o error.o http.o server.o str.o threads.o udp.o
HEADERS=benc.h config.h ctrack.h db.h error.h http.h server.h str.h threads.h udp.h
EXECUTABLE=ctrack


all:
	if [ "Linux" = `uname` ] ; then make linux ; \
	elif [ "SunOS" = `uname` ] ; then make solaris ; \
	elif [ "IRIX64" = `uname` ] ; then make irix ; \
	elif [ "FreeBSD" = `uname` ] ; then make freebsd ; \
	else echo "unknown system: `uname`" ; \
	fi

install: all
	strip $(EXECUTABLE)
	cp $(EXECUTABLE) /usr/bin/$(EXECUTABLE)
	cp ctrack.conf /etc/ctrack.conf

build: clean linux
	rm -f $(OBJECTS)

run: all
	./ctrack

clean: 
	rm -f $(EXECUTABLE) *.o 
 
$(EXECUTABLE): $(OBJECTS)
	$(LINKER) $(LDFLAGS) -o $(EXECUTABLE)  $(OBJECTS)

linux: 
	make $(EXECUTABLE) "LDFLAGS=$(LINK_LINUX)" 
solaris:
	make $(EXECUTABLE) "LDFLAGS=$(LINK_SOLARIS)"
freebsd:
	make $(EXECUTABLE) "LDFLAGS=$(LINK_FREEBSD)"
irix:
	make $(EXECUTABLE) "LDFLAGS=$(LINK_IRIX)"


benc.o: benc.cpp $(HEADERS)
	$(COMPILER) $(CFLAGS) -o benc.o benc.cpp
config.o: config.cpp $(HEADERS)
	$(COMPILER) $(CFLAGS) -o config.o config.cpp
ctrack.o: ctrack.cpp $(HEADERS)
	$(COMPILER) $(CFLAGS) $(DAEMON) -o ctrack.o ctrack.cpp
db.o: db.cpp $(HEADERS)
	$(COMPILER) $(CFLAGS) -o db.o db.cpp
error.o: error.cpp $(HEADERS)
	$(COMPILER) $(CFLAGS) -o error.o error.cpp
http.o: http.cpp $(HEADERS)
	$(COMPILER) $(CFLAGS) -o http.o http.cpp
server.o: server.cpp $(HEADERS)
	$(COMPILER) $(CFLAGS) -o server.o server.cpp
str.o: str.cpp $(HEADERS)
	$(COMPILER) $(CFLAGS) -o str.o str.cpp
threads.o: threads.cpp $(HEADERS)
	$(COMPILER) $(CFLAGS) -o threads.o threads.cpp
udp.o: udp.cpp error.h $(HEADERS)
	$(COMPILER) $(CFLAGS) -o udp.o udp.cpp

