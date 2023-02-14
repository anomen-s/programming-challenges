CFLAGS=-g -c -O2 -Wall
CPPFLAGS=$(CFLAGS)

TARGET=target
COMPILER=gcc
SOURCES=main.cpp
EXECUTABLE=main

all:
	mkdir -p target
	$(COMPILER) -lstdc++ -Wall -o $(TARGET)/$(EXECUTABLE) $(SOURCES)
	cp input* $(TARGET)

run: clean all
	$(TARGET)/$(EXECUTABLE)

clean: 
	rm -f $(TARGET)/*
