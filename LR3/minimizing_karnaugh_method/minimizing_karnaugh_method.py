from logical_formula_solver.logical_formula_solver import LogicalFormulaSolver, FullLogicalInterpretation
from dataclasses import dataclass
from typing import Optional, Union
import math
from itertools import chain, combinations


@dataclass
class KarnaughMap:
    row_variables: list[str]
    col_variables: list[str]
    gray_codes_row: list[str]
    gray_codes_col: list[str]
    map: list


class Cell:
    def __init__(self, x: Union[int, float], y: Union[int, float]):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if not isinstance(other, Cell):
            return False
        return self.x == other.x and self.y == other.y

    def __gt__(self, other):
        if not isinstance(other, Cell):
            return False
        return self.distance(Cell(0, 0)) > other.distance(Cell(0, 0))

    def __lt__(self, other):
        if not isinstance(other, Cell):
            return False
        return self.distance(Cell(0, 0)) < other.distance(Cell(0, 0))

    def __ge__(self, other):
        if not isinstance(other, Cell):
            return False
        return self.distance(Cell(0, 0)) >= other.distance(Cell(0, 0))

    def __le__(self, other):
        if not isinstance(other, Cell):
            return False
        return self.distance(Cell(0, 0)) <= other.distance(Cell(0, 0))

    def distance(self, other):
        if not isinstance(other, Cell):
            raise TypeError("Other object must be Cell type")
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    def __repr__(self):
        return f'Cell: ({self.x}, {self.y})'


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
        obligatory_areas = self.__get_obligatory_groups(self.__make_karnaugh_groups())
        self.__solve_karnaugh_map(obligatory_areas)
        return self.__minimized_func

    @staticmethod
    def __generate_gray_codes(bit_amount: int):
        gray_codes = []
        for number in range(2 ** bit_amount):
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
                                   [[0] * (2 ** len(row_variables)) for _ in range(2 ** len(col_variables))])
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

    def __make_karnaugh_groups(self):
        all_need_number_cells: list[Cell] = [Cell(i, j) for i in range(len(self.__karnaugh_map.map))
                                             for j in range(len(self.__karnaugh_map.map[i]))
                                             if self.__karnaugh_map.map[i][j] == self.need_number]
        all_possible_groups: list[tuple[Cell]] = list()
        max_possible_group_size = int(math.log(len(list(chain.from_iterable(self.__karnaugh_map.map))), 2))
        for i in range(max_possible_group_size + 1):
            all_possible_groups.extend(combinations(all_need_number_cells, 2 ** i))
        all_possible_groups = list(filter(lambda group: self.__is_group_rectangular(group), all_possible_groups))
        all_possible_groups = list(filter(lambda group: self.__is_karnaugh_neigbourhood(group), all_possible_groups))
        return all_possible_groups

    @staticmethod
    def __is_karnaugh_neigbourhood(group: Union[list[Cell], tuple[Cell]]):
        if len(group) <= 1:
            return True
        mass_center_x = sum([cell.x for cell in group]) / len(group)
        mass_center_y = sum([cell.y for cell in group]) / len(group)
        mass_center = Cell(mass_center_x, mass_center_y)
        distances = [(cell, mass_center.distance(cell)) for cell in group]
        min_distance = distances[0]
        for distance in distances:
            if distance[1] < min_distance[1]:
                min_distance = distance
        if min_distance[0].x == mass_center.x or min_distance[0].y == mass_center.y:
            return min_distance[1] - int(min_distance[1]) == 0.5
        projection_x = abs(mass_center_x - min_distance[0].x)
        projection_y = abs(mass_center_y - min_distance[0].y)
        return projection_x - int(projection_x) == 0.5 and projection_y - int(projection_y) == 0.5

    def __is_group_rectangular(self, group: Union[list[Cell], tuple[Cell]]):
        if len(group) <= 1:
            return True
        else:
            if len(set([cell.x for cell in group])) == 1 or len(set([cell.y for cell in group])) == 1:
                return True
            else:
                return self.__check_for_common_rectangularity(group)

    @staticmethod
    def __check_for_common_rectangularity(group: Union[list[Cell], tuple[Cell]]):
        x_lines_amount = len(set([cell.x for cell in group]))
        y_lines_amount = len(set([cell.y for cell in group]))
        for cell in group:
            x_y_symmetry = [0, 0]
            for other_cell in group:
                if cell == other_cell:
                    continue
                if cell.x == other_cell.x:
                    x_y_symmetry[0] += 1
                elif cell.y == other_cell.y:
                    x_y_symmetry[1] += 1
            if not x_y_symmetry == [x_lines_amount - 1, y_lines_amount - 1]:
                return False
        mass_center_x = sum([cell.x for cell in group]) / len(group)
        mass_center_y = sum([cell.y for cell in group]) / len(group)
        mass_center = Cell(mass_center_x, mass_center_y)
        distances = [mass_center.distance(cell) for cell in group]
        return len(set(distances)) == len(distances) // 2 or (len(set(distances)) == 1)

    @staticmethod
    def __get_obligatory_groups(karnaugh_groups: Union[list[list[Cell]], list[tuple[Cell]]]):
        karnaugh_groups = sorted(karnaugh_groups, key=len, reverse=True)
        covered_cells = list()
        obligatory_groups = list()
        for group in karnaugh_groups:
            if not all([cell in covered_cells for cell in group]):
                obligatory_groups.append(group)
                covered_cells.extend(group)
        return obligatory_groups

    def __solve_karnaugh_map(self, karnaugh_groups):
        terms = list()
        for group in karnaugh_groups:
            terms.append(self.__make_term_for_group(group))
        self.__minimized_func = self.outer_operation.join(terms)

    def __make_term_for_group(self, karnaugh_group):
        literals = list()
        variables_values = {variable: [] for variable in self.formula_variables}
        for cell in karnaugh_group:
            for i in range(len(self.__karnaugh_map.row_variables)):
                variables_values[self.__karnaugh_map.row_variables[i]] \
                    .append(int(self.__karnaugh_map.gray_codes_row[cell.y][i]))
            for i in range(len(self.__karnaugh_map.col_variables)):
                variables_values[self.__karnaugh_map.col_variables[i]] \
                    .append(int(self.__karnaugh_map.gray_codes_col[cell.x][i]))
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
