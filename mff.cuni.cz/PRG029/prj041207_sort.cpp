// prj041207_sort.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include <string>
#include <fstream>
#include <sstream>
#include <algorithm>
#include <deque>

using namespace std;

typedef deque < string > StringArray;

int len = -1;

bool lt( string elem1, string elem2 )
{
	char *buf1 = new char[len+1];
	char *buf2 = new char[len+1];
	memset(buf1,0,len+1);
	memset(buf2,0,len+1);
	strncpy(buf1, elem1.c_str(), len);
	strncpy(buf2, elem2.c_str(), len);
	for (int i = 0; i < len; i++)
	{
		if (buf1[i] != buf2[i]) {
			return (buf1[i] < buf2[i]);
		}
	}
	return false;
}

int main(int argc, _TCHAR* argv[])
{

	if (argc < 3) { return -1; }
	if (argc = 4) { len = atoi(argv[3]); }
	ifstream vstup;
	try {

	vstup.exceptions(ios::failbit);
	vstup.open(argv[1], ios::in);

	string str;
	StringArray pole;
	while (!vstup.eof()) {
		//vstup >> str;
		getline(vstup, str);
		istringstream s(str);
     	string str1;
     	int i;
     	s >> str1;
     	s >> i;
     	s >> i;
     	s >> i;


		pole.push_back(str);
	}
	if (len == -1) {
		sort( pole.begin( ), pole.end( ));
	} else {
		sort( pole.begin( ), pole.end( ), lt);
	}

	ofstream vystup;
	vystup.exceptions( ios::failbit);
	vystup.open(argv[2], ios::out);

	for ( StringArray::iterator i = pole.begin() ; i != pole.end() ; ++i )
   {
      vystup << *i << endl;
   }
	
	}   catch( ios_base::failure f ) 
   {
      cout << "Caught an exception." << endl;
   }

	return 0;
}

