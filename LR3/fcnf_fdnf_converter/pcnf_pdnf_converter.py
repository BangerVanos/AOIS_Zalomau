from logical_formula_solver.logical_formula_solver import LogicalFormulaSolver
from logical_formula_solver.logical_formula_solver import FullLogicalInterpretation


class FcnfFdnfFormConverter:
    def __init__(self, raw_formula: str):
        self.truth_table: list[FullLogicalInterpretation] = LogicalFormulaSolver(raw_formula).solve_formula()
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
                disjunction_sets.append('('+' ∨ '.join(disjunction_set)+')')
            implementation_number += 1
        self.__pcnf = ' ∧ '.join(disjunction_sets)
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
                conjunction_sets.append('(' + ' ∧ '.join(conjunction_set) + ')')
            implementation_number += 1
        self.__pdnf = ' ∨ '.join(conjunction_sets)
        self.pdnf_num_form = '∨(' + ', '.join(pdnf_implementation_numbers) + ')'

    @property
    def pcnf(self):
        self.build_pcnf()
        return self.__pcnf

    @property
    def pdnf(self):
        self.build_pdnf()
        return self.__pdnf
