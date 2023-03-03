#include <string>
#include <fstream>
#include <sstream>
#include <iostream>
#include <vector>
#include <map>
#include <regex>
#include <utility>
#include <algorithm>
#include "main.h"

using namespace std;

/*
 * Regular expressions
 */

///////////////////////////////////////
// part1
///////////////////////////////////////

vector<size_t> vector_matches(const Matcher &matcher, const size_t pos, const vector<int> &sub_rule_ids) {
  vector<size_t> result;
  // use recursion here
  // call match for first and then recursion for rest
  const vector<size_t> mlengths = matches(matcher, pos, sub_rule_ids[0]);
  if (mlengths.size() == 0) {
    return result;
  }
  if (sub_rule_ids.size() == 1) {
    return mlengths;
  }
  const vector<int> remaining = pop_front(sub_rule_ids);
  for (int len1 : mlengths) {
    size_t sub_pos = pos + len1;
    const auto &remlengths = vector_matches(matcher, sub_pos, remaining);
    for (const auto &remlength : remlengths) {
       result.push_back(len1 + remlength);
    }
  }
  return result;
}


// returns list of lengths of matches
vector<size_t> matches(const Matcher &matcher, size_t pos, int rule_id) {
  // cout << "R" << matcher.rules.size() << endl;
  const auto &rule = matcher.rules.at(rule_id);

  if (rule.type == r_term) {
    if (pos < matcher.line.length() && matcher.line.compare(pos, rule.str.length(), rule.str) == 0) {
      return { rule.str.length() };
    } else {
      return {};
    }
  }

  auto sub_matches = vector_matches(matcher, pos, rule.a);
  if (rule.b.size() > 0) {
    auto sub_matches_b = vector_matches(matcher, pos, rule.b);
    for (auto b: sub_matches_b) {
      sub_matches.push_back(b);
    }
  }

  return sub_matches;
}

///////////////////////////////////////
// part 2
///////////////////////////////////////

void transform_rules_2(map<int, Rule> &rules) {
  read_rule(rules, "8: 42 | 42 8");
  read_rule(rules, "11: 42 31 | 42 11 31");
}

///////////////////////////////////////
// main
///////////////////////////////////////

void print_rule(const Rule &rule) {
  cout << "Rule " << rule.id <<": ";
  if (rule.type == r_term)
    cout << "\"" << rule.str << "\"";
  for (auto id: rule.a)
    cout << id << " ";
  if (rule.type == r_alt) {
    cout << " | ";
    for (auto id: rule.b)
      cout << id << " ";
  }
  cout << endl;
}

template<typename T>
bool vector_contains(const std::vector<T> &v, const T &item) {
    return find(v.begin(), v.end(), item) != v.end();
}

vector<int> parse_int_list(const string &ids) {
  vector<int> result;
  istringstream bufferstream(ids);
  string s;
  while (getline(bufferstream, s, ' ')) {
    result.push_back(stoi(s));
  }
  return result;
}

template<typename T>
void extend_vector(vector<T> &target, const vector<T> &src) {
  for (size_t item: src)
    if (find(target.begin(), target.end(), item) == target.end())
      target.push_back(item);
}

template<typename T>
vector<T> pop_front(const vector<T> &src) {
  vector<T> result;
  for (size_t i = 1; i < src.size(); i++) {
    result.push_back(src[i]);
  }
  return result;
}

void read_rule(map<int, Rule> &rules, const string &line) {
  static const regex rule_pattern("(\\d+):\\s*([0-9 \"a-z]+)\\s*(\\|\\s*([0-9 ]+))?\\s*$");

  smatch sm;

  if (regex_match(line, sm, rule_pattern)) {
    // cout << sm[0] << " → <" << sm[1] << ">, <"  << sm[2] << ">, <"  << sm[4]   << ">" << endl;
    const int rule_id = stoi(sm[1]);

    // terminal
    const string rule_def = sm[2];
    if (rule_def[0] == '\"') {
      string term = rule_def.substr(1, rule_def.length()-2);
      rules[rule_id] = {rule_id, r_term, term};
      // cout << rule_id << " = " << term << endl;
      return;
    }

    // subrules
    vector<int> a = parse_int_list(sm[2]);
    vector<int> b = parse_int_list(sm[4]);
    rules[rule_id] = {rule_id, b.size() > 0 ? r_alt : r_single , "", a, b};
    // cout << rule_id << " -> " << a.size() << "/" << b.size() << endl;
  } else {
    throw runtime_error("Invalid input: " + line);
  }

}


bool process_string(const map<int, Rule> &rules, const string &line) {

  const Matcher matcher = {line, rules};
  vector<size_t> match_lengths = matches(matcher, 0, 0);
  return vector_contains(match_lengths, line.length());

  // cout << line << endl;
}


void process_file(const string &input) {
  ifstream ifs("input" + input, ifstream::in);

  int phase = 0;

  map<int, Rule> rules1;
  map<int, Rule> rules2;

  int valid_count1 = 0;
  int valid_count2 = 0;

  while (!ifs.eof()) {
    string buffer;
    getline(ifs, buffer);
    if (buffer.size() > 0) {
      if (phase == 0) {
        read_rule(rules1, buffer);
      } else {
        valid_count1 += process_string(rules1, buffer);
        valid_count2 += process_string(rules2, buffer);
      }
    } else {
      phase++;
      rules2 = rules1;
      transform_rules_2(rules2);
    }
  }
  ifs.close();

  cout << "Result: \t" << valid_count1 << "\t" << valid_count2 << endl;
}

int main() {
  cout << "*** Sample 1 ***" << endl << "Expected:\t2\t?" << endl;
  process_file(".sample1");
  cout << "*** Sample 2 ***" << endl << "Expected:\t?\t12" << endl;
  process_file(".sample2");
  cout << "*** Final ****" << endl << "Expected:\t195\t309" << endl;
  process_file("");
  return 0;
}
