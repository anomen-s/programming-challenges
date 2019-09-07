#ifndef benc_h
#define benc_h

#include <stdlib.h>

#include "db.h"

typedef struct {
	char *buffer;
	size_t length;
	size_t capacity;
} TBENCDATA, *BENCDATA;


BENCDATA benc_create_int(long i);
BENCDATA benc_create_string(const char* str);
BENCDATA benc_create_hash(InfoHash hash);


BENCDATA benc_list_create();
BENCDATA benc_list_add(BENCDATA list, BENCDATA value);
BENCDATA benc_list_close(BENCDATA list);

BENCDATA benc_dict_create();
BENCDATA benc_dict_str_add(BENCDATA dict, const char *key, BENCDATA value);
BENCDATA benc_dict_hash_add(BENCDATA dict, InfoHash hash, BENCDATA value);
BENCDATA benc_dict_close(BENCDATA dict);


void benc_free(BENCDATA data);

#endif
