#include <stdio.h>

#include <iostream>
#include <algorithm>

using namespace std;

/**
 * Compute seat ids and search for missing one.
 */

int compute_id(const char* seat) {
  int row = 0;
  for (int i = 0; i < 10; i++) {
    row = row * 2 + ((seat[i] == 'B') || (seat[i] == 'R'));
  }
  return row;
}

void process_file(bool final) {
  FILE *fptr = fopen(final ? "input" : "input.sample", "r");
  if (fptr == NULL) {
    printf("Error!");
    exit(1);
  }
  char buffer[100];
  int max_id = -1;
  bool occupied[1024] = {0};
  while (!feof(fptr)) {
    if (fgets(buffer, sizeof(buffer)-1, fptr)) {
      int id = compute_id(buffer);
      // cout << id << endl;
      max_id = max(max_id, id);
      occupied[id] = true;
    }
  }
  fclose(fptr);

  // part 1
  cout << "Result: \t" << max_id << "\t";

  // part 2
  for (size_t i = 1; i < (sizeof(occupied)/sizeof(bool))-1; i++) {
    if ((!occupied[i]) && occupied[i-1] && occupied[i+1]) {
      cout << i << endl;
    }
  }
  cout << endl;
}

int main() {
  cout << "*** Sample ***" << endl << "Expected:\t820" << endl;
  process_file(false);
  cout << "*** Final ****" << endl << "Expected:\t892\t625" << endl;
  process_file(true);
}
