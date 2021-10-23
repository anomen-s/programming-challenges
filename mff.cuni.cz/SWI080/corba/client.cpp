#include <assert.h>
#include <iostream>
#include <cstdlib>

#include <omniORB4/CORBA.h>
#include "master.h"

#define PING_VAL (3134)

// $Id: client.cpp 93 2009-04-01 19:24:24Z ludek $

using namespace std;
using namespace master;
using namespace consts;

int main (int iArgC, char *apArgV [])
{
	try
	{
		CORBA::ORB_var vORB;

		vORB = CORBA::ORB_init (iArgC, apArgV);

		CORBA::Object_var vServerBase;
		server_i_var vServer;

		assert (iArgC == 2);

		vServerBase = vORB->string_to_object (apArgV [1]);
		vServer = server_i::_narrow (vServerBase);

		// PING
		int pingres = vServer->ping(PING_VAL);
		
		if (pingres == PING_VAL) {
		    cout << "ping OK" << endl;
		} else {
		    cout << " ping KO - " << pingres << endl;
		}
		
		// 1. CONNECT
		//const char * peer = apArgV [2];

		CORBA::LongLong key = 1958756924L; // std::atol(apArgV[3]);
		CORBA::String_var cpeer = CORBA::string_dup("p5711");
		
		instance_i_ptr i = vServer->connect(cpeer, key);

		cout << "connected peer/key: " << cpeer << "/" << key << endl;
		
		// 2. attributes
		i->ready(true);
		
		cout << "ready: " << i->ready() << endl;
		while ( 0 == i->idle()) {
		    sleep(1);
		    cout << "idle: " <<i->idle() << endl;
		}
		
		// 3. get_status
		count_t cnt;
		cnt.long_long_value(key);
		cnt._d(vlong_long);
		octet_sequence_t_var seq;
		
		cout << "get_status... " << endl;
		i->get_status(cpeer.in(), cnt, seq);
		
		int seq_index = 0;
		if (cnt._d() == vlong) {
		    seq_index = cnt.long_value();
		}
		else if (cnt._d() == vshort) {
		    seq_index = cnt.short_value();
		}
		else {
		    cout << "unexpected type " << cnt._d() << endl;
		}
		
		// 4. request
		cout << "sending " << (int)(seq[seq_index]) << " from index " << seq_index << endl;
		request_t req;
		req.index = cnt;
		req.data <<= CORBA::Any::from_octet(seq[seq_index]);
		CORBA::Boolean r = i->request(req);
		cout << "Result: " << r << endl;
		
		// 5. END
		i->disconnect();
		vORB->destroy();
	}
	catch (const instance_i::protocol_e &iEx)
	{
		cerr << iEx._name() << " " << iEx.cause << endl;
	}
	catch (const server_i::connection_e &sEx)
	{
		cerr << sEx._name() << " " << sEx.cause << endl;
	}
}
