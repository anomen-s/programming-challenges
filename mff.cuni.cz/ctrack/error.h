#ifndef error_h
#define error_h

#include <stdlib.h>
#include <inttypes.h>


extern int *verbose;
extern unsigned int *announce_int;

#define C_RUN (0)
#define C_TERMINATE (2) // all threads should terminate
#define C_RESTART (1) // all threads should terminate
extern int c_control;

typedef int16_t INT16;
typedef int32_t INT32;
typedef int64_t INT64;

typedef uint16_t UINT16;
typedef uint32_t UINT32;
typedef uint64_t UINT64;


#ifndef TRUE
    #define TRUE (1)
#endif
#ifndef FALSE
    #define FALSE (0)
#endif

#ifndef SOCKET
	#define SOCKET int
#endif

#ifndef INVALID_SOCKET
	#define INVALID_SOCKET ((SOCKET)(-1))
#endif

#ifndef SOCKET_ERROR
	#define SOCKET_ERROR (-1)
#endif

// defines error number for recoverable errors
#define E_CONTINUE (0)
// error in network connection
#define E_SOCKETS (4)
// memory error
#define E_MEMORY (16)
// syscall or library function returned error
#define E_SYSTEM (17)
// input/output error
#define E_IO (18)
// internal error
#define E_INTERNAL (32)

extern void log(const char* msg);
extern void logf(const char *fmt, ...);

// prints error - same as errorf(E_CONTINUE,...)
extern void errorm(const char* fmt, ...);

// prints formatted error message
extern void errorf(int e, const char* fmt, ...);

extern void *emalloc(size_t size);

extern const char* str_error();

extern int ErrorInit();  

#endif

