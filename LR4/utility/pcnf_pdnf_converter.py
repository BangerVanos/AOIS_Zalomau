from .logical_formula_solver import LogicalFormulaSolver
from .logical_formula_solver import FullLogicalInterpretation
from typing import Union


class PcnfPdnfFormConverter:
    def __init__(self, boolean_parameter: Union[list[FullLogicalInterpretation], str]):
        #  We can pass here either ready truth table or string boolean algebra formula
        self.truth_table: list[FullLogicalInterpretation] = LogicalFormulaSolver(boolean_parameter).solve_formula()\
            if isinstance(boolean_parameter, str) else boolean_parameter
        self.__pcnf = ''
        self.__pdnf = ''
        self.pcnf_num_form = ''
        self.pdnf_num_form = ''
        truth_table_values = [implementation.formula_value for implementation in self.truth_table]
        self.formula_index = int(''.join([str(value) for value in truth_table_values]), 2)

    def build_pcnf(self):
        pcnf_implementation_numbers: list[str] = []
        implementation_number = 0
        disjunction_sets: list[str] = []
        for implementation in self.truth_table:
            if implementation.formula_value == 0:
                disjunction_set: list[str] = []
                pcnf_implementation_numbers.append(str(implementation_number))
                for var, value in implementation.logical_interpretation.items():
                    disjunction_set.append(var if value == 0 else '!'+var)
                disjunction_sets.append('('+' ∨ '.join(sorted(disjunction_set))+')')
            implementation_number += 1
        self.__pcnf = ' ∧ '.join(sorted(disjunction_sets))
        self.pcnf_num_form = '∧(' + ', '.join(pcnf_implementation_numbers) + ')'

    def build_pdnf(self):
        pdnf_implementation_numbers: list[str] = []
        implementation_number = 0
        conjunction_sets: list[str] = []
        for implementation in self.truth_table:
            if implementation.formula_value == 1:
                conjunction_set: list[str] = []
                pdnf_implementation_numbers.append(str(implementation_number))
                for var, value in implementation.logical_interpretation.items():
                    conjunction_set.append(var if value == 1 else '!' + var)
                conjunction_sets.append('(' + ' ∧ '.join(sorted(conjunction_set)) + ')')
            implementation_number += 1
        self.__pdnf = ' ∨ '.join(sorted(conjunction_sets))
        self.pdnf_num_form = '∨(' + ', '.join(pdnf_implementation_numbers) + ')'

    @property
    def pcnf(self):
        self.build_pcnf()
        return self.__pcnf

    @property
    def pdnf(self):
        self.build_pdnf()
        return self.__pdnf
