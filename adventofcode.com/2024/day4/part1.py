def count_xmas_in_matrix(matrix):
    def count_in_direction(x, y, dx, dy):
        count = 0
        rows, cols = len(matrix), len(matrix[0])
        for i in range(len("XMAS")):
            nx, ny = x + i * dx, y + i * dy
            if nx < 0 or ny < 0 or nx >= rows or ny >= cols or matrix[nx][ny] != "XMAS"[i]:
                return 0
        return 1

    rows, cols = len(matrix), len(matrix[0])
    directions = [
        (0, 1),    # Right
        (1, 0),    # Down
        (0, -1),   # Left
        (-1, 0),   # Up
        (1, 1),    # Down-Right diagonal
        (-1, -1),  # Up-Left diagonal
        (1, -1),   # Down-Left diagonal
        (-1, 1)    # Up-Right diagonal
    ]

    count = 0
    for x in range(rows):
        for y in range(cols):
            for dx, dy in directions:
                count += count_in_direction(x, y, dx, dy)

    return count

def read_matrix_from_file(filename):
    with open(filename, 'r') as file:
        return [line.strip() for line in file]

def main():
    input_file = "input"  # Replace with your input file name
    matrix = read_matrix_from_file(input_file)
    result = count_xmas_in_matrix(matrix)
    print(f"Total occurrences of 'XMAS': {result}")

if __name__ == "__main__":
    main()
