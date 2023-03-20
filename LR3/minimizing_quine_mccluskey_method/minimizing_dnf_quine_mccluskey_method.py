from fcnf_fdnf_converter.fcnf_fdnf_converter import FcnfFdnfFormConverter
from logical_formula_solver.logical_formula_solver import LogicalFormulaSolver


class QuineMcCluskeyDNFMinimizer:
    def __init__(self, raw_formula: str):
        self.non_minimized_fdnf = FcnfFdnfFormConverter(raw_formula).fdnf
        self.formula_variables = LogicalFormulaSolver(raw_formula).variables
        self.disjunctions_list = sorted(self.non_minimized_fdnf.split(' ∨ '))
        self.reduced_dnf = self.non_minimized_fdnf
        self.minimized_dnf = None

    def build_reduced_dnf(self, disjunctions_list=None):
        if disjunctions_list is None:
            disjunctions_list = self.disjunctions_list
        new_disjunctions_list = self.__build_canceled_list(disjunctions_list)
        iteration_dnf = ' ∨ '.join(sorted(new_disjunctions_list))
        if iteration_dnf != self.reduced_dnf:
            self.reduced_dnf = iteration_dnf
            self.build_reduced_dnf(disjunctions_list=new_disjunctions_list)
        else:
            return

    def __build_canceled_list(self, conjunctions_list):
        new_conjunctions_list = []
        indexes_of_canceled_conjunctions = set()
        for i in range(len(conjunctions_list)):
            conjunction_impossible_to_cancel = True
            if i in indexes_of_canceled_conjunctions:
                continue
            for j in range(len(conjunctions_list)):
                if (j in indexes_of_canceled_conjunctions) or i == j:
                    continue
                new_disjunction = self.__cancel_conjunctions(conjunctions_list[i], conjunctions_list[j])
                if new_disjunction is not None:
                    new_conjunctions_list.append(new_disjunction)
                    indexes_of_canceled_conjunctions.update([i, j])
                    conjunction_impossible_to_cancel = False
                    break
            if conjunction_impossible_to_cancel:
                new_conjunctions_list.append(conjunctions_list[i])
        return new_conjunctions_list

    def __cancel_conjunctions(self, first_conjunction: str, second_conjunction: str):
        first_conjunction_literals = self.__get_list_of_literals(first_conjunction)
        second_conjunction_literals = self.__get_list_of_literals(second_conjunction)
        if not self.__could_literals_be_canceled(first_conjunction_literals, second_conjunction_literals):
            return None
        for variable in self.formula_variables:
            if variable in first_conjunction_literals and '!' + variable in second_conjunction_literals:
                first_conjunction_literals.remove(variable)
                second_conjunction_literals.remove('!' + variable)
            elif '!' + variable in first_conjunction_literals and variable in second_conjunction_literals:
                first_conjunction_literals.remove('!' + variable)
                second_conjunction_literals.remove(variable)
        if first_conjunction_literals + second_conjunction_literals == []:
            return None
        for literal in first_conjunction_literals:
            second_conjunction_literals.remove(literal)
        return '(' + ' ∧ '.join(first_conjunction_literals + second_conjunction_literals) + ')'

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
    def __get_list_of_literals(conjunction_str: str):
        conjunction_str = conjunction_str.replace('(', '')
        conjunction_str = conjunction_str.replace(')', '')
        list_of_literals = conjunction_str.split(' ∧ ')
        return list_of_literals
