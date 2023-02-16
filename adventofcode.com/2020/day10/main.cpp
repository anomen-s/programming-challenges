#include <stdio.h>

#include <iostream>
#include <vector>
#include <cstdint>
#include <string>
#include <algorithm>

using namespace std;

/**
 * Sort input and compute differencies between elements.
 */

int64_t compute_differences(const vector<int> &values) {

  int cnt1 = 0;
  int cnt3 = 0;
  // cout << "start" << cnt1 << " " << cnt3 << endl;
  for (size_t i = 1; i < values.size(); i++)  {
    int diff = values[i] - values[i-1];
    if (diff == 1) {
      cnt1++;
    } else if (diff == 3) {
      cnt3++;
    } else {
      throw runtime_error("Unexpected difference: " + to_string(diff));
    }
  }
  return cnt1 * cnt3;
}

long compute_arrangements(const vector<int> &values) {

  size_t s = values.size();
  vector<int64_t> tab;
  tab.resize(s+2, 0);
  tab[s-1] = 1;
  for (long i = s-2; i >= 0; i--) {
    int curr = values[i];
    for (int c = 1; c < 4; c++) {
      int next = values[i+c];
      if (next <= (curr + 3)) {
        tab[i] += tab[i+c];
      }
    }
    // cout <<  i << "(" <<values[i] << "): " << tab[i] << endl;
  }
  return tab[0];
}


void process_file(bool final, char part) {
  char filename[] = "input.sampleX";
  if (final) {
    filename[5] = '\0';
  } else {
    filename[12] = part;
  }

  FILE *fptr = fopen(filename, "r");
  if (fptr == NULL)
    throw runtime_error(string("File not found: ") + filename);

  vector<int> msg;
  char buffer[20];
  while (!feof(fptr)) {
    if (fgets(buffer, sizeof(buffer)-1, fptr)) {
      msg.push_back(atoi(buffer));
    }
  }

  fclose(fptr);

  // add 0 and last+3 as per design and sort list
  msg.push_back(0);
  sort(msg.begin(), msg.end());
  msg.push_back(msg[msg.size()-1]+3);

  int64_t part1 = compute_differences(msg);
  int64_t part2 = compute_arrangements(msg);

  cout << "Result: \t" << part1 << "\t" << part2 << endl;
}

int main() {
  cout << "*** Sample1 ***\n" << "Expected:\t35\t8" << endl;
  process_file(false, '1');
  cout << "*** Sample2 ***\n" << "Expected:\t220\t19208" << endl;
  process_file(false, '2');
  cout << "*** Final ****\n" << "Expected:\t2048\t1322306994176" << endl;
  process_file(true, 0);
}
