CFLAGS=-g -O2 -Wall -Wno-psabi -march=native -std=c++17 -pedantic -fstack-protector -fsanitize=undefined -ftrapv

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
