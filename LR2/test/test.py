from conjuctive_form_converter.logical_formula_solver import LogicalFormulaSolver
from conjuctive_form_converter.fcnf_fdnf_converter import FcnfFdnfFormConverter


formula: str = '!((x1+x2)&!(x1&!x3))'
formula_solver = LogicalFormulaSolver(formula)
formula_solver.beautiful_result_print()
fcnf_fdnf_converter = FcnfFdnfFormConverter(formula)
fcnf_fdnf_converter.build_fcnf()
fcnf_fdnf_converter.build_fdnf()
print(f'FCNF: {fcnf_fdnf_converter.fcnf}\n'
      f'FCNF number form: {fcnf_fdnf_converter.fcnf_num_form}\n'
      f'FDNF: {fcnf_fdnf_converter.fdnf}\n'
      f'FDNF number form: {fcnf_fdnf_converter.fdnf_num_form}\n'
      f'Formula index: {fcnf_fdnf_converter.formula_index}')
