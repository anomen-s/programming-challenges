#include <stdio.h>

#include <cstring>
#include <iostream>
#include <sstream>
#include <vector>
#include <map>

using namespace std;

/*
 * Generate and search in integer sequence.
 */

long compute_seq(map<long, long> seq, long count) {
  long init = seq.size();
  long last = 0; // suppose init sequence has no duplicates
  for(long i = init+2; i <= count; i++) {
    if (seq.count(last) > 0) {
      long curr = i - 1 - seq[last];
      seq[last] = i - 1;
      last = curr;
    } else {
      seq[last] = i - 1;
      last = 0;
    }
  }
  return last;
}

///////////////////////////////////////
// main
///////////////////////////////////////

void trim(char* buffer) {
  char* lf = strchr(buffer, '\n');
  if (lf) *lf = 0;
  char* cr = strchr(buffer, '\r');
  if (cr) *cr = 0;
}

void process_file(bool final) {
  FILE *fptr = fopen(final ? "input" : "input.sample", "r");
  if (fptr == NULL)
    throw runtime_error("File not found");

  char buffer[100];

  while (fgets(buffer, sizeof(buffer)-1, fptr)) {
    trim(buffer);
    istringstream bufferstream(buffer);
    string s;
    map<long, long> seq;
    long line = 1;
    while (getline(bufferstream, s, ',')) {
      seq[stol(s)] = line++;
    }
    auto part1 = compute_seq(seq, 2020);
    auto part2 = compute_seq(seq, 30000000);
    cout << buffer << " -> \t" << part1 << ",\t" << part2 << endl;
  }

  fclose(fptr);
}

int main() {
  cout << "*** Sample ***" << endl << "Expected:\t436,1,10,27,78,438,1836\t175594,2578,3544142,261214,6895259,18,362" << endl;
  process_file(false);
  cout << "*** Final ****" << endl << "Expected:\t410\t238" << endl;
  process_file(true);
  return 0;
}
