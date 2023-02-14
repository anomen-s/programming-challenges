#include <stdio.h>
#include <string.h>

#include <iostream>
#include <algorithm>
#include <cstdint>

using namespace std;

/**
 * Compute number of characters present in (1) at least one line and (2) all lines in group.
 * Groups are separated by an empty line.
 */

// store number of members in group in this index
const size_t IDX_COUNTER = 256;

int sum_answers_any(const int yes_answers[]) {
    int yescnt = 0;
    for (int i = 'a'; i <= 'z'; i++) {
      yescnt += (yes_answers[i] > 0);
    }
    // cout << "count = " << yescnt << endl;
    return yescnt;
}

int sum_answers_all(const int yes_answers[]) {
    int yescnt = 0;
    for (size_t i = 'a'; i <= 'z'; i++) {
      yescnt += (yes_answers[i] == yes_answers[IDX_COUNTER]);
    }
    // cout << "count = " << yescnt << endl;
    return yescnt;
}

void process_file(bool final) {
  FILE *fptr = fopen(final ? "input" : "input.sample", "r");
  if (fptr == NULL) {
    printf("Error!");
    exit(1);
  }
  char buffer[200];
  int yes[IDX_COUNTER+1] = {0};
  int32_t sum1 = 0;
  int32_t sum2 = 0;
  while (!feof(fptr)) {
    if (fgets(buffer, sizeof(buffer)-1, fptr)) {
      if (buffer[0] >= 'a') {
        // process current line data
        for (size_t i = 0; i < strlen(buffer); i++) {
          yes[(size_t)buffer[i]]++;
        }
        yes[IDX_COUNTER]++;
      } else {
        // empty line -> compute number of answers
        sum1 += sum_answers_any(yes);
        sum2 += sum_answers_all(yes);
        memset(yes, 0, sizeof(yes));
      }
    }
  }
  sum1 += sum_answers_any(yes);
  sum2 += sum_answers_all(yes);
  fclose(fptr);

  cout << "Result: \t" << sum1 << "\t" << sum2 << endl;
}

int main() {
  cout << "*** Sample ***" << endl << "Expected:\t11\t6" << endl;
  process_file(false);
  cout << "*** Final ****" << endl << "Expected:\t6457\t3260" << endl;
  process_file(true);
}
