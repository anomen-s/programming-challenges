// prj040422.cpp : Defines the entry point for the console application.
#include "stdafx.h"

//  25.4.2004

typedef struct tagUZEL {
    int a;
    tagUZEL *potomci[2]; 
} UZEL;

typedef struct tagSTROM {
    UZEL *koren;
} STROM;

bool Init(STROM *strom) {
    strom->koren = NULL;
    return true;
}

bool SearchNode(UZEL *u, int a) {
    if (!u) 
        return false;
    if (u->a == a) 
        return true;
    return SearchNode(u->potomci[u->a < a],a);
}

bool Search(STROM *s, int a) {
    return(SearchNode(s->koren,a));
}

void DestroyNode(UZEL *u) {
    if (u->potomci[0]) DestroyNode(u->potomci[0]);
    if (u->potomci[1]) DestroyNode(u->potomci[1]);
    free(u);
}

bool Destroy(STROM *strom) {
    if (strom->koren) DestroyNode(strom->koren);
    return true;
}

UZEL *CreateNode(int a) {
  UZEL *u;
  if (!(u = (UZEL *)malloc(sizeof(UZEL)))) return NULL;
  u->a = a;
  u->potomci[0] = NULL;
  u->potomci[1] = NULL;
  return u;
}

bool InsertNode(UZEL *u, int a) {
    if (u->a == a)
        return true;
    UZEL *potomek = u->potomci[u->a < a];
    if (potomek) 
        return InsertNode(potomek,a);
    else
        return ( (u->potomci[u->a < a] = CreateNode(a)) != NULL);
}

bool Insert(STROM *s, int a) {
    if (s->koren) 
        return InsertNode(s->koren, a);
    else
        return ((s->koren = CreateNode(a)) != NULL);      
}

int FindMax(UZEL *u) {
    while (u->potomci[1]) u = u->potomci[1];
    return u->a;
}

UZEL *RemoveNode(UZEL *u, int a) {
     UZEL *u1;
     if (!u) return NULL;
     if (u->a == a) {
         if (u->potomci[0]) {   // levy podstrom je neprazdny
            if (u->potomci[1]) {// ... pravy take
               u->a = FindMax(u->potomci[0]);
              u->potomci[0] = RemoveNode(u->potomci[0], u->a);
              return u;
            } else {     // .. pravy je prazdny- uzel u nahradime levym podstromem
              u1 = u->potomci[0];
              free(u);
              return u1;
            }//if/else
         } else {        // levy podstrom je prazdny - uzel u nahradime pravym podstromem
            u1 = u->potomci[1];
            free(u);
            return u1;
         }//if/else
     } else {
         u->potomci[u->a < a] = RemoveNode(u->potomci[u->a < a], a);
         return u;
     }//else
}

bool Remove(STROM *s, int a) {
    if (s->koren) 
        return ((s->koren = RemoveNode(s->koren, a)) != NULL);
    else 
        return true;
}

void PrintNode(UZEL *u, int indent) {
 if (!u) return;
 PrintNode(u->potomci[0],indent+4);
 for (int i = 0; i < indent; i++) 
    printf(" ");
 printf("%d\n", u->a);
 PrintNode(u->potomci[1],indent+4);
}

void Print(STROM *s) {
  PrintNode(s->koren, 0);
}

char boolstr[2][4] = { "ne", "ano" };

int _tmain(int argc, _TCHAR* argv[])
{
    STROM s1;
    int i;

    Init(&s1);
    printf("vlozime prvky: ");
    for (i = 1; i < 11; i++) { 
      printf("%d ",(i*7+i) % 13);
      Insert(&s1, (i*7+i) % 13); 
    }//for

    printf("\n---------------------------------------------\n");

    Print(&s1);
    printf("strom obsahuje 7: %s | 5: %s\n", boolstr[Search(&s1, 7)], boolstr[Search(&s1, 5)]);
    printf("---------------------------------------------\n");
    printf("odebereme: ");

    for (i = 1; i < 7; i++) {
      printf("%d ",(i*5+i) % 17);
      Remove(&s1, (i*5+i) % 17); 
    }//for
                   
    printf("\n---------------------------------------------\n");

    Print(&s1);

    printf("strom obsahuje 7: %s | 5: %s\n", boolstr[Search(&s1, 7)], boolstr[Search(&s1, 5)]);

    char c;scanf("%c",&c);
    return 0;
}

