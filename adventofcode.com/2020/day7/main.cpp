#include <stdio.h>

#include <iostream>
#include <map>
#include <set>
#include <regex>

using namespace std;
/**
 * Given rules about bags containing other bags, compute how many types of bags can contain "Shiny gold" bag.
 * 
 */

const string MY_BAG = "shiny gold";

void add_rule(const string &rule, map<string, map<string, int>> &rules) {
  static const regex full_pattern("^([a-z ]+) bags contain (.+)\\s*$");
  static const regex bag_pattern("(\\d+) ([a-z ]+) bags?*");
  smatch sm;
  regex_match(rule, sm, full_pattern);
  if (sm.empty())
    throw invalid_argument("Invalid input " + rule);
  string bag_name = sm[1];
  string contains = sm[2];

  map<string, int> result;
  // cout << rule << " → " << contains << " →";

  while (regex_search(contains, sm, bag_pattern)) {
    string in_bag_name = sm[2];
    int in_bag_cnt = stoi(sm[1]);
    result[in_bag_name] = in_bag_cnt;
    // cout <<  in_bag_cnt << in_bag_name << "#";
    contains = sm.suffix().str();
  }
  rules[bag_name] = result;
  // cout << endl;
}

set<string> scan_bags(const map<string, map<string, int>> &rules) {
  set<string> names = { MY_BAG };
  // iteratively search direct containing bags
  bool added = true;
  while (added) {
    added = false;
    // go over all rules
    for (const auto &pair : rules) {
      const map<string, int> bag = pair.second;
      const string bag_name = pair.first;
      // if bag_name not in names
      if (names.count(bag_name) == 0) {
        // check if any sub-bag is present in names
        for (const auto &subpair : bag) {
          if (names.count(subpair.first) > 0) {
             names.insert(bag_name);
             added = true;
          }
        }
      }
    }
  }

  return names;
}

long compute_content(const map<string, map<string, int>> &rules, const string &current_bag) {
  // find bag
  for (const auto &pair : rules) {
    const map<string, int> bags = pair.second;
    const string bag_name = pair.first;

    // compute size
    if (bag_name == current_bag) {
      long cnt = 0;
      for (const auto &subpair : bags) {
        // cout << "Found: " << current_bag << " → " << subpair.first << "x " << subpair.second << endl;
        cnt += subpair.second * (1 + compute_content(rules, subpair.first));
      }
      // cout << "Found: " << current_bag << " → " << cnt << endl;
      return cnt;
    }
  }
  throw runtime_error("Unknown bag: " + current_bag);
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

  map<string, map<string, int>> rules;
  char buffer[400];
  while (!feof(fptr)) {
    if (fgets(buffer, sizeof(buffer)-1, fptr)) {
      add_rule(string(buffer), rules);
    }
  }

  set<string> bags1 = scan_bags(rules);
  long cnt1 = bags1.size() - 1;
  long cnt2 = compute_content(rules, MY_BAG);

  fclose(fptr);

  cout << "Result: \t" << cnt1 << "\t" << cnt2 << endl;
}

int main() {
  cout << "*** Sample1 ***\n" << "Expected:\t4\tx" << endl;
  process_file(false, '1');
  cout << "*** Sample2 ***\n" << "Expected:\tx\t126" << endl;
  process_file(false, '2');
  cout << "*** Final ****\n" << "Expected:\t287\t48160" << endl;
  process_file(true, 0);
  return 0;
}
