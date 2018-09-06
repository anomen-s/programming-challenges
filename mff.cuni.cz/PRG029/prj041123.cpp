// prj041123.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include <iostream>
#include <fstream>
#include <string>

#include <map>

using namespace std;

 typedef multimap <string, string > slovnik;

int main(int argc, _TCHAR* argv[])
{
  slovnik s1;

   ifstream soubor( "slovnik1.txt" );
   string cz, en;
//   char en[100];
   if( soubor ) {
       while ( soubor.good( ) ) {
        soubor >> cz >> en;
        //soubor.getline( &cz[0], 90, '\n' );
        //soubor.getline( &en[0], 90, '\n' );
        s1.insert(slovnik::value_type(cz,en));
        cout << cz << "  " << en << endl;
       }
   }
   cout << "  ---------- "  << endl;

   for (slovnik::const_iterator it = s1.begin(); it != s1.end(); ++it) {
     cout << it->first << " -> " << it->second << endl;
   }

  cout << "  ---------- "  << endl << "hledat heslo: ";
  string hledani;
  cin >> hledani;
  cout << endl;
  cout << endl << "find(\"" << hledani << "\"):  ";
  for (slovnik::const_iterator it = s1.lower_bound(hledani); it != s1.upper_bound(hledani);++it) {
    cout << it->second  << " ";
  }
  cout << endl;
  cin >> hledani;
  
	return 0;
}

