from src.sdbs3 import SDBS3
from src.d8421 import BinaryDecimalSynthesizer


if __name__ == '__main__':
    print('SDBS3'.center(20, '-'))
    sdbs = SDBS3()
    sdbs.print_all()
    print('D8421+n'.center(20, '-'))
    d8421_plus_one = BinaryDecimalSynthesizer(6)
    d8421_plus_one.print_all()
