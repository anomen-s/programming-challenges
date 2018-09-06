#include "glgame.h"

#include "gltext.h"
#include "gltools.h"
#include "globals.h"
#include "logger.h"

using namespace std;

static GLuint gametextures[20];
static GLuint poweruptextures[10];
//static GLuint gamelists;
static GLUquadricObj *q;

#define SQUARE_SIZE 1.0f

#define TEXTURE_ROCK 0
#define TEXTURE_ROCK1 1
#define TEXTURE_FLOOR 2
#define TEXTURE_PLAYER 3
#define TEXTURE_BOMB 4
#define TEXTURE_WALL 5

#define TEXTURE_EXPLODE_C 6  // must be in sequence
#define TEXTURE_EXPLODE_C1 7
#define TEXTURE_EXPLODE_M 8
#define TEXTURE_EXPLODE_M1 9
#define TEXTURE_EXPLODE_E 10
#define TEXTURE_EXPLODE_E1 11

//#define DL_ROCK 0 // display lists were removed
//#define DL_WALL 3
//#define DL_PLAYER 1
//#define DL_BOMB 2


bool glGameInit()
{
	gametextures[TEXTURE_ROCK] = loadtexture("gfx/stone.png");
	gametextures[TEXTURE_ROCK1] = loadtexture("gfx/stone1.png");
	gametextures[TEXTURE_WALL] = loadtexture("gfx/wall.png");
	gametextures[TEXTURE_FLOOR] = loadtexture("gfx/floor.png");
	gametextures[TEXTURE_PLAYER] = loadtexture("gfx/p_head.png");
	gametextures[TEXTURE_BOMB] = loadtexture("gfx/black.png");
	gametextures[TEXTURE_EXPLODE_C] = loadtexture("gfx/xcenter.png");
	gametextures[TEXTURE_EXPLODE_M] = loadtexture("gfx/xmiddle.png");
	gametextures[TEXTURE_EXPLODE_E] = loadtexture("gfx/xend.png");
	gametextures[TEXTURE_EXPLODE_C1] = loadtexture("gfx/xcenter.png");
	gametextures[TEXTURE_EXPLODE_M1] = loadtexture("gfx/xmiddle.png");
	gametextures[TEXTURE_EXPLODE_E1] = loadtexture("gfx/xend.png");

	poweruptextures[POWER_NOBOMB] = loadtexture("gfx/pup_nobomb.png");
	poweruptextures[POWER_STRENGTH] = loadtexture("gfx/pup_str.png");
	poweruptextures[POWER_BOMB] = loadtexture("gfx/pup_bomb.png");
	poweruptextures[POWER_SPEED] = loadtexture("gfx/pup_speed.png");

//	gamelists=glGenLists(10);

	q=gluNewQuadric();							// Create A Pointer To The Quadric Object (Return 0 If No Memory) (NEW)
	gluQuadricNormals(q, GLU_SMOOTH);			// Create Smooth Normals (NEW)
	gluQuadricTexture(q, GL_TRUE);				// Create Texture Coords (NEW)

	return true;
}

bool glGameDestroy()
{
	return true;
}

#define MENU_TOP 0.4f
#define MENU_SPACE 0.16f

