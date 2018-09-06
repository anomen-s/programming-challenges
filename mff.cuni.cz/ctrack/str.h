#ifndef str_h
#define str_h

#include "db.h"
#include "error.h"

extern char *itoa(int l, char *str);

extern char *str_trim(char *str);
//extern int hashcmp(InfoHash h1, InfoHash h2);

extern char* hashtostr(InfoHash info_hash, char* buffer);
extern int strtohash(const char* s, char* buffer);

// decodes url
// in-place
extern int urldecode(char *buffer);

// returns copy of first token in `src`
// modifies src to point to next token
extern char *gettoken(char **src, const char *separator);

extern char* hexdump(const char* buffer, size_t len);

extern INT64 ntoh64(INT64 val);

#define hton64 ntoh64 

#endif
