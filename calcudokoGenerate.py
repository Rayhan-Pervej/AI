import numpy as np
from math import prod
import random

def random_board(size):
    """Generate a valid board with unique numbers in rows and columns."""
    board = np.zeros((size, size), dtype=int)
    for row in range(size):
        while True:
            board[row, :] = 0
            for col in range(size):
                possible = set(range(1, size + 1)) - set(board[row, :]) - set(board[:, col])
                if not possible:
                    break
                board[row, col] = np.random.choice(list(possible))
            else:
                break
    return board

def partition_board(size, max_partition_size, difficulty):
    """Partition the board into connected groups based on difficulty."""
    partitions = []
    cells = set((r, c) for r in range(size) for c in range(size))
    min_cells = 1 if difficulty == "easy" else 2

    while cells:
        num_cells = np.random.randint(min_cells, max_partition_size + 1)
        partition = set()
        cell = cells.pop()
        partition.add(cell)
        frontier = [cell]

        while len(partition) < num_cells and frontier:
            r, c = frontier.pop()
            for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                new_cell = (r + dr, c + dc)
                if new_cell in cells:
                    partition.add(new_cell)
                    cells.remove(new_cell)
                    frontier.append(new_cell)
        partitions.append(list(partition))
    return partitions

def assign_operations(board, partitions, difficulty):
    """Assign operations and targets to each partition based on difficulty, ensuring variety."""
    required_ops = {
        "easy": ['+', '-'],  # Easy allows + and -
        "medium": ['+', '-', '*'],  # Medium allows +, -, *
        "hard": ['+', '-', '*', '/']  # Hard allows +, -, *, /
    }

    operations = []
    used_ops = {op: 0 for op in required_ops[difficulty]}

    for partition in partitions:
        values = [board[r][c] for r, c in partition]
        if len(values) == 1:
            # Single-cell partitions always use "none" if allowed
            operations.append(('none', values[0]))
            continue  # Skip further processing for single-cell partitions

        # Pick an operation considering the difficulty level
        available_ops = required_ops[difficulty]
        op = random.choice(available_ops)

        # Ensure all operators are used at least once for medium and hard difficulties
        if difficulty != "easy" and len(operations) >= len(partitions) - len(required_ops[difficulty]):
            op = random.choice([op for op in available_ops if used_ops[op] == 0] or available_ops)

        # Compute the target based on the operation
        if op == '+':
            target = sum(values)
        elif op == '-':
            target = abs(values[0] - values[1]) if len(values) == 2 else random.choice(values)
        elif op == '*':
            target = prod(values)
        elif op == '/':
            if len(values) == 2 and max(values) % min(values) == 0:
                target = max(values) // min(values)
            else:
                op, target = '+', sum(values)
        else:
            raise ValueError(f"Unhandled operation: {op}")

        operations.append((op, target))
        used_ops[op] += 1

    return operations



def generate_puzzle(size, difficulty):
    """Generate a Calcudoku puzzle."""
    max_partition_size = 4 if difficulty == "easy" else 3 if difficulty == "medium" else 2
    while True:
        board = random_board(size)
        partitions = partition_board(size, max_partition_size, difficulty)
        operations = assign_operations(board, partitions, difficulty)
        if validate_puzzle(size, partitions, operations):
            return board, partitions, operations

def validate_puzzle(size, partitions, operations):
    """Validate the puzzle using a solver."""
    solver = CalcudokuSolver(size, [{'clue': f"{target}{op}", 'cells': [(r, c) for r, c in p]}
                                     for p, (op, target) in zip(partitions, operations)])
    return solver.solve()

class CalcudokuSolver:
    def __init__(self, size, blocks):
        self.size = size
        self.blocks = blocks
        self.grid = [[0] * size for _ in range(size)]

    def check_valid(self, row, col, num):
        for i in range(self.size):
            if self.grid[row][i] == num or self.grid[i][col] == num:
                return False
        for block in self.blocks:
            if (row, col) in block['cells']:
                if not self.check_block(block, num):
                    return False
        return True

    def check_block(self, block, num):
        cells = block['cells']
        clue = block['clue']
        if 'none' in clue:
            return len(cells) == 1 and num == int(clue[:-4])
        target, operation = int(clue[:-1]), clue[-1]
        current_nums = [self.grid[r][c] for r, c in cells if self.grid[r][c] != 0]
        current_nums.append(num)
        if len(current_nums) > len(cells):
            return False
        if operation == '+':
            return sum(current_nums) == target if len(current_nums) == len(cells) else sum(current_nums) <= target
        elif operation == '-':
            return len(current_nums) == 2 and abs(current_nums[0] - current_nums[1]) == target
        elif operation == '*':
            return prod(current_nums) == target if len(current_nums) == len(cells) else prod(current_nums) <= target
        elif operation == '/':
            return len(current_nums) == 2 and max(current_nums) // min(current_nums) == target
        return False

    def solve(self):
        return self.backtrack(0, 0)

    def backtrack(self, row, col):
        if row == self.size:
            return True
        next_row, next_col = (row, col + 1) if col + 1 < self.size else (row + 1, 0)
        if self.grid[row][col] != 0:
            return self.backtrack(next_row, next_col)
        for num in range(1, self.size + 1):
            if self.check_valid(row, col, num):
                self.grid[row][col] = num
                if self.backtrack(next_row, next_col):
                    return True
                self.grid[row][col] = 0
        return False

def main():
    size = 4
    difficulty = "hard"
    board, partitions, operations = generate_puzzle(size, difficulty)
    print(f"\nBoard Size: {size}x{size}")
    print("Partitions and Clues:")
    for partition, (op, target) in zip(partitions, operations):
        cells = " ".join(f"({r + 1}, {c + 1})" for r, c in partition)
        print(f"{target}{op} -> {cells}")

main()
