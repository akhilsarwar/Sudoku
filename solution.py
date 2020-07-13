
#solution of sudoku

def Backtrack(grid, check):

    for i in range(9):
        for j in range(9):
            if grid[i,j] == 0:
                for num in range(1,10):
                    if check(grid, num, i, j):
                        grid[i,j] = num
                        state = Backtrack(grid, check)
                        if state:
                            return True
                        else:
                            grid[i,j]=0
                return False

    return True

