#include <pthread.h>
#include <string.h>

#include "server.h"
#include "threads.h"
#include "error.h"
#include "config.h"
#include "http.h"


extern int AllocNewThreads(int);
static void *HTTPThreadProc(void *status_ptr);

#define STATUS_START (-1)
#define STATUS_BUSY  (-2)
#define STATUS_WAITING (-3)
#define STATUS_DEAD (-4)
#define STATUS_ERROR (-5)

static pthread_t udp_thread;
static pthread_t http_thread;

static pthread_t *t_id;     // only modified by main thread

static int t_num = 0;     // only modified by main thread
static int *t_status;    // synchronized access

static pthread_mutex_t req_mutex = PTHREAD_MUTEX_INITIALIZER;
static pthread_cond_t req_cond;

static struct ClientConnData *req_data;

static int CreateThread(pthread_t *id, void*(func)(void*), void* arg) 
{
    pthread_attr_t attr;
    int result;
    pthread_attr_init(&attr);
    pthread_attr_setdetachstate(&attr, PTHREAD_CREATE_DETACHED);
    result = pthread_create(id, &attr, func, arg);
    pthread_attr_destroy(&attr);
    return (result == 0);
}

int ThreadInitCode()
{
/*		sigset_t set;  // this code is probably unnecessary
		sigemptyset(&set);
		pthread_sigmask(SIG_BLOCK, &set, NULL);*/
		pthread_setcancelstate(PTHREAD_CANCEL_ENABLE, NULL);
		pthread_setcanceltype(PTHREAD_CANCEL_ASYNCHRONOUS, NULL);
		return TRUE;
}

int HTTPThreadInit(void)
{
    int i;

    log("HTTP threads initialization");
    pthread_cond_init(&req_cond, NULL);

    t_num = 0; // create worker threads

    t_id = (pthread_t *)emalloc(1 * sizeof(pthread_t));
    t_status = (int *)emalloc(1 * sizeof(int));

    i = GetConfigUInt(CFG_THREAD_INIT);
    logf("init threads %i (%i)", i, AllocNewThreads(i));

    // create http server thread
    if (CreateThread(&http_thread, HTTPServerMain, NULL) == FALSE) {
        errorm("Failed to create HTTP thread");
        return FALSE;
    }//if

    return TRUE;
}

int UDPThreadInit(void)
{
    log("UDP thread initialization");

    if (CreateThread(&udp_thread, UDPServer, NULL) == FALSE) {
        errorm("Failed to create UDP thread");
        return FALSE;
    }//if
    log("Created UDP thread");
    return TRUE;
}


// Creates new threads if neccessary.
int AllocNewThreads(int tcount)
{       
    int i;

    for (i = 0; i < t_num; i++) {
        if (t_status[i] == STATUS_WAITING) {
            logf("thread %i should be ready",i);
            return -1;
        }//if
    }//for

    int a_num = t_num + tcount;
    if (GetConfigUInt(CFG_THREAD_MAX) < (unsigned int)a_num) { 
        return -2;// max. number of threads reached
    }//if

    pthread_mutex_lock(&req_mutex);

    // reallocate array of thread objects
    pthread_t *a_id = t_id;
    int *a_status = t_status;
    t_id = (pthread_t *)emalloc(a_num * sizeof(pthread_t));
    t_status = (int *)emalloc(a_num * sizeof(int));
    memcpy(t_id, a_id, t_num * sizeof(pthread_t));
    memcpy(t_status, a_status, t_num * sizeof(int));
    free(a_id);
    free(a_status);

    int created = 0;
    for (i = t_num; i < a_num; i++) {
        t_status[i] = i;
        if (CreateThread(&t_id[i], HTTPThreadProc, (void *)&t_status[i]) == FALSE) {
            t_status[i] = STATUS_ERROR;
            errorm("Failed to create new thread");
        }//if
        else { 
            logf("Created thread %i", i);
            created++; 
        }//else
    }//for
    t_num = a_num;

    pthread_mutex_unlock(&req_mutex);

    return created;
}

int ThreadsDestroy(void)
{
	pthread_cancel(udp_thread);
	pthread_cancel(http_thread);

    // broadcast exit signal to worker threads
    pthread_mutex_lock(&req_mutex);
    req_data = NULL;
    pthread_cond_broadcast(&req_cond);
    pthread_mutex_unlock(&req_mutex);
    

    // TODO: kill http server thread
    // TODO: kill udp server thread

	// TODO: wait
	// TODO: destroy
    pthread_cond_destroy(&req_cond);
    pthread_mutex_destroy(&req_mutex);

	// TODO: wait and cancel remaining threads

    return TRUE;
}

int WakeUpWorkerThread(ClientConnData *ccdata)
{
    int t_new = AllocNewThreads(GetConfigUInt(CFG_THREAD_ALLOC));
    switch (t_new) { 
        case -2: 
            logf("thread limit reached");
            break;
        case -1:
            logf("idle threads available");
            break;
        case 0:
            errorf(E_CONTINUE, "Couldn't create new threads!");
            break;
        default:
            logf("Created new threads (result: %i).", t_new);
    }//switch
    pthread_mutex_lock(&req_mutex);
    req_data = ccdata;
    pthread_cond_signal(&req_cond); // wake up one thread
    pthread_mutex_unlock(&req_mutex);

    return TRUE;
}

// HTTP worker thread code
static void *HTTPThreadProc(void *status_ptr)
{    

    if (status_ptr == NULL) {
        errorm("Thread started with NULL parameter");
        return NULL;
    }//if

	ThreadInitCode();

    int lifetime = (int)GetConfigUInt(CFG_THREAD_LIFETIME);

    logf("Thread started");

    int *status = (int *)status_ptr;
    int tid = *status;
    struct ClientConnData ccdata;

    logf("Thread %i started", tid);

    while (c_control == C_RUN ) {    // wait for wake up

        *status = STATUS_WAITING;

        pthread_mutex_lock(&req_mutex);
        while (req_data == NULL) {

        	if (c_control != C_RUN) {
        		*status = STATUS_DEAD;
        		pthread_mutex_unlock(&req_mutex);
                logf("Thread %i exited", tid);
        		return NULL;
        	}//if

            pthread_cond_wait(&req_cond, &req_mutex);
        }//while

        memcpy(&ccdata, req_data, sizeof(struct ClientConnData));
        logf("thread %i accepted request", tid);

        //case ACTION_ACCEPT:
        req_data = NULL;
        *status = STATUS_BUSY;
        pthread_mutex_unlock(&req_mutex);
        HTTPMain(&ccdata);
        logf("thread %i completed task.", tid);
        
        if (lifetime > 0) {
           if ((--lifetime) <= 0) {
                *status = STATUS_DEAD;
                logf("Thread %i expired", tid);
                return NULL;
            }//if
        }//if

    }//while
    return NULL;
}
