class AssociativeMemory:
    def __init__(self):
        self.__memory_table: list[list[int]] = [[0] * 16 for _ in range(16)]
        self.__is_table_diagonalized = False
        self.logical_operations = {'unequivalence': self.__unequivalence_operation,
                                   'equivalence': self.__equivalence_operation,
                                   'second_prohibition': self.__second_prohibition,
                                   'second_to_first_implication': self.__second_to_first_implication,
                                   'f6': self.__unequivalence_operation,
                                   'f9': self.__equivalence_operation,
                                   'f4': self.__second_prohibition,
                                   'f11': self.__second_to_first_implication}

    def diagonal_addressing(self):
        if self.__is_table_diagonalized:
            return
        new_memory_table = [[0] * 16 for _ in range(16)]
        for i in range(16):
            new_word = [word[i] for word in self.__memory_table]
            new_word = self.__word_shift(new_word, i)
            new_memory_table[i] = new_word
        self.__memory_table = list(map(list, zip(*new_memory_table)))
        self.__is_table_diagonalized = True

    def reverse_diagonal_addressing(self):
        if not self.__is_table_diagonalized:
            return
        new_memory_table = [[0] * 16 for _ in range(16)]
        self.__transpose_memory_table()
        for i in range(16):
            new_memory_table[i] = self.__word_shift(self.__memory_table[i], -i)
        self.__memory_table = list(map(list, zip(*new_memory_table)))
        self.__is_table_diagonalized = False

    def read_word(self, word_index: int):
        if not self.__is_table_diagonalized:
            self.diagonal_addressing()
        optimized_table = list(map(list, zip(*self.__memory_table)))
        return_word = ''.join([str(optimized_table[i][(word_index + i) % 16]) for i in range(16)])
        return return_word

    def write_word(self, word_index: int, word: str):
        if len(word) < 16 or len(word) > 16:
            raise ValueError('Word length must be equal to 16')
        if not self.__is_table_diagonalized:
            self.diagonal_addressing()
        optimized_word_representation = list(map(int, list(word)))
        optimized_table = list(map(list, zip(*self.__memory_table)))
        for i in range(16):
            optimized_table[i][(word_index + i) % 16] = optimized_word_representation[i]
        self.__memory_table = list(map(list, zip(*optimized_table)))

    def read_digit_col(self, digit_col_index: int):
        if not self.__is_table_diagonalized:
            self.diagonal_addressing()
        optimized_table = list(map(list, zip(*self.__memory_table)))
        return ''.join(list(map(str, self.__word_shift(optimized_table[digit_col_index], -digit_col_index))))

    def write_digit_col(self, digit_col_index: int, digit_col: str):
        if len(digit_col) < 16 or len(digit_col) > 16:
            raise ValueError('Digit column length must be equal to 16')
        if not self.__is_table_diagonalized:
            self.diagonal_addressing()
        optimized_col_representation = list(map(int, list(digit_col)))
        optimized_table = list(map(list, zip(*self.__memory_table)))
        optimized_col_representation = self.__word_shift(optimized_col_representation, digit_col_index)
        optimized_table[digit_col_index] = optimized_col_representation
        self.__memory_table = list(map(list, zip(*optimized_table)))

    @staticmethod
    def __word_shift(word: list[int], shift: int):
        shift = shift % 16
        return word[-shift:] + word[:-shift]

    def logical_operation(self, first_digit_col_index: int, second_digit_col_index: int, logical_operation: str) -> str:
        first_digit_col: list[int] = list(map(int, list(self.read_digit_col(first_digit_col_index))))
        second_digit_col: list[int] = list(map(int, list(self.read_digit_col(second_digit_col_index))))
        operation_result: list[int] = list()
        for i in range(16):
            x1, x2 = first_digit_col[i], second_digit_col[i]
            operation_result.append(self.logical_operations[logical_operation](x1, x2))
        return ''.join(list(map(str, operation_result)))

    @staticmethod
    def __unequivalence_operation(x1: int, x2: int) -> int:
        return int((not x1 and x2) or (x1 and not x2))

    @staticmethod
    def __equivalence_operation(x1: int, x2: int) -> int:
        return int((x1 and x2) or (not x1 and not x2))

    @staticmethod
    def __second_prohibition(x1: int, x2: int) -> int:
        return int(not x1 and x2)

    @staticmethod
    def __second_to_first_implication(x1: int, x2: int) -> int:
        return int(x1 or not x2)

    def arithmetical_operation(self, mask: str):
        for i in range(16):
            word = self.read_word(i)
            if word[:3] == mask:
                field_a, field_b = word[3:7], word[7:11]
                word = word[:11] + self.__full_number_addition(field_a, field_b)
                self.write_word(i, word)

    @staticmethod
    def __full_number_addition(first_number: str, second_number: str) -> str:
        first_number = list(map(int, first_number))
        second_number = list(map(int, second_number))
        result, carry = '', 0
        for fi, si in zip(first_number, second_number):
            result = str(int(fi ^ si ^ carry)) + result
            carry = int((fi and si) or (fi and carry) or (fi and carry))
        result = str(carry) + result
        return result

    @staticmethod
    def __comparison_flags(memory_word: str, search_word: str):
        prev_g_flag, prev_l_flag = False, False
        for i in range(16):
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
        search_words = [self.read_word(i) for i in range(16) if self.__compare_words(self.read_word(i),
                                                                                     upper_bound) == -1]
        search_words = list(filter(lambda word: self.__compare_words(word, lower_bound) == 1, search_words))
        return search_words

    def closest_pattern_search(self, pattern: str):
        difference_list = list()
        for i in range(16):
            difference_rank = 0
            word = self.read_word(i)
            for j in range(16):
                difference_rank += 1 if word[j] != pattern[j] and pattern[j] != 'x' else 0
            difference_list.append((word, difference_rank))
        min_difference_rank = min([i[1] for i in difference_list])
        difference_list = list(filter(lambda x: x[1] == min_difference_rank, difference_list))
        return [i[0] for i in difference_list]

    def ordered_sampling(self, **kwargs):
        primary_results: list[str] = list()
        if kwargs['search_mode'] == 'range':
            primary_results = self.search_within_given_range(kwargs['lower_bound'], kwargs['upper_bound'])
        elif kwargs['search_mode'] == 'pattern':
            primary_results = self.closest_pattern_search(kwargs['pattern'])
        if kwargs['filter_mode'] == 'sort':
            return sorted(primary_results, reverse=kwargs['reverse'])
        elif kwargs['filter_mode'] in ('min', 'max'):
            return self.__find_extremum_in_word_sequence(primary_results, kwargs['filter_mode'])

    def __find_extremum_in_word_sequence(self, sequence: list[str], mode: str = 'min'):
        extremum_word = '0' * 16
        result_sequence: list[str] = list()
        for word in sequence:
            if self.__compare_words(word, extremum_word) == {'min': -1, 'max': 1}[mode]:
                extremum_word = word
                result_sequence.clear()
            if self.__compare_words(word, extremum_word) == 0:
                result_sequence.append(word)
        return result_sequence

    def __transpose_memory_table(self):
        self.__memory_table = list(map(list, zip(*self.__memory_table)))

    def __str__(self):
        return_str = f'Is memory table diagonalized: {self.__is_table_diagonalized}\n' \
                     f'{"Memory Table".center(31, " ")}'
        for word in self.__memory_table:
            return_str += '\n' + ' '.join(list(map(str, word)))
        return return_str
