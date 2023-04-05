from utility.minimizing_calculation_quine_method import QuineAndCalculationMinimizer
from utility.pcnf_pdnf_converter import PcnfPdnfFormConverter
from utility.logical_formula_solver import FullLogicalInterpretation
from typing import Optional


INPUT_NAMES = ('X1', 'X2', 'X3', 'X4')
OUTPUT_NAMES = ('Y1', 'Y2', 'Y3', 'Y4')


class BinaryDecimalSynthesizer:
    def __init_(self, shift_number):
        self.__truth_tables: Optional[list[list[FullLogicalInterpretation]]] = None
        self.__shift_number = shift_number

    def __build_truth_tables(self):
        pass
