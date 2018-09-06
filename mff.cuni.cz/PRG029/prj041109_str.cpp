// prj041109_str.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include <iostream>
#include <vector>
#include <string>
#include <algorithm>

using namespace std;


typedef vector < string > StrArray;

// vyrobit vektor int a naplnit
int main(int argc, _TCHAR* argv[])
{
  StrArray sa;
  
  string str;
  
  for (int i=0;i<4;++i) {
		cin >> str;
		sa.push_back(str);
	}
  cout << endl;

  string rem = "ddd";
	StrArray::iterator new_end = remove ( sa.begin(), sa.end(),  rem);
	sa.erase(new_end,sa.end());

	for (StrArray::iterator it = sa.begin(); it != sa.end(); ++it) {
		cout << *it << "   ";	cout << endl;
  }

/*	while (!ia.empty()) {
		cout << ia.back() << "  ";
		ia.pop_back();
	}
	cout << endl;*/
  
	cout << endl;
  string x;
  cin >> x;
 	return 0;
}



