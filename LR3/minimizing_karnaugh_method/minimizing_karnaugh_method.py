from logical_formula_solver.logical_formula_solver import LogicalFormulaSolver, FullLogicalInterpretation
from dataclasses import dataclass
from typing import Optional, Union
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
    def __init__(self, x: Union[int, float], y: Union[int, float]):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if not isinstance(other, Cell):
            return False
        return self.x == other.x and self.y == other.y

    def are_cells_in_karnaugh_neighbourhood(self, other):
        if not isinstance(other, Cell):
            raise TypeError("Other object must be Cell type")
        if self.x == other.x:
            self_coordinate, other_coordinate = self.y, other.y
        elif self.y == other.y:
            self_coordinate, other_coordinate = self.x, other.x
        else:
            return False
        return abs(self_coordinate - other_coordinate) - 1 == 0 \
            or (abs(self_coordinate - other_coordinate) - 1 & abs(self_coordinate - other_coordinate) - 2 == 0
                and math.log(abs(self_coordinate - other_coordinate) - 1, 2) > 0)

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
        obligatory_areas = self.__get_obligatory_groups(self.__make_karnaugh_groups(v_mode=True))
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

    def __make_karnaugh_groups(self, v_mode: bool = True):
        karnaugh_groups = list()
        one_row_map = list(chain.from_iterable(self.__karnaugh_map.map)) if v_mode \
            else list(chain.from_iterable(list(zip(*self.__karnaugh_map.map))))
        i, j = 0, 0
        for i in range(len(one_row_map)):
            if not one_row_map[i] == self.need_number:
                continue
            karnaugh_group = [Cell(i // len(self.__karnaugh_map.map[0]), i % len(self.__karnaugh_map.map[0]))]
            last_covered_cell = i
            for j in self.__range_from_nearest_cells(i, one_row_map):
                if i == j or not one_row_map[j] == self.need_number:
                    continue
                if abs(last_covered_cell - j) - 1 & abs(last_covered_cell - j) - 2 == 0:
                    karnaugh_group.append(Cell(j // len(self.__karnaugh_map.map[0]),
                                               j % len(self.__karnaugh_map.map[0])))
                    last_covered_cell = j
            while not (len(karnaugh_group) & (len(karnaugh_group) - 1) == 0
                       and self.__is_group_rectangular(karnaugh_group)):
                karnaugh_group.pop(0 if i > j else len(karnaugh_group) - 1)
            karnaugh_groups.append(karnaugh_group)
        return karnaugh_groups

    def __make_group_for_cell(self):
        pass

    def __range_from_nearest_cells(self, first_cell_index, chain_map):
        all_cells = [Cell(i // len(self.__karnaugh_map.map[0]),
                          i % len(self.__karnaugh_map.map[0])) for i in range(len(chain_map))]
        first_cell = Cell(first_cell_index // len(self.__karnaugh_map.map[0]),
                          first_cell_index % len(self.__karnaugh_map.map[0]))
        distances = {all_cells.index(cell): first_cell.distance(cell) for cell in all_cells}
        return dict(sorted(distances.items(), key=lambda x: x[1]))

    @staticmethod
    def __get_index_of_the_remotest_point(group: list[Cell]):
        center_mass_x = sum([cell.x for cell in group]) / len(group)
        center_mass_y = sum([cell.y for cell in group]) / len(group)
        distances = []
        for cell in group:
            distances.append(Cell(center_mass_x, center_mass_y).distance(cell))
        return distances.index(max(distances))

    def __check_cell_for_neighbourhood(self, i: int, j: int):
        cell_1 = Cell(i // len(self.__karnaugh_map.map[0]), i % len(self.__karnaugh_map.map[0]))
        cell_2 = Cell(j // len(self.__karnaugh_map.map[0]), j % len(self.__karnaugh_map.map[0]))
        return cell_1.are_cells_in_karnaugh_neighbourhood(cell_2)

    @staticmethod
    def __is_group_rectangular(group: list[Cell]):
        if len(group) <= 1:
            return True
        center_mass_x = sum([cell.x for cell in group]) / len(group)
        center_mass_y = sum([cell.y for cell in group]) / len(group)
        distances = [Cell(center_mass_x, center_mass_y).distance(cell) for cell in group]
        return len(set(distances)) == len(group) // 2

    @staticmethod
    def __get_obligatory_groups(karnaugh_groups: list[list[Cell]]):
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
