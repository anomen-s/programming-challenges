#include "keyb.h"

#include <string>
#include <fstream>
#include "globals.h"

using namespace std;

static char keyNames[256][16];
static char skeyNames[256]; //shift

bool InitKeyboard()
{
	ifstream keylist;
	keylist.open("data/keys.txt", ios::in);
	if (!keylist.is_open()) { return false; }
	string buffer;
	int keycode;
	char keyname[16];
	char skeyname[16];
	memset(keyNames, 0, sizeof(keyNames));
	memset(skeyNames, 0, sizeof(skeyNames));
	while (!keylist.eof()) {
	    getline(keylist, buffer);
	    keycode = 0;
	    sscanf(buffer.c_str(),"%i %15s %1s", &keycode, keyname, skeyname);
	    strncpy(keyNames[(KEYCODE)keycode], keyname, strlen(keyname));
	    skeyNames[(KEYCODE)keycode] = skeyname[0];
	}//while
    keylist.close();
    return true;
}

const char* getKeyName(KEYCODE key)
{
    static const char* emptyStr = "";
    if (strlen(keyNames[key]) > 0) {
        return keyNames[key];
    }
    return emptyStr;
}

void clearKeyBuffer()
{
    for (int k = 0; k < 256; k++) {
        globals.keys[k] = false;
    }//for
}


bool testkey(KEYCODE key)
{
	if (globals.keys[key]) {
		globals.keys[key]=false;
		return true;
	}
	return false;
}

bool peekkey(KEYCODE key)
{
	return (globals.keys[key]);
}

bool testKeyRange(KEYCODE *key, int lo, int hi) 
{
	for (int i = lo; i <= hi; i++) {
		if (globals.keys[i]) {
			globals.keys[i] = false;
			*key = char(i);
			return true;
		}
	}//for
	return false;
}

KEYCODE scancode2char(KEYCODE i) 
{
  if ((GetKeyState(VK_SHIFT)& 0x80) && (skeyNames[i] != 0)) {
    return KEYCODE(skeyNames[i]);
  }
  else {
    return KEYCODE(keyNames[i][0]);
  }
}

bool readkey(KEYCODE *key, int range) 
{
	if (range == KEYS_ALL) {
		for (int i=0; i <= 255; i++) {
			if (globals.keys[i]) {
				globals.keys[i] = false;
				*key = char(i);
				return true;
			}
		}//for
		return false;
	}//if

	if (range == KEYS_TEXTINPUT) {
		for (int i=0; i <= 255; i++) {
			if (globals.keys[i])
			 if  ((strlen(keyNames[i])==1)) {
				globals.keys[i] = false;
				*key = scancode2char(i);
				return true;
			}
		}//for
		return false;
	}//if
	
	if (range & KEYS_SYMBOLS) {
    	if (testKeyRange(key, 0xBA, 0xE4)) { return true; }
	}//if
	
	if (range & KEYS_NUMPAD) {
    	if (testKeyRange(key, 0x60, 0x6F)) { return true; }
	}//if
	if (range & KEYS_NUM) {
    	if (testKeyRange(key, int('0'), int('9'))) { return true; }
	}//if
	if (range & KEYS_ALPHA) {
    	if (testKeyRange(key, int('A'), int('Z'))) { return true; }
	}//if

	return false;
}
