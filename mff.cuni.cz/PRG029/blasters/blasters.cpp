#include <windows.h>		// Header File For Windows
#include <stdio.h>			// Header File For Standard Input/Output
#include <string>			// Header File For Standard Input/Output
#include <gl/gl.h>			// Header File For The OpenGL32 Library
#include <gl/glu.h>			// Header File For The GLu32 Library
#include "gl/glpng.h"

#include "blasters.h"
#include "globals.h"
#include "glinit.h"
#include "glgame.h"
#include "game.h"
#include "gltext.h"
#include "gltools.h"
#include "menu.h"
#include "net.h"
#include "keyb.h"
#include "ai.h"
#include "logger.h"

using namespace std;

LRESULT CALLBACK WndProc(	HWND	hWnd,			// Handle For This Window
							UINT	uMsg,			// Message For This Window
							WPARAM	wParam,			// Additional Message Information
							LPARAM	lParam)			// Additional Message Information
{
	switch (uMsg)									// Check For Windows Messages
	{
		case WM_ACTIVATE:							// Watch For Window Activate Message
		{
			globals.active = (!HIWORD(wParam));     // Check Minimization State
			return 0;								// Return To The Message Loop
		}
		case WM_SYSCOMMAND:							// Intercept System Commands
		{
			switch (wParam)							// Check System Calls
			{
				case SC_SCREENSAVE:					// Screensaver Trying To Start?
				case SC_MONITORPOWER:				// Monitor Trying To Enter Powersave?
				return 0;							// Prevent From Happening
			}
			break;									// Exit
		}
		case WM_CLOSE:								// Did We Receive A Close Message?
		{
			PostQuitMessage(0);						// Send A Quit Message
			return 0;								// Jump Back
		}
		case WM_KEYDOWN:							// Is A Key Being Held Down?
		{
			globals.keys[wParam] = true;					// If So, Mark It As true
			return 0;								// Jump Back
		}
		case WM_KEYUP:								// Has A Key Been Released?
		{
			globals.keys[wParam] = false;					// If So, Mark It As false
			return 0;								// Jump Back
		}
		case WM_SIZE:								// Resize The OpenGL Window
		{
			ResizeGLScene(LOWORD(lParam),HIWORD(lParam));  // LoWord=Width, HiWord=Height
			return 0;								// Jump Back
		}
		case WM_MOUSEMOVE:
		{
//			fwKeys = wParam;        // key flags 
			globals.mousex = LOWORD(lParam);  // horizontal position of cursor 
			globals.mousey = HIWORD(lParam);  // vertical position of cursor 
		}
	}

	// Pass All Unhandled Messages To DefWindowProc
	return DefWindowProc(hWnd,uMsg,wParam,lParam);
}


int ProcessMessages(int sleep)
{
	MSG	msg;										// Windows Message Structure
	static int idle;

	while (PeekMessage(&msg,NULL,0,0,PM_REMOVE))	// Is There A Message Waiting?
	{
		idle = 0;
		if (msg.message==WM_QUIT)				// Have We Received A Quit Message?
		{
			return false;							// If So done=true
		}
		else									// If Not, Deal With Window Messages
		{
//			TranslateMessage(&msg);				// Translate The Message
			DispatchMessage(&msg);				// Dispatch The Message
		}
	}//while
	idle++;
//	if (idle > 10) { SleepEx(sleep, true); }

	if (globals.keys[VK_F11])				// Is F1 Being Pressed?
	{
		globals.keys[VK_F11]=false;			// If So Make Key false
		KillGLWindow();						// Kill Our Current Window
		globals.fullscreen=!globals.fullscreen;// Toggle Fullscreen / Windowed Mode
		if (!CreateGLWindow(SCREEN_WIDTH,SCREEN_HEIGHT,SCREEN_BITS)) { return false; }	// Quit If Window Was Not Created
	}//if F11

	if (globals.keys[VK_F12])				// Is F1 Being Pressed?
	{
		return false;
	}
	return true;

}

bool GetPlayerName(int player) 
{
	std::string name;
	if (player == LOCALPLAYER1) {
		name = globals.player1;
		if (gltGetStr("Player 1:", name)) {
			globals.player1 = name;
			return true;
		}//if
	} else {
		name = globals.player2;
		if (gltGetStr("Player 2:", name)) {
			globals.player2 = name;
			return true;
		}//if
	}//ifelse
	return false;

}

bool Beep(int freq) 
{
	Beep(freq,100);
	return true;
}

bool Exit(int r) 
{
    exit(r);
    return false;
}

