#include <string>
#include <iostream>
#include <fstream>
#include <vector>
#include <set>
#include <regex>
#include <algorithm>

using namespace std;

/*
 * 3D/4D Game of Life
 */


struct Coord {
    const int x;
    const int y;
    const int z;
    const int w;

    bool operator<(const Coord &other) const {
        if (x < other.x) return true;
        if (x > other.x) return false;
        if (y < other.y) return true;
        if (y > other.y) return false;
        if (z < other.z) return true;
        if (z > other.z) return false;
        return w < other.w;
    }
    Coord operator+(const Coord &other) const {
        return {(x + other.x), (y + other.y), (z + other.z), (w + other.w)};
    }
};

struct State {
 int iteration;
 long radius;
 int d;
 set<Coord> data;

  void activate(const Coord &coord) {
      data.insert(coord);
  }

  void activate(int x, int y, int z, int w) {
      data.insert({x, y, z, w});
  }

  long count() {
    return data.size();
  }
};

int count_neigh(const State &state, const Coord &coord);

void print_state(const State &state, int z, int w) {
  cout << "plane: " << z << "/" << w << endl;
  for (int y = -state.radius; y < state.radius;y++) {
    for (int x = -state.radius; x < state.radius;x++) {
      cout << (state.data.count({x,y,z,w}) > 0 ? '#' : '.');
    }
    cout << endl;
  }
}

///////////////////////////////////////
// part 1
///////////////////////////////////////

vector<Coord> build_neighbours3() {
  vector<Coord> result;
  for (int x = -1; x <= 1; x++)
    for (int y = -1; y <= 1; y++)
      for (int z = -1; z <= 1; z++)
        if (x | y | z)
          result.push_back({x,y,z,0});
  return result;    
}

void simulate_step3(const State &state, State &target) {

  target.radius = state.radius+1;
  target.iteration = state.iteration+1;
  target.d = state.d;
  target.data.clear();

  int radius = target.radius;
  for (int x = -radius; x <= radius; x++)
    for (int y = -radius; y <= radius; y++)
      for (int z = -radius; z <= radius; z++) {
        Coord coord = {x,y,z,0};
        int n = count_neigh(state, coord);
        if ((n == 3) || ((n == 2) && (state.data.count(coord) > 0))) {
          target.activate(coord);
        }
      }
}


long simulate3(const State &start, int count) {

  State state1 = start;
  state1.d = 3;
  State state2;

  State *prev = &state1;
  State *next = &state2;

  for (int i = 0; i < count; i++) {
    // print_state(*prev, 0);
    simulate_step3(*prev, *next);
    cout << next->count() << "..." << flush;
    // cout << "sim " << i << " from " << prev->count() << " to " << next->count() << endl;
    State *tmp = prev;
    prev = next;
    next = tmp;
  }
  cout << "|" << endl;
  return prev->count();
}



///////////////////////////////////////
// part 2
///////////////////////////////////////

vector<Coord> build_neighbours4() {
  vector<Coord> result;
  for (int x = -1; x <= 1; x++)
    for (int y = -1; y <= 1; y++)
      for (int z = -1; z <= 1; z++)
        for (int w = -1; w <= 1; w++)
        if (x | y | z | w)
            result.push_back({x,y,z,w});
  return result;    
}

void simulate_step4(const State &state, State &target) {

  target.iteration = state.iteration+1;
  target.d = state.d;
  target.data.clear();


  // checking only neighbourhood of active cells
  // (it's much faster then checking whole space)
  for (const Coord &c : state.data) {
    int radius = 1;
    for (int x = -radius; x <= radius; x++)
      for (int y = -radius; y <= radius; y++)
        for (int z = -radius; z <= radius; z++)
          for (int w = -radius; w <= radius; w++) {
            Coord coord = c + Coord({x,y,z,w});
            if (target.data.count(coord) == 0) {
              int n = count_neigh(state, coord);
              if ((n == 3) || ((n == 2) && (state.data.count(coord) > 0))) {
                target.activate(coord);
              }
            }
          }
  }
}

long simulate4(const State &start, int count) {

  State state1 = start;
  state1.d = 4;
  State state2;

  State *prev = &state1;
  State *next = &state2;

  for (int i = 0; i < count; i++) {
    // for (int z = -1;z < 2; z++)
    //   print_state(*prev, z, 1);
    simulate_step4(*prev, *next);
    cout << next->count() << "..." << flush;
    // cout << "sim " << i << " from " << prev->count() << " to " << next->count() << endl;
    State *tmp = prev;
    prev = next;
    next = tmp;
  }
  cout << "|" << endl;
  return prev->count();
}

///////////////////////////////////////
// main
///////////////////////////////////////

const vector<Coord> NEIGH[] = {{}, {}, {}, build_neighbours3(), build_neighbours4()};

int count_neigh(const State &state, const Coord &coord) {
  int r = 0;
  for (const auto &n : NEIGH[state.d]) {
    r += (state.data.count(coord + n) > 0);
  }
  return r;
}

void process_file(bool final) {

  ifstream ifs(final ? "input" : "input.sample", ifstream::in);


  State state = {0, 6, 0, {}};

  string buffer;
  int line = 0;
  while (!ifs.eof()) {
    getline(ifs, buffer);
    if (buffer.length() > 0) {
      for (size_t col = 0; col < buffer.length(); col++) {
        if (buffer[col] == '#') {
          state.activate(col-4,line-4,0,0);
        }
      }
    }
    line++;
  }
  ifs.close();

  auto part1 = simulate3(state, 6);
  auto part2 = simulate4(state, 6);

  cout << "Result: \t" << part1 << "\t" << part2 << endl;
}

int main() {
  cout << "*** Sample ***" << endl << "Expected:\t112\t848" << endl;
  process_file(false);
  cout << "*** Final ****" << endl << "Expected:\t317\t1692" << endl;
  process_file(true);
  return 0;
}
