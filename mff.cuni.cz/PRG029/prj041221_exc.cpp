// prj041221_exc.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include <string>

using namespace std;
class MyException //: public exception  
{
	public:
	virtual const char * what() const
	{
		return "MyException";
	}
	virtual ~MyException() {}
};

class My2Exception : public MyException
{
	public:
	virtual const char * what() const
	{
		return "My2Exception";
	}
};

int throwexception() throw (My2Exception) {
	if (1 > 0 ) {
		throw My2Exception();
	}
}
int throwexc() throw (int) {
	return throwexception()+1;
}

int main(int argc, _TCHAR* argv[])
{
	try { throwexception();
	} catch (MyException e)	{
		cout << "caught exception " << e.what() << endl;
	}

	try { throwexception();
	} catch (My2Exception e)	{  // potomek musi byt pred predkem !
		cout << "caught exception " << e.what() << endl;
	} catch (MyException e)	{
		cout << "caught exception " << e.what() << endl;
	}

	try { throwexception();
	} catch (MyException& e)	{
		cout << "caught exception " << e.what() << endl;
	}

	string x;
	cin >> x;
	return 0;
}

