#include <stdio.h>

#include <cstring>
#include <iostream>
#include <vector>
#include <map>
#include <regex>

using namespace std;

/*
 * Analyze memory content after writes with or/and bitmasks.
 */

typedef struct {
  int64_t or_mask;
  int64_t and_mask;
  int is_part1;
  vector<int64_t> x_bits;
} Context;

int64_t to_mask(const string &mask, char x) {
  string value = mask;
  for (size_t i = 0; i < value.length(); i++) {
    if (value[i] == 'X') {
      value[i] = x;
    }
  }
  return stoll(value, nullptr, 2);
}

vector<int64_t> to_x_list(const string &mask) {
  vector<int64_t> result;
  int64_t bitval = 1;
  bitval <<= (mask.length()-1);
  // cout << mask.length();
  for (size_t i = 0; i < mask.length(); i++) {
    if (mask[i] == 'X') {
      result.push_back(bitval);
    }
    bitval >>= 1;
  }

  // cout << mask << " = ";
  // for (auto x : result) 
  //   cout << " " << x;
  // cout << endl;
  return result;
}

int64_t memory_sum(const map<int64_t,int64_t> &mem) {
  int64_t result = 0;
  for (auto cell: mem) {
    // cout << cell.first << " = " << cell.second << endl;
    result += cell.second;
  }
  return result;
}

///////////////////////////////////////
// part1
///////////////////////////////////////

void process_write1(map<int64_t, int64_t> &mem, const Context &ctx, int64_t addr, int64_t value) {
    mem[addr] = (value & ctx.and_mask) | ctx.or_mask;
}

///////////////////////////////////////
// part2
///////////////////////////////////////

void process_write2(map<int64_t, int64_t> &mem, const Context &ctx, int64_t ins_addr, int64_t ins_value) {

    const int64_t base_addr = (ins_addr | ctx.or_mask);
    const int64_t cell_count = 1 << ctx.x_bits.size();
    // cout << "baseaddr " << base_addr << " × " << cell_count << " // " << (ins_addr | ctx.or_mask) << endl;

    for (int64_t i = 0; i < cell_count; i++) {
      // cout << "**********" << endl << "i " << i << endl;
      int64_t addr = base_addr;
      for (size_t b = 0; b < ctx.x_bits.size(); b++) {
        // cout << "b " << b << endl;
        if (i & (1 << b)) {
          addr ^= ctx.x_bits[b];
          // cout << "ib " << ctx.x_bits[b] << endl;
        }
      }
      // cout << "addr " << addr << " ← " << ins_value << endl;
      mem[addr] = ins_value;
    }

}


///////////////////////////////////////
// main
///////////////////////////////////////


bool process_mask(Context &ctx, const string &line) {
  static const regex mask_pattern("^mask\\s*=\\s*([01X]+)\\s*$");

  smatch sm;

  if (regex_match(line, sm, mask_pattern)) {
    ctx.and_mask = to_mask(sm[1], '1');
    ctx.or_mask = to_mask(sm[1], '0');
    ctx.x_bits = to_x_list(sm[1]);
    // cout << "mask " <<  sm[1] << " and " << mem.and_mask << " or " << mem.or_mask  << endl;
    return true;
  }
  return false;
}

void process_write(map<int64_t, int64_t> &mem, const Context &ctx, const string &line) {
  static const regex write_pattern("^mem\\[(\\d+)\\]\\s*=\\s*(\\d+)\\s*$");

  smatch sm;

  if (regex_match(line, sm, write_pattern)) {
    int64_t addr = stoll(sm[1]);
    int64_t value = stoll(sm[2]);
    if (ctx.is_part1) {
      process_write1(mem, ctx, addr, value);
    } else {
      process_write2(mem, ctx, addr, value);
    }
    // cout << "wrote " <<  mem.mem[addr] << endl;
  } else {
    throw invalid_argument("Invalid input " + line);
  }
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
    throw runtime_error("File not found");

  Context ctx = {0, 0, (part == '1'), {}};
  map<int64_t, int64_t> memory;

  char buffer[200];
  while (!feof(fptr)) {
    if (fgets(buffer, sizeof(buffer)-1, fptr)) {
      if (!process_mask(ctx, buffer)) {
        process_write(memory, ctx, buffer);
      }
      // cout << buffer << endl;
    }
  }

  fclose(fptr);

  auto r = memory_sum(memory);

  cout << "Result" << part << ": \t" << r << endl;
}

int main() {
  cout << "*** Sample ***" << endl << "Expected:\t165\t208" << endl;
  process_file(false, '1');
  process_file(false, '2');
  cout << "*** Final ****" << endl << "Expected:\t13496669152158\t3278997609887" << endl;
  process_file(true, '1');
  process_file(true, '2');
  return 0;
}