bool DrawGameStats(Game& game)
{
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);	// Clear The Screen And The Depth Buffer

	glMatrixMode(GL_PROJECTION);						
	glLoadIdentity();									
	GLfloat aspect = 0.5f * (((GLfloat)globals.width / (GLfloat)globals.height) + 1.0f);
	if (globals.width > globals.height) {glOrtho(-aspect,aspect,-1,1,-5,5); }
	else { glOrtho(-1,1,-aspect,aspect,-5,5); }
	glMatrixMode(GL_MODELVIEW);							
	glLoadIdentity();									

	GLfloat y = MENU_TOP - MENU_SPACE * 1;

	glColor3f(1,1,0);	
    string l = strprintf("Waiting for players...");
	if (!game.localGame()) {
	  l = game.ghost;
    }
    glTranslated(-0.04*l.length(), 0.6f, 0.5);
    gltPrint(l);
	glLoadIdentity();									

	if (game.localGame()) {     // bottom message
   	    glColor3f(0.7f,0.7f,0);	
        glTranslated(-1, -0.98f, 0.2);
        gltPrint("Press Enter to start game");
    	glLoadIdentity();									
        glTranslated(-1.15, -0.85f, 0.2);
        gltPrint("Press 1, 2 to remove players");
    	glLoadIdentity();									

	}//if

	
	y = MENU_TOP;
	glColor3f(1.0f,1.0f,1.0f);

	for (Players::iterator p = game.players.begin(); p != game.players.end(); ++p) {
        string l = strprintf("%i", (int)p->score); // SCORES
		glLoadIdentity();
		glTranslated(-0.6, y, 0.5);
		gltPrint(l);
        
		glLoadIdentity();
		glTranslated(-0.3, y, 0.5);
		gltPrint(p->name);                          // name

        if (((!game.localGame()) && (p->type() == Player::PT_LOCAL1)) || (p->ping > 0)) {
		    glLoadIdentity();
		    glTranslated(0.7, y, 0.5);
		    gltPrint(strprintf("[%i]", p->ping));       //pinf
        }//if
		y-=MENU_SPACE;
	}
	return true;
}

void DrawFloor(Game &game) 
{
	GLfloat w = (GLfloat)game.getWidth();
	GLfloat h = (GLfloat)game.getHeight();
	glLoadIdentity();									
	glColor3f(1.0f,1.0f,1.0f);
	glBindTexture(GL_TEXTURE_2D, gametextures[TEXTURE_FLOOR]);		// Select Our Font Texture
	glBegin(GL_QUADS);							// Use A Quad For Each Character
		glTexCoord2f(0,0);	glVertex3f(0,0,0);		// Vertex Coord (Bottom Left)
		glTexCoord2f(w,0);	glVertex3f(w,0,0);	// Vertex Coord (Bottom Right)
		glTexCoord2f(w,h);	glVertex3f(w,h,0);// Vertex Coord (Top Right)
		glTexCoord2f(0,h);	glVertex3f(0,h,0);	// Vertex Coord (Top Left)
		//WALL right
		glTexCoord2f(0,0);	glVertex3f(w,h,0);		// Vertex Coord (Bottom Left)
		glTexCoord2f(1,0);	glVertex3f(w,0,0);	// Vertex Coord (Bottom Right)
		glTexCoord2f(1,1);	glVertex3f(w+1,-1,1);// Vertex Coord (Top Right)
		glTexCoord2f(0,1);	glVertex3f(w+1,h+1,1);	// Vertex Coord (Top Left)
		//LEFT
		glTexCoord2f(0,0);	glVertex3f(0,0,0);		// Vertex Coord (Bottom Left)
		glTexCoord2f(1,0);	glVertex3f(0,h,0);	// Vertex Coord (Bottom Right)
		glTexCoord2f(1,1);	glVertex3f(-1,h+1,1);// Vertex Coord (Top Right)
		glTexCoord2f(0,1);	glVertex3f(-1,-1,1);	// Vertex Coord (Top Left)
		//TOP
		glTexCoord2f(0,0);	glVertex3f(0,h,0);		// Vertex Coord (Bottom Left)
		glTexCoord2f(1,0);	glVertex3f(w,h,0);	// Vertex Coord (Bottom Right)
		glTexCoord2f(1,1);	glVertex3f(w+1,h+1,1);// Vertex Coord (Top Right)
		glTexCoord2f(0,1);	glVertex3f(-1,h+1,1);	// Vertex Coord (Top Left)
		//BOTTOM
		glTexCoord2f(0,0);	glVertex3f(w,0,0);		// Vertex Coord (Bottom Left)
		glTexCoord2f(1,0);	glVertex3f(0,0,0);	// Vertex Coord (Bottom Right)
		glTexCoord2f(1,1);	glVertex3f(-1,-1,1);// Vertex Coord (Top Right)
		glTexCoord2f(0,1);	glVertex3f(w+1,-1,1);	// Vertex Coord (Top Left)
	glEnd();
}

