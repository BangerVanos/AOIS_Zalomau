import random


class AssociativeProcessor:
    def __init__(self, word_size: int, memory_matrix_size: int):
        self.__word_size = word_size
        self.__memory_table = ['0' * word_size] * memory_matrix_size
        self.__memory_matrix_size = memory_matrix_size
        self.__fill_memory_table()

    def __fill_memory_table(self):
        for i in range(self.__memory_matrix_size):
            self.__memory_table[i] = ''.join([str(random.randint(0, 1)) for _ in range(self.__word_size)])

    def __comparison_flags(self, memory_word: str, search_word: str):
        prev_g_flag, prev_l_flag = False, False
        for i in range(self.__word_size):
            memory_word_digit = bool(int(memory_word[i]))
            search_word_digit = bool(int(search_word[i]))
            next_g_flag = prev_g_flag or (not search_word_digit and memory_word_digit and not prev_l_flag)
            next_l_flag = prev_l_flag or (search_word_digit and not memory_word_digit and not prev_g_flag)
            prev_g_flag, prev_l_flag = next_g_flag, next_l_flag
        return {'g_flag': prev_g_flag,
                'l_flag': prev_l_flag}

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
        search_words = [word for word in self.__memory_table if self.__compare_words(word, upper_bound) == -1]
        search_words = list(filter(lambda word: self.__compare_words(word, lower_bound) == 1, search_words))
        return search_words

    def closest_pattern_search(self, pattern: str):
        difference_list = list()
        for word in self.__memory_table:
            difference_rank = 0
            for i in range(self.__word_size):
                difference_rank += 1 if word[i] != pattern[i] and pattern[i] != 'x' else 0
            difference_list.append((word, difference_rank))
        min_difference_rank = min([i[1] for i in difference_list])
        difference_list = list(filter(lambda x: x[1] == min_difference_rank, difference_list))
        return [i[0] for i in difference_list]

    def __str__(self):
        result_str = ''
        result_str += 'Memory Array'.center(self.__word_size, ' ') + '\n'
        for word in self.__memory_table:
            result_str += word + '\n'
        return result_str
