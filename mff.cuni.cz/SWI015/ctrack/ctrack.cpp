#include <sys/types.h>
#include <sys/stat.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <signal.h>
#include <pthread.h>
#include <time.h>

#include "error.h"
#include "server.h"
#include "threads.h"
#include "ctrack.h"
#include "config.h"
#include "db.h"
#include "str.h"

int c_control;

static const char syntax[] = "ctrack, BitTorrent Tracker Version " VERSION "\n"
"usage: ctrack [OPTIONS...] [INFOHASHES...]\n"
"\nOptions:\n"
" -h          print help\n"
" -V          print version number and exit\n"
" -v          verbose (print detailed log to stderr)\n"
" -q          not verbose\n"
" -p [port]   default port number\n"
" -t [port]   HTTP port number\n"
" -u [port]   UDP port number\n"
" -c [file]   configuration file\n"
" -d          run as daemon\n"
"\n"
;

void PrintSyntax(int exitcode)
{
    fprintf(stdout, "%s", syntax); 
    exit(exitcode);
}

int b_assign(int val, int min, int max, int *arg) 
{
  int ok = ((val >= min) && (val <= max));
  if (ok) {
      *arg = val;
  }//if
  else {
    errorm("Invalid argument value");
  }
  return ok;
}

int main(int argc, char *argv[])
{
    int done = FALSE;
    opterr = 0;

    //fprintf(stderr, "ctrack started.");
    c_control = C_RUN;

    srand((int)time(NULL));

	ErrorInit();    
    ConfigInit(); // initializes verbose; must be called before any output

   	ReadConfig(TRUE); // default loc.
    TorrentDBCreate();

    unsigned int p;
    while (!done) {
        switch (getopt(argc, argv, "+vqVhrdt:u:p:c:"))  { // + means "don't shuffle args"
            case '?': // invalid option
                PrintSyntax(1);
            case 'h': // help option
                PrintSyntax(0);
            case 'V':
            	printf("ctrack " VERSION "\n");
            	return 0;
                break;
            case 'v':
                SetConfigBool(CFG_VERBOSE, TRUE);
                log("Verbose mode");
                break;
            case 'q':
                SetConfigBool(CFG_VERBOSE, FALSE);
                log("Quiet mode");
                break;
            case 't':
                if (b_assign(atoi(optarg),1,65535,(int *)&p))
                    SetConfigUInt(CFG_HTTP_PORT, p);
                break;
            case 'u':
                if (b_assign(atoi(optarg),1,65535,(int *)&p))
                    SetConfigUInt(CFG_UDP_PORT, p);
                break;
            case 'p':
                if (b_assign(atoi(optarg),1,65535,(int *)&p))
                    SetConfigUInt(CFG_SERVER_PORT, p);
                break;
            case 'd':
                SetConfigBool(CFG_DAEMON, TRUE);
                break;
            case 'c': //config file
	            SetConfigString(CFG_CONFIG_FILE, optarg);
                ReadConfig(FALSE);
            	break;
            case -1:  //end of options
                done = TRUE;
                break;
            default:
                PrintSyntax(1);
                break;    
        }//switch
    }//while
    int i;
    for (i = optind; i < argc; i++) {
    	PTorrentInfo t;
    	char ibuffer[20];
    	if (strtohash(argv[i], ibuffer)) {
			NewTorrentInfo(&t, ibuffer);
		} else {
			errorm("Invalid hash: %s", argv[i]);
		}
    }//for

    //TODO:parse args
    //TODO:init torrent db

#ifdef DAEMON_SUPPORT
    if (GetConfigBool(CFG_DAEMON) == TRUE) {
    /* Our process ID and Session ID */
    pid_t pid, sid;

    /* Fork off the parent process */
    pid = fork();
    if (pid < 0) { exit(EXIT_FAILURE); }
    /* If we got a good PID, then we can exit the parent process. */
    if (pid > 0) { exit(EXIT_SUCCESS); }
    /* Change the file mode mask */
    umask(0);
        /* Create a new SID for the child process */
    sid = setsid();
    if (sid < 0) {
		errorm("setsid() failed: %s", str_error());
		exit(EXIT_FAILURE);
    }
    /* Change the current working directory */
    if ((chdir("/")) < 0) {
		errorm("chdir() failed: %s", str_error());
        exit(EXIT_FAILURE);
    }
    /* Close out the standard file descriptors */
    close(STDIN_FILENO);
    close(STDOUT_FILENO);
    close(STDERR_FILENO);

	if (daemon(TRUE, FALSE) != 0) 
        errorf(E_SYSTEM, "daemon() failed: %S", str_error());
    } else {
		extern int asdaemon;
		asdaemon = TRUE;
    }
#endif

    //SetupSignalHandlers
	sigset_t set;
	int sig;

    while (c_control == C_RUN) {
    	sigfillset(&set);
    	pthread_sigmask(SIG_SETMASK, &set, NULL);

        if (GetConfigBool(CFG_HTTP_SERVER)) { // HTTP server
	        if (SetUpListener())
    	        HTTPThreadInit();
	    }

	    if (GetConfigBool(CFG_UDP_SERVER)) { // UDP server
	        UDPThreadInit();
	    }

		//TODO: sigwait
		while (c_control == C_RUN) {
		    sigwait(&set, &sig);
			logf("Caught signal #%d", sig);
			switch (sig) {
				case SIGINT:
	                c_control = C_TERMINATE;
    	            log("Exitting...");
        	        break;
				case SIGHUP:
	                c_control = C_RESTART;
	                log("Restarting...");
                   	ReadConfig(FALSE);
	                break;
				case SIGSEGV:
	                c_control = C_TERMINATE;
    	            log("Exitting...");
			}//switch
		}//while
        ThreadsDestroy();
    	CloseTCPSocket();
    	CloseUDPSocket();

        if (c_control == C_RESTART) { c_control = C_RUN; }
    }//while

  	log("exit ");
    return ((sig==SIGINT) ? EXIT_SUCCESS : EXIT_FAILURE);
}

