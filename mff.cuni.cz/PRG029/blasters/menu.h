#ifndef menu_h
#define menu_h

#include <vector>
#include <windows.h>		// Header File For Windows
#include <gl\gl.h>			// Header File For The OpenGL32 Library

#define mtMENU 1
#define mtPROC 2

/* abstract base for menuitem handlers */
class MenuBase {
public:
	virtual bool run(const char*) = 0; // executed when selected appropriate menuitem
	virtual int menuType() = 0;
	virtual ~MenuBase() {}
};

// item of menu - contains handler & title */
struct MenuItem {
	MenuBase* submenu;
	const char* title;
};

typedef std::vector<MenuItem> MenuItems;


typedef bool(*boolProc)(int);

class MenuProc: public MenuBase {
public:
	MenuProc(boolProc proc, int param = 0): menuproc(proc), procparam(param) {}
	virtual bool run(const char*) { return menuproc(procparam); }
	virtual int menuType() { return mtPROC; }
	virtual ~MenuProc() {}
private:
	boolProc menuproc; // procedure invoked by run()
	int procparam;
};

class Menu: public MenuBase {
public:
	Menu(): selected(0) 
	{
	    title = "";
		initTextures();
	}
	virtual bool run(const char*) { return (showMenu() > 0); }
	virtual int menuType() { return mtMENU; }
	virtual ~Menu() {}
	bool add(const char* title, boolProc proc, int param = 0);
	bool add(const char* title, MenuBase* submenu);
protected:
	int showMenu();
	bool drawMenu();
	int selected;
	const char* title;
	void initTextures();
	MenuItems items;
	GLuint textures[1];
};


extern int ShowMainMenu();

#endif