void DrawTimer(Game& game) 
{
    if (game.timelimit > 0) {
        glPushMatrix();
        glLoadIdentity();
        glTranslatef(game.getWidth()/2.0f, game.getHeight()+1.0f, 2.0f);
        int timeout = (game.timelimit - int(globals.getGameTimer() - game.gamestart)) / 1000;
        int m = timeout / 60;
        int s = timeout - (m*60);
        glScalef(4, 4, 4);
        if (m == 0) {
            if (s <= 10) {      glColor3f(1, 1, 0); } 
            else if (s <= 5) {  glColor3f(1, 0, 0); } 
            else {              glColor3f(1, 1, 1); }
        }//if
        #ifdef _DEBUG
            gltPrintf("Time: %2i:%2i   [FPS: %i/%i]", m, s, logger->getFPS(0), logger->getFPS(1));
        #else
            gltPrintf("Time: %2i:%2i", m, s);
        #endif
        glPopMatrix();
    }//if
}

void DrawRockOrWall(int textype, float shear = 0.0f) 
{
	glColor3f(1.0f,1.0f,1.0f);
	glBindTexture(GL_TEXTURE_2D, gametextures[textype]);		// Select Our Font Texture
	glTranslatef(-0.5f, -0.5f, 0);
	glBegin(GL_QUADS);							// Use A Quad For Each Character
		//FRONT
		glTexCoord2f(0,0);	glVertex3f(0+shear,0+shear,SQUARE_SIZE);		// Vertex Coord (Bottom Left)
		glTexCoord2f(1,0);	glVertex3f(SQUARE_SIZE-shear,0+shear,SQUARE_SIZE);	// Vertex Coord (Bottom Right)
		glTexCoord2f(1,1);	glVertex3f(SQUARE_SIZE-shear,SQUARE_SIZE-shear,SQUARE_SIZE);// Vertex Coord (Top Right)
		glTexCoord2f(0,1);	glVertex3f(0+shear,SQUARE_SIZE-shear,SQUARE_SIZE);	// Vertex Coord (Top Left)
	glEnd();
	glBegin(GL_QUADS);							// Use A Quad For Each Character
		//LOWER SIDE
		glTexCoord2f(0,0);	glVertex3f(0, 0, 0);		// Vertex Coord (Bottom Left)
		glTexCoord2f(1,0);	glVertex3f(SQUARE_SIZE, 0, 0);	// Vertex Coord (Bottom Right)
		glTexCoord2f(1,1);	glVertex3f(SQUARE_SIZE-shear, 0+shear, SQUARE_SIZE);// Vertex Coord (Top Right)
		glTexCoord2f(0,1);	glVertex3f(0+shear, 0+shear, SQUARE_SIZE);	// Vertex Coord (Top Left)
		//RIGHT SIDE
		glTexCoord2f(0,0);	glVertex3f(SQUARE_SIZE, 0, 0);		// Vertex Coord (Bottom Left)
		glTexCoord2f(1,0);	glVertex3f(SQUARE_SIZE, SQUARE_SIZE, 0);	// Vertex Coord (Bottom Right)
		glTexCoord2f(1,1);	glVertex3f(SQUARE_SIZE-shear, SQUARE_SIZE-shear, SQUARE_SIZE);// Vertex Coord (Top Right)
		glTexCoord2f(0,1);	glVertex3f(SQUARE_SIZE-shear, 0+shear, SQUARE_SIZE);	// Vertex Coord (Top Left)
		//TOP SIDE
		glTexCoord2f(0,0);	glVertex3f(SQUARE_SIZE, SQUARE_SIZE, 0);		// Vertex Coord (Bottom Left)
		glTexCoord2f(1,0);	glVertex3f(0, SQUARE_SIZE, 0);	// Vertex Coord (Bottom Right)
		glTexCoord2f(1,1);	glVertex3f(0+shear, SQUARE_SIZE-shear, SQUARE_SIZE);// Vertex Coord (Top Right)
		glTexCoord2f(0,1);	glVertex3f(SQUARE_SIZE-shear, SQUARE_SIZE-shear, SQUARE_SIZE);	// Vertex Coord (Top Left)
		//LEFT SIDE
		glTexCoord2f(0,0);	glVertex3f(0, SQUARE_SIZE, 0);		// Vertex Coord (Bottom Left)
		glTexCoord2f(1,0);	glVertex3f(0, 0, 0);	// Vertex Coord (Bottom Right)
		glTexCoord2f(1,1);	glVertex3f(0+shear, 0+shear, SQUARE_SIZE);// Vertex Coord (Top Right)
		glTexCoord2f(0,1);	glVertex3f(0+shear, SQUARE_SIZE-shear, SQUARE_SIZE);	// Vertex Coord (Top Left)
	glEnd();
}

