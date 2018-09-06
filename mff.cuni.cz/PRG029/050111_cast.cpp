// 050111_cast.cpp : Defines the entry point for the console application.
//

// cast text

#include "stdafx.h"


template <class T, class U>
class Conv {
	typedef char SMALL;
	class BIG {
		char _d[2];
	};
	static SMALL test(U);
	static BIG	test(...);
	static T	makeT();
public:
	enum { exists = sizeof(test(makeT())) == sizeof(SMALL) };
};

int main(int argc, _TCHAR* argv[])
{
	return 0;
}

