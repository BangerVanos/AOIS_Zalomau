from minimizing_calculation_method.minimizing_cnf_calculation_method import CalculationCNFMinimizer
from minimizing_calculation_method.minimizing_dnf_calculation_method import CalculationDNFMinimizer


if __name__ == '__main__':
    minimizer = CalculationCNFMinimizer('(!((!x1+!x2)&!(x1&x3)))')
    minimizer.build_reduced_cnf()
    print(f'FCNF: {minimizer.non_minimized_fcnf}')
    print(f'Reduced CNF: {minimizer.reduced_cnf}')
    minimizer = CalculationDNFMinimizer('(!((!x1+!x2)&!(x1&x3)))')
    minimizer.build_reduced_dnf()
    print(f'FDNF: {minimizer.non_minimized_fdnf}')
    print(f'Reduced DNF: {minimizer.reduced_dnf}')
