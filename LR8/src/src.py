class AssociativeMemory:
    def __init__(self):
        self.__memory_table: list[list[int]] = [[0] * 16 for _ in range(16)]
        self.__is_table_diagonalized = False

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

    def __transpose_memory_table(self):
        self.__memory_table = list(map(list, zip(*self.__memory_table)))

    def __str__(self):
        return_str = f'Is memory table diagonalized: {self.__is_table_diagonalized}\n' \
                     f'{"Memory Table".center(31, " ")}'
        for word in self.__memory_table:
            return_str += '\n' + ' '.join(list(map(str, word)))
        return return_str
