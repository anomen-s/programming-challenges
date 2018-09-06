// prj050116_str.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include <string>
#include <iostream>

using namespace std;
int test(string prompt, string& text)
{
	
	cout << prompt << endl;
	cin >> text;
	return true;
}

int test1(const char *str)
{
	cout << str << endl;
	return true;
}

int main(int argc, char* argv[])
{
	std::string x("text");
	test("input:", x);

	x = x + ".";
	test1(x.c_str());
	return 0;
}

