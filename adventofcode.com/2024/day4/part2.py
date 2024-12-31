def count_a_with_specific_neighbors(matrix):
    def is_valid_position(x, y):
        return 0 <= x < len(matrix) and 0 <= y < len(matrix[0])

    def check_diagonal_neighbors(x, y):
        if matrix[x][y] != 'A':
            return 0

        # Get the diagonal neighbors
        diagonals = [
            (x - 1, y - 1), (x - 1, y + 1),
            (x + 1, y - 1), (x + 1, y + 1)
        ]

        # Check if the diagonals contain exactly two 'M' and two 'S'
        m_count = 0
        s_count = 0

        for dx, dy in diagonals:
            if is_valid_position(dx, dy):
                if matrix[dx][dy] == 'M':
                    m_count += 1
                elif matrix[dx][dy] == 'S':
                    s_count += 1

        # Ensure 'M' and 'S' are on the same line or column
        if m_count == 2 and s_count == 2:
            m_positions = [(dx, dy) for dx, dy in diagonals if is_valid_position(dx, dy) and matrix[dx][dy] == 'M']
            s_positions = [(dx, dy) for dx, dy in diagonals if is_valid_position(dx, dy) and matrix[dx][dy] == 'S']

            # Check alignment for both M and S
            same_line = all(m_positions[i][0] == m_positions[0][0] for i in range(len(m_positions)))
            same_column = all(m_positions[i][1] == m_positions[0][1] for i in range(len(m_positions)))

            same_line_s = all(s_positions[i][0] == s_positions[0][0] for i in range(len(s_positions)))
            same_column_s = all(s_positions[i][1] == s_positions[0][1] for i in range(len(s_positions)))

            if (same_line or same_column) and (same_line_s or same_column_s):
                return 1

        return 0

    count = 0
    rows, cols = len(matrix), len(matrix[0])
    for x in range(rows):
        for y in range(cols):
            count += check_diagonal_neighbors(x, y)

    return count

def read_matrix_from_file(filename):
    with open(filename, 'r') as file:
        return [line.strip() for line in file]

def main():
    input_file = "input"  # Replace with your input file name
    matrix = read_matrix_from_file(input_file)
    result = count_a_with_specific_neighbors(matrix)
    print(f"Total occurrences of 'A' with specific neighbors: {result}")

if __name__ == "__main__":
    main()
