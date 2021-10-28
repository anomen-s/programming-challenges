#include "plist.h"

const char *getpartname(uint8_t num)
{
    switch (num) {
        case 0x00: return "unused";
		case 0x01: return "FAT12";
		case 0x02: return "Xenix root";
		case 0x03: return "Xenix usr";
		case 0x04: return "FAT16";
		case 0x05: return "extended PT";
		case 0x06: return "BIGDOS";
		case 0x07: return "NTFS/HPFS";
		case 0x08: return "OS2/AIX";
		case 0x0B: return "FAT32";
		case 0x0C: return "FAT32 LBA";
		case 0x0E: return "FAT16 LBA";
		case 0x0F: return "extended PT (FAT32)";
		case 0x24: return "NEC DOS";
		case 0x38: return "THEOS3.2";
		case 0x39: return "THEOS4";
		case 0x3A: return "THEOS4";
		case 0x3B: return "THEOS4 ext";
		case 0x3C: return "Part.Magic";
		case 0x40: return "Venix 286";
		case 0x42: return "Linux swap";
		case 0x50: return "DM r/w";
		case 0x51: return "DM r/o";
        case 0x82: return "Linux swap";
        case 0x83: return "Linux ext2";
        default: return "unknown";
    }//switch
    
}
