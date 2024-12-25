import numpy as np
from typing import List, Set
from random import shuffle, randint

class Sudoku:

    def create_area(self):
        for y in range(9):
            for x in range(9):
                if self.area[y,x] == 0:
                    possible_values = list(range(1,10))
                    shuffle(possible_values)
                    for n in possible_values:
                        if self.is_valid(n, x, y):
                            self.area[y,x] = n
                            if self.create_area():
                                return True
                            self.area[y,x] = 0
                    return False
        return True

    def insert_zeros(self, num=10):
        possible_values = [(i, j) for i in range(9) for j in range(9)]
        for i in range(num):
            random_index = randint(0, len(possible_values)-1)
            pos = possible_values.pop(random_index)
            self.area[pos[0],pos[1]] = 0

    def __init__(self, arr=None):
        np.random.seed(2) # for testing purposes
        self.area = arr if arr else np.full(shape=(9,9), fill_value=0)
        self.create_area()
        self.insert_zeros(num=25)

    def __repr__(self):
        line = "-" * 25
        value_line = lambda x: f"- {x[0]} {x[1]} {x[2]} - {x[3]} {x[4]} {x[5]} - {x[6]} {x[7]} {x[8]} -"
        return f"""
            {line}
            {value_line(self.area[0])}
            {value_line(self.area[1])}
            {value_line(self.area[2])}
            {line}
            {value_line(self.area[3])}
            {value_line(self.area[4])}
            {value_line(self.area[5])}
            {line}
            {value_line(self.area[6])}
            {value_line(self.area[7])}
            {value_line(self.area[8])}
            {line}
        """

    def input_value(self, value, x, y):
        # check if placement is allowed
        if value in self.area[y,:] or value in self.area[:,x]: # check row and col
            return
        # check if value is in the block
        x_block = (x // 3) * 3
        y_block = (y // 3) * 3
        if value in self.area[y_block:y_block+3,x_block:x_block+3].flatten():
            return
        self.area[y,x] = value

    def is_valid(self, value, x, y):
        # check if placement is allowed
        if value in self.area[y,:] or value in self.area[:,x]: # check row and col
            return False
        # check if value is in the block
        x_block = (x // 3) * 3
        y_block = (y // 3) * 3
        if value in self.area[y_block:y_block+3,x_block:x_block+3].flatten():
            return False
        return True

    def fields_left(self):
        return 9 * 9 - np.count_nonzero(self.area)

class SudokuSolver:

    def __init__(self):
        pass

    def solve(self, s: Sudoku):
        # TODO: Implement
        # 1. Freies Feld aussuchen
        # 2. Überprüfen, welche Zahl eingesetzt werden kann (Reihe, Spalte und Block überprüfen, Schnittmenge bilden)
        # 3. Wenn nur eine Zahl möglich, dann einfach einsetzen und true zurückgeben
        # 4. Wenn keine Zahl möglich, dann false zurückgeben
        # 5. Wenn mehrere Zahlen möglich, dann eine einsetzen und rekursiv versuchen ein nächstes Feld zu belegen
        # 6. Wird mit einer Zahl true zurückgegeben, kann true zurückgegeben werden
        # 7. Schafft es keine Zahl, zum Schluss false zurückgeben


        for y, elem_y in enumerate(s.area):
            for x, elem in enumerate(elem_y):
                if elem == 0:
                    elements_missing_y = self.get_missing_elements(s.area[y,:])
                    elements_missing_x = self.get_missing_elements(s.area[:,x])
                    x_block = (x // 3) * 3
                    y_block = (y // 3) * 3
                    elements_missing_block = self.get_missing_elements(s.area[y_block:y_block+3,x_block:x_block+3])
                    possible_elements = list(elements_missing_x.intersection(elements_missing_y.intersection(elements_missing_block)))
                    if len(possible_elements) == 0:
                        return None
                    else:
                        for possible_element in possible_elements:
                            s.area[y,x] = possible_element
                            next_s = self.solve(s)
                            if next_s == None:
                                continue
                            if next_s.fields_left() == 0:
                                return next_s
        return s

    def solve_iterations(self, s: Sudoku, iterations: int):
        # TODO: Implement
        # 1. Freies Feld aussuchen
        # 2. Überprüfen, welche Zahl eingesetzt werden kann (Reihe, Spalte und Block überprüfen, Schnittmenge bilden)
        # 3. Wenn nur eine Zahl möglich, dann einfach einsetzen und true zurückgeben
        # 4. Wenn keine Zahl möglich, dann false zurückgeben
        # 5. Wenn mehrere Zahlen möglich, dann eine einsetzen und rekursiv versuchen ein nächstes Feld zu belegen
        # 6. Wird mit einer Zahl true zurückgegeben, kann true zurückgegeben werden
        # 7. Schafft es keine Zahl, zum Schluss false zurückgeben
        if iterations == 0:
            return s

        for y, elem_y in enumerate(s.area):
            for x, elem in enumerate(elem_y):
                if elem == 0:
                    elements_missing_y = self.get_missing_elements(s.area[y,:])
                    elements_missing_x = self.get_missing_elements(s.area[:,x])
                    x_block = (x // 3) * 3
                    y_block = (y // 3) * 3
                    elements_missing_block = self.get_missing_elements(s.area[y_block:y_block+3,x_block:x_block+3])
                    possible_elements = list(elements_missing_x.intersection(elements_missing_y.intersection(elements_missing_block)))
                    if len(possible_elements) == 0:
                        return None
                    elif len(possible_elements) == 1:
                        s.area[y,x] = possible_elements[0]
                        return s
                    else:
                        for possible_element in possible_elements:
                            s.area[y,x] = possible_element
                            s_next = self.solve_iterations(s, iterations - 1)
                            if s_next != None:
                                return s_next
        return s

    def get_missing_elements(self, arr) -> Set[int]:
        ''''''
        arr = np.ndarray.flatten(arr) # make sure arr is always a one dimensional list
        current_elements = [x for x in range(1, 10)]
        for element in arr:
            if element in current_elements:
                try:
                    current_elements.remove(element)
                except ValueError:
                    pass
        return set(current_elements)

if __name__ == '__main__':

    data = np.array([
        [4,3,0,1,8,0,2,9,0],
        [0,0,1,0,0,9,0,0,6],
        [2,9,0,6,4,0,8,7,0],
        [0,0,8,0,0,5,0,0,4],
        [3,6,0,8,7,1,0,5,2],
        [9,0,0,4,0,0,7,0,0],
        [0,8,7,0,5,2,0,4,3],
        [5,0,0,3,0,0,1,0,0],
        [0,4,3,0,1,8,0,2,9]
    ])

    #s = Sudoku(arr=data)
    s = Sudoku()
    print(s)
    solver = SudokuSolver()
    s_solved = solver.solve(s)
    print(s_solved)