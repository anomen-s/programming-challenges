#include <string.h>
#include <stdio.h>
#include <ctype.h>

#include "str.h"
#include "error.h"

INT64 ntoh64(INT64 val)
{
    INT64 result;
    int i;
    for (i = 0; i < 8; i++) {
        ((char*)&result)[i] = ((char*)&val)[7 - i]; 
    }
    return result;
}

static int hexdigit(char d)
{
	if ((d >= '0') && (d <= '9')) {
		return (d - '0');
	}
	if ((d >= 'a') && (d <= 'f')) {
		return (d - 'a' + 10);
	}
	if ((d >= 'A') && (d <= 'F')) {
		return (d - 'A' + 10);
	}
	return -1;
}

char *itoa(int l, char *str)
{
    sprintf(str, "%i", l);
    return str;
}

char *str_trim(char *str)
{
    char *last;
    char *pos;
    while ((str[0] != '\0') && (isspace(str[0]))) { str++; }

    last = pos = str;
    while (pos[0] != '\0') {
      if (!isspace(pos[0])) {
        last = pos+1;
      }
      pos++;
        
    }//while
    last[0] = '\0';
    return str;
}

static const char digits[] = "0123456789ABCDEF";

char* hashtostr(InfoHash info_hash, char* buffer)
{
    int i;
    int o = 0;
    for (i = 0; i < 20; i++) {
        buffer[o++] = digits[(info_hash[i] >> 4) & 0xF];
        buffer[o++] = digits[(unsigned)info_hash[i] & 0x0F];
    }//for
    buffer[o] = '\0';
    return buffer;    
}

int strtohash(const char* s, char* buffer)
{
    int i, l, h;
    if (strlen(s) != 40) { return FALSE; }
    for (i = 0; i < 20; i+=2) {
		l=hexdigit(s[2*i+1]);
		h=hexdigit(s[2*i]);
		if ((l == -1) || (h == -1)) { return FALSE; }
		buffer[i] = (char)(l | (h << 4));
    }//for
    return TRUE;    
}

char* hexdump(const char* buffer, size_t len)
{
	char *result = (char*)emalloc(3*len+10);
    int i;
    int o = 0;
    for (i = 0; i < (int)len; i++) {
        result[o++] = digits[(buffer[i] >> 4) & 0xF];
        result[o++] = digits[buffer[i] & 0x0F];
        switch (i & 0xF) {
        	case 0x0F: result[o++] = '\n'; break;
        	case 0x07: result[o++] = '-'; break;
       		default: result[o++] = ' ';break;
        }//switch
    }//for
    result[o] = '\0';
    return result;
}

int urldecode(char *buffer)
{
	char *src = buffer;
	char *dest = buffer;
    int len = 0;
	while (*src != '\0') {
        switch (*src) {
            case  '+':
    	       *dest = ' ';
    	       src++;
               break;
            case '%':
    			if ((!isxdigit(src[1])) || (!isxdigit(src[2]))) { return -1; }
    			*dest = (char)(((hexdigit(src[1])) << 4) | (hexdigit(src[2])));
    			src = &src[3];
    			break;
            default:
                *dest = *src;
                src++;
		}//switch
		dest++;
        len++;
	}//while
	*dest = '\0';
	return len;
}


char *gettoken(char **src, const char *separator)
{
    char *result;
    char *s = *src;
    int i = 0;
    while ((s[i] != '\0') && (strchr(separator, s[i]) == NULL)) {
        i++;
    }//while
    result = (char*)emalloc(1+i);
    strncpy(result, s, i);
    result[i] = '\0';
    while ((s[i] != '\0') && (strchr(separator, s[i]) != NULL)) {
        i++;
    }//while
    *src = &s[i];
    return result;
}


/* -- replaced with standard function memcmp
int hashcmp(InfoHash h1, InfoHash h2)
{
    int i;
    for (i = 0; i < 20; i++)
        if (h1[i] != h2[i])
            return (h1[i] - h2[i]);
    return 0;
}
*/
