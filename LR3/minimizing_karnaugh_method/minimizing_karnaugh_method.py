from logical_formula_solver.logical_formula_solver import LogicalFormulaSolver, FullLogicalInterpretation
from dataclasses import dataclass
from typing import Optional
import math
from itertools import chain


@dataclass
class KarnaughMap:
    row_variables: list[str]
    col_variables: list[str]
    gray_codes_row: list[str]
    gray_codes_col: list[str]
    map: list


class Cell:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if not isinstance(other, Cell):
            return False
        return self.x == other.x and self.y == other.y

    def are_points_in_karnaugh_neighbourhood(self, other):
        if not isinstance(other, Cell):
            return False
        if self.x == other.x:
            return abs(self.y - other.y) - 1 == 0 or (int(math.log(abs(self.y - other.y) - 1, 2)) ==
                                                      math.log(abs(self.y - other.y) - 1, 2)
                                                      and math.log(abs(self.y - other.y) - 1, 2) > 0)
        elif self.y == other.y:
            return abs(self.x - other.x) - 1 == 0 or (int(math.log(abs(self.x - other.x) - 1, 2)) ==
                                                      math.log(abs(self.x - other.x) - 1, 2)
                                                      and math.log(abs(self.x - other.x) - 1, 2) > 0)
        return False

    def __repr__(self):
        return f'Point: ({self.x}, {self.y})'


class KarnaughMinimizer:
    def __init__(self, raw_formula: str, mode: str = 'DNF'):
        self.__solver = LogicalFormulaSolver(raw_formula)
        self.formula_variables = sorted(list(self.__solver.variables))
        self.formula_solution: list[FullLogicalInterpretation] = LogicalFormulaSolver(raw_formula).solve_formula()
        self.__karnaugh_map: Optional[KarnaughMap] = None
        if mode == 'DNF':
            self.need_number = 1
            self.inner_operation = ' ∧ '
            self.outer_operation = ' ∨ '
        elif mode == 'CNF':
            self.need_number = 0
            self.inner_operation = ' ∨ '
            self.outer_operation = ' ∧ '
        self.__minimized_func: Optional[str] = None

    @property
    def minimized_func(self) -> str:
        self.__build_karnaugh_map()
        self.__solve_karnaugh_map(self.__make_karnaugh_areas())
        return self.__minimized_func

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

    def __make_karnaugh_areas(self):
        karnaugh_areas = list()
        one_row_map = list(chain.from_iterable(self.__karnaugh_map.map))
        i, j = 0, 0
        for i in range(len(one_row_map)):
            if not one_row_map[i] == self.need_number:
                continue
            karnaugh_area = [Cell(i // len(self.__karnaugh_map.map[0]), i % len(self.__karnaugh_map.map[0]))]
            last_covered_cell = i
            for j in range(len(one_row_map)):
                if i == j:
                    continue
                if one_row_map[j] == self.need_number and self.__check_cell_for_neighbourhood(last_covered_cell, j):
                    karnaugh_area.append(Cell(j // len(self.__karnaugh_map.map[0]),
                                              j % len(self.__karnaugh_map.map[0])))
                    last_covered_cell = j
            while not (int(math.log(len(karnaugh_area), 2)) == math.log(len(karnaugh_area), 2)
                       and self.__is_area_rectangular(karnaugh_area)):
                karnaugh_area.pop(0 if i > j else len(karnaugh_area) - 1)
            karnaugh_areas.append(karnaugh_area)
        return self.__get_obligatory_areas(karnaugh_areas)

    def __check_cell_for_neighbourhood(self, i: int, j: int):
        point_1 = Cell(i // len(self.__karnaugh_map.map[0]), i % len(self.__karnaugh_map.map[0]))
        point_2 = Cell(j // len(self.__karnaugh_map.map[0]), j % len(self.__karnaugh_map.map[0]))
        return point_1.are_points_in_karnaugh_neighbourhood(point_2)

    @staticmethod
    def __is_area_rectangular(area):
        if len(area) <= 2:
            return True
        is_there_horizontal_symmetry = True if len(set([point.x for point in area])) <= 1 else False
        is_there_vertical_symmetry = True if len(set([point.y for point in area])) <= 1 else False
        if is_there_vertical_symmetry or is_there_horizontal_symmetry:
            return True
        for cell in area:
            for other_cell in area:
                is_there_horizontal_symmetry = False
                is_there_vertical_symmetry = False
                if cell.x == other_cell.x:
                    is_there_horizontal_symmetry = True
                elif cell.y == other_cell.y:
                    is_there_vertical_symmetry = True
            if not (is_there_vertical_symmetry and is_there_horizontal_symmetry):
                return False
        return True

    @staticmethod
    def __get_obligatory_areas(karnaugh_areas: list[list[Cell]]):
        covered_cells = list()
        karnaugh_areas = sorted(karnaugh_areas, key=len, reverse=True)
        obligatory_areas = list()
        for area in karnaugh_areas:
            if not all([cell in covered_cells for cell in area]):
                obligatory_areas.append(area)
                covered_cells.extend(area)
        return obligatory_areas

    def __solve_karnaugh_map(self, karnaugh_areas):
        terms = list()
        for area in karnaugh_areas:
            terms.append(self.__make_term_for_area(area))
        self.__minimized_func = self.outer_operation.join(terms)

    def __make_term_for_area(self, karnaugh_area):
        literals = list()
        variables_values = {variable: [] for variable in self.formula_variables}
        for point in karnaugh_area:
            for i in range(len(self.__karnaugh_map.row_variables)):
                variables_values[self.__karnaugh_map.row_variables[i]]\
                    .append(int(self.__karnaugh_map.gray_codes_row[point.y][i]))
            for i in range(len(self.__karnaugh_map.col_variables)):
                variables_values[self.__karnaugh_map.col_variables[i]]\
                    .append(int(self.__karnaugh_map.gray_codes_col[point.x][i]))
        for variable in self.formula_variables:
            if len(set(variables_values[variable])) <= 1:
                literals.append('!' * (self.need_number ^ variables_values[variable].pop()) + variable)
        return '(' + self.inner_operation.join(literals) + ')'

    def print_karnaugh_map(self):
        self.__build_karnaugh_map()
        print(f'{"".join(self.__karnaugh_map.col_variables)}/{"".join(self.__karnaugh_map.row_variables)}'
              f' {" ".join(self.__karnaugh_map.gray_codes_row)}')
        for i in range(len(self.__karnaugh_map.map)):
            print(f'{self.__karnaugh_map.gray_codes_col[i]}{" " * len("".join(self.formula_variables)) + " "}'
                  f'{(" " * len(self.__karnaugh_map.row_variables)).join(list(map(str, self.__karnaugh_map.map[i])))}')

