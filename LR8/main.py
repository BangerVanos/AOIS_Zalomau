from src.src import AssociativeMemory
import random


if __name__ == '__main__':
    am = AssociativeMemory()
    for i in range(16):
        am.write_word(i, ''.join(list(map(str, [random.randint(0, 1) for _ in range(16)]))))
    print(am)
    for i in range(16):
        am.write_digit_col(i, am.read_digit_col(i))
    print(am)
