"""
Imagine you have an (m * n) grid where some cells contain an X while others a dot.  A battleship is any horizontal, or vertical, contiguous line of X's on the grid.

How would you determine how many battleships are on the grid?

Example 1:
grid = [["X",".",".","X"],
        [".",".",".","X"],
        ["X","X",".","X"]]

result = 3

Example 2:
grid = [[".",".","X","X"],
        [".","X",".","."],
        [".","X",".","."]]

result = 2
"""


def solution(grid):
  count = 0
  for item in range(len(grid)):
    for item2 in range(len(grid[item])):
      if grid[item][item2] == "X":
        if item == 0 or grid[item-1][item2] == ".":
          if item2 == 0 or grid[item][item2-1] == ".":
            count += 1
  return count


print(solution([["X",".",".","X"],
        [".",".",".","."],
        ["X","X",".","X"]]))

print(solution([["X",".",".","X"],
        [".",".",".","X"],
        ["X","X",".","X"]]))

print(solution([[".",".","X","X"],
        [".","X",".","."],
        [".","X",".","."]]))