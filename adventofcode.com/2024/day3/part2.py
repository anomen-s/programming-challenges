import re

def calculate_sum_of_multiplications(input_file):
    try:
        # Read the content of the input file
        with open(input_file, 'r') as file:
            content = file.read()

        # Find all substrings matching the pattern "mul(\d+,\d+)"
        matches = re.finditer(r"(do\(\)|don't\(\)|mul\((\d+),(\d+)\))", content)

        total_sum = 0
        processing = True  # Indicates if we should process multiplications

        for match in matches:
            print(match.group(1))
            if match.group(1) == "do()":
                processing = True
            elif match.group(1) == "don't()":
                processing = False
            elif processing and match.group(2) and match.group(3):
                # Perform multiplication only if in processing mode
                total_sum += int(match.group(2)) * int(match.group(3))

        return total_sum

    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Specify the input file name
input_file = "input.txt"
result = calculate_sum_of_multiplications(input_file)

if result is not None:
    print(f"The total sum of all multiplications is: {result}")
