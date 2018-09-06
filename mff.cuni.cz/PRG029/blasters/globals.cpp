#include "globals.h"

#include <math.h>
//#include <mmsystem.h>
//#include <sstream>
#include "logger.h"

using namespace std;

Globals globals;


string strprintf(const char *fmt, ...)
{
	char text[512];
    va_list ap;
    if (fmt == NULL) { return ""; }
    va_start(ap, fmt);
    vsprintf(text, fmt, ap);
    va_end(ap);
    return string(text);
}

int ftoi(float f) 
{
	return (int)floor(f+0.5f);
}

long ftol(float f) 
{
	return (long)floor(f+0.5f); 
}


////////////////////////////////////////////////////

void errorMsg(char *msg) 
{
    logger->log("ERROR MESSAGE: ", msg);
	MessageBox(NULL,msg,"ERROR",MB_OK | MB_ICONEXCLAMATION);
}

////////////////////////////////////////////////////

static bool end;            // terminates sound thread
static int playsounds[SOUNDS_COUNT];   // someone wants to play sound

static char* sound_buffers[SOUNDS_COUNT];
static char* sound_files[SOUNDS_COUNT] = { 
    ".\\sound\\exp.wav",   
    ".\\sound\\beep.wav" };

bool SoundInit()
{
    for (int i = 0; i < SOUNDS_COUNT; i++) {
        sound_buffers[i] = NULL;
        HANDLE hFile = CreateFile(sound_files[i], 
            GENERIC_READ, FILE_SHARE_READ, NULL, OPEN_EXISTING,FILE_ATTRIBUTE_NORMAL, NULL);
        DWORD size2;
        DWORD size = GetFileSize(hFile, &size2);
        if ((size > 0) && (size < (1024*1024))) {
            sound_buffers[i] = new char[size | 0x8];
            if ((ReadFile(hFile, sound_buffers[i], size, &size2, NULL) == 0) || (size2 = 0)) {
                    delete[] sound_buffers[i];
                    sound_buffers[i] = NULL;
                    logger->logf("Failed to read sound file %i: %i", sound_files[i], (int)GetLastError());
            }//if/else
        } else {
            logger->log("Sound file too large");
        }
        CloseHandle(hFile);
    }//for
    end = false;
    DWORD ThreadId = 0;
    extern DWORD WINAPI SoundThread(LPVOID);
    return (CreateThread(NULL, 0, SoundThread, NULL, 0, &ThreadId) != NULL);
}

void SoundFinish()
{
    // skip memory deallocation, it's just waste of time
    end = true;
}


bool playSound(int sound)
{
    if ((sound >= 0) && (sound < SOUNDS_COUNT)) {
        playsounds[sound] = true;
    } else {
        logger->log("invalid sound number: ", sound);
    }//if/else
    return true;
}

DWORD WINAPI SoundThread(LPVOID) 
{
    DWORD nextsound = GetTickCount();
    while (!end) {
        while (nextsound > GetTickCount()) {
            SleepEx(10, true);
        }//while
        for (int i = 0; i < SOUNDS_COUNT;i++) {
            if (playsounds[i]) {
                if (sound_buffers[i] != NULL) {
                    PlaySound(sound_buffers[i], NULL, SND_MEMORY | SND_ASYNC);
                } else {
                    PlaySound(sound_files[i], NULL, SND_FILENAME | SND_ASYNC);
                }//if/else
            }//if
            playsounds[i] = false;
        }//for
        nextsound = GetTickCount() + 200;
    }//while
    return true;
}


