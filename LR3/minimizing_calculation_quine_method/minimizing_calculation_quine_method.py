from fcnf_fdnf_converter.pcnf_pdnf_converter import FcnfFdnfFormConverter
from logical_formula_solver.logical_formula_solver import LogicalFormulaSolver, FullLogicalInterpretation


class QuineAndCalculationMinimizer:
    def __init__(self, raw_formula: str, mode: str = 'DNF'):
        self.__solver = LogicalFormulaSolver(raw_formula)
        self.formula_variables = self.__solver.variables
        if mode == 'DNF':
            self.inner_operation = ' ∧ '
            self.outer_operation = ' ∨ '
            self.non_minimized_func = FcnfFdnfFormConverter(raw_formula).pdnf
        elif mode == 'CNF':
            self.inner_operation = ' ∨ '
            self.outer_operation = ' ∧ '
            self.non_minimized_func = FcnfFdnfFormConverter(raw_formula).pcnf
        self.implicants_list = sorted(self.non_minimized_func.split(self.outer_operation))
        self.reduced_func = self.non_minimized_func
        self.minimized_func = None

    def reduce_func(self, implicants_list=None):
        if implicants_list is None:
            implicants_list = self.implicants_list
        new_implicants_list = self.__build_concatenated_implicants_list(implicants_list)
        iteration_func = self.outer_operation.join(set(sorted(new_implicants_list)))
        if iteration_func != self.reduced_func:
            self.reduced_func = iteration_func
            self.reduce_func(implicants_list=new_implicants_list)
        else:
            return

    def __build_concatenated_implicants_list(self, implicants_list):
        new_implicants_list = []
        concatenated_implicants = []
        for i in range(len(implicants_list)):
            for j in range(len(implicants_list)):
                if i == j:
                    continue
                new_implicant = self.__concatenate_implicants(implicants_list[i], implicants_list[j])
                if new_implicant is not None:
                    new_implicants_list.append(new_implicant)
                    concatenated_implicants += [implicants_list[i], implicants_list[j]]
        new_implicants_list += [i for i in implicants_list if i not in concatenated_implicants]
        return new_implicants_list

    def __concatenate_implicants(self, first_implicant: str, second_implicant: str):
        first_implicant_literals = self.__get_list_of_literals(first_implicant)
        second_implicant_literals = self.__get_list_of_literals(second_implicant)
        if not self.__could_literals_be_canceled(first_implicant_literals, second_implicant_literals):
            return None
        for variable in self.formula_variables:
            if variable in first_implicant_literals and '!' + variable in second_implicant_literals:
                first_implicant_literals.remove(variable)
                second_implicant_literals.remove('!' + variable)
            elif '!' + variable in first_implicant_literals and variable in second_implicant_literals:
                first_implicant_literals.remove('!' + variable)
                second_implicant_literals.remove(variable)
        if first_implicant_literals + second_implicant_literals == []:
            return None
        for literal in first_implicant_literals:
            second_implicant_literals.remove(literal)
        return self.__make_str_implicant(first_implicant_literals + second_implicant_literals)

    def __could_literals_be_canceled(self, first_literals: list[str], second_literals: list[str]):
        if len(first_literals) != len(second_literals):
            return False
        for literal in first_literals:
            if not (literal in second_literals or literal.replace('!', '') in second_literals):
                return False
        return self.__number_of_inverted_literals(first_literals, second_literals) == 1

    def __number_of_inverted_literals(self, first_literals: list[str], second_literals: list[str]):
        number_of_inverted_literals = 0
        for variable in self.formula_variables:
            if variable in first_literals and '!' + variable in second_literals:
                number_of_inverted_literals += 1
            elif '!' + variable in first_literals and variable in second_literals:
                number_of_inverted_literals += 1
        return number_of_inverted_literals

    def __get_list_of_literals(self, implicant_str: str):
        implicant_str = implicant_str.replace('(', '')
        implicant_str = implicant_str.replace(')', '')
        list_of_literals = implicant_str.split(self.inner_operation)
        return list_of_literals

    def minimize_func_calculation_method(self):
        self.__solver.beautiful_result_print()
        self.reduce_func()
        implicants_list = self.reduced_func.split(self.outer_operation)
        necessary_implicants, unnecessary_implicants = [], []
        solution_for_reduced_func = LogicalFormulaSolver('(' + self.reduced_func + ')').solve_formula()
        for implicant in implicants_list:
            shortened_implicants_list = [i for i in implicants_list if i != implicant]
            new_formula = '(' + self.outer_operation.join(shortened_implicants_list) + ')'
            solution_for_shortened_func = LogicalFormulaSolver(new_formula).solve_formula()
            if not self.__get_solution_vector(solution_for_shortened_func) == self.__get_solution_vector(
                    solution_for_reduced_func):
                necessary_implicants.append(implicant)
            else:
                unnecessary_implicants.append(implicant)
        shortened_func = self.outer_operation.join(necessary_implicants)
        solution_for_shortened_func = LogicalFormulaSolver('(' + shortened_func + ')').solve_formula()
        if not self.__get_solution_vector(solution_for_shortened_func) == self.__get_solution_vector(
                solution_for_reduced_func):
            necessary_implicants = self.__recover_implicants(necessary_implicants, unnecessary_implicants)
        self.minimized_func = self.outer_operation.join(sorted(necessary_implicants, key=len))

    def __recover_implicants(self, necessary_implicants: list[str], unnecessary_implicants: list[str]):
        unnecessary_implicants.sort(key=len, reverse=True)
        shortened_func = self.outer_operation.join(necessary_implicants)
        solution_for_shortened_func = LogicalFormulaSolver('(' + shortened_func + ')').solve_formula()
        solution_for_reduced_func = LogicalFormulaSolver('(' + self.reduced_func + ')').solve_formula()
        while not self.__get_solution_vector(solution_for_shortened_func) == self.__get_solution_vector(
                solution_for_reduced_func):
            necessary_implicants.append(unnecessary_implicants.pop())
            shortened_func = self.outer_operation.join(necessary_implicants)
            solution_for_shortened_func = LogicalFormulaSolver('(' + shortened_func + ')').solve_formula()
        return necessary_implicants

    def minimize_func_quine_method(self, debug: bool = False):
        self.__solver.beautiful_result_print()
        self.reduce_func()
        reduced_func_implicants = self.reduced_func.split(self.outer_operation)
        implicant_table = self.__fill_implicant_table(reduced_func_implicants)
        if debug:
            self.__print_implicant_table(reduced_func_implicants, implicant_table)
        core_implicants = self.__find_core_implicants(reduced_func_implicants, implicant_table)
        rest_implicants = self.__find_rest_implicants(reduced_func_implicants, implicant_table, core_implicants)
        self.minimized_func = self.outer_operation.join(sorted(core_implicants.union(rest_implicants), key=len))

    @staticmethod
    def __find_core_implicants(reduced_func_implicants: list[str], implicant_table):
        convenient_implicant_table = list(map(list, zip(*implicant_table)))
        core_implicants = set()
        for col in convenient_implicant_table:
            if sum(col) == 1:
                core_implicants.add(reduced_func_implicants[col.index(1)])
        return core_implicants

    @staticmethod
    def __find_rest_implicants(reduced_func_implicants: list[str], implicant_table, core_implicants):
        convenient_implicant_table = list(map(list, zip(*implicant_table)))
        rest_implicants = set()
        for col in convenient_implicant_table:
            col_cover_implicants = [reduced_func_implicants[j]
                                    for j in range(len(col)) if col[j] == 1]
            if any(implicant in core_implicants for implicant in col_cover_implicants):
                continue
            col_cover_implicants.sort(key=len, reverse=True)
            rest_implicants.add(col_cover_implicants.pop())
        return rest_implicants

    def __print_implicant_table(self, reduced_func_implicants: list[str], implicant_table):
        amount_of_delimiters = len(' ' * 20 + ' '.join(self.implicants_list))
        print('IMPLICANTS TABLE\n'.center(amount_of_delimiters, ' '))
        print(' ' * 20 + ' '.join(self.implicants_list))
        print('—' * amount_of_delimiters)
        for i in range(len(implicant_table)):
            print(reduced_func_implicants[i].center(20, ' ') +
                  ' '.join(['X'.center(len(self.implicants_list[j]), ' ') if implicant_table[i][j] == 1
                            else ' '.center(len(self.implicants_list[j]), ' ')
                            for j in range(len(implicant_table[i]))]).center(
                      len(' '.join(self.implicants_list)), ' '
                  ))
            print('—' * amount_of_delimiters)

    def __does_constituent_absorb_implicant(self, implicant: str, constituent: str):
        implicant_literals = self.__get_list_of_literals(implicant)
        constituent_literals = self.__get_list_of_literals(constituent)
        for literal in implicant_literals:
            if literal not in constituent_literals:
                return False
        return True

    def __fill_implicant_table(self, reduced_func_implicants: list[str]):
        implicant_table = [[0] * len(self.implicants_list) for _ in range(len(reduced_func_implicants))]
        for i in range(len(implicant_table)):
            for j in range(len(implicant_table[i])):
                if self.__does_constituent_absorb_implicant(reduced_func_implicants[i], self.implicants_list[j]):
                    implicant_table[i][j] = 1
        return implicant_table

    @staticmethod
    def __get_solution_vector(solution: list[FullLogicalInterpretation]):
        return ''.join([str(interpretation.formula_value) for interpretation in solution])

    def __make_str_implicant(self, literals_list: list[str]):
        return '(' + self.inner_operation.join(literals_list) + ')'