void DrawRocksAndWalls(Game &game) 
{
	for (int y = 0; y < game.getHeight(); y++) {
		for (int x = 0; x < game.getWidth(); x++) {
			glLoadIdentity();
			glTranslatef(x+0.5f,y+0.5f,0);
			if (game.cell(x,y) == CELL_WALL) {
				DrawRockOrWall(TEXTURE_WALL,0.1f);
			}//if
			else if (game.cell(x,y) == CELL_ROCK) {
				DrawRockOrWall(TEXTURE_ROCK);
			}//if
		}//for
	}//for
}


//enum Direction { UP = 2, DOWN = 3, LEFT = 4, RIGHT = 5 };
void Rotate(Direction dir) 
{
    GLfloat angle = 0.0f;
    switch (dir) {
        case UP:    angle = 180.0f;break;
        case DOWN:  angle =   0.0f;break;
        case LEFT:  angle = 270.0f;break;
        case RIGHT: angle =  90.0f;break;
        default: ;
    }//switch
    glRotatef(angle, 0.0f, 0.0f, 1.0f);
}

void DrawPlayers(Game &game) 
{
	for (Players::iterator p = game.players.begin(); p != game.players.end(); ++p) {
	    if (p->alive) {
		    glLoadIdentity();
		    glTranslatef(p->px+0.5f, p->py+0.5f, 0.6f);
		    Rotate(p->heading);
		    
		    glColor3f(10.f,1.0f,1.0f);  //HEAD
		    glBindTexture(GL_TEXTURE_2D, gametextures[TEXTURE_PLAYER]);		// Select Our Font Texture
		    gluSphere(q, 0.30, 12,12);	// sphere

		    glDisable(GL_TEXTURE_2D);

		    glColor3f(0.0f,0.0f,0.0f); // ANTENNA
		    glBegin(GL_LINES);
		      glVertex3f(0.0f,0.4f,0.4f);
		      glVertex3f(0,0,0.2f);
    	    glEnd();

		    glTranslatef(0.0f, 0.4f, 0.4f); // ANTENNA END-BALL
		    glColor3ubv(p->color.rgb);
		    gluSphere(q, 0.05f, 12,12);	// sphere

            glEnable(GL_TEXTURE_2D);
		}//if
	}//for
}

void DrawBombs(Game &game) 
{
	for (Bombs::iterator b = game.bombs.begin(); b != game.bombs.end(); ++b) {
		glLoadIdentity();
		glTranslatef(b->pos.x+0.5f, b->pos.y+0.5f, 0.5);
		GLfloat factor = 0.75f + GLfloat (abs((globals.getGameTimer() % 1000)-500) / 2000.0);
		glScalef(factor, factor, factor);
		glColor3f(1.0f,1.0f,1.0f);
		glBindTexture(GL_TEXTURE_2D, gametextures[TEXTURE_BOMB]);		// Select Our Font Texture
		gluSphere(q, 0.30, 12,12);	// sphere

        glDisable(GL_TEXTURE_2D);

		glColor3f(0.0f,0.0f,0.0f);

        // 0=bomb placed,...,1=bomb explosion
	    GLfloat btime = (globals.getGameTimer() - b->time) / (GLfloat)game.BOMBTIMEOUT;
	    
		glBegin(GL_LINES);
		    glVertex3f(-0.3f*(1-btime),0.3f*(1-btime),0.4f*(1-btime));
		    glVertex3f(0,0,0.3f);
    	glEnd();

    	glPointSize(2);
	    glBegin(GL_POINTS);
	    ColorType fcolors[] = { 
	        ColorType(255,0,0),ColorType(255,255,0),ColorType(255,169,70)
	    };
    	for (int i = 0; i < 3; i++) {
		    int r1 = (int(rand()) % 10) - 5;
		    int r2 = (int(rand()) % 10) - 5;
		    glColor3ubv(fcolors[int(rand()) % 4].rgb);
		    glVertex3f(
		        -0.3f+(r1*0.01f) +0.2f*btime,
		        0.3f+(r2*0.01f) -0.2f*btime,
		        0.4f -0.1f*btime);
        }//for
   	    glEnd();
	    glEnable(GL_TEXTURE_2D);
	}//for
}

