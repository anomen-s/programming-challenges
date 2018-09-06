// prj041109.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;


typedef vector < int > IntArray;

// vyrobit vektor int a naplnit
int main(int argc, _TCHAR* argv[])
{
  IntArray ia;
  int x;
  
  
	for (int i=0;i <5;i++) {
		cin >> x;
		ia.push_back(x);
	}

  IntArray::iterator new_end =  std::remove(ia.begin(), ia.end(), 11);

  for (IntArray::iterator it = ia.begin(); it != new_end; ++it) {
		cout << *it << "   ";
  }


/*	while (!ia.empty()) {
		cout << ia.back() << "  ";
		ia.pop_back();
	}
	cout << endl;*/
  
  cin >> x;
 	return 0;
}

