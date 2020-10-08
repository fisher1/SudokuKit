#Solver logic thanks to https://github.com/aaronfrederick/SudokuSolver

class SudokuSolver:
    def __init__(self, container):
        self.subtract_set = {1,2,3,4,5,6,7,8,9}
        self.container = container

    def solve(self):
        zero_count = 0
        for l in self.container:
            for v in l:
                if v == 0:
                    zero_count += 1
                    
        solving = True
        max_cycles = 81

        while solving:
            #Solver Portion
            self.container, stump_count = self.explicit_solver()
            
            #Loop-Breaking Portion
            zero_count = 0
            for l in self.container:
                for v in l:
                    if v == 0:
                        zero_count += 1
            if zero_count==0 or max_cycles==0:
                solving=False
            if stump_count > 0:
                for i in range(9):
                    for j in range(9):
                        self.container = self.implicit_solver(i, j)
            max_cycles -= 1
        return self.container

    def check_horizontal(self,i,j):
        return self.subtract_set - set(self.container[i])

    def check_vertical(self,i,j):
        ret_set = []
        for x in range(9):
            ret_set.append(self.container[x][j])
        return self.subtract_set - set(ret_set)

    def check_square(self,i,j):
        first = [0,1,2]
        second = [3,4,5]
        third = [6,7,8]
        find_square = [first,second,third]
        for l in find_square:
            if i in l:
                row = l
            if j in l:
                col = l
        ret_set = []
        for x in row:
            for y in col:
                ret_set.append(self.container[x][y])
        return self.subtract_set - set(ret_set)

    def get_poss_vals(self,i,j):
        poss_vals = list(self.check_square(i,j).intersection(self.check_horizontal(i,j)).intersection(self.check_vertical(i,j)))
        return poss_vals

    def explicit_solver(self):
        stump_count = 1
        for i in range(9):
            for j in range(9):
                if self.container[i][j] == 0:
                    poss_vals = self.get_poss_vals(i,j)
                    if len(poss_vals) == 1:
                        self.container[i][j] = list(poss_vals)[0]
                        stump_count = 0
        return self.container, stump_count

    def implicit_solver(self,i,j):
        if self.container[i][j] == 0:
            poss_vals = self.get_poss_vals(i,j)
            
            #check row
            row_poss = []
            for y in range(9):
                if y == j:
                    continue
                if self.container[i][y] == 0:
                    for val in self.get_poss_vals(i,y):
                        row_poss.append(val)
            if len(set(poss_vals)-set(row_poss)) == 1:
                self.container[i][j] = list(set(poss_vals)-set(row_poss))[0]
            
            #check column
            col_poss = []
            for x in range(9):
                if x == i:
                    continue
                if self.container[x][j] == 0:
                    for val in self.get_poss_vals(x,j):
                        col_poss.append(val)
            if len(set(poss_vals)-set(col_poss)) == 1:
                self.container[i][j] = list(set(poss_vals)-set(col_poss))[0]
                    
            #check square
            first = [0,1,2]
            second = [3,4,5]
            third = [6,7,8]
            find_square = [first,second,third]
            for l in find_square:
                if i in l:
                    row = l
                if j in l:
                    col = l
            square_poss = []
            for x in row:
                for y in col:
                    if self.container[x][y] == 0:
                        for val in self.get_poss_vals(x,y):
                            square_poss.append(val)
            if len(set(poss_vals)-set(square_poss)) == 1:
                self.container[i][j] = list(set(poss_vals)-set(square_poss))[0]
        return self.container

    