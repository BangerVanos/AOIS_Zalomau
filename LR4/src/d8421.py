from utility.minimizing_calculation_quine_method import QuineAndCalculationMinimizer
from utility.pcnf_pdnf_converter import PcnfPdnfFormConverter
from utility.logical_formula_solver import FullLogicalInterpretation
from typing import Optional
from itertools import product
from copy import deepcopy


INPUT_NAMES = ('X1', 'X2', 'X3', 'X4')
OUTPUT_NAMES = ('Y1', 'Y2', 'Y3', 'Y4')


class BinaryDecimalSynthesizer:
    def __init__(self, shift_number: int = 1):
        self.__truth_tables: Optional[list[list[FullLogicalInterpretation]]] = list()
        self.__shift_number = shift_number
        self.__minimized_funcs: Optional[list[str]] = list()

    def __build_truth_tables(self):
        for i in range(4):
            truth_table = self.__build_truth_table(i)
            self.__truth_tables.append(truth_table)

    def __build_truth_table(self, output_index: int):
        truth_table = []
        for i in range(16):
            input_values = '{0:04b}'.format(i)
            full_logical_interpretation = FullLogicalInterpretation(
                dict(zip(INPUT_NAMES, map(int, list(input_values)))), 0)
            if i <= 9:
                full_logical_interpretation.formula_value = int('{0:04b}'.format(i + self.__shift_number)[output_index])
            else:
                full_logical_interpretation.formula_value = -1
            truth_table.append(full_logical_interpretation)
        return truth_table

    def __find_shortest_funcs(self):
        for i in range(4):
            self.__minimized_funcs.append(self.__find_shortest_func(i))

    def __find_shortest_func(self, table_index: int):
        possible_complementions = sorted(list(product([0, 1], repeat=6)))
        all_dnfs: list[str] = list()
        all_cnfs: list[str] = list()
        for complemention in possible_complementions:
            complemented_truth_table = deepcopy(self.__truth_tables[table_index])
            for i in range(10, 16):
                complemented_truth_table[i].formula_value = complemention[i - 10]
            pnf_converter = PcnfPdnfFormConverter(complemented_truth_table)
            pcnf, pdnf = pnf_converter.pcnf, pnf_converter.pdnf
            dnf_minimizer = QuineAndCalculationMinimizer('(' + pdnf + ')')
            cnf_minimizer = QuineAndCalculationMinimizer('(' + pdnf + ')', mode='CNF')
            dnf_minimizer.minimize_func_quine_method()
            cnf_minimizer.minimize_func_quine_method()
            all_dnfs.append(dnf_minimizer.minimized_func)
            all_cnfs.append(cnf_minimizer.minimized_func)
        return sorted(all_cnfs, key=len)[0] if len(sorted(all_cnfs, key=len)[0]) < len(sorted(all_dnfs, key=len)[0])\
            else sorted(all_dnfs, key=len)[0]

    def solve_all(self):
        self.__build_truth_tables()
        self.__find_shortest_funcs()

    def print_all(self):
        self.solve_all()
        print('TRUTH TABLE'.center(25))
        print(' '.join(INPUT_NAMES) + ' ' + ' '. join(OUTPUT_NAMES))
        for i in range(16):
            interpretation_line = '  '.join(list(map(str, self.__truth_tables[0][i].logical_interpretation.values())))
            values_line = '  '.join(['-' if value == -1 else str(value) for value in
                                     [truth_table[i].formula_value for truth_table in self.__truth_tables]])
            print(f'{interpretation_line}  {values_line}')
        print('Minimized functions:')
        for i in range(4):
            print(f'{OUTPUT_NAMES[i]}: Fmin = {self.__minimized_funcs[i]}')
