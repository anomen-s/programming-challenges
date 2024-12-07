import argparse
import re

# Decrypts strings in Lua source code of the cartridge
# !!! First you have to extract decrypt_fn (it has random name) function and convert it into Python syntax

def decrypt_fn(r0_1):

  r1_1 = ""
  # 127 chars long substitution string
  r2_1 = "\'-xU\x19\x1a\\2VR~i,m<r\x18d]1>sz(`a)y\x00[{Y3|/\"Q\x14\x0b!8\rph\x02H\x0fK@\x17+\x06W$\x13e\x03}MXE\n\x1c:q\x12L\x04uI9j\x05G=\x07%A4\x08DwTF#lv\x1f.J^bP oO\x016?\t*;\x1dCgZ0&Bc\x15_\x1b\x10f7\x0cN\x1enS\x11k\x0e\x16t5"
  for r6_1 in range(len(r0_1)):
    r7_1 = ord(r0_1[r6_1])
    if (0 < r7_1) and (r7_1 <= 127):
      r1_1 = r1_1 + r2_1[r7_1-1]
    else:
      r1_1 = r1_1 + chr(r7_1)
  return r1_1


def decode_lua_unicode(string):
    """
    Decodes Lua Unicode sequences (\\u{xx}) to actual Unicode characters.
    """
    def replace_unicode(match):
        hex_code = match.group(1)
        try:
            return chr(int(hex_code, 16))  # Convert hexadecimal to Unicode character
        except ValueError:
            return match.group(0)  # Leave the sequence unchanged if invalid
    
    return re.sub(r'\\u\{([0-9A-Fa-f]+)\}', replace_unicode, string)

def extract_lua_strings(file_path):
    """
    Reads a file and extracts Lua strings, decoding Unicode escape sequences.
    """
    # Regular expression for Lua strings
    lua_string_pattern = r"""
        "([^"\\]*(?:\\.[^"\\]*)*)"       # Double-quoted strings
        |'([^'\\]*(?:\\.[^'\\]*)*)'      # Single-quoted strings
        |\[\[([\s\S]*?)\]\]              # Multiline strings in double square brackets
    """
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            matches = re.findall(lua_string_pattern, content, re.VERBOSE)
            
            # Combine matches into a single list and filter empty groups
            strings = [m[0] or m[1] or m[2] for m in matches]
            
            print("Extracted Lua Strings:")
            for i, lua_string in enumerate(strings, start=1):
                # Decode Unicode sequences
                decoded_string = decode_lua_unicode(lua_string)
                decrypted_string = decrypt_fn(decoded_string)
                print(f"{i}: {decoded_string} ||| {decrypted_string}")
    
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract Lua strings from a file.")
    parser.add_argument("filename", type=str, help="Path to the Lua file.")
    
    args = parser.parse_args()
    extract_lua_strings(args.filename)

