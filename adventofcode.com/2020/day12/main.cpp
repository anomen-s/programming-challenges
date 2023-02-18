#include <stdio.h>

#include <cstring>
#include <iostream>
#include <vector>
#include <utility>
#include <cmath>

using namespace std;

/*
 * Follow movement instructions.
 *
 */

// position with optional direction
typedef struct {
  long x;
  long y;
  int d;
} POS;

///////////////////////////////////////
// part 1
///////////////////////////////////////

void rotate(POS &pos, char rotate_dir, int rotate_deg) {
  int diff = rotate_deg/90;
  if (rotate_dir == 'L') 
    diff = -diff;
  pos.d = (4 + pos.d + diff) % 4;
}

void move(POS &pos, int dir, int num) {

  static const vector<pair<int, int>> dirs = {
    {1,0}, // E
    {0,1}, // S
    {-1,0},// W
    {0,-1} // N
  };

  const auto &d = dirs[dir];
  pos.x += num * d.first;
  pos.y += num * d.second;
}

long walk(const vector<string> &path) {

  POS pos = {0, 0, 0};
  for (const string &p : path) {
    char cmd = p[0];
    int num = stoi(p.substr(1));
    switch(cmd) {
      case 'L':
      case 'R':
        rotate(pos, cmd, num);
        break;
      case 'F':
        move(pos, pos.d, num);
        break;
      case 'E':
        move(pos, 0, num);
        break;
      case 'S':
        move(pos, 1, num);
        break;
      case 'W':
        move(pos, 2, num);
        break;
      case 'N':
        move(pos, 3, num);
        break;
      default:
        throw runtime_error("Invalid instruction");
    }
  }
  return labs(pos.x) + labs(pos.y);
}

///////////////////////////////////////
// part 2
///////////////////////////////////////

void move_towards(POS &pos, const POS &wp, int num) {
  pos.x += wp.x * num;
  pos.y += wp.y * num;
}

int get_rotate_index(int dir, int rotate_deg) {
  return (4 + (rotate_deg/90) * dir) % 4;
}

void rotate_wp(POS &wp, int rotate_by) {

  // https://en.wikipedia.org/wiki/Rotation_matrix
  static const vector<vector<int>> rotations = {
    {1, 0, 0, 1},  // 0
    {0, 1, -1, 0}, // 90L
    {-1, 0, 0, -1},// 180L
    {0, -1, 1, 0}, // 270L
  };

  const auto &r = rotations[rotate_by];

  long nx = wp.x * r[0] + wp.y * r[1];
  long ny = wp.x * r[2] + wp.y * r[3];

  wp.x = nx;
  wp.y = ny;
}

long follow_waypoints(const vector<string> &path) {

  POS pos = {0, 0, 0}; // ship position
  POS wp = {10, -1}; // waypoint, relative to ship
  for (const string &p : path) {
    char cmd = p[0];
    int num = stoi(p.substr(1));
    switch(cmd) {
      case 'L':
        rotate_wp(wp, get_rotate_index(1, num));
        break;
      case 'R':
        rotate_wp(wp, get_rotate_index(-1, num));
        break;
      case 'F':
        move_towards(pos, wp, num);
        break;
      case 'E':
        move(wp, 0, num);
        break;
      case 'S':
        move(wp, 1, num);
        break;
      case 'W':
        move(wp, 2, num);
        break;
      case 'N':
        move(wp, 3, num);
        break;
      default:
        throw runtime_error("Invalid instruction");
    }
  }
  return labs(pos.x) + labs(pos.y);
}

///////////////////////////////////////
///////////////////////////////////////
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
  char buffer[200];
  while (!feof(fptr)) {
    if (fgets(buffer, sizeof(buffer)-1, fptr)) {
      trim(buffer);
      path.push_back(buffer);
    }
  }

  fclose(fptr);
  
  long part1 = walk(path);
  long part2 = follow_waypoints(path);

  cout << "Result: \t" << part1 << "\t" << part2 << endl;
}

int main() {
  cout << "*** Sample ***\n" << "Expected:\t25\t286" << endl;
  process_file(false);
  cout << "*** Final ****\n" << "Expected:\t562\t101860" << endl;
  process_file(true);
  return 0;
}
