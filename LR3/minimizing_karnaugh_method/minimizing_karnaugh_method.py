from logical_formula_solver.logical_formula_solver import LogicalFormulaSolver, FullLogicalInterpretation
from dataclasses import dataclass
from typing import Optional


@dataclass
class KarnaughMap:
    row_variables: list[str]
    col_variables: list[str]
    gray_codes_row: list[str]
    gray_codes_col: list[str]
    map: list


class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if not isinstance(other, Point):
            return False
        return self.x == other.x and self.y == other.y


class KarnaughMinimizer:
    def __init__(self, raw_formula: str, mode: str = 'DNF'):
        self.__solver = LogicalFormulaSolver(raw_formula)
        self.formula_variables = sorted(list(self.__solver.variables))
        self.formula_solution: list[FullLogicalInterpretation] = LogicalFormulaSolver(raw_formula).solve_formula()
        self.__karnaugh_map: Optional[KarnaughMap] = None
        if mode == 'DNF':
            self.look_number = 1
            self.inner_operation = ' ∧ '
            self.outer_operation = ' ∨ '
        elif mode == 'CNF':
            self.look_number = 0
            self.inner_operation = ' ∨ '
            self.outer_operation = ' ∧ '

    @staticmethod
    def __generate_gray_codes(bit_amount: int):
        gray_codes = []
        for number in range(2**bit_amount):
            gray_number = number ^ (number >> 1)
            gray_codes.append(format(gray_number, f'#0{bit_amount + 2}b').split('b')[1])
        return gray_codes

    def __build_karnaugh_map(self):
        col_variables_amount = int(len(self.formula_variables) / 2)
        col_variables = [self.formula_variables[i] for i in range(col_variables_amount)]
        row_variables = [self.formula_variables[i] for i in range(col_variables_amount, len(self.formula_variables))]
        gray_codes_for_col = self.__generate_gray_codes(len(col_variables))
        gray_codes_for_row = self.__generate_gray_codes(len(row_variables))
        karnaugh_map = KarnaughMap(row_variables, col_variables,
                                   gray_codes_for_row,
                                   gray_codes_for_col,
                                   [[0] * (2**len(row_variables)) for _ in range(2**len(col_variables))])
        for i in range(len(karnaugh_map.map)):
            for j in range(len(karnaugh_map.map[i])):
                karnaugh_map.map[i][j] = self.__get_solution_value_for_implementation(
                    gray_codes_for_col[i] + gray_codes_for_row[j])
        self.__karnaugh_map = karnaugh_map

    def __get_solution_value_for_implementation(self, implementation: str):
        variables_with_values = dict(zip(self.formula_variables, list(map(int, list(implementation)))))
        for full_implementation in self.formula_solution:
            if full_implementation.logical_interpretation == variables_with_values:
                return full_implementation.formula_value

    def __solve_karnaugh_map(self):
        covered_cells = list()
        for i in range(len(self.__karnaugh_map.map)):
            for j in range(len(self.__karnaugh_map.map[i])):
                if not self.__karnaugh_map.map[i][j] == self.look_number:
                    continue

    def print_karnaugh_map(self):
        self.__build_karnaugh_map()
        print(f'{"".join(self.__karnaugh_map.col_variables)}/{"".join(self.__karnaugh_map.row_variables)}'
              f' {" ".join(self.__karnaugh_map.gray_codes_row)}')
        for i in range(len(self.__karnaugh_map.map)):
            print(f'{self.__karnaugh_map.gray_codes_col[i]}{" " * len("".join(self.formula_variables)) + " "}'
                  f'{(" " * len(self.__karnaugh_map.row_variables)).join(list(map(str, self.__karnaugh_map.map[i])))}')

