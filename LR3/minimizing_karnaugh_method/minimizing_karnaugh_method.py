from logical_formula_solver.logical_formula_solver import LogicalFormulaSolver, FullLogicalInterpretation


class KarnaughMinimizer:
    def __init__(self, raw_formula: str, mode: str = 'DNF'):
        self.formula_variables = LogicalFormulaSolver(raw_formula).variables
        self.solution: list[FullLogicalInterpretation] = LogicalFormulaSolver(raw_formula).solve_formula()
        if mode == 'DNF':
            self.look_number = 1
            self.inner_operation = ' ∧ '
            self.outer_operation = ' ∨ '
        elif mode == 'CNF':
            self.look_number = 0
            self.inner_operation = ' ∨ '
            self.outer_operation = ' ∧ '

    @staticmethod
    def __generate_gray_codes(bit_amount: int, first_number: int = 0, last_number: int = 0):
        gray_codes = []
        for number in range(first_number, last_number):
            gray_number = number ^ (number >> 1)
            gray_codes.append(format(gray_number, f'#0{bit_amount + 2}b').split('b')[1])
        return gray_codes
