#include <string>
#include <iostream>
#include <fstream>
#include <vector>
#include <regex>
#include <algorithm>

using namespace std;

/*
 * Check if value belongs to given ranges and assign proper ranges to table columns.
 */

typedef struct {
  vector<vector<long>> fields;
  vector<long> own_ticket;
  vector<vector<long>> tickets;
  vector<vector<long>> valid_tickets;
} Input;


bool check_rule(const vector<long> &field, long value) {
  if (field[0] <= value && value <= field[1]) {
    return true;
  }
  if (field[2] <= value && value <= field[3]) {
    return true;
  }
  return false;
}

bool contains(const vector<int> &vec, const int val) {
  return find(vec.begin(), vec.end(), val) != vec.end();
}

///////////////////////////////////////
// part 1
///////////////////////////////////////

bool check_with_all_rules(const Input &input, long value) {
  for (const auto &field: input.fields) {
      if (check_rule(field, value))
        return true;
  }
  return false;
}

long check_and_update_validity(Input &input) {
  long result = 0;
  for (const auto &ticket: input.tickets) {

    bool is_valid = true;
    for (const auto &value: ticket) {
      // cout << "Checking " << value << " ";
      if (!check_with_all_rules(input, value)) {
        result += value;
        is_valid = false;
      }
    }
    if (is_valid)
      input.valid_tickets.push_back(ticket);

    // cout << endl;
  }
  input.valid_tickets.push_back(input.own_ticket);
  return result;
}

///////////////////////////////////////
// part 2
///////////////////////////////////////

vector<int> find_matching_fields_for_column(const Input &input, int column) {
  vector<int> possible_fields;

  for (size_t fi = 0; fi < input.fields.size(); fi++) {
    bool is_valid = true;
    for (const auto &ticket: input.valid_tickets) {
      is_valid &= check_rule(input.fields[fi], ticket[column]);
    }
    if (is_valid)
      possible_fields.push_back(fi);
  }
  return possible_fields;
}

void remove_known_field(vector<vector<int>> &possible_fields, int field) {
 for (auto &pf: possible_fields) {
    if (pf.size() > 1 and contains(pf, field)) {
      remove(pf.begin(), pf.end(), field);
      pf.pop_back();
    }
  }
}

vector<int> assign_fields(const Input &input) {

  const int column_count = input.tickets[0].size();

  vector<vector<int>> possible_fields;

  for (int i = 0; i < column_count; i++) {
    possible_fields.push_back(find_matching_fields_for_column(input, i));
  }

  // analyze possible_fields
  vector<int> known_fields;
  bool new_known = true;
  while (new_known) {
    new_known = false;
    for (vector<int> &pf: possible_fields) {
      if ((pf.size() == 1) && !contains(known_fields, pf[0])) {
        known_fields.push_back(pf[0]);
        remove_known_field(possible_fields, pf[0]);
        new_known = true;
      }
    }
  }

  vector<int> result;
  for (int i = 0; i < column_count; i++) {
    result.push_back(possible_fields[i][0]);
  }
  return result;
}

long get_departure_data(const Input &input) {
  int64_t result = 1;
  vector<int> fieldpos = assign_fields(input);
  // product of first 6 fields "departure*"
  for (size_t i = 0; i < fieldpos.size(); i++)
    if (fieldpos[i] < 6) {
      result *= input.own_ticket[i];
    }

  return result;
}

///////////////////////////////////////
// main
///////////////////////////////////////

void process_field(Input &input, const string &line) {
  // cout << "Field: " << line << endl;
  static const regex field_pattern("^[^:]*: (\\d+)-(\\d+) or (\\d+)-(\\d+)\\s*$");
  smatch sm;
  if (!regex_match(line, sm, field_pattern))
    throw invalid_argument("Invalid input " + line);

  input.fields.push_back({stol(sm[1]),stol(sm[2]),stol(sm[3]),stol(sm[4])});
}

void process_ticket(Input &input, const string &line, bool own_ticket) {
  // cout << "ticket " << own_ticket << ": " << line << endl;
  static const regex num_pattern("(\\d+)");
  smatch sm;
  vector<long> ticket;
  string inputline = line;
  while (regex_search(inputline, sm, num_pattern)) {
    ticket.push_back(stoi(sm[1]));
    // cout <<  sm[1] << endl;
    inputline = sm.suffix().str();
  }
  if (own_ticket)
    input.own_ticket = ticket;
  else
    input.tickets.push_back(ticket);
}

void process_file(bool final) {

  ifstream ifs(final ? "input" : "input.sample", ifstream::in);

  Input input;

  int phase = 0;
  string buffer;
  while (!ifs.eof()) {
    getline(ifs, buffer);
    if (buffer.length() > 0) {
      switch (phase) {
        case 0:
          process_field(input, buffer);
          break;
        case 1:
          if (buffer != "your ticket:")
            throw runtime_error("Invalid line " + buffer);
          phase++;
          break;
        case 2:
          process_ticket(input, buffer, true);
          break;
        case 3:
          if (buffer != "nearby tickets:")
            throw runtime_error("Invalid line " + buffer);
          phase++;
          break;
        case 4:
          process_ticket(input, buffer, false);
          break;
      }
    } else {
      phase++;
    }
  }
  ifs.close();

  auto part1 = check_and_update_validity(input);
  auto part2 = get_departure_data(input);

  cout << "Result: \t" << part1 << "\t" << part2 << endl;
}

int main() {
  cout << "*** Sample ***" << endl << "Expected:\t71\t-" << endl;
  process_file(false);
  cout << "*** Final ****" << endl << "Expected:\t19240\t21095351239483" << endl;
  process_file(true);
  return 0;
}
