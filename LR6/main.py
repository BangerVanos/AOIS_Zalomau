from src.src import HashTable
from src.cool_text_colors import BGcolors


if __name__ == '__main__':
    hash_table = HashTable(5)
    print(f'{BGcolors.OKGREEN}Test 1 - just adding{BGcolors.ENDC}'.center(25, ' '))
    hash_table['Paracetamol'] = 'John'
    hash_table['Aspirin'] = 'Ivan'
    hash_table['Mig'] = 'Mikey'
    print(hash_table)
    print(f'{BGcolors.OKGREEN}Test 2 - changing data by key{BGcolors.ENDC}'.center(25, ' '))
    hash_table['Paracetamol'] = 'Buzz'
    print(hash_table)
    print(f'{BGcolors.OKGREEN}Test 3 - deleting with existing key{BGcolors.ENDC}'.center(25, ' '))
    hash_table.delete('Paracetamol')
    print(hash_table)
    print(f'{BGcolors.OKGREEN}Test 4 - deleting with not existing key{BGcolors.ENDC}'.center(25, ' '))
    try:
        hash_table.delete('Paracetamol')
    except KeyError as err:
        print(f'{BGcolors.FAIL}KeyError: {err}{BGcolors.ENDC}')
    print(f'{BGcolors.OKGREEN}Test 5 - collision test{BGcolors.ENDC}'.center(25, ' '))
    hash_table['Syringe'] = 'Grigory'
    hash_table['Ebola'] = 'Michael'
    hash_table['Pill'] = 'Helen'
    hash_table['Lutein'] = 'Ann'
    hash_table['Лекарство'] = 'Дмитрий'
    print(hash_table)
