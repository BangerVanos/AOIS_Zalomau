from fcnf_fdnf_converter.fcnf_fdnf_converter import FcnfFdnfFormConverter
from logical_formula_solver.logical_formula_solver import LogicalFormulaSolver


class CalculationCNFMinimizer:
    def __init__(self, raw_formula: str):
        self.non_minimized_fcnf = FcnfFdnfFormConverter(raw_formula).fcnf
        self.formula_variables = LogicalFormulaSolver(raw_formula).variables
        self.disjunctions_list = sorted(self.non_minimized_fcnf.split(' ∧ '))
        self.reduced_cnf = self.non_minimized_fcnf
        self.minimized_cnf = None

    def build_reduced_cnf(self, disjunctions_list=None):
        if disjunctions_list is None:
            disjunctions_list = self.disjunctions_list
        new_disjunctions_list = self.__build_canceled_list(disjunctions_list)
        iteration_cnf = ' ∧ '.join(sorted(new_disjunctions_list))
        if iteration_cnf != self.reduced_cnf:
            self.reduced_cnf = iteration_cnf
            self.build_reduced_cnf(disjunctions_list=new_disjunctions_list)
        else:
            return

    def __build_canceled_list(self, disjunctions_list):
        new_disjunctions_list = []
        indexes_of_canceled_disjunctions = set()
        for i in range(len(disjunctions_list)):
            disjunction_impossible_to_cancel = True
            if i in indexes_of_canceled_disjunctions:
                continue
            for j in range(len(disjunctions_list)):
                if (j in indexes_of_canceled_disjunctions) or i == j:
                    continue
                new_disjunction = self.__cancel_disjunctions(disjunctions_list[i], disjunctions_list[j])
                if new_disjunction is not None:
                    new_disjunctions_list.append(new_disjunction)
                    indexes_of_canceled_disjunctions.update([i, j])
                    disjunction_impossible_to_cancel = False
                    break
            if disjunction_impossible_to_cancel:
                new_disjunctions_list.append(disjunctions_list[i])
        return new_disjunctions_list

    def __cancel_disjunctions(self, first_disjunction: str, second_disjunction: str):
        first_disjunction_literals = self.__get_list_of_literals(first_disjunction)
        second_disjunction_literals = self.__get_list_of_literals(second_disjunction)
        if not self.__could_literals_be_canceled(first_disjunction_literals, second_disjunction_literals):
            return None
        for variable in self.formula_variables:
            if variable in first_disjunction_literals and '!' + variable in second_disjunction_literals:
                first_disjunction_literals.remove(variable)
                second_disjunction_literals.remove('!' + variable)
            elif '!' + variable in first_disjunction_literals and variable in second_disjunction_literals:
                first_disjunction_literals.remove('!' + variable)
                second_disjunction_literals.remove(variable)
        if first_disjunction_literals + second_disjunction_literals == []:
            return None
        for literal in first_disjunction_literals:
            second_disjunction_literals.remove(literal)
        return '(' + ' ∨ '.join(first_disjunction_literals + second_disjunction_literals) + ')'

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

    @staticmethod
    def __get_list_of_literals(disjunction_str: str):
        disjunction_str = disjunction_str.replace('(', '')
        disjunction_str = disjunction_str.replace(')', '')
        list_of_literals = disjunction_str.split(' ∨ ')
        return list_of_literals
