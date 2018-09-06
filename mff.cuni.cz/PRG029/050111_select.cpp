// 050111_select.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"


template <bool flag, class T, class U>
struct SELECT {
	 typedef T Result;
};
template <class T, class U>
struct SELECT <false,T,U>{
	typedef U Result;
};

template <class T>
typedef SELECT<sizeof(T) < 8, T, T*>::Result typ;



int main(int argc, _TCHAR* argv[])
{
	return 0;
}

