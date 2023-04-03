from minimizing_calculation_quine_method.minimizing_calculation_quine_method import QuineAndCalculationMinimizer
from minimizing_karnaugh_method.minimizing_karnaugh_method import KarnaughMinimizer


formula = '(!((!x1+!x2)&!(x1&x3)))'
good_formula = '(!((!x1+!x2)&!(x1&x3+(x3<->x4))))'
test_formula = '((!x1*!x2*x3)+(!x1*x2*!x3)+(!x1*x2*x3)+(x1*x2*!x3))'


def test_calculation_method():
    print('CALCULATION MINIMIZATION METHOD'.center(60, ' '))
    minimizer = QuineAndCalculationMinimizer(f'{good_formula}', mode='CNF')
    minimizer.minimize_func_calculation_method()
    print(f'PCNF: {minimizer.non_minimized_func}')
    print(f'Reduced CNF: {minimizer.reduced_func}')
    print(f'Minimized CNF: {minimizer.minimized_func}')
    minimizer = QuineAndCalculationMinimizer(f'{good_formula}', mode='DNF')
    minimizer.minimize_func_calculation_method()
    print(f'PDNF: {minimizer.non_minimized_func}')
    print(f'Reduced DNF: {minimizer.reduced_func}')
    print(f'Minimized DNF: {minimizer.minimized_func}')


def test_quine_method():
    print('QUINE MINIMIZATION METHOD'.center(60, ' '))
    minimizer = QuineAndCalculationMinimizer(f'{good_formula}', mode='CNF')
    minimizer.minimize_func_quine_method(debug=True)
    print(f'PCNF: {minimizer.non_minimized_func}')
    print(f'Reduced CNF: {minimizer.reduced_func}')
    print(f'Minimized CNF: {minimizer.minimized_func}')
    minimizer = QuineAndCalculationMinimizer(f'{good_formula}', mode='DNF')
    minimizer.minimize_func_quine_method(debug=True)
    print(f'PDNF: {minimizer.non_minimized_func}')
    print(f'Reduced DNF: {minimizer.reduced_func}')
    print(f'Minimized DNF: {minimizer.minimized_func}')


def test_karnaugh_method():
    print('KARNAUGH METHOD'.center(60, ' '))
    minimizer = KarnaughMinimizer(good_formula, mode='DNF')
    minimizer.print_karnaugh_map()
    print(f'Minimized DNF: {minimizer.minimized_func}')
    minimizer = KarnaughMinimizer(good_formula, mode='CNF')
    minimizer.print_karnaugh_map()
    print(f'Minimized CNF: {minimizer.minimized_func}')


if __name__ == '__main__':
    # test_calculation_method()
    # test_quine_method()
    test_karnaugh_method()
