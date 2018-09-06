#include "stdio.h"
#include "string.h" // pouzivame strlen()


/*
    Napsat funkci char *strreplace(char *kde, char *co, char *čím), která v řetězci kde nahradí všechny výskyty řetězce co řetězcem čím. Funkce vrací pointer kde.

    To vše musí fungovat bez dodatečného bufferu, tj. není možné úlohu vyřešit tak, že si vedle naalokuju dost místa, procházím kde a generuju postupně nový řetězec, jehož pointer pak vracím.

    Uživatel, který funkci volá, musí zaručit, že v kde je naalokováno dost místa.
*/

// funkce pro kopirovani p znaku
// upravena pro kopirovani prekryvajicich se bloku
char *strxcpy(char *kam, char *start, int p) {   
 char *dest = kam;
 if (kam != start) {
    if (kam < start) {
        while (p > 0) {
            *kam++ = *start++;
            p--;
        }//while
    } else {
        kam+=p-1;
        start+=p-1;
        while (p > 0) {
            *kam-- = *start--;
            p--;
        }//while
    }//if/else
 }//if
 return dest;
}

typedef struct tagSTRREPDATA {
 char   *co;
 char   *cim;
 int    delta;
 int    l_co;
 int    l_cim;
} STRREPDATA, *PSTRREPDATA;

void strrep(char *kde, char *kam, PSTRREPDATA data) 
{
   char *src;
   char *dest;
   char *start = kde;
   int p = 0;
   while (*kde) {  // prochazime retezec jde dokud nenajdeme podretezec 'co'
     src = kde;    // ... pak presuneme blok prev vyskytem a nahradime 'co' 'cim'
     dest = data->co; // ... a zavolame strrep() rekurzivne na zbytek  (nebo v obracenem poradi v zavislosti na data->delta)
     while ((*src == *dest) && *src) {  
       src++;           // najdeme prvni vyskyt podretezce
       dest++; 
     }//while
     if ((*src == *dest) || !(*dest)) {   // prvni podminka plati pokud 'co' lezi na konci
                                          // druha pokud substr lezi uvnitr
       if ((data->delta >= 0))  // pokud nahrazujeme delsim retezcem musime postupovat od konce retezce
         strrep(src, kam + p + data->l_cim, data); 
       strxcpy(kam, start, p);            // presuneme blok pred nalezenym vyskytem 'co'
       strxcpy(kam + p, data->cim, data->l_cim); // zkopirujeme 'cim' pres 'co'
       if ((data->delta < 0))   // nahrazujeme kratsim retezcem - rekurzi provedeme az na konec
         strrep(src, kam + p + data->l_cim, data);
       return;
     }//if
     kde++;
     p++;
   }//while
   p++;                    // zkopirujeme posledni blok v retezci 
   strxcpy(kam, start, p); // (od konce posledniho vyskytu podretezce az po NULL)
   return;
}

char *strreplace(char *kde, char *co, char *cim) // cim > co
{
  STRREPDATA data;              
  data.cim = cim;
  data.co = co;
  data.l_cim = strlen(cim);
  data.l_co = strlen(co);
  data.delta = data.l_cim - data.l_co;

  if (*co) strrep(kde, kde, &data); // pokud je co != ""
  return kde;
}



char buffer[100] = "abcdefghijcdAAABBBcdZZZcd";

int main(int argc, char* argv[])
{
  printf("%s\n\n", buffer);
  printf("%s\n", strreplace(buffer,"cd","XXX"));
  printf("%s\n", strreplace(buffer,"X","cd"));

  getc(stdin);
  return 0;
}
