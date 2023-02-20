#include <stdio.h>

#include <cstring>
#include <iostream>
#include <sstream>
#include <vector>
#include <utility>
#include <cmath>

using namespace std;

/*
 * Compute timetables.
 * (1) Find first bus leaving after given timestamp.
 * (2) Find timestamp when buses start to leave one by one in 1-unit intervals, see https://en.wikipedia.org/wiki/Chinese_remainder_theorem
 */

///////////////////////////////////////
// part 1
///////////////////////////////////////


int64_t waiting_for_bus(const vector<int> &buses, long ts) {
  int64_t min_w = ts;
  int64_t score = 0;
  for (auto bus : buses) {
    int64_t w = bus - (ts % bus);
    // cout << bus << " : " << w << endl;
    if ((bus > 0) && (w < min_w)) {
        min_w = w;
        score = w * bus;
    }
  }
  return score;
}

///////////////////////////////////////
// part 2
///////////////////////////////////////

int64_t compute_m(const vector<vector<int64_t>> &congruences) {
  int64_t m = 1;
  for (const auto &c: congruences) {
    m *= c[0];
  }
  return m;
}

int64_t compute_inv_stupid(int64_t a, int64_t m) {

  // this would be slow for bigger numbers

  for (int64_t i = 1; i < m; i++) {
    if (((a*i) % m) == 1) {
      return i;
    }
  }
  throw runtime_error("Inversion not found, mod=" + to_string(m) + ", a=" + to_string(a));
}


int64_t compute_inv(int64_t a, int64_t m) {

  // https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm

  auto update = [](int64_t &target1, int64_t &target2, int64_t value1, int64_t value2)
  {
    target1 = value1;
    target2 = value2;
  };

  int64_t old_r = a, r = m;
  int64_t old_s = 1, s = 0;
  int64_t old_t = 0, t = 1;

  while (r != 0) {
      int64_t quotient = old_r / r;
      update(old_r, r, r, old_r - quotient * r);
      update(old_s, s, s, old_s - quotient * s);
      update(old_t, t, t, old_t - quotient * t);
  }
  return (m + old_s) % m;
}

int64_t solve_congruences(const vector<vector<int64_t>> &congruences) {

  int64_t M = compute_m(congruences);
  // cout << "M=" << M << endl;
  int64_t result = 0;

  for (const auto &congr: congruences) {
    int64_t m = congr[0];
    int64_t a = congr[1];
    int64_t z = M / m;
    int64_t y = compute_inv(z, m); // y = z**-1 (mod m)
    int64_t w = (y * z) % M; // w = y*z (mod m)
    int64_t x = a * w; // x = a * w
    result += x;
    // cout << "mod:" << m << " a:" << a << " z:" << z << " y:" << y <<  " w:" << w << " x:" << x << endl;
  }
  return result % M;
}

int64_t find_subsequent_departures(const vector<int> &buses) {

  // vector of <m{i}, a{i}>
  vector<vector<int64_t>> congruences;
  int64_t i = 0;
  for (auto bus: buses) {
    if (bus > 0) {
      int64_t a = (bus*i - i) % bus;
      congruences.push_back({bus, a});
    }
    i++;
  }
  return solve_congruences(congruences);
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
  vector<string> path;
  char buffer[500];
  long ts;
  vector<int> buses;
  if (fgets(buffer, sizeof(buffer)-1, fptr)) {
    ts = atol(buffer);
  } else {
    throw runtime_error("Read error");
  }
  if (fgets(buffer, sizeof(buffer)-1, fptr)) {
    trim(buffer);
    istringstream bufferstream(buffer);
    string s;
    while (getline(bufferstream, s, ',')) {
      if (s == "x")
        buses.push_back(-1);
      else
        buses.push_back(stoi(s));
    }
  } else {
    throw runtime_error("Read error");
  }

  fclose(fptr);

  auto part1 = waiting_for_bus(buses, ts);
  auto part2 = find_subsequent_departures(buses);

  cout << "Result: \t" << part1 << "\t" << part2 << endl;
}

void test() {
  cout << "*** TEST ***" << endl;
  vector<vector<int64_t>> data = {{11, 6}, {16, 13}, {21, 9}, {25, 19}};
  auto r = solve_congruences(data);
  cout << "exp: 89469, got: " << r << endl;
}


int main() {
  test();
  cout << "*** Sample ***" << endl << "Expected:\t295\t1068781" << endl;
  process_file(false);
  cout << "*** Final ****" << endl << "Expected:\t203\t905694340256752" << endl;
  process_file(true);
  return 0;
}
