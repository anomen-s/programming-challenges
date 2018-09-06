#include "logger.h"

#include <fstream>
//#include <ostream>
#include <windows.h>

using namespace std;

static ofstream loggerOutput;

const Logger* Logger::instance = NULL;

const Logger* Logger::getInstance()
{
	if (instance == NULL) {
		instance = new Logger();
	}//if
	return instance;
}

void Logger::log(const char *str) const
{
	loggerOutput << str << endl;
}

void Logger::log(const string &str) const
{
	loggerOutput << str << endl;
}

void Logger::log(const char *str, int i) const
{
	loggerOutput << str << " " << i << endl;
}

void Logger::log(const char *str, const char *str2) const
{
	loggerOutput << str << " " << str2 << endl;
}

void Logger::log(const char *str, const string str2) const
{
	loggerOutput << str << " " << str2 << endl;
}

void Logger::log(const char *str, double d) const
{
	loggerOutput << str << " " << d << endl;
}

void Logger::logf(const char *fmt, ...) const
{
	char text[512];// Ukládá øetìzec
	va_list ap;// Pointer do argumentù funkce
	if (fmt == NULL) { return; }// Byl pøedán text?
	va_start(ap, fmt);// Rozbor øetìzce
	vsprintf(text, fmt, ap);// Zamìní symboly za konkrétní èísla
	va_end(ap);// Výsledek je uložen v text
	log(text);
}

Logger::~Logger()
{
	loggerOutput.close();
}

Logger::Logger()
{
    memset(&fpsCounter, 0, sizeof(fpsCounter));
    memset(&lastFPS, 0, sizeof(lastFPS));
    memset(&fpsStart, 0, sizeof(fpsStart));
    
	loggerOutput.open("log.txt", ios::out);
}

/*************************************************/

void Logger::updateFPS(int i) const
{
    if ((fpsStart[i] + 5000) < GetTickCount()) {
        lastFPS[i] = (fpsCounter[i]*1000) / (GetTickCount() - fpsStart[i]);
        fpsStart[i] = GetTickCount();
        fpsCounter[i] = 0;
    }//if
    fpsCounter[i]++;
}
int  Logger::getFPS(int i) const
{
    return lastFPS[i];
}

/*************************************************/

const Logger* logger = Logger::getInstance();

