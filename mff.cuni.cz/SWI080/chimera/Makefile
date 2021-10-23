CHIMERA_HOME=~/MWy/chimera-1.20
CC=gcc
CPP=g++

all: clean chat

chat: chat.o
	$(CPP) -o $@ chat.o $(CHIMERA_HOME)/lib/libchimera.a -lpthread -lssl

chat.o: chat.c channels.cpp
	$(CPP) -I $(CHIMERA_HOME)/include -c -o $@ $<

clean:
	rm -f *.o chat *~
