#include <string>
#include <fstream>
#include <iostream>
#include <vector>

using namespace std;

/*
 * Evaluate numeric expressions.
 */

///////////////////////////////////////
// part1
///////////////////////////////////////

enum token_type { op_plus, op_multiply, val_str, val_number };

struct Token {
   token_type type;
   string str;
   int64_t value;
};

void eval_stack(vector<Token> &tokens, bool plus_only = false) {
  for (size_t i = 0; i < tokens.size(); i++) {
    if (tokens[i].type == val_str) {
      long v = stol(tokens[i].str);
      tokens[i] = { val_number, "", v};
    }
  }
  while (tokens.size() >= 3) {
    int s = tokens.size() - 3;
    if ((tokens[s].type == val_number) && (tokens[s+2].type == val_number)) {
      if (tokens[s+1].type == op_plus) {
        int64_t r = tokens[s].value + tokens[s+2].value;
        tokens.pop_back();
        tokens.pop_back();
        tokens.pop_back();
        tokens.push_back({val_number, "", r});
      } else if (tokens[s+1].type == op_multiply) {
        if (plus_only) {
          // + has precedence
          return;
        }
        int64_t r = tokens[s].value * tokens[s+2].value;
        tokens.pop_back();
        tokens.pop_back();
        tokens.pop_back();
        tokens.push_back({val_number, "", r});
      } else {
        throw runtime_error("Unexpected operation");
      }
    } else {
      throw runtime_error("Unexpected tokens");
    }
  }
}

int64_t eval1(string::const_iterator &expr, const string::const_iterator &end, bool plus_precedence) {

  vector<Token> tokens;
  while (expr != end) {
    char c = *expr;
    switch (c) {
      case ' ':
        break;
      case '*':
        eval_stack(tokens);
        tokens.push_back({op_multiply});
        break;
      case '+':
        eval_stack(tokens, plus_precedence);
        tokens.push_back({op_plus});
        break;
      case '0':
      case '1':
      case '2':
      case '3':
      case '4':
      case '5':
      case '6':
      case '7':
      case '8':
      case '9':
        if ((tokens.size() == 0) || tokens[tokens.size()-1].type != val_str) {
          tokens.push_back({val_str, ""});
        }
        tokens[tokens.size()-1].str += c;
        break;
      case ')':
        eval_stack(tokens);
        return tokens[0].value;
      case '(':
        tokens.push_back({val_number, "", eval1(++expr, end, plus_precedence)});
        break;
      default:
        throw runtime_error("Unexpected char");
    }
    expr++;
  }
  eval_stack(tokens);
  return tokens[0].value;
}

///////////////////////////////////////
// main
///////////////////////////////////////

void process_file(bool final) {
  ifstream ifs(final ? "input" : "input.sample", ifstream::in);

  int64_t sum1 = 0;
  int64_t sum2 = 0;
  while (!ifs.eof()) {
    string buffer;
    getline(ifs, buffer);
    if (buffer.size() > 0) {
      auto buffer_it1 = buffer.cbegin();
      // cout << "EXPR: " << buffer << endl;
      sum1 += eval1(buffer_it1, buffer.cend(), false);
      auto buffer_it2 = buffer.cbegin();
      sum2 += eval1(buffer_it2, buffer.cend(), true);
    }

  }
  ifs.close();

  cout << "Result: \t" << sum1 << "\t" << sum2 << endl;
}

void test() {
}

int main() {
  test();
  cout << "*** Sample ***" << endl << "Expected:\t26386\t693942" << endl;
  process_file(false);
  cout << "*** Final ****" << endl << "Expected:\t67800526776934\t340789638435483" << endl;
  process_file(true);
  return 0;
}
