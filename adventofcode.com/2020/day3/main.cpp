#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <iostream>
#include <vector>

void trim(char* buffer) {
  char* lf = strchr(buffer, '\n');
  if (lf) *lf = 0;
  char* cr = strchr(buffer, '\r');
  if (cr) *cr = 0;
}

long walk(std::vector<char*> &lines, int incx, int incy) {
  int x = 0;
  int cnt = 0;
  int width = strlen(lines[0]);
  for (int i = 0; i < (int) lines.size(); i += incy) {
    cnt += (lines[i][x % width] == '#');
    x += incx;
  }
  return cnt;
}

void process_file(bool final) {
  FILE *fptr = fopen(final ? "input" : "input.sample", "r");
  if (fptr == NULL) {
    printf("Error!");
    exit(1);
  }
  std::vector<char*> lines;
  while (!feof(fptr)) {
    char* buffer = new char[100];
    if (fgets(buffer, 99, fptr)) {
      trim(buffer);
      lines.push_back(buffer);
    }
  }
  fclose(fptr);

  long p1 = walk(lines, 3, 1);
  long p2 = walk(lines, 1, 1) * p1 * walk(lines, 5, 1) * walk(lines, 7, 1) * walk(lines, 1, 2);
  std::cout << "Result: \t" << p1 << "\t" << p2 << "\n";
}

int main() {
  std::cout << "*** Sample ***\n" << "Expected:\t7\t336\n";
  process_file(false);
  std::cout << "*** Final ****\n" << "Expected:\t178\t3492520200\n";
  process_file(true);
  return 0;
}
