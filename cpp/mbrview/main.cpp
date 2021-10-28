#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <assert.h>
#include <errno.h>

#include "main.h"
#include "plist.h"

static const char syntax[] = "mbrViewer Version " VERSION "\n"
"usage: mbrview [OPTIONS...] [file]\n"
"\nOptions:\n"
" -h          print this help\n"
" -V          print version number and exit\n"
" -v          verbose (print detailed log to stderr)\n"
" -q          not verbose\n"
" -s count    skip sectors\n"
" -t          print as table\n"
" -i          ignore errors\n"
"\n"
"This is free software. "
"There is NO warranty; not even for MERCHANTABILITY "
"or FITNESS FOR A PARTICULAR PURPOSE. \n"
"\n"
;


static int verbose = FALSE;
static int skip_sectors = 0;
static int as_table = FALSE;
static int ignore_errors = FALSE;

int main(int argc, char *argv[])
{
//    fprintf(stderr, "%i\n\n",sizeof(mbr));
    assert(sizeof(pt_rec) == 0x10);
//    assert(sizeof(mbr) == 0x200);
    
    int done = FALSE;
    opterr = 0;
    
    while (!done) {
        switch (getopt(argc, argv, "+vqVhs:ti"))  { // + means "don't shuffle args"
            case '?': // invalid option
                fprintf(stderr,"Unknown option: %c\n", (char)optopt);
                fprintf(stderr, "%s", syntax); 
                exit(EXIT_FAILURE);
            case 'h': // help option
                fprintf(stdout, "%s", syntax); 
                exit(EXIT_SUCCESS);
            case 'q':
                verbose = FALSE;
                break;
            case 'V':
            	fprintf(stdout, "mbrViewer " VERSION "\n");
                exit(EXIT_SUCCESS);
            case 'v':
                verbose = TRUE;
                break;
            case 's':
                skip_sectors = atoi(optarg);
                break;
            case 't':
                as_table = TRUE;
                break;
            case 'i':
                ignore_errors = TRUE;
                break;
            case -1:  //end of options
                done = TRUE;
                break;
            default:
                fprintf(stderr,"unexpected error while option parsing");
                break;
        }//switch
    }//while

    if ((argv[optind] != NULL) && (strcmp("-",argv[optind]) != 0)) {
        int fd = open(argv[optind], O_RDONLY);
        if (fd == -1) {
            fprintf(stderr,"Open failed: %s\n", strerror(errno));
            exit(EXIT_FAILURE);
        }//if
        if (dup2(fd, STDIN_FILENO) == -1) {
            fprintf(stderr, "Couldn't duplicate handle: %s\n", strerror(errno));
            exit(EXIT_FAILURE);
        }//if
    }
    
    uint8_t buff[0x200];
    for (int i = 0; i <= skip_sectors; i++) {
        switch (read(STDIN_FILENO, &buff, 0x200)) {
            case -1: 
                fprintf(stderr, "Read error: %s\n", strerror(errno));
                exit(EXIT_FAILURE);
            case 0x200: 
                break; //ok
            default:
                fprintf(stderr, "Unexpected end of file\n");
                exit(EXIT_FAILURE);
        }//if
    }//for
    if (verbose != FALSE) {
        fprintf(stderr, "Skipped %i sectors\n", skip_sectors);
    }

    if ((buff[0x1fe] != 0x55) || (buff[0x1ff] != 0xAA)) {
        fprintf(stdout, "Invalid Master Boot Sector identification!\n");
        if (ignore_errors == FALSE) { exit(EXIT_FAILURE); }
    }//if

    if (as_table == FALSE) {
        fprintf(stdout, "boot\tfile system\t    start\t    size\tstart CHS\tend CHS" "\n");
    }//if
    
//    int ptbase = 0x1be;
    for (int i = 0; i < 4; i++) {
        const pt_rec *part = (const pt_rec *)&buff[0x1be + 0x10*i];
//        int bflag = buff[ptbase+0];
//        int32_t lba_start = *(const int32_t*)(&buff[ptbase+8]);
//        int32_t lba_size = *(const int32_t*)(&buff[ptbase+12]);
        char cboot;
        switch (part->bootf) {
            case 0x80:  
                    cboot='B'; 
                    break;
            case 0x00:  
                    cboot='-'; 
                    break;
            default:    
                    cboot='?'; 
                    if (ignore_errors != FALSE) { 
                        fprintf(stderr, "Invalid bootflag %2x\n", part->bootf);
                    }
                    break;
        }//switch
        int sc = ((part->s_cs >> 8) & 0xFF) | ((part->s_cs << 2) & 0x300);
        int ss = (part->s_cs & 0x3F);
        int ec = ((part->e_cs >> 8) & 0xFF) | ((part->e_cs << 2) & 0x300);
        int es = (part->e_cs & 0x3F);
        const char *ptname = getpartname(part->fs);
        if (as_table == FALSE) {
            fprintf(stdout, "[%c]\t%-14s\t%10u\t%10u\t%4i:%i:%i\t%4i:%i:%i\n", 
                cboot, ptname, part->lba_shift, part->lba_size,
                sc, (int)part->s_head, ss, ec, (int)part->e_head, es);
        } else {
            fprintf(stdout, "%c:%02X:%s:%u:%u:%i:%i:%i:%i:%i:%i\n", 
                cboot, (int)part->fs, ptname, part->lba_shift, part->lba_size,
                sc, (int)part->s_head, ss, ec, (int)part->e_head, es);
        }
    }//for

    return EXIT_SUCCESS;
}
