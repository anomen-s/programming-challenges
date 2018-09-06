#include <stdio.h>
#include <stdlib.h>
#include <stdarg.h>
#include <errno.h>
#include <pthread.h>
#include <syslog.h>
#include <string.h>

#include "error.h"

int *verbose;
unsigned int *announce_int;
int asdaemon = FALSE;

static pthread_mutex_t print_mutex = PTHREAD_MUTEX_INITIALIZER;

int ErrorInit()
{
	openlog("ctrack", LOG_PID, LOG_USER);
	return TRUE;
}

static void error(int e, const char* msg)
{
    pthread_mutex_lock(&print_mutex);	
    if (asdaemon) {
		syslog(LOG_ERR, "%s", msg);
    } else {
	    fprintf(stderr, "Error: %s\n", msg);
	    if (e > E_CONTINUE) { fprintf(stderr, "DEPRECATED\n"); }
    }
    pthread_mutex_unlock(&print_mutex);	
    if (e > E_CONTINUE) {
        pthread_exit(NULL);
    }
}
void log(const char* msg)
{
    if (*verbose) {
        pthread_mutex_lock(&print_mutex);	
        if (asdaemon) {
			syslog(LOG_INFO, "%s", msg);
        } else {
	        fprintf(stderr, "Log: %s\n", msg);
        }
        pthread_mutex_unlock(&print_mutex);	
    }
}

void errorm(const char* fmt, ...)
{
    char *text;
    const int len = 500;
    va_list ap;
    va_start(ap, fmt);

    text = (char *)emalloc(len * sizeof(char));

    vsnprintf(text, len-1, fmt, ap);
    va_end(ap);
    error(E_CONTINUE, text);

    free(text);
}

void errorf(int e, const char* fmt, ...)
{
    char *text;
    const int len = 500;
    va_list ap;
    va_start(ap, fmt);

    text = (char *)emalloc(len * sizeof(char));

    vsnprintf(text, len-1, fmt, ap);
    va_end(ap);
    error(e, text);

    free(text);
}

void logf(const char *fmt, ...)
{
    if ((!(*verbose)) || (fmt == NULL)) { 
        return; 
    }
    char *text;
    const int len = 500;
    va_list ap;

    va_start(ap, fmt);

//  len = _vscprintf(fmt, ap)+1; // _vscprintf doesn't count terminating '\0'
    text = (char *)emalloc(len * sizeof(char));

    vsnprintf(text, len-1, fmt, ap);
    va_end(ap);
    log(text);

    free(text);
}

extern const char* str_error()
{
    return strerror(errno);
}

void *emalloc(size_t size)
{
    void *mem;
    mem = malloc(size);
    if (mem == NULL) {
        error(E_MEMORY, "Not enough memory.");
    }//if
    return mem;
}