void DrawPowerups(Game &game) 
{
    const float TexSize = 0.8f;
	for (PowerUps::iterator p = game.powerups.begin(); p != game.powerups.end(); ++p) {
		glLoadIdentity();
		glTranslatef(p->pos.x+0.1f, p->pos.y+0.1f, 0.2f);
		glColor3f(1.0f,1.0f,1.0f);
		glBindTexture(GL_TEXTURE_2D, poweruptextures[p->type]);
		glBegin(GL_QUADS);
			//FRONT
			glTexCoord2f(0,0);	glVertex3f(0,0,0);		// Vertex Coord (Bottom Left)
			glTexCoord2f(1,0);	glVertex3f(TexSize,0,0);	// Vertex Coord (Bottom Right)
			glTexCoord2f(1,1);	glVertex3f(TexSize,TexSize,0);// Vertex Coord (Top Right)
			glTexCoord2f(0,1);	glVertex3f(0,TexSize,0);	// Vertex Coord (Top Left)
		glEnd();
    }//for
}
void DrawExpFlame(int strength, int state)
{
    glPushMatrix();
    glBindTexture(GL_TEXTURE_2D, gametextures[TEXTURE_EXPLODE_M+state]);
	for (int i = 1; i < strength; i++) {
    	glTranslated(0,1,0);
    	glBegin(GL_QUADS);
		    glTexCoord2f(0,0);	glVertex3f(-0.5f,-0.5f,-0.2f);		// Vertex Coord (Bottom Left)
		    glTexCoord2f(1,0);	glVertex3f(+0.5f,-0.5f,-0.2f);	// Vertex Coord (Bottom Right)
		    glTexCoord2f(1,1);	glVertex3f(+0.5f,+0.5f,-0.2f);// Vertex Coord (Top Right)
		    glTexCoord2f(0,1);	glVertex3f(-0.5f,+0.5f,-0.2f);	// Vertex Coord (Top Left)
		glEnd();
	}//for
   	glTranslated(0,1,0);
	if (strength > 0) {
        glBindTexture(GL_TEXTURE_2D, gametextures[TEXTURE_EXPLODE_E+state]);
    	glBegin(GL_QUADS);							// Use A Quad For Each Character
	        glTexCoord2f(0,0);	glVertex3f(-0.5f,-0.5f,-0.2f);		// Vertex Coord (Bottom Left)
	        glTexCoord2f(1,0);	glVertex3f(+0.5f,-0.5f,-0.2f);	// Vertex Coord (Bottom Right)
	        glTexCoord2f(1,1);	glVertex3f(+0.5f,+0.5f,-0.2f);// Vertex Coord (Top Right)
	        glTexCoord2f(0,1);	glVertex3f(-0.5f,+0.5f,-0.2f);	// Vertex Coord (Top Left)
		glEnd();
    }//if
    glPopMatrix();
}

