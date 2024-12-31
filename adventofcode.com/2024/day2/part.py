def check_line_order(numbers):
    """
    Checks if the numbers in a list are all increasing or all decreasing.
    Also checks if the difference between adjacent numbers is between 1 and 3.
    :param numbers: List of numbers.
    :return: True if all numbers are increasing or all decreasing and satisfy the difference condition, False otherwise.
    """
    is_increasing = all(numbers[i] < numbers[i + 1] for i in range(len(numbers) - 1))
    is_decreasing = all(numbers[i] > numbers[i + 1] for i in range(len(numbers) - 1))
    satisfies_difference = all(1 <= abs(numbers[i] - numbers[i + 1]) <= 3 for i in range(len(numbers) - 1))
    return (is_increasing or is_decreasing) and satisfies_difference


def count_increasing_decreasing_lines(file_path):
    """
    Reads a text file and counts lines where numbers are all increasing or all decreasing
    and satisfy the difference condition.
    :param file_path: Path to the input text file.
    :return: Number of lines with all increasing or all decreasing numbers satisfying the conditions.
    """
    count = 0
    with open(file_path, 'r') as file:
        for line in file:
            # Convert line to a list of numbers
            try:
                numbers = list(map(int, line.split()))
                if check_line_order(numbers):
                    count += 1
            except ValueError:
                print(f"Skipping invalid line: {line.strip()}")
    return count


if __name__ == "__main__":
    input_file = input("Enter the path to the input file: ")
    try:
        result = count_increasing_decreasing_lines(input_file)
        print(f"Number of lines with all increasing or all decreasing numbers satisfying the conditions: {result}")
    except FileNotFoundError:
        print("The specified file was not found.")
