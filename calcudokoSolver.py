from itertools import permutations
from math import prod


class calcudokoSolver:
  def __init__(self, size, blocks):
    self.size = size
    self.blocks = blocks
    self.grid = [[0] * size for _ in range(size)]

  #checking validation
  def checkValid(self, row, col, num):

    # row column constraints
    for i in range (self.size):
      if self.grid[row][i]== num or self.grid[i][col] == num:
        return False
    #block constraints
    for block in self.blocks:
      if (row, col) in block['cells']:
        if not self.checkBlock(block, num):
          return False

    return True

  def checkBlock(self, block, num):
    cells = block['cells']
    clue = block['clue']

    if clue.isdigit():
      if len(cells) == 1 and num == int(clue):
        return True
      return False


    # Operation based clues
    target, operation = int(clue[:-1]), clue[-1]
    current_nums = [self.grid[r][c] for r, c in cells if self.grid[r][c] != 0]
    current_nums.append(num)

    if len(current_nums) > len(cells):
      return False

    if operation == '+':
      if len(current_nums) == len(cells):
        return sum(current_nums) == target
      return sum(current_nums) <= target
    
    # elif operation == '-':
    #   if len(current_nums) < len(cells):
    #       return True  # only when block is full
    #   return abs(current_nums[0] - current_nums[1]) == target
    #   return False
    
##### TODO: try to solve 0-

    elif operation == '-':
      if len(current_nums) < len(cells):
          return True  # More numbers to be placed in the block
      # all permutations of current numbers
      for perm in permutations(current_nums):
          largest = perm[0]
          rest_sum = sum(perm[1:])
          if largest - rest_sum == target:
              return True
      return False

    elif operation == '*':
      if len(current_nums) == len(cells):
        return prod(current_nums) == target
      return prod(current_nums) <= target

    elif operation == '/':
      if len(current_nums) < len(cells):
          return True  # more numbers to be placed in the block
      if len(cells) == 2:
          # two cells are filled, check the division condition
          n1, n2 = current_nums[0], current_nums[1]
          return (n1 / n2 == target or n2 / n1 == target) if n1 != 0 and n2 != 0 else False
      return False

    return False

  #solving the blocks
  def solve(self):
    return self.backTrace(0,0)

  #backtrack algo with forwardcheck
  def backTrace(self, row, col):
    if row == self.size:
        return True

    nextRow, nextCol = (row, col+1) if col + 1 < self.size else (row+1, 0)

    if self.grid[row][col] != 0:
        return self.backTrace(nextRow, nextCol)

    # possible numbers for the current cell
    possible_numbers = [num for num in range(1, self.size + 1) if self.checkValid(row, col, num)]

    for num in possible_numbers:
        self.grid[row][col] = num
        if self.backTrace(nextRow, nextCol):
            return True
        self.grid[row][col] = 0

    return False

  # showing result
  def resultGrid(self):
    for row in self.grid:
      print(" ".join(map(str, row)))

# end of calcudokosolver class

# input part
def input(inputFile):
  with open(inputFile, 'r') as file:
    lines = file.readlines()

  size = int(lines[0].strip())
  totalBlocks = int(lines[1].strip())
  clueBlocks = []

  for i in range(totalBlocks):
    line = lines[2+i].strip().split()
    hint = line[0]
    cells=[(int(line[j]) -1, int(line[j+1]) - 1,) for j in range(1, len(line), 2)]
    clueBlocks.append({'clue': hint, 'cells': cells})

  return size, clueBlocks


# main
def main():
  inputFile = "input1.txt" # Need to add the file name like input.text
  puzzleSize, clueBlocks = input(inputFile) #definning the puzzle

  result = calcudokoSolver(puzzleSize, clueBlocks) #CSP

  #Result Part
  if result.solve():
    result.resultGrid()

  else:
    print("No Solution Exists")


main()