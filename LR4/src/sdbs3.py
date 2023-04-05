from utility.minimizing_calculation_quine_method import QuineAndCalculationMinimizer
from utility.pcnf_pdnf_converter import PcnfPdnfFormConverter
from utility.logical_formula_solver import FullLogicalInterpretation
from itertools import product


INPUT_NAMES = ('X1', 'X2', 'Bi')
BORROW_NAME = 'B'
DIFFERENCE_NAME = 'D'


def find_borrow_out(minuend: int, subtrahend: int, borrow_in: int):
    return int((not minuend and subtrahend) or (not minuend and borrow_in) or (subtrahend and borrow_in))


def find_difference(minuend: int, subtrahend: int, borrow_in: int):
    return int(minuend ^ subtrahend ^ borrow_in)


def get_sdbs3_truth_table():
    borrow_truth_table, difference_truth_table = [], []
    possible_input_combos = sorted(list(product([0, 1], repeat=len(INPUT_NAMES))))
    for combo in possible_input_combos:
        logical_interpretation = dict(zip(INPUT_NAMES, combo))
        borrow_truth_table.append(FullLogicalInterpretation(logical_interpretation,
                                                            find_borrow_out(combo[0], combo[1], combo[2])))
        difference_truth_table.append(FullLogicalInterpretation(logical_interpretation,
                                                                find_difference(combo[0], combo[1], combo[2])))
    return {'borrow_ttb': borrow_truth_table,
            'difference_ttb': difference_truth_table}


class SDBS3:
    def __init__(self):
        self.__truth_tables = get_sdbs3_truth_table()
        self.borrow_pdnf = PcnfPdnfFormConverter(self.__truth_tables['borrow_ttb']).pdnf
        self.difference_pdnf = PcnfPdnfFormConverter(self.__truth_tables['difference_ttb']).pdnf
        self.__borrow_dnf_minimizer = QuineAndCalculationMinimizer('(' + self.borrow_pdnf + ')')
        self.__borrow_dnf_minimizer.minimize_func_quine_method()
        self.borrow_minimized_dnf = self.__borrow_dnf_minimizer.minimized_func
        self.__difference_dnf_minimizer = QuineAndCalculationMinimizer('(' + self.difference_pdnf + ')')
        self.__difference_dnf_minimizer.minimize_func_quine_method()
        self.difference_minimized_dnf = self.__difference_dnf_minimizer.minimized_func

    def print_all(self):
        print('TRUTH TABLE'.center(13, ' '))
        print(' '.join(INPUT_NAMES) + f' {BORROW_NAME} {DIFFERENCE_NAME}')
        for i in range(len(self.__truth_tables['borrow_ttb'])):
            str_values = list(map(str, self.__truth_tables["borrow_ttb"][i].logical_interpretation.values()))
            print(f'{(" " * len(INPUT_NAMES[0])).join(str_values)}'
                  f'  {self.__truth_tables["borrow_ttb"][i].formula_value}'
                  f' {self.__truth_tables["difference_ttb"][i].formula_value}'.
                  center(len(' '.join(INPUT_NAMES) + f' {BORROW_NAME} {DIFFERENCE_NAME}')))
        print(f'BORROW PDNF: {self.borrow_pdnf}')
        print(f'BORROW MINIMIZED DNF: {self.borrow_minimized_dnf}')
        print(f'DIFFERENCE PDNF: {self.difference_pdnf}')
        print(f'DIFFERENCE MINIMIZED DNF: {self.difference_minimized_dnf}')
