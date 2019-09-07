#ifndef threads_h
#define threads_h

#include "server.h"

extern int ThreadInitCode();
extern int c_restart;

extern int UDPThreadInit(void);
extern int HTTPThreadInit(void);

// passes ccdata from server thread to one of worker threads
extern int WakeUpWorkerThread(struct ClientConnData *ccdata);

extern int ThreadsDestroy(void);

#endif

