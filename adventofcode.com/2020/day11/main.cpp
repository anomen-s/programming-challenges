#include <stdio.h>

#include <cstring>
#include <iostream>
#include <vector>
#include <utility>

using namespace std;

/*
 * Simulate seat usage following simple rules based on number of occupied seats around.
 */

void trim(char* buffer) {
  char* lf = strchr(buffer, '\n');
  if (lf) *lf = 0;
  char* cr = strchr(buffer, '\r');
  if (cr) *cr = 0;
}

inline bool in_range(size_t x, size_t y, size_t max_x, size_t max_y) {
   return (x >= 0) && (x < max_x) && (y >= 0) && (y < max_y);
}

char compute_seat(const vector<string> &board, size_t x, size_t y, bool search, int neigh_limit) {
  static const vector<pair<int, int>> dirs = {{-1,-1},{0,-1},{1,-1},{1,0},{1,1},{0,1},{-1,1},{-1,0}};
  const size_t w = board[0].size();
  const size_t h = board.size();
  int nocc = 0;
  for (const auto &d : dirs) {
    size_t nx = x + d.first;
    size_t ny = y + d.second;
    while (search && in_range(nx, ny, w, h) && (board[ny][nx] == '.')) {
       nx += d.first;
       ny += d.second;
    }
    if (in_range(nx, ny, w, h)) {
      nocc += (board[ny][nx] == '#');
    }
  }
  const char curr = board[y][x];
  if ((curr == 'L') && (nocc == 0)) {
    return '#';
  }
  if ((curr == '#') && (nocc >= neigh_limit)) {
    return 'L';
  }

  return curr;
}

void compute_next(const vector<string> &board, vector<string> &board_next, bool search, int neigh_limit) {
  for (size_t y = 0; y < board.size(); y++) {
    for (size_t x = 0; x < board[y].size(); x++) {
      if (board[y][x] != '.') {
        board_next[y][x] = compute_seat(board, x, y, search, neigh_limit);
      }
    }
  }
}

long count_occupied(const vector<string> &board) {
  long cnt = 0;
  for (size_t y = 0; y < board.size(); y++) {
    for (size_t x = 0; x < board[y].size(); x++) {
      cnt += (board[y][x] == '#');
    }
  }
  return cnt;
}

long solve(vector<string> board, bool search, int neigh_limit) {

  vector<string> board_next(board);
  while (true) {
    compute_next(board, board_next, search, neigh_limit);

    if (board == board_next) {
      return count_occupied(board);
    }
    board = board_next;
  }
}

void process_file(bool final) {
  FILE *fptr = fopen(final ? "input" : "input.sample", "r");
  if (fptr == NULL)
    throw runtime_error("File not found");
  vector<string> board;
  char buffer[200];
  while (!feof(fptr)) {
    if (fgets(buffer, sizeof(buffer)-1, fptr)) {
      trim(buffer);
      board.push_back(buffer);
    }
  }

  fclose(fptr);
  
  long part1 = solve(board, false, 4);
  long part2 = solve(board, true, 5);

  cout << "Result: \t" << part1 << "\t" << part2 << endl;
}

int main() {
  cout << "*** Sample ***\n" << "Expected:\t37\t26" << endl;
  process_file(false);
  cout << "*** Final ****\n" << "Expected:\t2204\t1986" << endl;
  process_file(true);
  return 0;
}
