#ifndef MAIN_H
#define MAIN_H

#include <string>
#include <vector>

enum Rule_type {
   r_term,   // terminal string
   r_single, // single rule sequence
   r_alt     // two sequences of rules
};

struct Rule {
   int id;
   Rule_type type;
   std::string str;
   std::vector<int> a;
   std::vector<int> b;
};


struct Matcher {
  const std::string &line;
  const std::map<int, Rule> &rules;
};


std::vector<size_t> matches(const Matcher &matcher, size_t pos, int rule_id);

std::vector<size_t> vector_matches(const Matcher &matcher, const size_t pos, const std::vector<int> &sub_rule_ids);

void read_rule(std::map<int, Rule> &rules, const std::string &line);

void print_rule(const Rule &rule);

template<typename T>
void extend_vector(std::vector<T> &target, const std::vector<T> &src);

template<typename T>
bool vector_contains(const std::vector<T> &v, const T &item);

template<typename T>
std::vector<T> pop_front(const std::vector<T> &src);

#endif
