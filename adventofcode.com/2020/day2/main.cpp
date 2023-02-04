#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <cstdio>
#include <iostream>

typedef struct {
  char len[10];
  int len_lo;
  int len_hi;
  char letter[4];
  char pass[100];
} TPASSREC, *PASSREC;

int count_char(PASSREC rec) {
  int i;
  int count = 0;
  for (i = 0; rec->pass[i]; i++) count += (rec->pass[i] == rec->letter[0]);
  return count;
}

int is_valid1(PASSREC rec) {
  int cnt = count_char(rec);
  return (rec->len_lo <= cnt) && (rec->len_hi >= cnt);
}

int is_valid2(PASSREC rec) {
  int m1 = (rec->pass[rec->len_lo - 1] == rec->letter[0]);
  int m2 = (rec->pass[rec->len_hi - 1] == rec->letter[0]);
  return m1 != m2;
}

void parse_rec(PASSREC rec) {
  char *sep = strchr(rec->len, '-');
  sep[0] = 0;
  rec->len_lo = atoi(rec->len);
  rec->len_hi = atoi(sep + 1);
}

void process_file(int final) {
  FILE *fptr = fopen(final ? "input" : "input.sample", "r");
  if (fptr == NULL) {
    printf("Error!");
    exit(1);
  }
  int valid1 = 0;
  int valid2 = 0;
  while (!feof(fptr)) {
    PASSREC rec = new TPASSREC;
    fscanf(fptr, "%9s %3s %199s", rec->len, rec->letter, rec->pass);
    if (strlen(rec->pass)) {
      parse_rec(rec);
      valid1 += is_valid1(rec);
      valid2 += is_valid2(rec);
      // std::cout << rec->len_lo << "-" << rec->len_hi << "x " << rec->letter
      // << " " << rec->pass << " -> " << valid << "\n";
    }
  }
  std::cout << "Valid(" << final << "): " << valid1 << "\t" << valid2 << "\n";
  fclose(fptr);
}

int main(int argc, char *argv[]) {
  process_file(false);
  process_file(true);
  return 0;
}
