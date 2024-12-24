import numpy as np
from typing import List, Set
from itertools import chain

class Sudoku:

    def __init__(self):
        np.random.seed(1) # for testing purposes
        self.area = np.full(shape=(9,9), fill_value=0)

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
                    possible_elements = elements_missing_x.intersection(elements_missing_y.intersection(elements_missing_block))
                    if len(possible_elements) == 0:
                        return None
                    elif len(possible_elements) == 1:
                        s.area[y,x] = possible_elements[0]
                        return s
                    else:
                        for possible_element in possible_elements:
                            s.area[y,x] = possible_element
                            next_s = self.solve(s)
                            if next_s.fields_left() == 0:
                                return next_s
                        return None
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
                        print(possible_elements)
                        s.area[y,x] = possible_elements[0]
                        return s
                    else:
                        for possible_element in possible_elements:
                            s.area[y,x] = possible_element
                            next_s = self.solve_iterations(s, iterations - 1)
                            
                            if next_s != None and next_s.fields_left() == 0:
                                return next_s
                        return None
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
    s = Sudoku()
    print(s)
    solver = SudokuSolver()
    puzzle = solver.solve_iterations(s, 10)
    print(puzzle)