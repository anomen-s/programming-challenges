# Function to read the input file and parse the numbers
def read_file(file_path):
    list1 = []
    list2 = []
    with open(file_path, 'r') as file:
        for line in file:
            # Split the line into two numbers
            num1, num2 = map(int, line.strip().split())
            list1.append(num1)
            list2.append(num2)
    return list1, list2

# Function to write the sorted output to a file
def write_file(file_path, list1, list2):
    with open(file_path, 'w') as file:
        for num1, num2 in zip(list1, list2):
            file.write(f"{num1} {num2}\n")

# Function to compute the sum based on occurrences
def compute_weighted_sum(list1, list2):
    from collections import Counter
    count2 = Counter(list2)
    return sum(num1 * count2[num1] for num1 in list1)

# Main function to process the lists
def process_file(input_path, output_path):
    # Read the input file
    list1, list2 = read_file(input_path)
    
    # Sort both lists
    sorted_list1 = sorted(list1)
    sorted_list2 = sorted(list2)
    
    # Write the sorted output to a file
    write_file(output_path, sorted_list1, sorted_list2)

    # Compute the weighted sum
    weighted_sum = compute_weighted_sum(sorted_list1, sorted_list2)
    print(f"Weighted sum: {weighted_sum}")

# Example usage
if __name__ == "__main__":
    input_file = "input.txt"  # Replace with your input file path
    output_file = "output.txt"  # Replace with your desired output file path
    process_file(input_file, output_file)
    print(f"Sorted lists have been written to {output_file}")
