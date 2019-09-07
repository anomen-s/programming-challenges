#ifndef config_h
#define config_h

enum ConfigID { 
	CFG_CONFIG_FILE, // location of configuration file
	CFG_TORRENT_FILE, // location of torrent db file
	CFG_DAEMON,
	CFG_SERVER_PORT, // server's default port number
	CFG_HTTP_PORT,
	CFG_UDP_PORT,
	CFG_HTTP_SERVER,
	CFG_UDP_SERVER,
	CFG_THREAD_INIT,// initial number of threads
	CFG_THREAD_ALLOC,// number of threads created when all existing threads are busy
	CFG_THREAD_MAX,// maximal number of threads
	CFG_THREAD_LIFETIME,
	CFG_VERBOSE, // be verbose
	CFG_ANNOUNCE_INTERVAL,// announce interval
	CFG_ALLOW_UPLOADS, //allow torrent uploads
	CFG_OPEN_DB
};

extern void ConfigInit();
extern int ReadConfig(int eignore);

extern int GetConfigInt(enum ConfigID);
extern int GetConfigBool(enum ConfigID);
extern unsigned int GetConfigUInt(enum ConfigID);
extern const char *GetConfigString(enum ConfigID);

extern void SetConfigInt(enum ConfigID id, int value);
extern void SetConfigUInt(enum ConfigID id, unsigned int value);
extern void SetConfigBool(enum ConfigID id, int value);
extern void SetConfigString(enum ConfigID id, const char *value);


#endif