bool SetupControls(int keyid)
{
    Controls* c;
    string title = "Player ";
    if ((keyid & PLAYER_BIT) == LOCALPLAYER1) {
        c = &globals.p1controls;
        title.append("1: ");
    }//if
    else {
        c = &globals.p2controls;
        title.append("2: ");
    }//else
    if (keyid & KEY_BIT(KEY_LEFT)) { gltGetChar(title.append("LEFT"), c->left); }//if
    if (keyid & KEY_BIT(KEY_RIGHT)) { gltGetChar(title.append("RIGHT"), c->right); }//if
    if (keyid & KEY_BIT(KEY_UP)) { gltGetChar(title.append("UP"), c->up); }//if
    if (keyid & KEY_BIT(KEY_DOWN)) { gltGetChar(title.append("DOWN"), c->down); }//if
    if (keyid & KEY_BIT(KEY_FIRE)) { gltGetChar(title.append("FIRE"), c->fire); }//if
    //TODO:
    return true;
}

/*********************************************************************
***************  SERVER
***********************************************************************/
bool sendPlayerList(Game& game) 
{
    string list = COMMAND_PLAYERLIST " \r\n";
    for (Players::iterator p = game.players.begin(); p != game.players.end();++p) {
        list.append(
            strprintf(COMMAND_PLAYER " %s %i %i %i \r\n",
                encode(p->name).c_str(), 
                (int)p->pid, 
                (int)p->score, 
                (int)p->ping));
    }//for
    return SendToClients(list.c_str());
}

void showWinnerMessage(Game& game) {
    int alivePlayers = 0;
    string winner = "";
    for (Players::iterator pi = game.players.begin(); pi != game.players.end(); ++pi){
        if (pi->alive) { 
            alivePlayers++;
            winner = pi->name;
        }//if
    }
    if (alivePlayers == 1) {
        winner = "Winner is: " + winner;
    }//if
    else { winner = "No winner."; }
    gltMessageBox("Game over",winner);
}

// event handler for menu "new game"
bool StartGame(int)
{
    bool acceptRemote = true;
    bool done = false;
    DWORD pingTimer = 0;
    string pingCode = "---";
    
    SetUpListener(globals.defaultPort);
    gConnections.clear();

	Game game(17,11); //replace with players screen
	Player p1(Player::PT_LOCAL1, game.newPID());
	game.players.push_back(p1);
	Player p2(Player::PT_LOCAL2, game.newPID());
	game.players.push_back(p2);

	while (!done) { //main cycle

        if (AcceptConnections()) { // accept new clients
            if (game.players.size() >= 4) {
                KickUnacceptedClients("Full game.");
            } 
            else if (acceptRemote) {
                while (true) {
                    PID newPID = game.newPID();
                    if (AcceptNewPlayer(newPID)) {//send pids
                        Player rp = Player(Player::PT_REMOTE, newPID);
                        game.players.push_back(rp);
                    } else {
                        break;
                    }
                }//while
                sendPlayerList(game);
            } else {
                KickUnacceptedClients("Local game.");
            }
        }//if

        Players::iterator p = game.players.begin(); 
        while (p != game.players.end()) {
            bool gotoNext = true;
            CommandStruct cmd;
            if (p->type() == Player::PT_REMOTE) {
                while (readCommandFromPlayer(p->pid, cmd)) {
                    if (cmd.cmd == COMMAND_HELLO) {
                        p->name = decode(cmd.strparam);
                        sendPlayerList(game);
                        break;
                    }//if
                    if (cmd.cmd == COMMAND_EXIT) {
                        p->removePlayer();
                        p = game.players.erase(p);
                        sendPlayerList(game);
                        gotoNext = false;
                        break;
                    }//if
                    if (cmd.cmd == COMMAND_PONG) {
                        if (cmd.strparam == pingCode) {
                            p->ping = globals.getGameTimer() - pingTimer;
                        }//if
                    }//if
                    if (cmd.cmd == COMMAND_PING) {
	                    string ping = COMMAND_PONG " " + cmd.strparam + " \r\n";
	                    SendToClients(ping.c_str());
                        break;
                    }//if
                }//while
            }//if
            if (gotoNext) { ++p; }
        }//while
        
        globals.updateGameTimer();
        if ((pingTimer+2000) < globals.getGameTimer()) {  //PING test
           pingTimer = globals.getGameTimer();
           pingCode = strprintf("S%i", (int)rand());
           SendToClients(strprintf(COMMAND_PING " %s \r\n",pingCode.c_str()).c_str());
        }//if
        
	    if (!ProcessMessages()) { done = true; }

   	    if ((!DrawGameStats(game)) || testkey(VK_ESCAPE))	{// Active?  Was There A Quit Received?
   	        done = true;
   	    } else { 
            SwapBuffers(globals.hDC);			// Swap Buffers (Double Buffering)
   	    }//if/else

	    if(testkey('N')) {
            acceptRemote = !acceptRemote;
	    }//if

    	if(testkey('A')) {
            Player aip = Player(Player::PT_REMOTE, game.newPID(), aiPlayerName(game));
            game.players.push_back(aip);
            sendPlayerList(game);
	    }//if
	    
    	if(testkey('1')) { // REMOVE 1st local player
    	    for (Players::iterator pi = game.players.begin(); pi != game.players.end(); ++pi) {
    	        if (pi->type() == Player::PT_LOCAL1) {
    	            game.players.erase(pi);
    	            break;
    	        }//if
    	    }//for
	        sendPlayerList(game);
        }//if
    	if(testkey('2')) { // REMOVE 2nd local player
    	    for (Players::iterator pi = game.players.begin(); pi != game.players.end(); ++pi) {
    	        if (pi->type() == Player::PT_LOCAL2) {
    	            game.players.erase(pi);
    	            break;
    	        }//if
    	    }//for
	        sendPlayerList(game);
        }//if
	    if(testkey(VK_RETURN)) {
            if (game.players.size() > 1) {
	            game.init();
                game.randomBoard(30, 20);
                game.sendInitData();
	            ServerGame(game);
                clearKeyBuffer(); // clear pressed keys flags
	            showWinnerMessage(game);
                clearKeyBuffer(); // clear pressed keys flags
            } else {
                //NOT ENOUGH PLAYERS
                gltMessageBox("Cannot start game", "Not enough players");
            }//if/else
        }//if
    }//while
    CloseGameConnections();
    return true;
}

