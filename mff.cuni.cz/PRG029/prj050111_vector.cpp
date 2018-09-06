// prj050111_vector.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include <vector>

using namespace std;

template <class U, int s> 
class uloz_pole {
private:
	U pbuffer[s];
public:
	uloz_pole() { cout << "uloz_pole" << s << endl; }
	U& index(int i) { return pbuffer[i]; }
};

template <int s>
class uloz_pole<int, s> {
public:
	int pbuffer[s];
public:
	int& index(int i) { return pbuffer[i]; }
	uloz_pole() { cout << "uloz_pole_int " << s << endl; }
};

template <>
class uloz_pole<int, 5> {
public:
	int pbuffer[5];
public:
	int& index(int i) { return pbuffer[i]; }
	uloz_pole() { cout << "uloz_pole_int_5" << endl; }
};

template <class U, int s> 
class uloz_vector {
private:
	vector<U> pbuffer;
public:
	uloz_vector() { 
		for (int i = 0; i < s; i++) { pbuffer.push_back(0); } 
		cout << "uloz_vector " << s << endl;
	}
	U& index(int i) { return pbuffer[i]; }
};


template <typename T, int size, template <class U, int s> class uloz = uloz_pole>
class pole {
public:
	int velikost() { return size; }
	T & operator [] (int i) { 
		return uloziste.index(i);
	}
	T get(int i) { 
		return uloziste.index(i); 
	}
	bool set(int i, T value) { 
		if ((i >= size) || (i < 0)) return false;
		uloziste.index(i) = value; 
	}
private:
	uloz<T,size> uloziste;
};

/*template <class T, int size>
T & pole<T,size>::operator [] (int i) {
	return pbuffer[i]; 
}*/



typedef pole <int, 210> intpole1;

int main(int argc, _TCHAR* argv[])
{
	intpole1 p1;
	p1[0] = 20;
	p1.set(1,10);

	cout << p1[0] << endl;
	cout << p1[1];
	return 0;
}

