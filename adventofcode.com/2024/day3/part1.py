import re

def calculate_sum_of_multiplications(input_file):
    try:
        # Read the content of the input file
        with open(input_file, 'r') as file:
            content = file.read()

        # Find all substrings matching the pattern "mul(\d+,\d+)"
        matches = re.findall(r"mul\((\d+),(\d+)\)", content)

        # Calculate the sum of all multiplications
        total_sum = sum(int(a) * int(b) for a, b in matches)

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
