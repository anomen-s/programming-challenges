#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <assert.h>

#include "config.h"
#include "error.h"
#include "str.h"

enum ConfigDataType { 
    TYPE_STRING, 
    TYPE_INT, 
    TYPE_UINT, 
    TYPE_BOOL 
};

struct ConfigItem {
    enum ConfigID id;
    const char *name;
    enum ConfigDataType type;
    union {
        unsigned int ui;    // TYPE_UINT
        int si;             // TYPE_INT
        int b;              // TYPE_BOOL
        char *s;      // TYPE_STRING
    } val;
};

static const char DEFAULT_INIT[] = "/etc/ctrack.conf";
static const char DEFAULT_TORRENT_DB[] = "/tmp/ctrack-torrent-db";

static struct ConfigItem Configuration[] = {
    { CFG_CONFIG_FILE,      "configfile",       TYPE_STRING, 0 },
	{ CFG_TORRENT_FILE,		"torrentfile",		TYPE_STRING, 0 },
    { CFG_DAEMON,           "daemon",           TYPE_BOOL, FALSE },
    { CFG_SERVER_PORT,      "serverport",       TYPE_UINT, 6969 },
    { CFG_HTTP_PORT,        "tcpport",          TYPE_UINT, 0 },
    { CFG_UDP_PORT,         "udpport",          TYPE_UINT, 0 },
    { CFG_HTTP_SERVER,      "httpserver",       TYPE_BOOL, TRUE },
    { CFG_UDP_SERVER,       "udpserver",        TYPE_BOOL, TRUE },
    { CFG_THREAD_INIT,      "thread_init",      TYPE_UINT, 4 },
    { CFG_THREAD_ALLOC,     "thread_alloc",     TYPE_UINT, 4 },
    { CFG_THREAD_MAX,       "thread_max",       TYPE_UINT, 64 },
    { CFG_THREAD_LIFETIME,  "thread_lifetime",  TYPE_UINT, 30 },
    { CFG_VERBOSE,          "verbose",          TYPE_BOOL, FALSE },
    { CFG_ANNOUNCE_INTERVAL,"announce_interval",TYPE_UINT, 1800 },
    { CFG_ALLOW_UPLOADS,    "allow_uploads",    TYPE_BOOL, TRUE },
    { CFG_OPEN_DB,			"open_database", 	TYPE_BOOL, TRUE }
};

static const int cfg_items = sizeof(Configuration)/sizeof(ConfigItem);

static struct ConfigItem *GetItem(enum ConfigID, enum ConfigDataType);
static struct ConfigItem *GetItemByName(const char *name);

static int SetConfigStrValue(const char *name, const char *value);


void ConfigInit()
{
    // obtain address of verbose variable
    verbose = &((GetItem(CFG_VERBOSE, TYPE_BOOL))->val.b);

    announce_int = &((GetItem(CFG_ANNOUNCE_INTERVAL, TYPE_UINT))->val.ui);

    //TODO: remove in final:
    //*verbose = TRUE;

    // set default config file location
    GetItem(CFG_CONFIG_FILE, TYPE_STRING)->val.s = strdup(DEFAULT_INIT);
    GetItem(CFG_TORRENT_FILE, TYPE_STRING)->val.s = strdup(DEFAULT_TORRENT_DB);
}

