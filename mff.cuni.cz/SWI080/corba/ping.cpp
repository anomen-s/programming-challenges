#include <assert.h>
#include <iostream>

#include <omniORB4/CORBA.h>
#include "master.h"

#define PING_VAL (133)

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

		int res = vServer->ping(PING_VAL);
		
		if (res == PING_VAL) {
		    cout << "OK - " << res << endl;
		} else {
		    cout << "KO - " << res << endl;
		}

		vORB->destroy ();
	}
	catch (const CORBA::SystemException &sEx)
	{
		cerr << sEx._name() << endl;
	}
}
