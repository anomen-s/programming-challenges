#include <stdio.h>

#include <iostream>
#include <map>
#include <set>
#include <regex>

using namespace std;

/**
 * Run given program and find value of accumulator before loop (= an instruction is going to be executed for the second time) occurs.
 */

typedef struct {
  string ins;
  int op;
} Instruction;

typedef struct {
  long acc;
  long patch_ip;
  bool finished;
} Context;


Instruction decode(const string &rule) {
  static const regex pattern("^([a-z]+)\\s+([+-]?[0-9]+)\\s*$");
  smatch sm;
  if (!regex_match(rule, sm, pattern))
    throw invalid_argument("Invalid input " + rule);
  return { sm[1], stoi(sm[2]) };
}

long execute(const vector<Instruction> &code, Context &context) {
  size_t ip = 0;
  bool visited[code.size()] = {false};

  while (!visited[ip]) {
    visited[ip] = true;
    if (ip >= code.size()) {
      context.finished = true;
      return context.acc;
    }
    const bool switch_here = (context.patch_ip == (long) ip);
    const string ins = code[ip].ins;
    const int op = code[ip].op;
    if (ins == "acc") {
      context.acc += op;
    }
    if (ins == "nop" && switch_here) {
      ip += op;
    } else if (ins == "jmp" && !switch_here) {
      ip += op;
    } else {
      ip++;
    }
  }
  context.finished = false;
  return context.acc;
}

void process_file(bool final) {
  char filename[] = "input.sample";
  if (final) {
    filename[5] = '\0';
  }

  FILE *fptr = fopen(filename, "r");
  if (fptr == NULL)
    throw runtime_error(string("File not found: ") + filename);

  vector<Instruction> code;
  char buffer[400];
  while (!feof(fptr)) {
    if (fgets(buffer, sizeof(buffer)-1, fptr)) {
      code.push_back(decode(buffer));
    }
  }

  Context context = {0, -1, false};
  
  long part1 = execute(code, context);

  long part2 = 0;

  for (size_t ip = 0; ip < code.size(); ip++)  {
    context = {0, (long) ip, false};
    execute(code, context);
    if (context.finished) {
      part2 = context.acc;
    }
  }

  fclose(fptr);

  cout << "Result: \t" << part1 << "\t" << part2 << endl;
}

int main() {
  cout << "*** Sample ***\n" << "Expected:\t5\t8" << endl;
  process_file(false);
  cout << "*** Final ****\n" << "Expected:\t1749\t515" << endl;
  process_file(true);
}
