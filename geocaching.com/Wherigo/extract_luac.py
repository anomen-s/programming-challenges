#!/usr/bin/env python3

#chatgpt

import sys

def extract_content(input_file, output_file, marker=b"\x1bLua"):
    try:
        with open(input_file, "rb") as infile:
            data = infile.read()
        
        # Find the first occurrence of the marker
        marker_position = data.find(marker)
        
        if marker_position == -1:
            print(f"Marker {marker} not found in the input file.")
            return
        
        # Write the content starting from the marker to the output file
        with open(output_file, "wb") as outfile:
            outfile.write(data[marker_position:])
        
        print(f"Content starting from marker {marker} written to {output_file}")
    
    except FileNotFoundError:
        print(f"File not found: {input_file}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python extract_luac.py <input_file> <output_file>")
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        extract_content(input_file, output_file)