// server game code !!!!!
bool ServerGame(Game &game)
{
	bool done = false;
    bool controlChange = true;
	while(!done)									// Loop That Runs While done=false
	{
		if (!ProcessMessages()) { return false; }
        // LOCAL PLAYERS
		controlChange = controlChange || game.playerControls(); // read keys
		
        // AI PLAYERS
        aiControl(game);
        // REMOTE PLAYERS.
        if (AcceptConnections()) {
            KickUnacceptedClients("Game in progress."); // don't accept new clients during game
        }//if
        game.remotePlayerControls();
        
        logger->updateFPS(1);
		if (globals.updateGameTimer()) {
	        logger->updateFPS(0);
            if (!game.updateGameState(controlChange)) { 
                done = true; 
            }
            controlChange = false;
            game.broadcastGameStateChange(); //send to clients
		}//if

		if (globals.active) {
            if ((!DrawGameScene(game)) || globals.keys[VK_ESCAPE]) {// Active?  Was There A Quit Received?
				return false;						// ESC or DrawGLScene Signalled A Quit
            } else {                                // Not Time To Quit, Update Screen
				SwapBuffers(globals.hDC);			// Swap Buffers (Double Buffering)
			}//if/else
		}//if active

	}//while !done*/
	return true;
}
/*********************************************************************
***************  CLIENT
***********************************************************************/
// event handler for menu "join game"
bool JoinGame(int)
{
    string server = "";
    bool done = false;
    CommandStruct cmd;
    if (!gltGetStr("Enter server address:", server)) {
        return true;
    }//if
    Game game(server.c_str(), globals.defaultPort);
    clearKeyBuffer();

    DWORD pingTimer = 0;
    string pingCode = "---";
    PID localpid = 0;

	while (!done) {
	    if (!clientConnection.ReadData()) {
	        gltMessageBox("Connection error", LastWinSockError());
	        done = true;
	    }//if

	    while (clientConnection.readCommandFromBuffer(cmd)) {
	        if(cmd.cmd == COMMAND_ACCEPT) {
	            localpid = cmd.intparams[0];
	            string pname = COMMAND_HELLO " " + encode(globals.player1) + " \r\n";
	            clientConnection.WriteData(pname.c_str());
	        }//if
	        else if(cmd.cmd == COMMAND_REJECT) {
	            gltMessageBox("Access denied", decode(cmd.strparam));
	            done = true;
	        }//if
	        else if (cmd.cmd == COMMAND_PLAYERLIST) {
	            game.players.clear();
	        }//if
	        else if (cmd.cmd == COMMAND_PLAYER) {
	            if (localpid == cmd.intparams[0]) {
    	            game.players.push_back(Player(Player::PT_LOCAL1, cmd.intparams[0], decode(cmd.strparam).c_str(), cmd.intparams[1]));
	            } else {
    	            game.players.push_back(Player(Player::PT_REMOTE, cmd.intparams[0], decode(cmd.strparam).c_str(), cmd.intparams[1]));
	            }//if/else
	        }//if
	        else if (cmd.cmd == COMMAND_PONG) {
	            if (cmd.strparam == pingCode) {
	                Player& localP = game.findByPID(localpid);
	                localP.ping = globals.getGameTimer() - pingTimer;
	            }
	        }//if
	        else if (cmd.cmd == COMMAND_PING) {
	            string ping = COMMAND_PONG " " + cmd.strparam + " \r\n";
	            clientConnection.WriteData(ping.c_str());
	        }//if
	        else if (cmd.cmd == COMMAND_EXIT) {
	            gltMessageBox("Server shutdown.","");
                done = true;
	        }//if
	        else if (cmd.cmd == COMMAND_GAME) {
                if (game.findByPID(localpid).pid != 0) { // pid test
    	            playSound(SOUND_BEEP);
    	            game.init();
	                game.recvBoard(cmd.strparam.c_str(), cmd.intparams[0], cmd.intparams[1]);
                    if (!ClientGame(game)) { done = true; }
                    clearKeyBuffer(); // clear pressed keys flags
                    showWinnerMessage(game);
                    clearKeyBuffer(); // clear pressed keys flags
                }//if
                else {
                    gltMessageBox("Could'n start game","Missing player ID");
                    return true;
                }
            }//if
	    }//while

        globals.updateGameTimer();
        if ((pingTimer+2000) < globals.getGameTimer()) {  //PING test
           pingTimer = globals.getGameTimer();
           pingCode = strprintf("X%i",(int)rand());
           clientConnection.WriteData(strprintf(COMMAND_PING " %s \r\n", pingCode.c_str()).c_str());
        }//if
	    
	    if (!ProcessMessages()) { done = true; }

   	    if ((!DrawGameStats(game)) || testkey(VK_ESCAPE))	{// Active?  Was There A Quit Received?
   	        done = true;
   	    } else { 
		    SwapBuffers(globals.hDC);			// Swap Buffers (Double Buffering)
   	    }//if/else
    }//while
    clientConnection.WriteData(COMMAND_EXIT " \r\n");
    CloseGameConnections();
    return true;
}


