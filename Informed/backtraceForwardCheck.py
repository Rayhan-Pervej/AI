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