// prj040311.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include "conio.h"
#include "string.h"



int porovnej(char *src, char *dest) 
{
	while ((*src == *dest) && *src) { src++;dest++; }
	return (*src  - *dest);
}

char *podretezec(char *s, char *subs )
{
   char * src;
   char * dest;
   for ( ; *s ;s++) {
     src = s;
	 dest = subs;
     while ((*src == *dest) && *src) {
		 src++;
		 dest++; 
	 }
     if ((*src == *dest) || !(*dest)) {   // prvni podminka plati pokud substr lezi na konci
		 return s;                        // druha pokud substr lezi uvnitr nebo je ""
	 }
   }
   return(0);
}

int main(int argc, char* argv[])
{
	char x1[] = "textf";
	char x2[] = "ext";
	//printf("Hello World!\n");
	printf("porovnej:  %i == %i \r\n",porovnej(x1,x2),strcmp(x1,x2));

    printf("%s == %s \n", podretezec(x1,x2), strstr(x1,x2));  // podretezec(co,kde)


	//getch();
	return 0;
}

