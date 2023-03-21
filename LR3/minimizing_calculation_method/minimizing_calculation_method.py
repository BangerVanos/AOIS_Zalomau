from fcnf_fdnf_converter.fcnf_fdnf_converter import FcnfFdnfFormConverter
from logical_formula_solver.logical_formula_solver import LogicalFormulaSolver


class CalculationMinimizer:
    def __init__(self, raw_formula: str, mode: str = 'DNF'):
        self.formula_variables = LogicalFormulaSolver(raw_formula).variables
        self.mode = mode
        if mode == 'DNF':
            self.inner_operation = ' ∧ '
            self.outer_operation = ' ∨ '
            self.non_minimized_func = FcnfFdnfFormConverter(raw_formula).fdnf
        elif mode == 'CNF':
            self.inner_operation = ' ∨ '
            self.outer_operation = ' ∧ '
            self.non_minimized_func = FcnfFdnfFormConverter(raw_formula).fcnf
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
        if self.__number_of_inverted_literals(first_literals, second_literals) != 1:
            return False
        return True

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

    def __make_str_implicant(self, literals_list: list[str]):
        return '(' + self.inner_operation.join(literals_list) + ')'