int ReadConfig(int eignore)
{
    char buffer[512];
    char *nvalue;
    char *nname;
    FILE *cfgfile;
    int longline;

    cfgfile = fopen(GetConfigString(CFG_CONFIG_FILE), "r");
    if(cfgfile == NULL) {
        if (!eignore) { errorf(E_CONTINUE, "Cannot open file (%s)", str_error()); }
        return FALSE;
    }//if
    

    while (!feof(cfgfile)) {
        fgets(buffer, sizeof(buffer)-1, cfgfile);
        longline = (strchr(buffer, '\n') == NULL);
        nname=strtok(buffer, "=");
        if ((nname != NULL) && (strchr(nname,'#') == NULL)) { 
            nvalue = strtok(NULL, "#\n");
            if (nvalue != NULL) {
                nname = str_trim(nname);
                nvalue = str_trim(nvalue);
                logf("config: \"%s\": \"%s\"\n", nname, nvalue);
                if (!SetConfigStrValue(nname,nvalue)) {
                    errorf(E_CONTINUE, "Unknown configuration variable: %s", nname);
                } else {
                    // todo   
                }//else
            }//if
        }//if
        while (longline && (!feof(cfgfile))) {
            fgets(buffer, sizeof(buffer)-1, cfgfile);
            longline = (strchr(buffer, '\n') == NULL);
        }//while
    }//while
    
    if (fclose(cfgfile) != 0) {
        errorf(E_CONTINUE, "Failed to close config file (error: %s)", str_error());
    }
    return 0;
}

static int SetConfigStrValue(const char *name, const char *value)
{
    struct ConfigItem *it;
    it = GetItemByName(name);
    int i;
    if (it == NULL) { return FALSE; }
    switch (it->type) {
        case TYPE_STRING: 
            if (it->val.s != NULL) free(it->val.s);
            it->val.s = strdup(value);
            break;
        case TYPE_INT: 
            it->val.si = atoi(value);
            break;
        case TYPE_UINT:
            i = atoi(value);
            if (i > 0) { it->val.ui = i; }
                else { it->val.ui = 0; }
            break;
        case TYPE_BOOL:
            if (strcasecmp("true", value) == 0) {
                it->val.b = TRUE;
            } else if (strcasecmp("false", value) == 0) {
                it->val.b = FALSE;
            } else {
                it->val.b = (atoi(value) != 0); 
            }
            break;
    }//switch
    return TRUE;
}


static struct ConfigItem *GetItemByName(const char *name)
{
    int i;
    for (i = 0; i < cfg_items; i++) {
        if (strcasecmp(Configuration[i].name, name) == 0)
            return &Configuration[i];
    }//for
    return NULL;
}

static int look_id(const void *key, const void *val)
{
    enum ConfigID id = *(enum ConfigID *)key;
    struct ConfigItem *es = (struct ConfigItem*)val;

    return (id - es->id);
}

static struct ConfigItem *GetItem(enum ConfigID id, enum ConfigDataType dt)
{
    struct ConfigItem *it;

    it = (struct ConfigItem *)bsearch(&id, Configuration, cfg_items, sizeof(struct ConfigItem), look_id);
    assert(it != NULL);
    assert(it->type == dt);

    return it;
}

int GetConfigInt(enum ConfigID id)
{
    return (GetItem(id, TYPE_INT))->val.si;
}

unsigned int GetConfigUInt(enum ConfigID id)
{
    return (GetItem(id, TYPE_UINT))->val.ui;
}

const char *GetConfigString(enum ConfigID id)
{
    return (GetItem(id, TYPE_STRING))->val.s;
}

int GetConfigBool(enum ConfigID id)
{
    return (GetItem(id, TYPE_BOOL))->val.b;
}

void SetConfigBool(enum ConfigID id, int value)
{
    struct ConfigItem *it = GetItem(id, TYPE_BOOL);
    assert(it != NULL);
    it->val.b = value;
}

void SetConfigUInt(enum ConfigID id, unsigned int value)
{
    struct ConfigItem *it = GetItem(id, TYPE_UINT);
    assert(it != NULL);
    it->val.ui = value;
}

void SetConfigInt(enum ConfigID id, int value)
{
    struct ConfigItem *it = GetItem(id, TYPE_INT);
    assert(it != NULL);
    it->val.si = value;
}

void SetConfigString(enum ConfigID id, const char *value)
{
    struct ConfigItem *it = GetItem(id, TYPE_STRING);
    assert(it != NULL);
    if (it->val.s != NULL) {
        free(it->val.s);
    }//if
    it->val.s = strdup(value);
}
