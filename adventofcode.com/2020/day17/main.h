#ifndef MAIN_H
#define MAIN_H

#include <set>
#include <vector>

class Coord {
  private:
    const int x;
    const int y;
    const int z;
    const int w;

  public:
    Coord(int x, int y, int z, int w);
    bool operator<(const Coord &other) const;
    Coord operator+(const Coord &other) const;
};


class State {
  public:
	int iteration;
	int radius;
	int d;
	std::set<Coord> data;

  	void activate(const Coord &coord);

  	void activate(int x, int y, int z, int w);

	int count_neigh(const Coord &coord) const;

	bool is_active(const Coord &coord) const;

  	long count() const;
};


void print_state(const State &state, int z, int w);

std::vector<Coord> build_neighbours3();

std::vector<Coord> build_neighbours4();

#endif
