from src.src import AssociativeMemory
from src.cool_text_colors import BGcolors as bg
import random


def test_1():
    print(f'{bg.HEADER}Test 1. Writing|Reading words{bg.ENDC}')
    am = AssociativeMemory()
    for i in range(16):
        am.write_word(i, ''.join(list(map(str, [random.randint(0, 1) for _ in range(16)]))))
    print(am)
    for i in range(16):
        print(f'[{i}]{" " * (len(str(i)) % 2)}: {am.read_word(i)}')


def test_2():
    print(f'{bg.HEADER}Test 2. Writing|Reading digit columns{bg.ENDC}')
    am = AssociativeMemory()
    for i in range(16):
        am.write_digit_col(i, ''.join(list(map(str, [random.randint(0, 1) for _ in range(16)]))))
    print(am)
    for i in range(16):
        print(f'[{i}]{" " * (len(str(i)) % 2)}: {am.read_digit_col(i)}')


def test_3():
    print(f'{bg.HEADER}Test 3. Diagonal addressing|Reversed diagonal addressing{bg.ENDC}')
    am = AssociativeMemory()
    for i in range(16):
        am.write_word(i, ''.join(list(map(str, [random.randint(0, 1) for _ in range(16)]))))
    print(am)
    am.reverse_diagonal_addressing()
    print(am)
    am.diagonal_addressing()
    print(am)


def test_4():
    print(f'{bg.HEADER}Test 4. Logical operations on digital columns{bg.ENDC}')
    am = AssociativeMemory()
    for i in range(16):
        am.write_word(i, ''.join(list(map(str, [random.randint(0, 1) for _ in range(16)]))))
    random_cols = random.randint(0, 15), random.randint(0, 15)
    print(f'First digit column: {am.read_digit_col(random_cols[0])}\n'
          f'Second digit column: {am.read_digit_col(random_cols[1])}')
    for i in (6, 9, 4, 11):
        print(f'f{i} result: {am.logical_operation(random_cols[0], random_cols[1], logical_operation=f"f{i}")}')


def test_5():
    print(f'{bg.HEADER}Test 5. Arithmetical operation on word{bg.ENDC}')
    am = AssociativeMemory()
    for i in range(16):
        am.write_word(i, ''.join(list(map(str, [random.randint(0, 1) for _ in range(16)]))))
    random_mask = ''.join(list(map(str, [random.randint(0, 1) for _ in range(3)])))
    print(f'Random mask [{random_mask}]')
    print(f'{bg.OKCYAN}Primary words{bg.ENDC}')
    for i in range(16):
        print(f'[{i}]{" " * (len(str(i)) % 2)}: {am.read_word(i)}')
    print(f'{bg.OKCYAN}Words after arithmetical operations{bg.ENDC}')
    am.arithmetical_operation(random_mask)
    for i in range(16):
        print(f'[{i}]{" " * (len(str(i)) % 2)}: {am.read_word(i)}')


def test_6():
    print(f'{bg.HEADER}Test 6. Ordered sampling(MIN|MAX|SORT) for CPS (closest pattern search){bg.ENDC}')
    am = AssociativeMemory()
    for i in range(16):
        am.write_word(i, ''.join(list(map(str, [random.randint(0, 1) for _ in range(16)]))))
    random_pattern = ''.join([('0', '1', 'x')[random.randint(0, 2)] for _ in range(16)])
    print(f'Pattern: {random_pattern}')
    print(f'CPS result: {" ".join(am.closest_pattern_search(random_pattern))}')
    print(f'{bg.OKCYAN}MIN{bg.ENDC}')
    print(f'{am.ordered_sampling(search_mode="pattern", pattern=random_pattern, filter_mode="min")}')
    print(f'{bg.OKCYAN}MAX{bg.ENDC}')
    print(f'{am.ordered_sampling(search_mode="pattern", pattern=random_pattern, filter_mode="max")}')
    print(f'{bg.OKCYAN}SORT (no reverse){bg.ENDC}')
    print(f'{am.ordered_sampling(search_mode="pattern", pattern=random_pattern, filter_mode="sort")}')
    print(f'{bg.OKCYAN}SORT (reverse){bg.ENDC}')
    print(f'{am.ordered_sampling(search_mode="pattern", pattern=random_pattern, filter_mode="sort", reverse=True)}')


if __name__ == '__main__':
    test_1()
    test_2()
    test_3()
    test_4()
    test_5()
    test_6()