void DrawXBombs(Game &game) 
{
	for (Bombs::iterator b = game.xbombs.begin(); b != game.xbombs.end(); ++b) {
		glColor3f(1.0f,0.5f,0.0f);
		int state = b->data[0] & 1;
		glLoadIdentity();
		glTranslatef(b->pos.x+0.5f, b->pos.y+0.5f, 0.5f);

        glColor4f(1.0f,1.0f,1.0f,1.0f);
        glBindTexture(GL_TEXTURE_2D, gametextures[TEXTURE_EXPLODE_C+state]);
    	glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
    	glEnable(GL_BLEND);
    	glBegin(GL_QUADS);	// EXPLOSION CENTER
		    glTexCoord2f(0,0);	glVertex3f(-0.5f,-0.5f,-0.2f);		// Vertex Coord (Bottom Left)
		    glTexCoord2f(1,0);	glVertex3f(+0.5f,-0.5f,-0.2f);	// Vertex Coord (Bottom Right)
		    glTexCoord2f(1,1);	glVertex3f(+0.5f,+0.5f,-0.2f);// Vertex Coord (Top Right)
		    glTexCoord2f(0,1);	glVertex3f(-0.5f,+0.5f,-0.2f);	// Vertex Coord (Top Left)
		glEnd();

/*    	int str;
		int f;
		str = 0;            // UP
		for (f = 1; f <= b->data[UP]; f++) {
		    if (game.cell(b->pos.x,b->pos.y+f) == CELL_EMPTY) { str = f; } else { break; }
		}//for
*/		DrawExpFlame(b->data[UP], state);
/*		str = 0;            // LEFT
		for (f = 1; f <= b->strength; f++) {
		    if (game.cell(b->pos.x-f,b->pos.y) == CELL_EMPTY) { str = f; } else { break; }
		}//for
*/		glRotatef(90,0,0,1);
		DrawExpFlame(b->data[LEFT], state);
/*		str = 0;            // DOWN
		for (f = 1; f <= b->strength; f++) {
		    if (game.cell(b->pos.x,b->pos.y-f) == CELL_EMPTY) { str = f; } else { break; }
		}//for
*/		glRotatef(90,0,0,1);
		DrawExpFlame(b->data[DOWN], state);
/*		str = 0;            // RIGHT
		for (f = 1; f <= b->strength; f++) {
		    if (game.cell(b->pos.x+f,b->pos.y) == CELL_EMPTY) { str = f; } else { break; }
		}//for
*/		glRotatef(90,0,0,1);
		DrawExpFlame(b->data[RIGHT], state);
		
    	glDisable(GL_BLEND);
/*      glDisable(GL_TEXTURE_2D);
//		glBindTexture(GL_TEXTURE_2D, gametextures[TEXTURE_WHITE]);		// Select Our Font Texture

		glPushMatrix();
		glScalef(factor*2+1, 1, 1);
		if ((b->strength >> XTIMERBITS) & 1) {
		    glColor3f(255,255,0);
		} else {
		    glColor3f(255,0,0);
		}
		gluSphere(q, 0.50, 12, 12);	// sphere

		glPopMatrix();
		glScalef(1, factor*2+1, 1);
		gluSphere(q, 0.50, 12, 12);	// sphere
        glEnable(GL_TEXTURE_2D);
*/

	}//for
}


//float z = 0;
int DrawGameScene(Game &game)
{

	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);	// Clear The Screen And The Depth Buffer

	glDisable(GL_BLEND);
	glEnable(GL_DEPTH_TEST);

	glMatrixMode(GL_PROJECTION);						// todo move to initialization
	glLoadIdentity();									
	gluPerspective(35, (GLfloat)globals.width/(GLfloat)globals.height, 1, 50);
	glTranslatef(GLfloat(-game.getWidth()/2.0),GLfloat(-game.getHeight()/2.0),GLfloat(-game.getWidth()*1.5f));

	glMatrixMode(GL_MODELVIEW);
	glLoadIdentity();

//	glPointSize(12);glBegin(GL_POINTS);glVertex3f(0,0,1);glEnd();


	DrawFloor(game);
    DrawTimer(game);
	DrawPowerups(game);
	DrawRocksAndWalls(game);
	DrawPlayers(game);
	DrawBombs(game);
	DrawXBombs(game);

	return true;										// Keep Going
}

