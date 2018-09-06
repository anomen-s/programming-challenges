#ifndef logger_h
#define logger_h

#include <string>
#include <stdarg.h>


#define FPS_COUNTERS 6

class Logger {
public:
	static const Logger* getInstance();
	void log(const char *) const;
	void log(const std::string &) const;
	void log(const char *, int) const;
	void log(const char *, double) const;
	void log(const char *, const char *) const;
    void log(const char *, const std::string) const;
	void logf(const char *fmt, ...) const;
	void updateFPS(int) const;
	int  getFPS(int) const;
private:
    mutable int fpsCounter[FPS_COUNTERS];
    mutable int lastFPS[FPS_COUNTERS];
    mutable unsigned int fpsStart[FPS_COUNTERS];
	Logger();
	virtual ~Logger();
	static const Logger* instance;

};

extern const Logger* logger;

#endif
