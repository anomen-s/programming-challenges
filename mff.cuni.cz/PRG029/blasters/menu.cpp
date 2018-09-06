#include "menu.h"

#include <windows.h>
#include <gl\gl.h>			// Header File For The OpenGL32 Library
#include "gl\glpng.h"

#include "blasters.h"
#include "gltools.h"
#include "gltext.h"
#include "globals.h"
#include "keyb.h"

#include <math.h>			// Header File For Windows Math Library

using namespace std;


class ConfigMenu: public Menu {
public:
    ConfigMenu(int p): player(p) {
		add("Player name", GetPlayerName, p);
		add("LEFT", SetupControls, p | KEY_BIT(KEY_LEFT));
		add("RIGHT", SetupControls, p | KEY_BIT(KEY_RIGHT));
		add("UP", SetupControls, p | KEY_BIT(KEY_UP));
		add("DOWN", SetupControls, p | KEY_BIT(KEY_DOWN));
		add("FIRE", SetupControls, p | KEY_BIT(KEY_FIRE));
//		add("Player controls", new ControlsMenu, p);
    }
private:
    int player;
};

/*class ControlsMenu: public Menu {
public:
    ControlsMenu(int p): player(p) {
		add("LEFT", SetupControls, p | KEY_BIT(KEY_LEFT));
		add("Player controls", SetupControls, p);
    }
private:
    int player;
};*/

class MainMenu: public Menu {
public:
	MainMenu() {
		add("Start Game",StartGame);
		add("Join Game",JoinGame);
		add("Player 1", new ConfigMenu(LOCALPLAYER1));
		add("Player 2", new ConfigMenu(LOCALPLAYER2));
		add("Exit", Exit, 0);
	}
};



#define MENU_TOP 0.3f
#define MENU_SPACE 0.16f



bool Menu::drawMenu()
{
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);	// Clear The Screen And The Depth Buffer

	glMatrixMode(GL_PROJECTION);						
	glLoadIdentity();									
	GLfloat aspect = 0.5f * (((GLfloat)globals.width / (GLfloat)globals.height) + 1.0f);
	if (globals.width > globals.height) {glOrtho(-aspect,aspect,-1,1,-5,5); }
	else { glOrtho(-1,1,-aspect,aspect,-5,5); }
	glMatrixMode(GL_MODELVIEW);							
	glLoadIdentity();									

	GLfloat y = MENU_TOP - MENU_SPACE * selected;

	glColor3f(0.1f,0.3f,0.6f);	// background
	glDisable(GL_TEXTURE_2D);
	glBegin(GL_QUADS);
		glVertex3f(-2,  -2,  -0.5f); // BL
		glVertex3f( 2,  -2,  -0.5f); // BR
		glVertex3f( 2, 2,  -0.5f); // TR
		glVertex3f(-2, 2,  -0.5f); // TL
	glEnd();
	glEnable(GL_TEXTURE_2D);

	glEnable(GL_BLEND);
	glBlendFunc(GL_SRC_ALPHA,GL_ONE);
	glDisable(GL_DEPTH_TEST);

	glColor3f(1,1,1);	
	glBindTexture(GL_TEXTURE_2D, textures[0]);
	glBegin(GL_QUADS);
		glTexCoord2f(0.0f, 0.0f); glVertex3f(-0.6f,  y,  -0.01f); // BL
		glTexCoord2f(1.0f, 0.0f); glVertex3f( 0.6f,  y,  -0.01f); // BR
		glTexCoord2f(1.0f, 1.0f); glVertex3f( 0.6f, y+0.75f*MENU_SPACE,  -0.01f); // TR
		glTexCoord2f(0.0f, 1.0f); glVertex3f(-0.6f, y+0.75f*MENU_SPACE,  -0.01f); // TL
	glEnd();
	
	y = MENU_TOP;

	glColor3f(1.0f,1.0f,1.0f);

	for (MenuItems::iterator it = items.begin(); it != items.end(); ++it) {
		glLoadIdentity();
		glTranslated(-0.0-0.5*0.1*strlen(it->title), y, 0);
		gltPrint(it->title);
		y-=MENU_SPACE;
	}
													
	glEnable(GL_DEPTH_TEST);
	return true;										// Keep Going
}

bool Menu::add(const char* title, boolProc proc, int param) {
	MenuItem mi;
	mi.title = title;
	mi.submenu = new MenuProc(proc, param);
	items.push_back(mi);
	return true;
}
bool Menu::add(const char* title, MenuBase* submenu) {
	MenuItem mi;
	mi.title = title;
	mi.submenu = submenu;
	items.push_back(mi);
	return true;
}
void Menu::initTextures() 
{
	textures[0] = loadtexture("gfx/menubar1.png");
}

int ShowMainMenu()
{
    playSound(SOUND_BEEP);
	MainMenu mainmenu;
	return mainmenu.run("Blasters");
}

int Menu::showMenu()
{
	ShowCursor(true);								// Show Mouse Pointer
	while (ProcessMessages())
	{
		if (globals.active) {
			if ((!drawMenu()) || testkey(VK_ESCAPE))	// print menu
			{
				return true;							// ESC or DrawGLScene Signalled A Quit
			}
			SwapBuffers(globals.hDC);			// Swap Buffers (Double Buffering)
		}//if active
		
		if (testkey(VK_UP)) {
			if ((selected) > 0) { selected--; }
		}
		if (testkey(VK_DOWN)) {
			if (selected < ((int)items.size()-1)) { selected++; }
		}
		if (testkey(VK_RETURN)) {
			MenuItem &mi = items[selected];
			mi.submenu->run(mi.title);
		}
		// parse keys
		
		// on mousePress call MenuHandler
	}//while

	return false;
}

