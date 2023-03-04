CFLAGS=-g -O2 -Wall -fstack-protector -fsanitize=undefined -ftrapv -Wno-psabi
#CFLAGS=-g -O0

TARGET=target
COMPILER=g++
SOURCES=main.cpp
EXECUTABLE=main

all:
	mkdir -p target
	$(COMPILER) $(CFLAGS) -o $(TARGET)/$(EXECUTABLE) $(SOURCES)
	cp input* $(TARGET)

run: clean all
	$(TARGET)/$(EXECUTABLE)

clean: 
	rm -f $(TARGET)/*
