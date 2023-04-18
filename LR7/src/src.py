import random
from itertools import chain


class AssociativeProcessor:
    def __init__(self, word_size: int, memory_matrix_size: int):
        self.__word_size = word_size
        self.__memory_table = [['0' * word_size] * memory_matrix_size for _ in range(memory_matrix_size)]
        self.__memory_matrix_size = memory_matrix_size
        self.__fill_memory_table()

    def __fill_memory_table(self):
        for i in range(self.__memory_matrix_size):
            for j in range(self.__memory_matrix_size):
                self.__memory_table[i][j] = ''.join([str(random.randint(0, 1)) for _ in range(self.__word_size)])

    def __comparison_flags(self, memory_word: str, search_word: str, compared_digit: int = 0):
        if compared_digit > self.__word_size - 1:
            return {'g_flag': 0, 'l_flag': 0}
        memory_word_digit = bool(int(memory_word[compared_digit]))
        search_word_digit = bool(int(search_word[compared_digit]))
        return {'g_flag': self.__comparison_flags(memory_word, search_word, compared_digit + 1)['g_flag'] or
                          (not search_word_digit and memory_word_digit and not
                           self.__comparison_flags(memory_word, search_word, compared_digit + 1)['l_flag']),
                'l_flag': self.__comparison_flags(memory_word, search_word, compared_digit + 1)['l_flag'] or
                          (search_word_digit and not memory_word_digit and not
                           self.__comparison_flags(memory_word, search_word, compared_digit + 1)['g_flag'])}

    def __compare_words(self, memory_word: str, search_word: str) -> int:
        comparison_flags = self.__comparison_flags(memory_word, search_word)
        if not comparison_flags['g_flag'] and not comparison_flags['l_flag']:
            return 0
        elif comparison_flags['g_flag'] and not comparison_flags['l_flag']:
            return 1
        elif not comparison_flags['g_flag'] and comparison_flags['l_flag']:
            return -1
        else:
            raise ValueError('Flags can\'t be equal to 1 at the same time')

    def search_within_given_range(self, lower_bound: str, upper_bound: str):
        memory_table = list(chain.from_iterable(self.__memory_table))
        search_words = [word for word in memory_table if self.__compare_words(word, upper_bound) == -1]
        search_words += [word for word in memory_table if self.__compare_words(word, lower_bound) == 1]
        return search_words

    def __str__(self):
        result_str = ''
        result_str += 'Memory Table'.center(self.__memory_matrix_size * (1 + self.__word_size), ' ') + '\n'
        for memory_row in self.__memory_table:
            result_str += ' '.join(memory_row) + '\n'
        return result_str
