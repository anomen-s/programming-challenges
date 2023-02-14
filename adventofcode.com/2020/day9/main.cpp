#include <stdio.h>

#include <iostream>
#include <vector>
#include <set>
#include <cstdint>
#include  <algorithm>

using namespace std;

/**
 * Analyze run in integer sequence.
 */

int64_t find_in_window(const vector<int64_t> &msg, size_t curr, size_t startup) {
  set<int64_t> avail;
  for (size_t i = 1; i <= startup; i++)  {
    avail.insert(msg[curr - i]);
  }
  for (size_t i = 1; i <= startup; i++)  {
    // cout << "checking " << i << " for " << curr << endl;
    int64_t a = msg[curr] - msg[curr - i];
    if (avail.count(a) > 0) {
      // cout << "got " << curr << " = " << msg[curr] << endl;
      return -1;
    }
  }
  return msg[curr];
}

int64_t find_sum(const vector<int64_t> &msg, int64_t c) {

  for (size_t s = 0; s < msg.size()-1; s++)  {
    int64_t sum = msg[s];
    int64_t vmin = msg[s];
    int64_t vmax = msg[s];
    size_t e = s;
    while ((sum < c) && (e < (msg.size()-1))) {
      e++;
      sum += msg[e];
      vmin = min(vmin, msg[e]);
      vmax = max(vmax, msg[e]);
    }
    if (sum == c) {
      return vmin + vmax;
    }
  }
  return 0;
}

void process_file(bool final, size_t startup) {
  char filename[] = "input.sample";
  if (final) {
    filename[5] = '\0';
  }

  FILE *fptr = fopen(filename, "r");
  if (fptr == NULL)
    throw runtime_error(string("File not found: ") + filename);

  vector<int64_t> msg;
  char buffer[20];
  while (!feof(fptr)) {
    if (fgets(buffer, sizeof(buffer)-1, fptr)) {
      msg.push_back(atoll(buffer));
    }
  }

  int64_t part1 = 0;
  for (size_t i = startup; i < msg.size(); i++)  {
    int64_t p1 = find_in_window(msg, i, startup);
    if (p1 > 0) {
      part1 = p1;
    }
  }

  int64_t part2 = find_sum(msg, part1);

  fclose(fptr);

  cout << "Result: \t" << part1 << "\t" << part2 << endl;
}

int main() {
  cout << "*** Sample ***\n" << "Expected:\t127\t62" << endl;
  process_file(false, 5);
  cout << "*** Final ****\n" << "Expected:\t400480901\t67587168" << endl;
  process_file(true, 25);
}
