from utility.minimizing_calculation_quine_method import QuineAndCalculationMinimizer
from utility.pcnf_pdnf_converter import PcnfPdnfFormConverter
from utility.logical_formula_solver import FullLogicalInterpretation
from itertools import product


INPUT_NAMES = ('X1', 'X2', 'X3')
CARRY_NAME = 'b'
DIFFERENCE_NAME = 'd'


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
        truth_tables = get_sdbs3_truth_table()
        self.borrow_pdnf = PcnfPdnfFormConverter(truth_tables['borrow_ttb']).pdnf
        self.difference_pdnf = PcnfPdnfFormConverter(truth_tables['difference_ttb']).pdnf
        self.minimized_borrow_dnf = QuineAndCalculationMinimizer('(' + self.borrow_pdnf + ')')
        self.minimized_difference_dnf = QuineAndCalculationMinimizer('(' + self.difference_pdnf + ')')
