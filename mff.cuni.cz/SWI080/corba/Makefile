all: client ping

master.h masterSK.cpp: master.idl
	~/omniORB/bin/omniidl -bcxx -Wbh=.h -Wbs=SK.cpp master.idl

masterSK.o: masterSK.cpp master.h
	g++ -I ~/omniORB/include -c -o $@ masterSK.cpp

client.o: client.cpp master.h
	g++ -I ~/omniORB/include -c -o $@ client.cpp


client: masterSK.o client.o
	g++ -o $@ -Wl,-rpath ~/omniORB/lib -L ~/omniORB/lib -lomniORB4 -lomniDynamic4 masterSK.o client.o


run: client IOR
	./client `cat IOR`


ping.o: ping.cpp master.h
	g++ -I ~/omniORB/include -c -o $@ ping.cpp

ping: masterSK.o ping.o
	g++ -o $@ -Wl,-rpath ~/omniORB/lib -L ~/omniORB/lib -lomniORB4 -lomniDynamic4 masterSK.o ping.o

run-ping: ping IOR
	./ping `cat IOR`


IOR:
	wget -O IOR http://dsrg.mff.cuni.cz/~ceres/sch/mwy/download/IOR

clean:
	rm -f *.o client ping master.h masterSK.cpp IOR
