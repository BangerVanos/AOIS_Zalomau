from minimizing_calculation_method.minimizing_calculation_method import CalculationMinimizer


formula = '(!((!x1+!x2)&!(x1&x3)))'
test_formula = '((!x1*!x2*x3)+(!x1*x2*!x3)+(!x1*x2*x3)+(x1*x2*!x3))'


if __name__ == '__main__':
    print('CALCULATION MINIMIZATION METHOD'.center(60, ' '))
    minimizer = CalculationMinimizer('(!((!x1+!x2)&!(x1&x3)))', mode='CNF')
    minimizer.reduce_func()
    print(f'FCNF: {minimizer.non_minimized_func}')
    print(f'Reduced CNF: {minimizer.reduced_func}')
    print(f'Minimized CNF: {minimizer.minimized_func}')
    minimizer = CalculationMinimizer('(!((!x1+!x2)&!(x1&x3)))', mode='DNF')
    minimizer.reduce_func()
    print(f'FDNF: {minimizer.non_minimized_func}')
    print(f'Reduced DNF: {minimizer.reduced_func}')
    print(f'Minimized DNF: {minimizer.minimized_func}')