bool ClientGame(Game &game)
{
	bool done = false;

	while(!done)									// Loop That Runs While done=false
	{
//	    logger->log("client: ", (int)GetTickCount());
		if (!ProcessMessages()) { return false; }//if

        if (game.playerControls()) { // read keys
            game.sendControlsToServer();
        }//if
		//parse server response
        if (!game.recvGameState()) { done = true; }

        logger->updateFPS(1);
        if (globals.updateGameTimer()) {
            logger->updateFPS(0);
            if (!game.updateGameState()) { done = true; }
		}//if

        if (globals.active) {
			if ((!DrawGameScene(game)) || globals.keys[VK_ESCAPE])	// Active?  Was There A Quit Received?
			{
				return false;						// ESC or DrawGLScene Signalled A Quit
			}
			else									// Not Time To Quit, Update Screen
			{
				SwapBuffers(globals.hDC);			// Swap Buffers (Double Buffering)
			}
		}//if active

	}//while !done*/
	return true;
}


int WINAPI WinMain(	HINSTANCE	hInstance,			// Instance
					HINSTANCE	hPrevInstance,		// Previous Instance
					LPSTR		lpCmdLine,			// Command Line Parameters
					int			nCmdShow)			// Window Show State
{

	globals.initGlobals();
#ifdef _DEBUG
	globals.fullscreen = false;
#endif
	pngSetStandardOrientation(true);
    srand((unsigned int)GetTickCount());
	pngSetStencil(0,0,0);

    if (!InitKeyboard()) { 
        errorMsg("File not found: ./data/keys.txt");
        return 0; 
    }
    if (!InitWinSock()) { 
        errorMsg("WinSock initialization failed");
        return 0; 
    }
    aiInit();
    SoundInit();
	if (!CreateGLWindow(SCREEN_WIDTH,SCREEN_HEIGHT,SCREEN_BITS)) { 
        errorMsg("couldn't create OpenGL window");
        return 0; 	// Quit If Window Was Not Created
    }
	gltInitFonts();
	glGameInit();

/*    DWORD x,y;
    BOOL z;
    GetSystemTimeAdjustment(&x,&y,&z);*/
    //SetSystemTimeAdjustment(50072, true);

	ShowMainMenu();

	// Shutdown
    SoundFinish();
	glGameDestroy();
	gltDeleteFonts();
	KillGLWindow();									// Kill The Window
	CleanupWinSock();

	return (0);//msg.wParam);							// Exit The Program
}
