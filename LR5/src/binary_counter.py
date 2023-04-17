from utility.minimizing_calculation_quine_method import QuineAndCalculationMinimizer
from utility.pcnf_pdnf_converter import PcnfPdnfFormConverter
from utility.logical_formula_solver import FullLogicalInterpretation

FSM_SIGNAL_NAME = 'V'
PRE_TACT_INPUT_NAMES = ('q1', 'q2', 'q3')
POST_TACT_INPUT_NAMES = ('Q1', 'Q2', 'Q3')
TRIGGER_FUNCTION_NAMES = ('H1', 'H2', 'H3')


def get_binary_counter_truth_tables():
    trigger_truth_tables = {'H1_tt': [], 'H2_tt': [], 'H3_tt': []}
    for i in range(16):
        pre_tact_number = i // 2
        fsm_signal = i % 2
        post_tact_number = pre_tact_number + fsm_signal
        pre_tact_inputs = list(map(int, list('{0:03b}'.format(pre_tact_number)[-3:])))
        post_tact_inputs = list(map(int, list('{0:03b}'.format(post_tact_number)[-3:])))
        for j in range(1, 4):
            trigger_truth_tables[f'H{j}_tt'].append(FullLogicalInterpretation(dict(list(zip(POST_TACT_INPUT_NAMES,
                                                                                            post_tact_inputs)) +
                                                                                   [(FSM_SIGNAL_NAME, fsm_signal)]),
                                                                              formula_value=int(pre_tact_inputs[j - 1]
                                                                                                != post_tact_inputs[
                                                                                                    j - 1])))
    return trigger_truth_tables


class BinaryCounter:
    def __init__(self):
        self.__trigger_truth_tables = get_binary_counter_truth_tables()
        self.__minimized_trigger_funcs = dict(zip(TRIGGER_FUNCTION_NAMES, [None] * len(TRIGGER_FUNCTION_NAMES)))

    @property
    def minimized_trigger_funcs(self):
        for trigger in TRIGGER_FUNCTION_NAMES:
            self.__minimized_trigger_funcs[trigger] = self.__find_minimized_func(self.__trigger_truth_tables[
                                                                                     f'{trigger}_tt'])
        return self.__minimized_trigger_funcs

    @staticmethod
    def __find_minimized_func(truth_table: list[FullLogicalInterpretation]):
        truth_table = list(filter(lambda interpretation:
                                  interpretation.logical_interpretation[FSM_SIGNAL_NAME] == 1, truth_table))
        truth_table = sorted(truth_table, key=lambda x: ''.join(list(map(str, x.logical_interpretation.values()))))
        pdnf = PcnfPdnfFormConverter(truth_table).pdnf
        minimizer = QuineAndCalculationMinimizer('(' + pdnf + ')')
        minimizer.minimize_func_quine_method()
        minimized_dnf = minimizer.minimized_func
        return minimized_dnf

    def print_all(self):
        print('TRANSITION TABLE'.center(27))
        print(' '.join(list(PRE_TACT_INPUT_NAMES) + [FSM_SIGNAL_NAME] + list(POST_TACT_INPUT_NAMES)
                       + list(TRIGGER_FUNCTION_NAMES)))
        for i in range(16):
            pre_tact_inputs = list('{0:03b}'.format(i // 2)[-3:])
            trigger_function_values = list(map(str, [truth_table[i].formula_value for truth_table
                                                     in self.__trigger_truth_tables.values()]))
            trigger_truth_table_inputs = list(map(str, [self.__trigger_truth_tables['H1_tt'][i].
                                                        logical_interpretation[key]
                                                        for key in [FSM_SIGNAL_NAME] + list(POST_TACT_INPUT_NAMES)]))
            print('  '.join(pre_tact_inputs + trigger_truth_table_inputs + trigger_function_values))
        print('MINIMIZED TRIGGER FUNCTIONS'.center(40))
        for trigger, minimized_func in self.minimized_trigger_funcs.items():
            print(f'{trigger}: {minimized_func}')
