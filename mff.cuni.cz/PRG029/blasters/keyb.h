#ifndef keyb_h
#define keyb_h

#define KEYS_ALPHA 1    // 0x41 - 0x5a
#define KEYS_NUM 2      // 0x30 - 0x39
#define KEYS_SYMBOLS 4
#define KEYS_NUMPAD 5   // 0x60 - 0x6F
#define KEYS_ALPHANUM (KEYS_ALPHA|KEYS_NUM)

#define KEYS_ALL (-1)
#define KEYS_TEXTINPUT (-2)

typedef unsigned char KEYCODE;

// tests if key is pressed and removes flag
extern bool testkey(KEYCODE);
	
// tests if key is pressed
extern bool peekkey(KEYCODE);

// looks for pressed key
// if range==KEYS_TEXTINPUT then key is set acording to keys.txt file
extern bool readkey(KEYCODE *, int range);

//initialization
// if false, program should end
extern bool InitKeyboard();

//clears keyboard buffer (sets all keypressed-flags to false)
extern void clearKeyBuffer();

extern const char* getKeyName(KEYCODE);
#endif
