// prj041012.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include "iostream"

using namespace std;

class Base {
public:
	Base();
	Base(Base & src) {cout << "Base::Base(Base&) "; };
	virtual int f(int i);
	virtual int f(float i);
	int g(int i);
	virtual ~Base(void) { cout << "~Base()" << endl; };
};

class D: public Base {
private: 
	D();
	int value;
public:
	D(int init);
	virtual int f(int i);
	using Base::f;
	int g(int i);
	virtual ~D(void) { cout << "~D()" << endl; };
};
// *****************************************************************************
Base::Base() { 
	cout << "Base::Base() "; 
}

int Base::f(int i) { 
	cout << "BASE.f(int "<< i << ")" << endl; 
	return i; 
}
int Base::f(float i) { 
	cout << "BASE.f(double "<< i << ")" << endl; 
	return static_cast<int>(i); 
}
int Base::g(int i) {
	cout << "BASE.g(int "<< i << ")" << endl; 
	return i; 
}
D::D(int init) {
	value = init;
	cout << "D::D("<<init<<") "; 
}
int D::f(int i) { 
	cout << "D.f(int "<< i << ")" << endl; 
	return 2*i; 
}
int D::g(int i) {
	cout << "D.g(int "<< i << ")" << endl; 
	return i; 
}



int main(int argc, _TCHAR* argv[])
{
	cout << "* base: ";
	Base *b = new Base;
	cout << endl;
	b->f(1);
	b->f(10.1f);
	b->g(30);

	cout << "** base: ";
	Base bb = *b;
	cout << endl;

	cout << "* derived: ";
	D *d = new D(0);
	cout << endl;
	d->f(1);
	d->f(10.1f);
	d->g(30);

	cout << "* polymorph: ";
	Base *pb = d;
	cout << endl;
	pb->f(1);
	pb->f(10.1f);
	pb->g(30);

	delete b; // je potreba virtualni destruktor
	delete d;
	getchar();
	return 0;
}

