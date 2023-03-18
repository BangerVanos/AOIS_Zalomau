from logical_formula_solver.logical_formula_solver import LogicalFormulaSolver
from logical_formula_solver.logical_formula_solver import FullLogicalInterpretation


class FcnfFdnfFormConverter:
    def __init__(self, raw_formula: str):
        self.truth_table: list[FullLogicalInterpretation] = LogicalFormulaSolver(raw_formula).solve_formula()
        self.fcnf = ''
        self.fdnf = ''
        self.fcnf_num_form = ''
        self.fdnf_num_form = ''
        truth_table_values = [implementation.formula_value for implementation in self.truth_table]
        self.formula_index = int(''.join([str(value) for value in truth_table_values]), 2)

    def build_fcnf(self):
        fcnf_implementation_numbers: list[str] = []
        implementation_number = 0
        disjunction_sets: list[str] = []
        for implementation in self.truth_table:
            if implementation.formula_value == 0:
                disjunction_set: list[str] = []
                fcnf_implementation_numbers.append(str(implementation_number))
                for var, value in implementation.logical_interpretation.items():
                    disjunction_set.append(var if value == 0 else '!'+var)
                disjunction_sets.append('('+' ∨ '.join(disjunction_set)+')')
            implementation_number += 1
        self.fcnf = ' ∧ '.join(disjunction_sets)
        self.fcnf_num_form = '∧(' + ', '.join(fcnf_implementation_numbers) + ')'

    def build_fdnf(self):
        fdnf_implementation_numbers: list[str] = []
        implementation_number = 0
        conjunction_sets: list[str] = []
        for implementation in self.truth_table:
            if implementation.formula_value == 1:
                conjunction_set: list[str] = []
                fdnf_implementation_numbers.append(str(implementation_number))
                for var, value in implementation.logical_interpretation.items():
                    conjunction_set.append(var if value == 1 else '!' + var)
                conjunction_sets.append('(' + ' ∧ '.join(conjunction_set) + ')')
            implementation_number += 1
        self.fdnf = ' ∨ '.join(conjunction_sets)
        self.fdnf_num_form = '∨(' + ', '.join(fdnf_implementation_numbers) + ')'
