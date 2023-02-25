CFLAGS=-g -O2 -Wall -std=c++14 -pedantic -fstack-protector -fsanitize=undefined -ftrapv

TARGET=target
COMPILER=g++
SOURCES=main.cpp
EXECUTABLE=main

all:
	mkdir -p target
	#$(COMPILER) $(CFLAGS) -o $(TARGET)/$(EXECUTABLE) maptest.cpp
	$(COMPILER) $(CFLAGS) -o $(TARGET)/$(EXECUTABLE) $(SOURCES)
	cp input* $(TARGET)

run: clean all
	$(TARGET)/$(EXECUTABLE)
	python3 solve.py

clean: 
	rm -f $(TARGET)/*
