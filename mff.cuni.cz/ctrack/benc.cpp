#include <string.h>
#include <stdio.h>

#include "benc.h"
#include "error.h"
#include "str.h"

static void benc_append(BENCDATA benc, const char *data, int length) 
{
	if (benc->capacity <= (benc->length+length)) {
		benc->capacity = 2*benc->capacity + length;
		benc->buffer = (char*)realloc(benc->buffer, benc->capacity);
	}//if
	memcpy(&(benc->buffer[benc->length]), data, length);
	benc->length += length;
}

static void benc_append_benc(BENCDATA benc, BENCDATA data) 
{
	benc_append(benc, data->buffer, data->length);
	benc_free(data);
}

void benc_free(BENCDATA data)
{
	free(data->buffer);
	free(data);
}

static BENCDATA benc_new() 
{
	BENCDATA b = (BENCDATA)emalloc(sizeof(TBENCDATA));
	b->capacity = 512;
	b->length = 0;
	b->buffer = (char*)emalloc(b->capacity);
	return b;
}

BENCDATA benc_create_int(long i)
{
	BENCDATA b = benc_new();
	char r[20];
	itoa(i, r);
	benc_append(b, "i", 1);
	benc_append(b, r, strlen(r));
	benc_append(b, "e", 1);
	return b;
}

BENCDATA benc_create_string(const char* str)
{
	BENCDATA b = benc_new();
	int len = strlen(str);
	char r[20];
	itoa(len, r);
	benc_append(b, r, strlen(r));
	benc_append(b, ":", 1);
	benc_append(b, str, len);
	return b;
}

BENCDATA benc_create_hash(InfoHash hash)
{
	BENCDATA b = benc_new();
	benc_append(b, "20:", 3);
	benc_append(b, hash, 20);
	return b;
}

 //////////////// LIST  /////////////////////////////
 
BENCDATA benc_list_create()
{
	BENCDATA list = benc_new();
	benc_append(list, "l", 1);
	return list;
}

BENCDATA benc_list_add(BENCDATA list, BENCDATA value)
{
	benc_append_benc(list, value);
	return list;
}

BENCDATA benc_list_close(BENCDATA list)
{
	benc_append(list, "e", 1);
	return list;
}

//////////////  DICTIONARY  //////////////////////////////////

BENCDATA benc_dict_create()
{
	BENCDATA dict = benc_new();
	benc_append(dict, "d", 1);
	return dict;
}

BENCDATA benc_dict_str_add(BENCDATA dict, const char *key, BENCDATA value)
{
	benc_append_benc(dict, benc_create_string(key));
	benc_append_benc(dict, value);
	return dict;
}

BENCDATA benc_dict_hash_add(BENCDATA dict, InfoHash hash, BENCDATA value)
{
	benc_append(dict, "20:", 3);
	benc_append(dict, hash, 20);
	benc_append_benc(dict, value);
	return dict;
}

BENCDATA benc_dict_close(BENCDATA dict)
{
	benc_append(dict, "e", 1);
	return dict;
}
