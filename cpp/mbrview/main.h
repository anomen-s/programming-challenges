#ifndef main_h
#define main_h

#include <inttypes.h>

#define VERSION "0.1"


#define MBR_ID 0xAA55 // Little Endian

typedef struct {
    uint8_t  bootf; // 0x80 bootable
    uint8_t  s_head;
    uint16_t s_cs;
    uint8_t  fs;
    uint8_t  e_head;
    uint16_t e_cs;
    uint32_t lba_shift;
    uint32_t lba_size;
} pt_rec;
 
typedef struct {  // doesn't work due to alignment
    int8_t  code[0x1BE];
    pt_rec  parts[4];
    int8_t id[2];
} mbr;

#define TRUE 1
#define FALSE 0

#endif
