#include <stdio.h>

#include <iostream>
#include <vector>
#include <regex>

using namespace std;

void trim(char* buffer) {
  char* lf = strchr(buffer, '\n');
  if (lf) *lf = 0;
  char* cr = strchr(buffer, '\r');
  if (cr) *cr = 0;
}

void append(vector<string> &passport, char* line) {
  char* f = strtok(line, " ");
  if (f == NULL) {
    printf("Parsing error");
    exit(1);
  }
  while (f != NULL) {
    passport.push_back(string(f));
    f = strtok(NULL, " ");
  }
}

int is_valid_year(const string &year, const int lo, const int hi) {
  static const regex pattern("^\\d{4}$");
  if (!regex_match(year, pattern))
    return false;
  int v = stoi(year);
  return (lo <= v) && (v <= hi);
}

int is_valid_hgt(const string &hgt) {
  static const regex pattern("^(\\d{2,3})(cm|in)$");
  smatch sm;
  regex_match(hgt, sm, pattern);
  if (sm.empty())
    return false;
  // cout << "stoi " << sm[1] << endl;
  int v = stoi(sm[1]);
  if (sm[2] == "cm") {
    return (150 <= v) && (v <= 193);
  } else {
    return (59 <= v) && (v <= 76);
  }
}

int is_valid_hcl(const string &year) {
  static const regex pattern("^#[0-9a-f]{6}$");
  return regex_match(year, pattern);
}

int is_valid_pid(const string &pid) {
  static const regex pattern("^\\d{9}$");
  return regex_match(pid, pattern);
}

int is_valid_byr(const string &byr) {
  // cout << "testing BYR " << byr << "\n";
  return is_valid_year(byr, 1920, 2002);
}

int is_valid_iyr(const string &iyr) {
  // cout << "testing IYR " << iyr << "\n";
  return is_valid_year(iyr, 2010, 2020);
}

int is_valid_eyr(const string &eyr) {
  // cout << "testing EYR " << eyr << "\n";
  return is_valid_year(eyr, 2020, 2030);
}

int is_valid_ecl(const string &ecl) {
  static const vector<string> v = { "amb", "blu", "brn", "gry", "grn", "hzl", "oth" };
  // cout << "testing ECL  " << ecl << "\n";
  return (find(v.begin(), v.end(), ecl) != v.end());
}

map<string, function<bool(string)>> fields = {
   {"ecl", is_valid_ecl}, 
   {"pid", is_valid_pid}, 
   {"eyr", is_valid_eyr},
   {"hcl", is_valid_hcl},
   {"byr", is_valid_byr},
   {"iyr", is_valid_iyr},
   {"hgt", is_valid_hgt}
 };

string find_key(const vector<string> &passport, const string &key) {
  for (const string &f : passport) {
    string fkey = f.substr(0, 3);
    if (fkey.compare(key) == 0) {
      return f.substr(4, string::npos);
    }
  }
  return "";
}

int is_valid2(const vector<string> &passport, const bool validate) {
  for (const auto &field : fields) {
    string fvalue = find_key(passport, field.first);
    if (!fvalue.empty()) {
      if (validate && !fields[field.first](fvalue)) {
        // cout << "failed test (" << field.first << ") " << fvalue << "\n";
        return false;
      }
    } else {
      return false;
    }
  }
  return true;
}

void process_file(bool final) {
  FILE *fptr = fopen(final ? "input" : "input.sample", "r");
  if (fptr == NULL) {
    printf("Error!");
    exit(1);
  }
  vector<string> passport;
  int cnt1 = 0;
  int cnt2 = 0;
  char buffer[200];
  while (!feof(fptr)) {
    if (fgets(buffer, 199, fptr)) {
      trim(buffer);
      if (strlen(buffer) > 1) {
        append(passport, buffer);
      } else {
        cnt1 += is_valid2(passport, false);
        cnt2 += is_valid2(passport, true);
        passport.clear();
      }
    }
  }
  cnt1 += is_valid2(passport, false);
  cnt2 += is_valid2(passport, true);
  
  fclose(fptr);

  cout << "Result: \t" << cnt1 << "\t" << cnt2 << endl;
}

int main() {
  cout << "*** Sample ***\n" << "Expected:\t2\t2" << endl;
  process_file(false);
  cout << "*** Final ****\n" << "Expected:\t213\t147" << endl;
  process_file(true);
  return 0;
}
